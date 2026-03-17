#!/usr/bin/env python3
"""IoT examples - sensor data and MQTT with fraq."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

from fraq import FraqSchema, FraqNode


def example_1_sensor_readings():
    """Generate realistic IoT sensor readings."""
    print("=" * 60)
    print("1. REALISTIC SENSOR READINGS")
    print("=" * 60)

    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("temperature", "float", transform=lambda v: round(18 + float(v) * 12, 2))
    schema.add_field("humidity", "float", transform=lambda v: round(float(v) * 100, 2))
    schema.add_field("pressure", "float", transform=lambda v: round(980 + float(v) * 80, 2))
    schema.add_field("battery", "float", transform=lambda v: round(20 + float(v) * 80, 2))

    sensors = []
    base_time = datetime.now()

    for sensor_id in ["sensor_001", "sensor_002", "sensor_003"]:
        readings = []
        for i, record in enumerate(schema.records(depth=2, branching=4)):
            if i >= 3:
                break
            readings.append({
                "sensor_id": sensor_id,
                "timestamp": (base_time + timedelta(minutes=i*10)).isoformat(),
                **record,
            })
        sensors.append({"sensor_id": sensor_id, "readings": readings})

    print(f"Generated data for {len(sensors)} sensors")
    for sensor in sensors:
        print(f"\n{sensor['sensor_id']}:")
        for r in sensor['readings'][:2]:
            print(f"  {r['timestamp'][11:19]}: T={r['temperature']}°C, H={r['humidity']}%, B={r['battery']}%")


def example_2_mqtt_payloads():
    """Generate MQTT-compatible message payloads."""
    print("\n" + "=" * 60)
    print("2. MQTT MESSAGE PAYLOADS")
    print("=" * 60)

    topics = [
        "factory/sensors/temperature/zone_1",
        "factory/sensors/humidity/zone_1",
        "home/living_room/temperature",
    ]

    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("value", "float")
    schema.add_field("unit", "float", transform=lambda v: "celsius" if float(v) < 0.33 else "percent")
    schema.add_field("quality", "float", transform=lambda v: "good" if float(v) > 0.8 else "fair")

    messages = []
    for topic in topics:
        for record in schema.records(depth=1, branching=1):
            payload = {
                "topic": topic,
                "value": round(record["value"] * 100, 2),
                "unit": record["unit"],
                "quality": record["quality"],
            }
            messages.append(payload)
            break

    print(f"Generated {len(messages)} MQTT messages")
    for msg in messages[:2]:
        print(f"\n  Topic: {msg['topic']}")
        print(f"  Payload: {json.dumps(msg, indent=2)[:100]}...")


def example_3_device_health():
    """Simulate IoT device registry with health status."""
    print("\n" + "=" * 60)
    print("3. DEVICE HEALTH MONITORING")
    print("=" * 60)

    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("device_id", "float", transform=lambda v: f"DEV-{int(float(v)*10000):06d}")
    schema.add_field("battery_level", "float", transform=lambda v: round(float(v) * 100, 1))
    schema.add_field("signal_strength", "float", transform=lambda v: round(-120 + float(v) * 80, 1))

    def health_status(v):
        battery = float(v) * 100
        signal = -120 + float(v) * 80
        if battery > 50 and signal > -80:
            return "healthy"
        elif battery > 20:
            return "degraded"
        else:
            return "critical"

    schema.add_field("status", "float", transform=health_status)

    devices = []
    for i, record in enumerate(schema.records(depth=2, branching=10)):
        if i >= 20:
            break
        devices.append(record)

    healthy = [d for d in devices if d["status"] == "healthy"]
    degraded = [d for d in devices if d["status"] == "degraded"]
    critical = [d for d in devices if d["status"] == "critical"]

    print(f"Device fleet: {len(devices)} total")
    print(f"  Healthy: {len(healthy)}, Degraded: {len(degraded)}, Critical: {len(critical)}")


if __name__ == "__main__":
    example_1_sensor_readings()
    example_2_mqtt_payloads()
    example_3_device_health()
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
