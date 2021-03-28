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
import random
import threading
from threading import Thread
import json
import itertools as it
import socket
from fnvhash import fnv1a_32
from copy import deepcopy

# RegEx for parsing agent definition files

file_re = re.compile( r'FILE (.*)' )
http_re = re.compile( r'HTTP (.*)' )
ws_re  = re.compile( r'WS (.*)' )
netcat_re = re.compile( r'NETCAT (.*)[:]([0-9]+)(?:[:](udp))?' )

delimiter_re = re.compile( r'DELIMITER (.*)' )
time_re = re.compile( r'TIME ([0-9.]+)' )
size_re = re.compile( r'SIZE ([0-9]+)' )
regex_re = re.compile( r'REGEX .*' )

var_re = re.compile( r'[?][a-zA-Z][a-zA-Z0-9_-]*' )

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

import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, FSMBehaviour, State
from spade.template import Template
from spade.message import Message
from spade import quit_spade
from aioxmpp.dispatcher import SimpleMessageDispatcher

import requests
# When using HTTPS with insecure servers this has to be uncommented
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings( InsecureRequestWarning )
import warnings

import asyncio
import aiofiles
import aiohttp
import concurrent.futures as cf
import logging
logging.getLogger( 'asyncio' ).setLevel( logging.CRITICAL )
import websockets
import nclib
import pexpect

from pyxf.pyxf import swipl

# Only for debug
DEBUG = False
TALK = True

if DEBUG:
    logging.basicConfig( level=logging.DEBUG )

    from aiodebug import log_slow_callbacks, monitor_loop_lag
    log_slow_callbacks.enable( 0.05 )
    


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

def verify( hashed, string ):
    '''
    Verify if a given hashed string is equal to a string when
    hashed with a FNV-1a function.
    '''
    return hashed == hash( string )

def hash( string ):
    '''
    Hash a given string using FNV-1a function.
    '''
    return hex( fnv1a_32( string.encode() ) )
    
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

class APiChannelDefinitionError( Exception ):
    '''Exception thrown when a channel is ill-defined'''
    pass

class APiShellInitError( Exception ):
    '''Exception thrown when shell server hasn't been initialized'''
    pass

class APiHTTPSWarning( Warning ):
    '''Warning when HTTP is used instead of HTTPS'''
    pass
    

class APiTalkingAgent( Agent ):
    '''
    Base agent (auxilliary methods and behaviours for all other
    types of agents
    '''
    def __init__( self, name, password, token=None ):
        super().__init__( name, password )
        #self.container.send = self.send
        
        self.token = token
        if token:
            self.auth = hash( str( self.jid.bare() ) + self.token )
        else:
            self.auth = None
        
        # Output buffer for messages to be send
        self.output_buffer = []
        # Input acknowledgement set for messages that are awaitng a reply
        self.input_ack = set()

        
        # TODO: This is a hardcoded delimiter for
        #       messages that are forwarded through
        #       the channel. Not an ideal solution.
        #       It would be good to see if something
        #       else would be better.
        self.delimiter = '\n' 

        # Address book of other agents
        self.address_book = {}

        self.LOG = logging.getLogger( 'APiAgent' )
    
    def say( self, *msg ):
        if TALK:
            '''
            out = [ '%s:' % self.name ]
            out += [ i for i in msg ]
            self.LOG.info( out )'''
            print( '%s:' % self.name, *msg )

    def verify( self, msg ):
        return verify( msg.metadata[ 'auth-token' ], str( msg.sender.bare() ) + self.token )

    def setup( self ):
        self.behaviour_output = self.OutputQueue()
        self.add_behaviour( self.behaviour_output )
        st = self.Stop()
        self.add_behaviour( st )


    async def schedule_message( self, to, body='', metadata={} ):
        # TODO: See if this can be done in a more elegant way ...
        msg = Message( to=to, body=body, metadata=deepcopy( metadata ) )
        self.say( 'Sending message:', msg.metadata, msg.to )
        await self.behaviour_output.send( deepcopy( msg ) )
        try:
            self.input_ack.add( msg.metadata[ 'reply-with' ] )
        except KeyError:
            pass

    class OutputQueue( CyclicBehaviour ):
        async def run( self ):
            pass


    class Stop( CyclicBehaviour ):
        # TODO: Test and validate this
        #       Also look up async def stop in APiHolon
        async def run( self ):
            msg = await self.receive( timeout=0.1 )
            if msg:
                try:
                    performative = msg.metadata[ "performative" ]
                    if performative == 'request' and msg.sender == self.agent.holon and msg.content == 'stop':
                        self.kill()
                except KeyError:
                    pass



class APiBaseAgent( APiTalkingAgent ):
    '''
    Base agent implementing all input/output mappings (e.g. STDIN/STDOUT/STDERR,
    file, HTTP, WebSocket, Netcat). Not to be instanced by itself, but should be
    used for inheritance.
    '''
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
                #print( '(read_ws) CONNECTING TO', url )
                async with websockets.connect( url ) as websocket:
                    #print( '(read_ws) CONNECTED TO WS', url )
                    not_timeout = True
                    while not_timeout:
                        try:
                            resp = await asyncio.wait_for( websocket.recv(), timeout=0.1 )
                            print( '(read_ws) JUST READ', resp )
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
                        #print( '(write_stdin) WRITING', buf )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        print( 'JUST GOT', data )
        if self.input_value_type == 'BINARY':
            data = data.encode( 'utf-8' )

        if self.input_delimiter:
            inp = [ i for i in data.split( self.input_delimiter ) if i ]
        else:
            inp = [ data ]

        print( 'INP IS NOW', inp )
        self.BUFFER.extend( inp )
        print( 'BUFFER IS NOW', self.BUFFER )

        if data == self.input_end:
            self.service_quit( 'Got end delimiter on STDIN, quitting!' )
        

    
    async def input_stdin_run( self, cmd ):
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE )

        await asyncio.gather(
            self.write_stdin( proc.stdin ),
            self.read_file( file_path ) )


    async def input_stdinhttp_run( self, cmd, url ):
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE )

        await asyncio.gather( self.read_file( file_path ) )

    async def input_filehttp_run( self, cmd, file_path, url ):
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
            try:
                loop = asyncio.get_event_loop()
            except:
                loop = asyncio.new_event_loop()
            loop.run_until_complete( self.ws( i, callback ) )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
        while not self.all_setup():
            await asyncio.sleep( 0.1 )
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
                self.nc_client.close()
                self.service_quit( 'NETCAT process ended, quitting!' )
                return None

    def output_callback( self, data ):
        err = 'Trying to call output_callback directly from APiBaseAgent. This method should be overriden!'
        raise APiCallbackException( err )

    def service_start( self ):
        '''
        Start main thread dealing with service input/output.
        '''
        try:
            if self.stdinout_thread:
                self.stdinout_thread.start()
            if self.stdinfile_thread:
                self.stdinfile_thread.start()
            if self.stdinhttp_thread:
                self.stdinhttp_thread.start()
            if self.stdinws_thread:
                self.stdinws_thread.start()
            if self.stdinnc_thread:
                self.stdinnc_thread.start()
            if self.stdinncrec_thread:
                self.stdinncrec_thread.start()
            if self.filestdout_thread:
                self.filestdout_thread.start()
            if self.filefile_thread:
                self.filefile_thread.start()
            if self.filehttp_thread:
                self.filehttp_thread.start()
            if self.filews_thread:
                self.filews_thread.start()
            if self.filenc_thread:
                self.filenc_thread.start()
            if self.filencrec_thread:
                self.filencrec_thread.start()
            if self.nc_output_thread:
                self.nc_output_thread.start()
            if self.httpstdout_thread:
                self.httpstdout_thread.start()
            if self.httpfile_thread:
                self.httpfile_thread.start()
            if self.httphttp_thread:
                self.httphttp_thread.start()
            if self.httpws_thread:
                self.httpws_thread.start()
            if self.httpnc_thread:
                self.httpnc_thread.start()
            if self.httpncrec_thread:
                self.httpncrec_thread.start()
            if self.wsstdout_thread:
                self.wsstdout_thread.start()
            if self.wsfile_thread:
                self.wsfile_thread.start()
            if self.wshttp_thread:
                self.wshttp_thread.start()
            if self.wsws_thread:
                self.wsws_thread.start()
            if self.wsnc_thread:
                self.wsnc_thread.start()
            if self.wsncrec_thread:
                self.wsncrec_thread.start()
            if self.ncstdout_thread:
                self.ncstdout_thread.start()
            if self.ncfile_thread:
                self.ncfile_thread.start()
            if self.nchttp_thread:
                self.nchttp_thread.start()
            if self.ncws_thread:
                self.ncws_thread.start()
            if self.ncnc_thread:
                self.ncnc_thread.start()
            if self.ncncrec_thread:
                self.ncncrec_thread.start()
        except Exception as e:
            pass

    def service_quit( self, msg='' ):
        '''
        Service quitting and clean up method. Joins all threads and
        kills all running processes (services).

        msg - optional message (more or less for debug purposes)
        '''
        #sleep( 0.5 )
        self.say( msg ) # firstly need to clean up and finish all threads
        self.input_ended = True
        #sleep( 0.5 )
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
            #self.stdinout_thread.start()
        elif self.input_type == 'STDIN' and self.output_type[ :4 ] == 'FILE':
            fl = file_re.findall( self.output_type )[ 0 ]
            self.output_file_path = fl
            
            self.input = self.input_stdin

            self.BUFFER = []
            self.stdinfile_thread = Thread( target=asyncio.run, args=( self.input_stdinfile_run( self.cmd, fl ), ) )
            #self.stdinfile_thread.start()
        elif self.input_type == 'STDIN' and self.output_type[ :4 ] == 'HTTP':
            url = http_re.findall( self.output_type )[ 0 ]
            self.output_url = url
            self.input = self.input_stdin
            self.BUFFER = []
            
            self.stdinhttp_thread = Thread( target=asyncio.run, args=( self.input_stdinhttp_run( self.cmd, url ), ) )
            #self.stdinhttp_thread.start()

        elif self.input_type == 'STDIN' and self.output_type[ :2 ] == 'WS':
            url = ws_re.findall( self.output_type )[ 0 ]
            self.output_url = url
            self.input = self.input_stdin
            self.BUFFER = []

            self.stdinws_thread = Thread( target=asyncio.run, args=( self.input_stdinws_run( self.cmd, url ), ) )
            #self.stdinws_thread.start()

        elif self.input_type == 'STDIN' and self.output_type[ :6 ] == 'NETCAT':
            host, port, udp = netcat_re.findall( self.output_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''
            self.input = self.input_stdin
            self.BUFFER = []

            self.stdinnc_thread = Thread( target=asyncio.run, args=( self.input_stdinnc_run( self.cmd, self.nc_host, self.nc_port, self.nc_udp ), ) )
            #self.stdinnc_thread.start()
            self.stdinncrec_thread = Thread( target=self.read_nc, args=( self.nc_host, self.nc_port, self.nc_udp ) )
            #self.stdinncrec_thread.start()
            
        elif self.input_type[ :4 ] == 'FILE' and self.output_type in ( 'STDOUT', 'STDERR' ):
            fl = file_re.findall( self.input_type )[ 0 ]
            self.input_file_path = fl
            self.input_file_written = False
            self.input = self.input_file
            self.filestdout_thread = Thread( target=asyncio.run, args=( self.input_file_run( self.cmd ), ) )
            #self.filestdout_thread.start()
        elif self.input_type[ :4 ] == 'FILE' and self.output_type[ :4 ] == 'FILE':
            infl = file_re.findall( self.input_type )[ 0 ]
            outfl = file_re.findall( self.output_type )[ 0 ]
            self.input_file_path = infl
            self.output_file_path = outfl
            self.input_file_written = False
            self.input = self.input_file
            self.filefile_thread = Thread( target=asyncio.run, args=( self.input_filefile_run( self.cmd, self.output_file_path ), ) )
            #self.filefile_thread.start()
        elif self.input_type[ :4 ] == 'FILE' and self.output_type[ :4 ] == 'HTTP':
            fl = file_re.findall( self.input_type )[ 0 ]
            self.input_file_path = fl
            self.input_file_written = False
            self.input = self.input_file
            url = http_re.findall( self.output_type )[ 0 ]
            self.output_url = url
            self.filehttp_thread = Thread( target=asyncio.run, args=( self.input_filehttp_run( self.cmd, self.input_file_path, self.output_url ), ) )
            #self.filehttp_thread.start()

        elif self.input_type[ :4 ] == 'FILE' and self.output_type[ :2 ] == 'WS':
            fl = file_re.findall( self.input_type )[ 0 ]
            self.input_file_path = fl
            self.input_file_written = False
            self.input = self.input_file
            url = ws_re.findall( self.output_type )[ 0 ]
            self.output_url = url
            self.filews_thread = Thread( target=asyncio.run, args=( self.input_filews_run( self.cmd, self.input_file_path, self.output_url ), ) )
            #self.filews_thread.start()

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
            #self.filenc_thread.start()
            self.filencrec_thread = Thread( target=self.read_nc, args=( self.nc_host, self.nc_port, self.nc_udp ) )
            #self.filencrec_thread.start() 

        elif self.input_type[ :4 ] == 'HTTP' and self.output_type in ( 'STDOUT', 'STDERR' ):
            url = http_re.findall( self.input_type )[ 0 ]
            self.http_url = url
            self.input = self.input_http 
            self.httpstdout_thread = Thread( target=asyncio.run, args=( self.input_httpstdout_run( self.cmd ),  ) )
            #self.httpstdout_thread.start()
            
        elif self.input_type[ :4 ] == 'HTTP' and self.output_type[ :4 ] == 'FILE':
            url = http_re.findall( self.input_type )[ 0 ]
            self.http_url = url
            self.input = self.input_http
            fl = file_re.findall( self.output_type )[ 0 ]
            self.output_file_path = fl

            
            self.httpfile_thread = Thread( target=asyncio.run, args=( self.input_httpfile_run( self.cmd, self.output_file_path ),  ) )
            #self.httpfile_thread.start()

            
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
                #self.httphttp_thread.start()

        elif self.input_type[ :4 ] == 'HTTP' and self.output_type[ :2 ] == 'WS':
            url = http_re.findall( self.input_type )[ 0 ]
            self.http_url = url
            url = ws_re.findall( self.output_type )[ 0 ]
            self.ws_output_url = url
            self.input = self.input_http

            self.httpws_thread = Thread( target=asyncio.run, args=( self.input_httpws_run( self.cmd, self.ws_output_url ), ) )
            #self.httpws_thread.start()

        
        elif self.input_type[ :4 ] == 'HTTP' and self.output_type[ :6 ] == 'NETCAT':
            url = http_re.findall( self.input_type )[ 0 ]
            self.http_url = url
            host, port, udp = netcat_re.findall( self.output_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''
            self.input = self.input_http

            
            self.httpnc_thread = Thread( target=asyncio.run, args=( self.input_httpnc_run( self.cmd ), ) )
            #self.httpnc_thread.start()
            self.httpncrec_thread = Thread( target=self.read_nc, args=( self.nc_host, self.nc_port, self.nc_udp ) )
            #self.httpncrec_thread.start() 
        
        elif self.input_type[ :2 ] == 'WS' and self.output_type in ( 'STDOUT', 'STDERR' ):
            url = ws_re.findall( self.input_type )[ 0 ]
            self.ws_url = url
            self.input = self.input_ws
            
            self.wsstdout_thread = Thread( target=asyncio.run, args=( self.input_wsstdout_run( self.cmd ), ) )
            #self.wsstdout_thread.start()
        
        elif self.input_type[ :2 ] == 'WS' and self.output_type[ :4 ] == 'FILE':
            url = ws_re.findall( self.input_type )[ 0 ]
            self.ws_url = url
            self.input = self.input_ws
            fl = file_re.findall( self.output_type )[ 0 ]
            self.output_file_path = fl

            
            self.wsfile_thread = Thread( target=asyncio.run, args=( self.input_wsfile_run( self.cmd, self.output_file_path ),  ) )
            #self.wsfile_thread.start()
        
        elif self.input_type[ :2 ] == 'WS' and self.output_type[ :4 ] == 'HTTP':
            url = ws_re.findall( self.input_type )[ 0 ]
            self.ws_url = url
            self.input = self.input_ws
            url = http_re.findall( self.output_type )[ 0 ]
            self.output_url = url
            
            self.wshttp_thread = Thread( target=asyncio.run, args=( self.input_wshttp_run( self.cmd, self.output_url ), ) )
            #self.wshttp_thread.start()
            
        
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
                #self.wsws_thread.start()
            
        
        elif self.input_type[ :2 ] == 'WS' and self.output_type[ :6 ] == 'NETCAT':
            url = ws_re.findall( self.input_type )[ 0 ]
            self.ws_url = url
            self.input = self.input_ws
            host, port, udp = netcat_re.findall( self.output_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''

            
            self.wsnc_thread = Thread( target=asyncio.run, args=( self.input_wsnc_run( self.cmd ), ) )
            #self.wsnc_thread.start()
            self.wsncrec_thread = Thread( target=self.read_nc, args=( self.nc_host, self.nc_port, self.nc_udp ) )
            #self.wsncrec_thread.start()

        
        elif self.input_type[ :6 ] == 'NETCAT' and self.output_type in ( 'STDOUT', 'STDERR' ):
            host, port, udp = netcat_re.findall( self.input_type )[ 0 ]
            self.nc_host = host
            self.nc_port = int( port )
            self.nc_udp = udp != ''
            self.input = self.input_nc
            
            self.ncstdout_thread = Thread( target=asyncio.run, args=( self.input_ncstdout_run( self.cmd ), ) )
            #self.ncstdout_thread.start()

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
            #self.ncfile_thread.start()
            # TODO: find out why only the first output is processed, i.e.
            # ncat writes to the file and closes it seemingly after each
            # input making it possible for read_file() to read it and end
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
            #self.nchttp_thread.start()
            
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
            #self.ncws_thread.start()
            
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
                #self.ncnc_thread.start()
    
                error = True
                while error:
                    try:
                        self.nc_client = nclib.Netcat( ( self.nc_host, self.nc_port ), udp=self.nc_udp )
                        
                        error = False
                    except Exception as e:
                        sleep( 0.1 )
            
                self.ncncrec_thread = Thread( target=self.read_nc, args=( self.nc_host_output, self.nc_port_output, self.nc_udp_output ) )
                #self.ncncrec_thread.start()

                
        else:
            err = 'Invalid input type "%s"\n' % self.input_type
            raise APiAgentDefinitionError( err )

        if self.input_value_type not in [ 'STRING', 'BINARY' ]:
            err = 'Invalid input value type "%s"\n' % self.input_value_type
            raise APiAgentDefinitionError( err )

                


    
class APiChannel( APiBaseAgent ):
    '''Channel agent.'''

    REPL_STR = '"$$$API_THIS_IS_VARIABLE_%s$$$"'
    def __init__( self, channelname, name, password, holon, token, portrange, channel_input=None, channel_output=None, transformer=None ):
        self.channelname = channelname
        self.holon = holon
        super().__init__( name, password, token )
        
        self.kb = swipl()
        self.var_re = re.compile( r'[\?][a-zA-Z][a-zA-Z0-9-_]*' )

        self.sender_agents = []
        self.receiver_agents = []

        self.min_port, self.max_port = portrange

        self.attach_servers = []
        self.subscribe_servers = []

        self.agree_message_template = {}
        self.agree_message_template[ 'performative' ] = 'agree'
        self.agree_message_template[ 'ontology' ] = 'APiDataTransfer'
        self.agree_message_template[ 'auth-token' ] = self.auth

        self.refuse_message_template = {}
        self.refuse_message_template[ 'performative' ] = 'refuse'
        self.refuse_message_template[ 'ontology' ] = 'APiDataTransfer'
        self.refuse_message_template[ 'auth-token' ] = self.auth
        
        self.input = channel_input
        self.output = channel_output
        self.transformer = transformer

        
        # TODO: return map function based on channel_input/output
        # descriptor (can be JSON, XML, REGEX, TRANSFORMER, TRANSPARENT)
        # * JSON -> JSON input or output
        # XML -> XML input or output
        # * REGEX -> Python style regex (with named groups) input
        # TRANSFORMER -> read definition from channel description (.cd) file
        # * TRANSPARENT -> no mapping needed, just forward
        #
        # * -> Done!

        
        if not self.input or not self.output:
            if self.transformer:
                self.map = self.map_transformer
            else:
                # TRANSPARENT channel (default)
                self.map = lambda x: x
        else:
            if self.transformer:
                err = "Both input/output combination and transformer defined. I don't know which mapping to use."
                raise APiChannelDefinitionError( err )
        
            
            elif self.input.startswith( 'regex( ' ):
                reg = self.input[ 7:-2 ]
                print( 'RE', reg )
                self.input_re = re.compile( reg )
                self.map = self.map_re
            elif self.input.startswith( 'json( ' ):
                self.input_json = self.input[ 6:-2 ]
                self.kb.query( 'use_module(library(http/json))' )
                cp = self.input_json
                replaces = {}
                for var in self.var_re.findall( self.input_json ):
                    rpl = self.REPL_STR % var
                    replaces[ rpl[ 1:-1 ] ] = var
                    cp = cp.replace( var, rpl )
                query = " APIRES = ok, open_string( '%s', S ), json_read_dict( S, X ). " % cp
                res = self.kb.query( query )
                prolog_json = res[ 0 ][ 'X' ]
                for k, v in replaces.items():
                    prolog_json = prolog_json.replace( k, 'X' + v[ 1: ] )

                self.input_json = prolog_json
                    
                self.map = self.map_json
            elif self.input.startswith( 'xml( ' ):
                # TODO: Implement XML
                raise NotImplementedError( NIE )
                

    def map( self, data ):
        pass

    def map_re( self, data ):
        print( 'MAPRE DATA', data )
        match = self.input_re.match( data )
        print( 'MAPRE MATCH', match )
        vars = self.input_re.groupindex.keys()
        print( 'MAPRE MATCH', vars )
        results = {}
        if not match:
            return ''
        for i in vars:
            results[ i ] = match.group( i )
        query = ''
        for var, val in results.items():
            query += 'X' + var + " = '" + val + "', "
        query = 'APIRES = ok, ' + query[ :-2 ]
        res = self.kb.query( query )
        return self.format_output( res )


    def format_output( self, res ):
        output = self.output
        for var, val in res[ 0 ].items():
            output = output.replace( '?' + var[ 1: ], val )
        return output
            

    def map_transformer( self, data ):
        # TODO: Implement transformer
        raise NotImplementedError( NIE )

    def map_json( self, data ):
        query = " APIRES = ok, open_string( '%s', S ), json_read_dict( S, X ). " % data
        res = self.kb.query( query )
        prolog_json = res[ 0 ][ 'X' ]
        query = " APIRES = ok, X = %s, Y = %s, X = Y. " % ( prolog_json, self.input_json )
        res = self.kb.query( query )
        del res[ 0 ][ 'X' ]
        del res[ 0 ][ 'Y' ]
        return self.format_output( res )

    def map_xml( self, data ):
        # TODO: Implement XML
        raise NotImplementedError( NIE )

    def get_free_port( self ):
        '''Get a free port on the host'''
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        port = self.min_port
        while port <= self.max_port:
            try:
                sock.bind( ( '', port ) )
                sock.close()
                return port
            except OSError:
                port += 1
        raise IOError( 'No free ports in range %d - %d' % ( self.min_port, self.max_port ) )

    def get_ip( self ):
        '''Get the current IP address of the agent'''
        # TODO: Verify this works with outside network
        #       addresses!
        s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        try:
            # doesn't even have to be reachable
            s.connect( ( '10.255.255.255', 1 ) )
            IP = s.getsockname()[ 0 ]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
    def get_server( self, srv_type ):
        '''Get a NetCat server for sending or receiving'''
        # TODO: Deal with TCP/UDP selection
        port =  self.get_free_port()
        host = self.get_ip()

        self.say( host, port )

        srv_created = False
        while not srv_created:
            try:
                srv = nclib.TCPServer( ( '0.0.0.0', port ) )
                srv_created = True
                print( 'SERVER CONNECTED AT PORT', port )
            except OSError as e:
                port = self.get_free_port()

                
        if srv_type == 'attach':
            self.attach_servers.append( srv )
            print( 'ATTACH SERVERS:', self.attach_servers )
        elif srv_type == 'subscribe':
            self.subscribe_servers.append( srv )
            print( 'SUBSCRIBE SERVERS:', self.subscribe_servers )
        else:
            raise APiChannelDefinitionError( 'Unknown server type:', srv_type )
        
        return host, str( port ), 'tcp'


    class Subscribe( CyclicBehaviour ):
        '''Agent wants to listen or write to channel'''
        async def run( self ):
            msg = await self.receive( timeout=0.1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(Subscribe) Message verified, processing ...' )
                    self.agent.receiver_agents.append( str( msg.sender ) )
                    metadata = deepcopy( self.agent.agree_message_template )
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    metadata[ 'agent' ] = self.agent.channelname
                    if msg.metadata[ 'performative' ] == 'subscribe':
                        metadata[ 'type' ] = 'input'
                        server, port, protocol = self.agent.get_server( 'subscribe' )
                        print( 'ADDED subscribe server', server, port )
                    elif msg.metadata[ 'performative' ] == 'request':
                        metadata[ 'type' ] = 'output'
                        server, port, protocol = self.agent.get_server( 'attach' )
                        print( 'ADDED attach server', server, port )
                    else:
                        self.agent.say( 'Unknown message' )
                        metadata = self.agent.refuse_message_template
                        metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                        metadata[ 'reason' ] = 'unknown-message'
                        await self.agent.schedule_message( str( msg.sender ), metadata=metadata )

                    
                    metadata[ 'server' ] = server
                    metadata[ 'port' ] = port
                    metadata[ 'protocol' ] = protocol
                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )
                    await asyncio.sleep( 0.1 )
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )
                    metadata = self.agent.refuse_message_template
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    metadata[ 'reason' ] = 'security-policy'
                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )
    class Forward( CyclicBehaviour ):
        '''Receive inputs, map them to outputs and send to subscribers'''
        # TODO: Test this behaviour
        async def run( self ):

            def iter_clients( srv ):
                srv.sock.settimeout( 0.1 )
                try:
                    c, a = srv.sock.accept()
                    client = nclib.Netcat( sock=c, server=a )
                    yield client
                    for client in srv:
                        yield client
                except Exception as e:
                    self.agent.say( e, srv.addr )
                    return
            
            if self.agent.attach_servers:
                for srv in self.agent.attach_servers:
                    for client in iter_clients( srv ):
                        self.agent.say( 'CLIENT', client, srv.addr )
                        result = client.recv_until( self.agent.delimiter, timeout=0.2 )
                        self.agent.say( 'RESULT', result, srv.addr )
                        if result:
                            self.agent.say( 'MAPPING RESULT', result.decode(), srv.addr )
                            msg = self.agent.map( result.decode() )
                            self.agent.say( 'MSG', msg, srv.addr )
                            self.agent.say( 'SERVER LIST 1', self.agent.subscribe_servers )
                            if self.agent.subscribe_servers:
                                self.agent.say( 'SERVER LIST 2', self.agent.subscribe_servers )
                                for srv_out in self.agent.subscribe_servers:
                                    self.agent.say( 'OUT SERVER', srv_out, srv_out.addr )
                                    for client_out in srv_out:
                                        self.agent.say( 'SENDING MSG TO', client_out, client_out.peer )
                                        client_out.sendline( msg.encode() )
                                        self.agent.say( 'DONE SENDING MSG' )
                    
    async def setup(self):
        super().setup()
            
        bsubs = self.Subscribe()
        bsubs_template = Template(
            metadata={ 
                       "ontology": "APiDataTransfer"
            } # "performative": "subscribe",
        )      
        self.add_behaviour( bsubs, bsubs_template )
        
        bfwd = self.Forward()
        self.add_behaviour( bfwd )




class APiAgent( APiBaseAgent ):
    '''Service wrapper agent.'''

    # TODO: Sort methods / coroutines by type and write documentation
    def __init__( self, agentname, name, password, holon, token, args=[], flows=[] ):
        '''
        Constructor.
        agentname - name as in agent definition (.ad) file.
        name - XMPP/Jabber username
        password - XMPP/Jabber password
        holon - parent holon
        token - token from holon
        args - list of arguments (from APi statement)
        flows - list of message flows (from APi statement)
        '''        
        try:
            fh = open( agentname + '.ad' )
        except IOError as e:
            err = 'Missing agent definition file or permission issue.\n' + str( e )
            raise APiIOError( err )
        super().__init__( name, password, token )
        
        self.agentname = agentname
        self.holon = holon
        self._load( fh )
        self.agentargs = args

        self.flows = []
        for f in flows:
            if len( f ) > 2:
                pairs = [ i for i in pairwise( f ) ]
                self.flows.extend( pairs )
            else:
                self.flows.append( f )


        # inputs are not allways on the LHS
        # and outputs are not allways on the RHS. We need
        # to analyze the flows, if self is on the RHS it is
        # an input to the process and if self is on the
        # LHS it is an output. If self isn't present
        # then it is a forward (not processed LHS input is
        # forwarded directly to RHS output)
        self.input_channels = set( i[ 0 ] for i in self.flows if i[ 1 ] == 'self' )
        self.output_channels = set( i[ 1 ] for i in self.flows if i[ 0 ] == 'self' )
        self.forward_channels = set( i for i in self.flows if i[ 0 ] != 'self' and i[ 1 ] != 'self' )

        print( self.flows )
        print( self.input_channels )
        print( self.output_channels )
        print( self.forward_channels )

        self.input_channel_query_buffer = []
        self.output_channel_query_buffer = []

        self.input_channel_servers = {}
        self.output_channel_servers = {}

        self.query_msg_template = {}
        self.query_msg_template[ 'performative' ] = 'query-ref'
        self.query_msg_template[ 'ontology' ] = 'APiQuery'
        self.query_msg_template[ 'auth-token' ] = self.auth

        self.subscribe_msg_template = {}
        self.subscribe_msg_template[ 'performative' ] = 'subscribe'
        self.subscribe_msg_template[ 'ontology' ] = 'APiDataTransfer'
        self.subscribe_msg_template[ 'auth-token' ] = self.auth

        self.attach_msg_template = {}
        self.attach_msg_template[ 'performative' ] = 'request'
        self.attach_msg_template[ 'ontology' ] = 'APiDataTransfer'
        self.attach_msg_template[ 'auth-token' ] = self.auth

        self.agree_msg_template = {}
        self.agree_msg_template[ 'performative' ] = 'agree'
        self.agree_msg_template[ 'ontology' ] = 'APiScheduling'
        self.agree_msg_template[ 'auth-token' ] = self.auth

        self.refuse_msg_template = {}
        self.refuse_msg_template[ 'performative' ] = 'refuse'
        self.refuse_msg_template[ 'ontology' ] = 'APiScheduling'
        self.refuse_msg_template[ 'auth-token' ] = self.auth
        # Add reason in actual behaviour (e.g. service-failed, security-policy)

        self.inform_msg_template = {}
        self.inform_msg_template[ 'performative' ] = 'inform'
        self.inform_msg_template[ 'ontology' ] = 'APiScheduling'
        self.inform_msg_template[ 'auth-token' ] = self.auth
        # Add exit-status (finished, error) and error-message (actual stacktrace, error code etc.); or add status (ready)

        for i in self.input_channels:
            try:
                self.subscribe_to_channel( i, 'input' )
            except NotImplementedError as e:
                print( 'Not implemented for', i )
        for i in self.output_channels:
            try:
                self.subscribe_to_channel( i, 'output' )
            except NotImplementedError as e:
                print( 'Not implemented for', i )
        for i, o in self.forward_channels:
            try:
                self.subscribe_to_channel( i, 'input' )
            except NotImplementedError as e:
                print( 'Not implemented for', i )
            try:
                self.subscribe_to_channel( o, 'output' )
            except NotImplementedError as e:
                print( 'Not implemented for', o )

        self.input_ended = False

        self.shell_ip_stdin = None
        self.shell_port_stdin = None
        self.shell_ip_stdout = None
        self.shell_port_stdout = None
        self.shell_buffer = []

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
            
        
    
    def output_callback( self, data ):
        '''
        Output callback method.
        data - data read from service.
        '''
        self.shell_buffer.append( data )
        self.say( 'I just received:', data )
        for srv in self.output_channel_servers.values():
            print( 'SENDING', data.encode(), 'to', srv[ 'port' ], '... ', end='' )
            sent = False
            srv[ 'socket' ] = nclib.Netcat( ( srv[ 'server' ], srv[ 'port' ] ) )
            while not sent:
                try:
                    srv[ 'socket' ].sendline( data.encode() )
                    sent = True
                    print( ' DONE!' )
                except ( BrokenPipeError, ConnectionResetError ):
                    print( 'ERROR SENDING', data, 'TO', srv[ 'server' ], srv[ 'port' ], '(BROKEN PIPE)' )
                    print( 'TRYING TO RECONNECT' )
                    srv[ 'socket' ] = nclib.Netcat( ( srv[ 'server' ], srv[ 'port' ] ) )
                    

    def subscribe_to_channel( self, channel, channel_type ):
        # TODO: Implement channel subscription (sender, receiver)
        # Channel types:
        # NIL -> sends stop to agent (0 process)
        # VOID -> sends output to /dev/null
        # STDIN -> reads input from stdin
        # STDOUT/STDERR -> writes output to STDIN/STDERR
        # <name> -> gets instructions from channel on how
        #           to connect (via Netcat)
        if channel_type == 'input':
            if channel == 'NIL':
                err = 'Input cannot be 0 (NIL)'
                raise APiChannelDefinitionError( err )
            elif channel == 'VOID':
                err = 'Input cannot be VOID'
                raise APiChannelDefinitionError( err )
            elif channel == 'STDOUT':
                err = 'Input cannot be STDOUT'
                raise APiChannelDefinitionError( err )
            elif channel == 'STDERR':
                err = 'Input cannot be STDERR'
                raise APiChannelDefinitionError( err )
            elif channel == 'STDIN':
                self.start_shell_client( prompt=True, await_stdin=True )
            else:
                self.say( 'Adding input channel', channel )
                self.input_channel_query_buffer.append( channel )
        elif channel_type == 'output':
            if channel == 'NIL':
                # TODO: stop agent
                raise NotImplementedError( NIE )
            elif channel == 'VOID':
                # TODO: send to /dev/null (i.e. do nothing )
                raise NotImplementedError( NIE )
            elif channel == 'STDOUT':
                self.start_shell_client( print_stdout=True )
            elif channel == 'STDERR':
                self.start_shell_client( print_stderr=False )
            elif channel == 'STDIN':
                err = 'Output cannot be STDIN'
                raise APiChannelDefinitionError( err )
            else:
                # TODO: send message to channel agent
                # and get instructions on how to
                # connect
                self.say( 'Adding output channel', channel )
                self.output_channel_query_buffer.append( channel )


    def start_shell_stdin( self, prompt=False ):
        '''
        Start socket server for STDIN shell. If prompt is True
        write standard prompt (agentname :- ) before each
        input.
        '''
        self.shell_socket_stdin = socket.socket()
        self.shell_socket_stdin.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        self.shell_socket_stdin.bind( ( '0.0.0.0', 0 ) )
        self.shell_socket_stdin.listen( 0 )
        self.shell_ip_stdin, self.shell_port_stdin = self.shell_socket_stdin.getsockname()

        self.shell_client_stdin, self.shell_client_stdin_addr = self.shell_socket_stdin.accept()

        if prompt:
            self.prompt = '\n%s (agent) :- ' % self.name
        else:
            self.prompt = None

        BUFFER_SIZE = 1024

        self.shell_client_stdin.settimeout( 0.1 )

        threads = []

        error = False
        while True:
            try:
                if self.prompt and not error:
                    self.shell_client_stdin.send( self.prompt.encode() )
                inp = self.shell_client_stdin.recv( BUFFER_SIZE ).decode()
                if inp == "exit":
                    self.shell_client_stdin.close()
                    self.shell_socket_stdin.close()
                    break
                if self.input_ended:
                    self.shell_client_stdin.send( 'Input end delimiter received, agent is shutting down...'.encode() )
                    self.shell_client_stdin.close()
                    self.shell_socket_stdin.close()
                    break
                else:
                    t = Thread( target=self.input, args=( inp, ) )
                    t.start()
                    threads.append( t )
                error = False                                
            except Exception as e:
                error = True
                sleep( 0.1 )

        # cleanup
        for t in threads:
            t.join()

    def start_shell_stdout( self ):
        '''
        Start socket server for STDOUT/STDERR shell. 
        '''

        self.shell_socket_stdout = socket.socket()
        self.shell_socket_stdout.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        self.shell_socket_stdout.bind( ( '0.0.0.0', 0 ) )
        self.shell_socket_stdout.listen( 0 )
        self.shell_ip_stdout, self.shell_port_stdout = self.shell_socket_stdout.getsockname()

        self.shell_client_stdout, self.shell_client_stdout_addr = self.shell_socket_stdout.accept()

        BUFFER_SIZE = 1024

        self.shell_client_stdout.settimeout( 0.1 )

        error = False
        while True:
            try:
                while self.shell_buffer:
                    if len( self.shell_buffer ) > 0:
                        data = self.shell_buffer.pop( 0 )
                        self.shell_client_stdout.send( data.encode() )
                    if self.output_end:
                        if data[ :-1 ] == self.output_end:
                            self.shell_client_stdout.send( 'Output end delimiter received, agent is shutting down...'.encode() )
                            self.shell_client_stdout.shutdown( 2 )
                            self.shell_client_stdout.close()
                            self.shell_socket_stdout.close()
                            return
                error = False                                
            except Exception as e:
                print( e )
                error = True
                sleep( 0.1 )



            
    def start_shell_client( self, prompt=True, await_stdin=True, print_stdout=True, print_stderr=False ):
        '''
        Start the agents shell client. 
        prompt - use a prompt for STDIN shell (will be ignored if await_stdin is False)
        await_stdin - if True attach agent's input to STDIN (print_stdout and print_stderr will be ignored)
        print_stdout - if True attach agent's output to STDOUT (print_stderr will be ignored)
        print_stderr - if True attach agent's output to STDERR
        '''
        if await_stdin:
            self.shell_stdin_thread = Thread( target=self.start_shell_stdin, args=( prompt, ) )
            self.shell_stdin_thread.start()
        elif print_stdout or print_stderr:
            self.shell_stdout_thread = Thread( target=self.start_shell_stdout )
            self.shell_stdout_thread.start()
        sleep( 0.1 )

        if await_stdin:
            self.shell_ip = self.shell_ip_stdin
            self.shell_port = self.shell_port_stdin
        elif print_stdout or print_stderr:
            self.shell_ip = self.shell_ip_stdout
            self.shell_port = self.shell_port_stdout

            
        # TODO: Move this part to main program (platform or listener).
        # Agent should have a method to return all hosts/ports for
        # active shells so remote clients can connect.
        # Also, implement attach command in core language
        # similar to start (e.g. attach agent1 stdin).
        # Nice to have: implement describe command in core
        # language that will print out an introspection
        # of an agent (i.e. statistics, active shells, flows etc.).
        # Additionally, implement statistics decorator function
        # to collect statistics about flows - i.e. how much
        # input (in bytes and messages), how much output (in bytes
        # and messages) etc.
        if not self.shell_ip and not self.shell_port:
            err = 'The shell has not been initialized'
            raise APiShellInitError( err )
        else:
            agent_tmp_dir = os.path.join( TMP_FOLDER, self.name )
            if not os.path.exists( agent_tmp_dir ):
                os.makedirs( agent_tmp_dir )
            if await_stdin:
                self.dtach_session = os.path.join( TMP_FOLDER, self.name, 'stdin' )
            elif print_stdout:
                self.dtach_session = os.path.join( TMP_FOLDER, self.name, 'stdout' )
            elif print_stderr:
                self.dtach_session = os.path.join( TMP_FOLDER, self.name, 'stderr' )
            else:
                err = 'No input and not output specified!'
                raise APiShellInitError( err )
            cmd = 'dtach -A %s ./../APishc.py %s %d' % ( self.dtach_session, self.shell_ip, self.shell_port )
            if await_stdin:
                cmd += ' --input'
            elif print_stdout:
                cmd += ' --output'
            elif print_stderr:
                cmd += ' --error'
            self.shell_client_proc = pexpect.spawn( cmd )

            def output_filter( s ):
                if 'EOF - dtach terminating' in s.decode():
                    return '\n'.encode()
                return s
            
            self.shell_client_proc.interact( output_filter=output_filter )

        if await_stdin:
            self.shell_stdin_thread.join()
        elif print_stdout or print_stderr:
            self.shell_stdout_thread.join()

    def get_channel_name( self, address ):
        '''Ugly hack'''
        return list( self.address_book.keys() )[ list( self.address_book.values() ).index( address ) ]

    
    def all_setup( self ):
        # TODO: Deal with forward channels
        try:
            connected_inputs = set( [ ch for ch in self.input_channel_servers.keys() ] )
            if self.input_channels == connected_inputs:
                connected_outputs = set( [ ch for ch in self.output_channel_servers.keys() ] )
                if self.output_channels == connected_outputs:
                    return True
        except AttributeError:
            pass
        return False

        
    async def setup( self ):        
        super().setup()
        
        self.behaviour_gca = self.GetChannelAdresses()
        self.add_behaviour( self.behaviour_gca )

        self.behaviour_stic = self.SubscribeToInputChannels()
        self.add_behaviour( self.behaviour_stic )

        self.behaviour_atoc = self.AttachToOutputChannels()
        self.add_behaviour( self.behaviour_atoc )
        
        self.behaviour_qc = self.QueryChannels()
        bqc_template = Template(
            metadata={ "ontology": "APiQuery" }
        )
        self.add_behaviour( self.behaviour_qc, bqc_template )

        self.behaviour_sic = self.SetupInputChannels()
        bsic_template = Template(
            metadata={ "ontology": "APiDataTransfer", "type":"input" }
        )
        self.add_behaviour( self.behaviour_sic, bsic_template )

        self.behaviour_soc = self.SetupOutputChannels()
        bsoc_template = Template(
            metadata={ "ontology": "APiDataTransfer", "type":"output" }
        )
        self.add_behaviour( self.behaviour_soc, bsoc_template )

        self.behaviour_l = self.Listen()
        self.add_behaviour( self.behaviour_l )

        self.behaviour_ss = self.StartService()
        bss_template = Template(
            metadata={ "ontology": "APiScheduling", "action":"start" }
        )
        self.add_behaviour( self.behaviour_ss, bss_template )
        

    class GetChannelAdresses( OneShotBehaviour ):
        async def run( self ):
            self.agent.say( 'Inputs:', self.agent.input_channel_query_buffer )
            for inp in self.agent.input_channel_query_buffer:
                metadata = self.agent.query_msg_template
                metadata[ 'reply-with' ] = str( uuid4().hex )
                metadata[ 'channel' ] = inp
                await self.agent.schedule_message( self.agent.holon, metadata=metadata )

            self.agent.say( 'Outputs:', self.agent.output_channel_query_buffer )    
            for out in self.agent.output_channel_query_buffer:
                self.agent.say( 'Looking up channel', out, 'in addressbook' )
                try:
                    channel = self.agent.address_book[ out ]
                    self.agent.say( 'Got channel', out, 'address', channel )
                    await asyncio.sleep( 0.1 )
                except KeyError:
                    self.agent.say( 'Could not find channel', out, 'in address book, querying' )
                    metadata = self.agent.query_msg_template
                    metadata[ 'reply-with' ] = str( uuid4().hex )
                    metadata[ 'channel' ] = out
                    await self.agent.schedule_message( self.agent.holon, metadata=metadata )

    class SubscribeToInputChannels( OneShotBehaviour ):
        async def run( self ):
            await self.agent.behaviour_gca.join()
            self.agent.say( 'Subscribing to inputs:', self.agent.input_channel_query_buffer )
            for inp in self.agent.input_channel_query_buffer:
                while inp not in self.agent.address_book:
                    await asyncio.sleep( 0.1 )
                channel = self.agent.address_book[ inp ]
                metadata = self.agent.subscribe_msg_template
                metadata[ 'reply-with' ] = str( uuid4().hex )
                await self.agent.schedule_message( channel, metadata=metadata )

    class AttachToOutputChannels( OneShotBehaviour ):
        async def run( self ):
            await self.agent.behaviour_stic.join()
            self.agent.say( 'Attaching to outputs', self.agent.output_channel_query_buffer )
            
            for out in self.agent.output_channel_query_buffer:
                while out not in self.agent.address_book:
                    await asyncio.sleep( 0.1 )
                channel = self.agent.address_book[ out ]
                metadata = self.agent.attach_msg_template
                metadata[ 'reply-with' ] = str( uuid4().hex )
                await self.agent.schedule_message( channel, metadata=metadata )
        
    

    class QueryChannels( CyclicBehaviour ):
        '''Ask holon for channel addresses'''
        async def run( self ):
            msg = await self.receive( timeout=0.1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(QueryChannels) Message verified, processing ...' )
                    channel = msg.metadata[ 'address' ]
                    try:
                        self.agent.input_ack.remove( msg.metadata[ 'in-reply-to' ] )

                        if msg.metadata[ 'performative' ] == 'refuse':
                            self.agent.say( 'Error getting channel address due to ' + msg.metadata[ 'reson' ] )
                            self.kill()
                        elif msg.metadata[ 'success' ] == 'true':
                            self.agent.address_book[ msg.metadata[ 'agent' ] ] = channel
                        else:
                            self.agent.say( 'Error getting channel address. Channel unknown to holon.' )
                            self.kill()
                            
                    except KeyError:
                        self.agent.say( 'I have no memory of this message (%s). (awkward Gandalf look)' % msg.metadata[ 'in-reply-to' ] )           
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )
                
    class SetupInputChannels( CyclicBehaviour ):
        async def run( self ):
            await self.agent.behaviour_atoc.join()
            msg = await self.receive( timeout=1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(SetupInputChannels) Message verified, processing ...' )
                    try:
                        self.agent.input_ack.remove( msg.metadata[ 'in-reply-to' ] )
                        if msg.metadata[ 'performative' ] == 'refuse':
                            self.agent.say( 'Error connecting to channel address due to ' + msg.metadata[ 'reason' ] )
                            self.kill()
                        else:
                            channel = msg.metadata[ 'agent' ]
                            servers = self.agent.input_channel_servers
                            self.agent.say( '(SetupInputChannels) Setting up', msg.metadata[ 'type' ], 'channel', channel )
                            servers[ channel ] = {}
                            servers[ channel ][ 'server' ] = msg.metadata[ 'server' ]
                            servers[ channel ][ 'port' ] = int( msg.metadata[ 'port' ] )
                            servers[ channel ][ 'protocol' ] = msg.metadata[ 'protocol' ]
                            servers[ channel ][ 'socket' ] = nclib.Netcat( ( msg.metadata[ 'server' ], int( msg.metadata[ 'port' ] ) ) )

                            if len( self.agent.output_channel_servers ) == len( self.agent.output_channels ) and len( self.agent.input_channel_servers ) == len( self.agent.input_channels ):
                                metadata = deepcopy( self.agent.inform_msg_template )
                                metadata[ 'status' ] = 'ready'
                                await self.agent.schedule_message( self.agent.holon, metadata=metadata )
                        
                    except KeyError:
                        self.agent.say( 'I have no memory of this message (%s). (awkward Gandalf look)' % msg.metadata[ 'in-reply-to' ])
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )

    class SetupOutputChannels( CyclicBehaviour ):
        async def run( self ):
            await self.agent.behaviour_atoc.join()
            msg = await self.receive( timeout=1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(SetupOutputChannels) Message verified, processing ...' )
                    try:
                        self.agent.input_ack.remove( msg.metadata[ 'in-reply-to' ] )
                        if msg.metadata[ 'performative' ] == 'refuse':
                            self.agent.say( 'Error connecting to channel address due to ' + msg.metadata[ 'reason' ] )
                            self.kill() # TODO: Inform holon about failure
                        else:
                            channel = msg.metadata[ 'agent' ]
                            servers = self.agent.output_channel_servers
                            self.agent.say( '(SetupOutputChannels) Setting up', msg.metadata[ 'type' ], 'channel', channel )
                            servers[ channel ] = {}
                            servers[ channel ][ 'server' ] = msg.metadata[ 'server' ]
                            servers[ channel ][ 'port' ] = int( msg.metadata[ 'port' ] )
                            servers[ channel ][ 'protocol' ] = msg.metadata[ 'protocol' ]
                            servers[ channel ][ 'socket' ] = nclib.Netcat( ( msg.metadata[ 'server' ], int( msg.metadata[ 'port' ] ) ) )

                            if len( self.agent.output_channel_servers ) == len( self.agent.output_channels ) and len( self.agent.input_channel_servers ) == len( self.agent.input_channels ):
                                metadata = deepcopy( self.agent.inform_msg_template )
                                metadata[ 'status' ] = 'ready'
                                await self.agent.schedule_message( self.agent.holon, metadata=metadata )
                        
                    except KeyError:
                        self.agent.say( 'I have no memory of this message (%s). (awkward Gandalf look)' % msg.metadata[ 'in-reply-to' ])
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )

    class Listen( CyclicBehaviour ):
        
        async def run( self ):
            # TODO: Deal with forward channels
            if self.agent.all_setup():
                for srv in self.agent.input_channel_servers.values():
                    result = srv[ 'socket' ].recv_until( self.agent.delimiter, timeout=0.2 )
                    sleep( 0.5 ) # TODO: Investigate if this line is needed
                    if result:
                        self.agent.say( '(Listen) Received', result, 'from server', srv[ 'server' ], srv[ 'port' ] )
                        self.agent.input( result.decode() )
                        print( '!'*100 )

    class StartService( CyclicBehaviour ):
        async def run( self ):
            msg = await self.receive( timeout=1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(StartService) Message verified, processing ...' )
                    self.agent.say( '(StartService) Holon has scheduled us to start. Starting service!' )
                    self.agent.service_start()
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )
                    

        
class APiHolon( APiTalkingAgent ):
    '''A holon created by an .api file.'''
    '''TODO: Finish holon implementation'''
    def __init__( self, holonname, name, password, agents, channels, environment, holons, execution_plan ):
        self.token = str( uuid4().hex )
        super().__init__( name, password, str( uuid4().hex ) )
        self.holonname = holonname
        self.address = str( self.jid.bare() )
        self.namespace = APiNamespace()
        self.registrar = APiRegistrationService( holonname )

        self.setup_environment( environment )

        self.channels = {}
        for c in channels:
            self.setup_channel( c )

        self.agents = {}
        for a in agents:
            self.setup_agent( a )

        self.holons = {}
        for h in holons:
            self.setup_holon( h )

        self.execution_plan = None
        self.setup_execution( execution_plan )

        self.all_started = False # Indicate if execution plan has been started already
        self.instantiate_all()

        self.query_message_template = {}
        self.query_message_template[ 'performative' ] = 'inform-ref'
        self.query_message_template[ 'ontology' ] = 'APiQuery'
        self.query_message_template[ 'auth-token' ] = self.auth

        self.refuse_message_template = {}
        self.refuse_message_template[ 'performative' ] = 'refuse'
        self.refuse_message_template[ 'ontology' ] = 'APiQuery'
        self.refuse_message_template[ 'auth-token' ] = self.auth
        self.refuse_message_template[ 'reason' ] = 'security-policy'

        self.request_message_template = {}
        self.request_message_template[ 'performative' ] = 'request'
        self.request_message_template[ 'ontology' ] = 'APiScheduling'
        self.request_message_template[ 'auth-token' ] = self.auth
        # Add action in actual behaviour (start or stop)

        self.confirm_message_template = {}
        self.confirm_message_template[ 'performative' ] = 'confirm'
        self.confirm_message_template[ 'ontology' ] = 'APiScheduling'
        self.confirm_message_template[ 'auth-token' ] = self.auth

        

    def setup_agent( self, agent ):
        '''TODO: This method should create and start an agent 
                 depending on type (local Unix, Docker, other 
                 container ...). If it is a container type
                 there should be a possibility to schedule it
                 directly on some orchestration platform (i.e.
                 Kubernetes, Docker Swarm or similar). This should
                 be specified in the agent definition file (.ag).'''
        self.say( 'Registering agent', agent[ 'name' ] )
        address, password = self.registrar.register( agent[ 'name' ] )
        agent[ 'cmd' ] = 'python3 ../agent.py "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % ( agent[ 'name' ], address, password, self.address, self.token, json.dumps( agent[ 'args' ] ).replace('"','\\"'), json.dumps( agent[ 'flows' ] ).replace('"','\\"') )
        agent[ 'address' ] = address
        agent[ 'status' ] = 'setup'
        self.agents[ agent[ 'name' ] ] = agent

    def setup_channel( self, channel ):
        ''' TODO: Same as above, it should be possible to 
                  create channels in an orchestration platform
                  if specified in the channel definition file.'''
        address, password = self.registrar.register( channel[ 'name' ] )
        self.say( 'Registering channel', channel[ 'name' ] )
        channel[ 'cmd' ] = 'python3 ../channel.py "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % ( channel[ 'name' ], address, password, self.address, self.token, json.dumps( ( self.registrar.min_port, self.registrar.max_port ) ), json.dumps( channel[ 'input' ] ).replace('"','\\"'), json.dumps( channel[ 'output' ] ).replace('"','\\"'), json.dumps( channel[ 'transformer' ] ).replace('"','\\"') )
        channel[ 'address' ] = address
        channel[ 'status' ] = 'setup'
        self.channels[ channel[ 'name' ] ] = channel

    def setup_holon( self, holon ):
        # TODO: implement starting included holons
        pass

    def setup_environment( self, env_spec ):
        # TODO: implement setting up environment
        #       channels (input + output)
        pass

    def setup_execution( self, execution_plan ):
        # TODO: Design and implement execution plans
        pass

    def agent_name_from_address( self, address ):
        # Ugly hack
        address = str( address )
        for name, agent in self.agents.items():
            if agent[ 'address' ] == address:
                return name

    def instantiate_all( self ):
        # Create agent and channel instances
        def start( cmd ):
            return sp.Popen( cmd, stderr=sp.STDOUT, start_new_session=True )
            
        for c in self.channels.values():
            cmd = shlex.split( c[ 'cmd' ] )
            print( 'Running channel with:', cmd )
            c[ 'instance' ] = Thread( target=start, args=( cmd, ) )
            c[ 'instance' ].start()
            c[ 'status' ] = 'started'
                
        for a in self.agents.values():
            cmd = shlex.split( a[ 'cmd' ] )
            print( 'Running agent with:', cmd )
            a[ 'instance' ] = Thread( target=start, args=( cmd, ) )
            a[ 'instance' ].start()
            a[ 'status' ] = 'instantiated'

    async def stop( self ):
        # TODO: implement stopping all agents
        #       and channels by sending them
        #       stopping messages.
        for c in self.channels.values():
            c[ 'instance' ].join()
            
        for a in self.agents.values():
            a[ 'instance' ].join()

        super().stop()
        

    async def setup( self ):
        super().setup()

        bqn = self.QueryName()
        bqn_template =  Template(
            metadata={ "performative": "query-ref",
                       "ontology": "APiQuery"
            }
        )
        self.add_behaviour( bqn, bqn_template )

        bgra = self.GetReadyAgents()
        bgra_template = Template(
            metadata={ "performative": "inform",
                       "ontology": "APiScheduling",
                       "status":"ready" }
        )
        self.add_behaviour( bgra, bgra_template )

        bep = self.ExecutePlan()
        self.add_behaviour( bep )
        
        self.say( self.channels )
        self.say( self.agents )

    class QueryName( CyclicBehaviour ):
        async def run( self ):
            msg = await self.receive( timeout=0.1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(QueryName) Message verified, processing ...' )
                    channel = msg.metadata[ 'channel' ]
                    metadata = self.agent.query_message_template
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    metadata[ 'agent' ] = channel

                    try:
                        ch_address = self.agent.channels[ channel ][ 'address' ]
                        self.agent.say( 'Found channel', channel, 'address is', ch_address )

                        metadata[ 'success' ] = 'true'
                        metadata[ 'address' ] = ch_address
                    except KeyError:
                        self.agent.say( 'Channel', channel, 'not found' )
                        metadata[ 'success' ] = 'false'
                        metadata[ 'address' ] = 'null'
                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )
                        
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )
                    metadata = self.agent.refuse_message_template
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )

    class GetReadyAgents( CyclicBehaviour ):
        async def run( self ):
            msg = await self.receive( timeout=0.1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(QueryNameGetReadyAgents) Message verified, processing ...' )
                    agent = self.agent.agent_name_from_address( msg.sender.bare() )
                    self.agent.say( '(QueryNameGetReadyAgents) Setting agent', agent, 'status to ready.' )
                    self.agent.agents[ agent ][ 'status' ] = 'ready'
                        
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )
                    metadata = self.agent.refuse_message_template
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )

    class ExecutePlan( CyclicBehaviour ):
        async def run( self ):
            if self.agent.execution_plan:
                # TODO: Design and implement execution plans
                pass
            else:
                # Tell all agents to start if they are ready
                all_ready = True
                for agent in self.agent.agents.values():
                    if agent[ 'status' ] != 'ready':
                        all_ready = False
                        break
                if all_ready and not self.agent.all_started:
                    self.agent.say( '(Execute plan) All agents ready, scheduling them for start!' )
                    metadata = deepcopy( self.agent.request_message_template )
                    metadata[ 'action' ] = 'start'
                    for agent in self.agent.agents.values():
                        if agent[ 'name' ] != 'bla_file_stdout':
                            await self.agent.schedule_message( agent[ 'address' ], metadata=metadata )
                    await asyncio.sleep( 15 )
                    print( 'NOW STARTING FILEREADER' )
                    await self.agent.schedule_message( self.agent.agents[ 'bla_file_stdout' ][ 'address' ], metadata=metadata )
                    self.agent.all_started = True
                    
            
        
               
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
        try:
            self.min_port = int( self.descriptor[ 'port-range' ][ 'min' ] )
            self.max_port = int( self.descriptor[ 'port-range' ][ 'max' ] )
        except Exception as e:
            err = 'Holon configuration file has invalid format.\n' + str( e )
            raise APiHolonConfigurationError( err )
            
        
    def register( self, name ):
        server = self.next()
        username = '%s_%s_%s' % ( self.name, name, str( uuid4().hex ) )
        password = str( uuid4().hex )
        url = "https://%s/register/%s/%s" % ( server, username, password )
        try:
            response = requests.get( url, verify=False )
        except requests.exceptions.ConnectionError as e:
            warnings.warn( 'Falling back to registering over insecure HTTP instead of HTTPS', APiHTTPSWarning )
            url = "http://%s/register/%s/%s" % ( server, username, password )
            response = requests.get( url, verify=False )

        host = server.split( ':' )[ 0 ]
        if response.status_code == 200:
            result = response.content.decode('utf-8')
            if result == 'OK':
                return (  '%s@%s' % ( username, host ), password )
            else:
                for i in range( self.MAX_RETRIES ):
                    response = requests.get( url, verify=False )
                    result = response.content.decode('utf-8')
                    if result == 'OK':
                        return ( '%s@%s' % ( username, host ), password )
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
        self.STACK = []
        self.PARSING_XML = False


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


    # Enter a parse tree produced by APiParser#iflow.
    def enterIflow(self, ctx:APiParser.IflowContext):
        pass

    # Exit a parse tree produced by APiParser#iflow.
    def exitIflow(self, ctx:APiParser.IflowContext):
        pass


    # Enter a parse tree produced by APiParser#oflow.
    def enterOflow(self, ctx:APiParser.OflowContext):
        pass

    # Exit a parse tree produced by APiParser#oflow.
    def exitOflow(self, ctx:APiParser.OflowContext):
        pass


    # Enter a parse tree produced by APiParser#s_start.
    def enterS_start(self, ctx:APiParser.S_startContext):
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


    # Enter a parse tree produced by APiParser#s_channel_transformer.
    def enterS_channel_transformer(self, ctx:APiParser.S_channel_transformerContext):
        pass

    # Exit a parse tree produced by APiParser#s_channel_transformer.
    def exitS_channel_transformer(self, ctx:APiParser.S_channel_transformerContext):
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


    # Enter a parse tree produced by APiParser#s_input.
    def enterS_input(self, ctx:APiParser.S_inputContext):
        pass

    # Exit a parse tree produced by APiParser#s_input.
    def exitS_input(self, ctx:APiParser.S_inputContext):
        pass


    # Enter a parse tree produced by APiParser#s_output.
    def enterS_output(self, ctx:APiParser.S_outputContext):
        pass

    # Exit a parse tree produced by APiParser#s_output.
    def exitS_output(self, ctx:APiParser.S_outputContext):
        pass


    # Enter a parse tree produced by APiParser#s_xml.
    def enterS_xml(self, ctx:APiParser.S_xmlContext):
        self.PARSING_XML = True

    # Exit a parse tree produced by APiParser#s_xml.
    def exitS_xml(self, ctx:APiParser.S_xmlContext):
        self.PARSING_XML = False


    # Enter a parse tree produced by APiParser#s_json.
    def enterS_json(self, ctx:APiParser.S_jsonContext):
        pass

    # Exit a parse tree produced by APiParser#s_json.
    def exitS_json(self, ctx:APiParser.S_jsonContext):
        pass


    # Enter a parse tree produced by APiParser#s_regex.
    def enterS_regex(self, ctx:APiParser.S_regexContext):
        self.STACK.append( 'regex( ' + ctx.children[ 1 ].getText()[ 1:-1 ] + ' )' )


    # Exit a parse tree produced by APiParser#s_regex.
    def exitS_regex(self, ctx:APiParser.S_regexContext):
        pass


    # Enter a parse tree produced by APiParser#json.
    def enterJson(self, ctx:APiParser.JsonContext):
        try:
            print( ctx.children[ 0 ].getText() )
        except:
            pass

    # Exit a parse tree produced by APiParser#json.
    def exitJson(self, ctx:APiParser.JsonContext):
        top = self.STACK.pop()
        self.STACK.append( 'json( %s )' % top )
        print( self.STACK[ -1 ] )

    # Enter a parse tree produced by APiParser#obj.
    def enterObj(self, ctx:APiParser.ObjContext):
        self.STACK.append( 'api_object_begin' )

    # Exit a parse tree produced by APiParser#obj.
    def exitObj(self, ctx:APiParser.ObjContext):
        prolog = 'object( '
        pair = None
        res = []
        while pair != 'api_object_begin':
            pair = self.STACK.pop()
            if pair != 'api_object_begin':
                res.append( pair )
        res.reverse()
        for val in res:
            prolog += "%s, " % val
        prolog = prolog[ :-2 ] + ' )'
        self.STACK.append( prolog )


    # Enter a parse tree produced by APiParser#pair.
    def enterPair(self, ctx:APiParser.PairContext):
        self.STACK.append( 'pair' )
        ch = ctx.children[ 0 ].getText()
        if ch[ 0 ] in [ "'", '"' ]:
            val = "'string:%s'" % ch[ 1:-1 ]
        elif ch[ 0 ] == '?':
            val = 'X' + ch[ 1: ]
        self.STACK.append( val )

    # Exit a parse tree produced by APiParser#pair.
    def exitPair(self, ctx:APiParser.PairContext):
        val = self.STACK.pop()
        key = self.STACK.pop()
        self.STACK.pop()
        self.STACK.append( "pair( %s, %s )" % ( key, val ) )


    # Enter a parse tree produced by APiParser#arr.
    def enterArr(self, ctx:APiParser.ArrContext):
        self.STACK.append( 'api_array_begin' )
        
    # Exit a parse tree produced by APiParser#arr.
    def exitArr(self, ctx:APiParser.ArrContext):
        val = None
        prolog = 'array( ['
        res = []
        while val != 'api_array_begin':
            val = self.STACK.pop()
            if val != 'api_array_begin':
                res.append( val )
        res.reverse()
        for val in res:
            prolog += "%s, " % val
        prolog = prolog[ :-2 ] + ' ] )'
        self.STACK.append( prolog )
        


    # Enter a parse tree produced by APiParser#value.
    def enterValue(self, ctx:APiParser.ValueContext):
        if not self.PARSING_XML:
            val = ctx.getText()
            if ctx.VARIABLE():
                self.STACK.append( 'X' + val[ 1: ] )
            elif ctx.STRING():
                self.STACK.append( "'string:%s'" % val[ 1:-1 ] )
            elif ctx.NUMBER():
                self.STACK.append( "'number:%s'" % val )
            elif val in [ 'true', 'false', 'null' ]:
                self.STACK.append( "'atom:%s'" % val )

    # Exit a parse tree produced by APiParser#value.
    def exitValue(self, ctx:APiParser.ValueContext):
        pass


    # Enter a parse tree produced by APiParser#xml.
    def enterXml(self, ctx:APiParser.XmlContext):
        self.STACK.append( 'xml' )

    # Exit a parse tree produced by APiParser#xml.
    def exitXml(self, ctx:APiParser.XmlContext):
        top = self.STACK.pop()
        self.STACK.append( 'xml( %s )' % top )
        print( self.STACK[ -1 ] )


    # Enter a parse tree produced by APiParser#prolog.
    def enterProlog(self, ctx:APiParser.PrologContext):
        self.STACK.append( 'api_prolog_begin' )

    # Exit a parse tree produced by APiParser#prolog.
    def exitProlog(self, ctx:APiParser.PrologContext):
        val = None
        prolog = 'prolog( '
        res = []
        while val != 'api_prolog_begin':
            val = self.STACK.pop()
            if val != 'api_prolog_begin':
                res.append( val )
        res.reverse()
        for val in res:
            prolog += '%s, ' % val
        prolog = prolog[ :-2 ] + ' )'
        self.STACK.append( prolog )


    # Enter a parse tree produced by APiParser#content.
    def enterContent(self, ctx:APiParser.ContentContext):
        self.STACK.append( 'api_content_begin' )

    # Exit a parse tree produced by APiParser#content.
    def exitContent(self, ctx:APiParser.ContentContext):
        val = None
        prolog = 'content( '
        res = []
        while val != 'api_content_begin':
            val = self.STACK.pop()
            if val != 'api_content_begin':
                res.append( val )
        res.reverse()
        for val in res:
            prolog += '%s, ' % val
        prolog = prolog[ :-2 ] + ' )'
        self.STACK.append( prolog )


    # Enter a parse tree produced by APiParser#element.
    def enterElement(self, ctx:APiParser.ElementContext):
        self.STACK.append( 'api_element_begin' )

    # Exit a parse tree produced by APiParser#element.
    def exitElement(self, ctx:APiParser.ElementContext):
        val = None
        prolog = 'element( '
        res = []
        while val != 'api_element_begin':
            val = self.STACK.pop()
            if val != 'api_element_begin':
                res.append( val )
        elem_name = res.pop()
        prolog += 'elem( %s ), ' % elem_name
        res.reverse()
        for val in res:
            prolog += '%s, ' % val
        prolog = prolog[ :-2 ] + ' )'
        self.STACK.append( prolog )


    # Enter a parse tree produced by APiParser#var_or_ident.
    def enterVar_or_ident(self, ctx:APiParser.Var_or_identContext):
        val = ctx.getText()
        if ctx.IDENT():
            self.STACK.append( "'ident:%s'" % val )
        elif ctx.VARIABLE():
            self.STACK.append( 'X' + val[ 1: ] )

    # Exit a parse tree produced by APiParser#var_or_ident.
    def exitVar_or_ident(self, ctx:APiParser.Var_or_identContext):
        pass


    # Enter a parse tree produced by APiParser#reference.
    def enterReference(self, ctx:APiParser.ReferenceContext):
        pass

    # Exit a parse tree produced by APiParser#reference.
    def exitReference(self, ctx:APiParser.ReferenceContext):
        pass


    # Enter a parse tree produced by APiParser#attribute.
    def enterAttribute(self, ctx:APiParser.AttributeContext):
        self.STACK.append( 'api_attribute_begin' )
        ch = ctx.children[ 2 ].getText()
        if ch[ 0 ] in [ "'", '"' ]:
            val = "'string:%s'" % ch[ 1:-1 ]
        elif ch[ 0 ] == '?':
            val = 'X' + ch[ 1: ]
        self.STACK.append( val )

    # Exit a parse tree produced by APiParser#attribute.
    def exitAttribute(self, ctx:APiParser.AttributeContext):
        val = None
        prolog = 'attribute( '
        res = []
        while val != 'api_attribute_begin':
            val = self.STACK.pop()
            if val != 'api_attribute_begin':
                res.append( val )
        for val in res:
            prolog += '%s, ' % val
        prolog = prolog[ :-2 ] + ' )'
        self.STACK.append( prolog )


    # Enter a parse tree produced by APiParser#chardata.
    def enterChardata(self, ctx:APiParser.ChardataContext):
        # TODO: This is a hackish solution. There must be a more elegant one.
        values = [ i.getText() for i in ctx.children ]
        for val in values:
            if val[ 0 ] == '?':
                self.STACK.append( 'X' + val[ 1: ] )
            else:
                self.STACK.append( "'atom:%s'" % val )

        
            

    # Exit a parse tree produced by APiParser#chardata.
    def exitChardata(self, ctx:APiParser.ChardataContext):
        pass


    # Enter a parse tree produced by APiParser#misc.
    def enterMisc(self, ctx:APiParser.MiscContext):
        pass

    # Exit a parse tree produced by APiParser#misc.
    def exitMisc(self, ctx:APiParser.MiscContext):
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
    try:
        return parser.STACK[ -1 ]
    except:
        pass # TODO: remove exception handling when all parts of parser are implemented
    

BYE = 'Bye!'
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
                    print( '\n%s!' % BYE )
                    quit_spade()
                    sys.exit()
                
                if command == "exit":
                    print( '%s!' % BYE )
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
                    
                if command:
                    stream = InputStream( command + '\n' )
                    process( stream )

def initialize():
    global BYE
    BYE = random.choice( [ i.strip().title() for i in open( 'bye.txt' ).readlines() ][ 1: ] )
    if not os.path.exists( TMP_FOLDER ):
        os.makedirs( TMP_FOLDER )
                    
if __name__ == '__main__':
    initialize()
    ns = APiNamespace()

    # TESTING
    os.chdir('test')
    rs = APiRegistrationService( 'APi-test' )
    #a1, a1pass = rs.register( 'ivek' )
    #a2, a2pass = rs.register( 'joza' )
    #c1, c1pass = rs.register( 'stefica' )

    #a = APiAgent( 'bla_stdin_stdout', a1 + '@rec.foi.hr', a1pass, flows=[ ( 'self', 'c' ) ] )
    #b = APiAgent( 'bla_stdin_ws', a2 + '@rec.foi.hr', a2pass, flows=[ ( 'c', 'self' ) ] )
    #c = APiChannel( 'c', c1 + '@rec.foi.hr', c1pass, channel_input='regex( x is (?P<act>[0-9]+) )', channel_output="{ 'action':?act, 'history':?act }" )

    #ns[ 'agents' ][ 'a' ] = a
    #ns[ 'agents' ][ 'b' ] = b
    #ns[ 'channels' ][ 'c' ] = c

    #c.start()

    h1name, h1password = rs.register( 'holonko1' )
    agents = [ { 'name':'bla_stdin_stdout', 'flows':[ ( 'c', 'self' ), ( 'self', 'd' ) ], 'args':None }, { 'name':'bla_stdin_http', 'flows':[ ( 'd', 'self' ) ], 'args':None }, { 'name':'bla_file_stdout', 'flows':[ ( 'self', 'c' ) ], 'args':None } ]
    channels = [ { 'name':'c', 'input':'regex( (?P<act>.*) )', 'output':"?act", 'transformer':None }, { 'name':'d', 'input':'regex( (?P<act>.*) )', 'output':"{ 'action':'?act', 'history':'?act' }", 'transformer':None } ]
    environment = None
    holons = []
    execution_plan = None
    print( h1name )
    h1 = APiHolon( 'holonko1', h1name, h1password, agents, channels, environment, holons, execution_plan )
    h1.start()
    

    
    #a = APiAgent( 'bla_ws_ws', 'bla0agent@dragon.foi.hr', 'tajna', flows=[ ('a', 'self'), ('self', 'c'), ('d', 'e', 'NIL'), ('b','VOID') ] ) # ('STDIN', 'self'),  ('self', 'STDOUT'),

    
    '''
    sleep( 1 )
    a.input( 'avauhu\nguhu\nbuhu\nwuhu\ncuhu\n' )
    sleep( 1 )
    a.input( 'juhu\n' )
    sleep( 1 )
    a.input( 'muhu\n' )
    a.input( 'ahu\n' )
    sleep( 1 )
    a.input( 'puhu\nluhu\n' )
    sleep( 1 )
    a.input( '<!eof!>' )'''
    
    #a.start_shell_client( await_stdin=True, print_stdout=True, print_stderr=True )
    

    #c = APiChannel( 'test', 'bla0agent@dragon.foi.hr', 'tajna', channel_input='regex( x is (?P<act>[0-9]+) )', channel_output="{ 'action':?act, 'history':?act }" )

    #print( c.map( 'x is 247 blakaka x is 222121' ) )

    #c = APiChannel( 'test', 'bla0agent@dragon.foi.hr', 'tajna', channel_input='json( { "gugu":?y, "bla":?x } )', channel_output='<bla><nana x="?x" /><y>?y</y></bla>' )

    #c.start()
    
    #print( c.map( '{ "bla":234, "gugu":1 }' ) )

    
    #c = APiChannel( 'test', 'bla0agent@dragon.foi.hr', 'tajna' ) # TRANSPARENT CHANNEL

    #print( c.map( '{ "bla":234, "gugu":1 }' ) ) 
    
    
    print( ns )

    
    main()
    
    spade.quit_spade()

