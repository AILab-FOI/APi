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
import threading
from threading import Thread

# RegEx for parsing agent definition files

file_re = re.compile( r'FILE (.*)' )
http_re = re.compile( r'HTTP (.*)' )
ws_re  = re.compile( r'WS (.*)' )
netcat_re = re.compile( r'NETCAT (.*)[:]([0-9]+)(?:[:](udp))?' )

delimiter_re = re.compile( r'DELIMITER (.*)' )
time_re = re.compile( r'TIME ([0-9.]+)' )
size_re = re.compile( r'SIZE ([0-9]+)' )
regex_re = re.compile( r'REGEX .*' )

# Not implemented error message

NIE = 'Sorry, it is planned, I promise ;-)'

# Temporary folder path

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

from pyxf.pyxf import swipl

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
        self.kb = swipl()

    def map( self, data ):
        pass

class APiAgent( APiBaseAgent ):
    '''Service wrapper agent.'''

    # TODO: Sort methods / coroutines by type
    def __init__( self, agentname, name, password, args=[], flows=[] ):
        '''
        Constructor.
        agentname - name as in agent definition (.ad) file.
        name - XMPP/Jabber username
        password - XMPP/Jabber password
        args - list of arguments (from APi statement)
        flows - list of message flows (from APi statement)
        '''
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
        '''
        Agent definition file (.ad) loader.
        fh - open agent definition file handle
        '''
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
            # Initialize attributes to be used later
            self.cmd = self.descriptor[ 'agent' ][ 'start' ]
            self.input_file_path = None
            self.input_delimiter = None
            self.http_proc = None
            self.ws_proc = None
            self.nc_proc = None
            self.output_nc_threaded = None
            self.nc_output_thread = None
            self.input_ended = None

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

            # HTTP threads
            self.httpstdout_thread = None
            self.httpfile_thread = None
            self.httphttp_thread = None
            self.httpws_thread = None
            self.httpnc_thread = None
            self.httpncrec_thread = None

            # WS threads
            self.wsstdout_thread = None
            self.wsfile_thread = None
            self.wshttp_thread = None
            self.wsws_thread = None
            self.wsnc_thread = None
            self.wsncrec_thread = None
            
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
            
        
        #self.say( self.descriptor )

    async def read_stdout( self, stdout ):
        '''
        Coroutine reading STDOUT and calling callback method.
        stdout - STDOUT file handle
        '''
        while True:
            buf =  await stdout.readline() 
            if not buf:
                break

            if self.output_type == 'STDOUT' and buf:
                self.output_callback( buf.decode() )


    async def read_stderr( self, stderr ):
        '''
        Coroutine reading STDERR and calling callback method.
        stderr - STDERR file handle
        '''
        while True:
            buf = await stderr.readline()
            if not buf:
                break
            
            if self.output_type == 'STDERR':
                self.output_callback( buf.decode() )

    
    async def read_file( self, file_path ):
        '''
        Coroutine reading file and calling callback method.
        file_path - file path to be read from
        '''
        file_empty = True
        while file_empty:
            async with aiofiles.open( file_path, mode='r' ) as f:
                async for line in f:
                    self.output_callback( line )
                    file_empty = False
            await asyncio.sleep( 0.1 )

    async def read_url( self, url ):
        '''
        Coroutine reading URL and calling callback method.
        url - URL to be read from
        '''
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
        '''
        Coroutine reading WebSocket and calling callback method.
        url - WS URL to be read from
        '''
        error = True
        not_timeout = True
        while error:
            try:
                async with websockets.connect( url ) as websocket:
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
                            not_timeout = False
                    error = False
            except Exception as e:
                try:
                    assert e.errno == 111
                except:
                    error = False
                    
                await asyncio.sleep( 0.2 )


    def read_nc( self, host, port, udp=False ):
        '''
        Method reading from NETCAT socket and calling callback method.
        host - host
        port - port
        udp=False - should NETCAT use UDP (if false, default is TCP)
        '''
        not_available = True
        while not_available:
            try:
                ncclient = nclib.Netcat( ( host, port ), udp=udp, raise_eof=True )
                not_available = False
            except Exception as e:
                print( e )
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
                elif self.input_ended:
                    raise Exception( 'Done' )
            except Exception as e:
                error = True
                
    async def write_stdin( self, stdin ):
        '''
        Coroutine writing to STDIN
        stdin - STDIN file handle
        '''
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

        
    def input_file( self, data ):
        '''
        File input method
        data - data to be written to file
        '''
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
        '''
        File to STDOUT/STDERR coroutine
        cmd - command to be started as service
        '''
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE )

        await asyncio.gather(
            self.read_stderr( proc.stderr ),
            self.read_stdout( proc.stdout ) )



    def input_stdin( self, data ):
        '''
        STDIN input method
        data - data to be written to STDIN
        '''
        if self.input_value_type == 'BINARY':
            data = data.encode( 'utf-8' )

        if self.input_delimiter:
            inp = [ i for i in data.split( self.input_delimiter ) if i ]
        else:
            inp = [ data ]
            
        self.BUFFER.extend( inp )

        if data == self.input_end:
            self.service_quit( 'Got end delimiter on STDIN, quitting!' )
        

    
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

    async def input_httpstdout_run( self, cmd ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE )

        
        await asyncio.gather(
            self.read_stderr( proc.stderr ),
            self.read_stdout( proc.stdout ) )
        
        
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_httphttp_run( self, cmd, url ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL )

        
        await asyncio.gather(
            self.read_url( url ) )
        
        while not self.input_ended:
            sleep( 0.1 )
        
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    

    async def input_httpfile_run( self, cmd, file_path ):
        proc = await asyncio.create_subprocess_shell(
            cmd )

        
        
        await asyncio.gather( self.read_file( file_path ) )
                
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_httpws_run( self, cmd, url ):
        proc = await asyncio.create_subprocess_shell(
            cmd )
        
        await asyncio.gather( self.read_ws( url ) )
                
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_httpnc_run( self, cmd ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL )
        
        while not self.input_ended:
            sleep( 0.1 )
            
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except Exception as e:
            pass
        
    def input_http( self, data, callback=False ):
        if self.input_value_type == 'BINARY':
            data = data.encode( 'utf-8' )
        if self.input_delimiter:
            inp = [ i for i in data.split( self.input_delimiter ) if i != '' ]
        else:
            inp = [ data ]
        for d in inp:
            url = self.http_url + d
            error = True
            while error:
                try:
                    response = requests.get( url, verify=False )
                    result = response.content.decode( 'utf-8' )
                    if callback:
                        if self.output_delimiter:
                            out = [ i for i in result.split( self.output_delimiter ) if i ]
                        else:
                            out = [ result ]
                        for i in out:
                            self.output_callback( i )
                    error = False
                except Exception as e:
                    sleep( 0.2 )
            if d == self.input_end:
                self.service_quit( 'Received end delimiter, shutting down HTTP server!' )
                return

    async def input_wsstdout_run( self, cmd ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE )

        await asyncio.gather(
            self.read_stderr( proc.stderr ),
            self.read_stdout( proc.stdout ) )
    
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass


    async def input_wsfile_run( self, cmd, file_path ):
        proc = await asyncio.create_subprocess_shell(
            cmd )

        await asyncio.gather( self.read_file( file_path ) )
                
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_wshttp_run( self, cmd, url ):
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

    async def input_wsws_run( self, cmd, url ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL )

        
        while not self.input_ended:
            sleep( 0.1 )
        
        await asyncio.gather(
            self.read_ws( url ) )
        
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_wsnc_run( self, cmd ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL )
        
        while not self.input_ended:
            sleep( 0.1 )
            
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except Exception as e:
            pass
        
    def input_ws( self, data, callback=False ):
        if self.input_value_type == 'BINARY':
            data = data.encode( 'utf-8' )
        if self.input_delimiter:
            inp = [ i for i in data.split( self.input_delimiter ) if i != '' ]
        else:
            imp = [ data ]
        for i in inp:
            asyncio.get_event_loop().run_until_complete( self.ws( i, callback ) )
            if i == self.input_end:
                self.service_quit( 'Received end delimiter, shutting down WebSocket server!' )
                return
        
    async def ws( self, msg, callback=False ):
        error = True
        while error:
            try:
                async with websockets.connect( self.ws_url ) as websocket:
                    await websocket.send( msg )
                    resp = await websocket.recv()
                    if callback:
                        if self.output_delimiter:
                            resp = [ i for i in resp.split( self.output_delimiter ) if i ]
                        else:
                            resp = [ resp ]
                        for i in resp:
                            self.output_callback( i )
                    error = False
            except Exception as e:
                sleep( 0.2 )

    async def input_ncstdout_run( self, cmd ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE )

        await asyncio.gather(
            self.read_stderr( proc.stderr ),
            self.read_stdout( proc.stdout ) )
    
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_ncfile_run( self, cmd, file_path ):
        proc = await asyncio.create_subprocess_shell(
            cmd )

        await asyncio.gather( self.read_file( file_path ) )
                
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_nchttp_run( self, cmd, url ):
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

    async def input_ncws_run( self, cmd, url ):
        proc = await asyncio.create_subprocess_shell(
            cmd )
        
        await asyncio.gather( self.read_ws( url ) )
                
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except:
            pass

    async def input_ncnc_run( self, cmd ):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL )
        
        while not self.input_ended:
            sleep( 0.1 )
            
        try:
            pid = proc.pid
            pr = psutil.Process( pid )
            for proc in pr.children( recursive=True ): 
                proc.kill()
            pr.kill()
        except Exception as e:
            pass
                
    def input_nc( self, data, callback=False ):
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
                self.nc_client.sendline( i.encode( 'utf-8' ) )
                if callback:
                    result = self.nc_client.read( timeout=1 ).decode( 'utf-8' )
                    if result:
                        if self.output_delimiter:
                            result = [ j for j in result.split( self.output_delimiter ) if j ]
                        else:
                            result = [ result ]
                        for j in result:
                            self.output_callback( j )
                    
            except Exception as e:
                print( e )
                self.nc_client.close()
                self.service_quit( 'NETCAT process ended, quitting!' )
                return None

    def output_callback( self, data ):
        '''
        Output callback method.
        data - data read from service.
        '''
        self.say( 'I just received:', data )
        # TODO: connect this to output channels

    def service_quit( self, msg='' ):
        '''
        Service quitting and clean up method. Joins all threads and
        kills all running processes (services).

        msg - optional message (more or less for debug purposes)
        '''
        sleep( 0.5 )
        self.say( msg ) # firstly need to clean up and finish all threads
        self.input_ended = True
        sleep( 0.5 )
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
            if self.httpstdout_thread:
                self.httpstdout_thread.join()
            if self.httpfile_thread:
                self.httpfile_thread.join()
            if self.httphttp_thread:
                self.httphttp_thread.join()
            if self.httpws_thread:
                self.httpws_thread.join()
            if self.httpnc_thread:
                self.httpnc_thread.join()
            if self.httpncrec_thread:
                self.httpncrec_thread.join()
            if self.wsstdout_thread:
                self.wsstdout_thread.join()
            if self.wsfile_thread:
                self.wsfile_thread.join()
            if self.wshttp_thread:
                self.wshttp_thread.join()
            if self.wsws_thread:
                self.wsws_thread.join()
            if self.wsnc_thread:
                self.wsnc_thread.join()
            if self.wsncrec_thread:
                self.wsncrec_thread.join()
            if self.ncstdout_thread:
                self.ncstdout_thread.join()
            if self.ncfile_thread:
                self.ncfile_thread.join()
            if self.nchttp_thread:
                self.nchttp_thread.join()
            if self.ncws_thread:
                self.ncws_thread.join()
            if self.ncnc_thread:
                self.ncnc_thread.join()
            if self.ncncrec_thread:
                self.ncncrec_thread.join()
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
        '''
        Agent descriptor processor (the heart of the agent). Processes
        the agent description (as loaded with self._load) and connects
        inputs to outputs for various types of communication channels
        (STDIN/STDOUT/STDERR, files, HTTP, WebSocket, Netcat). It also
        starts the defined services (subprocesses) and needed threads 
        and/or coroutines to handle and connect inputs to outputs.
        The basic rule is that the START value from the agent description
        file (.ad) is started as a subprocess (the microservice), input
        is written to the input as specified by the agent description 
        file and output is read from the output also specified in the 
        same file. The output threads / coroutines call the output_callback
        method to handle to output in a desired manner (i.e. forward it
        to a given output channel of the agent).
        '''
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

        elif self.input_type[ :4 ] == 'HTTP' and self.output_type in ( 'STDOUT', 'STDERR' ):
            url = http_re.findall( self.input_type )[ 0 ]
            self.http_url = url
            self.input = self.input_http 
            self.httpstdout_thread = Thread( target=asyncio.run, args=( self.input_httpstdout_run( self.cmd ),  ) )
            self.httpstdout_thread.start()
            
        elif self.input_type[ :4 ] == 'HTTP' and self.output_type[ :4 ] == 'FILE':
            url = http_re.findall( self.input_type )[ 0 ]
            self.http_url = url
            self.input = self.input_http
            fl = file_re.findall( self.output_type )[ 0 ]
            self.output_file_path = fl

            
            self.httpfile_thread = Thread( target=asyncio.run, args=( self.input_httpfile_run( self.cmd, self.output_file_path ),  ) )
            self.httpfile_thread.start()

            
        elif self.input_type[ :4 ] == 'HTTP' and self.output_type[ :4 ] == 'HTTP':
            url = http_re.findall( self.input_type )[ 0 ]
            self.http_url = url
            url = http_re.findall( self.output_type )[ 0 ]
            self.http_url_output = url
            if self.http_url == self.http_url_output:
                cmd = shlex.split( self.cmd + ' > /dev/null 2>&1 &' )
                self.http_proc = sp.Popen( cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL )
                self.input = lambda data: self.input_http( data, callback=True )
            else:
                self.input = self.input_http
                self.httphttp_thread = Thread( target=asyncio.run, args=( self.input_httphttp_run( self.cmd, self.http_url_output ), ) )
                self.httphttp_thread.start()

        elif self.input_type[ :4 ] == 'HTTP' and self.output_type[ :2 ] == 'WS':
            url = http_re.findall( self.input_type )[ 0 ]
            self.http_url = url
            url = ws_re.findall( self.output_type )[ 0 ]
            self.ws_output_url = url
            self.input = self.input_http

            self.httpws_thread = Thread( target=asyncio.run, args=( self.input_httpws_run( self.cmd, self.ws_output_url ), ) )
            self.httpws_thread.start()

        
        elif self.input_type[ :4 ] == 'HTTP' and self.output_type[ :6 ] == 'NETCAT':
            url = http_re.findall( self.input_type )[ 0 ]
            self.http_url = url
            host, port, udp = netcat_re.findall( self.output_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''
            self.input = self.input_http

            
            self.httpnc_thread = Thread( target=asyncio.run, args=( self.input_httpnc_run( self.cmd ), ) )
            self.httpnc_thread.start()
            self.httpncrec_thread = Thread( target=self.read_nc, args=( self.nc_host, self.nc_port, self.nc_udp ) )
            self.httpncrec_thread.start() 
        
        elif self.input_type[ :2 ] == 'WS' and self.output_type in ( 'STDOUT', 'STDERR' ):
            url = ws_re.findall( self.input_type )[ 0 ]
            self.ws_url = url
            self.input = self.input_ws
            
            self.wsstdout_thread = Thread( target=asyncio.run, args=( self.input_wsstdout_run( self.cmd ), ) )
            self.wsstdout_thread.start()
        
        elif self.input_type[ :2 ] == 'WS' and self.output_type[ :4 ] == 'FILE':
            url = ws_re.findall( self.input_type )[ 0 ]
            self.ws_url = url
            self.input = self.input_ws
            fl = file_re.findall( self.output_type )[ 0 ]
            self.output_file_path = fl

            
            self.wsfile_thread = Thread( target=asyncio.run, args=( self.input_wsfile_run( self.cmd, self.output_file_path ),  ) )
            self.wsfile_thread.start()
        
        elif self.input_type[ :2 ] == 'WS' and self.output_type[ :4 ] == 'HTTP':
            url = ws_re.findall( self.input_type )[ 0 ]
            self.ws_url = url
            self.input = self.input_ws
            url = http_re.findall( self.output_type )[ 0 ]
            self.output_url = url
            
            self.wshttp_thread = Thread( target=asyncio.run, args=( self.input_wshttp_run( self.cmd, self.output_url ), ) )
            self.wshttp_thread.start()
            
        
        elif self.input_type[ :2 ] == 'WS' and self.output_type[ :2 ] == 'WS':
            url = ws_re.findall( self.input_type )[ 0 ]
            self.ws_url = url
            self.input = self.input_ws
            url = ws_re.findall( self.output_type )[ 0 ]
            self.ws_output_url = url
            if self.ws_url == self.ws_output_url:
                cmd = shlex.split( self.cmd + ' > /dev/null 2>&1 &' )
                self.ws_proc = sp.Popen( cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL )
                self.input = lambda data: self.input_ws( data, callback=True )
            else:
                self.input = self.input_ws
                self.wsws_thread = Thread( target=asyncio.run, args=( self.input_wsws_run( self.cmd, self.ws_output_url ), ) )
                self.wsws_thread.start()
            
        
        elif self.input_type[ :2 ] == 'WS' and self.output_type[ :6 ] == 'NETCAT':
            url = ws_re.findall( self.input_type )[ 0 ]
            self.ws_url = url
            self.input = self.input_ws
            host, port, udp = netcat_re.findall( self.output_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''

            
            self.wsnc_thread = Thread( target=asyncio.run, args=( self.input_wsnc_run( self.cmd ), ) )
            self.wsnc_thread.start()
            self.wsncrec_thread = Thread( target=self.read_nc, args=( self.nc_host, self.nc_port, self.nc_udp ) )
            self.wsncrec_thread.start()

        
        elif self.input_type[ :6 ] == 'NETCAT' and self.output_type in ( 'STDOUT', 'STDERR' ):
            host, port, udp = netcat_re.findall( self.input_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''
            self.input = self.input_nc
            
            self.ncstdout_thread = Thread( target=asyncio.run, args=( self.input_ncstdout_run( self.cmd ), ) )
            self.ncstdout_thread.start()

            error = True
            while error:
                try:
                    self.nc_client = nclib.Netcat( ( self.nc_host, self.nc_port ), udp=self.nc_udp )
                    error = False
                except Exception as e:
                    sleep( 0.1 )

        elif self.input_type[ :6 ] == 'NETCAT' and self.output_type[ :4 ] == 'FILE':
            host, port, udp = netcat_re.findall( self.input_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''
            fl = file_re.findall( self.output_type )[ 0 ]
            self.output_file_path = fl
            self.input = self.input_nc
            
            self.ncfile_thread = Thread( target=asyncio.run, args=( self.input_ncfile_run( self.cmd, self.output_file_path ),  ) )
            self.ncfile_thread.start()
            # TODO: find out why only the first output is processed, i.e.
            # ncat writes to the file and closes it seemingly after each
            # input making it possible for read_file() to read it an end
            # prematurely. See if this can be avoided.
            
            error = True
            while error:
                try:
                    self.nc_client = nclib.Netcat( ( self.nc_host, self.nc_port ), udp=self.nc_udp )
                    error = False
                except Exception as e:
                    sleep( 0.1 )

        elif self.input_type[ :6 ] == 'NETCAT' and self.output_type[ :4 ] == 'HTTP':
            host, port, udp = netcat_re.findall( self.input_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''
            self.input = self.input_nc
            url = http_re.findall( self.output_type )[ 0 ]
            self.output_url = url
            
            self.nchttp_thread = Thread( target=asyncio.run, args=( self.input_nchttp_run( self.cmd, self.output_url ), ) )
            self.nchttp_thread.start()
            
            error = True
            while error:
                try:
                    self.nc_client = nclib.Netcat( ( self.nc_host, self.nc_port ), udp=self.nc_udp )
                    error = False
                except Exception as e:
                    sleep( 0.1 )

        elif self.input_type[ :6 ] == 'NETCAT' and self.output_type[ :2 ] == 'WS':
            host, port, udp = netcat_re.findall( self.input_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''
            self.input = self.input_nc
            url = ws_re.findall( self.output_type )[ 0 ]
            self.ws_output_url = url
            
            self.ncws_thread = Thread( target=asyncio.run, args=( self.input_ncws_run( self.cmd, self.ws_output_url ), ) )
            self.ncws_thread.start()
            
            error = True
            while error:
                try:
                    self.nc_client = nclib.Netcat( ( self.nc_host, self.nc_port ), udp=self.nc_udp )
                    error = False
                except Exception as e:
                    sleep( 0.1 )
                    
            # TODO: add adequate threads and finish other outputs
        elif self.input_type[ :6 ] == 'NETCAT' and self.output_type[ :6 ] == 'NETCAT':
            host, port, udp = netcat_re.findall( self.input_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''
            
            ohost, oport, oudp = netcat_re.findall( self.output_type )[ 0 ]
            self.nc_host_output = ohost
            self.nc_port_output = int( oport )
            self.nc_udp_output = oudp != ''


            if ( host, port, udp ) == ( ohost, oport, oudp ):
                self.nc_proc = sp.Popen( shlex.split( self.cmd ), stdout=sp.PIPE, stderr=sp.DEVNULL )
                sleep( 0.1 )
                self.input = lambda data: self.input_nc( data, callback=True )

                error = True
                while error:
                    try:
                        self.nc_client = nclib.Netcat( ( self.nc_host, self.nc_port ), udp=self.nc_udp )
                        error = False
                    except Exception as e:
                        sleep( 0.1 )

            else:
                self.input = self.input_nc
                self.ncnc_thread = Thread( target=asyncio.run, args=( self.input_ncnc_run( self.cmd ), ) )
                self.ncnc_thread.start()
    
                error = True
                while error:
                    try:
                        self.nc_client = nclib.Netcat( ( self.nc_host, self.nc_port ), udp=self.nc_udp )
                        
                        error = False
                    except Exception as e:
                        sleep( 0.1 )
            
                self.ncncrec_thread = Thread( target=self.read_nc, args=( self.nc_host_output, self.nc_port_output, self.nc_udp_output ) )
                self.ncncrec_thread.start()

                
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
                res = self.nc_client.recv_until( self.output_delimiter, timeout=1 ).decode( 'utf-8' )
                print( res )
            except Exception as e:
                print( e )
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

    # TESTING
    os.chdir('test')
    '''rs = APiRegistrationService( 'APi-test' )
    rs.register( 'ivek' )'''

    a = APiAgent( 'bla_nc_nc', 'bla0agent@dragon.foi.hr', 'tajna', flows=[ (1, 2), (3, 4), (1, 5), (3, 6), (1, 3, 5, 7) ] )

    sleep( 1 )
    a.input( 'avauhu\nguhu\nbuhu\nwuhu\ncuhu\n' )
    sleep( 3 )
    a.input( 'juhu\n' )
    sleep( 2 )
    a.input( 'muhu\n' )
    a.input( 'ahu\n' )
    sleep( 1 )
    a.input( 'puhu\nluhu\n' )
    sleep( 2 )
    a.input( '<!eof!>' )
    
    print( ns )

    
    main()
    
    spade.quit_spade()

