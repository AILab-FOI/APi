#!/usr/bin/env python3

from version import __version__

import sys
import errno
import os
from time import sleep
from itertools import tee, cycle
from uuid import uuid4
import subprocess as sp
import shlex
import pty
import re
import tempfile
from threading import Thread

file_re = re.compile( r'FILE (.*)' )
http_re = re.compile( r'HTTP (.*)' )
ws_re  = re.compile( r'WS (.*)' )
netcat_re = re.compile( r'NETCAT (.*)[:]([0-9]+)(?:[:](udp))?' )

delimiter_re = re.compile( r'DELIMITER (.*)' )
time_re = re.compile( r'TIME ([0-9.]+)' )
size_re = re.compile( r'SIZE ([0-9]+)' )
regex_re = re.compile( r'REGEX .*' )

NIE = 'Sorry, it is planned, I promise ;-)'

TMP_FOLDER = '/tmp/APi/'

from APiLexer import APiLexer
from APiListener import APiListener
from APiParser import APiParser
from antlr4 import *

from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade

import requests
# When using HTTPS with insecure servers this has to be uncommented
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import asyncio
import websockets
import nclib
    
def error( *msg ):
    '''Function for printing error messages'''
    print( 'ERROR:', *msg )

def pairwise( iterable ):
    '''
    Unpack an iterable to zipped pairs.
    Stolen from: 
    https://docs.python.org/3/library/itertools.html
    '''
    a, b = tee( iterable )
    next( b, None )
    return zip( a, b )

def output_fifo( FIFO ):
    '''
    Generator function to create a named pipe (FIFO) that will
    yield the output of a service (agent). Only to be used by
    the service_output function.
    '''
    try:
        os.mkfifo( FIFO )
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    while True:
        with open( FIFO ) as fifo:
            while True:
                data = fifo.readline()
                print( 'Output-fifo: Received', data )
                if len( data ) == 0:
                    fifo.close()
                    raise StopIteration
                yield data

def input_fifo( FIFO, DATA ):
    '''
    Input function that inputs DATA into a given named pipe
    (FIFO). Only to be used by the service_input function. 
    '''

    try:
        data = FIFO.write( DATA )
        FIFO.flush()
    except Exception as e:
        print( e, DATA )
    
def agent_fifo( cmd, fifo_in=None, fifo_out=None, infile=None ):
    '''
    Wrapper function around Unix filter (given in CMD). Redirects 
    input from named pipe (FIFO_IN) xor file (INFILE) to filter's 
    STDIN and filter's STDOUT to named pipe (FIFO_OUT).
    '''
    if fifo_in:
        cmd = 'cat %s | ' % fifo_in + cmd
        if infile:
            err = 'Agent cannot recieve data from both fifo (%s) and file (%s).' % ( fifo_in, infile )
            raise APiCommunicationError( err )
    if infile:
        cmd = 'cat %s | ' % infile + cmd
    if fifo_out:
        cmd = cmd + ' | cat > %s' % fifo_out
    print( 'Agent-fifo: Starting', cmd )
    os.system( cmd )

def service_input( data, fifo_in=None ):
    '''
    Service input function (must be called in separate thread).
    Argument data is a chunk of data to be written to the services
    STDIN.
    If fifo_in is specified it will create a named pipe, open it 
    and write the data to the pipe.
    '''
    if fifo_in:
        try:
            os.mkfifo( fifo_in )
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        
            fifo = open( fifo_in, mode='w' )
            print( 'Service-input: Writing', data )
            input_fifo( fifo, data )
            fifo.close()
    
    

def service_output( callback, fifo_out ):
    '''
    Service output function (must be called in separate thread).
    Callback function is called for any output line returned by 
    the current started service (agent).
    '''
    try:
        for i in output_fifo( fifo_out ):
            print( 'Service-output: Got', i )
            callback( i )
    except ( RuntimeError, StopIteration ):
        pass

    
class APiIOError( IOError ):
    '''Exception thrown when a file (usually agent definition) is not present.'''
    pass

class APiCommunicationError( IOError ):
    '''
    Exception thrown when there is a communication error (e.g. someone tries to
    write to and agent that does not accept input on this channel.
    '''
    pass

class APiAgentDefinitionError( Exception ):
    '''Exception thrown when an agent definition file is not parsable.'''
    pass

class APiHolonConfigurationError( Exception ):
    '''Exception thrown when a holon configuration file is not parsable.'''
    pass

class XMPPRegisterException( Exception ):
    '''Exception thrown when the system cannot register at a XMPP registration service'''
    pass

class APiBaseAgent( Agent ):
    '''
    Base agent (auxilliary methods and behaviours for all other
    types of agents
    '''
    def say( self, *msg ):
        print( '%s:' % self.name, *msg )

    # Add stopping behaviour on message

class APiChannel( APiBaseAgent ):
    '''Channel agent.'''
    def __init__( self, channelname, name, password, inputs, outputs ):
        self.channelname = channelname
        super().__init__( name, password )
        self.inputs = inputs
        self.outputs = outputs

class APiAgent( APiBaseAgent ):
    '''Service wrapper agent.'''
    def __init__( self, agentname, name, password, args=[], flows=[] ):
        try:
            fh = open( agentname + '.ad' )
        except IOError as e:
            err = 'Missing agent definition file or permission issue.\n' + str( e )
            raise APiIOError( err )
        super().__init__( name, password )
        self.agentname = agentname
        self._load( fh )
        self.agentargs = args

        self.flows = []
        for f in flows:
            if len( f ) > 2:
                pairs = [ i for i in pairwise( f ) ]
                self.flows.extend( pairs )
            else:
                self.flows.append( f )
        
        self.input_channels = set( i[ 0 ] for i in flows )
        self.output_channels = set( i[ 1 ] for i in flows )

    def _load( self, fh ):
        try:
            self.descriptor = load( fh.read(), Loader )
        except Exception as e:
            err = 'Agent definition file cannot be loaded.\n' + str( e )
            raise APiAgentDefinitionError( err )
        if self.agentname != self.descriptor[ 'agent' ][ 'name' ]:
            err = 'Name in agent definition file does not match file name: %s != %s !' % ( self.agentname, self.descriptor[ 'agent' ][ 'name' ] )
            raise APiAgentDefinitionError( err )
        try:
            self.description = self.descriptor[ 'agent' ][ 'description' ]
            self.type = self.descriptor[ 'agent' ][ 'type' ]
            self.input_type = self.descriptor[ 'agent' ][ 'input' ][ 'type' ]
            self.input_data_type = self.descriptor[ 'agent' ][ 'input' ][ 'data-type' ]
            self.input_fmt = self.descriptor[ 'agent' ][ 'input' ][ 'fmt' ]
            self.input_cutoff = self.descriptor[ 'agent' ][ 'input' ][ 'cutoff' ]
            self.input_end = self.descriptor[ 'agent' ][ 'input' ][ 'end' ]
            self.input_value_type = self.descriptor[ 'agent' ][ 'input' ][ 'value-type' ]
            self.output_type = self.descriptor[ 'agent' ][ 'output' ][ 'type' ]
            self.output_data_type = self.descriptor[ 'agent' ][ 'output' ][ 'data-type' ]
            self.output_fmt = self.descriptor[ 'agent' ][ 'output' ][ 'fmt' ]
            self.output_cutoff = self.descriptor[ 'agent' ][ 'output' ][ 'cutoff' ]
            self.output_end = self.descriptor[ 'agent' ][ 'output' ][ 'end' ]
            self.output_value_type = self.descriptor[ 'agent' ][ 'output' ][ 'value-type' ]
        except Exception as e:
            err = 'Agent definition file is invalid.\n' + str( e )
            raise APiAgentDefinitionError( err )

        if self.type == 'unix':
            # only for testing, need to filter by agent definition (e.g. data-type, fmt etc)
            self.cmd = self.descriptor[ 'agent' ][ 'start' ]
            self.fifo_in = None
            self.fifo_out = None
            self.input_file_path = None
            self.input_delimiter = None
            self.http_proc = None
            self.ws_proc = None
            self.nc_proc = None
            self.agent_thread = None
            self.output_thread = None
            # TODO: Put fifo_out into self.process_output()
            self.fifo_out = TMP_FOLDER + next( tempfile._get_candidate_names() )
            try:
                self.process_input()
            except Exception as e:
                err = 'Agent definition file is invalid.\n' + str( e )
                raise APiAgentDefinitionError( err )
            

            
            self.output_thread = Thread( target=service_output, args=( self.output_callback, self.fifo_out ) )
            self.threads_started = False
            self.threads = []

            
        elif self.type == 'docker':
            raise NotImplementedError( NIE )
        elif self.type == 'kubernetes':
            raise NotImplementedError( NIE )
        else:
            err = 'Invalid agent type: %s' % self.type
            raise APiAgentDefinitionError( err )
            
        
        self.say( self.descriptor )

    def input_file( self, data ):
        if self.input_file_written:
            err = 'Agent %s cannot write multiple times to input file "%s".' % ( self.name, self.input_file_path )
            raise APiCommunicationError( err )
        if self.input_value_type == 'BINARY':
            data = data.encode( 'utf-8' )
        fh = open( self.input_file_path, 'w' )
        fh.write( data )
        fh.close()
        self.input_file_written = True
        if not self.threads_started:
            self.output_thread.start()
            sleep( 0.1 )
            self.agent_thread.start()
            self.threads_started = True
        self.service_quit( 'Input file written, quitting!' )

    def input_stdin( self, data ):
        if data == self.input_end:
            self.service_quit( 'Got end delimiter on STDIN, quitting!' )
            return None
        if self.input_value_type == 'BINARY':
            data = data.encode( 'utf-8' )
        t = Thread( target=service_input, args=( data, ), kwargs={ 'fifo_in':self.fifo_in } )
        t.start()
        self.threads.append( t )
        if not self.threads_started:
            self.output_thread.start()
            sleep( 0.1 )
            self.agent_thread.start()
            self.threads_started = True

    def input_http( self, data ):
        if self.input_value_type == 'BINARY':
            data = data.encode( 'utf-8' )
        if self.input_delimiter:
            inp = [ i for i in data.split( self.input_delimiter ) if i != '' ]
        else:
            imp = [ data ]
        for d in inp:
            if d == self.input_end:
                self.service_quit( 'Received end delimiter, shutting down HTTP server!' )
                return
            url = self.http_url + d
            error = True
            while error:
                try:
                    response = requests.get( url, verify=False )
                    result = response.content.decode( 'utf-8' )
                    # TODO: define different outputs based on agent definition
                    self.output_callback( result )
                    error = False
                except Exception as e:
                    sleep( 0.2 )

    def input_ws( self, data ):
        if self.input_value_type == 'BINARY':
            data = data.encode( 'utf-8' )
        if self.input_delimiter:
            inp = [ i for i in data.split( self.input_delimiter ) if i != '' ]
        else:
            imp = [ data ]
        for i in inp:
            if i == self.input_end:
                self.service_quit( 'Received end delimiter, shutting down WebSocket server!' )
                return
            asyncio.get_event_loop().run_until_complete( self.ws( i ) )
        
    async def ws( self, msg ):
        error = True
        while error:
            try:
                async with websockets.connect( self.ws_url ) as websocket:
                    await websocket.send( msg )
                    resp = await websocket.recv()
                    self.output_callback( resp )
                    error = False
            except Exception as e:
                sleep( 0.2 )

    def input_nc( self, data ):
        if self.input_value_type == 'BINARY':
            data = data.encode( 'utf-8' )
        if data == self.input_end:
            self.service_quit( 'Got end delimiter, quitting NETCAT!' )
            return None
        if self.input_delimiter:
            inp = [ i for i in data.split( self.input_delimiter ) if i != '' ]
        else:
            imp = [ data ]
        sleep( 0.1 )
        try:
            nc = nclib.Netcat( ( self.nc_host, self.nc_port ), udp=self.nc_udp )
        except Exception as e:
            self.service_quit( 'NETCAT process ended, quitting!' )
            return None
        for i in inp:
            nc.send( data )

        sleep( 0.1 )
        res = nc.recv().decode( 'utf-8' )
        nc.close()
        # TODO: if self.output_delimiter: ...
        delimiter = '\n'
        out = [ i for i in res.split( delimiter ) if i != '' ]
        for i in out:
            self.output_callback( i )

            
            

    def output_callback( self, data ):
        self.say( 'I just received:', data )

    def service_quit( self, msg ):
        sleep( 0.5 )
        self.say( msg ) # firstly need to clean up and finish all threads
        for t in self.threads:
            t.join( timeout=2 )
            # Not sure if timeout should be used here to force joining.
            # Some input threads hang sometimes and never send the data.
            #print( 'Joined!' )

        try:
            if self.agent_thread.alive():
                self.agent_thread.join()
            if self.output_thread.alive():
                self.output_thread.join()
        except:
            pass

        if self.http_proc:
            self.http_proc.terminate()

        if self.ws_proc:
            self.ws_proc.terminate()

        if self.nc_proc:
            self.nc_proc.terminate()
        
        if self.fifo_in:
            os.remove( self.fifo_in )
        if self.fifo_out:
            try:
                os.remove( self.fifo_out )
            except:
                pass # TODO: remove try/except when output processing is finished

    def process_input( self ):
        if self.input_type == 'STDIN':
            self.fifo_in = TMP_FOLDER + next( tempfile._get_candidate_names() )
            self.input = self.input_stdin
            self.agent_thread = Thread( target=agent_fifo, args=( self.cmd, ), kwargs={ 'fifo_in':self.fifo_in, 'fifo_out':self.fifo_out  } )
        elif self.input_type[ :4 ] == 'FILE':
            fl = file_re.findall( self.input_type )[ 0 ]
            self.input_file_path = fl
            self.input_file_written = False
            self.input = self.input_file
            self.agent_thread = Thread( target=agent_fifo, args=( self.cmd, ), kwargs={ 'infile':self.input_file_path, 'fifo_out':self.fifo_out  } )
        elif self.input_type[ :4 ] == 'HTTP':
            cmd = shlex.split( self.cmd + ' > /dev/null 2>&1 &' )
            self.http_proc = sp.Popen( cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL )
            url = http_re.findall( self.input_type )[ 0 ]
            self.http_url = url
            self.input = self.input_http
        elif self.input_type[ :2 ] == 'WS':
            url = ws_re.findall( self.input_type )[ 0 ]
            cmd = shlex.split( self.cmd + ' > /dev/null 2>&1 &' )
            self.ws_proc = sp.Popen( cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL )
            self.ws_url = url
            self.input = self.input_ws
        elif self.input_type[ :6 ] == 'NETCAT':
            host, port, udp = netcat_re.findall( self.input_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''
            cmd = '%s > /dev/null 2>&1 &' % self.cmd
            os.system( cmd )
            self.input = self.input_nc
        else:
            err = 'Invalid input type "%s"\n' % self.input_type
            raise APiAgentDefinitionError( err )

        if self.input_value_type not in [ 'STRING', 'BINARY' ]:
            err = 'Invalid input value type "%s"\n' % self.input_value_type
            raise APiAgentDefinitionError( err )

        if self.input_data_type == 'ONEVALUE':
            pass
        elif self.input_data_type == 'STREAM':
            if self.input_cutoff[ :4 ] == 'TIME':
                time = float( time_re.findall( self.input_cutoff )[ 0 ] )
                print( time )
                raise NotImplementedError( NIE )                
            elif self.input_cutoff[ :4 ] == 'SIZE':
                size = int( size_re.findall( self.input_cutoff )[ 0 ] )
                print( size )
                raise NotImplementedError( NIE ) 
            elif self.input_cutoff[ :9 ] == 'DELIMITER':
                self.input_delimiter = delimiter_re.findall( self.input_cutoff )[ 0 ]
                if self.input_delimiter == 'NEWLINE':
                    self.input_delimiter = '\n'               
            elif self.input_cutoff[ :5 ] == 'REGEX':
                regex = int( regex_re.findall( self.input_cutoff )[ 0 ] )
                print( regex )
                raise NotImplementedError( NIE ) 
            else:
                err = 'Invalid input data type "%s"\n' % self.input_data_type
                raise APiAgentDefinitionError( err )

class APiHolon( APiBaseAgent ):
    '''A holon created by another api file.'''
    def __init__( self, holonname, name, password ):
        super().__init__( name, password )
        self.holonname = holonname

class APiRegistrationService:
    '''
    Registration service which generates unique agent names
    and registers them on XMPP server(s) according to rules
    given in config file.
    '''
    def __init__( self, holonname ):
        self.name = holonname
        try:
            fh = open( holonname + '.cfg' )
        except IOError as e:
            err = 'Missing holon configuration file or permission issue.\n' + str( e )
            raise APiIOError( err )
        self.services = []
        self._load( fh )
        self.next = lambda: cycle( self.services ).__next__()
        self.MAX_RETRIES = 4

    def _load( self, fh ):
        try:
            self.descriptor = load( fh.read(), Loader )
        except Exception as e:
            err = 'Holon configuration file cannot be loaded.\n' + str( e )
            raise APiHolonConfigurationError( err )
        try:
            self.services = self.descriptor[ 'registration-services' ]
        except Exception as e:
            err = 'Holon configuration file has invalid format.\n' + str( e )
            raise APiHolonConfigurationError( err )
        if not self.services:
            err = 'Holon configuration file does not list any services.'
            raise APiHolonConfigurationError( err )
        
    def register( self, name ):
        server = self.next()
        username = '%s_%s_%s' % ( self.name, name, str( uuid4().hex ) )
        password = str( uuid4().hex )
        url = "http://%s/register/%s/%s" % ( server, username, password )
        response = requests.get( url, verify=False )

        if response.status_code == 200:
            result = response.content.decode('utf-8')
            if result == 'OK':
                return ( username, password )
            else:
                for i in range( self.MAX_RETRIES ):
                    response = requests.get( url, verify=False )
                    result = response.content.decode('utf-8')
                    if result == 'OK':
                        return ( username, password )
                raise XMPPRegisterException( 'Cannot register agent "%s" after %d retries, giving up. Error from server: %s' % ( username, self.MAX_RETRIES, result ) )
        else:
            raise XMPPRegisterException( 'Error while communicating with server at "%s"' % server )

class APiNamespace( dict ):
    '''
    APi namespace class to keep track of various agent, channel,
    environment and holon identifiers.
    '''
    def __init__( self, *args, **kwargs ):
        self[ 'agents' ] = {}
        self[ 'channels' ] = {}
        self[ 'environment' ] = {}
        self[ 'holons' ] = {}

class APi( APiListener ):
    '''
    APi main listener.
    '''
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.ns = APiNamespace()

    # Enter a parse tree produced by APiParser#api_program.
    def enterApi_program(self, ctx:APiParser.Api_programContext):
        pass

    # Exit a parse tree produced by APiParser#api_program.
    def exitApi_program(self, ctx:APiParser.Api_programContext):
        pass


    # Enter a parse tree produced by APiParser#s_environment.
    def enterS_environment(self, ctx:APiParser.S_environmentContext):
        pass

    # Exit a parse tree produced by APiParser#s_environment.
    def exitS_environment(self, ctx:APiParser.S_environmentContext):
        pass


    # Enter a parse tree produced by APiParser#ioflow.
    def enterIoflow(self, ctx:APiParser.IoflowContext):
        pass

    # Exit a parse tree produced by APiParser#ioflow.
    def exitIoflow(self, ctx:APiParser.IoflowContext):
        pass


    # Enter a parse tree produced by APiParser#s_start.
    def enterS_start(self, ctx:APiParser.S_startContext):
        print( "It's a start..." )
        pass

    # Exit a parse tree produced by APiParser#s_start.
    def exitS_start(self, ctx:APiParser.S_startContext):
        pass


    # Enter a parse tree produced by APiParser#pi_expr.
    def enterPi_expr(self, ctx:APiParser.Pi_exprContext):
        pass

    # Exit a parse tree produced by APiParser#pi_expr.
    def exitPi_expr(self, ctx:APiParser.Pi_exprContext):
        pass


    # Enter a parse tree produced by APiParser#s_agent.
    def enterS_agent(self, ctx:APiParser.S_agentContext):
        pass

    # Exit a parse tree produced by APiParser#s_agent.
    def exitS_agent(self, ctx:APiParser.S_agentContext):
        pass


    # Enter a parse tree produced by APiParser#arglist.
    def enterArglist(self, ctx:APiParser.ArglistContext):
        pass

    # Exit a parse tree produced by APiParser#arglist.
    def exitArglist(self, ctx:APiParser.ArglistContext):
        pass


    # Enter a parse tree produced by APiParser#flow.
    def enterFlow(self, ctx:APiParser.FlowContext):
        pass

    # Exit a parse tree produced by APiParser#flow.
    def exitFlow(self, ctx:APiParser.FlowContext):
        pass


    # Enter a parse tree produced by APiParser#valid_channel.
    def enterValid_channel(self, ctx:APiParser.Valid_channelContext):
        pass

    # Exit a parse tree produced by APiParser#valid_channel.
    def exitValid_channel(self, ctx:APiParser.Valid_channelContext):
        pass


    # Enter a parse tree produced by APiParser#s_channel.
    def enterS_channel(self, ctx:APiParser.S_channelContext):
        pass

    # Exit a parse tree produced by APiParser#s_channel.
    def exitS_channel(self, ctx:APiParser.S_channelContext):
        pass


    # Enter a parse tree produced by APiParser#s_channel_spec.
    def enterS_channel_spec(self, ctx:APiParser.S_channel_specContext):
        pass

    # Exit a parse tree produced by APiParser#s_channel_spec.
    def exitS_channel_spec(self, ctx:APiParser.S_channel_specContext):
        pass


    # Enter a parse tree produced by APiParser#s_import.
    def enterS_import(self, ctx:APiParser.S_importContext):
        pass

    # Exit a parse tree produced by APiParser#s_import.
    def exitS_import(self, ctx:APiParser.S_importContext):
        pass


    # Enter a parse tree produced by APiParser#json.
    def enterJson(self, ctx:APiParser.JsonContext):
        pass

    # Exit a parse tree produced by APiParser#json.
    def exitJson(self, ctx:APiParser.JsonContext):
        pass


    # Enter a parse tree produced by APiParser#obj.
    def enterObj(self, ctx:APiParser.ObjContext):
        pass

    # Exit a parse tree produced by APiParser#obj.
    def exitObj(self, ctx:APiParser.ObjContext):
        pass


    # Enter a parse tree produced by APiParser#pair.
    def enterPair(self, ctx:APiParser.PairContext):
        pass

    # Exit a parse tree produced by APiParser#pair.
    def exitPair(self, ctx:APiParser.PairContext):
        pass


    # Enter a parse tree produced by APiParser#arr.
    def enterArr(self, ctx:APiParser.ArrContext):
        pass

    # Exit a parse tree produced by APiParser#arr.
    def exitArr(self, ctx:APiParser.ArrContext):
        pass


    # Enter a parse tree produced by APiParser#value.
    def enterValue(self, ctx:APiParser.ValueContext):
        pass

    # Exit a parse tree produced by APiParser#value.
    def exitValue(self, ctx:APiParser.ValueContext):
        pass




'''
Penguin ASCII art by apx stolen from:
http://www.ascii-art.de/ascii/pqr/penguins.txt
'''

splash = '''
                             ;
                         ('>-'
                        //-\\
                        (\_/)
                         ~ ~  
------------------------------------------------------------
Awkward π-nguin %s : Microservice orchestration language
------------------------------------------------------------
''' % __version__

def process( stream ):
    lexer = APiLexer( stream )
    lexer.recover = lambda x: sys.exit()
    stream = CommonTokenStream( lexer )
    parser = APiParser( stream )
    tree = parser.api_program()
    printer = APi()
    walker = ParseTreeWalker()
    walker.walk( printer, tree )
    
            
def main():
    if len( sys.argv ) > 2:
        print( 'Usage: APi [filename.api]' )
    else:
        if len( sys.argv ) == 2:
            fl = sys.argv[ 1 ]
            stream = FileStream( fl, encoding='utf-8' )
            process( stream )            
        else:
            print( splash )
            while True:
                try:
                    command = input( "Aπ :- " )
                except:
                    print( '\nBye!' )
                    quit_spade()
                    sys.exit()
                
                if command == "exit":
                    print( 'Bye!' )
                    quit_spade()
                    break
                elif command == '':
                    continue
                elif command.strip()[ -1 ] == ':':
                    line = input( '|' )
                    command += '\n' + line
                    while line[ 0 ] == '\t':
                        line = input( '|' )
                        command += '\n' + line
                        if not line:
                            break
                    
                else:
                    stream = InputStream( command + '\n' )
                    process( stream )

def initialize():
    if not os.path.exists( TMP_FOLDER ):
        os.makedirs( TMP_FOLDER )
                    
if __name__ == '__main__':
    initialize()
    ns = APiNamespace()
    '''
    try:
        a = APiAgent( 'bla0', 'bla0agent@dragon.foi.hr', 'tajna', flows=[ (1, 2), (3, 4), (1, 5), (3, 6), (1, 3, 5, 7) ] )
    except Exception as e:
        error( e )
    '''
    os.chdir('test')
    '''rs = APiRegistrationService( 'APi-test' )
    rs.register( 'ivek' )'''

    a = APiAgent( 'bla_nc', 'bla0agent@dragon.foi.hr', 'tajna', flows=[ (1, 2), (3, 4), (1, 5), (3, 6), (1, 3, 5, 7) ] )

    a.input( 'avauhu\nguhu\nbuhu\nwuhu\ncuhu\n' )
    
    a.input( 'juhu\n' )
    a.input( 'muhu\n' )
    a.input( 'ahu\n' )
    a.input( 'puhu\nluhu\n' )
    a.input( '<!eof!>' )
    
    print( ns )
    main()

