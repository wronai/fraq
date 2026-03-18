# fraq — API Reference

> 70 modules | 371 functions | 51 classes

## Contents

- [examples](#examples) (24 modules)
- [Core](#core) (2 modules)
- [fraq](#fraq) (38 modules)

## examples

### `examples.ai_ml.training_data` [source](https://github.com/wronai/fraq/blob/main/examples/ai_ml/training_data.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_1_classification` | `example_1_classification()` | 4 | Binary classification - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/ai_ml/training_data.py#L9) |
| `example_2_regression` | `example_2_regression()` | 3 | Regression - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/ai_ml/training_data.py#L33) |
| `example_3_timeseries` | `example_3_timeseries()` | 1 | Time-series - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/ai_ml/training_data.py#L57) |

### `examples.basic.app_integrations` [source](https://github.com/wronai/fraq/blob/main/examples/basic/app_integrations.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_celery_task` | `example_celery_task()` | 1 | Celery background tasks for fraq processing. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/app_integrations.py#L488) |
| `example_cli_chat` | `example_cli_chat()` | 1 | Interactive CLI chatbot with fraq + text2fraq. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/app_integrations.py#L190) |
| `example_fastapi_app` | `example_fastapi_app()` | 1 | FastAPI application with fraq endpoints. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/app_integrations.py#L14) |
| `example_flask_app` | `example_flask_app()` | 1 | Flask application with fraq blueprints. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/app_integrations.py#L133) |
| `example_grpc_service` | `example_grpc_service()` | 1 | gRPC service definition and implementation. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/app_integrations.py#L352) |
| `example_jupyter_notebook` | `example_jupyter_notebook()` | 1 | Jupyter notebook cells for interactive exploration. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/app_integrations.py#L437) |
| `example_kafka_producer` | `example_kafka_producer()` | 1 | Kafka producer/consumer with fraq streams. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/app_integrations.py#L297) |
| `example_streamlit_app` | `example_streamlit_app()` | 1 | Streamlit dashboard for fraq visualization. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/app_integrations.py#L74) |
| `example_websocket_server` | `example_websocket_server()` | 1 | WebSocket server for real-time fraq streaming. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/app_integrations.py#L246) |

### `examples.basic.applications` [source](https://github.com/wronai/fraq/blob/main/examples/basic/applications.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_1_iot_sensors` | `example_1_iot_sensors()` | 5 | IoT sensors - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/applications.py#L9) |
| `example_2_erp_invoices` | `example_2_erp_invoices()` | 4 | ERP invoices - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/applications.py#L37) |
| `example_3_ai_training` | `example_3_ai_training()` | 3 | AI training data - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/applications.py#L60) |
| `example_4_devops_metrics` | `example_4_devops_metrics()` | 3 | DevOps metrics - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/applications.py#L87) |
| `example_5_finance` | `example_5_finance()` | 2 | Finance - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/applications.py#L104) |

### `examples.basic.async_streaming` [source](https://github.com/wronai/fraq/blob/main/examples/basic/async_streaming.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_1_basic` | `example_1_basic()` | 2 | Basic async stream - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/async_streaming.py#L11) |
| `example_2_typed` | `example_2_typed()` | 2 | Typed stream - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/async_streaming.py#L24) |
| `example_3_kafka` | `example_3_kafka()` | 2 | Kafka pattern - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/async_streaming.py#L43) |
| `main` | `main()` | 1 | — | [source](https://github.com/wronai/fraq/blob/main/examples/basic/async_streaming.py#L62) |

### `examples.basic.query_examples` [source](https://github.com/wronai/fraq/blob/main/examples/basic/query_examples.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_1_basic_query` | `example_1_basic_query()` | 2 | Podstawowe zapytanie - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/query_examples.py#L9) |
| `example_2_json_output` | `example_2_json_output()` | 1 | JSON output - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/query_examples.py#L25) |
| `example_3_csv_output` | `example_3_csv_output()` | 2 | CSV output - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/query_examples.py#L43) |
| `example_4_streaming` | `example_4_streaming()` | 2 | Streaming - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/query_examples.py#L61) |
| `example_5_schema` | `example_5_schema()` | 2 | Schema - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/query_examples.py#L72) |
| `example_6_custom_schema` | `example_6_custom_schema()` | 2 | Custom schema - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/basic/query_examples.py#L87) |

### `examples.cli-docker.run` [source](https://github.com/wronai/fraq/blob/main/examples/cli-docker/run.sh)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `main` | `main()` | 3 | — | [source](https://github.com/wronai/fraq/blob/main/examples/cli-docker/run.py#L39) |
| `run_in_docker` | `run_in_docker(args_list)` | 1 | Uruchom fraq CLI w Docker | [source](https://github.com/wronai/fraq/blob/main/examples/cli-docker/run.py#L17) |
| `run_local` | `run_local(args_list)` | 1 | Uruchom fraq CLI lokalnie | [source](https://github.com/wronai/fraq/blob/main/examples/cli-docker/run.py#L28) |

### `examples.database.sqlite_examples` [source](https://github.com/wronai/fraq/blob/main/examples/database/sqlite_examples.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_1_sqlite` | `example_1_sqlite()` | 3 | Generuj dane do SQLite - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/database/sqlite_examples.py#L10) |
| `example_2_hybrid` | `example_2_hybrid()` | 3 | Hybrid: real + fractal - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/database/sqlite_examples.py#L43) |
| `example_3_schema_save` | `example_3_schema_save()` | 3 | Schema + save - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/database/sqlite_examples.py#L69) |

### `examples.etl.pipeline_examples` [source](https://github.com/wronai/fraq/blob/main/examples/etl/pipeline_examples.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_1_extract` | `example_1_extract()` | 4 | Extract - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/etl/pipeline_examples.py#L9) |
| `example_2_transform` | `example_2_transform()` | 3 | Transform - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/etl/pipeline_examples.py#L46) |
| `example_3_validate` | `example_3_validate()` | 4 | Validate - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/etl/pipeline_examples.py#L71) |
| `example_4_pipeline` | `example_4_pipeline()` | 5 | Pipeline - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/etl/pipeline_examples.py#L89) |

### `examples.fastapi-docker.api_server` [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `explore` | `explore(depth, dims, seed, format)` | 3 | Zoom into fractal at given depth. | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L114) |
| `files_list` | `files_list(path, ext, limit, sort, ...)` | 3 | List files (ls-style). | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L247) |
| `files_search` | `files_search(path, ext, pattern, limit, ...)` | 3 | Search files with fractal metadata. | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L213) |
| `files_stat` | `files_stat(file_path)` | 4 | Get file statistics with fractal coordinates. | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L269) |
| `health` | `health()` | 1 | Health check. | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L104) |
| `lifespan` | `lifespan(app)` | 1 | App lifespan manager. | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L60) |
| `natural_language` | `natural_language(query, path, format)` | 5 | Process natural language query (requires LLM). | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L303) |
| `query_data` | `query_data(fields, depth, format, limit, ...)` | 4 | Execute fractal query with typed fields. | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L164) |
| `root` | `root()` | 1 | API info. | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L89) |
| `schema_records` | `schema_records(fields, depth, branching, format, ...)` | 4 | Generate typed schema records. | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L186) |
| `stream` | `stream(count, dims, format)` | 5 | Stream cursor records. | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L136) |
| `ws_files` | `ws_files(websocket)` | 7 | WebSocket for file search streaming. | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L359) |
| `ws_stream` | `ws_stream(websocket)` | 6 | WebSocket streaming of fractal data. | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/api_server.py#L335) |

### `examples.fastapi-docker.main` [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/main.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `explore` | `explore(depth, dims, format)` | 2 | Explore fractal structure | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/main.py#L32) |
| `files_search` | `files_search(path, ext, limit, sort)` | 2 | Search files with fractal metadata | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/main.py#L46) |
| `files_stat` | `files_stat(file_path)` | 2 | Get file statistics with fractal coordinates | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/main.py#L62) |
| `health` | `health()` | 1 | — | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/main.py#L27) |
| `root` | `root()` | 1 | — | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/main.py#L22) |

### `examples.fastapi-docker.run` [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/run.sh)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `main` | `main()` | 4 | — | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/run.py#L79) |
| `run_docker` | `run_docker()` | 1 | Uruchom przez Docker | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/run.py#L29) |
| `run_local` | `run_local()` | 2 | Uruchom serwer lokalnie (bez Docker) | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/run.py#L16) |
| `stop_docker` | `stop_docker()` | 1 | Zatrzymaj Docker | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/run.py#L38) |
| `test_api` | `test_api()` | 4 | Przetestuj API | [source](https://github.com/wronai/fraq/blob/main/examples/fastapi-docker/run.py#L45) |

### `examples.fullstack-docker.api.main` [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/api/main.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `explore` | `explore(depth)` | 1 | — | [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/api/main.py#L24) |
| `files_search` | `files_search(path, ext, limit)` | 1 | — | [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/api/main.py#L31) |
| `health` | `health()` | 1 | — | [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/api/main.py#L19) |
| `root` | `root()` | 1 | — | [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/api/main.py#L14) |

### `examples.fullstack-docker.run` [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/run.sh)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `main` | `main()` | 4 | — | [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/run.py#L57) |
| `run_docker` | `run_docker()` | 1 | Uruchom przez Docker Compose | [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/run.py#L18) |
| `stop_docker` | `stop_docker()` | 1 | Zatrzymaj stack | [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/run.py#L28) |
| `test_stack` | `test_stack()` | 3 | Przetestuj stack | [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/run.py#L35) |

### `examples.fullstack-docker.websocket.main` [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/websocket/main.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `health` | `health()` | 1 | — | [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/websocket/main.py#L51) |
| `ws_files` | `ws_files(websocket)` | 5 | — | [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/websocket/main.py#L32) |
| `ws_stream` | `ws_stream(websocket)` | 5 | — | [source](https://github.com/wronai/fraq/blob/main/examples/fullstack-docker/websocket/main.py#L14) |

### `examples.iot.sensor_examples` [source](https://github.com/wronai/fraq/blob/main/examples/iot/sensor_examples.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_1_sensors` | `example_1_sensors()` | 3 | Generuj sensory - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/iot/sensor_examples.py#L10) |
| `example_2_mqtt` | `example_2_mqtt()` | 3 | MQTT - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/iot/sensor_examples.py#L33) |
| `example_3_streaming` | `example_3_streaming()` | 2 | Streaming - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/iot/sensor_examples.py#L63) |

### `examples.network.network_web_examples` [source](https://github.com/wronai/fraq/blob/main/examples/network/network_web_examples.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_fractal_coordinates` | `example_fractal_coordinates()` | 1 | Przykład 5: Fraktalne koordynaty dla sieci i web | [source](https://github.com/wronai/fraq/blob/main/examples/network/network_web_examples.py#L116) |
| `example_network_scan_async` | `example_network_scan_async()` | 3 | Przykład 2: Asynchroniczne skanowanie ze streamingiem | [source](https://github.com/wronai/fraq/blob/main/examples/network/network_web_examples.py#L42) |
| `example_network_scan_sync` | `example_network_scan_sync()` | 2 | Przykład 1: Synchroniczne skanowanie sieci | [source](https://github.com/wronai/fraq/blob/main/examples/network/network_web_examples.py#L13) |
| `example_streaming_comparison` | `example_streaming_comparison()` | 1 | Przykład 6: Porównanie streaming vs batch | [source](https://github.com/wronai/fraq/blob/main/examples/network/network_web_examples.py#L140) |
| `example_web_crawl_async` | `example_web_crawl_async()` | 2 | Przykład 4: Asynchroniczne crawlowanie ze streamingiem | [source](https://github.com/wronai/fraq/blob/main/examples/network/network_web_examples.py#L94) |
| `example_web_crawl_sync` | `example_web_crawl_sync()` | 2 | Przykład 3: Synchroniczny crawling strony | [source](https://github.com/wronai/fraq/blob/main/examples/network/network_web_examples.py#L64) |
| `main` | `main()` | 1 | Uruchom wszystkie przykłady | [source](https://github.com/wronai/fraq/blob/main/examples/network/network_web_examples.py#L169) |

### `examples.new_features_demo` [source](https://github.com/wronai/fraq/blob/main/examples/new_features_demo.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_1_faker` | `example_1_faker()` | 3 | Example 1: Generate realistic data with Faker. | [source](https://github.com/wronai/fraq/blob/main/examples/new_features_demo.py#L15) |
| `example_2_dataframes` | `example_2_dataframes()` | 2 | Example 2: Export to DataFrames. | [source](https://github.com/wronai/fraq/blob/main/examples/new_features_demo.py#L46) |
| `example_3_pytest_fixture` | `example_3_pytest_fixture()` | 5 | Example 3: pytest fixtures. | [source](https://github.com/wronai/fraq/blob/main/examples/new_features_demo.py#L70) |
| `example_4_ifs_generator` | `example_4_ifs_generator()` | 2 | Example 4: IFS Generator - true fractal data. | [source](https://github.com/wronai/fraq/blob/main/examples/new_features_demo.py#L96) |
| `example_5_fractal_inference` | `example_5_fractal_inference()` | 5 | Example 5: Infer fractal schema from real data. | [source](https://github.com/wronai/fraq/blob/main/examples/new_features_demo.py#L122) |
| `example_6_benchmarks` | `example_6_benchmarks()` | 2 | Example 6: Run benchmarks. | [source](https://github.com/wronai/fraq/blob/main/examples/new_features_demo.py#L158) |

### `examples.streaming.sse_examples` [source](https://github.com/wronai/fraq/blob/main/examples/streaming/sse_examples.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_1_sse` | `example_1_sse()` | 2 | SSE - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/streaming/sse_examples.py#L12) |
| `example_2_websocket` | `example_2_websocket()` | 1 | WebSocket template. | [source](https://github.com/wronai/fraq/blob/main/examples/streaming/sse_examples.py#L45) |
| `example_3_streaming` | `example_3_streaming()` | 2 | Streaming - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/streaming/sse_examples.py#L63) |
| `example_4_kafka` | `example_4_kafka()` | 2 | Kafka pattern - UPROSZCZONE. | [source](https://github.com/wronai/fraq/blob/main/examples/streaming/sse_examples.py#L77) |

### `examples.text2fraq.nlp2cmd_integration` [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/nlp2cmd_integration.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `build_erp_schema` | `build_erp_schema()` | 1 | Schemat ERP / accounting. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/nlp2cmd_integration.py#L37) |
| `build_sensor_schema` | `build_sensor_schema()` | 1 | Schemat IoT sensorów — bazowy przykład. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/nlp2cmd_integration.py#L25) |
| `example_asyncapi` | `example_asyncapi()` | 1 | AsyncAPI 3.0 — dla Kafka / WebSocket / NATS streaming. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/nlp2cmd_integration.py#L129) |
| `example_full_nlp2cmd_workflow` | `example_full_nlp2cmd_workflow()` | 3 | Pełny workflow: FraqSchema → NLP2CMD SchemaRegistry → Natural Language → Command. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/nlp2cmd_integration.py#L161) |
| `example_graphql` | `example_graphql()` | 1 | GraphQL — dla złożonych relacyjnych query. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/nlp2cmd_integration.py#L120) |
| `example_grpc_proto` | `example_grpc_proto()` | 1 | gRPC / Protobuf — high-performance dla edge computing. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/nlp2cmd_integration.py#L139) |
| `example_json_schema` | `example_json_schema()` | 1 | JSON Schema — walidacja rekordów. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/nlp2cmd_integration.py#L148) |
| `example_nlp2cmd_actions` | `example_nlp2cmd_actions()` | 3 | Generuj ActionRegistry entries dla NLP2CMD. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/nlp2cmd_integration.py#L74) |
| `example_nlp2cmd_command_schema` | `example_nlp2cmd_command_schema()` | 1 | Generuj NLP2CMD command schema → command_schemas/fraq_sensor.json | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/nlp2cmd_integration.py#L54) |
| `example_nlp2cmd_erp` | `example_nlp2cmd_erp()` | 3 | ERP schema dla NLP2CMD — business automation. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/nlp2cmd_integration.py#L86) |
| `example_openapi` | `example_openapi()` | 1 | OpenAPI 3.0 — dla FastAPI / REST endpoints. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/nlp2cmd_integration.py#L109) |

### `examples.text2fraq.text2fraq_examples` [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_examples.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_convenience_functions` | `example_convenience_functions()` | 3 | One-liner functions — simplest possible API. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_examples.py#L164) |
| `example_env_config` | `example_env_config()` | 1 | Load config from .env file. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_examples.py#L208) |
| `example_file_search_direct` | `example_file_search_direct()` | 3 | FileSearchAdapter — search real files on disk. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_examples.py#L184) |
| `example_full_pipeline` | `example_full_pipeline()` | 3 | Full pipeline NL → parse → execute / file search. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_examples.py#L223) |
| `example_llama32` | `example_llama32()` | 2 | llama3.2:3b — alternative lightweight model. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_examples.py#L123) |
| `example_phi3` | `example_phi3()` | 2 | phi3:3.8b — stronger reasoning-oriented option. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_examples.py#L142) |
| `example_qwen25` | `example_qwen25()` | 3 | qwen2.5:3b — good balance for Polish/English prompts. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_examples.py#L97) |
| `example_simple_parser` | `example_simple_parser()` | 3 | Rule-based parser — zero dependencies, works offline. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_examples.py#L68) |

### `examples.text2fraq.text2fraq_files` [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_files.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_convenience_function` | `example_convenience_function()` | 6 | Użycie funkcji text2filesearch. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_files.py#L135) |
| `example_file_search_adapter_direct` | `example_file_search_adapter_direct()` | 4 | Bezpośrednie użycie FileSearchAdapter. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_files.py#L169) |
| `example_llm_file_intent` | `example_llm_file_intent()` | 4 | Rozpoznawanie intencji plikowych przez LLM. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_files.py#L201) |
| `example_pdf_search_rule_based` | `example_pdf_search_rule_based()` | 5 | Wyszukiwanie PDF bez LLM - rule based. | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_files.py#L32) |
| `example_pdf_search_with_llm` | `example_pdf_search_with_llm()` | 9 | Wyszukiwanie PDF z użyciem LLM (qwen2.5). | [source](https://github.com/wronai/fraq/blob/main/examples/text2fraq/text2fraq_files.py#L69) |

### `examples.v028.new_features` [source](https://github.com/wronai/fraq/blob/main/examples/v028/new_features.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `example_combined_usage` | `example_combined_usage()` | 1 | Example: Combining all features. | [source](https://github.com/wronai/fraq/blob/main/examples/v028/new_features.py#L99) |
| `example_fastapi_server` | `example_fastapi_server()` | 1 | Example: Running FastAPI server. | [source](https://github.com/wronai/fraq/blob/main/examples/v028/new_features.py#L69) |
| `example_fraq_session` | `example_fraq_session()` | 1 | Example: FraqSession for multi-turn conversations. | [source](https://github.com/wronai/fraq/blob/main/examples/v028/new_features.py#L41) |
| `example_model_router` | `example_model_router()` | 1 | Example: ModelRouter routes queries to optimal models. | [source](https://github.com/wronai/fraq/blob/main/examples/v028/new_features.py#L11) |

### `examples.websocket-docker.main` [source](https://github.com/wronai/fraq/blob/main/examples/websocket-docker/main.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `health` | `health()` | 1 | — | [source](https://github.com/wronai/fraq/blob/main/examples/websocket-docker/main.py#L98) |
| `ws_files` | `ws_files(websocket)` | 7 | Stream file search results | [source](https://github.com/wronai/fraq/blob/main/examples/websocket-docker/main.py#L50) |
| `ws_stream` | `ws_stream(websocket)` | 6 | Stream fractal data | [source](https://github.com/wronai/fraq/blob/main/examples/websocket-docker/main.py#L17) |

### `examples.websocket-docker.run` [source](https://github.com/wronai/fraq/blob/main/examples/websocket-docker/run.sh)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `main` | `main()` | 4 | — | [source](https://github.com/wronai/fraq/blob/main/examples/websocket-docker/run.py#L69) |
| `run_docker` | `run_docker()` | 1 | Uruchom przez Docker | [source](https://github.com/wronai/fraq/blob/main/examples/websocket-docker/run.py#L19) |
| `run_local` | `run_local()` | 2 | Uruchom lokalnie | [source](https://github.com/wronai/fraq/blob/main/examples/websocket-docker/run.py#L32) |
| `stop_docker` | `stop_docker()` | 1 | Zatrzymaj Docker | [source](https://github.com/wronai/fraq/blob/main/examples/websocket-docker/run.py#L26) |
| `test_websocket` | `test_websocket()` | 3 | Przetestuj WebSocket | [source](https://github.com/wronai/fraq/blob/main/examples/websocket-docker/run.py#L45) |

## Core

### `fraq` [source](https://github.com/wronai/fraq/blob/main/fraq/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `BaseAdapter` | 4 | Interface every data-source adapter must implement. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/base.py#L12) |
| `FileAdapter` | 2 | Read/write fractal state from local files. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_adapter.py#L16) |
| `FileSearchAdapter` | 4 | Adapter for searching files on disk using fractal patterns. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_search.py#L78) |
| `FileSystemPort` | 4 | Port for filesystem I/O operations. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_search.py#L20) |
| `RealFileSystem` | 4 | Real filesystem implementation of FileSystemPort. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_search.py#L45) |
| `HTTPAdapter` | 2 | Fetch fractal roots from remote HTTP APIs. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/http_adapter.py#L15) |
| `HybridAdapter` | 3 | Combine roots from several adapters into one fractal. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/hybrid_adapter.py#L12) |
| `SensorAdapter` | 3 | Simulate or consume live sensor data as fractal streams. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/sensor_adapter.py#L14) |
| `SQLAdapter` | 3 | Map fractal nodes to/from relational tables. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/sql_adapter.py#L13) |
| `BenchmarkResult` | 0 | Single benchmark result. | [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py#L22) |
| `MemoryBenchmark` | 2 | Benchmark memory usage - fraq's zero-storage advantage. | [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py#L81) |
| `SpeedBenchmark` | 2 | Benchmark generation speed. | [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py#L31) |
| `StructuralBenchmark` | 2 | Benchmark fractal self-similarity vs random data. | [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py#L139) |
| `FieldDef` | 0 | One field in a FraqSchema. | [source](https://github.com/wronai/fraq/blob/main/fraq/core.py#L216) |
| `FraqCursor` | 6 | Stateful walk through the fractal. | [source](https://github.com/wronai/fraq/blob/main/fraq/core.py#L359) |
| `FraqNode` | 4 | A single point in the infinite fractal data space. | [source](https://github.com/wronai/fraq/blob/main/fraq/core.py#L70) |
| `FraqSchema` | 3 | Typed projection of a fractal into structured records. | [source](https://github.com/wronai/fraq/blob/main/fraq/core.py#L226) |
| `FormatRegistry` | 4 | Registry of serialisation backends. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/registry.py#L10) |
| `FibonacciGenerator` | 0 | Value based on generalised Fibonacci sequence at the node's depth. | [source](https://github.com/wronai/fraq/blob/main/fraq/generators.py#L44) |
| `HashGenerator` | 0 | Deterministic pseudo-random values via SHA-256. | [source](https://github.com/wronai/fraq/blob/main/fraq/generators.py#L19) |
| `PerlinGenerator` | 0 | Simplified 1-D Perlin-ish noise from the L2 norm of position. | [source](https://github.com/wronai/fraq/blob/main/fraq/generators.py#L66) |
| `SensorStreamGenerator` | 0 | Simulate an infinite IoT sensor stream. | [source](https://github.com/wronai/fraq/blob/main/fraq/generators.py#L88) |
| `AffineTransform` | 1 | Affine transformation for IFS. | [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py#L38) |
| `IFSGenerator` | 3 | Iterated Function System generator. | [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py#L66) |
| `NetworkMapper` | 1 | Mapper for network topology data. | [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py#L229) |
| `OrganizationalMapper` | 1 | Mapper for organizational hierarchy data. | [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py#L196) |
| `ValueMapper` | 1 | Protocol for mapping fractal coordinates to data values. | [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py#L58) |
| `FractalAnalyzer` | 3 | Analyze data for fractal properties. | [source](https://github.com/wronai/fraq/blob/main/fraq/inference.py#L56) |
| `FractalDimension` | 0 | Fractal dimension analysis result. | [source](https://github.com/wronai/fraq/blob/main/fraq/inference.py#L39) |
| `InferredSchema` | 2 | Schema inferred from real data with fractal properties. | [source](https://github.com/wronai/fraq/blob/main/fraq/inference.py#L250) |
| `PatternSignature` | 0 | Detected pattern in data column. | [source](https://github.com/wronai/fraq/blob/main/fraq/inference.py#L47) |
| `FakerProvider` | 2 | Faker-based value provider for realistic data generation. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L36) |
| `ProviderRegistry` | 4 | Registry of value providers. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L104) |
| `ValueProvider` | 2 | Protocol for value providers. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L24) |
| `FraqExecutor` | 2 | Execute a FraqQuery against a root node. | [source](https://github.com/wronai/fraq/blob/main/fraq/query.py#L147) |
| `FraqFilter` | 1 | Post-zoom predicate on a record field. | [source](https://github.com/wronai/fraq/blob/main/fraq/query.py#L42) |
| `FraqQuery` | 6 | Declarative query against fractal data. | [source](https://github.com/wronai/fraq/blob/main/fraq/query.py#L70) |
| `SourceType` | 0 | Known data source families. | [source](https://github.com/wronai/fraq/blob/main/fraq/query.py#L30) |
| `FilesSearchRequest` | 0 | File search request. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L71) |
| `NLQueryRequest` | 0 | Natural language query request. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L57) |
| `NLQueryResponse` | 0 | Natural language query response. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L64) |
| `AsyncFraqStream` | 2 | Async generator that yields fractal records at a controlled rate. | [source](https://github.com/wronai/fraq/blob/main/fraq/streaming.py#L17) |
| `Text2FraqConfig` | 1 | Configuration for text2fraq. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/config.py#L14) |
| `FileSearchText2Fraq` | 3 | Natural language to file search converter. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/file_search_parser.py#L17) |
| `LiteLLMClient` | 1 | LiteLLM client for text completion. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/llm_client.py#L15) |
| `LLMClient` | 1 | Protocol for LLM clients. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/models.py#L38) |
| `ParsedQuery` | 1 | Parsed natural language query. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/models.py#L12) |
| `Text2Fraq` | 2 | Natural language to fractal query converter (LLM-based). | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/parser_llm.py#L17) |
| `Text2FraqSimple` | 2 | Rule-based text2fraq without LLM (fallback for offline use). | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/parser_rules.py#L43) |
| `ModelRouter` | 2 | Route queries to the best model based on complexity. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/router.py#L11) |
| `FraqSession` | 3 | Multi-turn conversation with context memory. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/session.py#L15) |

**`BaseAdapter` methods:**

- `load_root(uri)` — Materialise a root node from the source.
- `save(node, uri, fmt)` — Persist a node (or subtree) back to the source. Return the path/URI.
- `execute(query)` — Load root from *query.source_uri*, then run the query.
- `execute_iter(query)`

**`FileAdapter` methods:**

- `load_root(uri)`
- `save(node, uri, fmt)`

**`FileSearchAdapter` methods:**

- `load_root(uri)`
- `search(extension, pattern, limit, sort_by, ...)` — Search files - orchestrates I/O and applies pure logic.
- `save(node, uri, fmt)` — Save node data to file.
- `stream(extension, pattern, count)` — Stream files lazily.

**`FileSystemPort` methods:**

- `stat(path)` — Get file stats. Returns None if file doesn't exist or no permission.
- `list_files(base_path, pattern, recursive)` — List files matching pattern. Yields Path objects.
- `is_file(path)` — Check if path is a file.
- `write_bytes(path, data)` — Write bytes to file.

**`RealFileSystem` methods:**

- `stat(path)`
- `list_files(base_path, pattern, recursive)`
- `is_file(path)`
- `write_bytes(path, data)`

**`HTTPAdapter` methods:**

- `load_root(uri)`
- `save(node, uri, fmt)`

**`HybridAdapter` methods:**

- `add(adapter, uri)`
- `load_root(uri)`
- `save(node, uri, fmt)`

**`SensorAdapter` methods:**

- `load_root(uri)`
- `save(node, uri, fmt)`
- `stream(depth, count, direction)`

**`SQLAdapter` methods:**

- `load_root(uri)`
- `save(node, uri, fmt)`
- `generate_sql_function(dims)`

**`MemoryBenchmark` methods:**

- `measure_memory_usage(generator_fn, count)` — Measure peak memory usage during generation.
- `compare_memory(count)` — Compare memory usage of different approaches.

**`SpeedBenchmark` methods:**

- `fraq_generate(count)` — Benchmark fraq generate().
- `fraq_stream(count)` — Benchmark fraq streaming (lazy).

**`StructuralBenchmark` methods:**

- `test_self_similarity(data, column)` — Test if data has self-similar structure.
- `compare_structures()` — Compare structural properties of different generators.

**`FraqCursor` methods:**

- `advance(direction)` — Move one level deeper and return the new node.
- `back()` — Go up one level.
- `reset()` — Return to root.
- `snapshot()` — Serialisable state.

**`FraqNode` methods:**

- `zoom(direction)` — Zoom into the fractal along *direction* by *steps* levels.
- `children(directions)` — Return children in several directions (auto-generated if omitted).
- `to_dict(max_depth)` — Snapshot of this node as a plain dict.

**`FraqSchema` methods:**

- `add_field(name, type, direction, transform)`
- `record(node)` — Produce a single record from *node* (defaults to root).
- `records(depth, branching, count, node)` — Yield records by exploring children.

**`FormatRegistry` methods:**

- `register(cls, name, fn)` — Register a formatter. Can be used as a decorator.
- `get(cls, name)`
- `available(cls)`
- `serialize(cls, name, data)`

**`IFSGenerator` methods:**

- `generate_coordinate(depth, start)` — Generate a fractal coordinate at given depth.
- `generate(count, depth, mapper)` — Generate records with fractal structure.
- `generate_hierarchy(root, branching, depth)` — Generate hierarchical data (tree structure).

**`FractalAnalyzer` methods:**

- `box_counting_dimension(values, min_box_size, max_box_size)` — Calculate box-counting dimension of value distribution.
- `detect_hierarchy(data, parent_column)` — Detect hierarchical structure in data.
- `analyze_correlations(data)` — Analyze correlations between columns for fractal relationships.

**`InferredSchema` methods:**

- `generate(count, seed)` — Generate synthetic data with same fractal structure.
- `to_dict()` — Serialize to dictionary.

**`FakerProvider` methods:**

- `supports(type_spec)` — Check if type_spec is a faker specification.
- `generate(type_spec, seed)` — Generate value using Faker.

**`ProviderRegistry` methods:**

- `register(provider)` — Register a value provider.
- `get_faker_provider(locale)` — Get or create Faker provider.
- `find_provider(type_spec)` — Find provider that supports the given type specification.
- `generate(type_spec, seed)` — Generate value using appropriate provider.

**`ValueProvider` methods:**

- `supports(type_spec)` — Check if this provider supports the given type specification.
- `generate(type_spec, seed)` — Generate a value for the given type specification.

**`FraqExecutor` methods:**

- `execute(query)` — Run *query* and return serialised output.
- `execute_iter(query)` — Lazily yield filtered records (no serialisation).

**`FraqQuery` methods:**

- `zoom(depth, direction)`
- `select()` — Add fields, e.g. ``q.select("name:str", "value:float")``.
- `where(field, op, value)`
- `output(fmt)`
- `take(n)`
- `from_source(source, uri)`

**`FileSearchText2Fraq` methods:**

- `parse(text)` — Parse natural language file query to search parameters.
- `search(text)` — Parse query and execute file search.
- `format_results(results, fmt, fields)` — Format file search results to specified format.

**`Text2Fraq` methods:**

- `parse(text)` — Parse natural language text to structured query.
- `execute(text, root)` — Parse text and execute query immediately.

**`Text2FraqSimple` methods:**

- `parse(text)` — Parse using rule-based matching.
- `execute(text, root)` — Parse and execute query.

**`ModelRouter` methods:**

- `route(text)` — Select best model based on query complexity.
- `get_config_for_model(model)` — Get recommended config for model.

**`FraqSession` methods:**

- `ask(text)` — Process query with context awareness.
- `get_context_summary()` — Get summary of current session context.
- `clear()` — Clear session history and context.

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `get_adapter` | `get_adapter(source)` | 3 | Factory: return the right adapter for a source type. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/registry.py#L26) |
| `generate` | `generate(fields, count, seed, output)` | 6 | Generate records with simple field specification. | [source](https://github.com/wronai/fraq/blob/main/fraq/api.py#L72) |
| `quick_schema` | `quick_schema()` | 6 | Create schema from simple field names. Auto-detects types. | [source](https://github.com/wronai/fraq/blob/main/fraq/api.py#L181) |
| `stream` | `stream(fields, count, interval)` | 10 | Stream records lazily. Like generate() but returns iterator. | [source](https://github.com/wronai/fraq/blob/main/fraq/api.py#L136) |
| `print_summary` | `print_summary(results)` | 11 ⚠️ | Print benchmark summary. | [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py#L230) |
| `run_all_benchmarks` | `run_all_benchmarks(speed_count, memory_count)` | 5 | Run all benchmarks and return results. | [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py#L190) |
| `cmd_explore` | `cmd_explore(args)` | 1 | — | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L32) |
| `cmd_files_list` | `cmd_files_list(args)` | 5 | List files in directory (ls-like). | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L92) |
| `cmd_files_search` | `cmd_files_search(args)` | 5 | Search files with natural language or explicit parameters. | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L63) |
| `cmd_files_stat` | `cmd_files_stat(args)` | 2 | Show file statistics with fractal coordinates. | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L152) |
| `cmd_network_scan` | `cmd_network_scan(args)` | 8 | Scan network for devices. | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L201) |
| `cmd_nl` | `cmd_nl(args)` | 3 | Natural language query (requires LLM). | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L164) |
| `cmd_schema` | `cmd_schema(args)` | 3 | — | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L49) |
| `cmd_stream` | `cmd_stream(args)` | 2 | — | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L39) |
| `cmd_web_crawl` | `cmd_web_crawl(args)` | 7 | Crawl website. | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L241) |
| `main` | `main(argv)` | 1 | Main entry point - 4 line orchestrator: parse -> dispatch. | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L460) |
| `generate_df` | `generate_df(fields, count, seed, output)` | 4 | Generate records with specified output format. | [source](https://github.com/wronai/fraq/blob/main/fraq/dataframes.py#L145) |
| `to_arrow` | `to_arrow(fields, count, seed)` | 2 | Generate records and return as PyArrow Table. | [source](https://github.com/wronai/fraq/blob/main/fraq/dataframes.py#L105) |
| `to_pandas` | `to_pandas(fields, count, seed)` | 2 | Generate records and return as Pandas DataFrame. | [source](https://github.com/wronai/fraq/blob/main/fraq/dataframes.py#L70) |
| `to_polars` | `to_polars(fields, count, seed)` | 2 | Generate records and return as Polars DataFrame. | [source](https://github.com/wronai/fraq/blob/main/fraq/dataframes.py#L35) |
| `mp_encode` | `mp_encode(obj)` | 11 ⚠️ | Minimal msgpack-ish encoder. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/binary.py#L38) |
| `to_binary` | `to_binary(data)` | 3 | Minimal tagged binary encoding. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/binary.py#L16) |
| `to_msgpack_lite` | `to_msgpack_lite(data)` | 1 | Ultra-light MessagePack-ish encoding (no external deps). | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/binary.py#L33) |
| `encode_value` | `encode_value(v)` | 6 | Encode a single value to binary format. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/prepare.py#L32) |
| `prepare` | `prepare(obj)` | 8 | Recursively convert FraqNode / bytes / tuples for JSON compat. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/prepare.py#L14) |
| `simple_yaml` | `simple_yaml(obj, indent)` | 7 | Dead-simple YAML emitter (no dependency). | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L50) |
| `to_csv` | `to_csv(data)` | 4 | Serialise list of flat dicts to CSV. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L31) |
| `to_json` | `to_json(data)` | 1 | Serialise to JSON string. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L18) |
| `to_jsonl` | `to_jsonl(data)` | 3 | Serialise iterable of records to JSON-Lines. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L23) |
| `to_yaml` | `to_yaml(data)` | 1 | Serialise to YAML (simple dumper, no PyYAML dependency). | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L45) |
| `create_ifs` | `create_ifs(pattern, seed)` | 3 | Factory function to create pre-configured IFS generators. | [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py#L251) |
| `infer_fractal` | `infer_fractal(data, min_depth, max_depth)` | 2 | Infer fractal schema from existing data. | [source](https://github.com/wronai/fraq/blob/main/fraq/inference.py#L210) |
| `generate_with_faker` | `generate_with_faker(type_spec, seed)` | 1 | Convenience function to generate value with Faker. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L153) |
| `get_provider_registry` | `get_provider_registry()` | 2 | Get global provider registry. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L145) |
| `query` | `query(depth, direction, fields, format, ...)` | 5 | One-shot fractal query. | [source](https://github.com/wronai/fraq/blob/main/fraq/query.py#L197) |
| `to_asyncapi` | `to_asyncapi(schema, title, version)` | 2 | Generate an AsyncAPI 3.0 specification for streaming channels. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L348) |
| `to_graphql` | `to_graphql(schema, type_name)` | 2 | Generate a GraphQL schema definition. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L317) |
| `to_json_schema` | `to_json_schema(schema, title)` | 2 | Generate a JSON Schema for validation. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L459) |
| `to_nlp2cmd_actions` | `to_nlp2cmd_actions(schema)` | 2 | Export fraq operations as NLP2CMD ActionRegistry entries. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L149) |
| `to_nlp2cmd_schema` | `to_nlp2cmd_schema(schema, command_name, version, category)` | 5 | Export a FraqSchema as an NLP2CMD command schema. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L61) |
| `to_openapi` | `to_openapi(schema, title, version, base_path)` | 2 | Generate an OpenAPI 3.0 specification. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L208) |
| `to_proto` | `to_proto(schema, package, message_name)` | 2 | Generate a .proto file. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L408) |
| `clear_session` | `clear_session(session_id)` | 2 | Clear a conversation session. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L207) |
| `files_nl` | `files_nl(query, path)` | 1 | Natural language file search. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L142) |
| `files_search` | `files_search(ext, pattern, limit, sort_by, ...)` | 1 | Search files with fractal coordinates. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L112) |
| `files_search_post` | `files_search_post(request)` | 1 | Search files with POST request. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L130) |
| `health_check` | `health_check()` | 1 | Health check endpoint. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L197) |
| `natural_language` | `natural_language(query)` | 4 | Natural language → fraq result with session support. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L81) |
| `ws_stream` | `ws_stream(websocket)` | 8 | WebSocket endpoint for streaming fractal data. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L150) |
| `async_query` | `async_query(query, root, dims)` | 1 | Run a FraqQuery asynchronously (useful in async frameworks). | [source](https://github.com/wronai/fraq/blob/main/fraq/streaming.py#L66) |
| `async_stream` | `async_stream(root, count, interval, direction, ...)` | 3 | Convenience async generator with a count limit. | [source](https://github.com/wronai/fraq/blob/main/fraq/streaming.py#L78) |
| `text2filesearch` | `text2filesearch(text, base_path, fmt)` | 2 | One-liner to search files via natural language. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/shortcuts.py#L21) |
| `text2fraq` | `text2fraq(text, config, root)` | 2 | Convert text and execute query. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/shortcuts.py#L40) |
| `text2query` | `text2query(text, config)` | 2 | Convert text to ParsedQuery. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/shortcuts.py#L34) |

### `main_websocket` [source](https://github.com/wronai/fraq/blob/main/main_websocket.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `health` | `health()` | 1 | — | [source](https://github.com/wronai/fraq/blob/main/main_websocket.py#L51) |
| `ws_files` | `ws_files(websocket)` | 5 | — | [source](https://github.com/wronai/fraq/blob/main/main_websocket.py#L32) |
| `ws_stream` | `ws_stream(websocket)` | 5 | — | [source](https://github.com/wronai/fraq/blob/main/main_websocket.py#L14) |

## fraq

### `fraq.adapters` [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `BaseAdapter` | 4 | Interface every data-source adapter must implement. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/base.py#L12) |
| `FileAdapter` | 2 | Read/write fractal state from local files. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_adapter.py#L16) |
| `FileSearchAdapter` | 4 | Adapter for searching files on disk using fractal patterns. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_search.py#L78) |
| `FileSystemPort` | 4 | Port for filesystem I/O operations. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_search.py#L20) |
| `RealFileSystem` | 4 | Real filesystem implementation of FileSystemPort. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_search.py#L45) |
| `HTTPAdapter` | 2 | Fetch fractal roots from remote HTTP APIs. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/http_adapter.py#L15) |
| `HybridAdapter` | 3 | Combine roots from several adapters into one fractal. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/hybrid_adapter.py#L12) |
| `SensorAdapter` | 3 | Simulate or consume live sensor data as fractal streams. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/sensor_adapter.py#L14) |
| `SQLAdapter` | 3 | Map fractal nodes to/from relational tables. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/sql_adapter.py#L13) |

**`BaseAdapter` methods:**

- `load_root(uri)` — Materialise a root node from the source.
- `save(node, uri, fmt)` — Persist a node (or subtree) back to the source. Return the path/URI.
- `execute(query)` — Load root from *query.source_uri*, then run the query.
- `execute_iter(query)`

**`FileAdapter` methods:**

- `load_root(uri)`
- `save(node, uri, fmt)`

**`FileSearchAdapter` methods:**

- `load_root(uri)`
- `search(extension, pattern, limit, sort_by, ...)` — Search files - orchestrates I/O and applies pure logic.
- `save(node, uri, fmt)` — Save node data to file.
- `stream(extension, pattern, count)` — Stream files lazily.

**`FileSystemPort` methods:**

- `stat(path)` — Get file stats. Returns None if file doesn't exist or no permission.
- `list_files(base_path, pattern, recursive)` — List files matching pattern. Yields Path objects.
- `is_file(path)` — Check if path is a file.
- `write_bytes(path, data)` — Write bytes to file.

**`RealFileSystem` methods:**

- `stat(path)`
- `list_files(base_path, pattern, recursive)`
- `is_file(path)`
- `write_bytes(path, data)`

**`HTTPAdapter` methods:**

- `load_root(uri)`
- `save(node, uri, fmt)`

**`HybridAdapter` methods:**

- `add(adapter, uri)`
- `load_root(uri)`
- `save(node, uri, fmt)`

**`SensorAdapter` methods:**

- `load_root(uri)`
- `save(node, uri, fmt)`
- `stream(depth, count, direction)`

**`SQLAdapter` methods:**

- `load_root(uri)`
- `save(node, uri, fmt)`
- `generate_sql_function(dims)`

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `get_adapter` | `get_adapter(source)` | 3 | Factory: return the right adapter for a source type. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/registry.py#L26) |

### `fraq.adapters.base` [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/base.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `BaseAdapter` | 4 | Interface every data-source adapter must implement. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/base.py#L12) |

**`BaseAdapter` methods:**

- `load_root(uri)` — Materialise a root node from the source.
- `save(node, uri, fmt)` — Persist a node (or subtree) back to the source. Return the path/URI.
- `execute(query)` — Load root from *query.source_uri*, then run the query.
- `execute_iter(query)`

### `fraq.adapters.file_adapter` [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_adapter.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FileAdapter` | 2 | Read/write fractal state from local files. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_adapter.py#L16) |

**`FileAdapter` methods:**

- `load_root(uri)`
- `save(node, uri, fmt)`

### `fraq.adapters.file_search` [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_search.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FileSearchAdapter` | 4 | Adapter for searching files on disk using fractal patterns. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_search.py#L78) |
| `FileSystemPort` | 4 | Port for filesystem I/O operations. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_search.py#L20) |
| `RealFileSystem` | 4 | Real filesystem implementation of FileSystemPort. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/file_search.py#L45) |

**`FileSearchAdapter` methods:**

- `load_root(uri)`
- `search(extension, pattern, limit, sort_by, ...)` — Search files - orchestrates I/O and applies pure logic.
- `save(node, uri, fmt)` — Save node data to file.
- `stream(extension, pattern, count)` — Stream files lazily.

**`FileSystemPort` methods:**

- `stat(path)` — Get file stats. Returns None if file doesn't exist or no permission.
- `list_files(base_path, pattern, recursive)` — List files matching pattern. Yields Path objects.
- `is_file(path)` — Check if path is a file.
- `write_bytes(path, data)` — Write bytes to file.

**`RealFileSystem` methods:**

- `stat(path)`
- `list_files(base_path, pattern, recursive)`
- `is_file(path)`
- `write_bytes(path, data)`

### `fraq.adapters.http_adapter` [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/http_adapter.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `HTTPAdapter` | 2 | Fetch fractal roots from remote HTTP APIs. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/http_adapter.py#L15) |

**`HTTPAdapter` methods:**

- `load_root(uri)`
- `save(node, uri, fmt)`

### `fraq.adapters.hybrid_adapter` [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/hybrid_adapter.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `HybridAdapter` | 3 | Combine roots from several adapters into one fractal. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/hybrid_adapter.py#L12) |

**`HybridAdapter` methods:**

- `add(adapter, uri)`
- `load_root(uri)`
- `save(node, uri, fmt)`

### `fraq.adapters.registry` [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/registry.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `get_adapter` | `get_adapter(source)` | 3 | Factory: return the right adapter for a source type. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/registry.py#L26) |

### `fraq.adapters.sensor_adapter` [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/sensor_adapter.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `SensorAdapter` | 3 | Simulate or consume live sensor data as fractal streams. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/sensor_adapter.py#L14) |

**`SensorAdapter` methods:**

- `load_root(uri)`
- `save(node, uri, fmt)`
- `stream(depth, count, direction)`

### `fraq.adapters.sql_adapter` [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/sql_adapter.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `SQLAdapter` | 3 | Map fractal nodes to/from relational tables. | [source](https://github.com/wronai/fraq/blob/main/fraq/adapters/sql_adapter.py#L13) |

**`SQLAdapter` methods:**

- `load_root(uri)`
- `save(node, uri, fmt)`
- `generate_sql_function(dims)`

### `fraq.api` [source](https://github.com/wronai/fraq/blob/main/fraq/api.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `generate` | `generate(fields, count, seed, output)` | 6 | Generate records with simple field specification. | [source](https://github.com/wronai/fraq/blob/main/fraq/api.py#L72) |
| `quick_schema` | `quick_schema()` | 6 | Create schema from simple field names. Auto-detects types. | [source](https://github.com/wronai/fraq/blob/main/fraq/api.py#L181) |
| `stream` | `stream(fields, count, interval)` | 10 | Stream records lazily. Like generate() but returns iterator. | [source](https://github.com/wronai/fraq/blob/main/fraq/api.py#L136) |

### `fraq.benchmarks` [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `BenchmarkResult` | 0 | Single benchmark result. | [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py#L22) |
| `MemoryBenchmark` | 2 | Benchmark memory usage - fraq's zero-storage advantage. | [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py#L81) |
| `SpeedBenchmark` | 2 | Benchmark generation speed. | [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py#L31) |
| `StructuralBenchmark` | 2 | Benchmark fractal self-similarity vs random data. | [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py#L139) |

**`MemoryBenchmark` methods:**

- `measure_memory_usage(generator_fn, count)` — Measure peak memory usage during generation.
- `compare_memory(count)` — Compare memory usage of different approaches.

**`SpeedBenchmark` methods:**

- `fraq_generate(count)` — Benchmark fraq generate().
- `fraq_stream(count)` — Benchmark fraq streaming (lazy).

**`StructuralBenchmark` methods:**

- `test_self_similarity(data, column)` — Test if data has self-similar structure.
- `compare_structures()` — Compare structural properties of different generators.

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `print_summary` | `print_summary(results)` | 11 ⚠️ | Print benchmark summary. | [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py#L230) |
| `run_all_benchmarks` | `run_all_benchmarks(speed_count, memory_count)` | 5 | Run all benchmarks and return results. | [source](https://github.com/wronai/fraq/blob/main/fraq/benchmarks.py#L190) |

### `fraq.cli` [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `cmd_explore` | `cmd_explore(args)` | 1 | — | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L32) |
| `cmd_files_list` | `cmd_files_list(args)` | 5 | List files in directory (ls-like). | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L92) |
| `cmd_files_search` | `cmd_files_search(args)` | 5 | Search files with natural language or explicit parameters. | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L63) |
| `cmd_files_stat` | `cmd_files_stat(args)` | 2 | Show file statistics with fractal coordinates. | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L152) |
| `cmd_network_scan` | `cmd_network_scan(args)` | 8 | Scan network for devices. | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L201) |
| `cmd_nl` | `cmd_nl(args)` | 3 | Natural language query (requires LLM). | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L164) |
| `cmd_schema` | `cmd_schema(args)` | 3 | — | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L49) |
| `cmd_stream` | `cmd_stream(args)` | 2 | — | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L39) |
| `cmd_web_crawl` | `cmd_web_crawl(args)` | 7 | Crawl website. | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L241) |
| `main` | `main(argv)` | 1 | Main entry point - 4 line orchestrator: parse -> dispatch. | [source](https://github.com/wronai/fraq/blob/main/fraq/cli.py#L460) |

### `fraq.core` [source](https://github.com/wronai/fraq/blob/main/fraq/core.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FieldDef` | 0 | One field in a FraqSchema. | [source](https://github.com/wronai/fraq/blob/main/fraq/core.py#L216) |
| `FraqCursor` | 6 | Stateful walk through the fractal. | [source](https://github.com/wronai/fraq/blob/main/fraq/core.py#L359) |
| `FraqNode` | 4 | A single point in the infinite fractal data space. | [source](https://github.com/wronai/fraq/blob/main/fraq/core.py#L70) |
| `FraqSchema` | 3 | Typed projection of a fractal into structured records. | [source](https://github.com/wronai/fraq/blob/main/fraq/core.py#L226) |

**`FraqCursor` methods:**

- `advance(direction)` — Move one level deeper and return the new node.
- `back()` — Go up one level.
- `reset()` — Return to root.
- `snapshot()` — Serialisable state.

**`FraqNode` methods:**

- `zoom(direction)` — Zoom into the fractal along *direction* by *steps* levels.
- `children(directions)` — Return children in several directions (auto-generated if omitted).
- `to_dict(max_depth)` — Snapshot of this node as a plain dict.

**`FraqSchema` methods:**

- `add_field(name, type, direction, transform)`
- `record(node)` — Produce a single record from *node* (defaults to root).
- `records(depth, branching, count, node)` — Yield records by exploring children.

### `fraq.dataframes` [source](https://github.com/wronai/fraq/blob/main/fraq/dataframes.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `generate_df` | `generate_df(fields, count, seed, output)` | 4 | Generate records with specified output format. | [source](https://github.com/wronai/fraq/blob/main/fraq/dataframes.py#L145) |
| `to_arrow` | `to_arrow(fields, count, seed)` | 2 | Generate records and return as PyArrow Table. | [source](https://github.com/wronai/fraq/blob/main/fraq/dataframes.py#L105) |
| `to_pandas` | `to_pandas(fields, count, seed)` | 2 | Generate records and return as Pandas DataFrame. | [source](https://github.com/wronai/fraq/blob/main/fraq/dataframes.py#L70) |
| `to_polars` | `to_polars(fields, count, seed)` | 2 | Generate records and return as Polars DataFrame. | [source](https://github.com/wronai/fraq/blob/main/fraq/dataframes.py#L35) |

### `fraq.formats` [source](https://github.com/wronai/fraq/blob/main/fraq/formats/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FormatRegistry` | 4 | Registry of serialisation backends. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/registry.py#L10) |

**`FormatRegistry` methods:**

- `register(cls, name, fn)` — Register a formatter. Can be used as a decorator.
- `get(cls, name)`
- `available(cls)`
- `serialize(cls, name, data)`

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `mp_encode` | `mp_encode(obj)` | 11 ⚠️ | Minimal msgpack-ish encoder. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/binary.py#L38) |
| `to_binary` | `to_binary(data)` | 3 | Minimal tagged binary encoding. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/binary.py#L16) |
| `to_msgpack_lite` | `to_msgpack_lite(data)` | 1 | Ultra-light MessagePack-ish encoding (no external deps). | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/binary.py#L33) |
| `encode_value` | `encode_value(v)` | 6 | Encode a single value to binary format. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/prepare.py#L32) |
| `prepare` | `prepare(obj)` | 8 | Recursively convert FraqNode / bytes / tuples for JSON compat. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/prepare.py#L14) |
| `simple_yaml` | `simple_yaml(obj, indent)` | 7 | Dead-simple YAML emitter (no dependency). | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L50) |
| `to_csv` | `to_csv(data)` | 4 | Serialise list of flat dicts to CSV. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L31) |
| `to_json` | `to_json(data)` | 1 | Serialise to JSON string. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L18) |
| `to_jsonl` | `to_jsonl(data)` | 3 | Serialise iterable of records to JSON-Lines. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L23) |
| `to_yaml` | `to_yaml(data)` | 1 | Serialise to YAML (simple dumper, no PyYAML dependency). | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L45) |

### `fraq.formats.binary` [source](https://github.com/wronai/fraq/blob/main/fraq/formats/binary.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `mp_encode` | `mp_encode(obj)` | 11 ⚠️ | Minimal msgpack-ish encoder. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/binary.py#L38) |
| `to_binary` | `to_binary(data)` | 3 | Minimal tagged binary encoding. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/binary.py#L16) |
| `to_msgpack_lite` | `to_msgpack_lite(data)` | 1 | Ultra-light MessagePack-ish encoding (no external deps). | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/binary.py#L33) |

### `fraq.formats.prepare` [source](https://github.com/wronai/fraq/blob/main/fraq/formats/prepare.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `encode_value` | `encode_value(v)` | 6 | Encode a single value to binary format. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/prepare.py#L32) |
| `prepare` | `prepare(obj)` | 8 | Recursively convert FraqNode / bytes / tuples for JSON compat. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/prepare.py#L14) |

### `fraq.formats.registry` [source](https://github.com/wronai/fraq/blob/main/fraq/formats/registry.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FormatRegistry` | 4 | Registry of serialisation backends. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/registry.py#L10) |

**`FormatRegistry` methods:**

- `register(cls, name, fn)` — Register a formatter. Can be used as a decorator.
- `get(cls, name)`
- `available(cls)`
- `serialize(cls, name, data)`

### `fraq.formats.text` [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `simple_yaml` | `simple_yaml(obj, indent)` | 7 | Dead-simple YAML emitter (no dependency). | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L50) |
| `to_csv` | `to_csv(data)` | 4 | Serialise list of flat dicts to CSV. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L31) |
| `to_json` | `to_json(data)` | 1 | Serialise to JSON string. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L18) |
| `to_jsonl` | `to_jsonl(data)` | 3 | Serialise iterable of records to JSON-Lines. | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L23) |
| `to_yaml` | `to_yaml(data)` | 1 | Serialise to YAML (simple dumper, no PyYAML dependency). | [source](https://github.com/wronai/fraq/blob/main/fraq/formats/text.py#L45) |

### `fraq.generators` [source](https://github.com/wronai/fraq/blob/main/fraq/generators.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FibonacciGenerator` | 0 | Value based on generalised Fibonacci sequence at the node's depth. | [source](https://github.com/wronai/fraq/blob/main/fraq/generators.py#L44) |
| `HashGenerator` | 0 | Deterministic pseudo-random values via SHA-256. | [source](https://github.com/wronai/fraq/blob/main/fraq/generators.py#L19) |
| `PerlinGenerator` | 0 | Simplified 1-D Perlin-ish noise from the L2 norm of position. | [source](https://github.com/wronai/fraq/blob/main/fraq/generators.py#L66) |
| `SensorStreamGenerator` | 0 | Simulate an infinite IoT sensor stream. | [source](https://github.com/wronai/fraq/blob/main/fraq/generators.py#L88) |

### `fraq.ifs` [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `AffineTransform` | 1 | Affine transformation for IFS. | [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py#L38) |
| `IFSGenerator` | 3 | Iterated Function System generator. | [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py#L66) |
| `NetworkMapper` | 1 | Mapper for network topology data. | [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py#L229) |
| `OrganizationalMapper` | 1 | Mapper for organizational hierarchy data. | [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py#L196) |
| `ValueMapper` | 1 | Protocol for mapping fractal coordinates to data values. | [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py#L58) |

**`IFSGenerator` methods:**

- `generate_coordinate(depth, start)` — Generate a fractal coordinate at given depth.
- `generate(count, depth, mapper)` — Generate records with fractal structure.
- `generate_hierarchy(root, branching, depth)` — Generate hierarchical data (tree structure).

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `create_ifs` | `create_ifs(pattern, seed)` | 3 | Factory function to create pre-configured IFS generators. | [source](https://github.com/wronai/fraq/blob/main/fraq/ifs.py#L251) |

### `fraq.inference` [source](https://github.com/wronai/fraq/blob/main/fraq/inference.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FractalAnalyzer` | 3 | Analyze data for fractal properties. | [source](https://github.com/wronai/fraq/blob/main/fraq/inference.py#L56) |
| `FractalDimension` | 0 | Fractal dimension analysis result. | [source](https://github.com/wronai/fraq/blob/main/fraq/inference.py#L39) |
| `InferredSchema` | 2 | Schema inferred from real data with fractal properties. | [source](https://github.com/wronai/fraq/blob/main/fraq/inference.py#L250) |
| `PatternSignature` | 0 | Detected pattern in data column. | [source](https://github.com/wronai/fraq/blob/main/fraq/inference.py#L47) |

**`FractalAnalyzer` methods:**

- `box_counting_dimension(values, min_box_size, max_box_size)` — Calculate box-counting dimension of value distribution.
- `detect_hierarchy(data, parent_column)` — Detect hierarchical structure in data.
- `analyze_correlations(data)` — Analyze correlations between columns for fractal relationships.

**`InferredSchema` methods:**

- `generate(count, seed)` — Generate synthetic data with same fractal structure.
- `to_dict()` — Serialize to dictionary.

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `infer_fractal` | `infer_fractal(data, min_depth, max_depth)` | 2 | Infer fractal schema from existing data. | [source](https://github.com/wronai/fraq/blob/main/fraq/inference.py#L210) |

### `fraq.providers` [source](https://github.com/wronai/fraq/blob/main/fraq/providers/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FakerProvider` | 2 | Faker-based value provider for realistic data generation. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L36) |
| `ProviderRegistry` | 4 | Registry of value providers. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L104) |
| `ValueProvider` | 2 | Protocol for value providers. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L24) |

**`FakerProvider` methods:**

- `supports(type_spec)` — Check if type_spec is a faker specification.
- `generate(type_spec, seed)` — Generate value using Faker.

**`ProviderRegistry` methods:**

- `register(provider)` — Register a value provider.
- `get_faker_provider(locale)` — Get or create Faker provider.
- `find_provider(type_spec)` — Find provider that supports the given type specification.
- `generate(type_spec, seed)` — Generate value using appropriate provider.

**`ValueProvider` methods:**

- `supports(type_spec)` — Check if this provider supports the given type specification.
- `generate(type_spec, seed)` — Generate a value for the given type specification.

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `generate_with_faker` | `generate_with_faker(type_spec, seed)` | 1 | Convenience function to generate value with Faker. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L153) |
| `get_provider_registry` | `get_provider_registry()` | 2 | Get global provider registry. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L145) |

### `fraq.providers.faker_provider` [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FakerProvider` | 2 | Faker-based value provider for realistic data generation. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L36) |
| `ProviderRegistry` | 4 | Registry of value providers. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L104) |
| `ValueProvider` | 2 | Protocol for value providers. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L24) |

**`FakerProvider` methods:**

- `supports(type_spec)` — Check if type_spec is a faker specification.
- `generate(type_spec, seed)` — Generate value using Faker.

**`ProviderRegistry` methods:**

- `register(provider)` — Register a value provider.
- `get_faker_provider(locale)` — Get or create Faker provider.
- `find_provider(type_spec)` — Find provider that supports the given type specification.
- `generate(type_spec, seed)` — Generate value using appropriate provider.

**`ValueProvider` methods:**

- `supports(type_spec)` — Check if this provider supports the given type specification.
- `generate(type_spec, seed)` — Generate a value for the given type specification.

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `generate_with_faker` | `generate_with_faker(type_spec, seed)` | 1 | Convenience function to generate value with Faker. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L153) |
| `get_provider_registry` | `get_provider_registry()` | 2 | Get global provider registry. | [source](https://github.com/wronai/fraq/blob/main/fraq/providers/faker_provider.py#L145) |

### `fraq.query` [source](https://github.com/wronai/fraq/blob/main/fraq/query.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FraqExecutor` | 2 | Execute a FraqQuery against a root node. | [source](https://github.com/wronai/fraq/blob/main/fraq/query.py#L147) |
| `FraqFilter` | 1 | Post-zoom predicate on a record field. | [source](https://github.com/wronai/fraq/blob/main/fraq/query.py#L42) |
| `FraqQuery` | 6 | Declarative query against fractal data. | [source](https://github.com/wronai/fraq/blob/main/fraq/query.py#L70) |
| `SourceType` | 0 | Known data source families. | [source](https://github.com/wronai/fraq/blob/main/fraq/query.py#L30) |

**`FraqExecutor` methods:**

- `execute(query)` — Run *query* and return serialised output.
- `execute_iter(query)` — Lazily yield filtered records (no serialisation).

**`FraqQuery` methods:**

- `zoom(depth, direction)`
- `select()` — Add fields, e.g. ``q.select("name:str", "value:float")``.
- `where(field, op, value)`
- `output(fmt)`
- `take(n)`
- `from_source(source, uri)`

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `query` | `query(depth, direction, fields, format, ...)` | 5 | One-shot fractal query. | [source](https://github.com/wronai/fraq/blob/main/fraq/query.py#L197) |

### `fraq.schema_export` [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `to_asyncapi` | `to_asyncapi(schema, title, version)` | 2 | Generate an AsyncAPI 3.0 specification for streaming channels. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L348) |
| `to_graphql` | `to_graphql(schema, type_name)` | 2 | Generate a GraphQL schema definition. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L317) |
| `to_json_schema` | `to_json_schema(schema, title)` | 2 | Generate a JSON Schema for validation. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L459) |
| `to_nlp2cmd_actions` | `to_nlp2cmd_actions(schema)` | 2 | Export fraq operations as NLP2CMD ActionRegistry entries. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L149) |
| `to_nlp2cmd_schema` | `to_nlp2cmd_schema(schema, command_name, version, category)` | 5 | Export a FraqSchema as an NLP2CMD command schema. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L61) |
| `to_openapi` | `to_openapi(schema, title, version, base_path)` | 2 | Generate an OpenAPI 3.0 specification. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L208) |
| `to_proto` | `to_proto(schema, package, message_name)` | 2 | Generate a .proto file. | [source](https://github.com/wronai/fraq/blob/main/fraq/schema_export.py#L408) |

### `fraq.server` [source](https://github.com/wronai/fraq/blob/main/fraq/server.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FilesSearchRequest` | 0 | File search request. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L71) |
| `NLQueryRequest` | 0 | Natural language query request. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L57) |
| `NLQueryResponse` | 0 | Natural language query response. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L64) |

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `clear_session` | `clear_session(session_id)` | 2 | Clear a conversation session. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L207) |
| `files_nl` | `files_nl(query, path)` | 1 | Natural language file search. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L142) |
| `files_search` | `files_search(ext, pattern, limit, sort_by, ...)` | 1 | Search files with fractal coordinates. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L112) |
| `files_search_post` | `files_search_post(request)` | 1 | Search files with POST request. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L130) |
| `health_check` | `health_check()` | 1 | Health check endpoint. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L197) |
| `natural_language` | `natural_language(query)` | 4 | Natural language → fraq result with session support. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L81) |
| `ws_stream` | `ws_stream(websocket)` | 8 | WebSocket endpoint for streaming fractal data. | [source](https://github.com/wronai/fraq/blob/main/fraq/server.py#L150) |

### `fraq.streaming` [source](https://github.com/wronai/fraq/blob/main/fraq/streaming.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `AsyncFraqStream` | 2 | Async generator that yields fractal records at a controlled rate. | [source](https://github.com/wronai/fraq/blob/main/fraq/streaming.py#L17) |

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `async_query` | `async_query(query, root, dims)` | 1 | Run a FraqQuery asynchronously (useful in async frameworks). | [source](https://github.com/wronai/fraq/blob/main/fraq/streaming.py#L66) |
| `async_stream` | `async_stream(root, count, interval, direction, ...)` | 3 | Convenience async generator with a count limit. | [source](https://github.com/wronai/fraq/blob/main/fraq/streaming.py#L78) |

### `fraq.text2fraq` [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Text2FraqConfig` | 1 | Configuration for text2fraq. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/config.py#L14) |
| `FileSearchText2Fraq` | 3 | Natural language to file search converter. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/file_search_parser.py#L17) |
| `LiteLLMClient` | 1 | LiteLLM client for text completion. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/llm_client.py#L15) |
| `LLMClient` | 1 | Protocol for LLM clients. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/models.py#L38) |
| `ParsedQuery` | 1 | Parsed natural language query. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/models.py#L12) |
| `Text2Fraq` | 2 | Natural language to fractal query converter (LLM-based). | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/parser_llm.py#L17) |
| `Text2FraqSimple` | 2 | Rule-based text2fraq without LLM (fallback for offline use). | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/parser_rules.py#L43) |
| `ModelRouter` | 2 | Route queries to the best model based on complexity. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/router.py#L11) |
| `FraqSession` | 3 | Multi-turn conversation with context memory. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/session.py#L15) |

**`FileSearchText2Fraq` methods:**

- `parse(text)` — Parse natural language file query to search parameters.
- `search(text)` — Parse query and execute file search.
- `format_results(results, fmt, fields)` — Format file search results to specified format.

**`Text2Fraq` methods:**

- `parse(text)` — Parse natural language text to structured query.
- `execute(text, root)` — Parse text and execute query immediately.

**`Text2FraqSimple` methods:**

- `parse(text)` — Parse using rule-based matching.
- `execute(text, root)` — Parse and execute query.

**`ModelRouter` methods:**

- `route(text)` — Select best model based on query complexity.
- `get_config_for_model(model)` — Get recommended config for model.

**`FraqSession` methods:**

- `ask(text)` — Process query with context awareness.
- `get_context_summary()` — Get summary of current session context.
- `clear()` — Clear session history and context.

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `text2filesearch` | `text2filesearch(text, base_path, fmt)` | 2 | One-liner to search files via natural language. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/shortcuts.py#L21) |
| `text2fraq` | `text2fraq(text, config, root)` | 2 | Convert text and execute query. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/shortcuts.py#L40) |
| `text2query` | `text2query(text, config)` | 2 | Convert text to ParsedQuery. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/shortcuts.py#L34) |

### `fraq.text2fraq.config` [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/config.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Text2FraqConfig` | 1 | Configuration for text2fraq. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/config.py#L14) |

### `fraq.text2fraq.file_search_parser` [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/file_search_parser.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FileSearchText2Fraq` | 3 | Natural language to file search converter. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/file_search_parser.py#L17) |

**`FileSearchText2Fraq` methods:**

- `parse(text)` — Parse natural language file query to search parameters.
- `search(text)` — Parse query and execute file search.
- `format_results(results, fmt, fields)` — Format file search results to specified format.

### `fraq.text2fraq.llm_client` [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/llm_client.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `LiteLLMClient` | 1 | LiteLLM client for text completion. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/llm_client.py#L15) |

### `fraq.text2fraq.models` [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/models.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `LLMClient` | 1 | Protocol for LLM clients. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/models.py#L38) |
| `ParsedQuery` | 1 | Parsed natural language query. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/models.py#L12) |

### `fraq.text2fraq.parser_llm` [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/parser_llm.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Text2Fraq` | 2 | Natural language to fractal query converter (LLM-based). | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/parser_llm.py#L17) |

**`Text2Fraq` methods:**

- `parse(text)` — Parse natural language text to structured query.
- `execute(text, root)` — Parse text and execute query immediately.

### `fraq.text2fraq.parser_rules` [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/parser_rules.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Text2FraqSimple` | 2 | Rule-based text2fraq without LLM (fallback for offline use). | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/parser_rules.py#L43) |

**`Text2FraqSimple` methods:**

- `parse(text)` — Parse using rule-based matching.
- `execute(text, root)` — Parse and execute query.

### `fraq.text2fraq.router` [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/router.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `ModelRouter` | 2 | Route queries to the best model based on complexity. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/router.py#L11) |

**`ModelRouter` methods:**

- `route(text)` — Select best model based on query complexity.
- `get_config_for_model(model)` — Get recommended config for model.

### `fraq.text2fraq.session` [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/session.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FraqSession` | 3 | Multi-turn conversation with context memory. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/session.py#L15) |

**`FraqSession` methods:**

- `ask(text)` — Process query with context awareness.
- `get_context_summary()` — Get summary of current session context.
- `clear()` — Clear session history and context.

### `fraq.text2fraq.shortcuts` [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/shortcuts.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `text2filesearch` | `text2filesearch(text, base_path, fmt)` | 2 | One-liner to search files via natural language. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/shortcuts.py#L21) |
| `text2fraq` | `text2fraq(text, config, root)` | 2 | Convert text and execute query. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/shortcuts.py#L40) |
| `text2query` | `text2query(text, config)` | 2 | Convert text to ParsedQuery. | [source](https://github.com/wronai/fraq/blob/main/fraq/text2fraq/shortcuts.py#L34) |
