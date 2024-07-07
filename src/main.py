import asyncio
import json

import websockets


async def handler(websocket):
    while True:
        async for message in websocket:
            print(message)
            event = {}
            await websocket.send(json.dumps(event))


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
