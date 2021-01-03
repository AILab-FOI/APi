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
http_re = re.compile( r'HTTP (.*):([0-9]+)' )
ws_re  = re.compile( r'WS (.*):([0-9]+)' )
netcat_re = re.compile( r'NETCAT (.*)' )

delimiter_re = re.compile( r'DELIMITER (.*)' )
time_re = re.compile( r'TIME ([0-9.]+)' )
size_re = re.compile( r'SIZE ([0-9]+)' )
regex_re = re.compile( r'REGEX .*' )

NIE = 'Sorry, it is planned, I promise ;-)'

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
        #print( "Output: Opening FIFO..." )
        with open( FIFO ) as fifo:
            #print( "Output: FIFO opened" )
            while True:
                data = fifo.readline()
                if len( data ) == 0:
                    #print( "Output: Writer closed ")
                    return
                #print( 'Output: read -> "{0}"'.format( data ) )
                yield data

def input_fifo( FIFO, DATA ):
    '''
    Input function that inputs DATA into a given named pipe
    (FIFO). Only to be used by the service_input function. 
    '''
    #print( 'Input: data is', DATA )

    try:
        #print( "Input: FIFO opened" )
        try:
            data = FIFO.write( DATA )
        except Exception as e:
            print( e, DATA )
        #print('Input: wrote -> "{0}"'.format( DATA ) )
    except Exception as e:
        #print( e )
        pass

def agent_fifo( FIFO_IN, FIFO_OUT, CMD ):
    '''
    Wrapper function around Unix filter (given in CMD). Redirects 
    input from named pipe (FIFO_IN) to filter's STDIN and filter's 
    STDOUT to named pipe (FIFO_OUT).
    '''
    cmd = 'cat %s | ' % FIFO_IN + CMD + ' | cat > %s' % FIFO_OUT
    #print( 'Agent:', cmd )
    os.system( cmd )

'''    
fifo_in = '/tmp/APi/' + next( tempfile._get_candidate_names() ) 
fifo_out = '/tmp/APi/' + next( tempfile._get_candidate_names() )

cmd = 'sort | grep bla | wc'
cmd = 'grep bla'
data = [ 'bla %d\n' % i for i in range( 100 ) ]
data = 'bla\nhshsbla\n'
'''

def service_input( data, fifo_in ):
    '''
    Service input function (must be called in separate thread).
    Argument data is a chunk of data to be written to the services
    STDIN.
    '''
    try:
        os.mkfifo( fifo_in )
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    fifo = open( fifo_in, mode='w' )
    input_fifo( fifo, data )
    
    

def service_output( callback, fifo_out ):
    '''
    Service output function (must be called in separate thread).
    Callback function is called for any output line returned by 
    the current started service (agent).
    '''
    for i in output_fifo( fifo_out ):
        callback( i )

'''
t1 = Thread( target=service_input, args=( data, fifo_in ) )
t4 = Thread( target=service_input, args=( 'bababla\nhhdhd\nblabla\n', ) )        
t2 = Thread( target=agent_fifo, args=( fifo_in, fifo_out, cmd ) )
t3 = Thread( target=service_output, args=( print, fifo_out ) )


t2.start()

t3.start()

t1.start()
t4.start()


#t1.join()

#t2.join()

#t3.join()
'''


    
class APiIOError( IOError ):
    '''Exception thrown when a file (usually agent definition is not present.'''
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

            try:
                self.process_input()
            except Exception as e:
                err = 'Agent definition file is invalid.\n' + str( e )
                raise APiAgentDefinitionError( err )
            

            self.fifo_in = '/tmp/APi/' + next( tempfile._get_candidate_names() )
            self.fifo_out = '/tmp/APi/' + next( tempfile._get_candidate_names() )
            
            self.agent_thread = Thread( target=agent_fifo, args=( self.fifo_in, self.fifo_out, self.cmd ) )
            self.output_thread = Thread( target=service_output, args=( self.output_callback, self.fifo_out ) )

            self.output_thread.start()
            self.agent_thread.start()

            self.threads = []

            self.input = self.input_unix
            self.output = lambda: print( 'njanjanjanjanjanja' )
            
        elif self.type == 'docker':
            raise NotImplementedError( NIE )
        elif self.type == 'kubernetes':
            raise NotImplementedError( NIE )
        else:
            err = 'Invalid agent type: %s' % self.type
            raise APiAgentDefinitionError( err )
            
        
        self.say( self.descriptor )

    def input_unix( self, data ):
        if data == self.input_end:
            self.service_quit()
            return None
        if self.input_value_type == 'BINARY':
            data = data.encode( 'utf-8' )
        t = Thread( target=service_input, args=( data, self.fifo_in ) )
        t.start()
        self.threads.append( t )
            

    def output_callback( self, data ):
        self.say( 'I just received:', data )

    def output_unix( self ):
        print( 'Reading data' )
        data = self.fifo_out.read()
        print( data, '... Done!' )
        if len( data ) == 0:
            return None # Process has finished
        else:
            return data

    def service_quit( self ):
        self.say( 'Got end delimiter, quitting!' ) # firstly need to clean up and finish all threads
        for t in self.threads:
            #print( t, t.is_alive() )
            t.join( timeout=2 )
            # Not sure if timeout should be used here to force joining.
            # Some input threads hang sometimes and never send the data.
            #print( 'Joined!' )
        self.agent_thread.join()
        self.output_thread.join()

    def process_input( self ):
        if self.input_type == 'STDIN':
            inp_pipe = sp.PIPE
        elif self.input_type[ :4 ] == 'FILE':
            fl = file_re.findall( self.input_type )[ 0 ]
            inp_pipe = open( fl )
        elif self.input_type[ :4 ] == 'HTTP':
            host, port = http_re.findall( self.input_type )[ 0 ]
            print( host, port )
            raise NotImplementedError( NIE )
        elif self.input_type[ :2 ] == 'WS':
            host, port = ws_re.findall( self.input_type )[ 0 ]
            print( host, port )
            raise NotImplementedError( NIE )
        elif self.input_type[ :6 ] == 'NETCAT':
            cmd = netcat_re.findall( self.input_type )[ 0 ]
            print( cmd )
            raise NotImplementedError( NIE )
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
                delimiter = delimiter_re.findall( self.input_cutoff )[ 0 ]
                print( delimiter )
                if delimiter == 'NEWLINE':
                    delimiter = '\n'               
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

if __name__ == '__main__':
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

    a = APiAgent( 'bla0', 'bla0agent@dragon.foi.hr', 'tajna', flows=[ (1, 2), (3, 4), (1, 5), (3, 6), (1, 3, 5, 7) ] )


    a.input( 'juhu\n' )
    a.input( 'muhu\n' )
    a.input( 'ahu\n' )
    a.input( 'puhu\nluhu\n' )
    a.input( 'avauhu\nguhu\nbuhu\nwuhu\n\ncuhu\n' )
    a.input( '<!eof!>' )
    print( ns )
    main()

