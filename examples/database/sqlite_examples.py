#!/usr/bin/env python3
"""Database examples - UPROSZCZONE z nowym API fraq."""

from __future__ import annotations

import sqlite3
from fraq import generate, FraqSchema


def example_1_sqlite():
    """Generuj dane do SQLite - UPROSZCZONE."""
    print("=" * 60)
    print("1. GENERUJ → SQLITE (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: generate() zamiast root + schema + records
    records = generate({
        'temperature': 'float:10-40',
        'humidity': 'float:0-100',
        'pressure': 'float:980-1060',
        'sensor_id': 'str',
    }, count=50)

    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE sensors (temp REAL, humidity REAL, pressure REAL, sensor_id TEXT)
    """)

    for r in records:
        conn.execute(
            "INSERT INTO sensors VALUES (?, ?, ?, ?)",
            (r['temperature'], r['humidity'], r['pressure'], r['sensor_id'])
        )
    conn.commit()

    cursor = conn.execute("SELECT * FROM sensors LIMIT 5")
    print(f"Wstawiono {len(records)} rekordów")
    for row in cursor.fetchall():
        print(f"  {row[3]}: {row[0]}°C, {row[1]}%, {row[2]}hPa")
    conn.close()


def example_2_hybrid():
    """Hybrid: real + fractal - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("2. HYBRID: REAL + FRACTAL")
    print("=" * 60)

    customers = [
        {"customer_id": "C001", "name": "Acme Corp"},
        {"customer_id": "C002", "name": "TechStart"},
    ]

    # UPROSZCZONE: generate() dla danych fraktalnych
    transactions = generate({
        'tx_id': 'str',
        'amount': 'float:100-10000',
        'risk': 'float:0-1',
    }, count=6)

    print(f"Klienci: {len(customers)}")
    for i, cust in enumerate(customers):
        txs = transactions[i*3:(i+1)*3]
        print(f"\n  {cust['name']}:")
        for tx in txs:
            print(f"    {tx['tx_id']}: ${tx['amount']:.2f} (risk: {tx['risk']:.2f})")


def example_3_schema_save():
    """Schema + save - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("3. SCHEMA → SQLITE")
    print("=" * 60)

    # UPROSZCZONE: FraqSchema() bez root
    schema = FraqSchema()
    schema.add_field('device_id', 'str')
    schema.add_field('value', 'float')
    schema.add_field('status', 'float', transform=lambda v: 'OK' if float(v) > 0.5 else 'FAIL')

    records = list(schema.records(count=10))
    print(f"Generated {len(records)} records via schema")
    for r in records[:3]:
        print(f"  {r}")


if __name__ == "__main__":
    example_1_sqlite()
    example_2_hybrid()
    example_3_schema_save()
    print("\n" + "=" * 60)
    print("Done! Nowe uproszczone API fraq")
    print("=" * 60)
