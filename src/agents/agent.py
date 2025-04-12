import argparse
import asyncio
import json
import os
import socket
import time
from copy import deepcopy
from threading import Thread
from time import sleep
from uuid import uuid4

import nclib
import pexpect
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template

from src.agents.base.base_wrapper_agent import APiBaseWrapperAgent
from src.utils.constants import NIE, TMP_FOLDER
import io
from src.utils.errors import (
    APiAgentDefinitionError,
    APiChannelDefinitionError,
    APiIOError,
    APiShellInitError,
)
from src.utils.helpers import pairwise
from src.utils.logger import setup_logger
from typing import Dict, List

try:
    from yaml import CLoader as Loader
    from yaml import load
except ImportError:
    from yaml import Loader, load


_AGENT_FILE_NAME_TEMPLATE = "{file_name}.ad"

logger = setup_logger("agent")


class APiAgent(APiBaseWrapperAgent):
    """
    Service wrapper agent.
    """

    def __init__(
        self,
        agentname: str,
        name: str,
        password: str,
        holon: str,
        holon_name: str,
        token: str,
        flows: List = [],
    ):
        """
        Constructor.
        agentname - name as in agent definition (.ad) file.
        name - XMPP/Jabber username
        password - XMPP/Jabber password
        holon - parent holon
        token - token from holon
        flows - list of message flows (from APi statement)
        """

        global logger
        logger = setup_logger("agent " + agentname)

        logger.info("Initializing agent...")

        try:
            file_name = "../examples/agent_definitions/" + _AGENT_FILE_NAME_TEMPLATE.format(
                file_name=agentname
            )
            fh = open(file_name)
        except IOError as e:
            err = "Missing agent definition file or permission issue.\n" + str(e)
            raise APiIOError(err)
        super().__init__(name, password, token)

        self.agentname = agentname
        self.holon_name = holon_name
        self.holon = holon
        self._load(fh)

        self.flows = []
        for f in flows:
            if len(f) == 2:
                pairs = [i for i in pairwise(f)]
                self.flows.extend(pairs)
            else:
                self.flows.append(f)

        self.input_channels = set(i[0] for i in self.flows if i[1] == "self" and len(i) == 2)
        self.output_channels = set(i[1] for i in self.flows if i[0] == "self" and len(i) == 2)

        self.input_channel_query_buffer = []
        self.output_channel_query_buffer = []
        self.input_env_query_buffer = []
        self.output_env_query_buffer = []

        self.input_channel_servers = {}
        self.output_channel_servers = {}

        self.query_msg_template = {}
        self.query_msg_template["performative"] = "query-ref"
        self.query_msg_template["ontology"] = "APiQuery"
        self.query_msg_template["auth-token"] = self.auth

        self.subscribe_msg_template = {}
        self.subscribe_msg_template["performative"] = "subscribe"
        self.subscribe_msg_template["ontology"] = "APiDataTransfer"
        self.subscribe_msg_template["auth-token"] = self.auth

        self.attach_msg_template = {}
        self.attach_msg_template["performative"] = "request"
        self.attach_msg_template["ontology"] = "APiDataTransfer"
        self.attach_msg_template["auth-token"] = self.auth

        self.environment_msg_template = {}
        self.environment_msg_template["ontology"] = "APiDataTransfer"
        self.environment_msg_template["auth-token"] = self.auth

        self.agree_msg_template = {}
        self.agree_msg_template["performative"] = "agree"
        self.agree_msg_template["ontology"] = "APiScheduling"
        self.agree_msg_template["auth-token"] = self.auth

        self.refuse_msg_template = {}
        self.refuse_msg_template["performative"] = "refuse"
        self.refuse_msg_template["ontology"] = "APiScheduling"
        self.refuse_msg_template["auth-token"] = self.auth
        # Add reason in actual behaviour (e.g. service-failed, security-policy)

        self.inform_msg_template = {}
        self.inform_msg_template["performative"] = "inform"
        self.inform_msg_template["ontology"] = "APiScheduling"
        self.inform_msg_template["type"] = "agent"
        self.inform_msg_template["auth-token"] = self.auth
        # Add exit-status (finished, error) and error-message (actual stacktrace, error code etc.); or add status (ready)

        for i in self.input_channels:
            try:
                self.subscribe_to_channel(i, "input")
            except NotImplementedError as e:
                logger.error(f"Not implemented for {str(e)}", i)
        for i in self.output_channels:
            try:
                self.subscribe_to_channel(i, "output")
            except NotImplementedError as e:
                logger.error(f"Not implemented for {str(e)}", i)

        self.input_ended = False

        self.shell_ip_stdin = None
        self.shell_port_stdin = None
        self.shell_ip_stdout = None
        self.shell_port_stdout = None
        self.shell_buffer = []

    def _load(self, fh: io.TextIOWrapper) -> None:
        """
        Agent definition file (.ad) loader.
        fh - open agent definition file handle
        """

        try:
            self.descriptor = load(fh.read(), Loader)
        except Exception as e:
            err = "Agent definition file cannot be loaded.\n" + str(e)
            raise APiAgentDefinitionError(err)
        if self.agentname != self.descriptor["agent"]["name"]:
            err = "Name in agent definition file does not match file name: %s != %s !" % (
                self.agentname,
                self.descriptor["agent"]["name"],
            )
            raise APiAgentDefinitionError(err)
        try:
            self.description = self.descriptor["agent"]["description"]
            self.type = self.descriptor["agent"]["type"]
            self.input_type = self.descriptor["agent"]["input"]["type"]
            self.input_data_type = self.descriptor["agent"]["input"]["data-type"]
            self.input_fmt = self.descriptor["agent"]["input"]["fmt"]
            self.input_cutoff = self.descriptor["agent"]["input"]["cutoff"]
            self.input_end = self.descriptor["agent"]["input"]["end"]
            self.input_value_type = self.descriptor["agent"]["input"]["value-type"]
            self.output_type = self.descriptor["agent"]["output"]["type"]
            self.output_data_type = self.descriptor["agent"]["output"]["data-type"]
            self.output_fmt = self.descriptor["agent"]["output"]["fmt"]
            self.output_cutoff = self.descriptor["agent"]["output"]["cutoff"]
            self.output_end = self.descriptor["agent"]["output"]["end"]
            self.output_value_type = self.descriptor["agent"]["output"]["value-type"]
        except Exception as e:
            err = "Agent definition file is invalid.\n" + str(e)
            raise APiAgentDefinitionError(err)

        if self.type == "unix":
            self.cmd = self.descriptor["agent"]["start"]
        elif self.type == "docker":
            name = self.descriptor["agent"]["name"]
            cmd = self.descriptor["agent"]["start"]

            self.cmd = f"docker run -a stdin -a stdout -i -t {name} {cmd}"
        elif self.type == "kubernetes":
            name = self.descriptor["agent"]["name"]
            cmd = self.descriptor["agent"]["start"]

            self.cmd = (
                f"kubectl run {name} --rm -it --restart=Never --image={name} --command -- {cmd}"
            )

        if self.type in ["unix", "docker", "kubernetes"]:
            # Initialize attributes to be used later
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

            # NC threads
            self.ncstdout_thread = None
            self.ncfile_thread = None
            self.nchttp_thread = None
            self.ncws_thread = None
            self.ncnc_thread = None
            self.ncncrec_thread = None

            try:
                self.process_descriptor()
            except Exception as e:
                err = "Agent definition file is invalid.\n" + str(e)
                raise APiAgentDefinitionError(err)
        else:
            err = "Invalid agent type: %s" % self.type
            raise APiAgentDefinitionError(err)

    async def output_callback(self, data: bytes) -> None:
        """
        Method used to send agent output / message to channels / environments it is attached to.
        """

        self.shell_buffer.append(data)
        logger.info(f"About to send {data.encode()} to attached channels")
        for channel, srv in self.output_channel_servers.items():
            logger.info(f"Sending {data.encode()} to {channel}...")
            is_udp = srv["protocol"] == "udp"
            sent = False
            srv["socket"] = nclib.Netcat((srv["server"], srv["port"]), udp=is_udp)
            while not sent:
                try:
                    srv["socket"].sendline(data.encode())
                    sent = True
                    logger.info(f"Done sending to channel {channel}")
                except (BrokenPipeError, ConnectionResetError):
                    logger.error(f"Error sending {data} (BROKEN PIPE)")
                    logger.info("Attempting to reconnect")
                    srv["socket"] = nclib.Netcat((srv["server"], srv["port"]), udp=is_udp)
        if data == self.output_delimiter:  # TODO: Verify this
            self.service_quit("End of output")

    def subscribe_to_channel(self, channel: str, channel_type: str) -> None:
        """
        Subscribe to a channel.
        """

        # TODO: Implement channel subscription (sender, receiver)
        # Channel types:
        # STDIN -> reads input from stdin
        # STDOUT/STDERR -> writes output to STDIN/STDERR
        # <name> -> gets instructions from channel on how
        #           to connect (via Netcat)
        if channel_type == "input":
            if channel == "STDOUT":
                err = "Input cannot be STDOUT"
                raise APiChannelDefinitionError(err)
            elif channel == "STDERR":
                err = "Input cannot be STDERR"
                raise APiChannelDefinitionError(err)
            elif channel == "STDIN":
                self.start_shell_client(prompt=True, await_stdin=True)
            elif channel == "ENV_INPUT":
                self.input_env_query_buffer.append(channel)
            else:
                self.input_channel_query_buffer.append(channel)
        elif channel_type == "output":
            if channel == "STDOUT":
                self.start_shell_client(print_stdout=True)
            elif channel == "STDERR":
                self.start_shell_client(print_stderr=False)
            elif channel == "STDIN":
                err = "Output cannot be STDIN"
                raise APiChannelDefinitionError(err)
            elif channel == "ENV_OUTPUT":
                self.output_env_query_buffer.append(channel)
            else:
                self.output_channel_query_buffer.append(channel)

    def start_shell_stdin(self, prompt: bool = False) -> None:
        """
        Start socket server for STDIN shell. If prompt is True
        write standard prompt (agentname :- ) before each
        input.
        """
        self.shell_socket_stdin = socket.socket()
        self.shell_socket_stdin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.shell_socket_stdin.bind(("0.0.0.0", 0))
        self.shell_socket_stdin.listen(0)
        self.shell_ip_stdin, self.shell_port_stdin = self.shell_socket_stdin.getsockname()

        self.shell_client_stdin, self.shell_client_stdin_addr = self.shell_socket_stdin.accept()

        if prompt:
            self.prompt = "\n%s (agent) :- " % self.name
        else:
            self.prompt = None

        BUFFER_SIZE = 1024

        self.shell_client_stdin.settimeout(0.1)

        threads = []

        error = False
        while True:
            try:
                if self.prompt and not error:
                    self.shell_client_stdin.send(self.prompt.encode())
                inp = self.shell_client_stdin.recv(BUFFER_SIZE).decode()
                if inp == "exit":
                    self.shell_client_stdin.close()
                    self.shell_socket_stdin.close()
                    break
                if self.input_ended:
                    self.shell_client_stdin.send(
                        "Input end delimiter received, agent is shutting down...".encode()
                    )
                    self.shell_client_stdin.close()
                    self.shell_socket_stdin.close()
                    break
                else:
                    t = Thread(target=self.input, args=(inp,))
                    t.start()
                    threads.append(t)
                error = False
            except Exception as e:
                logger.error("Error receiving from client", e)
                error = True
                sleep(0.1)

        # cleanup
        for t in threads:
            t.join()

    def start_shell_stdout(self) -> None:
        """
        Start socket server for STDOUT/STDERR shell.
        """

        self.shell_socket_stdout = socket.socket()
        self.shell_socket_stdout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.shell_socket_stdout.bind(("0.0.0.0", 0))
        self.shell_socket_stdout.listen(0)
        self.shell_ip_stdout, self.shell_port_stdout = self.shell_socket_stdout.getsockname()

        self.shell_client_stdout, self.shell_client_stdout_addr = self.shell_socket_stdout.accept()

        self.shell_client_stdout.settimeout(0.1)

        while True:
            try:
                while self.shell_buffer:
                    if len(self.shell_buffer) > 0:
                        data = self.shell_buffer.pop(0)
                        self.shell_client_stdout.send(data.encode())
                    if self.output_end:
                        if data[:-1] == self.output_end:
                            self.shell_client_stdout.send(
                                "Output end delimiter received, agent is shutting down...".encode()
                            )
                            self.shell_client_stdout.shutdown(2)
                            self.shell_client_stdout.close()
                            self.shell_socket_stdout.close()
                            return
            except Exception as e:
                logger.error("Error in start_shell_stdout", e)
                sleep(0.1)

    def start_shell_client(
        self,
        prompt: bool = True,
        await_stdin: bool = True,
        print_stdout: bool = True,
        print_stderr: bool = False,
    ) -> None:
        """
        Start the agents shell client.
        prompt - use a prompt for STDIN shell (will be ignored if await_stdin is False)
        await_stdin - if True attach agent's input to STDIN (print_stdout and print_stderr will be ignored)
        print_stdout - if True attach agent's output to STDOUT (print_stderr will be ignored)
        print_stderr - if True attach agent's output to STDERR
        """
        if await_stdin:
            self.shell_stdin_thread = Thread(target=self.start_shell_stdin, args=(prompt,))
            self.shell_stdin_thread.start()
        elif print_stdout or print_stderr:
            self.shell_stdout_thread = Thread(target=self.start_shell_stdout)
            self.shell_stdout_thread.start()
        sleep(0.1)

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
            err = "The shell has not been initialized"
            raise APiShellInitError(err)
        else:
            agent_tmp_dir = os.path.join(TMP_FOLDER, self.name)
            if not os.path.exists(agent_tmp_dir):
                os.makedirs(agent_tmp_dir)
            if await_stdin:
                self.dtach_session = os.path.join(TMP_FOLDER, self.name, "stdin")
            elif print_stdout:
                self.dtach_session = os.path.join(TMP_FOLDER, self.name, "stdout")
            elif print_stderr:
                self.dtach_session = os.path.join(TMP_FOLDER, self.name, "stderr")
            else:
                err = "No input and not output specified!"
                raise APiShellInitError(err)
            cmd = "dtach -A %s ./APishc.py %s %d" % (
                self.dtach_session,
                self.shell_ip,
                self.shell_port,
            )
            if await_stdin:
                cmd += " --input"
            elif print_stdout:
                cmd += " --output"
            elif print_stderr:
                cmd += " --error"
            self.shell_client_proc = pexpect.spawn(cmd)

            def output_filter(s):
                if "EOF - dtach terminating" in s.decode():
                    return "\n".encode()
                return s

            self.shell_client_proc.interact(output_filter=output_filter)

        if await_stdin:
            self.shell_stdin_thread.join()
        elif print_stdout or print_stderr:
            self.shell_stdout_thread.join()

    def get_channel_name(self, address: str) -> str:
        """
        Get the channel name from the address.
        """
        return list(self.address_book.keys())[list(self.address_book.values()).index(address)]

    def all_setup(self) -> bool:
        """
        Check if all channels are connected.
        """
        # TODO: Deal with forward channels
        try:
            connected_inputs = set([ch for ch in self.input_channel_servers.keys()])
            if self.input_channels == connected_inputs:
                connected_outputs = set([ch for ch in self.output_channel_servers.keys()])
                if self.output_channels == connected_outputs:
                    return True
        except AttributeError:
            pass
        return False

    async def setup(self) -> None:
        """
        Setup the agent.
        """

        super().setup()

        self.behaviour_sl = self.Ready()
        self.add_behaviour(self.behaviour_sl)

        self.behaviour_gca = self.RequestAdresses()
        self.add_behaviour(self.behaviour_gca)

        self.behaviour_qc = self.ReceiveAdresses()
        bqc_template = Template(metadata={"ontology": "APiQuery"})
        self.add_behaviour(self.behaviour_qc, bqc_template)

        self.behaviour_stic = self.SubscribeToReadFromChannels()
        self.add_behaviour(self.behaviour_stic)

        self.behaviour_atoc = self.SubscribeToWriteToChannels()
        self.add_behaviour(self.behaviour_atoc)

        self.behaviour_ste = self.SubscribeToReadFromInputEnvironment()
        self.add_behaviour(self.behaviour_ste)

        self.behaviour_ate = self.SubscribeToWriteToOutputEnvironment()
        self.add_behaviour(self.behaviour_ate)

        self.behaviour_sic = self.SetupReadChannelSockets()
        bsic_template = Template(metadata={"ontology": "APiDataTransfer", "type": "input"})
        self.add_behaviour(self.behaviour_sic, bsic_template)

        self.behaviour_soc = self.SetupWriteChannelSockets()
        bsoc_template = Template(metadata={"ontology": "APiDataTransfer", "type": "output"})
        self.add_behaviour(self.behaviour_soc, bsoc_template)

        # Note: this behaviour is attached inside Start behaviour
        self.behaviour_l = self.Listening()

        self.behaviour_ss = self.Start()
        bss_template = Template(metadata={"ontology": "APiScheduling", "action": "start"})
        self.add_behaviour(self.behaviour_ss, bss_template)

    class Ready(OneShotBehaviour):
        """
        Ready behaviour.

        Once the agent is created, this one shot behaviour is used to inform the holon of
        the agent's status.
        """

        async def run(self) -> None:
            metadata = deepcopy(self.agent.inform_msg_template)
            metadata["status"] = "listening"
            await self.agent.schedule_message(self.agent.holon, metadata=metadata)

    class RequestAdresses(OneShotBehaviour):
        """
        Request addresses.

        Sending msg to holon once flows of this agent are identified, so that holon
        can pass down XMPP details for this agent to communicate with other agents via channels.

        Ontology: APiQuery
        """

        async def run(self) -> None:
            # waiting for address book containing input channels from holon
            logger.debug(f"Inputs: {self.agent.input_channel_query_buffer}")
            for inp in self.agent.input_channel_query_buffer:
                metadata = self.agent.query_msg_template
                metadata["reply-with"] = str(uuid4().hex)
                metadata["channel"] = inp
                await self.agent.schedule_message(self.agent.holon, metadata=metadata)

            logger.debug(f"Outputs: {self.agent.output_channel_query_buffer}")
            for out in self.agent.output_channel_query_buffer:
                logger.debug(f"Looking up channel {out} in addressbook")
                # in case we retrieved the channel from input channels address book batch
                try:
                    channel = self.agent.address_book[out]
                    logger.debug(f"Got channel {out} address {channel}")
                    await asyncio.sleep(0.1)
                except KeyError:
                    logger.debug(f"Could not find channel {out} in address book, querying")
                    metadata = self.agent.query_msg_template
                    metadata["reply-with"] = str(uuid4().hex)
                    metadata["channel"] = out
                    await self.agent.schedule_message(self.agent.holon, metadata=metadata)

            if (
                len(self.agent.input_env_query_buffer) > 0
                or len(self.agent.output_env_query_buffer) > 0
            ):
                metadata = self.agent.query_msg_template
                metadata["reply-with"] = str(uuid4().hex)
                metadata["channel"] = "ENVIRONMENT"
                await self.agent.schedule_message(self.agent.holon, metadata=metadata)

    class SubscribeToReadFromChannels(OneShotBehaviour):
        """
        Subscribe to read from channels behaviour.

        Sending requests to channels to subscribe them for reading its messages.
        """

        async def run(self) -> None:
            await self.agent.behaviour_gca.join()
            logger.debug(f"Subscribing to inputs: {self.agent.input_channel_query_buffer}")
            for inp in self.agent.input_channel_query_buffer:
                # waiting until holon sends the address book
                while inp not in self.agent.address_book:
                    await asyncio.sleep(0.1)
                channel = self.agent.address_book[inp]
                metadata = self.agent.subscribe_msg_template
                metadata["reply-with"] = str(uuid4().hex)
                await self.agent.schedule_message(channel, metadata=metadata)

    class SubscribeToWriteToChannels(OneShotBehaviour):
        """
        Subscribe to write to channels behaviour.

        Sending requests to channels to subscribe them for writing to them.
        """

        async def run(self) -> None:
            await self.agent.behaviour_gca.join()
            logger.debug(f"Attaching to outputs: {self.agent.output_channel_query_buffer}")
            for out in self.agent.output_channel_query_buffer:
                # waiting until holon sends the address book
                while out not in self.agent.address_book:
                    await asyncio.sleep(0.1)
                channel = self.agent.address_book[out]
                metadata = self.agent.attach_msg_template
                metadata["reply-with"] = str(uuid4().hex)
                await self.agent.schedule_message(channel, metadata=metadata)

    class SubscribeToReadFromInputEnvironment(OneShotBehaviour):
        """
        Subscribe to read from input environment behaviour.

        Sending requests to input environment to subscribe it for reading its messages.
        """

        async def run(self) -> None:
            await self.agent.behaviour_gca.join()
            logger.debug(f"Subscribing to environment inputs: {self.agent.input_env_query_buffer}")
            for inp in self.agent.input_env_query_buffer:
                # waiting until holon sends the address book
                while "ENVIRONMENT" not in self.agent.address_book:
                    await asyncio.sleep(0.1)
                channel = self.agent.address_book["ENVIRONMENT"]
                metadata = self.agent.environment_msg_template
                metadata["performative"] = (
                    "subscribe_to_input" if inp == "ENV_INPUT" else "subscribe_to_output"
                )
                metadata["reply-with"] = str(uuid4().hex)
                await self.agent.schedule_message(channel, metadata=metadata)

    class SubscribeToWriteToOutputEnvironment(OneShotBehaviour):
        """
        Subscribe to read from input environment behaviour.

        Sending requests to output environment to subscribe it for writing to it.
        """

        async def run(self) -> None:
            await self.agent.behaviour_gca.join()
            logger.debug(
                f"Subscribing to environment outputs: {self.agent.output_env_query_buffer}"
            )
            for out in self.agent.output_env_query_buffer:
                # waiting until holon sends the address book
                while "ENVIRONMENT" not in self.agent.address_book:
                    await asyncio.sleep(0.1)
                env = self.agent.address_book["ENVIRONMENT"]
                metadata = self.agent.environment_msg_template
                metadata["performative"] = (
                    "request_to_input" if out == "ENV_INPUT" else "request_to_output"
                )
                metadata["reply-with"] = str(uuid4().hex)
                await self.agent.schedule_message(env, metadata=metadata)

    class ReceiveAdresses(CyclicBehaviour):
        """
        Receive addresses behaviour.

        Holon will pass down the address book to the agent for the requested channels.
        """

        async def run(self) -> None:
            msg = await self.receive(timeout=0.1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(ReceiveAdresses) Message verified, processing ...")
                    channel = msg.metadata["address"]
                    try:
                        self.agent.input_ack.remove(msg.metadata["in-reply-to"])

                        if msg.metadata["performative"] == "refuse":
                            logger.debug(
                                f"Error getting channel address due to {msg.metadata['reason']}"
                            )
                            await self.agent.stop()
                        elif msg.metadata["success"] == "true":
                            self.agent.address_book[msg.metadata["agent"]] = channel
                        else:
                            logger.debug("Error getting channel address. Channel unknown to holon.")
                            await self.agent.stop()

                    except KeyError:
                        logger.debug(
                            f"I have no memory of this message ({msg.metadata['in-reply-to']}). (awkward Gandalf look)"
                        )
                else:
                    logger.debug("Message could not be verified.")

    class SetupReadChannelSockets(CyclicBehaviour):
        """
        Setup read channel sockets behaviour.

        Once agent has requested to subscribe to channel, channel will query back with open socket details.
        """

        async def run(self):
            await self.agent.behaviour_atoc.join()
            msg = await self.receive(timeout=1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(SetupReadChannelSockets) Message verified, processing ...")
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
                            servers = self.agent.input_channel_servers
                            logger.debug(
                                f"(SetupReadChannelSockets) Setting up {msg.metadata['type']} channel {channel}"
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

                            if len(self.agent.output_channel_servers) == len(
                                self.agent.output_channels
                            ) and len(self.agent.input_channel_servers) == len(
                                self.agent.input_channels
                            ):
                                # letting holon know once agent is all set up
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

    class SetupWriteChannelSockets(CyclicBehaviour):
        """
        Setup write channel sockets behaviour.

        Once agent has requested to subscribe to channel, channel will query back with open socket details.
        """

        async def run(self) -> None:
            await self.agent.behaviour_atoc.join()
            msg = await self.receive(timeout=1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(SetupWriteChannelSockets) Message verified, processing ...")
                    try:
                        self.agent.input_ack.remove(msg.metadata["in-reply-to"])
                        if msg.metadata["performative"] == "refuse":
                            logger.debug(
                                f"Error connecting to channel address due to {msg.metadata['reason']}"
                            )
                            await self.agent.stop()  # TODO: Inform holon about failure
                        else:
                            channel = msg.metadata["agent"]
                            is_udp = msg.metadata["protocol"] == "udp"
                            servers = self.agent.output_channel_servers
                            logger.debug(
                                f"(SetupWriteChannelSockets) Setting up {msg.metadata['type']} channel {channel}"
                            )
                            servers[channel] = {}
                            servers[channel]["server"] = msg.metadata["server"]
                            servers[channel]["port"] = int(msg.metadata["port"])
                            servers[channel]["protocol"] = msg.metadata["protocol"]
                            servers[channel]["socket"] = nclib.Netcat(
                                (msg.metadata["server"], int(msg.metadata["port"])),
                                udp=is_udp,
                            )

                            logger.info(
                                f"Connected to output channel {channel} at {msg.metadata['server']}:{msg.metadata['port']}"
                            )

                            if len(self.agent.output_channel_servers) == len(
                                self.agent.output_channels
                            ) and len(self.agent.input_channel_servers) == len(
                                self.agent.input_channels
                            ):
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

    class Listening(CyclicBehaviour):
        """
        Listening behaviour.

        This is behaviour runs cyclically which adheres to how sockets work (in loop).
        It listens for incoming connections and messages from channels / environment that this agent is subscribed to.
        """

        async def run(self) -> None:
            # TODO: Deal with forward channels
            if self.agent.all_setup():
                for channel, srv in self.agent.input_channel_servers.items():
                    is_udp = True if srv["protocol"] == "udp" else False

                    if is_udp:
                        result = srv["socket"].recv_until(self.agent.delimiter, timeout=0.1)
                    else:
                        result = srv["socket"].recv_until(self.agent.delimiter, timeout=0.2)
                    # sleep( 0.5 ) # TODO: Investigate if this line is needed
                    if result:
                        logger.info(f"Received message from channel {channel}: {result}")
                        self.agent.input(result.decode())

    class Start(CyclicBehaviour):
        """
        Start behaviour.

        Agent informs holon that it is ready to start. Holon will let agent know when it is time to start.

        Ontology: APiScheduling
        Status: Start
        """

        async def run(self) -> None:
            msg = await self.receive(timeout=1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(Start) Message verified, processing ...")
                    logger.debug("(Start) Holon has scheduled us to start. Starting service!")
                    # based on agent description (ws, http, etc.), this will setup the agent to be able to communicate
                    self.agent.service_start()
                    self.agent.add_behaviour(self.agent.behaviour_l)  # Start listening for input
                else:
                    logger.debug("Message could not be verified.")


def main(
    name: str,
    address: str,
    password: str,
    holon: str,
    holon_name: str,
    token: str,
    flows: str,
) -> None:
    """
    Main function to start the agent.
    """

    flows = json.loads(flows)
    flows = [(i[0], i[1]) if len(i) == 2 else (i[0], i[1], i[2]) for i in flows]
    a = APiAgent(name, address, password, holon, holon_name, token, flows)

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
    parser.add_argument("name", metavar="NAME", type=str, help="Agent's local APi name")
    parser.add_argument("address", metavar="ADDRESS", type=str, help="Agent's XMPP/JID address")
    parser.add_argument("password", metavar="PWD", type=str, help="Agent's XMPP/JID password")
    parser.add_argument(
        "holon",
        metavar="HOLON",
        type=str,
        help="Agent's instantiating holon's XMPP/JID address",
    )
    parser.add_argument(
        "holon_name",
        metavar="HOLON_NAME",
        type=str,
        help="Agent's instantiating holon's name",
    )
    parser.add_argument("token", metavar="TOKEN", type=str, help="Agent's security token")
    parser.add_argument("flows", metavar="FLOWS", type=str, help="Agent's communication flows")

    args = parser.parse_args()

    main(
        args.name,
        args.address,
        args.password,
        args.holon,
        args.holon_name,
        args.token,
        args.flows,
    )
