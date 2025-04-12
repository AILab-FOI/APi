from typing import Optional

import requests

# When using HTTPS with insecure servers this has to be uncommented
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from src.utils.helpers import hash, verify
from src.utils.logger import setup_logger

logger = setup_logger("base_talking_agent")

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


import logging
from copy import deepcopy


class APiCommunication(Agent):
    """
    Logic for communication with other SPADE agents.
    """

    def __init__(self, name: str, password: str, token: Optional[str] = None):
        super().__init__(name, password)

        self.token = token
        if token:
            self.auth = hash(str(self.jid.bare()) + self.token)
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
        self.delimiter = "\n"

        # Address book of other agents
        self.address_book = {}

        self.LOG = logging.getLogger("APiAgent")

    def verify(self, msg: Message) -> bool:
        """
        Verify the message
        """
        return verify(msg.metadata["auth-token"], str(msg.sender.bare()) + self.token)

    def setup(self) -> None:
        """
        Setup the agent
        """
        self.behaviour_output = self.OutputQueue()
        self.add_behaviour(self.behaviour_output)

        st_template = Template(metadata={"ontology": "APiScheduling", "action": "stop"})
        st = self.Stop()
        self.add_behaviour(st, st_template)

        bt_template = Template(
            metadata={
                "ontology": "APiScheduling",
                "action": "finish",
                "performative": "confirm",
            }
        )
        bt = self.Terminate()
        self.add_behaviour(bt, bt_template)

    async def schedule_message(self, to: str, body: str = "", metadata: dict = {}) -> None:
        """
        Schedule a message
        """
        # TODO: See if this can be done in a more elegant way ...
        msg = Message(to=to, body=body, metadata=deepcopy(metadata))
        logger.debug(f"Sending message: {msg.metadata} {msg.to}")
        await self.behaviour_output.send(deepcopy(msg))
        try:
            self.input_ack.add(msg.metadata["reply-with"])
        except KeyError:
            pass

    class OutputQueue(CyclicBehaviour):
        """
        Output queue behaviour
        """

        async def run(self) -> None:
            pass

    class Stop(CyclicBehaviour):
        """
        Stop behaviour
        """

        async def run(self) -> None:
            msg = await self.receive(timeout=1)
            if msg:
                if self.agent.verify(msg):
                    logger.debug("(StopAgent) Message verified, processing ...")
                    logger.debug("(StopAgent) Holon has scheduled us to stop. Stopping!")

                    metadata = deepcopy(self.agent.inform_msg_template)
                    metadata["status"] = "stopped"
                    await self.agent.schedule_message(self.agent.holon, metadata=metadata)

                    await self.agent.stop()
                else:
                    logger.debug("Message could not be verified. IMPOSTER!!!!!!")

    class Terminate(CyclicBehaviour):
        """
        Terminate behaviour
        """

        async def run(self) -> None:
            msg = await self.receive(timeout=1)
            if msg:
                if self.agent.verify(msg):
                    await self.agent.stop()
                else:
                    logger.debug("Message could not be verified. IMPOSTER!!!!!!")
