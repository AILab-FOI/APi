import asyncio
import json
import shlex
import subprocess as sp
from copy import deepcopy
from threading import Thread
from uuid import uuid4

from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template

from src.agents.base.base_communication import APiCommunication
from src.agents.tools.execution_plan import resolve_execution_plan
from src.models.namespace import APiNamespace
from src.orchestration.registrar import APiRegistrationService
from src.utils.logger import setup_logger
from typing import Dict, List

logger = setup_logger("holon")


class APiHolon(APiCommunication):
    """A holon created by an .api file."""

    def __init__(
        self,
        holonname,
        name,
        password,
        agents,
        channels,
        environment,
        holons_addressbook,
        execution_plans,
    ):
        self.token = str(uuid4().hex)
        super().__init__(name, password, str(uuid4().hex))
        self.holonname = holonname
        self.address = str(self.jid.bare())
        self.namespace = APiNamespace()
        self.registrar = APiRegistrationService(holonname)

        self.environment = None
        if environment:
            self.setup_environment(environment)

        self.channels = {}
        for c in channels:
            self.setup_channel(c)

        self.agent_types = {}
        self.agents = {}
        for a in agents:
            self.create_agent_types_map(a)

        self.holons = holons_addressbook

        self.execution_plans = None
        if len(execution_plans) > 0:
            self.setup_execution(execution_plans)

        self.all_channels_listening = False
        self.all_agents_listening = False

        self.all_started = False  # Indicate if execution plan has been started already
        self.start_env_and_channels()

        self.query_message_template = {}
        self.query_message_template["performative"] = "inform-ref"
        self.query_message_template["ontology"] = "APiQuery"
        self.query_message_template["auth-token"] = self.auth

        self.refuse_message_template = {}
        self.refuse_message_template["performative"] = "refuse"
        self.refuse_message_template["ontology"] = "APiQuery"
        self.refuse_message_template["auth-token"] = self.auth
        self.refuse_message_template["reason"] = "security-policy"

        self.request_message_template = {}
        self.request_message_template["performative"] = "request"
        self.request_message_template["ontology"] = "APiScheduling"
        self.request_message_template["auth-token"] = self.auth
        # Add action in actual behaviour (start or stop)

        # template used for ack
        self.confirm_message_template = {}
        self.confirm_message_template["performative"] = "confirm"
        self.confirm_message_template["ontology"] = "APiScheduling"
        self.confirm_message_template["auth-token"] = self.auth

    def create_agent_types_map(self, agent: Dict) -> None:
        """
        Create a map of agent types.
        """

        self.agent_types[agent["name"]] = agent

    def adjust_flows_by_args(self, agent_args: List, agent_params: List, flows: List) -> List:
        """
        Adjust flows by arguments.
        """

        param_by_arg = {}
        for i in range(0, len(agent_args)):
            arg_name = agent_args[i]
            param_value = agent_params[i]

            param_by_arg[arg_name] = param_value

        adjusted_flows = []
        for source, destination in flows:
            adjusted_flow = (
                param_by_arg.get(source, source),
                param_by_arg.get(destination, destination),
            )
            adjusted_flows.append(adjusted_flow)

        return adjusted_flows

    def setup_agent(
        self, agent_type: str, id: str = None, plan_id: str = None, params: List = None
    ) -> None:
        """
        Setup an agent.
        """

        if not id:
            id = uuid4().hex

        agent = deepcopy(self.agent_types[agent_type])
        logger.debug(f"Registering agent {agent['name']}")
        address, password = self.registrar.register(agent["name"])
        if params:
            flows = self.adjust_flows_by_args(agent["args"], params, agent["flows"])
        else:
            flows = agent["flows"]

        # NOTE: This should be updated if agent.py is moved around
        agent["cmd"] = (
            'poetry run python ../src/agents/agent.py "%s" "%s" "%s" "%s" "%s" "%s" "%s"'
            % (
                agent["name"],
                address,
                password,
                self.address,
                self.holonname,
                self.token,
                json.dumps(flows).replace('"', '\\"'),
            )
        )
        agent["address"] = address
        agent["status"] = "setup"
        agent["id"] = id
        agent["plan_id"] = plan_id
        self.agents[id] = agent

    def setup_channel(self, channel: Dict) -> None:
        """
        Setup a channel.
        """

        address, password = self.registrar.register(channel["name"])
        logger.debug(f"Registering channel {channel['name']}")

        # NOTE: This should be updated if channel.py is moved around
        channel["cmd"] = (
            'poetry run python ../src/agents/channel.py "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"'
            % (
                channel["name"],
                address,
                password,
                self.address,
                self.token,
                json.dumps((self.registrar.min_port, self.registrar.max_port)),
                channel["protocol"],
                json.dumps(channel["input"]).replace('"', '""'),
                json.dumps(channel["output"]).replace('"', '""'),
            )
        )
        channel["address"] = address
        channel["status"] = "setup"
        self.channels[channel["name"]] = channel

    def setup_environment(self, env: Dict) -> None:
        """
        Setup an environment.
        """

        environment = {}
        environment["name"] = f"{self.holonname}-environment"
        address, password = self.registrar.register(environment["name"])

        # NOTE: This should be updated if environment.py is moved around
        environment["cmd"] = (
            'poetry run python ../src/agents/environment.py "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"'
            % (
                environment["name"],
                address,
                password,
                self.address,
                self.holonname,
                self.token,
                json.dumps((self.registrar.min_port, self.registrar.max_port)),
                env["input_protocol"],
                env["output_protocol"],
                json.dumps(env["input"]).replace('"', '""'),
                json.dumps(env["output"]).replace('"', '""'),
                json.dumps(self.holons).replace('"', '\\"'),
            )
        )
        environment["address"] = address
        environment["status"] = "setup"
        self.environment = environment

    def setup_execution(self, execution_plans: List) -> None:
        """
        Setup an execution.
        """

        if execution_plans is None:
            return

        resolved_execution_plans = [resolve_execution_plan(plan) for plan in execution_plans]
        self.execution_plans = resolved_execution_plans

    def agent_name_from_address(self, address: str) -> str:
        """
        Get the name of an agent from its address.
        """

        address = str(address)
        for name, agent in self.agents.items():
            if agent["address"] == address:
                return name

    def channel_name_from_address(self, address: str) -> str:
        """
        Get the name of a channel from its address.
        """

        address = str(address)
        for name, channel in self.channels.items():
            if channel["address"] == address:
                return name

    def start_basic_agent_thread(self, cmd: List) -> sp.Popen:
        """
        Start a basic agent thread.
        """

        return sp.Popen(cmd, stderr=sp.STDOUT, start_new_session=True)

    def agent_finished(self, a_id: str, plan_id: str, status_code: int) -> None:
        """
        Agent finished.
        """

        plan = None
        for p in self.execution_plans:
            if p["id"] == plan_id:
                plan = p
        agent_exec = plan["plan"].get(a_id, None)

        # may not be needed, unless errored
        self.agents[a_id]["status"] = "stopped"

        operator = agent_exec["operator"]
        succeeding_agent_id = None
        # start agent again
        if operator == "+":
            succeeding_agent_id = a_id
        # start new agent if current errors
        elif operator == "!":
            if status_code != 0:
                succeeding_agent_id = agent_exec["succeeding_agent_id"]
        # start new agent if current succeeds
        elif operator == "&":
            if status_code == 0:
                succeeding_agent_id = agent_exec["succeeding_agent_id"]
        # no matter the status, start the new agent
        elif not operator:
            succeeding_agent_id = agent_exec["succeeding_agent_id"]

        succeeding_agent = None
        if succeeding_agent_id is not None:
            for a in self.agents.values():
                if a["id"] == succeeding_agent_id:
                    succeeding_agent = a

        if succeeding_agent is not None:
            self.run_agent_thread(succeeding_agent, "dependant")

    def start_dependant_agent_thread(self, a_id: str, plan_id: str, cmd: List) -> None:
        """
        Start a dependant agent thread.
        """

        proc = sp.Popen(cmd, start_new_session=True)
        proc.communicate()
        return_code = proc.returncode

        self.agent_finished(a_id, plan_id, return_code)

    def start_env_and_channels(self) -> None:
        """
        Start the environment and channels.
        """

        if self.environment:
            cmd = shlex.split(self.environment["cmd"])
            logger.debug(f"Running environment: {self.environment.get('name')}")
            self.environment["instance"] = Thread(target=self.start_basic_agent_thread, args=(cmd,))
            self.environment["instance"].start()
            self.environment["status"] = "started"

        for c in self.channels.values():
            cmd = shlex.split(c["cmd"])
            logger.debug(f"Running channel: {c.get('name')}")
            c["instance"] = Thread(target=self.start_basic_agent_thread, args=(cmd,))
            c["instance"].start()
            c["status"] = "started"

    def setup_agents(self) -> None:
        """
        Setup agents.
        """

        if self.execution_plans:
            for execution_plan in self.execution_plans:
                plan = execution_plan["plan"]
                plan_id = execution_plan["id"]
                agent_ids = [a_id for a_id in plan.keys()]
                for a_id in agent_ids:
                    a_ref = plan[a_id]
                    a_type = a_ref["name"]
                    a_args = a_ref.get("args", None)
                    self.setup_agent(a_type, a_id, plan_id, a_args)
        else:
            for a_type in self.agent_types.keys():
                self.setup_agent(a_type)

    def run_agent_thread(self, a: Dict, start_type: str) -> None:
        """
        Run an agent thread.
        """

        cmd = shlex.split(a["cmd"])
        a_id = a["id"]
        plan_id = a["plan_id"]
        logger.debug(f"Running agent: {a.get('name')}")
        if start_type == "dependant":
            a["instance"] = Thread(
                target=self.start_dependant_agent_thread, args=(a_id, plan_id, cmd)
            )
        else:
            a["instance"] = Thread(target=self.start_basic_agent_thread, args=(cmd,))
        a["instance"].start()
        a["status"] = "started"

    def start_initial_agents(self) -> None:
        """
        Start initial agents.
        """

        if self.execution_plans:
            for execution_plan in self.execution_plans:
                i_agent_ids = execution_plan["initial_agents_to_run"]
                for a in self.agents.values():
                    if a["id"] in i_agent_ids:
                        self.run_agent_thread(a, "dependant")
        else:
            for a in self.agents.values():
                self.run_agent_thread(a, "basic")

    async def stop(self) -> None:
        """
        Stop all agents & channels.
        """

        logger.debug("(Stop Agents) Stopping all agents & channels!")
        metadata = deepcopy(self.request_message_template)
        metadata["action"] = "stop"
        for c in self.channels.values():
            await self.schedule_message(c["address"], metadata=metadata)
        for a in self.agents.values():
            await self.schedule_message(a["address"], metadata=metadata)

    async def setup(self) -> None:
        """
        Setup the holon behaviours.
        """

        super().setup()

        bqn = self.RequestForAddress()
        bqn_template = Template(metadata={"performative": "query-ref", "ontology": "APiQuery"})
        self.add_behaviour(bqn, bqn_template)

        bgra = self.GetReadyAgents()
        bgra_template = Template(
            metadata={
                "performative": "inform",
                "ontology": "APiScheduling",
                "type": "agent",
                "status": "ready",
            }
        )
        self.add_behaviour(bgra, bgra_template)

        bgla = self.GetListeningAgentsAndChannels()
        bgla_template = Template(
            metadata={
                "performative": "inform",
                "ontology": "APiScheduling",
                "status": "listening",
            }
        )
        self.add_behaviour(bgla, bgla_template)

        bcl = self.AllChannelsListening()
        self.add_behaviour(bcl)

        bep = self.ExecutePlan()
        self.add_behaviour(bep)

        bfa = self.FinishedAgents()
        bfa_template = Template(
            metadata={
                "performative": "inform",
                "ontology": "APiScheduling",
                "status": "finished",
            }
        )
        self.add_behaviour(bfa, bfa_template)

        bsa = self.StopAgents()
        bsa_template = Template(
            metadata={
                "performative": "inform",
                "ontology": "APiScheduling",
                "status": "stopped",
            }
        )
        self.add_behaviour(bsa, bsa_template)

    class RequestForAddress(CyclicBehaviour):
        """
        Agent request for address.

        Agent will request for address of a channel. Holon will respond with the address.
        """

        async def run(self) -> None:
            msg = await self.receive(timeout=0.1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(QueryName) Message verified, processing ...")
                    channel = msg.metadata["channel"]
                    metadata = deepcopy(self.agent.query_message_template)
                    metadata["in-reply-to"] = msg.metadata["reply-with"]
                    metadata["agent"] = channel

                    try:
                        if (
                            channel == "ENVIRONMENT" or channel == self.agent.holonname
                        ) and self.agent.environment is not None:
                            address = self.agent.environment["address"]
                        else:
                            address = self.agent.channels[channel]["address"]

                        logger.debug(f"Found channel {channel} address is {address}")

                        metadata["success"] = "true"
                        metadata["address"] = address
                    except KeyError:
                        logger.debug(f"Channel {channel} not found")
                        metadata["success"] = "false"
                        metadata["address"] = "null"
                    await self.agent.schedule_message(str(msg.sender), metadata=metadata)

                else:
                    logger.debug("Message could not be verified.")
                    metadata = deepcopy(self.agent.refuse_message_template)
                    metadata["in-reply-to"] = msg.metadata["reply-with"]
                    await self.agent.schedule_message(str(msg.sender), metadata=metadata)

    class GetReadyAgents(CyclicBehaviour):
        """
        Get ready agents behaviour.

        Started up agents will notify when they are ready and waiting for further instructions.
        Once all agents are ready, holon will inform them they can start with the execution.
        """

        async def run(self) -> None:
            msg = await self.receive(timeout=0.1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(QueryNameGetReadyAgents) Message verified, processing ...")
                    agent = self.agent.agent_name_from_address(msg.sender.bare())
                    logger.debug(
                        f"(QueryNameGetReadyAgents) Setting agent {agent} status to ready."
                    )
                    self.agent.agents[agent]["status"] = "ready"
                else:
                    logger.debug("Message could not be verified.")
                    metadata = deepcopy(self.agent.refuse_message_template)
                    metadata["in-reply-to"] = msg.metadata["reply-with"]
                    await self.agent.schedule_message(str(msg.sender), metadata=metadata)

    class GetListeningAgentsAndChannels(CyclicBehaviour):
        """
        Get listening agents and channels behaviour.

        All agents and channels will notify when they are listening.
        """

        async def run(self) -> None:
            msg = await self.receive(timeout=0.1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(GetListeningAgentsAndChannels) Message verified, processing ...")
                    type = msg.metadata["type"]

                    if type == "channel":
                        channel = self.agent.channel_name_from_address(msg.sender.bare())
                        logger.debug(
                            f"(GetListeningAgentsAndChannels) Setting channel {channel} status to listening."
                        )
                        self.agent.channels[channel]["status"] = "listening"

                        all_ready = True
                        for channel in self.agent.channels.values():
                            if channel["status"] != "listening":
                                all_ready = False

                        if all_ready:
                            self.agent.all_channels_listening = True
                    elif type == "agent":
                        agent = self.agent.agent_name_from_address(msg.sender.bare())
                        logger.debug(
                            f"(QueryNameGetReadyAgents) Setting agent {agent} status to listening."
                        )
                        self.agent.agents[agent]["status"] = "listening"

                        all_ready = True
                        for agent in self.agent.agents.values():
                            if agent["status"] != "ready" and agent["status"] != "listening":
                                all_ready = False
                                break

                            if all_ready:
                                self.agent.all_agents_listening = True
                    elif type == "environment":
                        self.agent.environment["status"] = "listening"
                else:
                    logger.debug("Message could not be verified.")
                    metadata = deepcopy(self.agent.refuse_message_template)
                    metadata["in-reply-to"] = msg.metadata["reply-with"]
                    await self.agent.schedule_message(str(msg.sender), metadata=metadata)

    class AllChannelsListening(OneShotBehaviour):
        """
        All channels listening behaviour.

        Behaviour that checks if all channels are listening, in which case it will start the agents.
        """

        async def run(self) -> None:
            while (
                len(self.agent.channels.values()) > 0 and not self.agent.all_channels_listening
            ) or (
                self.agent.environment is not None
                and self.agent.environment["status"] != "listening"
            ):
                await asyncio.sleep(1)

            self.agent.setup_agents()
            self.agent.start_initial_agents()

    class ExecutePlan(CyclicBehaviour):
        """
        Execute plan behaviour.

        This behaviour checks what are the execution plans that can be executed.
        """

        async def run(self) -> None:
            # wait until we have some agents running
            if len(self.agent.agents.values()) == 0:
                return

            metadata = deepcopy(self.agent.request_message_template)
            metadata["action"] = "start"

            if self.agent.execution_plans:
                for plan in self.agent.execution_plans:
                    # starting dependant agents once the execution plan has already been started (and initial agents launched)
                    if plan["started"]:
                        for p_a_id in plan["plan"].keys():
                            a = self.agent.agents[p_a_id]
                            if a["status"] == "ready":
                                self.agent.agents[p_a_id]["status"] = "executing"
                                await self.agent.schedule_message(a["address"], metadata=metadata)

                        # no need to check flow below, as it deals with inital agents, which are already started
                        continue

                    # starting initial agents
                    i_agent_ids = plan["initial_agents_to_run"]

                    all_ready = True
                    for agent in self.agent.agents.values():
                        if agent["id"] in i_agent_ids and agent["status"] != "ready":
                            all_ready = False

                    if all_ready:
                        logger.debug("(Execute plan) All agents ready, scheduling them for start!")
                        for agent in self.agent.agents.values():
                            if agent["id"] in i_agent_ids:
                                self.agent.agents[agent["id"]]["status"] = "executing"
                                await self.agent.schedule_message(
                                    agent["address"], metadata=metadata
                                )
                        plan["started"] = True

            else:
                # Tell all agents to start if they are ready
                all_ready = True
                for agent in self.agent.agents.values():
                    if agent["status"] != "ready":
                        all_ready = False
                        break
                if all_ready and not self.agent.all_started:
                    logger.debug("(Execute plan) All agents ready, scheduling them for start!")
                    for agent in self.agent.agents.values():
                        self.agent.agents[agent["id"]]["status"] = "executing"
                        await self.agent.schedule_message(agent["address"], metadata=metadata)
                    self.agent.all_started = True

    class FinishedAgents(CyclicBehaviour):
        """
        Finished agents behaviour.

        Behaviour that listens to XMPP mesage that is sent from an agent when it is finished processing.
        Agent will communicate their status over XMPP. Deleberatelly stopped & finished agents share the same status.

        Ontology: APiScheduling
        Status: finished
        """

        async def run(self) -> None:
            msg = await self.receive(timeout=0.1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(FinishedAgents) Message verified, processing ...")
                    agent = self.agent.agent_name_from_address(msg.sender.bare())

                    if msg.metadata["error-message"] != "null":
                        logger.debug(
                            f"Agent {agent} finished with error {str(msg['error-message'])}"
                        )
                    else:
                        logger.debug(f"Agent {agent} finished gracefully.")
                    self.agent.agents[agent]["status"] = "stopped"

                    # sending message to ack that agent has stopped, so they can terminate
                    metadata = deepcopy(self.agent.confirm_message_template)
                    metadata["action"] = "finish"
                    metadata["in-reply-to"] = msg.metadata["reply-with"]

                    await self.agent.schedule_message(str(msg.sender), metadata=metadata)

                else:
                    logger.debug("Message could not be verified.")
                    metadata = deepcopy(self.agent.refuse_message_template)
                    metadata["in-reply-to"] = msg.metadata["reply-with"]
                    await self.agent.schedule_message(str(msg.sender), metadata=metadata)

    class StopAgents(CyclicBehaviour):
        """
        Stop agents behaviour.

        Agent will communicate their status over XMPP. Deleberatelly stopped & finished agents share the same status.

        Ontology: APiScheduling
        Status: finished
        """

        def all_stopped(self, agents: List) -> bool:
            """
            Check if all agents are stopped.
            """

            if any(a["status"] != "stopped" for a in agents):
                return False

            return True

        async def run(self) -> None:
            msg = await self.receive(timeout=0.1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(StopAgents) Message verified, processing ...")
                    agent = self.agent.agent_name_from_address(msg.sender.bare())

                    if msg.metadata["error-message"] != "null":
                        logger.debug(
                            f"Agent {agent} stopped with error {str(msg['error-message'])}"
                        )
                    else:
                        logger.debug(f"Agent {agent} stopped gracefully.")
                    self.agent.agents[agent]["status"] = "stopped"

                    all_stopped = self.all_stopped(
                        [*self.agent.agents.values(), *self.agent.channels.values()]
                    )

                    if all_stopped:
                        logger.debug("(StopAgents) All agents have stopped ...")
                        logger.debug("(StopAgents) Holon stopping ...")

                        await super().stop()

                else:
                    logger.debug("Message could not be verified.")
                    metadata = deepcopy(self.agent.refuse_message_template)
                    metadata["in-reply-to"] = msg.metadata["reply-with"]
                    await self.agent.schedule_message(str(msg.sender), metadata=metadata)
