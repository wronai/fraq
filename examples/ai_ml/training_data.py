#!/usr/bin/env python3
"""
AI/ML examples - synthetic training data with fraq.

Shows how to:
1. Generate classification datasets
2. Create regression training data
3. Build time-series for forecasting
4. Generate NLP text corpora
5. Create image augmentation parameters

Run:
    pip install fraq pandas scikit-learn
    python ai_ml/training_data.py
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

from fraq import FraqSchema, query


def example_1_classification_dataset():
    """Generate binary classification dataset."""
    print("=" * 60)
    print("1. BINARY CLASSIFICATION DATASET")
    print("=" * 60)

    schema = FraqSchema()
    schema.add_field("feature_1", "float")
    schema.add_field("feature_2", "float")
    schema.add_field("feature_3", "float")
    # Label: 1 if sum of features > 1.5, else 0
    schema.add_field("label", "bool", transform=lambda v: sum([v, v, v]) > 1.5)

    # Generate 100 samples
    samples = []
    for i, record in enumerate(schema.records(depth=4, branching=3)):
        if i >= 100:
            break
        samples.append(record)

    # Statistics
    positive = sum(1 for s in samples if s["label"])
    negative = len(samples) - positive

    print(f"Generated {len(samples)} samples")
    print(f"Class distribution: {positive} positive, {negative} negative")
    print("\nSample records:")
    for s in samples[:3]:
        print(f"  f1={s['feature_1']:.3f}, f2={s['feature_2']:.3f}, f3={s['feature_3']:.3f} → {s['label']}")

    # Export as CSV
    csv_lines = ["feature_1,feature_2,feature_3,label"]
    for s in samples:
        csv_lines.append(f"{s['feature_1']:.6f},{s['feature_2']:.6f},{s['feature_3']:.6f},{int(s['label'])}")

    print(f"\nCSV format ({len(csv_lines)} lines)")


def example_2_regression_data():
    """Generate regression training data with target variable."""
    print("\n" + "=" * 60)
    print("2. REGRESSION DATASET (House Prices)")
    print("=" * 60)

    schema = FraqSchema()
    schema.add_field("sqm", "float", transform=lambda v: int(20 + v * 180))  # 20-200 m²
    schema.add_field("bedrooms", "int", transform=lambda v: int(1 + v * 4))  # 1-5 bedrooms
    schema.add_field("age_years", "int", transform=lambda v: int(v * 50))  # 0-50 years
    schema.add_field("distance_city", "float", transform=lambda v: round(v * 30, 2))  # 0-30 km

    # Price = base + factors (deterministic formula)
    def calculate_price(v):
        sqm = int(20 + v * 180)
        bedrooms = int(1 + v * 4)
        age = int(v * 50)
        dist = round(v * 30, 2)
        base = 100000
        price = base + sqm * 3000 + bedrooms * 50000 - age * 2000 - dist * 5000
        return round(price, 2)

    schema.add_field("price", "float", transform=calculate_price)

    houses = []
    for i, record in enumerate(schema.records(depth=3, branching=4)):
        if i >= 50:
            break
        houses.append(record)

    print(f"Generated {len(houses)} house records")
    print("\nSample houses:")
    for h in houses[:3]:
        print(f"  {h['sqm']}m², {h['bedrooms']}br, {h['age_years']}y, {h['distance_city']}km → ${h['price']:,.0f}")

    avg_price = sum(h["price"] for h in houses) / len(houses)
    print(f"\nAverage price: ${avg_price:,.0f}")


def example_3_time_series_forecasting():
    """Generate time-series data for forecasting."""
    print("\n" + "=" * 60)
    print("3. TIME-SERIES FORECASTING DATA")
    print("=" * 60)

    start_date = datetime(2024, 1, 1)

    schema = FraqSchema()
    # Generate hourly patterns with trend and seasonality
    schema.add_field("hour_offset", "int", transform=lambda v: int(v * 168))  # 1 week = 168 hours
    schema.add_field("base_value", "float", transform=lambda v: 100 + v * 50)  # 100-150 base
    schema.add_field("noise", "float", transform=lambda v: (v - 0.5) * 20)  # -10 to +10 noise

    def calculate_ts(v):
        hour = int(v * 168)
        base = 100 + v * 50
        noise = (v - 0.5) * 20
        # Daily seasonality (peak at noon)
        seasonality = 20 * ((hour % 24) / 24)
        return round(base + seasonality + noise, 2)

    schema.add_field("value", "float", transform=calculate_ts)

    # Generate 7 days of hourly data
    series = []
    for i, record in enumerate(schema.records(depth=3, branching=6)):
        if i >= 168:  # 7 days * 24 hours
            break
        timestamp = start_date + timedelta(hours=record["hour_offset"])
        series.append({
            "timestamp": timestamp.isoformat(),
            "value": record["value"],
            "hour": timestamp.hour,
            "day": timestamp.strftime("%A"),
        })

    print(f"Generated {len(series)} hourly data points")
    print("\nFirst 3 hours:")
    for s in series[:3]:
        print(f"  {s['timestamp']}: {s['value']}")

    print("\nLast 3 hours:")
    for s in series[-3:]:
        print(f"  {s['timestamp']}: {s['value']}")


def example_4_nlp_text_corpus():
    """Generate synthetic text data for NLP."""
    print("\n" + "=" * 60)
    print("4. NLP TEXT CORPUS")
    print("=" * 60)

    # Word lists for generation
    subjects = ["customer", "product", "service", "team", "system", "application"]
    verbs = ["improved", "processed", "analyzed", "generated", "optimized", "deployed"]
    adjectives = ["efficient", "reliable", "scalable", "robust", "innovative", "dynamic"]
    objects = ["data pipeline", "API endpoint", "database query", "user interface", "report", "workflow"]

    schema = FraqSchema()
    schema.add_field("seed_val", "float")

    def generate_sentence(v):
        idx = int(v * 1000)
        subject = subjects[idx % len(subjects)]
        verb = verbs[(idx // 6) % len(verbs)]
        adj = adjectives[(idx // 36) % len(adjectives)]
        obj = objects[(idx // 216) % len(objects)]
        return f"The {adj} {subject} {verb} the {obj}."

    schema.add_field("text", "str", transform=generate_sentence)
    schema.add_field("label", "str", transform=lambda v: "positive" if v > 0.5 else "neutral")

    corpus = []
    for i, record in enumerate(schema.records(depth=2, branching=10)):
        if i >= 20:
            break
        corpus.append({
            "id": f"doc_{i:04d}",
            "text": record["text"],
            "label": record["label"],
        })

    print(f"Generated {len(corpus)} documents")
    print("\nSample documents:")
    for doc in corpus[:3]:
        print(f"  [{doc['label']}] {doc['text']}")


def example_5_multiclass_classification():
    """Generate multi-class classification dataset."""
    print("\n" + "=" * 60)
    print("5. MULTI-CLASS CLASSIFICATION")
    print("=" * 60)

    schema = FraqSchema()
    schema.add_field("x", "float")
    schema.add_field("y", "float")

    def classify(v):
        # 4 quadrants as classes
        x, y = v, v  # In real use, would be different values
        if v < 0.25:
            return "class_A"
        elif v < 0.5:
            return "class_B"
        elif v < 0.75:
            return "class_C"
        else:
            return "class_D"

    schema.add_field("class", "str", transform=classify)

    samples = []
    for i, record in enumerate(schema.records(depth=3, branching=5)):
        if i >= 200:
            break
        samples.append(record)

    # Count per class
    from collections import Counter
    distribution = Counter(s["class"] for s in samples)

    print(f"Generated {len(samples)} samples")
    print("Class distribution:")
    for cls, count in sorted(distribution.items()):
        pct = count / len(samples) * 100
        print(f"  {cls}: {count} ({pct:.1f}%)")


if __name__ == "__main__":
    example_1_classification_dataset()
    example_2_regression_data()
    example_3_time_series_forecasting()
    example_4_nlp_text_corpus()
    example_5_multiclass_classification()

    print("\n" + "=" * 60)
    print("Done! See ai_ml/training_data.py")
    print("=" * 60)
