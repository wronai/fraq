#!/usr/bin/env python3
"""Database examples - SQL integration with fraq."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from fraq import FraqSchema, FraqNode
from fraq.adapters.sql_adapter import SQLAdapter


def example_1_generate_to_sqlite():
    """Generate fractal sensor data and store in SQLite."""
    print("=" * 60)
    print("1. GENERATE FRACTAL DATA → SQLITE")
    print("=" * 60)

    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE sensor_readings (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            pressure REAL,
            sensor_id TEXT,
            fraq_seed INTEGER
        )
    """)

    # Generate fractal data - use float type for all fields with transforms
    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("temperature", "float", transform=lambda v: round(float(v) * 40 - 10, 2))
    schema.add_field("humidity", "float", transform=lambda v: round(float(v) * 100, 2))
    schema.add_field("pressure", "float", transform=lambda v: round(980 + float(v) * 80, 2))
    schema.add_field("sensor_id", "float", transform=lambda v: f"sensor_{int(float(v) * 1000):04d}")

    now = datetime.now()
    for i, record in enumerate(schema.records(depth=3, branching=4)):
        if i >= 50:
            break
        conn.execute(
            "INSERT INTO sensor_readings (timestamp, temperature, humidity, pressure, sensor_id, fraq_seed) VALUES (?, ?, ?, ?, ?, ?)",
            (now.isoformat(), record["temperature"], record["humidity"], record["pressure"], record["sensor_id"], i)
        )
    conn.commit()

    cursor = conn.execute("SELECT * FROM sensor_readings LIMIT 5")
    rows = cursor.fetchall()

    print(f"Inserted 50 sensor readings into SQLite")
    print("Sample records:")
    for row in rows:
        print(f"  {row[5]}: {row[2]}°C, {row[3]}%, {row[4]}hPa")

    conn.close()


def example_2_sql_adapter():
    """Use SQL adapter to work with database."""
    print("\n" + "=" * 60)
    print("2. SQL ADAPTER")
    print("=" * 60)

    adapter = SQLAdapter(table="invoices")
    rows = [
        {"invoice_id": "INV-001", "amount": 1234.56, "paid": 1},
        {"invoice_id": "INV-002", "amount": 5678.90, "paid": 0},
    ]
    node = adapter.load_root(rows=rows)

    print(f"Loaded {len(rows)} rows via SQL adapter")
    print(f"Node seed: {node.seed}")


def example_3_hybrid_data():
    """Combine real DB data with fractal-generated data."""
    print("\n" + "=" * 60)
    print("3. HYBRID: REAL DATA + FRACTAL DATA")
    print("=" * 60)

    real_customers = [
        {"customer_id": "C001", "name": "Acme Corp", "region": "EU"},
        {"customer_id": "C002", "name": "TechStart Inc", "region": "US"},
    ]

    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("transaction_id", "float", transform=lambda v: f"TX-{int(float(v) * 100000):06d}")
    schema.add_field("amount", "float", transform=lambda v: round(float(v) * 10000, 2))
    schema.add_field("risk_score", "float", transform=lambda v: round(float(v), 4))

    print(f"Real customers: {len(real_customers)}")
    for customer in real_customers:
        transactions = []
        for record in schema.records(depth=1, branching=3):
            if len(transactions) >= 3:
                break
            transactions.append({
                **record,
                "customer_id": customer["customer_id"],
                "customer_name": customer["name"],
            })

        print(f"\n  {customer['name']}:")
        for tx in transactions[:2]:
            print(f"    {tx['transaction_id']}: ${tx['amount']} (risk: {tx['risk_score']})")


if __name__ == "__main__":
    example_1_generate_to_sqlite()
    example_2_sql_adapter()
    example_3_hybrid_data()
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
