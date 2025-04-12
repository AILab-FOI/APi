import argparse
import asyncio
import json
import time
from copy import deepcopy
from threading import Thread

import nclib
from spade.behaviour import CyclicBehaviour
from spade.template import Template

from src.agents.base.base_channel import APiBaseChannel
from src.utils.logger import setup_logger
from typing import Tuple

logger = setup_logger("channel")


class APiChannel(APiBaseChannel):
    """
    Channel.
    """

    def __init__(
        self,
        channelname: str,
        name: str,
        password: str,
        holon: str,
        token: str,
        portrange: Tuple[int, int],
        protocol: str,
        channel_input: str = None,
        channel_output: str = None,
    ) -> None:
        global logger
        logger = setup_logger("channel " + channelname)

        super().__init__(
            channelname,
            name,
            password,
            holon,
            token,
            portrange,
            channel_input,
            channel_output,
        )

        # TODO we can use a single server for write instead of multiple
        self.write_servers = []

        self.agree_message_template = {}
        self.agree_message_template["performative"] = "agree"
        self.agree_message_template["ontology"] = "APiDataTransfer"
        self.agree_message_template["auth-token"] = self.auth

        self.refuse_message_template = {}
        self.refuse_message_template["performative"] = "refuse"
        self.refuse_message_template["ontology"] = "APiDataTransfer"
        self.refuse_message_template["auth-token"] = self.auth

        self.inform_msg_template = {}
        self.inform_msg_template["performative"] = "inform"
        self.inform_msg_template["ontology"] = "APiScheduling"
        self.inform_msg_template["type"] = "channel"
        self.inform_msg_template["auth-token"] = self.auth

        # we create one channel each, for tcp & udp communication since agent may request
        # one protocol or another
        self.protocol = protocol
        srv, ip, port, protocol = self.get_server(protocol)
        self.read_socket_server = {
            "server": srv,
            "ip": ip,
            "port": port,
            "protocol": protocol,
        }

        self.socket_clients["subscribe"] = []

        # iterating over netcat server clients is blocking, thus we run it in thread
        # that wont block the runtime
        self.cli_socket = Thread(
            target=self.get_server_clients, args=(srv, "subscribe", self.protocol)
        )
        self.cli_socket.start()

    def send_to_subscribed_read_agents(self, msg: bytes) -> None:
        """
        Send message to subscribed read agents.
        """

        if self.protocol == "udp":
            for client in self.socket_clients["subscribe"]:
                self.read_socket_server["server"].respond(msg, client)
        else:
            closed_clients = []
            for idx, client in enumerate(self.socket_clients["subscribe"]):
                try:
                    client.sendline(msg)
                except Exception as ex:
                    logger.error(f"Run into error sending a msg over socket: {ex}")
                    closed_clients.append(idx)

            # remove closed sockets -- might have to deal with concurrency
            # for idx in closed_clients:
            # del self.socket_clients['subscribe][idx]

    def get_read_server(self, protocol: str) -> Tuple[str, str, int, str]:
        """
        Get read server.
        """

        instance = self.read_socket_server

        srv = instance["server"]
        ip = instance["ip"]
        port = instance["port"]
        protocol = instance["protocol"]

        return srv, ip, port, protocol

    def get_write_server(self, protocol: str) -> Tuple[str, str, int, str]:
        """
        Get write server.
        """

        srv, host, port, protocol = self.get_server(protocol)

        self.write_servers.append(srv)

        return srv, host, port, protocol

    class Subscribe(CyclicBehaviour):
        """
        Subscribe behaviour.

        This behaviour is runs cyclically and is used for agent to subscribe to the channel.
        Agent can either listen (read) to the messages from the channel or send messages (write) to the channel.
        """

        async def run(self) -> None:
            msg = await self.receive(timeout=0.1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(Subscribe) Message verified, processing ...")
                    metadata = deepcopy(self.agent.agree_message_template)
                    metadata["in-reply-to"] = msg.metadata["reply-with"]
                    metadata["agent"] = self.agent.channelname
                    if msg.metadata["performative"] == "subscribe":
                        metadata["type"] = "input"
                        _, ip, port, protocol = self.agent.get_read_server(self.agent.protocol)
                        logger.info(f"Added subscribe server: {ip} for port {port}")
                    elif msg.metadata["performative"] == "request":
                        metadata["type"] = "output"
                        _, ip, port, protocol = self.agent.get_write_server(self.agent.protocol)
                        logger.info(f"Added write server: {ip} for port {port}")
                    else:
                        logger.debug("Unknown message")
                        metadata = self.agent.refuse_message_template
                        metadata["in-reply-to"] = msg.metadata["reply-with"]
                        metadata["reason"] = "unknown-message"
                        await self.agent.schedule_message(str(msg.sender), metadata=metadata)

                    metadata["server"] = ip
                    metadata["port"] = port
                    metadata["protocol"] = protocol
                    await self.agent.schedule_message(str(msg.sender), metadata=metadata)
                    await asyncio.sleep(0.1)
                else:
                    logger.debug("Message could not be verified.")
                    metadata = self.agent.refuse_message_template
                    metadata["in-reply-to"] = msg.metadata["reply-with"]
                    metadata["reason"] = "security-policy"
                    await self.agent.schedule_message(str(msg.sender), metadata=metadata)

    class Listening(CyclicBehaviour):
        """
        Listening behaviour.

        This is behaviour runs cyclically which adheres to how sockets work (in loop).
        It listens for incoming connections and messages from agents that are subscribed to the channel.
        """

        async def run(self) -> None:
            def iter_clients(srv):
                if self.agent.protocol == "udp":
                    yield srv
                else:
                    try:
                        c, a = srv.sock.accept()
                        is_udp = True if self.agent.protocol == "udp" else False
                        client = nclib.Netcat(sock=c, server=a, udp=is_udp)
                        yield client
                        for client in srv:
                            yield client
                    except Exception as e:
                        if str(e) != "timed out":
                            logger.error(f"Error accepting client: {e}")
                        return

            if self.agent.write_servers:
                for srv in self.agent.write_servers:
                    srv.sock.settimeout(0.1)
                    for client in iter_clients(srv):
                        # TODO should put in a method instead
                        if self.agent.protocol == "udp":
                            result = None
                            try:
                                result, _ = client.sock.recvfrom(1024)
                            except Exception as e:
                                logger.error(f"Error receiving from client: {e}")
                                pass
                        else:
                            result = client.recv_until(self.agent.delimiter, timeout=0.1)
                        logger.info(f"Received result: {result}")
                        if result:
                            logger.info(f"Mapping result: {result}")
                            msg = self.agent.map(result.decode())
                            print("msasdg", result.decode())
                            logger.info(f"Sending msg: {msg}")

                            self.agent.send_to_subscribed_read_agents(msg.encode())

    async def setup(self) -> None:
        """
        Setup the channel behaviours.
        """

        super().setup()

        bsl = self.Ready()
        self.add_behaviour(bsl)

        bsubs = self.Subscribe()
        bsubs_template = Template(metadata={"ontology": "APiDataTransfer"})
        self.add_behaviour(bsubs, bsubs_template)

        blist = self.Listening()
        self.add_behaviour(blist)


def main(
    name: str,
    address: str,
    password: str,
    holon: str,
    token: str,
    portrange: str,
    protocol: str,
    input: str,
    output: str,
) -> None:
    a = APiChannel(
        name,
        address,
        password,
        holon,
        token,
        portrange,
        protocol=protocol,
        channel_input=input,
        channel_output=output,
    )

    a.start()

    # is_alive() might return false on first check, as agent won't be yet starter
    # thus there is is_init_set flag which will ensure that we wait for is_alive() to
    # return true at least once before we would even expect is_alive() to return truthy false
    is_init_set = False
    while a.is_alive() or not is_init_set:
        if a.is_alive():
            is_init_set = True
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="APi agent.")
    parser.add_argument("name", metavar="NAME", type=str, help="Channel's local APi name")
    parser.add_argument("address", metavar="ADDRESS", type=str, help="Channel's XMPP/JID address")
    parser.add_argument("password", metavar="PWD", type=str, help="Channel's XMPP/JID password")
    parser.add_argument(
        "holon",
        metavar="HOLON",
        type=str,
        help="Channel's instantiating holon's XMPP/JID address",
    )
    parser.add_argument("token", metavar="TOKEN", type=str, help="Channel's security token")
    parser.add_argument("portrange", metavar="PORTRANGE", type=str, help="Channel's port range")
    parser.add_argument(
        "protocol",
        metavar="PROTOCOL",
        type=str,
        help="Channel's protocol specification",
    )
    parser.add_argument("input", metavar="INPUT", type=str, help="Channel's input specification")
    parser.add_argument("output", metavar="OUTPUT", type=str, help="Channel's output specification")

    args = parser.parse_args()
    main(
        args.name,
        args.address,
        args.password,
        args.holon,
        args.token,
        args.portrange,
        args.protocol,
        args.input,
        args.output,
    )
