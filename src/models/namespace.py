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

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_channel(self, channel):
        self.channels.append(channel)

    def add_environment(self, environment):
        self.environment = environment

    def add_execution_plan(self, plan):
        self.execution_plans.append(plan)

    def add_holon(self, holon):
        self.holons.append(holon)
