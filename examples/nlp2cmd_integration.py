#!/usr/bin/env python3
"""
fraq × NLP2CMD — Schema integration examples.

Pokazuje jak wyeksportować FraqSchema do formatów kompatybilnych z:
- NLP2CMD SchemaRegistry (command schemas + actions)
- OpenAPI 3.0 (FastAPI / REST)
- GraphQL
- AsyncAPI 3.0 (Kafka / WebSocket / NATS)
- gRPC / Protocol Buffers
- JSON Schema (walidacja)

Te eksporty pozwalają NLP2CMD transformować natural language → fraq commands:
  "Pokaż temperaturę z ostatnich 100 odczytów" → fraq query --fields "temp:float" --limit 100
"""

import json
from fraq import (
    FraqNode, FraqSchema,
    to_nlp2cmd_schema, to_nlp2cmd_actions,
    to_openapi, to_graphql, to_asyncapi, to_proto, to_json_schema,
)


def build_sensor_schema() -> FraqSchema:
    """Schemat IoT sensorów — bazowy przykład."""
    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("temperature", "float")
    schema.add_field("humidity", "float")
    schema.add_field("pressure", "float")
    schema.add_field("sensor_id", "str")
    schema.add_field("active", "bool")
    return schema


def build_erp_schema() -> FraqSchema:
    """Schemat ERP / accounting."""
    root = FraqNode(position=(0.0, 0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("invoice_id", "str")
    schema.add_field("amount", "float")
    schema.add_field("vat_rate", "float")
    schema.add_field("client_id", "str")
    schema.add_field("paid", "bool")
    schema.add_field("line_items", "int")
    return schema


# ═══════════════════════════════════════════════════════════════════════════
# NLP2CMD INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════

def example_nlp2cmd_command_schema():
    """Generuj NLP2CMD command schema → command_schemas/fraq_sensor.json"""
    schema = build_sensor_schema()
    cmd_schema = to_nlp2cmd_schema(
        schema,
        command_name="fraq_sensor",
        version="1.0",
        category="iot",
    )
    print("=== NLP2CMD Command Schema ===")
    print(json.dumps(cmd_schema, indent=2)[:600])
    print("...\n")

    # NLP2CMD rozumie teraz:
    #   "Show temperature readings"   → fraq query --fields "temperature:float" --depth 1
    #   "Stream 100 sensor records"   → fraq stream --count 100
    #   "Zoom into direction [1,0,0]" → fraq zoom --depth 5 --direction "[1,0,0]"
    return cmd_schema


def example_nlp2cmd_actions():
    """Generuj ActionRegistry entries dla NLP2CMD."""
    schema = build_sensor_schema()
    actions = to_nlp2cmd_actions(schema)
    print("=== NLP2CMD Actions ===")
    for action in actions:
        params = ", ".join(p["name"] for p in action["parameters"])
        print(f"  {action['name']}({params})")
    print()
    return actions


def example_nlp2cmd_erp():
    """ERP schema dla NLP2CMD — business automation."""
    schema = build_erp_schema()
    cmd_schema = to_nlp2cmd_schema(
        schema,
        command_name="fraq_erp",
        category="business",
    )
    print("=== NLP2CMD ERP Schema ===")
    print(f"  command: {cmd_schema['command']}")
    print(f"  fields: {[p['name'] for p in cmd_schema['parameters'][:6]]}")
    print(f"  templates: {len(cmd_schema['templates'])}")
    print(f"  examples:")
    for ex in cmd_schema["examples"]:
        print(f"    NL: {ex['input']}")
        print(f"    → {ex['command']}")
    print()


# ═══════════════════════════════════════════════════════════════════════════
# STANDARD EXPORTS
# ═══════════════════════════════════════════════════════════════════════════

def example_openapi():
    """OpenAPI 3.0 — dla FastAPI / REST endpoints."""
    schema = build_sensor_schema()
    spec = to_openapi(schema, title="Fraq IoT API", base_path="/api/v1/sensors")
    print("=== OpenAPI 3.0 ===")
    print(f"  Endpoints: {list(spec['paths'].keys())}")
    print(f"  Record fields: {list(spec['components']['schemas']['FraqRecord']['properties'].keys())}")
    print(json.dumps(spec["paths"]["/api/v1/sensors/zoom"], indent=2)[:300])
    print("...\n")


def example_graphql():
    """GraphQL — dla złożonych relacyjnych query."""
    schema = build_sensor_schema()
    gql = to_graphql(schema, type_name="SensorReading")
    print("=== GraphQL Schema ===")
    print(gql)
    print()


def example_asyncapi():
    """AsyncAPI 3.0 — dla Kafka / WebSocket / NATS streaming."""
    schema = build_sensor_schema()
    spec = to_asyncapi(schema, title="Fraq Sensor Streams")
    print("=== AsyncAPI 3.0 ===")
    print(f"  Channels: {list(spec['channels'].keys())}")
    print(json.dumps(spec["channels"]["fraq/stream"], indent=2)[:300])
    print("...\n")


def example_grpc_proto():
    """gRPC / Protobuf — high-performance dla edge computing."""
    schema = build_sensor_schema()
    proto = to_proto(schema, package="iot.sensors", message_name="SensorReading")
    print("=== gRPC Proto ===")
    print(proto)
    print()


def example_json_schema():
    """JSON Schema — walidacja rekordów."""
    schema = build_sensor_schema()
    js = to_json_schema(schema, title="SensorReading")
    print("=== JSON Schema ===")
    print(json.dumps(js, indent=2))
    print()


# ═══════════════════════════════════════════════════════════════════════════
# FULL NLP2CMD INTEGRATION WORKFLOW
# ═══════════════════════════════════════════════════════════════════════════

def example_full_nlp2cmd_workflow():
    """
    Pełny workflow: FraqSchema → NLP2CMD SchemaRegistry → Natural Language → Command.

    W produkcji:
        1. Zdefiniuj FraqSchema
        2. Wyeksportuj to_nlp2cmd_schema()
        3. Zarejestruj w NLP2CMD SchemaRegistry
        4. Użytkownik pisze "Show all active sensors with temp > 25"
        5. NLP2CMD generuje: fraq query --fields "temperature:float,active:bool"
                              --depth 2 --format json
        6. fraq wykonuje query i zwraca dane
    """
    # Step 1: Schema
    sensor_schema = build_sensor_schema()

    # Step 2: Export for NLP2CMD
    nlp2cmd_schema = to_nlp2cmd_schema(sensor_schema, command_name="fraq")
    nlp2cmd_actions = to_nlp2cmd_actions(sensor_schema)

    # Step 3: Symuluj rejestrację w NLP2CMD
    print("=== Full NLP2CMD Workflow ===")
    print(f"  Registered command: {nlp2cmd_schema['command']}")
    print(f"  Registered actions: {[a['name'] for a in nlp2cmd_actions]}")
    print()

    # Step 4-5: Symuluj NL → Command
    nl_examples = [
        ("Show all active sensors with high temperature",
         'fraq query --fields "temperature:float,active:bool" --depth 2 --format json'),
        ("Stream 50 pressure readings as CSV",
         'fraq stream --count 50 --format csv --fields "pressure:float"'),
        ("Zoom into sensor cluster at depth 10",
         'fraq zoom --depth 10 --direction "[1,0,0]" --format json'),
        ("Save sensor data to database",
         'fraq save --uri "postgresql://db/sensors" --format json --source sql'),
    ]

    for nl_input, expected_cmd in nl_examples:
        print(f"  NL: \"{nl_input}\"")
        print(f"  →  {expected_cmd}")
        print()

    # Step 6: Simulate execution
    from fraq import FraqExecutor, FraqQuery
    q = FraqQuery().zoom(2).select("temperature:float", "active:bool").output("records").take(3)
    result = FraqExecutor(sensor_schema.root).execute(q)
    print(f"  Execution result: {result}")
    print()


# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    example_nlp2cmd_command_schema()
    example_nlp2cmd_actions()
    example_nlp2cmd_erp()
    example_openapi()
    example_graphql()
    example_asyncapi()
    example_grpc_proto()
    example_json_schema()
    example_full_nlp2cmd_workflow()
