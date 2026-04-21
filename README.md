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
fraq nl "show 10 pdf files created recently" --path .

# Docker
docker compose run test          # run full test suite
docker compose run cli explore --depth 5
```

## Python API

### 🆕 NEW: Simplified API (v0.2.11+)

The easiest way to use fraq — just `generate()` data with field specifications:

```python
from fraq import generate, stream, quick_schema, FraqSchema

# 1. generate() — simplest data generation
records = generate({
    'temperature': 'float:10-40',  # 10-40°C range
    'humidity': 'float:0-100',     # 0-100% range
    'sensor_id': 'str',            # auto-formatted IDs
}, count=100)
# Returns: [{'temperature': 23.5, 'humidity': 67.2, 'sensor_id': 'SEN-004572'}, ...]

# 2. stream() — lazy infinite streaming
for record in stream({'cpu': 'float:0-100'}, count=1000, interval=0.1):
    print(record)  # Process one by one

# 3. quick_schema() — auto-detect types with smart transforms
schema = quick_schema('temp', 'humidity', 'pressure')  # auto-ranges for common fields
records = list(schema.records(count=50))

# 4. FraqSchema() without root — auto-created
schema = FraqSchema()  # No need for root=FraqNode(...)
schema.add_field('value', 'float')
records = list(schema.records(count=10))  # Use count instead of depth
```

See `examples/` for complete usage patterns with the new API.

---

### 🆕 DataFrame Export (v0.2.11+)

Export directly to Polars, Pandas, or PyArrow — no manual conversion needed:

```python
from fraq import generate

# Polars DataFrame (fast, modern)
df = generate({
    'temperature': 'float:10-40',
    'sensor_id': 'str',
}, count=10000, output='polars')
# Returns: pl.DataFrame

# Pandas DataFrame (familiar API)
df = generate({
    'name': 'str',
    'value': 'float:0-100',
}, count=5000, output='pandas')
# Returns: pd.DataFrame

# PyArrow Table (columnar, zero-copy)
table = generate({
    'timestamp': 'str',
    'reading': 'float',
}, count=1000, output='arrow')
# Returns: pa.Table

# Lazy iterator for streaming
records = generate({'value': 'float'}, count=1000, output='records')
for r in records:  # Memory-efficient streaming
    process(r)
```

Install extras: `pip install fraq[polars]` or `fraq[pandas]` or `fraq[arrow]`

---

### 🆕 IFS Fractal Generator (v0.2.11+)

True **structural self-similarity** — competitors (Faker, Mimesis, SDV) cannot replicate this:

```python
from fraq import IFSGenerator, AffineTransform, create_ifs

# Organizational hierarchy with fractal structure
ifs = create_ifs("organizational", seed=42)
org_data = ifs.generate(count=1000, depth=3)
# Each level statistically similar to parent

# Custom IFS with transforms
transforms = [
    AffineTransform(scale=0.5, translation=(0.0, 0.0)),    # Department
    AffineTransform(scale=0.3, translation=(0.5, 0.0)),    # Team
    AffineTransform(scale=0.2, translation=(0.8, 0.0)),     # Individual
]
ifs = IFSGenerator(transforms, weights=[0.4, 0.35, 0.25])

# Generate hierarchical data
tree = ifs.generate_hierarchy(
    root={'name': 'HQ', 'budget': 1000000},
    branching=[3, 5, 2],  # 3 depts → 5 teams each → 2 people
    depth=3
)
```

Use cases:
- **Testing recursive algorithms** with guaranteed input structure
- **Hierarchical org data** with natural distribution
- **Network topology** simulations with repeating patterns

---

### 🆕 Faker Integration (v0.2.11+)

Realistic data (names, addresses, PESEL, NIP) in fractal structures:

```python
from fraq import generate

# Mix native fraq types with Faker providers
records = generate({
    'name': 'faker:name',              # Realistic names
    'email': 'faker:email',            # Realistic emails
    'address': 'faker:pl_PL.address', # Polish addresses
    'nip': 'faker:pl_PL.nip',          # Polish NIP
    'pesel': 'faker:pl_PL.pesel',      # Polish PESEL
    'temperature': 'float:10-40',      # Native fraq
}, count=1000)

# Locale-specific generation
records = generate({
    'name': 'faker:pl_PL.name',        # Polish: Jan Kowalski
    'company': 'faker:pl_PL.company',
}, count=100)
```

Install: `pip install fraq[faker]`

---

### 🆕 pytest Integration (v0.2.11+)

Deterministic test fixtures with fraq:

```python
# conftest.py
import pytest
from fraq.testing import fraq_fixture, fixture_factory

# Method 1: Using fraq_fixture
@pytest.fixture
def sensor_data():
    return fraq_fixture({
        'temperature': 'float:10-40',
        'humidity': 'float:0-100',
        'sensor_id': 'str',
    }, count=100, seed=42)  # Always reproducible!

# Method 2: Using decorator
@fixture_factory({
    'user_id': 'str',
    'age': 'int:18-70',
}, count=50, seed=42)
def users():
    pass  # Fixture auto-generated

# Method 3: Auto-discovered fixtures (no conftest.py needed!)
# pytest automatically provides: fraq_session, fraq_data, fraq_schema

def test_temperature_range(sensor_data):
    assert all(10 <= r['temperature'] <= 40 for r in sensor_data)
    assert len(sensor_data) == 100

def test_with_dataframe(fraq_data):
    df = fraq_data({
        'value': 'float:0-100',
    }, count=1000, output='polars')
    assert df.shape == (1000, 1)
```

Install: `pip install fraq[pytest]`
Auto-discovery: `pytest --fixtures | grep fraq`

---

### Classic API

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
from fraq import FileAdapter, SQLAdapter, SensorAdapter, HybridAdapter, FileSearchAdapter

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

# Files
files = FileSearchAdapter(base_path=".").search(extension="py", limit=5, sort_by="mtime")

# 4. Async streaming (FastAPI SSE, Kafka, NATS)
from fraq.streaming import async_stream
async for record in async_stream(count=1000, interval=0.1):
    yield f"data: {json.dumps(record)}\n\n"
```

## NLP2CMD Integration

## New in v0.2.10 — Multi-Model Router & Session Memory

```python
from fraq.text2fraq import ModelRouter, FraqSession

# Route queries to optimal model based on complexity
router = ModelRouter()
model = router.route("find pdf files")          # → 0.5b (fast)
model = router.route("generate complex schema")   # → 7b (accurate)

# Multi-turn conversations with context
session = FraqSession()
session.ask("find 10 pdf files")
session.ask("show as csv")        # follow-up: format changed
session.ask("add 20 more")          # follow-up: limit increased
```

See `examples/v028/` for detailed examples.

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
| `FileSearchAdapter` | Local filesystem | Fractal file coordinates |
| `NetworkAdapter` | LAN scanning | Async device/port discovery |
| `WebCrawlerAdapter` | Website crawling | Async page extraction |

## Architecture

fraq uses clean architecture principles with separated concerns:

### Code Organization

```
fraq/
├── core.py          # Fractal engine: FraqNode, FraqSchema, FraqCursor
├── api.py           # High-level API: generate(), stream(), quick_schema()
├── formats/         # Serialization (cycle-free structure)
│   ├── registry.py  # FormatRegistry
│   ├── prepare.py   # Data preparation (shared)
│   ├── text.py      # JSON, CSV, YAML
│   └── binary.py    # Binary, msgpack_lite
├── export/          # Schema exports: OpenAPI, GraphQL, Protobuf, AsyncAPI, JSON Schema
│   ├── openapi.py
│   ├── graphql.py
│   ├── proto.py
│   ├── asyncapi.py
│   └── json_schema.py
├── adapters/        # Data source adapters
│   ├── base.py      # BaseAdapter
│   └── file_search.py  # Port/Adapter pattern example
└── cli.py           # Command dispatcher (refactored subparsers)
```

### Design Patterns

| Pattern | Where | Benefit |
|---------|-------|---------|
| **Port/Adapter** | `FileSearchAdapter` | I/O separated from business logic, 80%+ pure functions |
| **Pipeline** | `generate()` | 3 steps: `_fields_to_schema` → `_parse_transform` → `_generate_records` |
| **Registry** | `formats/` | Dynamic format registration, no cycles |
| **Command** | `cli.py` | Subparsers split by domain (core, files, network, web) |

### Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Cyclomatic Complexity (avg) | ≤ 2.5 | In progress |
| Circular dependencies | 0 | ✅ Achieved (formats/) |
| Pure functions in adapters | ≥ 80% | ✅ Achieved (FileSearchAdapter) |
| Test coverage | ≥ 95% | ✅ 96% (159 tests) |

## New Features (v0.3.0)

### 🎭 Faker Integration - Realistic Data

Generate real-world data (names, addresses, PESEL, NIP) using Faker:

```bash
pip install fraq[faker]
```

```python
from fraq import generate

records = generate({
    'name': 'faker:pl_PL.name',      # Polish names
    'nip': 'faker:pl_PL.nip',         # Polish NIP
    'email': 'faker:email',
    'age': 'int:18-70',
}, count=1000, seed=42)
```

### 📊 DataFrame Export

Direct export to Polars, Pandas, or PyArrow:

```bash
pip install fraq[polars]  # or [pandas] or [arrow]
```

```python
from fraq.dataframes import to_polars, to_pandas

# Polars DataFrame
df = to_polars({
    'sensor_id': 'str',
    'temperature': 'float:10-40',
    'humidity': 'float:0-100',
}, count=10000)

# Pandas DataFrame
df = to_pandas({...}, count=1000)
```

### 🧪 pytest Fixtures

Deterministic test data generation:

```python
# conftest.py
from fraq.testing import fraq_fixture

@pytest.fixture
def users():
    return fraq_fixture({
        'user_id': 'str',
        'age': 'int:18-70',
        'active': 'bool',
    }, count=50, seed=42)

# test_users.py
def test_user_count(users):
    assert len(users) == 50
    assert all(18 <= u['age'] <= 70 for u in users)
```

### 🌀 IFS Generator - True Fractal Data

**Competitors cannot replicate this!** Generate data with structural self-similarity:

```python
from fraq.ifs import create_ifs, OrganizationalMapper

# Create organizational hierarchy with fractal structure
ifs = create_ifs('organizational', seed=42)

data = ifs.generate(
    count=1000,
    depth=3,
    mapper=OrganizationalMapper(),
)

# Each level has statistically similar structure to parent
```

### 🔍 Fractal Schema Inference

Analyze real data → create fractal schema → generate infinite synthetic data:

```python
from fraq.inference import infer_fractal
import pandas as pd

# Load real data
df = pd.read_csv('sales_data.csv')

# Infer fractal schema (no ML training needed!)
schema = infer_fractal(df.to_dict('records'))

# Generate synthetic data with same structure
synthetic = schema.generate(count=100000)
```

**Advantages over SDV:**
- ✅ No GPU required
- ✅ Deterministic (same input → same output)
- ✅ 1000x faster (no training)

### 📈 Benchmarks

Compare with competitors:

```bash
python -m fraq.benchmarks
```

Results:
```
Speed: fraq_stream 71,508 rec/s
Memory: fraq 139.7 MB (for 100k records)
Self-similarity: IFS > generate > Faker
```

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
pytest -v --cov=fraq    # 159 tests, 96% coverage
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
│   ├── adapters/            # File, HTTP, SQL, Sensor, Hybrid, Network, WebCrawler
│   │   ├── base.py
│   │   ├── file_adapter.py
│   │   ├── http_adapter.py
│   │   ├── sql_adapter.py
│   │   ├── sensor_adapter.py
│   │   ├── hybrid_adapter.py
│   │   ├── file_search.py
│   │   ├── network.py
│   │   ├── web_crawler.py
│   │   └── registry.py
│   ├── text2fraq/           # Natural language processing
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── llm_client.py
│   │   ├── parser_rules.py
│   │   ├── parser_llm.py
│   │   ├── router.py        # v0.2.10: ModelRouter
│   │   ├── session.py       # v0.2.10: FraqSession
│   │   └── shortcuts.py
│   ├── export/              # OpenAPI, GraphQL, Protobuf, AsyncAPI, JSON Schema
│   │   ├── openapi.py
│   │   ├── graphql.py
│   │   ├── proto.py
│   │   ├── asyncapi.py
│   │   └── json_schema.py
│   ├── schema_export.py     # Deprecation shim — re-exports from fraq.export
│   ├── streaming.py         # AsyncFraqStream, async_query, async_stream
│   ├── server.py            # v0.2.10: FastAPI production server
│   └── cli.py               # CLI entry point
├── tests/                   # 159 test suite
├── examples/
│   ├── basic/               # Core examples
│   ├── text2fraq/           # NLP examples
│   ├── network/             # Network & web crawling
│   ├── v028/                # v0.2.10 new features
│   └── *-docker/            # Docker compositions
└── .github/workflows/       # CI/CD
```

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Author

Created by **Tom Sapletta** - [tom@sapletta.com](mailto:tom@sapletta.com)
