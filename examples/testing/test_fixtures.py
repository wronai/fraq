#!/usr/bin/env python3
"""
Testing examples - mock data and test fixtures with fraq.

Shows how to:
1. Generate test fixtures for unit tests
2. Create mock API responses
3. Build property-based test data
4. Database test fixtures
5. Load testing data generation

Run:
    pip install fraq pytest
    python testing/test_fixtures.py
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable
from dataclasses import dataclass

from fraq import FraqSchema, query


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
        """Generate deterministic test users."""
        schema = FraqSchema()
        schema.add_field("user_id", "str", transform=lambda v: f"USR-{int(v*10000):06d}")
        schema.add_field("name", "str", transform=lambda v: f"User_{int(v*1000):03d}")
        schema.add_field("email", "str", transform=lambda v: f"user{int(v*1000)}@test.com")
        schema.add_field("age", "int", transform=lambda v: int(18 + v * 50))  # 18-68
        schema.add_field("active", "bool")

        users = []
        for i, record in enumerate(schema.records(depth=2, branching=5)):
            if i >= count:
                break
            users.append(User(**record))
        return users

    # Generate test users
    test_users = generate_users(5)

    print(f"Generated {len(test_users)} test users")
    for user in test_users:
        status = "✓" if user.active else "✗"
        print(f"  {status} {user.user_id}: {user.name}, {user.age}y, {user.email}")

    # Test assertions
    assert len(test_users) == 5
    assert all(isinstance(u.age, int) for u in test_users)
    assert all(u.user_id.startswith("USR-") for u in test_users)
    print("\n✓ All assertions passed")


def example_2_mock_api_responses():
    """Generate mock API responses for testing."""
    print("\n" + "=" * 60)
    print("2. MOCK API RESPONSES")
    print("=" * 60)

    def mock_api_response(endpoint: str, count: int = 3) -> Dict[str, Any]:
        """Generate realistic API response."""

        if endpoint == "/api/products":
            schema = FraqSchema()
            schema.add_field("product_id", "str", transform=lambda v: f"PROD-{int(v*10000):06d}")
            schema.add_field("name", "str", transform=lambda v: f"Product {int(v*1000)}")
            schema.add_field("price", "float", transform=lambda v: round(9.99 + v * 990, 2))
            schema.add_field("in_stock", "bool")
            schema.add_field("category", "str", transform=lambda v: ["A", "B", "C"][int(v * 3)])

            products = []
            for i, record in enumerate(schema.records(depth=2, branching=4)):
                if i >= count:
                    break
                products.append(record)

            return {
                "status": "success",
                "count": len(products),
                "data": products,
                "meta": {"page": 1, "per_page": count}
            }

        elif endpoint == "/api/orders":
            return {
                "status": "success",
                "order_id": f"ORD-{int(query(seed=hash(endpoint))['value'] * 100000):08d}",
                "total": round(query(seed=hash(endpoint))['value'] * 500, 2),
                "items": count,
            }

        return {"status": "error", "message": "Unknown endpoint"}

    # Mock different endpoints
    products = mock_api_response("/api/products", 3)
    orders = mock_api_response("/api/orders", 2)

    print("Mock /api/products response:")
    print(f"  Status: {products['status']}")
    print(f"  Products: {len(products['data'])}")
    for p in products['data'][:2]:
        stock = "✓" if p['in_stock'] else "✗"
        print(f"    {stock} {p['name']}: ${p['price']}")

    print(f"\nMock /api/orders response:")
    print(f"  Order: {orders['order_id']}, Total: ${orders['total']}")


def example_3_property_based_data():
    """Generate data for property-based testing."""
    print("\n" + "=" * 60)
    print("3. PROPERTY-BASED TEST DATA")
    print("=" * 60)

    def generate_edge_cases() -> List[Dict[str, Any]]:
        """Generate edge case values."""
        schema = FraqSchema()

        # Values at boundaries
        def edge_value(v):
            if v < 0.2:
                return 0  # Zero
            elif v < 0.4:
                return 1  # One
            elif v < 0.6:
                return -1  # Negative
            elif v < 0.8:
                return float('inf')  # Infinity
            else:
                return None  # Null

        schema.add_field("value", "any", transform=edge_value)
        schema.add_field("expected_type", "str", transform=lambda v: type(edge_value(v)).__name__)

        cases = []
        for i, record in enumerate(schema.records(depth=2, branching=5)):
            cases.append(record)

        return cases

    edge_cases = generate_edge_cases()

    print(f"Generated {len(edge_cases)} edge cases")
    for case in edge_cases:
        val = case['value']
        type_str = case['expected_type']
        display = "None" if val is None else ("inf" if val == float('inf') else val)
        print(f"  value={display}, type={type_str}")


def example_4_database_fixtures():
    """Generate database test fixtures."""
    print("\n" + "=" * 60)
    print("4. DATABASE TEST FIXTURES")
    print("=" * 60)

    def generate_sql_fixtures(table: str, count: int = 5) -> List[str]:
        """Generate SQL INSERT statements."""

        if table == "customers":
            schema = FraqSchema()
            schema.add_field("customer_id", "str", transform=lambda v: f"CUST{int(v*10000):06d}")
            schema.add_field("name", "str", transform=lambda v: f"Customer {int(v*1000)}")
            schema.add_field("email", "str", transform=lambda v: f"cust{int(v*1000)}@example.com")
            schema.add_field("created_at", "str", transform=lambda v: (datetime.now() - timedelta(days=int(v*365))).isoformat())

            inserts = []
            for i, record in enumerate(schema.records(depth=2, branching=5)):
                if i >= count:
                    break
                sql = f"""INSERT INTO customers (customer_id, name, email, created_at)
VALUES ('{record['customer_id']}', '{record['name']}', '{record['email']}', '{record['created_at']}');"""
                inserts.append(sql)
            return inserts

        return []

    fixtures = generate_sql_fixtures("customers", 3)

    print(f"Generated {len(fixtures)} SQL fixtures")
    print("Sample INSERT statements:")
    for sql in fixtures[:2]:
        print(f"  {sql[:80]}...")


def example_5_load_testing_data():
    """Generate data for load testing."""
    print("\n" + "=" * 60)
    print("5. LOAD TESTING DATA")
    print("=" * 60)

    def generate_load_test_payloads(count: int = 1000) -> List[Dict[str, Any]]:
        """Generate payloads for load testing."""
        schema = FraqSchema()
        schema.add_field("request_id", "str", transform=lambda v: f"REQ-{int(v*1000000):010d}")
        schema.add_field("user_id", "str", transform=lambda v: f"USR-{int(v*10000):06d}")
        schema.add_field("endpoint", "str", transform=lambda v: ["/api/users", "/api/products", "/api/orders"][int(v * 3)])
        schema.add_field("method", "str", transform=lambda v: ["GET", "POST", "PUT", "DELETE"][int(v * 4)])
        schema.add_field("payload_size", "int", transform=lambda v: int(100 + v * 9900))  # 100B - 10KB
        schema.add_field("expected_latency_ms", "int", transform=lambda v: int(10 + v * 490))  # 10-500ms

        payloads = []
        for i, record in enumerate(schema.records(depth=4, branching=8)):
            if i >= count:
                break
            payloads.append(record)
        return payloads

    # Generate 1000 load test payloads
    payloads = generate_load_test_payloads(1000)

    # Statistics
    by_endpoint = {}
    for p in payloads:
        ep = p["endpoint"]
        by_endpoint[ep] = by_endpoint.get(ep, 0) + 1

    by_method = {}
    for p in payloads:
        m = p["method"]
        by_method[m] = by_method.get(m, 0) + 1

    print(f"Generated {len(payloads)} load test payloads")
    print(f"\nBy endpoint:")
    for ep, count in sorted(by_endpoint.items()):
        print(f"  {ep}: {count} ({count/len(payloads)*100:.1f}%)")

    print(f"\nBy method:")
    for method, count in sorted(by_method.items()):
        print(f"  {method}: {count} ({count/len(payloads)*100:.1f}%)")

    avg_latency = sum(p["expected_latency_ms"] for p in payloads) / len(payloads)
    print(f"\nAverage expected latency: {avg_latency:.0f}ms")


if __name__ == "__main__":
    example_1_unit_test_fixtures()
    example_2_mock_api_responses()
    example_3_property_based_data()
    example_4_database_fixtures()
    example_5_load_testing_data()

    print("\n" + "=" * 60)
    print("Done! See testing/test_fixtures.py")
    print("=" * 60)
