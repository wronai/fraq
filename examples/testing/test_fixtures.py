#!/usr/bin/env python3
"""Testing examples - mock data and test fixtures with fraq."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dataclasses import dataclass

from fraq import FraqSchema, FraqNode


def example_1_unit_test_fixtures():
    """Generate fixtures for unit testing."""
    print("=" * 60)
    print("1. UNIT TEST FIXTURES")
    print("=" * 60)

    @dataclass
    class User:
        user_id: str
        name: str
        email: str
        age: int
        active: bool

    def generate_users(count: int = 5) -> List[User]:
        root = FraqNode(position=(0.0, 0.0, 0.0))
        schema = FraqSchema(root=root)
        schema.add_field("user_id", "float", transform=lambda v: f"USR-{int(float(v)*10000):06d}")
        schema.add_field("name", "float", transform=lambda v: f"User_{int(float(v)*1000):03d}")
        schema.add_field("email", "float", transform=lambda v: f"user{int(float(v)*1000)}@test.com")
        schema.add_field("age", "float", transform=lambda v: int(18 + float(v) * 50))
        schema.add_field("active", "bool")

        users = []
        for i, record in enumerate(schema.records(depth=2, branching=5)):
            if i >= count:
                break
            users.append(User(**record))
        return users

    test_users = generate_users(5)

    print(f"Generated {len(test_users)} test users")
    for user in test_users[:3]:
        status = "✓" if user.active else "✗"
        print(f"  {status} {user.user_id}: {user.name}, {user.age}y")

    assert len(test_users) == 5
    assert all(isinstance(u.age, int) for u in test_users)
    print("\n✓ All assertions passed")


def example_2_mock_api():
    """Generate mock API responses."""
    print("\n" + "=" * 60)
    print("2. MOCK API RESPONSES")
    print("=" * 60)

    def mock_products(count: int = 3) -> Dict[str, Any]:
        root = FraqNode(position=(0.0, 0.0, 0.0))
        schema = FraqSchema(root=root)
        schema.add_field("product_id", "float", transform=lambda v: f"PROD-{int(float(v)*10000):06d}")
        schema.add_field("name", "float", transform=lambda v: f"Product {int(float(v)*1000)}")
        schema.add_field("price", "float", transform=lambda v: round(9.99 + float(v) * 990, 2))
        schema.add_field("in_stock", "bool")

        products = []
        for i, record in enumerate(schema.records(depth=2, branching=4)):
            if i >= count:
                break
            products.append(record)

        return {"status": "success", "count": len(products), "data": products}

    response = mock_products(3)
    print(f"Mock API response:")
    print(f"  Status: {response['status']}")
    print(f"  Products: {len(response['data'])}")
    for p in response['data'][:2]:
        stock = "✓" if p['in_stock'] else "✗"
        print(f"    {stock} {p['name']}: ${p['price']}")


def example_3_load_testing():
    """Generate data for load testing."""
    print("\n" + "=" * 60)
    print("3. LOAD TESTING DATA")
    print("=" * 60)

    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("request_id", "float", transform=lambda v: f"REQ-{int(float(v)*1000000):010d}")
    schema.add_field("user_id", "float", transform=lambda v: f"USR-{int(float(v)*10000):06d}")
    schema.add_field("endpoint", "float", transform=lambda v: ["/api/users", "/api/products", "/api/orders"][int(float(v) * 3)])
    schema.add_field("payload_size", "float", transform=lambda v: int(100 + float(v) * 9900))

    payloads = []
    for i, record in enumerate(schema.records(depth=4, branching=8)):
        if i >= 1000:
            break
        payloads.append(record)

    by_endpoint = {}
    for p in payloads:
        ep = p["endpoint"]
        by_endpoint[ep] = by_endpoint.get(ep, 0) + 1

    print(f"Generated {len(payloads)} load test payloads")
    for ep, count in sorted(by_endpoint.items())[:3]:
        print(f"  {ep}: {count} ({count/len(payloads)*100:.1f}%)")


if __name__ == "__main__":
    example_1_unit_test_fixtures()
    example_2_mock_api()
    example_3_load_testing()
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
