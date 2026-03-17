#!/usr/bin/env python3
"""AI/ML examples - UPROSZCZONE używając text2fraq."""

from __future__ import annotations

from fraq.text2fraq import text2fraq, text2query


def example_1_classification():
    """Generate binary classification dataset - UPROSZCZONE."""
    print("=" * 60)
    print("1. BINARY CLASSIFICATION (text2fraq)")
    print("=" * 60)

    # Uproszczone: jedna linia zamiast schema + root + records
    result = text2fraq("generuj 100 próbek klasyfikacji binarnej 3 cechy label")
    print(f"Result type: {type(result).__name__}")
    if isinstance(result, list):
        print(f"Generated {len(result)} samples")
        for r in result[:3]:
            print(f"  {r}")


def example_2_regression():
    """Generate regression dataset - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("2. REGRESSION HOUSES (text2fraq)")
    print("=" * 60)

    # Uproszczone: NL zamiast ręcznego definiowania pól
    result = text2fraq("generuj 50 rekordów regresji ceny domów sqm bedrooms age price")
    print(f"Generated {len(result) if isinstance(result, list) else 'N/A'} houses")


def example_3_timeseries():
    """Generate time-series - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("3. TIME-SERIES (text2fraq)")
    print("=" * 60)

    # Uproszczone: jedna komenda
    result = text2fraq("generuj time-series 168 godzin wartości trend seasonality noise")
    print(f"Generated {len(result) if isinstance(result, list) else 'N/A'} data points")


def example_4_query_parse():
    """Parse query - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("4. PARSE QUERY (text2query)")
    print("=" * 60)

    # Uproszczone: parsowanie bez wykonania
    query = text2query("show 10 sensor readings temperature humidity pressure")
    print(f"Parsed: {query}")
    print(f"Fields: {getattr(query, 'fields', 'N/A')}")


if __name__ == "__main__":
    example_1_classification()
    example_2_regression()
    example_3_timeseries()
    example_4_query_parse()
    print("\n" + "=" * 60)
    print("Done! Użyj: from fraq.text2fraq import text2fraq")
    print("=" * 60)
