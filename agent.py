#!/usr/bin/env python3
from baseagent import *
import json
import argparse

class APiAgent( APiBaseAgent ):
    '''Service wrapper agent.'''

    def __init__( self, agentname, name, password, holon, token, args={}, flows=[] ):
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
        self.read_args( args )

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
        self.subscribe_msg_template[ 'protocol' ] = self.agent_args[ 'protocol' ]
        self.subscribe_msg_template[ 'ontology' ] = 'APiDataTransfer'
        self.subscribe_msg_template[ 'auth-token' ] = self.auth

        self.attach_msg_template = {}
        self.attach_msg_template[ 'performative' ] = 'request'
        self.attach_msg_template[ 'protocol' ] = self.agent_args[ 'protocol' ]
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
            
    def read_args( self, args ):
        self.agent_args = {}
        self.agent_args[ 'protocol' ] = 'tcp'
        if args != None and args[ 'protocol' ]:
            self.agent_args[ 'protocol' ] = args[ 'protocol' ]
    
    def output_callback( self, data ):
        '''
        Output callback method.
        data - data read from service.
        '''
        self.shell_buffer.append( data )
        self.say( 'I just received:', data )
        for srv in self.output_channel_servers.values():
            print( 'SENDING', data.encode(), 'to', srv[ 'port' ], '... ', end='' )
            is_udp = srv[ 'protocol' ] == 'udp'
            sent = False
            srv[ 'socket' ] = nclib.Netcat( ( srv[ 'server' ], srv[ 'port' ] ), udp=is_udp )
            while not sent:
                try:
                    srv[ 'socket' ].sendline( data.encode() )
                    sent = True
                    print( ' DONE!' )
                except ( BrokenPipeError, ConnectionResetError ):
                    print( 'ERROR SENDING', data, 'TO', srv[ 'server' ], srv[ 'port' ], '(BROKEN PIPE)' )
                    print( 'TRYING TO RECONNECT' )
                    srv[ 'socket' ] = nclib.Netcat( ( srv[ 'server' ], srv[ 'port' ] ), udp=is_udp )
        if data == self.output_delimiter: # TODO: Verify this
            self.service_quit( 'End of output' )
                    

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
        #self.add_behaviour( self.behaviour_l )

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
                            is_udp = msg.metadata[ 'protocol' ] == 'udp'
                            servers = self.agent.input_channel_servers
                            self.agent.say( '(SetupInputChannels) Setting up', msg.metadata[ 'type' ], 'channel', channel )
                            servers[ channel ] = {}
                            servers[ channel ][ 'server' ] = msg.metadata[ 'server' ]
                            servers[ channel ][ 'port' ] = int( msg.metadata[ 'port' ] )
                            servers[ channel ][ 'protocol' ] = msg.metadata[ 'protocol' ]
                            servers[ channel ][ 'socket' ] = nclib.Netcat( ( msg.metadata[ 'server' ], int( msg.metadata[ 'port' ] ) ), udp=is_udp )

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
                            is_udp = msg.metadata['protocol'] == 'udp'
                            servers = self.agent.output_channel_servers
                            self.agent.say( '(SetupOutputChannels) Setting up', msg.metadata[ 'type' ], 'channel', channel )
                            servers[ channel ] = {}
                            servers[ channel ][ 'server' ] = msg.metadata[ 'server' ]
                            servers[ channel ][ 'port' ] = int( msg.metadata[ 'port' ] )
                            servers[ channel ][ 'protocol' ] = msg.metadata[ 'protocol' ]
                            servers[ channel ][ 'socket' ] = nclib.Netcat( ( msg.metadata[ 'server' ], int( msg.metadata[ 'port' ] ) ), udp=is_udp )

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
                    self.agent.add_behaviour( self.agent.behaviour_l ) # Start listening for input
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )


def main( name, address, password, holon, token, args, flows ):
    args = json.loads( args )
    flows = json.loads( flows )
    flows = [ ( i[ 0 ], i[ 1 ] ) for i in flows ]
    a = APiAgent( name, address, password, holon, token, args, flows )
    a.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='APi agent.')
    parser.add_argument( 'name', metavar='NAME', type=str, help="Agent's local APi name" )
    parser.add_argument( 'address', metavar='ADDRESS', type=str, help="Agent's XMPP/JID address" )
    parser.add_argument( 'password', metavar='PWD', type=str, help="Agent's XMPP/JID password" )
    parser.add_argument( 'holon', metavar='HOLON', type=str, help="Agent's instantiating holon's XMPP/JID address" )
    parser.add_argument( 'token', metavar='TOKEN', type=str, help="Agent's security token" )
    parser.add_argument( 'args', metavar='ARGS', type=str, help="Agent's instantiation arguments" )
    parser.add_argument( 'flows', metavar='FLOWS', type=str, help="Agent's communication flows" )

    args = parser.parse_args()
    main( args.name, args.address, args.password, args.holon, args.token, args.args, args.flows )
