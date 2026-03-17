#!/usr/bin/env python3
"""
Database examples - SQL integration with fraq.

Shows how to:
1. Generate fractal data and save to SQLite
2. Query existing database with fraq SQL adapter
3. Generate SQL schemas and functions
4. Hybrid: combine fractal data with real DB records

Run:
    pip install fraq
    python database/sqlite_examples.py
"""

from __future__ import annotations

import sqlite3
import json
from datetime import datetime
from pathlib import Path

from fraq import FraqSchema, FraqNode, query
from fraq.adapters.sql_adapter import SQLAdapter


def example_1_generate_to_sqlite():
    """Generate fractal sensor data and store in SQLite."""
    print("=" * 60)
    print("1. GENERATE FRACTAL DATA → SQLITE")
    print("=" * 60)

    # Create in-memory database
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

    # Generate fractal data
    schema = FraqSchema()
    schema.add_field("temperature", "float", transform=lambda v: round(v * 40 - 10, 2))  # -10 to 30°C
    schema.add_field("humidity", "float", transform=lambda v: round(v * 100, 2))  # 0-100%
    schema.add_field("pressure", "float", transform=lambda v: round(980 + v * 80, 2))  # 980-1060 hPa
    schema.add_field("sensor_id", "str", transform=lambda v: f"sensor_{int(v * 1000):04d}")

    # Insert 50 records
    now = datetime.now()
    for i, record in enumerate(schema.records(depth=3, branching=4)):  # 4^3 = 64 records
        if i >= 50:
            break
        timestamp = now.isoformat()
        conn.execute(
            "INSERT INTO sensor_readings (timestamp, temperature, humidity, pressure, sensor_id, fraq_seed) VALUES (?, ?, ?, ?, ?, ?)",
            (timestamp, record["temperature"], record["humidity"], record["pressure"], record["sensor_id"], i)
        )
    conn.commit()

    # Query back
    cursor = conn.execute("SELECT * FROM sensor_readings LIMIT 5")
    rows = cursor.fetchall()

    print(f"Inserted 50 sensor readings into SQLite")
    print("Sample records:")
    for row in rows:
        print(f"  {row[5]}: {row[2]}°C, {row[3]}%, {row[4]}hPa")

    conn.close()


def example_2_sql_adapter_query():
    """Use SQL adapter to query existing database."""
    print("\n" + "=" * 60)
    print("2. SQL ADAPTER → QUERY EXISTING DATABASE")
    print("=" * 60)

    # Create temp database with sample data
    db_path = "/tmp/fraq_example.db"
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY,
            invoice_id TEXT,
            amount REAL,
            vat_rate REAL,
            client_id TEXT,
            paid BOOLEAN
        )
    """)

    # Insert sample data
    sample_data = [
        ("INV-2024-001", 1234.56, 0.23, "CLI-001", 1),
        ("INV-2024-002", 5678.90, 0.23, "CLI-002", 0),
        ("INV-2024-003", 999.99, 0.08, "CLI-001", 1),
        ("INV-2024-004", 4567.89, 0.23, "CLI-003", 0),
        ("INV-2024-005", 2345.67, 0.08, "CLI-002", 1),
    ]
    conn.executemany(
        "INSERT INTO invoices (invoice_id, amount, vat_rate, client_id, paid) VALUES (?, ?, ?, ?, ?)",
        sample_data
    )
    conn.commit()
    conn.close()

    # Use SQL adapter
    adapter = SQLAdapter(connection_string=f"sqlite:///{db_path}")

    # Load as fraq node
    node = adapter.load_root("SELECT * FROM invoices WHERE paid = 1")

    print(f"Query: SELECT * FROM invoices WHERE paid = 1")
    print(f"Records found: {len(node.meta.get('rows', []))}")
    for row in node.meta.get("rows", [])[:3]:
        print(f"  {row['invoice_id']}: {row['amount']} PLN (paid: {row['paid']})")

    Path(db_path).unlink(missing_ok=True)


def example_3_generate_sql_function():
    """Generate PostgreSQL function for fractal queries."""
    print("\n" + "=" * 60)
    print("3. GENERATE SQL FUNCTION")
    print("=" * 60)

    schema = FraqSchema()
    schema.add_field("reading_id", "str")
    schema.add_field("value", "float")
    schema.add_field("timestamp", "int")

    sql_function = schema.to_sql_function(
        name="fraq_sensor_zoom",
        dialect="postgresql",
        level_param="p_level",
        direction_param="p_direction"
    )

    print("Generated PostgreSQL function:")
    print(sql_function[:500] + "..." if len(sql_function) > 500 else sql_function)


def example_4_hybrid_data():
    """Combine real DB data with fractal-generated data."""
    print("\n" + "=" * 60)
    print("4. HYBRID: REAL DATA + FRACTAL DATA")
    print("=" * 60)

    # Real data from DB
    real_customers = [
        {"customer_id": "C001", "name": "Acme Corp", "region": "EU"},
        {"customer_id": "C002", "name": "TechStart Inc", "region": "US"},
    ]

    # Generate fractal transactions for each customer
    schema = FraqSchema()
    schema.add_field("transaction_id", "str", transform=lambda v: f"TX-{int(v * 100000):06d}")
    schema.add_field("amount", "float", transform=lambda v: round(v * 10000, 2))
    schema.add_field("risk_score", "float", transform=lambda v: round(v, 4))

    print(f"Real customers: {len(real_customers)}")
    print("Generated transactions per customer:")

    for customer in real_customers:
        # Generate 3 transactions per customer
        transactions = []
        for record in schema.records(depth=1, branching=3):
            if len(transactions) >= 3:
                break
            transactions.append({
                **record,
                "customer_id": customer["customer_id"],
                "customer_name": customer["name"],
                "region": customer["region"]
            })

        print(f"\n  {customer['name']} ({customer['region']}):")
        for tx in transactions:
            print(f"    {tx['transaction_id']}: ${tx['amount']} (risk: {tx['risk_score']})")


if __name__ == "__main__":
    example_1_generate_to_sqlite()
    example_2_sql_adapter_query()
    example_3_generate_sql_function()
    example_4_hybrid_data()

    print("\n" + "=" * 60)
    print("Done! See database/sqlite_examples.py for more.")
    print("=" * 60)
