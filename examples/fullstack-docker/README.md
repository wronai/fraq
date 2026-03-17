# Fullstack fraq w Docker

Kompletny stack: REST API + WebSocket + Frontend (Streamlit)

## Szybki start

```bash
cd examples/fullstack-docker
docker-compose up --build

# Usługi:
# - API:      http://localhost:8000
# - WebSocket: ws://localhost:8001
# - Frontend: http://localhost:8501 (Streamlit)
```

## Architektura

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Streamlit  │────▶│  FastAPI    │────▶│  fraq core  │
│  (frontend) │     │  (REST API) │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  WebSocket  │
                     │  (real-time)│
                     └─────────────┘
```

## Endpointy

- **Frontend**: http://localhost:8501 - interaktywna aplikacja
- **REST API**: http://localhost:8000
  - `/explore` - eksploracja fraktala
  - `/files/search` - wyszukiwanie plików
  - `/health` - health check
- **WebSocket**: ws://localhost:8001
  - `/ws/stream` - streaming fraktalny
  - `/ws/files` - streaming plików

## Użycie

### 1. Frontend (Streamlit)
Otwórz http://localhost:8501 w przeglądarce.

Funkcje:
- Wyszukiwanie plików z UI
- Eksploracja fraktala
- Streamingu danych w czasie rzeczywistym

### 2. API bezpośrednio
```bash
# Wyszukaj pliki
curl 'http://localhost:8000/files/search?ext=pdf&limit=5'

# Eksploruj fraktal
curl 'http://localhost:8000/explore?depth=3'
```

### 3. WebSocket
```bash
websocat ws://localhost:8001/ws/stream
{"action": "stream", "count": 10}
```

## Konfiguracja

Zmienne w `.env`:
```env
FRAQ_DIMS=3
FRAQ_SEED=0
LITELLM_MODEL=qwen2.5:3b
```

## Rozwijanie

```bash
# Rebuild po zmianach
docker-compose up --build

# Logi
docker-compose logs -f api

# Zatrzymaj
docker-compose down
```
