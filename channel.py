#!/usr/bin/env python3

from baseagent import *
import json
import argparse

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

        self.inform_msg_template = {}
        self.inform_msg_template[ 'performative' ] = 'inform'
        self.inform_msg_template[ 'ontology' ] = 'APiScheduling'
        self.inform_msg_template[ 'type' ] = 'channel'
        self.inform_msg_template[ 'auth-token' ] = self.auth
        
        self.input = channel_input
        self.output = channel_output
        self.transformer = transformer

        # we create one channel each, for tcp & udp communication since agent may request
        # one protocol or another
        tcp_srv, tcp_ip, tcp_port, tcp_protocol = self.get_server( 'tcp' )
        self.tcp_sub_server = {
            "server": tcp_srv,
            "ip": tcp_ip,
            "port": tcp_port,
            "protocol": tcp_protocol
        }        
        udp_srv, udp_ip, udp_port, udp_protocol = self.get_server( 'udp' )
        self.udp_sub_server = {
            "server": udp_srv,
            "ip": udp_ip,
            "port": udp_port,
            "protocol": udp_protocol
        }

        self.client_sockets = []

        # iterating over netcat server clients is blocking, thus we run it in thread
        # that wont block the runtime
        self.tcp_cli_sock_t = Thread( target=self.get_server_clients, args=(tcp_srv,) )
        self.tcp_cli_sock_t.start()
        self.udp_cli_sock_t = Thread( target=self.get_server_clients, args=(udp_srv,) )
        self.udp_cli_sock_t.start()
        
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
                self.map = lambda x: eval(self.transformer)
            else:
                self.map = lambda x: x
        else:
            if self.transformer:
                err = "Both input/output combination and transformer defined. I don't know which mapping to use."
                raise APiChannelDefinitionError( err )
        
            
            elif self.input.startswith( 'regex( ' ):
                reg = self.input[ 7:-2 ]
                # print( 'RE', reg )
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

    def get_server_clients( self, server ):
        for client in server:
            self.client_sockets.append( client )

    def send_to_subscribed_agents( self, msg ):
        closed_clients = []
        for idx, client in enumerate( self.client_sockets ):
            try:
                client.sendline( msg )
            except Exception as ex:
                print("Run into error sending a msg over socket", ex)
                closed_clients.append(idx)

        # remove closed sockets -- might have to deal with concurrency
        # for idx in closed_clients:
            # del self.client_sockets[idx]

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
    
    def create_server( self, port, protocol ):
        if protocol == 'udp':
            return nclib.UDPServer( ( '0.0.0.0', port ) )
        
        return nclib.TCPServer( ( '0.0.0.0', port ) )

    def get_server( self, protocol ):
        '''Get a NetCat server for sending or receiving'''
        port =  self.get_free_port()
        host = self.get_ip()

        self.say( host, port )

        srv_created = False
        while not srv_created:
            try:
                srv = self.create_server( port, protocol )
                srv_created = True
                print( f'{protocol} SERVER CONNECTED AT PORT', port )
            except OSError as e:
                port = self.get_free_port()

        return srv, host, str( port ), protocol


    def get_subscribe_server( self, protocol ):
        instance = self.tcp_sub_server if protocol == "tcp" else self.udp_sub_server

        srv = instance['server']
        ip = instance['ip']
        port = instance['port']
        protocol = instance['protocol']
        
        return srv, ip, port, protocol

    def get_attach_server( self, protocol ):
        srv, host, port, protocol = self.get_server( protocol )

        self.attach_servers.append( srv )

        return srv, host, port, protocol


    class StatusListening( OneShotBehaviour ):
        async def run( self ):
            metadata = deepcopy( self.agent.inform_msg_template )
            metadata[ 'status' ] = 'listening'
            metadata[ 'type' ] = 'channel'
            await self.agent.schedule_message( self.agent.holon, metadata=metadata )
    
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
                    req_protocol = msg.metadata[ 'protocol' ]
                    if msg.metadata[ 'performative' ] == 'subscribe':
                        metadata[ 'type' ] = 'input'
                        _, ip, port, protocol = self.agent.get_subscribe_server( req_protocol )
                        print( 'ADDED subscribe server', ip, port )
                    elif msg.metadata[ 'performative' ] == 'request':
                        metadata[ 'type' ] = 'output'
                        _, ip, port, protocol = self.agent.get_attach_server( req_protocol )
                        print( 'ADDED attach server', ip, port )
                    else:
                        self.agent.say( 'Unknown message' )
                        metadata = self.agent.refuse_message_template
                        metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                        metadata[ 'reason' ] = 'unknown-message'
                        await self.agent.schedule_message( str( msg.sender ), metadata=metadata )

                    metadata[ 'server' ] = ip
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
                try:
                    c, a = srv.sock.accept()
                    client = nclib.Netcat( sock=c, server=a )
                    yield client
                    for client in srv:
                        yield client
                except Exception as e:
                    return
            
            # Slusaju se poruke od svih agenata koji su attached, te je ovo cyclic behv jer
            # rec_until nije awaitan, nego mora biti u loopu. nakon sto se dohvati poruka, onda
            # se iterira kroz subscribed agente, te se njima salje result
            if self.agent.attach_servers:
                for srv in self.agent.attach_servers:
                    srv.sock.settimeout( 0.1 )
                    for client in iter_clients( srv ):
                        self.agent.say( 'CLIENT', client, srv.addr )
                        result = client.recv_until( self.agent.delimiter, timeout=0.1 )
                        self.agent.say( 'RESULT', result, srv.addr )
                        if result:
                            self.agent.say( 'MAPPING RESULT', result.decode(), srv.addr )
                            msg = self.agent.map( result.decode() )
                            self.agent.say( 'MSG', msg, srv.addr )
                            self.agent.say( 'SERVER LIST 1', self.agent.subscribe_servers )

                            self.agent.send_to_subscribed_agents( msg.encode() )

                            # if self.agent.subscribe_servers:
                            #     self.agent.say( 'SERVER LIST 2', self.agent.subscribe_servers )
                            #     for srv_out in self.agent.subscribe_servers:
                            #         self.agent.say( 'OUT SERVER', srv_out, srv_out.addr )
                            #         for client_out in srv_out:
                            #             self.agent.say( 'SENDING MSG TO', client_out, client_out.peer )
                            #             client_out.sendline( msg.encode() )
                            #             self.agent.say( 'DONE SENDING MSG' )
                    
    async def setup(self):
        super().setup()

        bsl = self.StatusListening()
        self.add_behaviour( bsl )
            
        bsubs = self.Subscribe()
        bsubs_template = Template(
            metadata={ 
                       "ontology": "APiDataTransfer"
            } # "performative": "subscribe",
        )      
        self.add_behaviour( bsubs, bsubs_template )
        
        bfwd = self.Forward()
        self.add_behaviour( bfwd )


def main( name, address, password, holon, token, portrange, input, output, transformer ):
    portrange = json.loads( portrange )
    input = json.loads( input )
    output = json.loads( output )
    transformer = json.loads( transformer )
    a = APiChannel( name, address, password, holon, token, portrange, channel_input=input, channel_output=output, transformer=transformer )
    a.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='APi agent.')
    parser.add_argument( 'name', metavar='NAME', type=str, help="Channel's local APi name" )
    parser.add_argument( 'address', metavar='ADDRESS', type=str, help="Channel's XMPP/JID address" )
    parser.add_argument( 'password', metavar='PWD', type=str, help="Channel's XMPP/JID password" )
    parser.add_argument( 'holon', metavar='HOLON', type=str, help="Channel's instantiating holon's XMPP/JID address" )
    parser.add_argument( 'token', metavar='TOKEN', type=str, help="Channel's security token" )
    parser.add_argument( 'portrange', metavar='PORTRANGE', type=str, help="Channel's port range" )
    parser.add_argument( 'input', metavar='INPUT', type=str, help="Channel's input specification" )
    parser.add_argument( 'output', metavar='OUTPUT', type=str, help="Channel's output specification" )
    parser.add_argument( 'transformer', metavar='TRANSFORMER', type=str, help="Channel's transformer specification" )

    args = parser.parse_args()
    main( args.name, args.address, args.password, args.holon, args.token, args.portrange, args.input, args.output, args.transformer )
