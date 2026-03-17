#!/usr/bin/env python3
"""ETL examples - UPROSZCZONE z nowym API fraq."""

from __future__ import annotations

from fraq import generate, FraqSchema


def example_1_extract():
    """Extract - UPROSZCZONE."""
    print("=" * 60)
    print("1. ETL EXTRACT (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: generate() dla każdego źródła
    api_data = generate({
        'user_id': 'str',
        'name': 'str',
        'balance': 'float:1000-10000',
    }, count=3, seed=1)

    csv_data = generate({
        'id': 'str',
        'customer': 'str',
        'amount': 'float:1000-10000',
    }, count=2, seed=2)

    # Normalize
    normalized = []
    for r in api_data:
        normalized.append({
            'user_id': r['user_id'], 'name': r['name'], 
            'balance': r['balance'], 'source': 'api'
        })
    for r in csv_data:
        normalized.append({
            'user_id': r['id'], 'name': r['customer'],
            'balance': r['amount'], 'source': 'csv'
        })

    print(f"Unified {len(normalized)} records from multiple sources")
    for r in normalized[:3]:
        print(f"  [{r['source']:4}] {r['user_id']}: {r['name']} - ${r['balance']:.2f}")


def example_2_transform():
    """Transform - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("2. ETL TRANSFORM (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: generate() + transform
    raw = generate({
        'raw_temp': 'float',
        'raw_humidity': 'float',
    }, count=5)

    processed = []
    for r in raw:
        processed.append({
            'temperature': round(10 + float(r['raw_temp']) * 30, 2),
            'humidity': round(float(r['raw_humidity']) * 100, 2),
            'heat_index': round(10 + float(r['raw_temp']) * 30 + float(r['raw_humidity']) * 10, 2),
        })

    print(f"Transformed {len(processed)} records")
    for p in processed[:3]:
        print(f"  {p['temperature']}°C, {p['humidity']}% → heat: {p['heat_index']}")


def example_3_validate():
    """Validate - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("3. ETL VALIDATE (UPROSZCZONE)")
    print("=" * 60)

    records = generate({
        'account_id': 'str',
        'amount': 'float:0-15000',
    }, count=10)

    valid = [r for r in records if r['amount'] > 0 and r['account_id']]
    invalid = len(records) - len(valid)

    print(f"Validated {len(records)} transactions")
    print(f"  Valid: {len(valid)}, Invalid: {invalid}")


def example_4_pipeline():
    """Pipeline - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("4. ETL PIPELINE (UPROSZCZONE)")
    print("=" * 60)

    # Stage 1: Extract
    raw = generate({
        'customer_id': 'str',
        'revenue': 'float:1000-15000',
    }, count=5)
    print(f"Extract: {len(raw)} records")

    # Stage 2: Transform
    transformed = []
    for r in raw:
        transformed.append({
            'id': r['customer_id'],
            'revenue': r['revenue'],
            'tier': 'gold' if r['revenue'] > 10000 else 'silver' if r['revenue'] > 5000 else 'bronze',
        })
    print(f"Transform: {len(transformed)} records with tiers")

    # Stage 3: Result
    for t in transformed[:3]:
        print(f"  {t['id']}: ${t['revenue']:.2f} ({t['tier']})")


if __name__ == "__main__":
    example_1_extract()
    example_2_transform()
    example_3_validate()
    example_4_pipeline()
    print("\n" + "=" * 60)
    print("Done! ETL w wersji uproszczonej")
    print("=" * 60)
