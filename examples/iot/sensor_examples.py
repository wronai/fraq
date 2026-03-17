#!/usr/bin/env python3
"""IoT examples - UPROSZCZONE z nowym API fraq."""

from __future__ import annotations

import json
from fraq import generate, stream


def example_1_sensors():
    """Generuj sensory - UPROSZCZONE."""
    print("=" * 60)
    print("1. SENSORY (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: generate() z range hints
    records = generate({
        'temperature': 'float:18-30',
        'humidity': 'float:0-100',
        'pressure': 'float:980-1060',
        'battery': 'float:20-100',
        'sensor_id': 'str',
    }, count=15)

    # Grupuj po sensorze
    for sensor_num in range(3):
        sensor_records = records[sensor_num*5:(sensor_num+1)*5]
        print(f"\nSensor_{sensor_num+1:03d}:")
        for r in sensor_records[:2]:
            print(f"  T={r['temperature']}°C, H={r['humidity']}%, B={r['battery']}%")


def example_2_mqtt():
    """MQTT - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("2. MQTT PAYLOADS (UPROSZCZONE)")
    print("=" * 60)

    topics = [
        "factory/sensors/temperature",
        "factory/sensors/humidity",
        "home/living_room/temperature",
    ]

    # UPROSZCZONE: generate()
    records = generate({
        'value': 'float:0-100',
        'unit': 'str',
        'quality': 'float',
    }, count=len(topics))

    for i, topic in enumerate(topics):
        r = records[i]
        payload = {
            "topic": topic,
            "value": round(r['value'], 2),
            "unit": "celsius" if "temp" in topic else "percent",
        }
        print(f"\n  {topic}:")
        print(f"    {json.dumps(payload)[:60]}...")


def example_3_streaming():
    """Streaming - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("3. STREAMING (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: stream() dla leniwego strumieniowania
    print("Streaming 5 records:")
    for i, record in enumerate(stream({
        'temp': 'float:10-40',
        'alert': 'bool',
    }, count=5)):
        print(f"  [{i}] {record}")


if __name__ == "__main__":
    example_1_sensors()
    example_2_mqtt()
    example_3_streaming()
    print("\n" + "=" * 60)
    print("Done! Uproszczone API fraq")
    print("=" * 60)
