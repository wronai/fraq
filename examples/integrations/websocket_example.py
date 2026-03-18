"""
WebSocket integration example for fraq.

Run: python websocket_example.py
"""

from __future__ import annotations

import asyncio
import json
import websockets

from fraq import stream


async def fraq_websocket_handler(websocket, path):
    """Handle WebSocket connections and stream fraq data."""
    try:
        async for message in websocket:
            data = json.loads(message)
            command = data.get("command")
            
            if command == "generate":
                fields = data.get("fields", {"value": "float"})
                count = data.get("count", 10)
                
                # Stream records
                for record in stream(fields, count=count):
                    await websocket.send(json.dumps({
                        "type": "record",
                        "data": record
                    }))
                
                await websocket.send(json.dumps({
                    "type": "complete",
                    "count": count
                }))
            
            elif command == "ping":
                await websocket.send(json.dumps({"type": "pong"}))
            
            else:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": f"Unknown command: {command}"
                }))
    
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")


async def main():
    """Start WebSocket server."""
    server = await websockets.serve(
        fraq_websocket_handler,
        "localhost",
        8765
    )
    print("WebSocket server running on ws://localhost:8765")
    await server.wait_closed()


async def test_client():
    """Test client for WebSocket server."""
    uri = "ws://localhost:8765"
    
    async with websockets.connect(uri) as websocket:
        # Send generate command
        await websocket.send(json.dumps({
            "command": "generate",
            "fields": {"temperature": "float:0-100"},
            "count": 5
        }))
        
        # Receive records
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            
            if data["type"] == "complete":
                print(f"Received {data['count']} records")
                break
            elif data["type"] == "record":
                print(f"Record: {data['data']}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "client":
        asyncio.run(test_client())
    else:
        asyncio.run(main())
