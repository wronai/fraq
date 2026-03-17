#!/usr/bin/env python3
"""ETL examples - UPROSZCZONE używając text2fraq."""

from __future__ import annotations

from fraq.text2fraq import text2fraq


def example_1_extract():
    """Extract - UPROSZCZONE."""
    print("=" * 60)
    print("1. ETL EXTRACT (text2fraq)")
    print("=" * 60)

    result = text2fraq("etl extract api json csv database 50 records unified")
    print(f"Extracted: {len(result) if isinstance(result, list) else 'N/A'} records")


def example_2_transform():
    """Transform - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("2. ETL TRANSFORM (text2fraq)")
    print("=" * 60)

    result = text2fraq("transform raw sensor temp humidity to processed normalized")
    print(f"Transformed: {len(result) if isinstance(result, list) else 'N/A'} records")


def example_3_validate():
    """Validate - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("3. ETL VALIDATE (text2fraq)")
    print("=" * 60)

    result = text2fraq("validate 100 transactions amount account quality check")
    print(f"Validated: {len(result) if isinstance(result, list) else 'N/A'} records")


def example_4_pipeline():
    """Pipeline - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("4. ETL PIPELINE (text2fraq)")
    print("=" * 60)

    result = text2fraq("pipeline etl extract transform load customers 5 stages")
    print(f"Pipeline result: {len(result) if isinstance(result, list) else 'N/A'} records")


if __name__ == "__main__":
    example_1_extract()
    example_2_transform()
    example_3_validate()
    example_4_pipeline()
    print("\n" + "=" * 60)
    print("Done! ETL w wersji uproszczonej")
    print("=" * 60)
