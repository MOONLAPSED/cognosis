import asyncio
import websockets

async def websocket_communication(url, data):
    async with websockets.connect(url) as ws:
        await ws.send(json.dumps(data))
        result = await ws.recv()
        return json.loads(result)
