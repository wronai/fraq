#!/usr/bin/env python3
"""Streaming examples - UPROSZCZONE z nowym API fraq."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime
from fraq import stream, generate


def example_1_sse():
    """SSE - UPROSZCZONE."""
    print("=" * 60)
    print("1. SERVER-SENT EVENTS (UPROSZCZONE)")
    print("=" * 60)

    async def generate_sse(count: int = 3):
        records = generate({
            'temperature': 'float:15-35',
            'humidity': 'float:0-100',
        }, count=count)
        
        for i, r in enumerate(records):
            event = {
                "event": "sensor_reading",
                "data": {**r, "timestamp": datetime.now().isoformat()},
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
    for e in events[:2]:
        print(f"  {e[:70]}...")


def example_2_websocket():
    """WebSocket template."""
    print("\n" + "=" * 60)
    print("2. WEBSOCKET CLIENT (template)")
    print("=" * 60)
    print("""
import websockets
import json
from fraq import stream

async def ws_client():
    async with websockets.connect("ws://localhost:8001/ws") as ws:
        # Stream fractal data via WebSocket
        for record in stream({'temp': 'float', 'humidity': 'float'}, count=100):
            await ws.send(json.dumps(record))
""")


def example_3_streaming():
    """Streaming - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("3. STREAM UTILITY (UPROSZCZONE)")
    print("=" * 60)

    print("Streaming 5 records with interval:")
    for i, record in enumerate(stream({
        'value': 'float:0-100',
        'status': 'bool',
    }, count=5)):
        print(f"  [{i}] value={record['value']:.2f}, status={record['status']}")


def example_4_kafka():
    """Kafka pattern - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("4. KAFKA PATTERN (UPROSZCZONE)")
    print("=" * 60)

    records = generate({
        'user_id': 'str',
        'event_type': 'str',
        'value': 'float:0-100',
    }, count=5)

    print("Producing messages:")
    for r in records:
        partition = int(r['user_id'][-1]) % 3
        print(f"  → user-events[{partition}]: {r['user_id']} - {r['event_type']}")


if __name__ == "__main__":
    example_1_sse()
    example_2_websocket()
    example_3_streaming()
    example_4_kafka()
    print("\n" + "=" * 60)
    print("Done! Uproszczone API fraq")
    print("=" * 60)
