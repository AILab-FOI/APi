#!/usr/bin/env python3

import logging
logging.getLogger( 'asyncio' ).setLevel( logging.CRITICAL )

# Only for debug
DEBUG = False
TALK = True

if DEBUG:
    logging.basicConfig( level=logging.DEBUG )

    from aiodebug import log_slow_callbacks, monitor_loop_lag
    log_slow_callbacks.enable( 0.05 )
