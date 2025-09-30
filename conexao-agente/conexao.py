from fastapi import FastAPI, Request
import asyncio
import websockets
import json
import uvicorn

app = FastAPI()
WS_URL = "ws://localhost:8765"

ws_connection = None
ws_lock = asyncio.Lock()

async def get_ws_connection():
    global ws_connection
    if ws_connection is None or ws_connection.closed:
        ws_connection = await websockets.connect(WS_URL)
    return ws_connection

@app.post("/send_message")
async def send_message(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    async with ws_lock:
        ws = await get_ws_connection()
        await ws.send(json.dumps({"message": user_message}))
        response = await ws.recv()
        return json.loads(response)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
