# Changelog

## [Unreleased]

## [0.2.11] - 2026-03-17

### Docs
- Update README.md
- Update docs/README.md
- Update examples/README.md
- Update project/README.md

### Other
- Update examples/ai_ml/training_data.py
- Update examples/bash_examples.sh
- Update examples/database/sqlite_examples.py
- Update examples/etl/pipeline_examples.py
- Update examples/iot/sensor_examples.py
- Update examples/streaming/sse_examples.py
- Update examples/testing/test_fixtures.py
- Update examples/v028/new_features.py
- Update project/analysis.toon
- Update project/calls.mmd
- ... and 11 more files

## [0.2.10] - 2026-03-17

### Other
- Update examples/testing/test_fixtures.py

## [0.2.9] - 2026-03-17

### Docs
- Update CHANGELOG.md
- Update README.md
- Update docs/README.md

### Other
- Update examples/v028/new_features_v030.py
- Update fraq/server.py
- Update project/analysis.toon
- Update project/calls.mmd
- Update project/compact_flow.mmd
- Update project/dashboard.html
- Update project/flow.mmd
- Update project/flow.png
- Update project/flow.toon
- Update project/map.toon
- ... and 1 more files

## [0.2.8] - 2026-03-17

### Added
- **ModelRouter** - Intelligent model selection based on query complexity (`fraq.text2fraq.router`)
- **FraqSession** - Multi-turn conversations with context memory (`fraq.text2fraq.session`)
- **FastAPI Server** - Production-ready API with WebSocket streaming (`fraq.server`)
- **Hub Types** - NewType aliases for type clarity (`fraq.types`)
- **Examples v028** - New features demonstration

### Changed
- **CLI Refactoring** - Reduced CC in main() from 13 to 4 using Command Registry pattern
- **Adapters Refactoring** - Extracted pure functions from FileSearchAdapter, WebCrawlerAdapter, NetworkAdapter
- **Fan-out Reduction** - cmd_files_stat() split into _collect_file_stat() and _print_stat()
- **Lazy Loading** - Circular dependencies broken via __getattr__ in __init__.py

### Removed
- **11 Duplicate Classes** - Removed fraq/adapters.py and fraq/text2fraq.py monoliths

### Fixed
- **Bug** - FileSearchText2Fraq.search() now properly uses injected adapter

## [0.2.7] - 2026-03-17

### Docs
- Update docs/README.md
- Update project/README.md
- Update project/context.md

### Test
- Update tests/test_new_features.py

### Other
- Update examples/basic/app_integrations.py
- Update examples/basic/applications.py
- Update examples/basic/async_streaming.py
- Update examples/basic/query_examples.py
- Update examples/cli-docker/bash_examples.sh
- Update examples/fastapi-docker/api_server.py
- Update examples/network/network_web_examples.py
- Update examples/text2fraq/nlp2cmd_integration.py
- Update examples/text2fraq/text2fraq_examples.py
- Update examples/text2fraq/text2fraq_files.py
- ... and 19 more files

## [0.2.6] - 2026-03-17

### Docs
- Update docs/README.md
- Update project/README.md
- Update project/context.md

### Test
- Update tests/test_text2fraq.py

### Other
- Update fraq/adapters/__init__.py
- Update fraq/adapters/base.py
- Update fraq/adapters/file_adapter.py
- Update fraq/adapters/file_search.py
- Update fraq/adapters/http_adapter.py
- Update fraq/adapters/hybrid_adapter.py
- Update fraq/adapters/network.py
- Update fraq/adapters/registry.py
- Update fraq/adapters/sensor_adapter.py
- Update fraq/adapters/sql_adapter.py
- ... and 23 more files

## [0.2.5] - 2026-03-17

### Docs
- Update PLAN_REFACTORING.md
- Update docs/README.md
- Update project/README.md
- Update project/context.md

### Other
- Update examples/network_web_examples.py
- Update examples/text2fraq_examples.py
- Update fraq/__init__.py
- Update fraq/adapters.py
- Update fraq/cli.py
- Update fraq/query.py
- Update project/analysis.toon
- Update project/calls.mmd
- Update project/calls.png
- Update project/compact_flow.mmd
- ... and 10 more files

## [0.2.4] - 2026-03-17

### Docs
- Update README.md
- Update docs/README.md
- Update examples/README.md
- Update examples/cli-docker/README.md
- Update examples/fastapi-docker/README.md
- Update examples/websocket-docker/README.md
- Update project/README.md
- Update project/context.md

### Test
- Update tests/test_text2fraq.py

### Other
- Update examples/cli-docker/run.py
- Update examples/cli-docker/run.sh
- Update examples/fastapi-docker/run.sh
- Update examples/fullstack-docker/run.py
- Update examples/fullstack-docker/run.sh
- Update examples/websocket-docker/run.py
- Update examples/websocket-docker/run.sh
- Update fraq/cli.py
- Update fraq/text2fraq.py
- Update project/analysis.toon
- ... and 11 more files

## [0.2.3] - 2026-03-17

### Docs
- Update docs/README.md
- Update examples/cli-docker/README.md
- Update examples/fastapi-docker/README.md
- Update examples/fullstack-docker/README.md
- Update examples/websocket-docker/README.md
- Update project/context.md

### Other
- Update Dockerfile.cli
- Update Dockerfile.websocket
- Update examples/cli-docker/Dockerfile
- Update examples/cli-docker/docker-compose.yml
- Update examples/cli-docker/run.sh
- Update examples/fastapi-docker/Dockerfile
- Update examples/fastapi-docker/docker-compose.yml
- Update examples/fastapi-docker/main.py
- Update examples/fastapi-docker/run.py
- Update examples/fastapi-docker/run.sh
- ... and 21 more files

## [0.2.2] - 2026-03-17

### Docs
- Update README.md
- Update docs/README.md
- Update examples/CLI_CURL_GUIDE.md
- Update project/README.md
- Update project/context.md

### Test
- Update tests/test_text2fraq.py

### Other
- Update examples/api_server.py
- Update examples/bash_examples.sh
- Update examples/text2fraq_files.py
- Update fraq/__init__.py
- Update fraq/adapters.py
- Update fraq/cli.py
- Update fraq/text2fraq.py
- Update project/analysis.toon
- Update project/calls.mmd
- Update project/calls.png
- ... and 11 more files

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
