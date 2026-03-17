# Changelog

## [Unreleased]

## [0.2.1] - 2026-03-17

### Docs
- Update README.md
- Update docs/README.md
- Update project/README.md
- Update project/context.md

### Other
- Update .env.example
- Update examples/app_integrations.py
- Update examples/text2fraq_examples.py
- Update fraq/__init__.py
- Update fraq/text2fraq.py
- Update project.sh
- Update project/analysis.toon
- Update project/calls.mmd
- Update project/calls.png
- Update project/compact_flow.mmd
- ... and 10 more files


All notable changes to **fraq** are documented here.

## [0.2.0] — 2026-03-16

### Added
- **Unified Query Language** (`fraq/query.py`)
  - `FraqQuery` fluent builder with `.zoom()`, `.select()`, `.where()`, `.output()`, `.take()`
  - `FraqFilter` with operators: eq, ne, gt, lt, gte, lte, contains
  - `FraqExecutor` for running queries against any root node
  - `query()` one-liner convenience function

- **Data Source Adapters** (`fraq/adapters.py`)
  - `FileAdapter` — JSON/YAML/CSV on disk with save/load roundtrip
  - `HTTPAdapter` — REST API with deterministic fallback
  - `SQLAdapter` — PostgreSQL/SQLite row mapping, SQL function generation
  - `SensorAdapter` — infinite IoT stream simulation
  - `HybridAdapter` — merge multiple sources (mean position, XOR seeds)
  - `get_adapter()` factory function

- **Schema Export** (`fraq/schema_export.py`)
  - `to_nlp2cmd_schema()` — NLP2CMD command schemas
  - `to_nlp2cmd_actions()` — NLP2CMD ActionRegistry entries
  - `to_openapi()` — OpenAPI 3.0 specification
  - `to_graphql()` — GraphQL type definitions
  - `to_asyncapi()` — AsyncAPI 3.0 for streaming channels
  - `to_proto()` — gRPC/Protobuf .proto files
  - `to_json_schema()` — JSON Schema for validation

- **Async Streaming** (`fraq/streaming.py`)
  - `AsyncFraqStream` with `async for` iteration
  - `async_query()` — async execution via thread pool
  - `async_stream()` — convenience async generator with count limit

- **Examples** (`examples/`)
  - `query_examples.py` — disk, HTTP, SQL, sensor, hybrid queries
  - `nlp2cmd_integration.py` — full NLP2CMD workflow
  - `applications.py` — IoT, ERP, AI/ML, DevOps, Finance, Legal
  - `async_streaming.py` — FastAPI SSE, Kafka patterns

### Changed
- Test suite expanded from 64 to 132 tests
- Coverage maintained at 96%

## [0.1.0] — 2026-03-16

### Added
- Core fractal structures: `FraqNode`, `FraqSchema`, `FraqCursor`
- Format registry with 6 built-in serialisers (json, jsonl, csv, yaml, binary, msgpack_lite)
- 4 generators: `HashGenerator`, `FibonacciGenerator`, `PerlinGenerator`, `SensorStreamGenerator`
- CLI with `explore`, `stream`, `schema` subcommands
- Dockerfile + docker-compose.yml
- 64 tests, 96% coverage
