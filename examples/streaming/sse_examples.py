#!/usr/bin/env python3
"""
Streaming examples - real-time data with fraq.

Shows how to:
1. Server-Sent Events (SSE) endpoint
2. WebSocket streaming
3. Kafka-style streaming
4. Async generators

Run:
    pip install fraq fastapi uvicorn websockets
    python streaming/sse_server.py
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime
from typing import AsyncIterator

from fraq import FraqSchema, query
from fraq.streaming import async_stream


def example_1_sse_generator():
    """Generate SSE-formatted events."""
    print("=" * 60)
    print("1. SERVER-SENT EVENTS (SSE)")
    print("=" * 60)

    async def generate_sensor_sse(count: int = 5) -> AsyncIterator[str]:
        """Generate SSE events with sensor data."""
        schema = FraqSchema()
        schema.add_field("temperature", "float", transform=lambda v: round(15 + v * 20, 2))
        schema.add_field("humidity", "float", transform=lambda v: round(v * 100, 2))
        schema.add_field("sensor_id", "str", transform=lambda v: f"S{int(v * 100):03d}")

        for i, record in enumerate(schema.records(depth=2)):
            if i >= count:
                break
            event = {
                "event": "sensor_reading",
                "data": {
                    **record,
                    "timestamp": datetime.now().isoformat(),
                },
                "id": i,
            }
            yield f"data: {json.dumps(event)}\n\n"
            await asyncio.sleep(0.1)  # Simulate streaming delay

    # Run async generator
    async def run():
        events = []
        async for event in generate_sensor_sse(3):
            events.append(event.strip())
        return events

    events = asyncio.run(run())

    print("Generated SSE events:")
    for event in events:
        print(f"  {event[:80]}...")


def example_2_websocket_client():
    """WebSocket client example (code template)."""
    print("\n" + "=" * 60)
    print("2. WEBSOCKET CLIENT (template)")
    print("=" * 60)

    code = '''
import websockets
import json
from fraq import query

async def websocket_client():
    uri = "ws://localhost:8001/ws"
    async with websockets.connect(uri) as ws:
        # Subscribe to sensor stream
        await ws.send(json.dumps({
            "action": "subscribe",
            "channel": "sensors",
            "params": {"count": 100}
        }))

        async for message in ws:
            data = json.loads(message)
            print(f"Received: {data}")
'''
    print(code)


def example_3_kafka_pattern():
    """Simulate Kafka producer pattern."""
    print("\n" + "=" * 60)
    print("3. KAFKA-STYLE STREAMING")
    print("=" * 60)

    async def kafka_producer(topic: str, count: int = 5):
        """Simulate producing to Kafka topic."""
        schema = FraqSchema()
        schema.add_field("user_id", "str", transform=lambda v: f"user_{int(v * 10000):05d}")
        schema.add_field("event_type", "str", transform=lambda v: "click" if v < 0.5 else "purchase")
        schema.add_field("value", "float", transform=lambda v: round(v * 100, 2))

        messages = []
        for i, record in enumerate(schema.records(depth=2)):
            if i >= count:
                break
            message = {
                "topic": topic,
                "key": record["user_id"],
                "value": {
                    **record,
                    "timestamp": datetime.now().isoformat(),
                },
                "partition": int(record["user_id"][-1]) % 3,  # 3 partitions
            }
            messages.append(message)
            print(f"  → {topic}[{message['partition']}]: {record['user_id']} - {record['event_type']}")

        return messages

    messages = asyncio.run(kafka_producer("user-events", 5))
    print(f"\nProduced {len(messages)} messages to 'user-events'")


def example_4_async_stream():
    """Use fraq async_stream utility."""
    print("\n" + "=" * 60)
    print("4. ASYNC STREAM UTILITY")
    print("=" * 60)

    async def stream_with_backpressure():
        """Stream with rate limiting."""
        records = []
        async for record in async_stream(count=5, interval=0.05):
            records.append(record)
            if len(records) >= 5:
                break
        return records

    records = asyncio.run(stream_with_backpressure())

    print(f"Streamed {len(records)} records with backpressure:")
    for r in records[:3]:
        print(f"  depth={r.get('depth', 'N/A')}, value={r.get('value', 'N/A'):.4f}")


def example_5_fastapi_sse_endpoint():
    """FastAPI SSE endpoint (code template)."""
    print("\n" + "=" * 60)
    print("5. FASTAPI SSE ENDPOINT (template)")
    print("=" * 60)

    code = '''
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fraq import FraqSchema, async_stream
import json
import asyncio

app = FastAPI()

@app.get("/stream/sensors")
async def stream_sensors():
    """Stream sensor data as SSE."""
    schema = FraqSchema()
    schema.add_field("temp", "float")
    schema.add_field("humidity", "float")

    async def event_generator():
        async for record in async_stream(count=100, interval=0.1):
            yield f"data: {json.dumps(record)}\\n\\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
'''
    print(code)


if __name__ == "__main__":
    example_1_sse_generator()
    example_2_websocket_client()
    example_3_kafka_pattern()
    example_4_async_stream()
    example_5_fastapi_sse_endpoint()

    print("\n" + "=" * 60)
    print("Done! See streaming/sse_examples.py")
    print("=" * 60)
