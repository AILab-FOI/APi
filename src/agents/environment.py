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
from typing import Tuple, Optional

logger = setup_logger("environment")


class APiEnvironment(APiBaseChannel):
    """
    Environment.
    """

    def __init__(
        self,
        channelname: str,
        name: str,
        password: str,
        holon: str,
        holon_name: str,
        token: Optional[str] = None,
        portrange: Optional[Tuple[int, int]] = None,
        input_protocol: Optional[str] = None,
        output_protocol: Optional[str] = None,
        input: Optional[str] = None,
        output: Optional[str] = None,
    ):
        # revert and pass proper input & output
        super().__init__(channelname, name, password, holon, token, portrange, input, output)
        # used for external agents that will communicate with holon / environment
        self.input_write_servers = []
        self.output_write_servers = []

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
        self.inform_msg_template["type"] = "environment"
        self.inform_msg_template["auth-token"] = self.auth

        self.holon_name = holon_name
        self.input_protocol = input_protocol
        self.output_protocol = output_protocol
        # we create one channel each, for tcp & udp communication since agent may request
        # one protocol or another
        srv, ip, port, protocol = self.get_server(input_protocol)
        self.input_subscribe_socket_server = {
            "server": srv,
            "ip": ip,
            "port": port,
            "protocol": protocol,
        }
        srv, ip, port, protocol = self.get_server(output_protocol)
        # used for external agents that will communicate with holon / environment
        self.output_subscribe_socket_server = {
            "server": srv,
            "ip": ip,
            "port": port,
            "protocol": protocol,
        }

        self.socket_clients["input_subscribe_socket_clients"] = []
        self.socket_clients["output_subscribe_socket_clients"] = []

        # iterating over netcat server clients is blocking, thus we run it in thread
        # that wont block the runtime
        self.input_subscribe_cli_socket = Thread(
            target=self.get_server_clients,
            args=(
                self.input_subscribe_socket_server["server"],
                "input_subscribe_socket_clients",
                self.input_protocol,
            ),
        )
        self.input_subscribe_cli_socket.start()
        self.output_subscribe_cli_socket = Thread(
            target=self.get_server_clients,
            args=(
                self.output_subscribe_socket_server["server"],
                "output_subscribe_socket_clients",
                self.output_protocol,
            ),
        )
        self.output_subscribe_cli_socket.start()

    def send_to_subscribed_read_agents_and_holons(self, env_type: str, msg: bytes) -> None:
        """
        Send message to subscribed agents.
        """

        socket_clients = (
            self.socket_clients["input_subscribe_socket_clients"]
            if env_type == "input"
            else self.socket_clients["output_subscribe_socket_clients"]
        )
        s_server = (
            self.input_subscribe_socket_server
            if env_type == "input"
            else self.output_subscribe_socket_server
        )
        protocol = self.input_protocol if env_type == "input" else self.output_protocol

        if protocol == "udp":
            for client in socket_clients:
                s_server["server"].respond(msg, client)
        else:
            closed_clients = []
            for idx, client in enumerate(socket_clients):
                try:
                    client.sendline(msg)
                except Exception as ex:
                    logger.info("Run into error sending a msg over socket", ex)
                    closed_clients.append(idx)

            # remove closed sockets -- might have to deal with concurrency
            # for idx in closed_clients:
            # del self.socket_clients[idx]

    def get_read_server(self, env_type: str, protocol: str) -> tuple[str, str, int, str]:
        """
        Get read server.
        """

        instance = (
            self.input_subscribe_socket_server
            if env_type == "input"
            else self.output_subscribe_socket_server
        )

        srv = instance["server"]
        ip = instance["ip"]
        port = instance["port"]
        protocol = instance["protocol"]

        return srv, ip, port, protocol

    def get_write_server(self, env_type: str, protocol: str) -> tuple[str, str, int, str]:
        """
        Get write server.
        """

        srv, host, port, protocol = self.get_server(protocol)

        if env_type == "input":
            self.input_write_servers.append(srv)
        else:
            self.output_write_servers.append(srv)

        return srv, host, port, protocol

    class Subscribe(CyclicBehaviour):
        """
        Subscribe behaviour.

        This behaviour is runs cyclically and is used for agent to subscribe to the environment.
        Agent can either listen (read) to the messages from the environment or send messages (write) to the environment.
        """

        async def run(self):
            msg = await self.receive(timeout=0.1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(Subscribe) Message verified, processing ...")
                    metadata = deepcopy(self.agent.agree_message_template)
                    metadata["in-reply-to"] = msg.metadata["reply-with"]
                    # subscribing to environment input
                    if msg.metadata["performative"] == "subscribe_to_input":
                        metadata["agent"] = "ENV_INPUT"
                        metadata["type"] = "input"
                        _, ip, port, protocol = self.agent.get_read_server(
                            "input", self.agent.input_protocol
                        )
                        logger.info("ADDED input subscribe server", ip, port)
                    # subscribing to environment output
                    elif msg.metadata["performative"] == "subscribe_to_output":
                        metadata["agent"] = "ENV_OUTPUT"
                        metadata["type"] = "input"
                        _, ip, port, protocol = self.agent.get_read_server(
                            "output", self.agent.output_protocol
                        )
                        logger.info("ADDED output subscribe server", ip, port)
                    # attaching to environment output
                    elif msg.metadata["performative"] == "request_to_input":
                        metadata["agent"] = "ENV_INPUT"
                        metadata["type"] = "output"
                        _, ip, port, protocol = self.agent.get_write_server(
                            "input", self.agent.input_protocol
                        )
                        logger.info("ADDED input attach server", ip, port)
                    elif msg.metadata["performative"] == "request_to_output":
                        metadata["agent"] = "ENV_OUTPUT"
                        metadata["type"] = "output"
                        _, ip, port, protocol = self.agent.get_write_server(
                            "output", self.agent.output_protocol
                        )
                        logger.info("ADDED output attach server", ip, port)
                    else:
                        logger.debug("Unknown message")
                        metadata = self.agent.refuse_message_template
                        metadata["in-reply-to"] = msg.metadata["reply-with"]
                        metadata["reason"] = "unknown-message"
                        await self.agent.schedule_message(str(msg.sender), metadata=metadata)

                    if msg.metadata.get("external", "") == "True":
                        metadata["agent"] = self.agent.holon_name

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
        It listens for incoming connections and messages from agents and other holons that are subscribed to the environment.
        """

        def __init__(self, sub_type: str, write_servers: list) -> None:
            super().__init__()
            self.sub_type = sub_type
            self.write_servers = write_servers
            self.protocol = (
                self.agent.input_protocol if sub_type == "input" else self.agent.output_protocol
            )

        async def run(self) -> None:
            """
            Listen for incoming connections and messages.
            """

            def iter_clients(srv):
                if self.protocol == "udp":
                    yield srv
                else:
                    try:
                        c, a = srv.sock.accept()
                        is_udp = True if self.protocol == "udp" else False
                        client = nclib.Netcat(sock=c, server=a, udp=is_udp)
                        yield client
                        for client in srv:
                            yield client
                    except Exception as e:
                        logger.info("Error accepting client", e)
                        return

            if self.write_servers:
                for srv in self.write_servers:
                    srv.sock.settimeout(0.1)
                    for client in iter_clients(srv):
                        logger.debug(f"CLIENT {client} {srv.addr}")
                        # TODO should put in a method instead
                        if self.protocol == "udp":
                            result = None
                            try:
                                result, _ = client.sock.recvfrom(1024)
                            except Exception as e:
                                logger.info("Error receiving from client", e)
                                pass
                        else:
                            result = client.recv_until(self.agent.delimiter, timeout=0.1)
                        logger.debug(f"RESULT {result} {srv.addr}")
                        if result:
                            logger.debug(f"MAPPING RESULT {result.decode()} {srv.addr}")
                            msg = self.agent.map(result.decode())
                            logger.debug(f"MSG {msg} {srv.addr}")

                            self.agent.send_to_subscribed_read_agents_and_holons(
                                self.sub_type, msg.encode()
                            )

    async def setup(self) -> None:
        """
        Setup the environment.
        """

        super().setup()

        bsl = self.Ready()
        self.add_behaviour(bsl)

        bsubs = self.Subscribe()
        bsubs_template = Template(metadata={"ontology": "APiDataTransfer"})
        self.add_behaviour(bsubs, bsubs_template)

        bifwd = self.Listening("input", self.input_write_servers)
        self.add_behaviour(bifwd)

        bofwd = self.Listening("output", self.output_write_servers)
        self.add_behaviour(bofwd)


def main(
    name: str,
    address: str,
    password: str,
    holon: str,
    holon_name: str,
    token: str,
    portrange: str,
    input_protocol: str,
    output_protocol: str,
    input: str,
    output: str,
):
    portrange = json.loads(portrange)
    input = None if input == "null" else input
    output = None if output == "null" else output
    a = APiEnvironment(
        name,
        address,
        password,
        holon,
        holon_name,
        token,
        portrange,
        input_protocol,
        output_protocol,
        input,
        output,
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
    parser.add_argument("name", metavar="NAME", type=str, help="Environment's local APi name")
    parser.add_argument(
        "address", metavar="ADDRESS", type=str, help="Environment's XMPP/JID address"
    )
    parser.add_argument("password", metavar="PWD", type=str, help="Environment's XMPP/JID password")
    parser.add_argument(
        "holon",
        metavar="HOLON",
        type=str,
        help="Environment's instantiating holon's XMPP/JID address",
    )
    parser.add_argument(
        "holon_name",
        metavar="HOLON_NAME",
        type=str,
        help="Agent's instantiating holon's name",
    )
    parser.add_argument("token", metavar="TOKEN", type=str, help="Environment's security token")
    parser.add_argument("portrange", metavar="PORTRANGE", type=str, help="Environment's port range")
    parser.add_argument(
        "input_protocol",
        metavar="INPUT_PROTOCOL",
        type=str,
        help="Environment's input protocol specification",
    )
    parser.add_argument(
        "output_protocol",
        metavar="OUTPUT_PROTOCOL",
        type=str,
        help="Environment's output protocol specification",
    )
    parser.add_argument(
        "input", metavar="INPUT", type=str, help="Environment's input specification"
    )
    parser.add_argument(
        "output", metavar="OUTPUT", type=str, help="Environment's output specification"
    )

    args = parser.parse_args()
    main(
        args.name,
        args.address,
        args.password,
        args.holon,
        args.holon_name,
        args.token,
        args.portrange,
        args.input_protocol,
        args.output_protocol,
        args.input,
        args.output,
    )
