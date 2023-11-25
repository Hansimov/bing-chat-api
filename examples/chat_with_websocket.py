import asyncio
import websockets


async def chat_with_websocket(url, message):
    async with websockets.connect(url) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(response)


server = "localhost"
port = 22222
ws_url = f"ws://{server}:{port}/create"

prompt = "Hello, who are you?"
event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(chat_with_websocket(ws_url, prompt))
event_loop.close()
