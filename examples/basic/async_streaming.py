#!/usr/bin/env python3
"""Async streaming - UPROSZCZONE z nowym API fraq."""

from __future__ import annotations

import asyncio
from fraq import stream, generate, FraqSchema
from fraq.streaming import async_stream


async def example_1_basic():
    """Basic async stream - UPROSZCZONE."""
    print("=" * 60)
    print("1. ASYNC STREAM (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: async_stream już istnieje w bibliotece
    i = 0
    async for record in async_stream(count=5, interval=0.01):
        print(f"  [{i}] depth={record['depth']} value={record['value']:.4f}")
        i += 1


async def example_2_typed():
    """Typed stream - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("2. TYPED STREAM (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: FraqSchema() bez root
    schema = FraqSchema()
    schema.add_field("temperature", "float", transform=lambda v: round(15 + float(v) * 20, 2))
    schema.add_field("sensor_id", "str")
    schema.add_field("alert", "bool")

    # Convert to async
    records = list(schema.records(count=5))
    for i, r in enumerate(records):
        await asyncio.sleep(0.01)
        print(f"  [{i}] {r['sensor_id']}: {r['temperature']}°C alert={r['alert']}")


async def example_3_kafka():
    """Kafka pattern - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("3. KAFKA PATTERN (UPROSZCZONE)")
    print("=" * 60)

    records = generate({
        'user_id': 'str',
        'event': 'str',
        'value': 'float:0-100',
    }, count=5)

    print("Producing to Kafka:")
    for r in records:
        await asyncio.sleep(0.01)
        partition = int(r['user_id'][-1]) % 3
        print(f"  → topic[partition={partition}]: {r['user_id']} {r['event']}")


async def main():
    await example_1_basic()
    await example_2_typed()
    await example_3_kafka()
    print("\n" + "=" * 60)
    print("Done! Async streaming w wersji uproszczonej")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
