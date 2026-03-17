"""
WebSocket server for docker-compose
"""
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from fraq import FileSearchAdapter, FraqNode
from fraq.generators import HashGenerator

app = FastAPI(title="fraq WebSocket")


@app.websocket("/ws/stream")
async def ws_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_json()
            if msg.get("action") == "stream":
                count = msg.get("count", 10)
                root = FraqNode(position=(0.0, 0.0, 0.0), generator=HashGenerator())
                cursor = root.cursor()
                for i in range(count):
                    cursor.advance()
                    await websocket.send_json({"index": i, "value": cursor.current.value})
                    await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass


@app.websocket("/ws/files")
async def ws_files(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_json()
            if msg.get("action") == "search":
                path = msg.get("path", "/data")
                ext = msg.get("ext")
                limit = msg.get("limit", 10)
                adapter = FileSearchAdapter(base_path=path, recursive=True)
                for record in adapter.stream(extension=ext, count=limit):
                    await websocket.send_json(record)
                    await asyncio.sleep(0.01)
                await websocket.send_json({"done": True})
    except WebSocketDisconnect:
        pass


@app.get("/health")
def health():
    return {"status": "ok"}
