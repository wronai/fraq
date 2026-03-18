<!-- code2docs:start --># fraq

![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-%3E%3D3.10-blue) ![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey) ![functions](https://img.shields.io/badge/functions-451-green)
> **451** functions | **60** classes | **98** files | CC̄ = 2.7

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
pip install fraq[faker]    # faker features
pip install fraq[polars]    # polars features
pip install fraq[pandas]    # pandas features
pip install fraq[arrow]    # arrow features
pip install fraq[pytest]    # pytest features
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
    ├── formats/├── main_websocket    ├── streaming    ├── dataframes    ├── cli├── fraq/    ├── benchmarks    ├── types    ├── ifs    ├── generators    ├── api    ├── query    ├── core    ├── inference/    ├── schema_export    ├── new_features_demo        ├── nlp2cmd_integration        ├── text2fraq_files        ├── run        ├── run        ├── main        ├── network_web_examples        ├── sensor_examples        ├── sse_examples        ├── new_features        ├── training_data        ├── run        ├── text2fraq_examples        ├── run        ├── pipeline_examples        ├── main        ├── sqlite_examples        ├── applications        ├── async_streaming        ├── query_examples        ├── app_integrations        ├── grpc_example        ├── api_server        ├── fastapi_example        ├── flask_example        ├── streamlit_example        ├── jupyter_example        ├── kafka_example        ├── websocket_example            ├── app        ├── cli_chat_example        ├── quickstart            ├── main        ├── advanced_usage            ├── main        ├── common    ├── export/        ├── asyncapi        ├── proto        ├── json_schema        ├── openapi        ├── graphql        ├── nlp2cmd        ├── config    ├── text2fraq/        ├── parser_rules        ├── file_search_parser        ├── router        ├── session        ├── parser_llm        ├── models        ├── shortcuts        ├── registry        ├── prepare        ├── binary    ├── providers/        ├── text        ├── faker_provider        ├── schema        ├── dimension        ├── correlation        ├── base        ├── registry        ├── hierarchy    ├── adapters/        ├── file_adapter        ├── http_adapter        ├── sql_adapter        ├── sensor_adapter        ├── hybrid_adapter├── project    ├── nlp_examples    ├── bash_examples        ├── bash_examples        ├── file_search    ├── server        ├── llm_client```

## API Overview

### Classes

- **`AsyncFraqStream`** — Async generator that yields fractal records at a controlled rate.
- **`BenchmarkResult`** — Single benchmark result.
- **`SpeedBenchmark`** — Benchmark generation speed.
- **`MemoryBenchmark`** — Benchmark memory usage - fraq's zero-storage advantage.
- **`StructuralBenchmark`** — Benchmark fractal self-similarity vs random data.
- **`AffineTransform`** — Affine transformation for IFS.
- **`ValueMapper`** — Protocol for mapping fractal coordinates to data values.
- **`IFSGenerator`** — Iterated Function System generator.
- **`OrganizationalMapper`** — Mapper for organizational hierarchy data.
- **`NetworkMapper`** — Mapper for network topology data.
- **`HashGenerator`** — Deterministic pseudo-random values via SHA-256.
- **`FibonacciGenerator`** — Value based on generalised Fibonacci sequence at the node's depth.
- **`PerlinGenerator`** — Simplified 1-D Perlin-ish noise from the L2 norm of position.
- **`SensorStreamGenerator`** — Simulate an infinite IoT sensor stream.
- **`TypeTransformRegistry`** — Registry for type transform factories. Reduces CC from 10 to ≤3.
- **`StreamConfig`** — Configuration for stream().
- **`SourceType`** — Known data source families.
- **`FraqFilter`** — Post-zoom predicate on a record field.
- **`FraqQuery`** — Declarative query against fractal data.
- **`FraqExecutor`** — Execute a FraqQuery against a root node.
- **`FraqNode`** — A single point in the infinite fractal data space.
- **`FieldDef`** — One field in a FraqSchema.
- **`FraqSchema`** — Typed projection of a fractal into structured records.
- **`FraqCursor`** — Stateful walk through the fractal.
- **`FractalDimension`** — Fractal dimension analysis result.
- **`PatternSignature`** — Detected pattern in data column.
- **`FractalAnalyzer`** — Facade delegating to specialized analyzers.
- **`InferredSchema`** — Schema inferred from real data with fractal properties.
- **`FraqChat`** — Interactive CLI for fraq operations.
- **`Text2FraqConfig`** — Configuration for text2fraq.
- **`Text2FraqSimple`** — Rule-based text2fraq without LLM (fallback for offline use).
- **`FileSearchText2Fraq`** — Natural language to file search converter.
- **`ModelRouter`** — Route queries to the best model based on complexity.
- **`FraqSession`** — Multi-turn conversation with context memory.
- **`Text2Fraq`** — Natural language to fractal query converter (LLM-based).
- **`ParsedQuery`** — Parsed natural language query.
- **`LLMClient`** — Protocol for LLM clients.
- **`FormatRegistry`** — Registry of serialisation backends.
- **`ValueProvider`** — Protocol for value providers.
- **`FakerProvider`** — Faker-based value provider for realistic data generation.
- **`ProviderRegistry`** — Registry of value providers.
- **`InferredSchema`** — Schema inferred from real data with fractal properties.
- **`FractalDimension`** — Fractal dimension analysis result.
- **`BoxCountingAnalyzer`** — Isolated box-counting fractal dimension estimator.
- **`CorrelationAnalyzer`** — Analyze self-similar correlations between columns.
- **`BaseAdapter`** — Interface every data-source adapter must implement.
- **`PatternSignature`** — Detected pattern in data column.
- **`HierarchyDetector`** — Detect hierarchical patterns in data columns.
- **`FileAdapter`** — Read/write fractal state from local files.
- **`HTTPAdapter`** — Fetch fractal roots from remote HTTP APIs.
- **`SQLAdapter`** — Map fractal nodes to/from relational tables.
- **`SensorAdapter`** — Simulate or consume live sensor data as fractal streams.
- **`HybridAdapter`** — Combine roots from several adapters into one fractal.
- **`FileSystemPort`** — Port for filesystem I/O operations.
- **`RealFileSystem`** — Real filesystem implementation of FileSystemPort.
- **`FileSearchAdapter`** — Adapter for searching files on disk using fractal patterns.
- **`NLQueryRequest`** — Natural language query request.
- **`NLQueryResponse`** — Natural language query response.
- **`FilesSearchRequest`** — File search request.
- **`LiteLLMClient`** — LiteLLM client for text completion.

### Functions

- `ws_stream(websocket)` — —
- `ws_files(websocket)` — —
- `health()` — —
- `async_query(query, root, dims)` — Run a FraqQuery asynchronously (useful in async frameworks).
- `async_stream(root, count, interval, direction)` — Convenience async generator with a count limit.
- `to_polars(fields, count, seed)` — Generate records and return as Polars DataFrame.
- `to_pandas(fields, count, seed)` — Generate records and return as Pandas DataFrame.
- `to_arrow(fields, count, seed)` — Generate records and return as PyArrow Table.
- `generate_df(fields, count, seed, output)` — Generate records with specified output format.
- `cmd_explore(args)` — —
- `cmd_stream(args)` — —
- `cmd_schema(args)` — —
- `cmd_files_search(args)` — Search files with natural language or explicit parameters.
- `cmd_files_list(args)` — List files in directory (ls-like).
- `cmd_files_stat(args)` — Show file statistics with fractal coordinates.
- `cmd_nl(args)` — Natural language query (requires LLM).
- `cmd_network_scan(args)` — Scan network for devices.
- `cmd_web_crawl(args)` — Crawl website.
- `main(argv)` — Main entry point - 4 line orchestrator: parse -> dispatch.
- `run_all_benchmarks(speed_count, memory_count)` — Run all benchmarks and return results.
- `print_summary(results)` — Print benchmark summary.
- `create_ifs(pattern, seed)` — Factory function to create pre-configured IFS generators.
- `generate(fields, count, seed, output)` — Generate records with simple field specification.
- `stream(fields, count, interval)` — Stream records lazily. Like generate() but returns iterator.
- `quick_schema()` — Create schema from simple field names. Auto-detects types.
- `query(depth, direction, fields, format)` — One-shot fractal query.
- `infer_fractal(data, min_depth, max_depth)` — Infer fractal schema from existing data.
- `to_nlp2cmd_schema(schema, command_name, version, category)` — Export a FraqSchema as an NLP2CMD command schema.
- `to_nlp2cmd_actions(schema)` — Export fraq operations as NLP2CMD ActionRegistry entries.
- `to_openapi(schema, title, version, base_path)` — Generate an OpenAPI 3.0 specification.
- `to_graphql(schema, type_name)` — Generate a GraphQL schema definition.
- `to_asyncapi(schema, title, version)` — Generate an AsyncAPI 3.0 specification for streaming channels.
- `to_proto(schema, package, message_name)` — Generate a .proto file.
- `to_json_schema(schema, title)` — Generate a JSON Schema for validation.
- `example_1_faker()` — Example 1: Generate realistic data with Faker.
- `example_2_dataframes()` — Example 2: Export to DataFrames.
- `example_3_pytest_fixture()` — Example 3: pytest fixtures.
- `example_4_ifs_generator()` — Example 4: IFS Generator - true fractal data.
- `example_5_fractal_inference()` — Example 5: Infer fractal schema from real data.
- `example_6_benchmarks()` — Example 6: Run benchmarks.
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
- `run_in_docker(args_list)` — Uruchom fraq CLI w Docker
- `run_local(args_list)` — Uruchom fraq CLI lokalnie
- `main()` — —
- `ws_stream(websocket)` — Stream fractal data
- `ws_files(websocket)` — Stream file search results
- `health()` — —
- `example_network_scan_sync()` — Przykład 1: Synchroniczne skanowanie sieci
- `example_network_scan_async()` — Przykład 2: Asynchroniczne skanowanie ze streamingiem
- `example_web_crawl_sync()` — Przykład 3: Synchroniczny crawling strony
- `example_web_crawl_async()` — Przykład 4: Asynchroniczne crawlowanie ze streamingiem
- `example_fractal_coordinates()` — Przykład 5: Fraktalne koordynaty dla sieci i web
- `example_streaming_comparison()` — Przykład 6: Porównanie streaming vs batch
- `main()` — Uruchom wszystkie przykłady
- `example_1_sensors()` — Generuj sensory - UPROSZCZONE.
- `example_2_mqtt()` — MQTT - UPROSZCZONE.
- `example_3_streaming()` — Streaming - UPROSZCZONE.
- `example_1_sse()` — SSE - UPROSZCZONE.
- `example_2_websocket()` — WebSocket template.
- `example_3_streaming()` — Streaming - UPROSZCZONE.
- `example_4_kafka()` — Kafka pattern - UPROSZCZONE.
- `example_model_router()` — Example: ModelRouter routes queries to optimal models.
- `example_fraq_session()` — Example: FraqSession for multi-turn conversations.
- `example_fastapi_server()` — Example: Running FastAPI server.
- `example_combined_usage()` — Example: Combining all features.
- `example_1_classification()` — Binary classification - UPROSZCZONE.
- `example_2_regression()` — Regression - UPROSZCZONE.
- `example_3_timeseries()` — Time-series - UPROSZCZONE.
- `run_docker()` — Uruchom przez Docker Compose
- `stop_docker()` — Zatrzymaj stack
- `test_stack()` — Przetestuj stack
- `main()` — —
- `example_simple_parser()` — Rule-based parser — zero dependencies, works offline.
- `example_qwen25()` — qwen2.5:3b — good balance for Polish/English prompts.
- `example_llama32()` — llama3.2:3b — alternative lightweight model.
- `example_phi3()` — phi3:3.8b — stronger reasoning-oriented option.
- `example_convenience_functions()` — One-liner functions — simplest possible API.
- `example_file_search_direct()` — FileSearchAdapter — search real files on disk.
- `example_env_config()` — Load config from .env file.
- `example_full_pipeline()` — Full pipeline NL → parse → execute / file search.
- `run_local()` — Uruchom serwer lokalnie (bez Docker)
- `run_docker()` — Uruchom przez Docker
- `stop_docker()` — Zatrzymaj Docker
- `test_api()` — Przetestuj API
- `main()` — —
- `example_1_extract()` — Extract - UPROSZCZONE.
- `example_2_transform()` — Transform - UPROSZCZONE.
- `example_3_validate()` — Validate - UPROSZCZONE.
- `example_4_pipeline()` — Pipeline - UPROSZCZONE.
- `root()` — —
- `health()` — —
- `explore(depth, dims, format)` — Explore fractal structure
- `files_search(path, ext, limit, sort)` — Search files with fractal metadata
- `files_stat(file_path)` — Get file statistics with fractal coordinates
- `example_1_sqlite()` — Generuj dane do SQLite - UPROSZCZONE.
- `example_2_hybrid()` — Hybrid: real + fractal - UPROSZCZONE.
- `example_3_schema_save()` — Schema + save - UPROSZCZONE.
- `example_1_iot_sensors()` — IoT sensors - UPROSZCZONE.
- `example_2_erp_invoices()` — ERP invoices - UPROSZCZONE.
- `example_3_ai_training()` — AI training data - UPROSZCZONE.
- `example_4_devops_metrics()` — DevOps metrics - UPROSZCZONE.
- `example_5_finance()` — Finance - UPROSZCZONE.
- `example_1_basic()` — Basic async stream - UPROSZCZONE.
- `example_2_typed()` — Typed stream - UPROSZCZONE.
- `example_3_kafka()` — Kafka pattern - UPROSZCZONE.
- `main()` — —
- `example_1_basic_query()` — Podstawowe zapytanie - UPROSZCZONE.
- `example_2_json_output()` — JSON output - UPROSZCZONE.
- `example_3_csv_output()` — CSV output - UPROSZCZONE.
- `example_4_streaming()` — Streaming - UPROSZCZONE.
- `example_5_schema()` — Schema - UPROSZCZONE.
- `example_6_custom_schema()` — Custom schema - UPROSZCZONE.
- `example_fastapi_app()` — FastAPI application with fraq endpoints.
- `example_streamlit_app()` — Streamlit dashboard for fraq visualization.
- `example_flask_app()` — Flask application with fraq blueprints.
- `example_cli_chat()` — Interactive CLI chatbot with fraq + text2fraq.
- `example_websocket_server()` — WebSocket server for real-time fraq streaming.
- `example_kafka_producer()` — Kafka producer/consumer with fraq streams.
- `example_grpc_service()` — gRPC service definition and implementation.
- `example_jupyter_notebook()` — Jupyter notebook cells for interactive exploration.
- `example_celery_task()` — Celery background tasks for fraq processing.
- `generate_proto_file()` — Generate a .proto file for fraq service.
- `example_grpc_server_stub()` — Example gRPC server using fraq data.
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
- `root()` — —
- `query_data(fields, depth, fmt, limit)` — Query fractal data with typed fields.
- `stream_data(count, interval)` — Stream fractal records via SSE.
- `zoom(depth, direction)` — Zoom into fractal at given depth and direction.
- `generate_data(fields, count, seed)` — Generate synthetic data with fraq.
- `index()` — —
- `api_generate()` — Generate fractal data.
- `api_stream()` — Stream fractal data.
- `api_schema()` — Get or create schema.
- `health()` — —
- `jupyter_basic_usage()` — Basic fraq usage in Jupyter.
- `jupyter_visualization()` — Visualize fraq data in Jupyter.
- `jupyter_interactive_widget()` — Interactive widget for fraq in Jupyter.
- `jupyter_fractal_analysis()` — Analyze fractal patterns in generated data.
- `produce_to_kafka(count)` — Generate fraq data and produce to Kafka.
- `stream_to_kafka(duration_seconds)` — Stream fraq data to Kafka for specified duration.
- `consume_from_kafka(topic, max_records)` — Consume and display fraq data from Kafka.
- `fraq_websocket_handler(websocket, path)` — Handle WebSocket connections and stream fraq data.
- `main()` — Start WebSocket server.
- `test_client()` — Test client for WebSocket server.
- `main()` — Run CLI chat.
- `ws_stream(websocket)` — —
- `ws_files(websocket)` — —
- `health()` — —
- `root()` — —
- `health()` — —
- `explore(depth)` — —
- `files_search(path, ext, limit)` — —
- `to_asyncapi(schema, title, version)` — Generate an AsyncAPI 3.0 specification for streaming channels.
- `to_proto(schema, package, message_name)` — Generate a .proto file.
- `to_json_schema(schema, title)` — Generate a JSON Schema for validation.
- `to_openapi(schema, title, version, base_path)` — Generate an OpenAPI 3.0 specification.
- `to_graphql(schema, type_name)` — Generate a GraphQL schema definition.
- `to_nlp2cmd_schema(schema, command_name, version, category)` — Export a FraqSchema as an NLP2CMD command schema.
- `to_nlp2cmd_actions(schema)` — Export fraq operations as NLP2CMD ActionRegistry entries.
- `text2filesearch(text, base_path, fmt)` — One-liner to search files via natural language.
- `text2query(text, config)` — Convert text to ParsedQuery.
- `text2fraq(text, config, root)` — Convert text and execute query.
- `prepare(obj)` — Recursively convert FraqNode / bytes / tuples for JSON compat.
- `encode_value(v)` — Encode a single value to binary format.
- `to_binary(data)` — Minimal tagged binary encoding.
- `to_msgpack_lite(data)` — Ultra-light MessagePack-ish encoding (no external deps).
- `mp_encode(obj)` — Minimal msgpack-ish encoder using lookup table.
- `to_json(data)` — Serialise to JSON string.
- `to_jsonl(data)` — Serialise iterable of records to JSON-Lines.
- `to_csv(data)` — Serialise list of flat dicts to CSV.
- `to_yaml(data)` — Serialise to YAML (simple dumper, no PyYAML dependency).
- `simple_yaml(obj, indent)` — Dead-simple YAML emitter (no dependency).
- `get_provider_registry()` — Get global provider registry.
- `generate_with_faker(type_spec, seed)` — Convenience function to generate value with Faker.
- `get_adapter(source)` — Factory: return the right adapter for a source type.
- `natural_language(query)` — Natural language → fraq result with session support.
- `files_search(ext, pattern, limit, sort_by)` — Search files with fractal coordinates.
- `files_search_post(request)` — Search files with POST request.
- `files_nl(query, path)` — Natural language file search.
- `ws_stream(websocket)` — WebSocket endpoint for streaming fractal data.
- `health_check()` — Health check endpoint.
- `clear_session(session_id)` — Clear a conversation session.


## Project Structure

📄 `docs.examples.advanced_usage`
📄 `docs.examples.quickstart`
📄 `examples.ai_ml.training_data` (3 functions)
📄 `examples.bash_examples`
📄 `examples.basic.app_integrations` (9 functions)
📄 `examples.basic.applications` (5 functions)
📄 `examples.basic.async_streaming` (4 functions)
📄 `examples.basic.query_examples` (6 functions)
📄 `examples.cli-docker.bash_examples`
📄 `examples.cli-docker.run`
📄 `examples.database.sqlite_examples` (3 functions)
📄 `examples.etl.pipeline_examples` (4 functions)
📄 `examples.fastapi-docker.api_server` (13 functions)
📄 `examples.fastapi-docker.main` (5 functions)
📄 `examples.fastapi-docker.run`
📄 `examples.fullstack-docker.api.main` (4 functions)
📄 `examples.fullstack-docker.frontend.app`
📄 `examples.fullstack-docker.run`
📄 `examples.fullstack-docker.websocket.main` (3 functions)
📄 `examples.integrations.cli_chat_example` (10 functions, 1 classes)
📄 `examples.integrations.fastapi_example` (5 functions)
📄 `examples.integrations.flask_example` (5 functions)
📄 `examples.integrations.grpc_example` (2 functions)
📄 `examples.integrations.jupyter_example` (4 functions)
📄 `examples.integrations.kafka_example` (3 functions)
📄 `examples.integrations.streamlit_example`
📄 `examples.integrations.websocket_example` (3 functions)
📄 `examples.iot.sensor_examples` (3 functions)
📄 `examples.network.network_web_examples` (7 functions)
📄 `examples.new_features_demo` (6 functions)
📄 `examples.nlp_examples`
📄 `examples.streaming.sse_examples` (4 functions)
📄 `examples.text2fraq.nlp2cmd_integration` (11 functions)
📄 `examples.text2fraq.text2fraq_examples` (11 functions)
📄 `examples.text2fraq.text2fraq_files` (5 functions)
📄 `examples.v028.new_features` (4 functions)
📄 `examples.websocket-docker.main` (3 functions)
📄 `examples.websocket-docker.run`
📦 `fraq` (1 functions)
📦 `fraq.adapters`
📄 `fraq.adapters.base` (4 functions, 1 classes)
📄 `fraq.adapters.file_adapter` (3 functions, 1 classes)
📄 `fraq.adapters.file_search` (18 functions, 3 classes)
📄 `fraq.adapters.http_adapter` (2 functions, 1 classes)
📄 `fraq.adapters.hybrid_adapter` (4 functions, 1 classes)
📄 `fraq.adapters.registry` (1 functions)
📄 `fraq.adapters.sensor_adapter` (4 functions, 1 classes)
📄 `fraq.adapters.sql_adapter` (5 functions, 1 classes)
📄 `fraq.api` (18 functions, 2 classes)
📄 `fraq.benchmarks` (8 functions, 4 classes)
📄 `fraq.cli` (24 functions)
📄 `fraq.core` (17 functions, 4 classes)
📄 `fraq.dataframes` (4 functions)
📦 `fraq.export`
📄 `fraq.export.asyncapi` (1 functions)
📄 `fraq.export.common`
📄 `fraq.export.graphql` (1 functions)
📄 `fraq.export.json_schema` (1 functions)
📄 `fraq.export.nlp2cmd` (2 functions)
📄 `fraq.export.openapi` (1 functions)
📄 `fraq.export.proto` (1 functions)
📦 `fraq.formats`
📄 `fraq.formats.binary` (11 functions)
📄 `fraq.formats.prepare` (2 functions)
📄 `fraq.formats.registry` (4 functions, 1 classes)
📄 `fraq.formats.text` (5 functions)
📄 `fraq.generators` (9 functions, 4 classes)
📄 `fraq.ifs` (11 functions, 5 classes)
📦 `fraq.inference` (5 functions, 1 classes)
📄 `fraq.inference.correlation` (4 functions, 1 classes)
📄 `fraq.inference.dimension` (8 functions, 2 classes)
📄 `fraq.inference.hierarchy` (7 functions, 2 classes)
📄 `fraq.inference.schema` (5 functions, 1 classes)
📦 `fraq.providers`
📄 `fraq.providers.faker_provider` (13 functions, 3 classes)
📄 `fraq.query` (12 functions, 4 classes)
📄 `fraq.schema_export` (7 functions)
📄 `fraq.server` (7 functions, 3 classes)
📄 `fraq.streaming` (5 functions, 1 classes)
📦 `fraq.text2fraq`
📄 `fraq.text2fraq.config` (1 functions, 1 classes)
📄 `fraq.text2fraq.file_search_parser` (11 functions, 1 classes)
📄 `fraq.text2fraq.llm_client` (2 functions, 1 classes)
📄 `fraq.text2fraq.models` (2 functions, 2 classes)
📄 `fraq.text2fraq.parser_llm` (7 functions, 1 classes)
📄 `fraq.text2fraq.parser_rules` (8 functions, 1 classes)
📄 `fraq.text2fraq.router` (4 functions, 1 classes)
📄 `fraq.text2fraq.session` (8 functions, 1 classes)
📄 `fraq.text2fraq.shortcuts` (3 functions)
📄 `fraq.types`
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