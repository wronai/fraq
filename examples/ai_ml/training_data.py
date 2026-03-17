#!/usr/bin/env python3
"""AI/ML examples - synthetic training data with fraq."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Dict, Any

from fraq import FraqSchema, FraqNode


def example_1_classification():
    """Generate binary classification dataset."""
    print("=" * 60)
    print("1. BINARY CLASSIFICATION DATASET")
    print("=" * 60)

    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("feature_1", "float")
    schema.add_field("feature_2", "float")
    schema.add_field("feature_3", "float")
    # Label based on sum of features
    schema.add_field("label", "float", transform=lambda v: float(v) * 3 > 1.5)

    samples = []
    for i, record in enumerate(schema.records(depth=4, branching=3)):
        if i >= 100:
            break
        samples.append(record)

    positive = sum(1 for s in samples if s["label"])
    negative = len(samples) - positive

    print(f"Generated {len(samples)} samples")
    print(f"Class distribution: {positive} positive, {negative} negative")
    print("\nSample records:")
    for s in samples[:3]:
        print(f"  f1={s['feature_1']:.3f}, f2={s['feature_2']:.3f}, f3={s['feature_3']:.3f} → {s['label']}")


def example_2_regression():
    """Generate regression training data."""
    print("\n" + "=" * 60)
    print("2. REGRESSION DATASET (House Prices)")
    print("=" * 60)

    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("sqm", "float", transform=lambda v: int(20 + float(v) * 180))
    schema.add_field("bedrooms", "float", transform=lambda v: int(1 + float(v) * 4))
    schema.add_field("age_years", "float", transform=lambda v: int(float(v) * 50))
    schema.add_field("distance_city", "float", transform=lambda v: round(float(v) * 30, 2))

    def calc_price(v):
        sqm = int(20 + float(v) * 180)
        bedrooms = int(1 + float(v) * 4)
        age = int(float(v) * 50)
        base = 100000
        price = base + sqm * 3000 + bedrooms * 50000 - age * 2000
        return round(price, 2)

    schema.add_field("price", "float", transform=calc_price)

    houses = []
    for i, record in enumerate(schema.records(depth=3, branching=4)):
        if i >= 50:
            break
        houses.append(record)

    print(f"Generated {len(houses)} house records")
    print("\nSample houses:")
    for h in houses[:3]:
        print(f"  {h['sqm']}m², {int(h['bedrooms'])}br, {int(h['age_years'])}y → ${h['price']:,.0f}")

    avg_price = sum(h["price"] for h in houses) / len(houses)
    print(f"\nAverage price: ${avg_price:,.0f}")


def example_3_time_series():
    """Generate time-series data for forecasting."""
    print("\n" + "=" * 60)
    print("3. TIME-SERIES FORECASTING DATA")
    print("=" * 60)

    start_date = datetime(2024, 1, 1)

    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)

    def calc_value(v):
        hour = int(float(v) * 168)
        base = 100 + float(v) * 50
        noise = (float(v) - 0.5) * 20
        seasonality = 20 * ((hour % 24) / 24)
        return round(base + seasonality + noise, 2)

    schema.add_field("value", "float", transform=calc_value)

    series = []
    for i, record in enumerate(schema.records(depth=3, branching=6)):
        if i >= 168:
            break
        timestamp = start_date + timedelta(hours=i)
        series.append({
            "timestamp": timestamp.isoformat(),
            "value": record["value"],
        })

    print(f"Generated {len(series)} hourly data points")
    print("\nFirst 3 hours:")
    for s in series[:3]:
        print(f"  {s['timestamp'][:16]}: {s['value']}")


if __name__ == "__main__":
    example_1_classification()
    example_2_regression()
    example_3_time_series()
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
