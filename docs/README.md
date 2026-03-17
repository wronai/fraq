<!-- code2docs:start --># fraq

![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-%3E%3D3.10-blue) ![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey) ![functions](https://img.shields.io/badge/functions-348-green)
> **348** functions | **46** classes | **54** files | CC̄ = 2.8

> Auto-generated project documentation from source code analysis.

**Author:** Softreck / Prototypowanie.pl  
**License:** Apache-2.0[(LICENSE)](./LICENSE)  
**Repository:** [https://github.com/wronai/fraq](https://github.com/wronai/fraq)

## Installation

### From PyPI

```bash
pip install fraq
```

### From Source

```bash
git clone https://github.com/wronai/fraq
cd fraq
pip install -e .
```

### Optional Extras

```bash
pip install fraq[http]    # http features
pip install fraq[async]    # async features
pip install fraq[fast]    # fast features
pip install fraq[ai]    # ai features
pip install fraq[all]    # all optional features
pip install fraq[dev]    # development tools
```

## Quick Start

### CLI Usage

```bash
# Generate full documentation for your project
fraq ./my-project

# Only regenerate README
fraq ./my-project --readme-only

# Preview what would be generated (no file writes)
fraq ./my-project --dry-run

# Check documentation health
fraq check ./my-project

# Sync — regenerate only changed modules
fraq sync ./my-project
```

### Python API

```python
from fraq import generate_readme, generate_docs, Code2DocsConfig

# Quick: generate README
generate_readme("./my-project")

# Full: generate all documentation
config = Code2DocsConfig(project_name="mylib", verbose=True)
docs = generate_docs("./my-project", config=config)
```

## Generated Output

When you run `fraq`, the following files are produced:

```
<project>/
├── README.md                 # Main project README (auto-generated sections)
├── docs/
│   ├── api.md               # Consolidated API reference
│   ├── modules.md           # Module documentation with metrics
│   ├── architecture.md      # Architecture overview with diagrams
│   ├── dependency-graph.md  # Module dependency graphs
│   ├── coverage.md          # Docstring coverage report
│   ├── getting-started.md   # Getting started guide
│   ├── configuration.md    # Configuration reference
│   └── api-changelog.md    # API change tracking
├── examples/
│   ├── quickstart.py       # Basic usage examples
│   └── advanced_usage.py   # Advanced usage examples
├── CONTRIBUTING.md         # Contribution guidelines
└── mkdocs.yml             # MkDocs site configuration
```

## Configuration

Create `fraq.yaml` in your project root (or run `fraq init`):

```yaml
project:
  name: my-project
  source: ./
  output: ./docs/

readme:
  sections:
    - overview
    - install
    - quickstart
    - api
    - structure
  badges:
    - version
    - python
    - coverage
  sync_markers: true

docs:
  api_reference: true
  module_docs: true
  architecture: true
  changelog: true

examples:
  auto_generate: true
  from_entry_points: true

sync:
  strategy: markers    # markers | full | git-diff
  watch: false
  ignore:
    - "tests/"
    - "__pycache__"
```

## Sync Markers

fraq can update only specific sections of an existing README using HTML comment markers:

```markdown
<!-- fraq:start -->
# Project Title
... auto-generated content ...
<!-- fraq:end -->
```

Content outside the markers is preserved when regenerating. Enable this with `sync_markers: true` in your configuration.

## Architecture

```
fraq/
├── main_websocket    ├── formats    ├── streaming├── fraq/    ├── generators    ├── cli    ├── schema_export    ├── adapters/    ├── applications    ├── async_streaming    ├── query_examples    ├── network_web_examples    ├── app_integrations    ├── text2fraq_examples    ├── nlp2cmd_integration    ├── api_server    ├── text2fraq_files        ├── run        ├── main        ├── run        ├── run        ├── run        ├── main            ├── app            ├── main            ├── main        ├── config        ├── file_search_parser    ├── core    ├── text2fraq        ├── parser_rules        ├── parser_llm    ├── query        ├── shortcuts        ├── base        ├── registry        ├── file_adapter        ├── web_crawler        ├── http_adapter        ├── sql_adapter        ├── sensor_adapter        ├── hybrid_adapter        ├── file_search        ├── network├── project    ├── bash_examples        ├── models        ├── llm_client```

## API Overview

### Classes

- **`FormatRegistry`** — Registry of serialisation backends.
- **`AsyncFraqStream`** — Async generator that yields fractal records at a controlled rate.
- **`HashGenerator`** — Deterministic pseudo-random values via SHA-256.
- **`FibonacciGenerator`** — Value based on generalised Fibonacci sequence at the node's depth.
- **`PerlinGenerator`** — Simplified 1-D Perlin-ish noise from the L2 norm of position.
- **`SensorStreamGenerator`** — Simulate an infinite IoT sensor stream.
- **`BaseAdapter`** — Interface every data-source adapter must implement.
- **`FileAdapter`** — Read/write fractal state from local files.
- **`HTTPAdapter`** — Fetch fractal roots from remote HTTP APIs and push results back.
- **`SQLAdapter`** — Map fractal nodes to/from relational tables.
- **`SensorAdapter`** — Simulate or consume live sensor data as fractal streams.
- **`FileSearchAdapter`** — Adapter for searching files on disk using fractal patterns.
- **`NetworkAdapter`** — Async adapter for scanning local network devices and services.
- **`WebCrawlerAdapter`** — Async adapter for crawling websites and extracting links/content.
- **`HybridAdapter`** — Combine roots from several adapters into one fractal.
- **`Text2FraqConfig`** — Configuration for text2fraq.
- **`FileSearchText2Fraq`** — Natural language to file search converter.
- **`FraqNode`** — A single point in the infinite fractal data space.
- **`FieldDef`** — One field in a FraqSchema.
- **`FraqSchema`** — Typed projection of a fractal into structured records.
- **`FraqCursor`** — Stateful walk through the fractal.
- **`Text2FraqSimple`** — Rule-based text2fraq without LLM (fallback for offline use).
- **`Text2Fraq`** — Natural language to fractal query converter (LLM-based).
- **`SourceType`** — Known data source families.
- **`FraqFilter`** — Post-zoom predicate on a record field.
- **`FraqQuery`** — Declarative query against fractal data.
- **`FraqExecutor`** — Execute a FraqQuery against a root node.
- **`BaseAdapter`** — Interface every data-source adapter must implement.
- **`FileAdapter`** — Read/write fractal state from local files.
- **`WebCrawlerAdapter`** — Async adapter for crawling websites and extracting links/content.
- **`HTTPAdapter`** — Fetch fractal roots from remote HTTP APIs.
- **`SQLAdapter`** — Map fractal nodes to/from relational tables.
- **`SensorAdapter`** — Simulate or consume live sensor data as fractal streams.
- **`HybridAdapter`** — Combine roots from several adapters into one fractal.
- **`FileSearchAdapter`** — Adapter for searching files on disk using fractal patterns.
- **`NetworkAdapter`** — Async adapter for scanning local network devices and services.
- **`ParsedQuery`** — Parsed natural language query.
- **`LLMClient`** — Protocol for LLM clients.
- **`LiteLLMClient`** — LiteLLM client for text completion.
- **`Text2FraqConfig`** — Configuration for text2fraq.
- **`ParsedQuery`** — Parsed natural language query.
- **`LLMClient`** — Protocol for LLM clients.
- **`LiteLLMClient`** — LiteLLM client for text completion.
- **`FileSearchText2Fraq`** — Natural language to file search converter.
- **`Text2Fraq`** — Natural language to fractal query converter.
- **`Text2FraqSimple`** — Rule-based text2fraq without LLM (fallback for offline use).

### Functions

- `ws_stream(websocket)` — —
- `ws_files(websocket)` — —
- `health()` — —
- `async_query(query, root, dims)` — Run a FraqQuery asynchronously (useful in async frameworks).
- `async_stream(root, count, interval, direction)` — Convenience async generator with a count limit.
- `cmd_explore(args)` — —
- `cmd_stream(args)` — —
- `cmd_schema(args)` — —
- `cmd_files_search(args)` — Search files with natural language or explicit parameters.
- `cmd_files_list(args)` — List files in directory (ls-like).
- `cmd_files_stat(args)` — Show file statistics with fractal coordinates.
- `cmd_nl(args)` — Natural language query (requires LLM).
- `cmd_network_scan(args)` — Scan network for devices.
- `cmd_web_crawl(args)` — Crawl website.
- `main(argv)` — —
- `to_nlp2cmd_schema(schema, command_name, version, category)` — Export a FraqSchema as an NLP2CMD command schema.
- `to_nlp2cmd_actions(schema)` — Export fraq operations as NLP2CMD ActionRegistry entries.
- `to_openapi(schema, title, version, base_path)` — Generate an OpenAPI 3.0 specification.
- `to_graphql(schema, type_name)` — Generate a GraphQL schema definition.
- `to_asyncapi(schema, title, version)` — Generate an AsyncAPI 3.0 specification for streaming channels.
- `to_proto(schema, package, message_name)` — Generate a .proto file.
- `to_json_schema(schema, title)` — Generate a JSON Schema for validation.
- `get_adapter(source)` — Factory: return the right adapter for a source type.
- `example_iot_sensor_network()` — Symulacja 10k sensorów bez storage'u — dla firmware dev na RPi/ESP32.
- `example_erp_invoices()` — Dynamiczne faktury z nieskończonymi detalami.
- `example_ai_training_data()` — Nieskończone datasety treningowe — zero disk, perfect dla federated learning.
- `example_devops_load_test()` — Generuj test payloads dla K8s load testing.
- `example_finance_leasing()` — Nieskończone warianty leasingu + modyfikacje camper van.
- `example_legal_clauses()` — Nieskończone klauzule umów — każdy zoom = nowy poziom detali.
- `example_perlin_organic()` — Smooth data z PerlinGenerator — organic sensor patterns.
- `example_basic_stream()` — Prosty async stream — 10 rekordów.
- `example_typed_stream()` — Stream z typowanym schematem.
- `example_async_query()` — Async query — offloaded do thread pool.
- `example_fastapi_sse_pattern()` — Wzorzec dla FastAPI SSE endpoint:
- `example_kafka_producer_pattern()` — Wzorzec dla Kafka / NATS producer:
- `main()` — —
- `example_disk_json()` — Query na lokalnym pliku JSON.
- `example_disk_csv()` — Eksport do CSV — dla ERP / accounting workflows.
- `example_disk_yaml()` — YAML output — dla Kubernetes configs / IoT dashboards.
- `example_http_api()` — Query zdalne API — z fallbackiem na deterministyczny root.
- `example_sql_query()` — Query z mapowaniem SQL rows → fractal nodes.
- `example_sql_custom_mapping()` — Custom row→node mapping dla geolokalizacji.
- `example_sensor_stream()` — Nieskończony sensor stream — deterministyczny, zero storage.
- `example_sensor_to_formats()` — Sensor data → różne formaty eksportu.
- `example_hybrid_merge()` — Merge wielu źródeł w jeden fractal.
- `example_oneliners()` — Szybkie query bez budowania obiektów.
- `example_network_scan_sync()` — Przykład 1: Synchroniczne skanowanie sieci
- `example_network_scan_async()` — Przykład 2: Asynchroniczne skanowanie ze streamingiem
- `example_web_crawl_sync()` — Przykład 3: Synchroniczny crawling strony
- `example_web_crawl_async()` — Przykład 4: Asynchroniczne crawlowanie ze streamingiem
- `example_fractal_coordinates()` — Przykład 5: Fraktalne koordynaty dla sieci i web
- `example_streaming_comparison()` — Przykład 6: Porównanie streaming vs batch
- `main()` — Uruchom wszystkie przykłady
- `example_fastapi_app()` — FastAPI application with fraq endpoints.
- `example_streamlit_app()` — Streamlit dashboard for fraq visualization.
- `example_flask_app()` — Flask application with fraq blueprints.
- `example_cli_chat()` — Interactive CLI chatbot with fraq + text2fraq.
- `example_websocket_server()` — WebSocket server for real-time fraq streaming.
- `example_kafka_producer()` — Kafka producer/consumer with fraq streams.
- `example_grpc_service()` — gRPC service definition and implementation.
- `example_jupyter_notebook()` — Jupyter notebook cells for interactive exploration.
- `example_celery_task()` — Celery background tasks for fraq processing.
- `example_simple_parser()` — Rule-based parser — zero dependencies, works offline.
- `example_qwen25()` — qwen2.5:3b — good balance for Polish/English prompts.
- `example_llama32()` — llama3.2:3b — alternative lightweight model.
- `example_phi3()` — phi3:3.8b — stronger reasoning-oriented option.
- `example_convenience_functions()` — One-liner functions — simplest possible API.
- `example_file_search_direct()` — FileSearchAdapter — search real files on disk.
- `example_env_config()` — Load config from .env file.
- `example_full_pipeline()` — Full pipeline NL → parse → execute / file search.
- `build_sensor_schema()` — Schemat IoT sensorów — bazowy przykład.
- `build_erp_schema()` — Schemat ERP / accounting.
- `example_nlp2cmd_command_schema()` — Generuj NLP2CMD command schema → command_schemas/fraq_sensor.json
- `example_nlp2cmd_actions()` — Generuj ActionRegistry entries dla NLP2CMD.
- `example_nlp2cmd_erp()` — ERP schema dla NLP2CMD — business automation.
- `example_openapi()` — OpenAPI 3.0 — dla FastAPI / REST endpoints.
- `example_graphql()` — GraphQL — dla złożonych relacyjnych query.
- `example_asyncapi()` — AsyncAPI 3.0 — dla Kafka / WebSocket / NATS streaming.
- `example_grpc_proto()` — gRPC / Protobuf — high-performance dla edge computing.
- `example_json_schema()` — JSON Schema — walidacja rekordów.
- `example_full_nlp2cmd_workflow()` — Pełny workflow: FraqSchema → NLP2CMD SchemaRegistry → Natural Language → Command.
- `lifespan(app)` — App lifespan manager.
- `root()` — API info.
- `health()` — Health check.
- `explore(depth, dims, seed, format)` — Zoom into fractal at given depth.
- `stream(count, dims, format)` — Stream cursor records.
- `query_data(fields, depth, format, limit)` — Execute fractal query with typed fields.
- `schema_records(fields, depth, branching, format)` — Generate typed schema records.
- `files_search(path, ext, pattern, limit)` — Search files with fractal metadata.
- `files_list(path, ext, limit, sort)` — List files (ls-style).
- `files_stat(file_path)` — Get file statistics with fractal coordinates.
- `natural_language(query, path, format)` — Process natural language query (requires LLM).
- `ws_stream(websocket)` — WebSocket streaming of fractal data.
- `ws_files(websocket)` — WebSocket for file search streaming.
- `example_pdf_search_rule_based()` — Wyszukiwanie PDF bez LLM - rule based.
- `example_pdf_search_with_llm()` — Wyszukiwanie PDF z użyciem LLM (qwen2.5).
- `example_convenience_function()` — Użycie funkcji text2filesearch.
- `example_file_search_adapter_direct()` — Bezpośrednie użycie FileSearchAdapter.
- `example_llm_file_intent()` — Rozpoznawanie intencji plikowych przez LLM.
- `run_docker()` — Uruchom przez Docker
- `stop_docker()` — Zatrzymaj Docker
- `run_local()` — Uruchom lokalnie
- `test_websocket()` — Przetestuj WebSocket
- `main()` — —
- `ws_stream(websocket)` — Stream fractal data
- `ws_files(websocket)` — Stream file search results
- `health()` — —
- `run_in_docker(args_list)` — Uruchom fraq CLI w Docker
- `run_local(args_list)` — Uruchom fraq CLI lokalnie
- `main()` — —
- `run_docker()` — Uruchom przez Docker Compose
- `stop_docker()` — Zatrzymaj stack
- `test_stack()` — Przetestuj stack
- `main()` — —
- `run_local()` — Uruchom serwer lokalnie (bez Docker)
- `run_docker()` — Uruchom przez Docker
- `stop_docker()` — Zatrzymaj Docker
- `test_api()` — Przetestuj API
- `main()` — —
- `root()` — —
- `health()` — —
- `explore(depth, dims, format)` — Explore fractal structure
- `files_search(path, ext, limit, sort)` — Search files with fractal metadata
- `files_stat(file_path)` — Get file statistics with fractal coordinates
- `ws_stream(websocket)` — —
- `ws_files(websocket)` — —
- `health()` — —
- `root()` — —
- `health()` — —
- `explore(depth)` — —
- `files_search(path, ext, limit)` — —
- `query(depth, direction, fields, format)` — One-shot fractal query.
- `text2filesearch(text, base_path, fmt)` — One-liner to search files via natural language.
- `text2query(text, config)` — Convert text to ParsedQuery.
- `text2fraq(text, config, root)` — Convert text and execute query.
- `get_adapter(source)` — Factory: return the right adapter for a source type.
- `text2filesearch(text, base_path, fmt)` — One-liner to search files via natural language.
- `text2query(text, config)` — Convert text to ParsedQuery.
- `text2fraq(text, config, root)` — Convert text and execute query.


## Project Structure

📄 `examples.api_server` (13 functions)
📄 `examples.app_integrations` (9 functions)
📄 `examples.applications` (7 functions)
📄 `examples.async_streaming` (6 functions)
📄 `examples.bash_examples`
📄 `examples.cli-docker.run`
📄 `examples.fastapi-docker.main` (5 functions)
📄 `examples.fastapi-docker.run`
📄 `examples.fullstack-docker.api.main` (4 functions)
📄 `examples.fullstack-docker.frontend.app`
📄 `examples.fullstack-docker.run`
📄 `examples.fullstack-docker.websocket.main` (3 functions)
📄 `examples.network_web_examples` (7 functions)
📄 `examples.nlp2cmd_integration` (11 functions)
📄 `examples.query_examples` (10 functions)
📄 `examples.text2fraq_examples` (11 functions)
📄 `examples.text2fraq_files` (5 functions)
📄 `examples.websocket-docker.main` (3 functions)
📄 `examples.websocket-docker.run`
📦 `fraq`
📦 `fraq.adapters`
📄 `fraq.adapters.base` (4 functions, 1 classes)
📄 `fraq.adapters.file_adapter` (3 functions, 1 classes)
📄 `fraq.adapters.file_search` (5 functions, 1 classes)
📄 `fraq.adapters.http_adapter` (2 functions, 1 classes)
📄 `fraq.adapters.hybrid_adapter` (4 functions, 1 classes)
📄 `fraq.adapters.network` (9 functions, 1 classes)
📄 `fraq.adapters.registry` (1 functions)
📄 `fraq.adapters.sensor_adapter` (4 functions, 1 classes)
📄 `fraq.adapters.sql_adapter` (5 functions, 1 classes)
📄 `fraq.adapters.web_crawler` (10 functions, 1 classes)
📄 `fraq.cli` (14 functions)
📄 `fraq.core` (17 functions, 4 classes)
📄 `fraq.formats` (14 functions, 1 classes)
📄 `fraq.generators` (9 functions, 4 classes)
📄 `fraq.query` (12 functions, 4 classes)
📄 `fraq.schema_export` (7 functions)
📄 `fraq.streaming` (5 functions, 1 classes)
📄 `fraq.text2fraq` (31 functions, 7 classes)
📄 `fraq.text2fraq.config` (1 functions, 1 classes)
📄 `fraq.text2fraq.file_search_parser` (8 functions, 1 classes)
📄 `fraq.text2fraq.llm_client` (2 functions, 1 classes)
📄 `fraq.text2fraq.models` (2 functions, 2 classes)
📄 `fraq.text2fraq.parser_llm` (7 functions, 1 classes)
📄 `fraq.text2fraq.parser_rules` (8 functions, 1 classes)
📄 `fraq.text2fraq.shortcuts` (3 functions)
📄 `main_websocket` (3 functions)
📄 `project`

## Requirements

- Python >= >=3.10


## Contributing

**Contributors:**
- Tom Sapletta

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/wronai/fraq
cd fraq

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Documentation

- 📖 [Full Documentation](https://github.com/wronai/fraq/tree/main/docs) — API reference, module docs, architecture
- 🚀 [Getting Started](https://github.com/wronai/fraq/blob/main/docs/getting-started.md) — Quick start guide
- 📚 [API Reference](https://github.com/wronai/fraq/blob/main/docs/api.md) — Complete API documentation
- 🔧 [Configuration](https://github.com/wronai/fraq/blob/main/docs/configuration.md) — Configuration options
- 💡 [Examples](./examples) — Usage examples and code samples

### Generated Files

| Output | Description | Link |
|--------|-------------|------|
| `README.md` | Project overview (this file) | — |
| `docs/api.md` | Consolidated API reference | [View](./docs/api.md) |
| `docs/modules.md` | Module reference with metrics | [View](./docs/modules.md) |
| `docs/architecture.md` | Architecture with diagrams | [View](./docs/architecture.md) |
| `docs/dependency-graph.md` | Dependency graphs | [View](./docs/dependency-graph.md) |
| `docs/coverage.md` | Docstring coverage report | [View](./docs/coverage.md) |
| `docs/getting-started.md` | Getting started guide | [View](./docs/getting-started.md) |
| `docs/configuration.md` | Configuration reference | [View](./docs/configuration.md) |
| `docs/api-changelog.md` | API change tracking | [View](./docs/api-changelog.md) |
| `CONTRIBUTING.md` | Contribution guidelines | [View](./CONTRIBUTING.md) |
| `examples/` | Usage examples | [Browse](./examples) |
| `mkdocs.yml` | MkDocs configuration | — |

<!-- code2docs:end -->