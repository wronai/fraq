# fraq — Configuration Reference

> Project metadata, dependencies, environment, deployment, and release management.

## Metadata

| Property | Value |
|----------|-------|
| **name** | `fraq` |
| **version** | `0.2.14` |
| **python_requires** | `>=3.10` |
| **license** | Apache-2.0 |
| **ecosystem** | SUMD + DOQL + testql + taskfile |

## Configuration

```yaml
project:
  name: fraq
  version: 0.2.14
  env: local
```

## Dependencies

### Runtime

*(see `pyproject.toml`)*

### Development

```text
pytest>=7.0
pytest-cov>=4.0
pytest-asyncio>=0.21.0
mypy>=1.0
ruff>=0.1.0
faker>=20.0
polars>=1.0
```

## Deployment

```bash
pip install fraq

# development install
pip install -e .[dev]
```

### Docker

- **base image**: `python:3.11-slim`
- **expose**: `8000`
- **entrypoint**: `["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`

### Docker Compose (`docker-compose.yml`)

| Service | Context | Dockerfile | Ports |
|---------|---------|------------|-------|
| **fraq-api** | `.` | `Dockerfile` | `8000:8000` |
| **fraq-websocket** | `.` | `Dockerfile.websocket` | `8001:8001` |
| **fraq-cli** | `.` | `Dockerfile.cli` | — |

## Environment Variables (`.env.example`)

| Variable | Default | Description |
|----------|---------|-------------|
| `LITELLM_PROVIDER` | `ollama` | API provider: openai, ollama, anthropic, cohere, etc. |
| `LITELLM_MODEL` | `qwen2.5:3b` | Model name (supports small models like qwen2.5:3b, llama3.2:3b, phi3:3.8b) |
| `LITELLM_API_KEY` | *(not set)* | Leave empty for local models via Ollama |
| `LITELLM_BASE_URL` | `http://localhost:11434` | Base URL for API (e.g., for Ollama: http://localhost:11434, for OpenRouter) |
| `LITELLM_TEMPERATURE` | `0.1` | Temperature for generation (0.0 - 1.0, lower = more deterministic) |
| `LITELLM_MAX_TOKENS` | `512` | Max tokens per request |
| `LITELLM_TIMEOUT` | `30` | Timeout in seconds |
| `TEXT2FRAQ_DEFAULT_FORMAT` | `json` | Default output format: json, csv, yaml, jsonl |
| `TEXT2FRAQ_DEFAULT_DIMS` | `3` | Default dimensions for fractal (2-10) |
| `TEXT2FRAQ_DEFAULT_DEPTH` | `3` | Default depth for queries (1-20) |
| `TEXT2FRAQ_CACHE_ENABLED` | `true` | Enable caching of parsed queries |
| `TEXT2FRAQ_CACHE_TTL` | `3600` | Cache TTL in seconds (3600 = 1 hour) |
| `SENSOR_BASE_TEMP` | `23.5` | IoT/Sensor simulation settings |
| `SENSOR_BASE_HUMIDITY` | `60.0` |  |
| `SENSOR_SAMPLE_HZ` | `10` |  |
| `DATABASE_URL` | `sqlite:///fraq_examples.db` | Example: postgresql://user:pass@localhost/fraq or sqlite:///fraq.db |
| `HTTP_API_BASE_URL` | `https://api.example.com` | HTTP API base URL (for HTTP adapter examples) |
| `ENABLE_IOT_EXAMPLES` | `true` | Enable/disable specific examples |
| `ENABLE_ERP_EXAMPLES` | `true` |  |
| `ENABLE_FINANCE_EXAMPLES` | `true` |  |
| `ENABLE_LEGAL_EXAMPLES` | `true` |  |
| `ENABLE_AI_ML_EXAMPLES` | `true` |  |
| `ENABLE_DEVOPS_EXAMPLES` | `true` |  |

## Quality Pipeline (`pyqual.yaml`)

```yaml
pipeline:
  name: fraq-quality

  metrics:
    cc_max: 15
    critical_max: 0

  custom_tools:
    - name: code2llm_fraq
      binary: code2llm
      command: >-
        code2llm {workdir} -f toon -o ./project --no-chunk
        --exclude .git .venv .venv_test build dist __pycache__ .pytest_cache .code2llm_cache .benchmarks .mypy_cache .ruff_cache node_modules
      output: ""
      allow_failure: false

    - name: vallm_fraq
      binary: vallm
      command: >-
        vallm batch {workdir} --recursive --format toon --output ./project
        --exclude .git,.venv,.venv_test,build,dist,__pycache__,.pytest_cache,.code2llm_cache,.benchmarks,.mypy_cache,.ruff_cache,node_modules
      output: ""
      allow_failure: false

  stages:
    - name: analyze
      tool: code2llm_fraq
      optional: true
      timeout: 0

    - name: validate
      tool: vallm_fraq
      optional: true
      timeout: 0

    - name: lint
      tool: ruff
      optional: true

    - name: fix
      tool: prefact
      optional: true
      when: metrics_fail
      timeout: 900

    - name: test
      run: python3 -m pytest -q
      when: always

  loop:
    max_iterations: 3
    on_fail: report

  env:
    LLM_MODEL: openrouter/qwen/qwen3-coder-next
```

## Release Management (`goal.yaml`)

- **versioning**: `semver`
- **commits**: `conventional` scope=`fraq`
- **changelog**: `keep-a-changelog`
- **build strategies**: `python`, `nodejs`, `rust`
- **version files**: `VERSION`, `pyproject.toml:version`, `fraq/__init__.py:__version__`