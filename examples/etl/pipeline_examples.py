#!/usr/bin/env python3
"""ETL examples - data pipelines with fraq."""

from __future__ import annotations

import json
import csv
from datetime import datetime
from io import StringIO
from typing import List, Dict, Any

from fraq import FraqSchema, FraqNode


def example_1_multi_source():
    """Extract from multiple sources and normalize."""
    print("=" * 60)
    print("1. MULTI-SOURCE EXTRACTION")
    print("=" * 60)

    api_data = [
        {"userId": "U001", "fullName": "John Doe", "balance": 1234.56},
        {"userId": "U002", "fullName": "Jane Smith", "balance": 5678.90},
    ]

    csv_data = """id,name,amount
C001,Alice Jones,2345.67
C002,Bob Brown,3456.78"""

    normalized = []
    for record in api_data:
        normalized.append({
            "user_id": record["userId"],
            "name": record["fullName"],
            "balance": record["balance"],
            "source": "api",
        })

    reader = csv.DictReader(StringIO(csv_data))
    for record in reader:
        normalized.append({
            "user_id": record["id"],
            "name": record["name"],
            "balance": float(record["amount"]),
            "source": "csv",
        })

    print(f"Extracted and normalized {len(normalized)} records")
    for r in normalized[:3]:
        print(f"  [{r['source']:6}] {r['user_id']}: {r['name']} - ${r['balance']}")


def example_2_transformation():
    """Transform data using fraq schemas."""
    print("\n" + "=" * 60)
    print("2. SCHEMA TRANSFORMATION")
    print("=" * 60)

    root = FraqNode(position=(0.0, 0.0, 0.0))
    raw_schema = FraqSchema(root=root)
    raw_schema.add_field("raw_temp", "float")
    raw_schema.add_field("raw_humidity", "float")

    def transform_record(raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "temperature_c": round(10 + float(raw["raw_temp"]) * 30, 2),
            "humidity_percent": round(float(raw["raw_humidity"]) * 100, 2),
        }

    processed = []
    for i, raw in enumerate(raw_schema.records(depth=2, branching=5)):
        if i >= 5:
            break
        processed.append(transform_record(raw))

    print(f"Transformed {len(processed)} records")
    for p in processed[:3]:
        print(f"  {p['temperature_c']}°C, {p['humidity_percent']}%")


def example_3_validation():
    """Validate data quality during ETL."""
    print("\n" + "=" * 60)
    print("3. DATA VALIDATION")
    print("=" * 60)

    def validate(record: Dict[str, Any]) -> bool:
        return record.get("amount", 0) > 0 and record.get("account_id", "") != ""

    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("account_id", "float", transform=lambda v: f"ACC{int(float(v)*10000):06d}")
    schema.add_field("amount", "float", transform=lambda v: round(float(v) * 10000, 2))

    transactions = []
    valid_count = 0

    for i, record in enumerate(schema.records(depth=3, branching=5)):
        if i >= 10:
            break
        is_valid = validate(record)
        if is_valid:
            valid_count += 1
        transactions.append({**record, "_valid": is_valid})

    print(f"Processed {len(transactions)} transactions")
    print(f"  Valid: {valid_count}, Invalid: {len(transactions) - valid_count}")


def example_4_pipeline():
    """Simple pipeline orchestration."""
    print("\n" + "=" * 60)
    print("4. PIPELINE ORCHESTRATION")
    print("=" * 60)

    class Pipeline:
        def __init__(self, name: str):
            self.name = name
            self.stages = []

        def add_stage(self, name: str, func):
            self.stages.append((name, func))
            return self

        def run(self, data: Any) -> Any:
            result = data
            print(f"Running pipeline: {self.name}")
            for stage_name, stage_func in self.stages:
                result = stage_func(result)
                print(f"  {stage_name}: {len(result) if isinstance(result, list) else 1} records")
            return result

    pipeline = Pipeline("Customer ETL")

    def extract(data):
        root = FraqNode(position=(0.0, 0.0, 0.0))
        schema = FraqSchema(root=root)
        schema.add_field("customer_id", "float", transform=lambda v: f"CUST{int(float(v)*10000):06d}")
        schema.add_field("revenue", "float", transform=lambda v: round(float(v) * 10000, 2))
        return list(schema.records(depth=2, branching=5))[:5]

    def transform(records):
        return [{"id": r["customer_id"], "revenue": r["revenue"]} for r in records]

    pipeline.add_stage("extract", extract)
    pipeline.add_stage("transform", transform)

    result = pipeline.run(None)
    print(f"\nFinal output ({len(result)} records)")


if __name__ == "__main__":
    example_1_multi_source()
    example_2_transformation()
    example_3_validation()
    example_4_pipeline()
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
