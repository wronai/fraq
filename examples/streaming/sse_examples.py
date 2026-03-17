#!/usr/bin/env python3
"""Streaming examples - real-time data with fraq."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime
from typing import AsyncIterator

from fraq import FraqSchema, FraqNode
from fraq.streaming import async_stream


def example_1_sse_generator():
    """Generate SSE-formatted events."""
    print("=" * 60)
    print("1. SERVER-SENT EVENTS (SSE)")
    print("=" * 60)

    async def generate_sse(count: int = 3) -> AsyncIterator[str]:
        root = FraqNode(position=(0.0, 0.0, 0.0))
        schema = FraqSchema(root=root)
        schema.add_field("temperature", "float", transform=lambda v: round(15 + float(v) * 20, 2))
        schema.add_field("humidity", "float", transform=lambda v: round(float(v) * 100, 2))

        for i, record in enumerate(schema.records(depth=2)):
            if i >= count:
                break
            event = {
                "event": "sensor_reading",
                "data": {**record, "timestamp": datetime.now().isoformat()},
                "id": i,
            }
            yield f"data: {json.dumps(event)}\n\n"
            await asyncio.sleep(0.01)

    async def run():
        events = []
        async for event in generate_sse(3):
            events.append(event.strip())
        return events

    events = asyncio.run(run())
    print(f"Generated {len(events)} SSE events:")
    for event in events[:2]:
        print(f"  {event[:80]}...")


def example_2_websocket_template():
    """WebSocket client example template."""
    print("\n" + "=" * 60)
    print("2. WEBSOCKET CLIENT (template)")
    print("=" * 60)
    print("""
import websockets
import json

async def websocket_client():
    uri = "ws://localhost:8001/ws"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"action": "subscribe", "count": 100}))
        async for message in ws:
            data = json.loads(message)
            print(f"Received: {data}")
""")


def example_3_async_stream():
    """Use fraq async_stream utility."""
    print("\n" + "=" * 60)
    print("3. ASYNC STREAM UTILITY")
    print("=" * 60)

    async def stream_data():
        records = []
        async for record in async_stream(count=5, interval=0.01):
            records.append(record)
            if len(records) >= 5:
                break
        return records

    records = asyncio.run(stream_data())
    print(f"Streamed {len(records)} records")
    for r in records[:2]:
        print(f"  depth={r.get('depth', 'N/A')}, value={r.get('value', 0):.4f}")


if __name__ == "__main__":
    example_1_sse_generator()
    example_2_websocket_template()
    example_3_async_stream()
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
