# fraq — Fractal Query Data Library

> Model data as infinite, self-similar fractal structures in hyperspace.
> Each zoom level reveals procedurally generated detail — data exists only
> virtually and materialises on demand via lazy evaluation.

## Core Idea

Imagine a schema that is itself an **infinite fractal**. You can zoom into
any region and receive an unbounded amount of deterministic data in any
format you choose (JSON, CSV, YAML, binary).  The data doesn't live in
memory or on disk — it is *generated* on the fly from the fractal
coordinates and a deterministic seed.

```
root (depth 0)
 ├── zoom (1,0,0) → child A (depth 1)
 │    ├── zoom (1,0,0) → grandchild AA (depth 2) …
 │    └── zoom (0,1,0) → grandchild AB (depth 2) …
 └── zoom (0,0,1) → child B (depth 1)
      └── … infinite …
```

### Key Properties

| Property | Description |
|---|---|
| **Deterministic** | Same path → same data, always |
| **Lazy** | Nodes materialise only when accessed |
| **Unbounded** | No depth limit — zoom forever |
| **Format-agnostic** | JSON, CSV, YAML, binary, msgpack-lite, or register your own |
| **Source-agnostic** | File, HTTP, SQL, Sensor, Hybrid — same query interface |
| **Schema-exportable** | NLP2CMD, OpenAPI, GraphQL, AsyncAPI, gRPC, JSON Schema |
| **Zero storage** | Data exists only as computation |

## Quick Start

```bash
pip install -e ".[dev]"

# CLI
fraq explore --dims 3 --depth 5 --format json
fraq stream  --dims 2 --count 20 --format csv
fraq schema  --fields "name:str,value:float,flag:bool" --depth 2

# Docker
docker compose run test          # run full test suite
docker compose run cli explore --depth 5
```

## Python API

```python
from fraq import FraqNode, FraqSchema, FraqCursor, FormatRegistry, query

# 1. One-liner query
data = query(depth=2, fields=["temp:float", "id:str"], format="csv", limit=10)

# 2. Fluent query builder
from fraq import FraqQuery, FraqExecutor

q = (
    FraqQuery()
    .zoom(5, direction=(0.1, 0.2, 0.7))
    .select("temperature:float", "sensor_id:str", "active:bool")
    .where("temperature", "gt", 0.5)
    .output("json")
    .take(20)
)
result = FraqExecutor(dims=3).execute(q)

# 3. Source adapters — same query, different sources
from fraq import FileAdapter, SQLAdapter, SensorAdapter, HybridAdapter

# Disk
adapter = FileAdapter()
root = adapter.load_root("gradient_root.json")

# SQL
adapter = SQLAdapter(table="sensors")
root = adapter.load_root("", rows=[{"id": 1, "x": 0.0, "y": 0.0, "z": 0.0}])

# Sensors (infinite stream, zero storage)
adapter = SensorAdapter(base_temp=23.5)
for reading in adapter.stream(depth=3, count=100):
    print(reading)  # {'temperature': 24.1, 'humidity': 58.3, ...}

# Hybrid (merge multiple sources)
hybrid = HybridAdapter()
hybrid.add(FileAdapter(), "local_backup.json")
hybrid.add(SensorAdapter(), "")
merged = hybrid.load_root()

# 4. Async streaming (FastAPI SSE, Kafka, NATS)
from fraq.streaming import async_stream
async for record in async_stream(count=1000, interval=0.1):
    yield f"data: {json.dumps(record)}\n\n"
```

## NLP2CMD Integration

Export FraqSchema to NLP2CMD's SchemaRegistry for natural language → command transformation:

```python
from fraq import FraqNode, FraqSchema, to_nlp2cmd_schema, to_nlp2cmd_actions

schema = FraqSchema(root=FraqNode(position=(0.0, 0.0, 0.0)))
schema.add_field("temperature", "float")
schema.add_field("sensor_id", "str")

# Command schema → command_schemas/fraq_sensor.json
nlp2cmd_schema = to_nlp2cmd_schema(schema, command_name="fraq_sensor")

# Action registry entries
actions = to_nlp2cmd_actions(schema)
# → fraq_zoom, fraq_query, fraq_stream, fraq_save

# NLP2CMD can now transform:
#   "Show active sensors" → fraq query --fields "temperature:float,sensor_id:str" --depth 2
```

## Schema Export Formats

```python
from fraq import to_openapi, to_graphql, to_asyncapi, to_proto, to_json_schema

to_openapi(schema)     # OpenAPI 3.0 — /zoom, /query, /stream endpoints
to_graphql(schema)     # GraphQL type + Query definitions
to_asyncapi(schema)    # AsyncAPI 3.0 — Kafka/WebSocket channels
to_proto(schema)       # gRPC .proto with FraqService (Zoom + Stream RPCs)
to_json_schema(schema) # JSON Schema for validation
```

## Generators

| Generator | Output | Use Case |
|---|---|---|
| `HashGenerator` | `float` in configurable range | General-purpose pseudo-random |
| `FibonacciGenerator` | `float` based on depth | Mathematical sequences |
| `PerlinGenerator` | Smooth `float` noise | Organic sensor streams |
| `SensorStreamGenerator` | `dict` with IoT fields | Embedded / edge simulation |

## Data Source Adapters

| Adapter | Source | Key Feature |
|---|---|---|
| `FileAdapter` | JSON/YAML/CSV on disk | Save/load roundtrip |
| `HTTPAdapter` | REST APIs | Fallback to deterministic roots |
| `SQLAdapter` | PostgreSQL/SQLite | Row mapping, SQL function generation |
| `SensorAdapter` | IoT streams (RPi/ESP32) | Infinite deterministic readings |
| `HybridAdapter` | Multiple sources merged | Mean position, XOR seeds |

## text2fraq — Natural Language to Fractal Query

Convert natural language to fractal queries using LLM (LiteLLM) or rule-based fallback.

### Setup (Ollama with small models)

```bash
# Install Ollama: https://ollama.com
ollama pull qwen2.5:3b      # Fast, instruction-tuned
ollama pull llama3.2:3b     # Balanced, multilingual
ollama pull phi3:3.8b       # Strong reasoning

# Install with AI extras
pip install -e ".[ai]"

# Copy and edit config
cp .env.example .env
```

### Usage

```python
from fraq import text2fraq, Text2Fraq, Text2FraqSimple

# One-liner (auto-fallback to rule-based if LLM unavailable)
result = text2fraq("Show 20 temperature readings in CSV")

# With specific model
from fraq.text2fraq import Text2FraqConfig
t2f = Text2Fraq(Text2FraqConfig(model="qwen2.5:3b"))
parsed = t2f.parse("Get deep analysis with depth 5")

# Rule-based (deterministic, no LLM needed)
parser = Text2FraqSimple()
query = parser.parse("Stream sensor data as JSON")
```

### Environment Variables (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `LITELLM_PROVIDER` | `ollama` | LLM provider |
| `LITELLM_MODEL` | `qwen2.5:3b` | Model name |
| `LITELLM_BASE_URL` | `http://localhost:11434` | API endpoint |
| `LITELLM_TEMPERATURE` | `0.1` | Generation temperature |
| `TEXT2FRAQ_DEFAULT_FORMAT` | `json` | Default output format |
| `TEXT2FRAQ_DEFAULT_DIMS` | `3` | Default fractal dimensions |
| `TEXT2FRAQ_DEFAULT_DEPTH` | `3` | Default query depth |

## Application Integrations

See `examples/app_integrations.py` for templates:

- **FastAPI** — REST API with `/query`, `/stream` (SSE), `/zoom/{depth}`
- **Streamlit** — Interactive dashboard with sliders and charts
- **Flask** — Blueprints with NL endpoints
- **WebSocket** — Real-time streaming server
- **Kafka** — Producer/consumer with aiokafka
- **gRPC** — High-performance RPC service
- **Celery** — Background task processing
- **Jupyter** — Interactive exploration widgets

## Testing

```bash
pytest -v --cov=fraq    # 132 tests, 96% coverage
```

## Project Structure

```
fraq/
├── fraq/
│   ├── __init__.py          # public API
│   ├── core.py              # FraqNode, FraqSchema, FraqCursor
│   ├── formats.py           # FormatRegistry + 6 built-in serialisers
│   ├── generators.py        # Hash, Fibonacci, Perlin, SensorStream
│   ├── query.py             # FraqQuery, FraqExecutor, FraqFilter
│   ├── adapters.py          # File, HTTP, SQL, Sensor, Hybrid adapters
│   ├── schema_export.py     # NLP2CMD, OpenAPI, GraphQL, AsyncAPI, Proto, JSON Schema
│   ├── streaming.py         # AsyncFraqStream, async_query, async_stream
│   └── cli.py               # CLI entry point
├── tests/                   # test suite
├── examples/
│   ├── query_examples.py    # All data sources (disk, HTTP, SQL, sensor, hybrid)
│   ├── nlp2cmd_integration.py  # NLP2CMD schema workflow
│   ├── applications.py      # IoT, ERP, AI/ML, DevOps, Finance, Legal
│   ├── app_integrations.py  # FastAPI, Flask, Streamlit, Kafka, gRPC, Celery
│   ├── text2fraq_examples.py # LiteLLM + Ollama + small local model examples
│   └── async_streaming.py   # FastAPI SSE, Kafka patterns
├── .env.example             # LiteLLM and text2fraq configuration template
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Author

Created by **Tom Sapletta** - [tom@sapletta.com](mailto:tom@sapletta.com)
