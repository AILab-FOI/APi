#!/usr/bin/env python3

from baseagent import *
from registrar import *
from namespace import *

class APiHolon( APiTalkingAgent ):
    '''A holon created by an .api file.'''
    '''TODO: Finish holon implementation'''
    def __init__( self, holonname, name, password, agents, channels, environment, holons, execution_plan ):
        self.token = str( uuid4().hex )
        super().__init__( name, password, str( uuid4().hex ) )
        self.holonname = holonname
        self.address = str( self.jid.bare() )
        self.namespace = APiNamespace()
        self.registrar = APiRegistrationService( holonname )

        self.environment = None
        self.setup_environment( environment )

        self.channels = {}
        for c in channels:
            self.setup_channel( c )

        self.agents = {}
        for a in agents:
            self.setup_agent( a )

        self.holons = {}
        for h in holons:
            self.setup_holon( h )

        self.execution_plan = None
        self.setup_execution( execution_plan )

        self.all_started = False # Indicate if execution plan has been started already
        self.instantiate_all()

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

        self.confirm_message_template = {}
        self.confirm_message_template[ 'performative' ] = 'confirm'
        self.confirm_message_template[ 'ontology' ] = 'APiScheduling'
        self.confirm_message_template[ 'auth-token' ] = self.auth

        

    def setup_agent( self, agent ):
        '''TODO: This method should create and start an agent 
                 depending on type (local Unix, Docker, other 
                 container ...). If it is a container type
                 there should be a possibility to schedule it
                 directly on some orchestration platform (i.e.
                 Kubernetes, Docker Swarm or similar). This should
                 be specified in the agent definition file (.ag).'''
        self.say( 'Registering agent', agent[ 'name' ] )
        address, password = self.registrar.register( agent[ 'name' ] )
        agent[ 'cmd' ] = 'python3 ../agent.py "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % ( agent[ 'name' ], address, password, self.address, self.holonname, self.token, json.dumps( agent[ 'args' ] ).replace('"','\\"'), json.dumps( agent[ 'flows' ] ).replace('"','\\"') )
        agent[ 'address' ] = address
        # TODO: properly handle status change
        agent[ 'status' ] = 'setup'
        self.agents[ agent[ 'name' ] ] = agent

    def setup_channel( self, channel ):
        ''' TODO: Same as above, it should be possible to 
                  create channels in an orchestration platform
                  if specified in the channel definition file.'''
        address, password = self.registrar.register( channel[ 'name' ] )
        self.say( 'Registering channel', channel[ 'name' ] )
        channel[ 'cmd' ] = 'python3 ../channel.py "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % ( channel[ 'name' ], address, password, self.address, self.token, json.dumps( ( self.registrar.min_port, self.registrar.max_port ) ), json.dumps( channel[ 'input' ] ).replace('"','\\"'), json.dumps( channel[ 'output' ] ).replace('"','\\"'), json.dumps( channel[ 'transformer' ] ).replace('"','\\"') )
        channel[ 'address' ] = address
        channel[ 'status' ] = 'setup'
        self.channels[ channel[ 'name' ] ] = channel

    def setup_holon( self, holon ):
        # TODO: implement starting included holons
        pass

    def setup_environment( self, env_spec ):
        # TODO: implement setting up environment
        #       channels (input + output)
        self.say( 'Registering environment' )
        environment = {}
        environment[ 'holon_name' ] = self.holonname
        environment[ 'name' ] = f'{self.holonname}-environment'
        address, password = self.registrar.register( environment[ 'name' ] )
        environment[ 'cmd' ] = 'python3 ../environment.py "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % ( environment[ 'name' ], address, password, self.address, self.token, json.dumps( env_spec ).replace('"','\\"') )
        environment[ 'address' ] = address
        environment[ 'status' ] = 'setup'
        self.environment = environment

    def setup_execution( self, execution_plan ):
        # TODO: Design and implement execution plans
        pass

    def agent_name_from_address( self, address ):
        # Ugly hack
        address = str( address )
        for name, agent in self.agents.items():
            if agent[ 'address' ] == address:
                return name

    def instantiate_all( self ):
        # Create agent and channel instances
        def start( cmd ):
            return sp.Popen( cmd, stderr=sp.STDOUT, start_new_session=True )
            
        for c in self.channels.values():
            cmd = shlex.split( c[ 'cmd' ] )
            print( 'Running channel with:', cmd )
            c[ 'instance' ] = Thread( target=start, args=( cmd, ) )
            c[ 'instance' ].start()
            c[ 'status' ] = 'started'
                
        for a in self.agents.values():
            cmd = shlex.split( a[ 'cmd' ] )
            print( 'Running agent with:', cmd )
            a[ 'instance' ] = Thread( target=start, args=( cmd, ) )
            a[ 'instance' ].start()
            a[ 'status' ] = 'instantiated'

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
                       "status":"ready" }
        )
        self.add_behaviour( bgra, bgra_template )

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
                        if channel == self.agent.environment[ 'holon_name' ]:
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

    class ExecutePlan( CyclicBehaviour ):
        async def run( self ):
            if self.agent.execution_plan:
                # TODO: Design and implement execution plans
                pass
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
                    
                    metadata = deepcopy( self.agent.confirm_message_template )
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]

                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )
                        
                else:
                    self.agent.say( 'Message could not be verified. IMPOSTER!!!!!!' )
                    metadata = deepcopy( self.agent.refuse_message_template )
                    metadata[ 'in-reply-to' ] = msg.metadata[ 'reply-with' ]
                    await self.agent.schedule_message( str( msg.sender ), metadata=metadata )

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
