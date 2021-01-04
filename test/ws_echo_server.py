#!/usr/bin/env python3
import asyncio
import websockets

async def echo( websocket, path ):
    msg = await websocket.recv()
    await websocket.send( msg )

    
echo_server = websockets.serve( echo, "localhost", 3618 )

asyncio.get_event_loop().run_until_complete( echo_server )
asyncio.get_event_loop().run_forever()
