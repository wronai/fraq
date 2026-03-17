#!/usr/bin/env python3
"""Basic query examples - UPROSZCZONE z nowym API fraq."""

from __future__ import annotations

from fraq import generate, stream, quick_schema, FraqSchema


def example_1_basic_query():
    """Podstawowe zapytanie - UPROSZCZONE."""
    print("=" * 60)
    print("1. PODSTAWOWE ZAPYTANIE (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: generate() zamiast query()
    records = generate({
        'value': 'float',
    }, count=5)

    print(f"Generated {len(records)} records:")
    for r in records:
        print(f"  value = {r['value']:.4f}")


def example_2_json_output():
    """JSON output - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("2. JSON OUTPUT (UPROSZCZONE)")
    print("=" * 60)

    import json

    records = generate({
        'id': 'str',
        'name': 'str',
        'value': 'float:0-100',
        'active': 'bool',
    }, count=3)

    print(json.dumps(records, indent=2))


def example_3_csv_output():
    """CSV output - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("3. CSV OUTPUT (UPROSZCZONE)")
    print("=" * 60)

    records = generate({
        'timestamp': 'str',
        'temperature': 'float:10-40',
        'humidity': 'float:0-100',
    }, count=5)

    # Print as CSV
    print("timestamp,temperature,humidity")
    for r in records:
        print(f"{r['timestamp']},{r['temperature']},{r['humidity']}")


def example_4_streaming():
    """Streaming - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("4. STREAMING (UPROSZCZONE)")
    print("=" * 60)

    print("Streaming 10 values:")
    for i, record in enumerate(stream({'reading': 'float'}, count=10)):
        print(f"  [{i:2}] {record['reading']:.4f}")


def example_5_schema():
    """Schema - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("5. SCHEMA (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: quick_schema()
    schema = quick_schema('temp', 'humidity', 'pressure')
    records = list(schema.records(count=3))

    print(f"Quick schema generated {len(records)} records")
    for r in records[:2]:
        print(f"  {r}")


def example_6_custom_schema():
    """Custom schema - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("6. CUSTOM SCHEMA (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: FraqSchema() bez root
    schema = FraqSchema()
    schema.add_field('sensor_id', 'str')
    schema.add_field('temperature', 'float', transform=lambda v: round(10 + float(v) * 30, 1))
    schema.add_field('status', 'bool')

    records = list(schema.records(count=3))
    print(f"Custom schema: {len(records)} records")
    for r in records:
        print(f"  {r['sensor_id']}: {r['temperature']}°C, active={r['status']}")


if __name__ == "__main__":
    example_1_basic_query()
    example_2_json_output()
    example_3_csv_output()
    example_4_streaming()
    example_5_schema()
    example_6_custom_schema()
    print("\n" + "=" * 60)
    print("Done! Query examples w wersji uproszczonej")
    print("=" * 60)
