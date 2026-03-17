#!/usr/bin/env python3
"""
fraq — Praktyczne zastosowania.

IoT, ERP, AI/ML, DevOps, Legal, Finance — każde z zero storage.
"""

from fraq import (
    FraqNode, FraqSchema, FraqCursor, FraqQuery, FraqExecutor,
    SensorAdapter, SQLAdapter, FormatRegistry,
    HashGenerator, PerlinGenerator, SensorStreamGenerator,
    to_nlp2cmd_schema, to_openapi, to_proto,
)


# ═══════════════════════════════════════════════════════════════════════════
# 1. EMBEDDED / IoT — Sensor network simulation
# ═══════════════════════════════════════════════════════════════════════════

def example_iot_sensor_network():
    """Symulacja 10k sensorów bez storage'u — dla firmware dev na RPi/ESP32."""
    adapter = SensorAdapter(base_temp=23.5, base_humidity=60.0)

    print("=== IoT: 10 sensor readings ===")
    for i, reading in enumerate(adapter.stream(depth=5, count=10)):
        print(f"  sensor[{i}] → {reading['temperature']:.1f}°C, "
              f"{reading['humidity']:.1f}%, {reading['pressure']:.1f}hPa")

    # Eksport do Protobuf schema dla edge gateway
    root = adapter.load_root()
    schema = FraqSchema(root=root)
    schema.add_field("temperature", "float")
    schema.add_field("humidity", "float")
    schema.add_field("device_id", "str")
    proto = to_proto(schema, package="iot.edge")
    print(f"\n  Proto schema generated: {len(proto)} chars")
    print()


# ═══════════════════════════════════════════════════════════════════════════
# 2. ERP / ACCOUNTING — Invoice generation
# ═══════════════════════════════════════════════════════════════════════════

def example_erp_invoices():
    """Dynamiczne faktury z nieskończonymi detalami."""
    root = FraqNode(position=(0.0, 0.0, 0.0, 0.0), seed=2026)
    schema = FraqSchema(root=root)
    schema.add_field("invoice_id", "str")
    schema.add_field("amount", "float", transform=lambda v: round(v * 10000, 2))
    schema.add_field("vat", "float", transform=lambda v: round(v * 0.23, 4))
    schema.add_field("client_id", "str")
    schema.add_field("paid", "bool")

    print("=== ERP: Invoices (depth=2, branching=3 → 9 invoices) ===")
    for rec in schema.records(depth=2, branching=3):
        status = "PAID" if rec["paid"] else "PENDING"
        print(f"  {rec['invoice_id']} | {rec['amount']:>10.2f} PLN | "
              f"VAT {rec['vat']:.4f} | {rec['client_id']} | {status}")

    # SQL integration
    adapter = SQLAdapter(table="invoices")
    insert = adapter.save(root, "")
    print(f"\n  SQL: {insert[:80]}...")
    print()


# ═══════════════════════════════════════════════════════════════════════════
# 3. AI/ML — Training data generation
# ═══════════════════════════════════════════════════════════════════════════

def example_ai_training_data():
    """Nieskończone datasety treningowe — zero disk, perfect dla federated learning."""
    root = FraqNode(position=(0.0, 0.0, 0.0), seed=1337)
    schema = FraqSchema(root=root)
    schema.add_field("feature_1", "float")
    schema.add_field("feature_2", "float")
    schema.add_field("feature_3", "float")
    schema.add_field("label", "bool")

    q = FraqQuery().zoom(3).select(
        "feature_1:float", "feature_2:float", "feature_3:float", "label:bool"
    ).output("records").take(20)

    records = FraqExecutor(root).execute(q)
    print(f"=== AI/ML: {len(records)} training samples ===")
    for i, r in enumerate(records[:5]):
        print(f"  [{i}] f1={r['feature_1']:.4f} f2={r['feature_2']:.4f} "
              f"f3={r['feature_3']:.4f} label={r['label']}")
    print(f"  ... ({len(records)} total)")

    # NDJSON export for LLM fine-tuning
    ndjson = FormatRegistry.serialize("jsonl", records[:3])
    print(f"\n  NDJSON preview:\n  {ndjson[:200]}")
    print()


# ═══════════════════════════════════════════════════════════════════════════
# 4. DEVOPS — Load / chaos testing
# ═══════════════════════════════════════════════════════════════════════════

def example_devops_load_test():
    """Generuj test payloads dla K8s load testing."""
    root = FraqNode(position=(0.0, 0.0, 0.0), seed=9999,
                    generator=HashGenerator(range_min=0.0, range_max=100.0))

    print("=== DevOps: Load test payloads ===")
    cursor = FraqCursor(root=root)
    for i in range(5):
        cursor.advance()
        val = cursor.current.value
        print(f"  request[{i}] → CPU load: {val:.1f}%, depth: {cursor.depth}")

    # OpenAPI spec for the test endpoint
    schema = FraqSchema(root=root)
    schema.add_field("cpu_percent", "float")
    schema.add_field("memory_mb", "int")
    schema.add_field("request_id", "str")
    spec = to_openapi(schema, title="Load Test API", base_path="/chaos")
    print(f"\n  OpenAPI spec: {len(spec['paths'])} endpoints")
    print()


# ═══════════════════════════════════════════════════════════════════════════
# 5. FINANCE — Leasing scenario simulation
# ═══════════════════════════════════════════════════════════════════════════

def example_finance_leasing():
    """Nieskończone warianty leasingu + modyfikacje camper van."""
    root = FraqNode(position=(0.0, 0.0, 0.0), seed=150000)
    schema = FraqSchema(root=root)
    schema.add_field("monthly_rate", "float", transform=lambda v: round(v * 5000, 2))
    schema.add_field("total_cost", "float", transform=lambda v: round(v * 200000, 2))
    schema.add_field("mods_included", "bool")
    schema.add_field("scenario_id", "str")

    print("=== Finance: Leasing scenarios ===")
    for rec in schema.records(depth=2, branching=3):
        mods = "WITH mods" if rec["mods_included"] else "base"
        print(f"  {rec['scenario_id']} | monthly: {rec['monthly_rate']:>8.2f} PLN | "
              f"total: {rec['total_cost']:>10.2f} PLN | {mods}")
    print()


# ═══════════════════════════════════════════════════════════════════════════
# 6. LEGAL — Document clause generation
# ═══════════════════════════════════════════════════════════════════════════

def example_legal_clauses():
    """Nieskończone klauzule umów — każdy zoom = nowy poziom detali."""
    root = FraqNode(position=(0.0, 0.0, 0.0), seed=42)
    schema = FraqSchema(root=root)
    schema.add_field("clause_id", "str")
    schema.add_field("weight", "float", transform=lambda v: round(v, 3))
    schema.add_field("binding", "bool")

    print("=== Legal: Contract clauses (depth 2) ===")
    for rec in schema.records(depth=2, branching=3):
        binding = "BINDING" if rec["binding"] else "advisory"
        print(f"  §{rec['clause_id']} | weight: {rec['weight']} | {binding}")
    print()


# ═══════════════════════════════════════════════════════════════════════════
# 7. SMOOTH DATA — Perlin noise for organic patterns
# ═══════════════════════════════════════════════════════════════════════════

def example_perlin_organic():
    """Smooth data z PerlinGenerator — organic sensor patterns."""
    gen = PerlinGenerator(frequency=2.0, amplitude=10.0)
    root = FraqNode(position=(0.0,), generator=gen)

    print("=== Perlin: Organic sensor pattern ===")
    cursor = FraqCursor(root=root)
    for i in range(15):
        cursor.advance()
        val = cursor.current.value
        bar = "█" * max(0, int((val + 10) * 2))
        print(f"  t={i:>2} | {val:>6.2f} | {bar}")
    print()


# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    example_iot_sensor_network()
    example_erp_invoices()
    example_ai_training_data()
    example_devops_load_test()
    example_finance_leasing()
    example_legal_clauses()
    example_perlin_organic()
