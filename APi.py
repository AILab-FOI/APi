#!/usr/bin/env python3

from version import __version__

import sys
import errno
import os
import signal
from time import sleep
from itertools import tee, cycle
from uuid import uuid4
import subprocess as sp
import shlex
import psutil
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
import aiofiles
import aiohttp
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
            self.input_file_path = None
            self.input_delimiter = None
            self.http_proc = None
            self.ws_proc = None
            self.nc_proc = None
            self.output_nc_threaded = None
            self.nc_output_thread = None

            # Threads

            # STDIN threads
            self.stdinout_thread = None
            self.stdinfile_thread = None
            self.stdinhttp_thread = None
            self.stdinws_thread = None
            self.stdinnc_thread = None
            self.stdinncrec_thread = None

            # FILE threads
            self.filestdout_thread = None
            self.filefile_thread = None
            self.filehttp_thread = None
            self.filews_thread = None
            self.filenc_thread = None
            self.filencrec_thread = None
            
            try:
                self.process_descriptor()
            except Exception as e:
                err = 'Agent definition file is invalid.\n' + str( e )
                raise APiAgentDefinitionError( err )


            
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
        # TODO: This needs to be synchronized with
        # processes reading the file (i.e. the process
        # should not start until the file has been
        # written. Also the service should not stop
        # until the process has read the file.
        self.service_quit( 'Input file written, quitting!' )


    async def input_file_run( self, cmd ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE )

        await asyncio.gather(
            self.read_stderr( proc.stderr ),
            self.read_stdout( proc.stdout ) )



    def input_stdin( self, data ):
        if self.input_value_type == 'BINARY':
            data = data.encode( 'utf-8' )

        if self.input_delimiter:
            inp = [ i for i in data.split( self.input_delimiter ) if i ]
        else:
            inp = [ data ]
            
        self.BUFFER.extend( inp )

        if data == self.input_end:
            self.service_quit( 'Got end delimiter on STDIN, quitting!' )
        

    async def read_stdout( self, stdout ):
        while True:
            buf = await stdout.readline()
            if not buf:
                break

            if self.output_type == 'STDOUT':
                self.output_callback( buf.decode() )


    async def read_stderr( self, stderr ):
        while True:
            buf = await stderr.read()
            if not buf:
                break

            
            if self.output_type == 'STDERR':
                self.output_callback( buf.decode() )

    
    async def read_file( self, file_path ):
        file_empty = True
        while file_empty:
            async with aiofiles.open( file_path, mode='r' ) as f:
                async for line in f:
                    self.output_callback( line )
                    file_empty = False
            await asyncio.sleep( 0.1 )

    async def read_url( self, url ):
        not_available = True
        while not_available:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get( url ) as resp:
                        result = await resp.text()
                        if self.output_delimiter:
                            res = [ i for i in result.split( self.output_delimiter ) if i ]
                        else:
                            res = [ result ]
                        for r in res:
                            self.output_callback( r )
                not_available = False
            except Exception as e:
                await asyncio.sleep( 0.2 )

    async def read_ws( self, url ):
        error = True
        not_timeout = True
        while error:
            try:
                async with websockets.connect( url ) as websocket:
                    #resp = await websocket.recv()
                    not_timeout = True
                    while not_timeout:
                        try:
                            resp = await asyncio.wait_for( websocket.recv(), timeout=0.1 )
                            if self.output_delimiter:
                                res = [ i for i in resp.split( self.output_delimiter ) if i ]
                            else:
                                res = [ resp ]
                            for r in res:
                                self.output_callback( r )
                        except asyncio.TimeoutError:
                            print( 'TIMEOUT' )
                            not_timeout = False
                    error = False
            except Exception as e:
                try:
                    assert e.errno == 111
                except:
                    error = False
                    
                await asyncio.sleep( 0.2 )


    def read_nc( self, host, port, udp=False ):
        not_available = True
        while not_available:
            try:
                ncclient = nclib.Netcat( ( host, port ), udp=udp, raise_eof=True )
                not_available = False
            except Exception as e:
                sleep( 0.2 )

        error = False
        while not error:
            try:
                result = ncclient.recv_until( self.output_delimiter, timeout=0.2 )
                sleep( 0.5 )
                if result:
                    result = result.decode()
                    if self.output_delimiter:
                        res = [ i for i in result.split( self.output_delimiter ) if i ]
                    else:
                        res = [ result ]
                    for r in res:
                        self.output_callback( r )
            except Exception as e:
                error = True
                
    async def write_stdin( self, stdin ):
        send = True
        while send:
            if not self.BUFFER:
                await asyncio.sleep( 0.1 )
            else:
                i = self.BUFFER.pop( 0 )
                if i == self.input_end:
                    send = False
                else:
                    buf = f'{ i }\n'.encode()

                    try:
                        stdin.write( buf )
                        await stdin.drain()
                        await asyncio.sleep( 0.1 )
                    except ConnectionResetError as e:
                        self.service_quit( 'STDIN connection reset, quitting!' )
                        break
        stdin.close()

    async def input_stdin_run( self, cmd ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE )

        await asyncio.gather(
            self.read_stderr( proc.stderr ),
            self.read_stdout( proc.stdout ),
            self.write_stdin( proc.stdin ) )

    async def input_stdinfile_run( self, cmd, file_path ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE )

        await asyncio.gather(
            self.write_stdin( proc.stdin ),
            self.read_file( file_path ) )


    async def input_stdinhttp_run( self, cmd, url ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL )

        await asyncio.gather(
            self.write_stdin( proc.stdin ),
            self.read_url( url ) )

        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_stdinws_run( self, cmd, url ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL )

        await asyncio.gather(
            self.write_stdin( proc.stdin ),
            self.read_ws( url ) )

        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_stdinnc_run( self, cmd, host, port, udp ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL )
            

        await asyncio.gather(
            self.write_stdin( proc.stdin ) )
        

        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_filefile_run( self, cmd, file_path ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE )

        await asyncio.gather( self.read_file( file_path ) )

    async def input_filehttp_run( self, cmd, file_path, url ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL )

        await asyncio.gather( self.read_url( url ) )

        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_filews_run( self, cmd, file_path, url ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL )

        await asyncio.gather( self.read_ws( url ) )

        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_filenc_run( self, cmd, file_path ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL )
        while not self.input_file_written:
            await asyncio.sleep( 0.1 )
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except Exception as e:
            pass
        
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
            self.nc_client.close()
            self.service_quit( 'Got end delimiter, quitting NETCAT!' )
            return None
        if self.input_delimiter:
            inp = [ i for i in data.split( self.input_delimiter ) if i != '' ]
        else:
            imp = [ data ]
        sleep( 0.1 )
        for i in inp:
            try:
                # TODO: add output delimiter here
                delimiter = '\n'
                self.nc_client.send( i + delimiter )
                #print( 'input_nc: sent', i )
            except Exception as e:
                self.service_quit( 'NETCAT process ended, quitting!' )
                return None

    def output_callback( self, data ):
        self.say( 'I just received:', data )
        # TODO: connect this to output channels

    def service_quit( self, msg ):
        sleep( 0.5 )
        self.say( msg ) # firstly need to clean up and finish all threads
        try:
            if self.stdinout_thread:
                self.stdinout_thread.join()
            if self.stdinfile_thread:
                self.stdinfile_thread.join()
            if self.stdinhttp_thread:
                self.stdinhttp_thread.join()
            if self.stdinws_thread:
                self.stdinws_thread.join()
            if self.stdinnc_thread:
                self.stdinnc_thread.join()
            if self.stdinncrec_thread:
                self.stdinncrec_thread.join()
            if self.filestdout_thread:
                self.filestdout_thread.join()
            if self.filefile_thread:
                self.filefile_thread.join()
            if self.filehttp_thread:
                self.filehttp_thread.join()
            if self.filews_thread:
                self.filews_thread.join()
            if self.filenc_thread:
                self.filenc_thread.join()
            if self.filencrec_thread:
                self.filencrec_thread.join()
            if self.nc_output_thread:
                self.nc_output_thread.join()
        except Exception as e:
            pass

        if self.http_proc:
            self.http_proc.terminate()

        if self.ws_proc:
            self.ws_proc.terminate()

        if self.nc_proc:
            # Total overkill ;-)
            pid = self.nc_proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
            self.nc_proc.terminate()
            os.system( 'kill -9 %d' % pid )
        self.nc_output_thread_flag = False
        
    def process_descriptor( self ):
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
                err = 'Invalid input cutoff "%s"\n' % self.input_cutoff
                raise APiAgentDefinitionError( err )

            if self.input_end == 'NEWLINE':
                self.input_end = '\n'
        else:
            err = 'Invalid input data type "%s"\n' % self.input_data_type
            raise APiAgentDefinitionError( err )

        # I hate to do this the way down there, i.e. writing the same more
        # or less twice with different attributes, but I am not going into
        # AspectOP just for the sake of a few lines of duplicate code :P
        if self.output_data_type == 'ONEVALUE':
            pass
        elif self.output_data_type == 'STREAM':
            if self.output_cutoff[ :4 ] == 'TIME':
                time = float( time_re.findall( self.output_cutoff )[ 0 ] )
                print( time )
                raise NotImplementedError( NIE )                
            elif self.output_cutoff[ :4 ] == 'SIZE':
                size = int( size_re.findall( self.output_cutoff )[ 0 ] )
                print( size )
                raise NotImplementedError( NIE ) 
            elif self.output_cutoff[ :9 ] == 'DELIMITER':
                self.output_delimiter = delimiter_re.findall( self.output_cutoff )[ 0 ]
                if self.output_delimiter == 'NEWLINE':
                    self.output_delimiter = '\n'               
            elif self.output_cutoff[ :5 ] == 'REGEX':
                regex = int( regex_re.findall( self.output_cutoff )[ 0 ] )
                print( regex )
                raise NotImplementedError( NIE ) 
            else:
                err = 'Invalid output cutoff "%s"\n' % self.output_cutoff
                raise APiAgentDefinitionError( err )

            if self.output_end == 'NEWLINE':
                self.output_end = '\n'
        else:
            err = 'Invalid output data type "%s"\n' % self.output_data_type
            raise APiAgentDefinitionError( err )
        
        if self.input_type == 'STDIN' and self.output_type in ( 'STDOUT', 'STDERR' ):
            self.input = self.input_stdin

            self.BUFFER = []
            self.stdinout_thread = Thread( target=asyncio.run, args=( self.input_stdin_run( self.cmd ), ) )
            self.stdinout_thread.start()
        elif self.input_type == 'STDIN' and self.output_type[ :4 ] == 'FILE':
            fl = file_re.findall( self.output_type )[ 0 ]
            self.output_file_path = fl
            
            self.input = self.input_stdin

            self.BUFFER = []
            self.stdinfile_thread = Thread( target=asyncio.run, args=( self.input_stdinfile_run( self.cmd, fl ), ) )
            self.stdinfile_thread.start()
        elif self.input_type == 'STDIN' and self.output_type[ :4 ] == 'HTTP':
            url = http_re.findall( self.output_type )[ 0 ]
            self.output_url = url
            self.input = self.input_stdin
            self.BUFFER = []
            
            self.stdinhttp_thread = Thread( target=asyncio.run, args=( self.input_stdinhttp_run( self.cmd, url ), ) )
            self.stdinhttp_thread.start()

        elif self.input_type == 'STDIN' and self.output_type[ :2 ] == 'WS':
            url = ws_re.findall( self.output_type )[ 0 ]
            self.output_url = url
            self.input = self.input_stdin
            self.BUFFER = []

            self.stdinws_thread = Thread( target=asyncio.run, args=( self.input_stdinws_run( self.cmd, url ), ) )
            self.stdinws_thread.start()

        elif self.input_type == 'STDIN' and self.output_type[ :6 ] == 'NETCAT':
            host, port, udp = netcat_re.findall( self.output_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''
            self.input = self.input_stdin
            self.BUFFER = []

            self.stdinnc_thread = Thread( target=asyncio.run, args=( self.input_stdinnc_run( self.cmd, self.nc_host, self.nc_port, self.nc_udp ), ) )
            self.stdinnc_thread.start()
            self.stdinncrec_thread = Thread( target=self.read_nc, args=( self.nc_host, self.nc_port, self.nc_udp ) )
            self.stdinncrec_thread.start()
            
        elif self.input_type[ :4 ] == 'FILE' and self.output_type in ( 'STDOUT', 'STDERR' ):
            fl = file_re.findall( self.input_type )[ 0 ]
            self.input_file_path = fl
            self.input_file_written = False
            self.input = self.input_file
            self.filestdout_thread = Thread( target=asyncio.run, args=( self.input_file_run( self.cmd ), ) )
            self.filestdout_thread.start()
        elif self.input_type[ :4 ] == 'FILE' and self.output_type[ :4 ] == 'FILE':
            infl = file_re.findall( self.input_type )[ 0 ]
            outfl = file_re.findall( self.output_type )[ 0 ]
            self.input_file_path = infl
            self.output_file_path = outfl
            self.input_file_written = False
            self.input = self.input_file
            self.filefile_thread = Thread( target=asyncio.run, args=( self.input_filefile_run( self.cmd, self.output_file_path ), ) )
            self.filefile_thread.start()
        elif self.input_type[ :4 ] == 'FILE' and self.output_type[ :4 ] == 'HTTP':
            fl = file_re.findall( self.input_type )[ 0 ]
            self.input_file_path = fl
            self.input_file_written = False
            self.input = self.input_file
            url = http_re.findall( self.output_type )[ 0 ]
            self.output_url = url
            self.filehttp_thread = Thread( target=asyncio.run, args=( self.input_filehttp_run( self.cmd, self.input_file_path, self.output_url ), ) )
            self.filehttp_thread.start()

        elif self.input_type[ :4 ] == 'FILE' and self.output_type[ :2 ] == 'WS':
            fl = file_re.findall( self.input_type )[ 0 ]
            self.input_file_path = fl
            self.input_file_written = False
            self.input = self.input_file
            url = ws_re.findall( self.output_type )[ 0 ]
            self.output_url = url
            self.filews_thread = Thread( target=asyncio.run, args=( self.input_filews_run( self.cmd, self.input_file_path, self.output_url ), ) )
            self.filews_thread.start()

        elif self.input_type[ :4 ] == 'FILE' and self.output_type[ :6 ] == 'NETCAT':
            fl = file_re.findall( self.input_type )[ 0 ]
            self.input_file_path = fl
            self.input_file_written = False
            self.input = self.input_file
            host, port, udp = netcat_re.findall( self.output_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''

            
            self.filenc_thread = Thread( target=asyncio.run, args=( self.input_filenc_run( self.cmd, self.input_file_path ), ) )
            self.filenc_thread.start()
            self.filencrec_thread = Thread( target=self.read_nc, args=( self.nc_host, self.nc_port, self.nc_udp ) )
            self.filencrec_thread.start() 
            
            # TODO: add adequate threads and finish other outputs
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
            self.nc_proc = sp.Popen( shlex.split( self.cmd ), stdout=sp.PIPE, stderr=sp.DEVNULL )
            sleep( 0.1 )
            error = True
            while error:
                try:
                    self.nc_client = nclib.Netcat( ( self.nc_host, self.nc_port ), udp=self.nc_udp )
                    error = False
                except Exception as e:
                    sleep( 0.1 )
            self.nc_output_thread_flag = True
            self.nc_output_thread = Thread( target=self.output_nc_threaded )
            self.nc_output_thread.start()
            self.input = self.input_nc
        else:
            err = 'Invalid input type "%s"\n' % self.input_type
            raise APiAgentDefinitionError( err )

        if self.input_value_type not in [ 'STRING', 'BINARY' ]:
            err = 'Invalid input value type "%s"\n' % self.input_value_type
            raise APiAgentDefinitionError( err )

    def output_nc_threaded( self ):
        error = False
        # TODO: if self.output_delimiter: ...
        delimiter = '\n'
        while not error:
            if not self.nc_output_thread_flag:
                return None
            try:
                res = self.nc_client.recv_until( delimiter, timeout=1 ).decode( 'utf-8' )
            except Exception as e:
                self.error = True
                self.service_quit( 'NETCAT process ended, quitting!' )
                return None
            if res:
                self.output_callback( res )

        
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

    a = APiAgent( 'bla_file_nc', 'bla0agent@dragon.foi.hr', 'tajna', flows=[ (1, 2), (3, 4), (1, 5), (3, 6), (1, 3, 5, 7) ] )

    sleep( 1 )
    a.input( 'avauhu\nguhu\nbuhu\nwuhu\ncuhu\n' )
    '''sleep( 3 )
    a.input( 'juhu\n' )
    sleep( 2 )
    a.input( 'muhu\n' )
    a.input( 'ahu\n' )
    sleep( 1 )
    a.input( 'puhu\nluhu\n' )
    sleep( 2 )
    a.input( '<!eof!>' )'''
    
    print( ns )
    main()

    spade.quit_spade()

