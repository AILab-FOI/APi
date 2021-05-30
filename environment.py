#!/usr/bin/env python3

from baseagent import *
import json
import argparse

class APiEnvironment( APiBaseAgent ):
    '''Environment agent.'''

    REPL_STR = '"$$$API_THIS_IS_VARIABLE_%s$$$"'
    def __init__( self, environment_name, name, password, holon, token, communication ):
        super().__init__( name, password, token )
        
        self.environment_name = environment_name
        self.holon = holon
        self.communication = communication

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

    def get_server( self, srv_type, protocol, io_name ):
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

                
        if srv_type == 'attach':
            self.attach_servers.append( { 'socket': srv, 'io_name': io_name } )
            print( 'ATTACH SERVERS:', self.attach_servers )
        elif srv_type == 'subscribe':
            self.subscribe_servers.append( { 'socket': srv, 'io_name': io_name } )
            print( 'SUBSCRIBE SERVERS:', self.subscribe_servers )
        else:
            raise APiChannelDefinitionError( 'Unknown server type:', srv_type, io_name )
        
        return host, str( port ), protocol


    class Subscribe( CyclicBehaviour ):
        '''Agent wants to listen or write to environment'''
        async def run( self ):
            msg = await self.receive( timeout=0.1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(Subscribe) Message verified, processing ...' )

                    metadata = deepcopy( self.agent.agree_message_template )
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    metadata[ 'agent' ] = self.agent.channelname
                    req_protocol = msg.metadata[ 'protocol' ]
                    if msg.metadata[ 'performative' ] == 'subscribe':
                        metadata[ 'type' ] = 'input'
                        server, port, protocol = self.agent.get_server( 'subscribe', req_protocol, msg.metadata[ 'io-name' ] )
                        print( 'ADDED subscribe server', server, port )
                    elif msg.metadata[ 'performative' ] == 'request':
                        metadata[ 'type' ] = 'output'
                        server, port, protocol = self.agent.get_server( 'attach', req_protocol, msg.metadata[ 'io-name' ]  )
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
                try:
                    c, a = srv.sock.accept()
                    client = nclib.Netcat( sock=c, server=a )
                    yield client
                    for client in srv:
                        yield client
                except Exception as e:
                    return
            
            if self.agent.attach_servers:
                for entry in self.agent.attach_servers:
                    srv = entry[ 'srv' ]
                    io_name = entry[ 'io_name' ]

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
        bsubs_template = Template( metadata={ "ontology": "APiDataTransfer" } )      
        self.add_behaviour( bsubs, bsubs_template )

        bfwd = self.Forward()
        self.add_behaviour( bfwd )

def main( name, address, password, holon, token, communication ):
    communication = json.loads( communication )
    a = APiEnvironment( name, address, password, holon, token, communication )
    a.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='APi environment.')
    parser.add_argument( 'name', metavar='NAME', type=str, help="Environment's local APi name" )
    parser.add_argument( 'address', metavar='ADDRESS', type=str, help="Environment's XMPP/JID address" )
    parser.add_argument( 'password', metavar='PWD', type=str, help="Environment's XMPP/JID password" )
    parser.add_argument( 'holon', metavar='HOLON', type=str, help="Environment's instantiating holon's XMPP/JID address" )
    parser.add_argument( 'token', metavar='TOKEN', type=str, help="Environment's security token" )
    parser.add_argument( 'communication', metavar='COMMUNICATION', type=str, help="Environment's inputs/outputs definition" )

    args = parser.parse_args()
    main( args.name, args.address, args.password, args.holon, args.token, args.communication )
