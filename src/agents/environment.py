import argparse
import asyncio
import json
import time
from copy import deepcopy
from threading import Thread

import nclib
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template

from src.agents.base.base_channel import APiBaseChannel
from src.utils.logger import setup_logger
from typing import Tuple, Optional, Dict
from uuid import uuid4

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
        holons_address_book: Optional[Dict] = {},
    ):
        # revert and pass proper input & output
        super().__init__(channelname, name, password, holon, token, portrange, input, output)
        # used for external agents that will communicate with holon / environment
        self.input_write_servers = []
        self.output_write_servers = []

        self.holon_read_servers = []
        self.read_holons_address_book = holons_address_book

        self.query_msg_template = {}
        self.query_msg_template["performative"] = "query-ref"
        self.query_msg_template["ontology"] = "APiQuery"
        self.query_msg_template["auth-token"] = self.auth

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

        self.environment_msg_template = {}
        self.environment_msg_template["ontology"] = "APiDataTransfer"
        self.environment_msg_template["auth-token"] = self.auth

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

    class RequestHolonEnvironmentAddresses(OneShotBehaviour):
        """
        Request holon environment adresses.

        Requesting holon environment adresses from the other holon.
        """

        async def run(self) -> None:
            # waiting for address book containing input channels from holon
            for inp in self.agent.read_holons_address_book.keys():
                metadata = self.agent.query_msg_template
                metadata["reply-with"] = str(uuid4().hex)
                metadata["channel"] = inp
                address = self.agent.read_holons_address_book[inp]
                await self.agent.schedule_message(address, metadata=metadata)

    class ReceiveHolonEnvironmentAddress(CyclicBehaviour):
        """
        Receive holon environment address behaviour.

        Holon will pass down the address book to the agent for the requested environments.
        """

        async def run(self) -> None:
            msg = await self.receive(timeout=0.1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug(
                        "(ReceiveHolonEnvironmentAddress) Message verified, processing ..."
                    )
                    channel = msg.metadata["address"]
                    try:
                        self.agent.input_ack.remove(msg.metadata["in-reply-to"])

                        if msg.metadata["performative"] == "refuse":
                            logger.debug(
                                f"Error getting holon environment address due to {msg.metadata['reason']}"
                            )
                            await self.agent.stop()
                        elif msg.metadata["success"] == "true":
                            self.agent.address_book[msg.metadata["agent"]] = channel
                        else:
                            logger.debug(
                                "Error getting holon environment address. Address unknown to holon."
                            )
                            await self.agent.stop()

                    except KeyError:
                        logger.debug(
                            f"I have no memory of this message ({msg.metadata['in-reply-to']}). (awkward Gandalf look)"
                        )
                else:
                    logger.debug("Message could not be verified.")

    class RequestSubscribeToHolonOutputEnvironment(OneShotBehaviour):
        """
        Request subscribe to holon output environment.

        The external holon will have its messages available on the output environment,
        hence this holon will subscribe to it.
        """

        async def run(self) -> None:
            await self.agent.behaviour_gca.join()
            for inp in self.agent.read_holons_address_book.keys():
                # waiting until holon sends the address book
                while inp not in self.agent.address_book:
                    await asyncio.sleep(0.1)
                channel = self.agent.address_book[inp]
                metadata = self.agent.environment_msg_template
                metadata["performative"] = "subscribe_to_output"
                metadata["reply-with"] = str(uuid4().hex)
                metadata["external"] = "True"
                await self.agent.schedule_message(channel, metadata=metadata)

    class SetupReadSockets(CyclicBehaviour):
        """
        Setup read sockets behaviour.

        Once environment has requested to subscribe to read other holon output environment, the holon environment
        will query back with open socket details, that this environment will use to setup the sockets.
        """

        async def run(self):
            await self.agent.behaviour_stic.join()
            msg = await self.receive(timeout=1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(SetupReadSockets) Message verified, processing ...")
                    try:
                        self.agent.input_ack.remove(msg.metadata["in-reply-to"])
                        if msg.metadata["performative"] == "refuse":
                            logger.debug(
                                f"Error connecting to channel address due to {msg.metadata['reason']}"
                            )
                            await self.agent.stop()
                        else:
                            channel = msg.metadata["agent"]
                            is_udp = msg.metadata["protocol"] == "udp"
                            servers = self.agent.holon_read_servers
                            logger.debug(
                                f"(SetupReadSockets) Setting up {msg.metadata['type']} channel {channel}"
                            )
                            servers[channel] = {}
                            servers[channel]["server"] = msg.metadata["server"]
                            servers[channel]["port"] = int(msg.metadata["port"])
                            servers[channel]["protocol"] = msg.metadata["protocol"]
                            servers[channel]["socket"] = nclib.Netcat(
                                (msg.metadata["server"], int(msg.metadata["port"])),
                                udp=is_udp,
                            )
                            if is_udp:
                                servers[channel]["socket"].send("connected")

                            logger.info(
                                f"Connected to input channel {channel} at {msg.metadata['server']}:{msg.metadata['port']}"
                            )

                            if len(self.agent.holon_read_servers) == len(
                                self.agent.read_holons_address_book.keys()
                            ):
                                # letting holon know once environment is all set up
                                metadata = deepcopy(self.agent.inform_msg_template)
                                metadata["status"] = "ready"
                                await self.agent.schedule_message(
                                    self.agent.holon, metadata=metadata
                                )

                    except KeyError:
                        logger.debug(
                            f"I have no memory of this message ({msg.metadata['in-reply-to']}). (awkward Gandalf look)"
                        )
                else:
                    logger.debug("Message could not be verified.")

    class HolonMessageListening(CyclicBehaviour):
        """
        Holon message listening behaviour.

        This is behaviour runs cyclically which adheres to how sockets work (in loop).
        It listens for incoming connections and messages from holon environment that this environment is subscribed to.
        """

        async def run(self) -> None:
            for channel, srv in self.agent.holon_read_servers.items():
                is_udp = True if srv["protocol"] == "udp" else False

                if is_udp:
                    result = srv["socket"].recv_until(self.agent.delimiter, timeout=0.1)
                else:
                    result = srv["socket"].recv_until(self.agent.delimiter, timeout=0.2)
                if result:
                    logger.info(f"Received message from holon {channel}: {result}")
                    self.agent.input(result.decode())

    class SubscriptionRequest(CyclicBehaviour):
        """
        Subscription request behaviour.

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

    class AgentMessageListening(CyclicBehaviour):
        """
        Agent message listening behaviour.

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

        # State behaviour
        bsl = self.Ready()
        self.add_behaviour(bsl)

        # Subscription request handling
        bsubs = self.SubscriptionRequest()
        bsubs_template = Template(metadata={"ontology": "APiDataTransfer"})
        self.add_behaviour(bsubs, bsubs_template)

        # Setup sockets
        self.behaviour_sic = self.SetupReadSockets()
        bsic_template = Template(metadata={"ontology": "APiDataTransfer", "type": "input"})
        self.add_behaviour(self.behaviour_sic, bsic_template)

        # Incoming messages handling
        bifwd = self.AgentMessageListening("input", self.input_write_servers)
        self.add_behaviour(bifwd)

        bofwd = self.AgentMessageListening("output", self.output_write_servers)
        self.add_behaviour(bofwd)

        holon_msg_listening = self.HolonMessageListening()
        self.add_behaviour(holon_msg_listening)

        # Address handling behaviours
        self.behaviour_gca = self.RequestHolonEnvironmentAddresses()
        self.add_behaviour(self.behaviour_gca)

        self.behaviour_qc = self.ReceiveHolonEnvironmentAddress()
        bqc_template = Template(metadata={"ontology": "APiQuery"})
        self.add_behaviour(self.behaviour_qc, bqc_template)

        # Request subscribe to holon environments
        self.behaviour_stic = self.RequestSubscribeToHolonOutputEnvironment()
        self.add_behaviour(self.behaviour_stic)


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
    holons_address_book: Dict = {},
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
        holons_address_book,
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
    parser.add_argument(
        "holons_address_book",
        metavar="holons",
        type=str,
        help="Agent's holons address book",
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
        args.holons_address_book,
    )
