#!/usr/bin/env python3
"""Testing examples - UPROSZCZONE z nowym API fraq."""

from __future__ import annotations

from dataclasses import dataclass
from fraq import generate


@dataclass
class User:
    user_id: str
    name: str
    email: str
    age: int
    active: bool


def example_1_fixtures():
    """Unit test fixtures - UPROSZCZONE."""
    print("=" * 60)
    print("1. UNIT TEST FIXTURES (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: generate() zamiast ręcznego tworzenia
    records = generate({
        'user_id': 'str',
        'name': 'str',
        'email': 'str',
        'age': 'int:18-70',
        'active': 'bool',
    }, count=5)

    users = [User(**r) for r in records]

    print(f"Generated {len(users)} test users")
    for u in users[:3]:
        status = "✓" if u.active else "✗"
        print(f"  {status} {u.user_id}: {u.name}, {u.age}y")

    # Assertions
    assert len(users) == 5
    assert all(isinstance(u.age, int) for u in users)
    print("\n✓ All assertions passed")


def example_2_mock_api():
    """Mock API - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("2. MOCK API RESPONSES (UPROSZCZONE)")
    print("=" * 60)

    products = generate({
        'product_id': 'str',
        'name': 'str',
        'price': 'float:10-1000',
        'in_stock': 'bool',
    }, count=3)

    response = {
        "status": "success",
        "count": len(products),
        "data": products,
    }

    print(f"Mock response: {response['status']}, {response['count']} products")
    for p in products[:2]:
        stock = "✓" if p['in_stock'] else "✗"
        print(f"  {stock} {p['name']}: ${p['price']:.2f}")


def example_3_load_testing():
    """Load testing - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("3. LOAD TESTING (UPROSZCZONE)")
    print("=" * 60)

    requests = generate({
        'request_id': 'str',
        'endpoint': 'str',
        'method': 'str',
        'payload_size': 'int:100-10000',
    }, count=100)

    # Stats
    by_endpoint = {}
    for r in requests:
        ep = r['endpoint']
        by_endpoint[ep] = by_endpoint.get(ep, 0) + 1

    print(f"Generated {len(requests)} load test requests")
    for ep, count in sorted(by_endpoint.items(), key=lambda x: -x[1])[:3]:
        print(f"  {ep}: {count} ({count/len(requests)*100:.1f}%)")


if __name__ == "__main__":
    example_1_fixtures()
    example_2_mock_api()
    example_3_load_testing()
    print("\n" + "=" * 60)
    print("Done! Testing w wersji uproszczonej")
    print("=" * 60)
