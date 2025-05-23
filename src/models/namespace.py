from typing import Dict


class APiNamespace:
    """
    APi namespace class to keep track of various agent, channel,
    environment and holon identifiers.
    """

    def __init__(self):
        self.agents = []
        self.channels = []
        self.environment = None
        self.execution_plans = []
        self.holons = []

    def add_agent(self, agent: Dict) -> None:
        """
        Add an agent to the namespace.
        """

        self.agents.append(agent)

    def add_channel(self, channel: Dict) -> None:
        """
        Add a channel to the namespace.
        """

        self.channels.append(channel)

    def add_environment(self, environment: Dict) -> None:
        """
        Add an environment to the namespace.
        """

        self.environment = environment

    def add_execution_plan(self, plan: Dict) -> None:
        """
        Add an execution plan to the namespace.
        """

        self.execution_plans.append(plan)

    def add_holon(self, holon: Dict) -> None:
        """
        Add a holon to the namespace.
        """

        self.holons.append(holon)
