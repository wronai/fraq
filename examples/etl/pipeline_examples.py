#!/usr/bin/env python3
"""
ETL examples - data pipelines with fraq.

Shows how to:
1. Extract from multiple sources
2. Transform with fraq schemas
3. Load to different destinations
4. Data validation and quality checks
5. Pipeline orchestration patterns

Run:
    pip install fraq pandas
    python etl/pipeline_examples.py
"""

from __future__ import annotations

import json
import csv
from datetime import datetime
from io import StringIO
from typing import List, Dict, Any, Iterator

from fraq import FraqSchema, query


def example_1_multi_source_extract():
    """Extract from multiple sources and normalize."""
    print("=" * 60)
    print("1. MULTI-SOURCE EXTRACTION")
    print("=" * 60)

    # Source 1: JSON API response
    api_data = [
        {"userId": "U001", "fullName": "John Doe", "accountBalance": 1234.56},
        {"userId": "U002", "fullName": "Jane Smith", "accountBalance": 5678.90},
    ]

    # Source 2: CSV file
    csv_data = """id,name,balance
C001,Alice Jones,2345.67
C002,Bob Brown,3456.78"""

    # Source 3: Database records
    db_data = [
        {"customer_id": "D001", "name": "Charlie Day", "amount": 4567.89},
    ]

    # Normalize with fraq schema
    schema = FraqSchema()
    schema.add_field("user_id", "str")
    schema.add_field("name", "str")
    schema.add_field("balance", "float")

    normalized = []

    # Transform API data
    for record in api_data:
        normalized.append({
            "user_id": record["userId"],
            "name": record["fullName"],
            "balance": record["accountBalance"],
            "source": "api",
        })

    # Transform CSV data
    reader = csv.DictReader(StringIO(csv_data))
    for record in reader:
        normalized.append({
            "user_id": record["id"],
            "name": record["name"],
            "balance": float(record["balance"]),
            "source": "csv",
        })

    # Transform DB data
    for record in db_data:
        normalized.append({
            "user_id": record["customer_id"],
            "name": record["name"],
            "balance": record["amount"],
            "source": "database",
        })

    print(f"Extracted and normalized {len(normalized)} records")
    print("\nUnified schema:")
    for r in normalized:
        print(f"  [{r['source']:8}] {r['user_id']}: {r['name']} - ${r['balance']}")


def example_2_schema_transformation():
    """Transform data using fraq schemas."""
    print("\n" + "=" * 60)
    print("2. SCHEMA TRANSFORMATION")
    print("=" * 60)

    # Raw sensor data
    raw_schema = FraqSchema()
    raw_schema.add_field("sensor_id", "str", transform=lambda v: f"SENSOR_{int(v*1000):04d}")
    raw_schema.add_field("raw_temp", "float", transform=lambda v: v)  # 0-1 range
    raw_schema.add_field("raw_humidity", "float", transform=lambda v: v)

    # Transform to processed schema
    def transform_record(raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "device_id": raw["sensor_id"],
            "temperature_c": round(10 + raw["raw_temp"] * 30, 2),  # 10-40°C
            "humidity_percent": round(raw["raw_humidity"] * 100, 2),  # 0-100%
            "heat_index": round(
                10 + raw["raw_temp"] * 30 + raw["raw_humidity"] * 10, 2
            ),  # Combined metric
            "timestamp": datetime.now().isoformat(),
            "quality_flag": "good" if raw["raw_temp"] > 0.1 else "suspect",
        }

    # Process records
    processed = []
    for i, raw in enumerate(raw_schema.records(depth=2, branching=5)):
        if i >= 5:
            break
        processed.append(transform_record(raw))

    print(f"Transformed {len(processed)} records")
    print("\nRaw → Processed:")
    for i, p in enumerate(processed[:3]):
        print(f"  {p['device_id']}: {p['temperature_c']}°C, {p['humidity_percent']}%")
        print(f"    → heat_index: {p['heat_index']}, quality: {p['quality_flag']}")


def example_3_data_validation():
    """Validate data quality during ETL."""
    print("\n" + "=" * 60)
    print("3. DATA VALIDATION & QUALITY")
    print("=" * 60)

    def validate_transaction(record: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate transaction record."""
        errors = []

        if not record.get("amount") or record["amount"] <= 0:
            errors.append("Invalid amount")

        if not record.get("account_id") or len(record["account_id"]) < 3:
            errors.append("Invalid account_id")

        if record.get("amount", 0) > 1000000:
            errors.append("Amount exceeds limit")

        return len(errors) == 0, errors

    # Generate test transactions
    schema = FraqSchema()
    schema.add_field("account_id", "str", transform=lambda v: f"ACC{int(v*10000):06d}")
    schema.add_field("amount", "float", transform=lambda v: round(v * 1500000, 2))  # Some will exceed limit
    schema.add_field("currency", "str", transform=lambda v: ["USD", "EUR", "GBP"][int(v * 3)])

    transactions = []
    valid_count = 0
    invalid_count = 0

    for i, record in enumerate(schema.records(depth=3, branching=5)):
        if i >= 10:
            break

        is_valid, errors = validate_transaction(record)
        transactions.append({
            **record,
            "_valid": is_valid,
            "_errors": errors,
        })

        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1

    print(f"Processed {len(transactions)} transactions")
    print(f"  ✓ Valid: {valid_count}")
    print(f"  ✗ Invalid: {invalid_count}")

    print("\nValidation details:")
    for t in transactions[:5]:
        status = "✓" if t["_valid"] else "✗"
        errors = f" ({', '.join(t['_errors'])})" if t["_errors"] else ""
        print(f"  {status} {t['account_id']}: ${t['amount']:,.2f} {t['currency']}{errors}")


def example_4_incremental_load():
    """Simulate incremental data loading."""
    print("\n" + "=" * 60)
    print("4. INCREMENTAL LOAD PATTERN")
    print("=" * 60)

    def generate_incremental_batch(last_id: int = 0, count: int = 5) -> List[Dict[str, Any]]:
        """Generate next batch of records."""
        schema = FraqSchema()
        schema.add_field("sequence", "int", transform=lambda v: last_id + int(v * count) + 1)
        schema.add_field("event_type", "str", transform=lambda v: ["click", "view", "purchase"][int(v * 3)])
        schema.add_field("value", "float", transform=lambda v: round(v * 100, 2))

        batch = []
        for i, record in enumerate(schema.records(depth=1, branching=count)):
            if i >= count:
                break
            batch.append({
                "id": record["sequence"],
                "type": record["event_type"],
                "value": record["value"],
                "processed_at": datetime.now().isoformat(),
            })

        return batch

    # Simulate 3 incremental loads
    last_processed_id = 0
    all_records = []

    for batch_num in range(1, 4):
        batch = generate_incremental_batch(last_processed_id, 3)
        all_records.extend(batch)

        # Update watermark
        last_processed_id = max(r["id"] for r in batch)

        print(f"Batch {batch_num}: loaded {len(batch)} records (IDs: {batch[0]['id']}-{batch[-1]['id']})")

    print(f"\nTotal records: {len(all_records)}")
    print(f"Watermark: {last_processed_id}")


def example_5_pipeline_orchestration():
    """Simple pipeline orchestration pattern."""
    print("\n" + "=" * 60)
    print("5. PIPELINE ORCHESTRATION")
    print("=" * 60)

    class ETLPipeline:
        """Simple ETL pipeline with stages."""

        def __init__(self, name: str):
            self.name = name
            self.stages = []
            self.metrics = {}

        def add_stage(self, name: str, func):
            self.stages.append((name, func))
            return self

        def run(self, data: Any) -> Any:
            result = data
            print(f"Running pipeline: {self.name}")

            for stage_name, stage_func in self.stages:
                start_time = datetime.now()
                result = stage_func(result)
                duration = (datetime.now() - start_time).total_seconds()

                self.metrics[stage_name] = {
                    "duration": duration,
                    "records": len(result) if isinstance(result, list) else 1,
                }
                print(f"  ✓ {stage_name}: {self.metrics[stage_name]['records']} records in {duration:.3f}s")

            return result

    # Define pipeline
    pipeline = ETLPipeline("Customer Data Pipeline")

    # Stage 1: Extract
    def extract(data):
        schema = FraqSchema()
        schema.add_field("customer_id", "str", transform=lambda v: f"CUST{int(v*10000):06d}")
        schema.add_field("revenue", "float", transform=lambda v: round(v * 10000, 2))
        return list(schema.records(depth=2, branching=5))[:5]

    # Stage 2: Transform
    def transform(records):
        return [{
            "id": r["customer_id"],
            "revenue_usd": r["revenue"],
            "tier": "gold" if r["revenue"] > 5000 else "silver" if r["revenue"] > 2000 else "bronze",
            "processed": datetime.now().isoformat(),
        } for r in records]

    # Stage 3: Validate
    def validate(records):
        return [r for r in records if r["revenue_usd"] > 0]

    pipeline.add_stage("extract", extract)
    pipeline.add_stage("transform", transform)
    pipeline.add_stage("validate", validate)

    # Run
    result = pipeline.run(None)

    print(f"\nFinal output ({len(result)} records):")
    for r in result[:3]:
        print(f"  {r['id']}: ${r['revenue_usd']:,.2f} ({r['tier']})")


if __name__ == "__main__":
    example_1_multi_source_extract()
    example_2_schema_transformation()
    example_3_data_validation()
    example_4_incremental_load()
    example_5_pipeline_orchestration()

    print("\n" + "=" * 60)
    print("Done! See etl/pipeline_examples.py")
    print("=" * 60)
