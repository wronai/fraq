"""
WebSocket + fraq Docker example
Real-time streaming of fractal data and file search
"""

import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from fraq import FileSearchAdapter, FraqNode
from fraq.generators import HashGenerator

app = FastAPI(title="fraq WebSocket Docker", version="0.2.2")


@app.websocket("/ws/stream")
async def ws_stream(websocket: WebSocket):
    """Stream fractal data"""
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_json()
            action = msg.get("action")
            
            if action == "stream":
                count = msg.get("count", 10)
                interval = msg.get("interval", 0.1)
                
                # Generate fractal stream
                root = FraqNode(position=(0.0, 0.0, 0.0), generator=HashGenerator())
                cursor = root.cursor()
                
                for i in range(count):
                    cursor.advance()
                    await websocket.send_json({
                        "index": i,
                        "value": cursor.current.value,
                        "position": cursor.current.position,
                    })
                    await asyncio.sleep(interval)
                    
            elif action == "ping":
                await websocket.send_json({"pong": True, "timestamp": asyncio.get_event_loop().time()})
                
    except WebSocketDisconnect:
        print("Client disconnected from /ws/stream")


@app.websocket("/ws/files")
async def ws_files(websocket: WebSocket):
    """Stream file search results"""
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_json()
            action = msg.get("action")
            
            if action == "search":
                path = msg.get("path", "/data")
                ext = msg.get("ext")
                pattern = msg.get("pattern")
                limit = msg.get("limit", 10)
                
                adapter = FileSearchAdapter(base_path=path, recursive=True)
                
                # Stream results one by one
                count = 0
                for record in adapter.stream(extension=ext, pattern=pattern, count=limit):
                    await websocket.send_json(record)
                    count += 1
                    await asyncio.sleep(0.01)
                
                await websocket.send_json({"done": True, "count": count})
                
            elif action == "stat":
                from pathlib import Path
                from datetime import datetime
                
                file_path = msg.get("file")
                path = Path(file_path)
                
                if path.exists():
                    stat = path.stat()
                    await websocket.send_json({
                        "file": str(path),
                        "size": stat.st_size,
                        "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "fraq_seed": hash(str(path)) % (2**32),
                    })
                else:
                    await websocket.send_json({"error": "File not found"})
                    
    except WebSocketDisconnect:
        print("Client disconnected from /ws/files")


@app.get("/health")
def health():
    return {"status": "ok", "websocket": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
