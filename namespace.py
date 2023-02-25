#!/usr/bin/env python3

class APiNamespace( dict ):
    '''
    APi namespace class to keep track of various agent, channel,
    environment and holon identifiers.
    '''
    def __init__( self, *args, **kwargs ):
        self[ 'agents' ] = []
        self[ 'channels' ] = []
        self[ 'environment' ] = {}
        self[ 'execution_plans' ] = []

    def add_agent ( self, agent ):
        self[ 'agents' ].append( agent )    
        
    def add_channel ( self, channel ):
        self[ 'channels' ].append( channel )    
        
    def add_environment ( self, environment ):
        self[ 'environment' ] = environment

    def add_execution_plan( self, plan ):
        self[ 'execution_plans' ].append( plan )
