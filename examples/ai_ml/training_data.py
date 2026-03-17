#!/usr/bin/env python3
"""AI/ML examples - UPROSZCZONE z nowym API fraq."""

from __future__ import annotations

from fraq import generate, FraqSchema


def example_1_classification():
    """Binary classification - UPROSZCZONE."""
    print("=" * 60)
    print("1. BINARY CLASSIFICATION (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: generate() z field hints
    samples = generate({
        'feature_1': 'float',
        'feature_2': 'float',
        'feature_3': 'float',
        'label': 'bool',
    }, count=100)

    positive = sum(1 for s in samples if s['label'])
    negative = len(samples) - positive

    print(f"Generated {len(samples)} samples")
    print(f"Distribution: {positive} positive, {negative} negative")
    print("\nSamples:")
    for s in samples[:3]:
        print(f"  f1={s['feature_1']:.2f}, f2={s['feature_2']:.2f} → {s['label']}")


def example_2_regression():
    """Regression - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("2. REGRESSION HOUSES (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: range hints dla realistic data
    houses = generate({
        'sqm': 'int:20-200',
        'bedrooms': 'int:1-5',
        'age_years': 'int:0-50',
        'distance_km': 'float:0-30',
        'price': 'float:50000-500000',
    }, count=50)

    print(f"Generated {len(houses)} houses")
    print("\nSamples:")
    for h in houses[:3]:
        print(f"  {h['sqm']}m², {h['bedrooms']}br, {h['age_years']}y → ${h['price']:,.0f}")

    avg_price = sum(h['price'] for h in houses) / len(houses)
    print(f"\nAverage price: ${avg_price:,.0f}")


def example_3_timeseries():
    """Time-series - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("3. TIME-SERIES (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: FraqSchema() bez root
    schema = FraqSchema()
    schema.add_field('value', 'float', transform=lambda v: round(100 + float(v) * 50, 2))

    series = list(schema.records(count=168))  # 7 days * 24 hours

    print(f"Generated {len(series)} hourly points")
    print(f"First: {series[0]['value']}, Last: {series[-1]['value']}")


if __name__ == "__main__":
    example_1_classification()
    example_2_regression()
    example_3_timeseries()
    print("\n" + "=" * 60)
    print("Done! AI/ML w wersji uproszczonej")
    print("=" * 60)
