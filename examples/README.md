# fraq — Przykłady

Kompletne przykłady użycia biblioteki fraq z różnymi technologiami.

## 📁 Struktura

```
examples/
├── basic/                         # Podstawowe przykłady
│   ├── query_examples.py          # Zapytania i formaty
│   ├── applications.py            # IoT, ERP, Finance
│   ├── async_streaming.py         # Async/SSE/Kafka
│   └── app_integrations.py        # FastAPI/Streamlit/Flask
│
├── text2fraq/                     # Natural language
│   ├── text2fraq_examples.py      # NL do zapytań
│   ├── text2fraq_files.py         # NL wyszukiwanie plików
│   └── nlp2cmd_integration.py     # NLP2CMD schema
│
├── v028/                          # Nowe funkcje v0.2.10
│   └── new_features.py            # ModelRouter, FraqSession
│
├── database/                      # Bazy danych
│   └── sqlite_examples.py         # SQLite/PostgreSQL/SQL
│
├── streaming/                     # Streaming
│   └── sse_examples.py            # SSE/WebSocket/Kafka
│
├── ai_ml/                         # AI/ML
│   └── training_data.py           # Synthetic datasets
│
├── iot/                           # IoT
│   └── sensor_examples.py         # MQTT/Time-series
│
├── etl/                           # ETL/Pipelines
│   └── pipeline_examples.py       # Data pipelines
│
├── testing/                       # Testing
│   └── test_fixtures.py           # Mock data/fixtures
│
├── network/                       # Network
│   └── network_web_examples.py    # Scanning/crawling
│
├── cli-docker/                    # CLI w Docker
├── fastapi-docker/                # REST API w Docker
├── websocket-docker/              # WebSocket w Docker
├── fullstack-docker/              # Full stack w Docker
│
└── CLI_CURL_GUIDE.md              # Pełna dokumentacja
```

## 🚀 Szybki start

### Python Examples

```bash
# Podstawowe
PYTHONPATH=/home/tom/github/wronai/fraq python3 basic/query_examples.py
PYTHONPATH=/home/tom/github/wronai/fraq python3 basic/applications.py

# Nowe funkcje v0.2.10
PYTHONPATH=/home/tom/github/wronai/fraq python3 v028/new_features.py

# Nowe kategorie
PYTHONPATH=/home/tom/github/wronai/fraq python3 database/sqlite_examples.py
PYTHONPATH=/home/tom/github/wronai/fraq python3 ai_ml/training_data.py
PYTHONPATH=/home/tom/github/wronai/fraq python3 iot/sensor_examples.py
PYTHONPATH=/home/tom/github/wronai/fraq python3 etl/pipeline_examples.py
PYTHONPATH=/home/tom/github/wronai/fraq python3 testing/test_fixtures.py
PYTHONPATH=/home/tom/github/wronai/fraq python3 streaming/sse_examples.py
```

### CLI

```bash
pip install fraq[ai]

# Wyszukaj pliki
fraq files search --ext pdf --limit 10 ~

# Natural language
fraq nl "pokaż 10 najnowszych plików"
fraq nl "pokaż pliki python w folderze domowym"
```

### Docker

```bash
# CLI w Docker
cd cli-docker && ./run.sh fraq explore --depth 5

# REST API
cd fastapi-docker && ./run.sh up

# WebSocket
cd websocket-docker && ./run.sh up

# Fullstack
cd fullstack-docker && ./run.sh up
```

## 📖 Kategorie

### 🔧 Basic
| Plik | Opis |
|------|------|
| `query_examples.py` | JSON, CSV, YAML, SQL, streaming |
| `applications.py` | IoT sensors, ERP invoices, AI/ML, DevOps |
| `async_streaming.py` | Async generators, SSE, Kafka pattern |
| `app_integrations.py` | FastAPI, Streamlit, Flask templates |

### 🗄️ Database
| Plik | Opis |
|------|------|
| `sqlite_examples.py` | SQLite, PostgreSQL, SQL functions |

### 📡 Streaming
| Plik | Opis |
|------|------|
| `sse_examples.py` | SSE, WebSocket, Kafka, async stream |

### 🤖 AI/ML
| Plik | Opis |
|------|------|
| `training_data.py` | Classification, regression, time-series, NLP |

### 🔌 IoT
| Plik | Opis |
|------|------|
| `sensor_examples.py` | MQTT, anomalies, device registry, edge computing |

### 🔄 ETL
| Plik | Opis |
|------|------|
| `pipeline_examples.py` | Multi-source extract, transform, validate, load |

### 🧪 Testing
| Plik | Opis |
|------|------|
| `test_fixtures.py` | Unit tests, mock APIs, property-based, load testing |

### 🌐 Network
| Plik | Opis |
|------|------|
| `network_web_examples.py` | Network scanning, web crawling |

### 💬 Natural Language
| Plik | Opis |
|------|------|
| `text2fraq_examples.py` | Rule-based + LLM parsing |
| `text2fraq_files.py` | NL file search |
| `nlp2cmd_integration.py` | NLP2CMD schema export |

### 🆕 Nowe funkcje v0.2.10
| Plik | Opis |
|------|------|
| `v028/new_features.py` | ModelRouter, FraqSession, FastAPI |

## 🐳 Docker

Alternatywnie, użyj głównego `docker-compose.yml` w root projektu:

```bash
# Wszystkie usługi
docker-compose up -d

# Tylko API
docker-compose up fraq-api -d

# CLI (on-demand)
docker-compose --profile cli run fraq-cli files search /host/home
```

## 🔧 Wymagania

- **CLI**: `pip install fraq[ai]`
- **Docker**: Docker + docker-compose
- **WebSocket test**: `websocat` (opcjonalnie)

## 📚 Więcej

- Główny README: `../README.md`
- Dokumentacja API: `CLI_CURL_GUIDE.md`
- Testy: `../tests/`
