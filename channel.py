#!/usr/bin/env python3

from basechannel import *
import json
import time
import argparse

class APiChannel( APiBaseChannel ):
    '''Channel agent.'''

    def __init__( self, channelname, name, password, holon, token, portrange, protocol, channel_input=None, channel_output=None ):
        super().__init__( channelname, name, password, holon, token, portrange, channel_input, channel_output )

        # TODO we can use a single server for attach instead of multiple
        self.attach_servers = []

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

        # we create one channel each, for tcp & udp communication since agent may request
        # one protocol or another
        self.protocol = protocol
        srv, ip, port, protocol = self.get_server( protocol )
        self.socket_server = {
            "server": srv,
            "ip": ip,
            "port": port,
            "protocol": protocol
        }        

        self.socket_clients['subscribe'] = []

        # iterating over netcat server clients is blocking, thus we run it in thread
        # that wont block the runtime
        self.cli_socket = Thread( target=self.get_server_clients, args=(srv, "subscribe", self.protocol) )
        self.cli_socket.start()    


    def send_to_subscribed_agents( self, msg ):
        if self.protocol == "udp":
            for client in self.socket_clients['subscribe']:
                self.socket_server['server'].respond(msg, client)
        else:
            closed_clients = []
            for idx, client in enumerate( self.socket_clients['subscribe'] ):
                try:
                    client.sendline( msg )
                except Exception as ex:
                    print("Run into error sending a msg over socket", ex)
                    closed_clients.append(idx)

            # remove closed sockets -- might have to deal with concurrency
            # for idx in closed_clients:
                # del self.socket_clients['subscribe][idx]

    def get_subscribe_server( self, protocol ):
        instance = self.socket_server

        srv = instance['server']
        ip = instance['ip']
        port = instance['port']
        protocol = instance['protocol']
        
        return srv, ip, port, protocol

    def get_attach_server( self, protocol ):
        srv, host, port, protocol = self.get_server( protocol )

        self.attach_servers.append( srv )

        return srv, host, port, protocol

    class Subscribe( CyclicBehaviour ):
        '''Agent wants to listen or write to channel'''
        async def run( self ):
            msg = await self.receive( timeout=0.1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(Subscribe) Message verified, processing ...' )
                    metadata = deepcopy( self.agent.agree_message_template )
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    metadata[ 'agent' ] = self.agent.channelname
                    if msg.metadata[ 'performative' ] == 'subscribe':
                        metadata[ 'type' ] = 'input'
                        _, ip, port, protocol = self.agent.get_subscribe_server( self.agent.protocol )
                        print( 'ADDED subscribe server', ip, port )
                    elif msg.metadata[ 'performative' ] == 'request':
                        metadata[ 'type' ] = 'output'
                        _, ip, port, protocol = self.agent.get_attach_server( self.agent.protocol )
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
        async def run( self ):

            def iter_clients( srv ):
                if self.agent.protocol == "udp":
                    yield srv
                else:
                    try:
                        c, a = srv.sock.accept()
                        is_udp = True if self.agent.protocol == "udp" else False
                        client = nclib.Netcat( sock=c, server=a, udp=is_udp )
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
                        # TODO should put in a method instead
                        if self.agent.protocol == "udp":
                            result = None
                            try:
                                result, _ = client.sock.recvfrom(1024)
                            except:
                                pass
                        else:
                            result = client.recv_until( self.agent.delimiter, timeout=0.1 )
                        self.agent.say( 'RESULT', result, srv.addr )
                        if result:
                            self.agent.say( 'MAPPING RESULT', result.decode(), srv.addr )
                            msg = self.agent.map( result.decode() )
                            self.agent.say( 'MSG', msg, srv.addr )                        

                            self.agent.send_to_subscribed_agents( msg.encode() )

                    
    async def setup(self):
        super().setup()

        bsl = self.StatusListening()
        self.add_behaviour( bsl )
            
        bsubs = self.Subscribe()
        bsubs_template = Template(metadata={"ontology": "APiDataTransfer"})      
        self.add_behaviour( bsubs, bsubs_template )
        
        bfwd = self.Forward()
        self.add_behaviour( bfwd )


def main( name, address, password, holon, token, portrange, protocol, input, output ):
    portrange = json.loads( portrange )
    input = None if input == "null" else input
    output = None if output == "null" else output

    a = APiChannel( name, address, password, holon, token, portrange, protocol=protocol, channel_input=input, channel_output=output )
    
    a.start()

    # is_alive() might return false on first check, as agent won't be yet starter
    # thus there is is_init_set flag which will ensure that we wait for is_alive() to
    # return true at least once before we would even expect is_alive() to return truthy false
    is_init_set = False
    while a.is_alive() or not is_init_set:
        if a.is_alive():
            is_init_set = True
        time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='APi agent.')
    parser.add_argument( 'name', metavar='NAME', type=str, help="Channel's local APi name" )
    parser.add_argument( 'address', metavar='ADDRESS', type=str, help="Channel's XMPP/JID address" )
    parser.add_argument( 'password', metavar='PWD', type=str, help="Channel's XMPP/JID password" )
    parser.add_argument( 'holon', metavar='HOLON', type=str, help="Channel's instantiating holon's XMPP/JID address" )
    parser.add_argument( 'token', metavar='TOKEN', type=str, help="Channel's security token" )
    parser.add_argument( 'portrange', metavar='PORTRANGE', type=str, help="Channel's port range" )
    parser.add_argument( 'protocol', metavar='PROTOCOL', type=str, help="Channel's protocol specification" )
    parser.add_argument( 'input', metavar='INPUT', type=str, help="Channel's input specification" )
    parser.add_argument( 'output', metavar='OUTPUT', type=str, help="Channel's output specification" )
    
    args = parser.parse_args()
    main( args.name, args.address, args.password, args.holon, args.token, args.portrange, args.protocol, args.input, args.output )
