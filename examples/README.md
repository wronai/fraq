# fraq — Przykłady

Kompletne przykłady użycia biblioteki fraq z różnymi technologiami.

## 📁 Struktura

```
examples/
├── CLI & curl/                    # Użycie bez Docker
│   ├── CLI_CURL_GUIDE.md         # Pełna dokumentacja CLI/API
│   └── bash_examples.sh          # Skrypt z przykładami bash/curl
│
├── fastapi-docker/                # REST API w Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── main.py                   # Aplikacja FastAPI
│   ├── run.sh                    # Skrypt uruchamiający (bash)
│   ├── run.py                    # Skrypt uruchamiający (python)
│   └── README.md
│
├── cli-docker/                    # CLI w Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── run.sh
│   ├── run.py
│   └── README.md
│
├── websocket-docker/              # WebSocket w Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── main.py
│   ├── run.sh
│   ├── run.py
│   └── README.md
│
├── fullstack-docker/              # Kompletny stack w Docker
│   ├── docker-compose.yml
│   ├── api/                      # Usługa REST API
│   ├── websocket/                # Usługa WebSocket
│   ├── frontend/                 # Streamlit frontend
│   ├── run.sh
│   ├── run.py
│   └── README.md
│
└── (pliki Python)                 # Przykłady bez Docker
    ├── api_server.py             # Pełny serwer API (FastAPI + WS)
    ├── text2fraq_examples.py     # Przykłady text2fraq
    ├── text2fraq_files.py        # Przykłady wyszukiwania plików
    ├── query_examples.py         # Przykłady zapytań
    ├── applications.py           # Zastosowania praktyczne
    ├── async_streaming.py        # Streaming asynchroniczny
    └── nlp2cmd_integration.py    # Integracja NLP2CMD
```

## 🚀 Szybki start

### 1. CLI (natywnie)

```bash
pip install fraq[ai]

# Wyszukaj pliki
fraq files search --ext pdf --limit 10 ~

# Natural language
fraq nl "pokaż 10 najnowszych plików"
```

### 2. REST API (Docker)

```bash
cd examples/fastapi-docker
./run.sh up

# Test
curl 'http://localhost:8000/files/search?ext=pdf&limit=5'
```

### 3. Fullstack (Docker)

```bash
cd examples/fullstack-docker
./run.sh up

# Otwórz:
# - Frontend: http://localhost:8501
# - API: http://localhost:8000
```

## 📖 Dokumentacja

| Przykład | Opis | Uruchomienie |
|----------|------|--------------|
| `fastapi-docker/` | REST API | `./run.sh up` |
| `cli-docker/` | CLI w kontenerze | `./run.sh [komenda]` |
| `websocket-docker/` | WebSocket streaming | `./run.sh up` |
| `fullstack-docker/` | API + WS + Frontend | `./run.sh up` |
| `CLI_CURL_GUIDE.md` | Kompletna dokumentacja CLI/API | - |

## 🐳 Docker Compose (root)

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
