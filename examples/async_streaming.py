#!/usr/bin/env python3
"""
fraq — Async streaming examples.

Nieskończone streamy z asyncio — dla FastAPI SSE, Kafka, NATS, WebSocket.
"""

import asyncio
from fraq import FraqNode, FraqSchema
from fraq.streaming import AsyncFraqStream, async_query, async_stream
from fraq.query import FraqQuery


async def example_basic_stream():
    """Prosty async stream — 10 rekordów."""
    print("=== Async: Basic stream ===")
    i = 0
    async for record in async_stream(count=10, interval=0.01, dims=2):
        print(f"  [{i}] depth={record['depth']} value={record['value']:.6f}")
        i += 1
    print()


async def example_typed_stream():
    """Stream z typowanym schematem."""
    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("temperature", "float")
    schema.add_field("sensor_id", "str")
    schema.add_field("alert", "bool")

    stream = AsyncFraqStream(root=root, interval=0.01, schema=schema)

    print("=== Async: Typed sensor stream ===")
    i = 0
    async for record in stream:
        alert_mark = " ⚠" if record["alert"] else ""
        print(f"  [{i}] temp={record['temperature']:.6f} "
              f"id={record['sensor_id']}{alert_mark}")
        i += 1
        if i >= 8:
            stream.stop()
            break
    print()


async def example_async_query():
    """Async query — offloaded do thread pool."""
    q = FraqQuery().zoom(2).select("x:float", "y:int").output("records").take(5)
    results = await async_query(q, dims=2)
    print("=== Async: Query results ===")
    for r in results:
        print(f"  x={r['x']:.6f} y={r['y']}")
    print()


async def example_fastapi_sse_pattern():
    """
    Wzorzec dla FastAPI SSE endpoint:

        @app.get("/stream/sensors")
        async def sensor_sse():
            async def generate():
                async for record in async_stream(count=100, interval=0.1):
                    yield f"data: {json.dumps(record)}\\n\\n"
            return StreamingResponse(generate(), media_type="text/event-stream")
    """
    print("=== Async: FastAPI SSE pattern (5 events) ===")
    import json
    async for record in async_stream(count=5, interval=0.01, dims=3):
        # W FastAPI to byłoby yield do StreamingResponse
        event = f"data: {json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in record.items()})}"
        print(f"  {event}")
    print()


async def example_kafka_producer_pattern():
    """
    Wzorzec dla Kafka / NATS producer:

        producer = aiokafka.AIOKafkaProducer(...)
        async for record in async_stream(count=1000, interval=0.1):
            await producer.send("fraq.sensors", json.dumps(record).encode())
    """
    print("=== Async: Kafka producer pattern (5 messages) ===")
    import json
    topic = "fraq.sensors"
    async for record in async_stream(count=5, interval=0.01, dims=3):
        payload = json.dumps(record, default=str)
        print(f"  → {topic}: {payload[:80]}...")
    print()


async def main():
    await example_basic_stream()
    await example_typed_stream()
    await example_async_query()
    await example_fastapi_sse_pattern()
    await example_kafka_producer_pattern()


if __name__ == "__main__":
    asyncio.run(main())
