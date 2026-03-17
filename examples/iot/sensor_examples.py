#!/usr/bin/env python3
"""
IoT examples - sensor data and MQTT with fraq.

Shows how to:
1. Generate realistic sensor readings
2. Create MQTT-style message payloads
3. Build time-series with anomalies
4. Device registry and health monitoring
5. Edge computing data prep

Run:
    pip install fraq
    python iot/sensor_examples.py
"""

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

    schema = FraqSchema()

    # Temperature with realistic bounds
    schema.add_field("temperature", "float", transform=lambda v: round(18 + v * 12, 2))  # 18-30°C
    # Humidity 0-100%
    schema.add_field("humidity", "float", transform=lambda v: round(v * 100, 2))
    # Pressure 980-1060 hPa
    schema.add_field("pressure", "float", transform=lambda v: round(980 + v * 80, 2))
    # Light level 0-1000 lux
    schema.add_field("light", "float", transform=lambda v: round(v * 1000, 2))
    # Battery level 0-100%
    schema.add_field("battery", "float", transform=lambda v: round(20 + v * 80, 2))

    # Generate readings for multiple sensors
    sensors = []
    base_time = datetime.now()

    for sensor_id in ["sensor_001", "sensor_002", "sensor_003"]:
        readings = []
        for i, record in enumerate(schema.records(depth=2, branching=4)):
            if i >= 5:  # 5 readings per sensor
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
        "factory/sensors/vibration/machine_3",
        "home/living_room/temperature",
        "home/living_room/motion",
    ]

    schema = FraqSchema()
    schema.add_field("value", "float")
    schema.add_field("unit", "str", transform=lambda v: "celsius" if v < 0.33 else ("percent" if v < 0.66 else "boolean"))
    schema.add_field("quality", "str", transform=lambda v: "good" if v > 0.8 else ("fair" if v > 0.5 else "poor"))

    messages = []
    for topic in topics:
        for i, record in enumerate(schema.records(depth=1, branching=1)):
            payload = {
                "topic": topic,
                "payload": {
                    "value": round(record["value"] * 100, 2),
                    "unit": record["unit"],
                    "timestamp": datetime.now().isoformat(),
                    "quality": record["quality"],
                },
                "qos": 1 if "factory" in topic else 0,
                "retain": "home" in topic,
            }
            messages.append(payload)
            break  # 1 message per topic

    print(f"Generated {len(messages)} MQTT messages")
    for msg in messages[:3]:
        print(f"\n  Topic: {msg['topic']}")
        print(f"  QoS: {msg['qos']}, Retain: {msg['retain']}")
        print(f"  Payload: {json.dumps(msg['payload'], indent=2)[:100]}...")


def example_3_time_series_with_anomalies():
    """Generate time-series data with injected anomalies."""
    print("\n" + "=" * 60)
    print("3. TIME-SERIES WITH ANOMALIES")
    print("=" * 60)

    base_time = datetime(2024, 3, 15, 10, 0, 0)  # Start at 10:00 AM

    schema = FraqSchema()

    def generate_with_anomaly(v):
        # Normal range: 20-25°C
        base = 20 + v * 5
        # Inject anomaly at specific thresholds
        if v > 0.7 and v < 0.75:  # Spike
            return round(base + 15, 2), True, "temperature_spike"
        elif v > 0.4 and v < 0.45:  # Drop
            return round(base - 10, 2), True, "temperature_drop"
        else:
            return round(base, 2), False, "normal"

    schema.add_field("reading", "float", transform=generate_with_anomaly)

    series = []
    for i, record in enumerate(schema.records(depth=3, branching=5)):
        if i >= 50:
            break
        temp, is_anomaly, anomaly_type = record["reading"]
        series.append({
            "timestamp": (base_time + timedelta(minutes=i*5)).isoformat(),
            "temperature": temp,
            "is_anomaly": is_anomaly,
            "type": anomaly_type,
        })

    print(f"Generated {len(series)} readings with anomalies")

    normal = [s for s in series if not s["is_anomaly"]]
    anomalies = [s for s in series if s["is_anomaly"]]

    print(f"  Normal: {len(normal)}, Anomalies: {len(anomalies)}")

    if anomalies:
        print("\nDetected anomalies:")
        for a in anomalies:
            print(f"  {a['timestamp'][11:19]}: {a['temperature']}°C ({a['type']})")


def example_4_device_registry():
    """Simulate IoT device registry with health status."""
    print("\n" + "=" * 60)
    print("4. DEVICE REGISTRY & HEALTH MONITORING")
    print("=" * 60)

    schema = FraqSchema()
    schema.add_field("device_id", "str", transform=lambda v: f"DEV-{int(v*10000):06d}")
    schema.add_field("firmware", "str", transform=lambda v: f"v{1 + int(v*3)}.{int(v*10)}")
    schema.add_field("uptime_hours", "int", transform=lambda v: int(v * 720))  # 0-30 days
    schema.add_field("battery_level", "float", transform=lambda v: round(v * 100, 1))
    schema.add_field("signal_strength", "float", transform=lambda v: round(-120 + v * 80, 1))  # -120 to -40 dBm

    def health_status(v):
        battery = v * 100
        signal = -120 + v * 80
        if battery > 50 and signal > -80:
            return "healthy"
        elif battery > 20 and signal > -100:
            return "degraded"
        else:
            return "critical"

    schema.add_field("status", "str", transform=health_status)

    devices = []
    for i, record in enumerate(schema.records(depth=2, branching=10)):
        if i >= 20:
            break
        devices.append(record)

    # Group by status
    healthy = [d for d in devices if d["status"] == "healthy"]
    degraded = [d for d in devices if d["status"] == "degraded"]
    critical = [d for d in devices if d["status"] == "critical"]

    print(f"Device fleet: {len(devices)} total")
    print(f"  🟢 Healthy: {len(healthy)}")
    print(f"  🟡 Degraded: {len(degraded)}")
    print(f"  🔴 Critical: {len(critical)}")

    if critical:
        print("\nCritical devices need attention:")
        for d in critical[:3]:
            print(f"  {d['device_id']}: battery={d['battery_level']}%, signal={d['signal_strength']}dBm")


def example_5_edge_computing():
    """Simulate edge computing data preprocessing."""
    print("\n" + "=" * 60)
    print("5. EDGE COMPUTING DATA PREP")
    print("=" * 60)

    # Raw sensor data at the edge
    schema = FraqSchema()
    schema.add_field("raw_value", "float")

    def edge_process(v):
        # Apply calibration
        calibrated = v * 100 + 10
        # Apply smoothing (moving average simulation)
        smoothed = calibrated * 0.8 + 50 * 0.2
        # Threshold detection
        threshold_exceeded = smoothed > 80
        # Compression: only send if significant change
        return {
            "processed": round(smoothed, 2),
            "original": round(v, 4),
            "threshold_exceeded": threshold_exceeded,
            "send_to_cloud": threshold_exceeded or v < 0.1,  # Send anomalies or calibration checks
        }

    schema.add_field("edge_result", "dict", transform=edge_process)

    results = []
    for i, record in enumerate(schema.records(depth=2, branching=8)):
        if i >= 10:
            break
        result = record["edge_result"]
        results.append({
            "reading_id": i,
            **result,
        })

    cloud_sent = [r for r in results if r["send_to_cloud"]]
    filtered = [r for r in results if not r["send_to_cloud"]]

    print(f"Processed {len(results)} readings at edge")
    print(f"  Sent to cloud: {len(cloud_sent)} ({len(cloud_sent)/len(results)*100:.0f}%)")
    print(f"  Filtered locally: {len(filtered)} ({len(filtered)/len(results)*100:.0f}%)")

    print("\nSample processing:")
    for r in results[:3]:
        action = "📤 SEND" if r["send_to_cloud"] else "💾 LOCAL"
        print(f"  {action}: {r['original']} → {r['processed']} (alert: {r['threshold_exceeded']})")


if __name__ == "__main__":
    example_1_sensor_readings()
    example_2_mqtt_payloads()
    example_3_time_series_with_anomalies()
    example_4_device_registry()
    example_5_edge_computing()

    print("\n" + "=" * 60)
    print("Done! See iot/sensor_examples.py")
    print("=" * 60)
