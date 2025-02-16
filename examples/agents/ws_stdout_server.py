#!/usr/bin/env python3
import asyncio
import websockets
import sys


async def writeout(websocket, path):
    msg = await websocket.recv()
    print(msg, file=sys.stdout)
    await websocket.send(msg)
    if msg == "<!eof!>":
        sys.exit()


try:
    stdout_server = websockets.serve(writeout, "localhost", 3618)

    asyncio.get_event_loop().run_until_complete(stdout_server)
    asyncio.get_event_loop().run_forever()
except Exception as e:
    print("err", e)
