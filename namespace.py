#!/usr/bin/env python3

class APiNamespace( dict ):
    '''
    APi namespace class to keep track of various agent, channel,
    environment and holon identifiers.
    '''
    def __init__( self, *args, **kwargs ):
        self[ 'agents' ] = []
        self[ 'channels' ] = []
        self[ 'environment' ] = []
        self[ 'holons' ] = []

    def add_agent ( self, agent ):
        self[ 'agents' ].append( agent )    
        
    def add_channel ( self, channel ):
        self[ 'channels' ].append( channel )    
        
    def add_environment ( self, environment ):
        self[ 'environment' ].append( environment )

    def add_holon( self, name ):
        self[ 'holons' ].append( name )
