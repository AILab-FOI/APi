#!/usr/bin/env python3

from baseagent import *
from registrar import *
from namespace import *

from execution_plan import resolve_execution_plan

class APiHolon( APiTalkingAgent ):
    '''A holon created by an .api file.'''
    '''TODO: Finish holon implementation'''
    def __init__( self, holonname, name, password, agents, channels, environment, holons, execution_plans ):
        self.token = str( uuid4().hex )
        super().__init__( name, password, str( uuid4().hex ) )
        self.holonname = holonname
        self.address = str( self.jid.bare() )
        self.namespace = APiNamespace()
        self.registrar = APiRegistrationService( holonname )

        self.environment = None
        if not environment == None:
            self.setup_environment( environment )

        self.channels = {}
        for c in channels:
            self.setup_channel( c )

        self.agent_types = {}
        self.agents = {}
        for a in agents:
            self.create_agent_types_map( a )

        self.holons = {}
        for h in holons:
            self.setup_holon( h )

        self.execution_plans = None
        self.setup_execution( execution_plans )

        self.all_channels_listening = False
        self.all_agents_listening = False

        self.all_started = False # Indicate if execution plan has been started already
        self.start_env_and_channels_all()

        self.query_message_template = {}
        self.query_message_template[ 'performative' ] = 'inform-ref'
        self.query_message_template[ 'ontology' ] = 'APiQuery'
        self.query_message_template[ 'auth-token' ] = self.auth

        self.refuse_message_template = {}
        self.refuse_message_template[ 'performative' ] = 'refuse'
        self.refuse_message_template[ 'ontology' ] = 'APiQuery'
        self.refuse_message_template[ 'auth-token' ] = self.auth
        self.refuse_message_template[ 'reason' ] = 'security-policy'

        self.request_message_template = {}
        self.request_message_template[ 'performative' ] = 'request'
        self.request_message_template[ 'ontology' ] = 'APiScheduling'
        self.request_message_template[ 'auth-token' ] = self.auth
        # Add action in actual behaviour (start or stop)

        # template used for ack
        self.confirm_message_template = {}
        self.confirm_message_template[ 'performative' ] = 'confirm'
        self.confirm_message_template[ 'ontology' ] = 'APiScheduling'
        self.confirm_message_template[ 'auth-token' ] = self.auth

    def create_agent_types_map( self, agent ):
        self.agent_types[ agent[ 'name' ] ] = agent
        
    def adjust_flows_by_args( self, agent_args, agent_params, flows ):
        param_by_arg = {}
        for i in range(0, len(agent_args)):
            arg_name = agent_args[i]
            param_value = agent_params[i]

            param_by_arg[arg_name] = param_value

        adjusted_flows = []
        for source, destination in flows:
            adjusted_flow = (param_by_arg.get(source, source), param_by_arg.get(destination, destination))
            adjusted_flows.append(adjusted_flow)

        return adjusted_flows


    def setup_agent( self, agent_type, id = None, plan_id = None, params = None ):
        if not id:
            id = uuid4().hex
        agent = deepcopy( self.agent_types[ agent_type ] )
        self.say( 'Registering agent', agent[ 'name' ] )
        address, password = self.registrar.register( agent[ 'name' ] )
        if params:
            flows = self.adjust_flows_by_args(agent[ 'args' ], params, agent[ 'flows' ])
        else:
            flows = agent[ 'flows' ]
        agent[ 'cmd' ] = 'python3 ../agent.py "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % ( agent[ 'name' ], address, password, self.address, self.holonname, self.token, json.dumps( flows ).replace('"','\\"') )
        agent[ 'address' ] = address
        agent[ 'status' ] = 'setup'
        agent[ 'id' ] = id
        agent[ 'plan_id' ] = plan_id
        self.agents[ id ] = agent

    def setup_channel( self, channel ):
        address, password = self.registrar.register( channel[ 'name' ] )
        self.say( 'Registering channel', channel[ 'name' ] )
        channel[ 'cmd' ] = 'python3 ../channel.py "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % ( channel[ 'name' ], address, password, self.address, self.token, json.dumps( ( self.registrar.min_port, self.registrar.max_port ) ), channel[ 'protocol' ], json.dumps( channel[ 'input' ] ).replace('"','\\"'), json.dumps( channel[ 'output' ] ).replace('"','\\"') )
        channel[ 'address' ] = address
        channel[ 'status' ] = 'setup'
        self.channels[ channel[ 'name' ] ] = channel

    def setup_holon( self, holon ):
        # TODO: implement starting included holons
        pass

    def setup_environment( self, env ):
        environment = {}
        environment[ 'name' ] = f'{self.holonname}-environment'
        address, password = self.registrar.register( environment[ 'name' ] )
        environment[ 'cmd' ] = 'python3 ../environment.py "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % ( environment[ 'name' ], address, password, self.address, self.token, json.dumps( ( self.registrar.min_port, self.registrar.max_port ) ), 'tcp', json.dumps( env[ 'input' ] ).replace('"','\\"'), json.dumps( env[ 'output' ] ).replace('"','\\"') )
        environment[ 'address' ] = address
        environment[ 'status' ] = 'setup'
        self.environment = environment

    def setup_execution( self, execution_plans ):
        if execution_plans is None:
            return

        resolved_execution_plans = [resolve_execution_plan(plan) for plan in execution_plans]
        self.execution_plans = resolved_execution_plans

    def agent_name_from_address( self, address ):
        # Ugly hack
        address = str( address )
        for name, agent in self.agents.items():
            if agent[ 'address' ] == address:
                return name

    def channel_name_from_address( self, address ):
        # Ugly hack
        address = str( address )
        for name, channel in self.channels.items():
            if channel[ 'address' ] == address:
                return name

    def start_basic_agent_thread( self, cmd ):
        return sp.Popen( cmd, stderr=sp.STDOUT, start_new_session=True )

    def agent_finished( self, a_id, plan_id, status ):
        print("finished", a_id, plan_id, status)
        print("finished", a_id, plan_id, status)
        print("finished", a_id, plan_id, status)
        print("finished", a_id, plan_id, status)
        pass

    def start_dependant_agent_thread( self, a_id, plan_id, cmd ):
        proc = sp.Popen( cmd, start_new_session=True )
        proc.communicate()
        return_code = proc.returncode

        self.agent_finished(a_id, plan_id, return_code)

    def start_env_and_channels_all( self ):
        if not self.environment == None:
            cmd = shlex.split( self.environment[ 'cmd' ] )
            self.say('Running environment:', self.environment.get('name'))
            self.environment[ 'instance' ] = Thread( target=self.start_basic_agent_thread, args=( cmd, ) )
            self.environment[ 'instance' ].start()
            self.environment[ 'status' ] = 'started'

        for c in self.channels.values():
            cmd = shlex.split( c[ 'cmd' ] )
            self.say( 'Running channel:', c.get('name') )
            c[ 'instance' ] = Thread( target=self.start_basic_agent_thread, args=( cmd, ) )
            c[ 'instance' ].start()
            c[ 'status' ] = 'started'
                
    def setup_agents( self ):
        if not self.execution_plans == None:
            for execution_plan in self.execution_plans:
                plan = execution_plan[ 'plan' ]
                plan_id = execution_plan['id']
                agent_ids = [a_id for a_id in plan.keys()]
                for a_id in agent_ids:
                    a_ref = plan[ a_id ]
                    a_type = a_ref[ 'name' ]
                    a_args = a_ref.get('args', None)
                    self.setup_agent( a_type, a_id, plan_id, a_args )
        else:            
            for a_type in self.agent_types.keys():                
                self.setup_agent( a_type )

    def start_initial_agents( self ):
        def run( a, start_type ):
            cmd = shlex.split( a[ 'cmd' ] )
            a_id = a[ 'id' ]
            plan_id = a[ 'plan_id' ]
            self.say( 'Running agent:', a.get('name') )
            if start_type == "dependant":
                a[ 'instance' ] = Thread( target=self.start_dependant_agent_thread, args=( a_id, plan_id, cmd ) )
            else:
                a[ 'instance' ] = Thread( target=self.start_basic_agent_thread, args=( cmd, ) )
            a[ 'instance' ].start()
            a[ 'status' ] = 'started'

        if not self.execution_plans == None:
            for execution_plan in self.execution_plans:
                i_agent_ids = execution_plan[ 'initial_agents_to_run' ]
                for a in self.agents.values():
                    if a[ 'id' ] in i_agent_ids:
                        run( a, 'dependant' )
        else:
            for a in self.agents.values():
                run( a, 'basic' )

    async def stop( self ):
        self.say( '(Stop Agents) Stopping all agents & channels!' )
        metadata = deepcopy( self.request_message_template )
        metadata[ 'action' ] = 'stop'
        for c in self.channels.values():
            await self.schedule_message( c[ 'address' ], metadata=metadata )
        for a in self.agents.values():
            await self.schedule_message( a[ 'address' ], metadata=metadata )

    async def setup( self ):
        super().setup()

        bqn = self.QueryName()
        bqn_template =  Template(
            metadata={ "performative": "query-ref",
                       "ontology": "APiQuery"
            }
        )
        self.add_behaviour( bqn, bqn_template )

        bgra = self.GetReadyAgents()
        bgra_template = Template(
            metadata={ "performative": "inform",
                       "ontology": "APiScheduling",
                       "type": "agent",
                       "status":"ready" }
        )
        self.add_behaviour( bgra, bgra_template )

        bgla = self.GetListeningAgents()
        bgla_template = Template(
            metadata={ "performative": "inform",
                       "ontology": "APiScheduling",
                       "status":"listening" }
        )
        self.add_behaviour( bgla, bgla_template )

        bcl = self.AllChannelsListening()
        self.add_behaviour( bcl )

        bep = self.ExecutePlan()
        self.add_behaviour( bep )

        bfa = self.FinishedAgents()
        bfa_template = Template(
            metadata={ "performative": "inform",
                       "ontology": "APiScheduling",
                       "status":"finished" }
        )
        self.add_behaviour( bfa, bfa_template )

        bsa = self.StopAgents()
        bsa_template = Template( metadata={ "performative": "inform", "ontology": "APiScheduling", "status": "stopped" } )
        self.add_behaviour( bsa, bsa_template )
        
        self.say( self.channels )
        self.say( self.agents )

    class QueryName( CyclicBehaviour ):
        async def run( self ):
            msg = await self.receive( timeout=0.1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(QueryName) Message verified, processing ...' )
                    channel = msg.metadata[ 'channel' ]                    
                    metadata = deepcopy( self.agent.query_message_template )
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    metadata[ 'agent' ] = channel

                    try:
                        if self.agent.environment and channel == self.agent.environment[ 'holon_name' ]:
                            address = self.agent.environment[ 'address' ]
                        else:                            
                            address = self.agent.channels[ channel ][ 'address' ]
                        self.agent.say( 'Found channel', channel, 'address is', address )

                        metadata[ 'success' ] = 'true'
                        metadata[ 'address' ] = address
                    except KeyError:
                        self.agent.say( 'Channel', channel, 'not found' )
                        metadata[ 'success' ] = 'false'
                        metadata[ 'address' ] = 'null'
                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )
                        
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )
                    metadata = deepcopy( self.agent.refuse_message_template )
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )

    """
    Behaviour that listens to XMPP mesage that is sent from an agent when it is ready setting up.
    Agent will communicate their status over XMPP.

    Ontology: APiScheduling
    Status: finished
    """
    class GetReadyAgents( CyclicBehaviour ):
        async def run( self ):
            msg = await self.receive( timeout=0.1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(QueryNameGetReadyAgents) Message verified, processing ...' )
                    agent = self.agent.agent_name_from_address( msg.sender.bare() )
                    self.agent.say( '(QueryNameGetReadyAgents) Setting agent', agent, 'status to ready.' )
                    self.agent.agents[ agent ][ 'status' ] = 'ready'
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )
                    metadata = deepcopy( self.agent.refuse_message_template )
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )

    class GetListeningAgents( CyclicBehaviour ):
        async def run( self ):
            msg = await self.receive( timeout=0.1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(GetListeningAgents) Message verified, processing ...' )
                    type = msg.metadata[ 'type' ]
                    if type == 'channel':
                        channel = self.agent.channel_name_from_address( msg.sender.bare() )
                        self.agent.say( '(QueryNameGetReadyChannel) Setting channel', channel, 'status to listening.' )
                        self.agent.channels[ channel ][ 'status' ] = 'listening'

                        all_ready = True
                        for channel in self.agent.channels.values():
                            if channel[ 'status' ] != 'listening':
                                all_ready = False
                                
                        if all_ready:
                            self.agent.all_channels_listening = True
                    elif type == 'agent':
                        agent = self.agent.agent_name_from_address( msg.sender.bare() )
                        self.agent.say( '(QueryNameGetReadyAgents) Setting agent', agent, 'status to ready.' )
                        self.agent.agents[ agent ][ 'status' ] = 'listening'

                        all_ready = True
                        for agent in self.agent.agents.values():
                            if agent[ 'status' ] != 'ready' and agent[ 'status' ] != 'listening':
                                all_ready = False
                                break

                            if all_ready:
                                self.agent.all_agents_listening = True
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )
                    metadata = deepcopy( self.agent.refuse_message_template )
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )

    class AllChannelsListening( OneShotBehaviour ):
        async def run( self ):
            while (not self.agent.all_channels_listening):
                await asyncio.sleep( 1 )

            self.agent.setup_agents()
            self.agent.start_initial_agents()

    class ExecutePlan( CyclicBehaviour ):
        async def run( self ):
            # wait until we have some agents running
            if len(self.agent.agents.values()) == 0:
                return

            if not self.agent.execution_plans is None:
                for plan in self.agent.execution_plans:
                    if plan[ 'started' ]:
                        continue

                    i_agent_ids = plan[ 'initial_agents_to_run' ]

                    all_ready = True
                    for agent in self.agent.agents.values():
                        if agent[ 'id' ] in i_agent_ids and agent[ 'status' ] != 'ready':
                            all_ready = False
                            
                    if all_ready:
                        self.agent.say( '(Execute plan) All agents ready, scheduling them for start!' )
                        metadata = deepcopy( self.agent.request_message_template )
                        metadata[ 'action' ] = 'start'
                        for agent in self.agent.agents.values():
                            if agent[ 'id' ] in i_agent_ids:
                                await self.agent.schedule_message( agent[ 'address' ], metadata=metadata )
                        plan[ 'started' ] = True
                
            else:
                # Tell all agents to start if they are ready
                all_ready = True
                for agent in self.agent.agents.values():
                    if agent[ 'status' ] != 'ready':
                        all_ready = False
                        break
                if all_ready and not self.agent.all_started:
                    self.agent.say( '(Execute plan) All agents ready, scheduling them for start!' )
                    metadata = deepcopy( self.agent.request_message_template )
                    metadata[ 'action' ] = 'start'
                    for agent in self.agent.agents.values():
                        await self.agent.schedule_message( agent[ 'address' ], metadata=metadata )
                    self.agent.all_started = True

    """
    Behaviour that listens to XMPP mesage that is sent from an agent when it is finished setting up.
    Agent will communicate their status over XMPP. Deleberatelly stopped & finished agents share the same status.

    Ontology: APiScheduling
    Status: finished
    """
    class FinishedAgents( CyclicBehaviour ):
        async def run( self ):
            msg = await self.receive( timeout=0.1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(FinishedAgents) Message verified, processing ...' )
                    agent = self.agent.agent_name_from_address( msg.sender.bare() )

                    if msg.metadata[ 'error-message' ] != 'null':
                        self.agent.say( 'Agent', agent, 'finished with error', str( msg[ 'error-message' ] ) )
                    else:
                        self.agent.say( 'Agent', agent, 'finished gracefully.' )
                    self.agent.agents[ agent ][ 'status' ] = 'stopped'
                    
                    # sending message to ack that agent has stopped, so they can terminate
                    metadata = deepcopy( self.agent.confirm_message_template )
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]

                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )
                        
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )
                    metadata = deepcopy( self.agent.refuse_message_template )
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )

    """
    Behaviour that listens to XMPP mesage that is sent from an agent when it is finished setting up.
    Agent will communicate their status over XMPP. Deleberatelly stopped & finished agents share the same status.

    Ontology: APiScheduling
    Status: finished
    """
    class StopAgents( CyclicBehaviour ):
        def all_stopped( self, agents ):
            if any( a[ 'status' ] != 'stopped' for a in agents ):
                return False

            return True

        async def run( self ):
            msg = await self.receive( timeout=0.1 )
            if msg:
                if self.agent.verify( msg ):
                    self.agent.say( '(StopAgents) Message verified, processing ...' )
                    agent = self.agent.agent_name_from_address( msg.sender.bare() )

                    if msg.metadata[ 'error-message' ] != 'null':
                        self.agent.say( 'Agent', agent, 'stopped with error', str( msg[ 'error-message' ] ) )
                    else:
                        self.agent.say( 'Agent', agent, 'stopped gracefully.' )
                    self.agent.agents[ agent ][ 'status' ] = 'stopped'

                    all_stopped = self.all_stopped( [ *self.agent.agents.values(), *self.agent.channels.values() ] )

                    if all_stopped:
                        self.agent.say( '(StopAgents) All agents have stopped ...' )
                        self.agent.say( '(StopAgents) Holon stopping ...' )

                        super().stop()

                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )
                    metadata = deepcopy( self.agent.refuse_message_template )
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )
