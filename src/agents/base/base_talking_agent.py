from src.utils.helpers import verify, hash
from typing import Optional

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message

import requests

# When using HTTPS with insecure servers this has to be uncommented
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


import logging
from copy import deepcopy


class APiTalkingAgent(Agent):
    """
    Base agent that implements logic for communication with other SPADE agents.
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

    def say(self, *msg):
        pass

    def verify(self, msg):
        return verify(msg.metadata["auth-token"], str(msg.sender.bare()) + self.token)

    def setup(self):
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

    async def schedule_message(self, to, body="", metadata={}):
        # TODO: See if this can be done in a more elegant way ...
        msg = Message(to=to, body=body, metadata=deepcopy(metadata))
        self.say("Sending message:", msg.metadata, msg.to)
        await self.behaviour_output.send(deepcopy(msg))
        try:
            self.input_ack.add(msg.metadata["reply-with"])
        except KeyError:
            pass

    class OutputQueue(CyclicBehaviour):
        async def run(self):
            pass

    class Stop(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=1)
            if msg:
                if self.agent.verify(msg):
                    self.agent.say("(StopAgent) Message verified, processing ...")
                    self.agent.say(
                        "(StopAgent) Holon has scheduled us to stop. Stopping!"
                    )

                    metadata = deepcopy(self.agent.inform_msg_template)
                    metadata["status"] = "stopped"
                    await self.agent.schedule_message(
                        self.agent.holon, metadata=metadata
                    )

                    await self.agent.stop()
                else:
                    self.agent.say("Message could not be verified. IMPOSTER!!!!!!")

    class Terminate(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=1)
            if msg:
                if self.agent.verify(msg):
                    await self.agent.stop()
                else:
                    self.agent.say("Message could not be verified. IMPOSTER!!!!!!")
