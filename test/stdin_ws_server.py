#!/usr/bin/env python3
import asyncio
import websockets
import fileinput

acc = []

async def echo_stdin( websocket, path ):
    global acc
    for i in acc:
        await websocket.send( i )

for line in fileinput.input():
    acc.append( line )
    
echo_server = websockets.serve( echo_stdin, "localhost", 3618 )

asyncio.get_event_loop().run_until_complete( echo_server )
asyncio.get_event_loop().run_forever()
