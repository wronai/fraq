# FastAPI + fraq w Docker

REST API do obsługi zapytań fraktalnych i wyszukiwania plików.

## Szybki start

```bash
cd examples/fastapi-docker
docker-compose up --build

# API dostępne na http://localhost:8000
```

## Endpointy

- `GET /` - info
- `GET /health` - health check
- `GET /explore?depth=3&dims=3` - eksploracja fraktala
- `GET /files/search?ext=pdf&limit=10` - wyszukiwanie plików
- `GET /files/stat/{path}` - statystyki pliku

## Przykłady użycia

```bash
# Health check
curl http://localhost:8000/health

# Wyszukaj pliki PDF
curl 'http://localhost:8000/files/search?ext=pdf&limit=5' | jq .

# Eksploruj fraktal
curl 'http://localhost:8000/explore?depth=3&format=json' | jq .
```

## Konfiguracja

Zmienne środowiskowe w `docker-compose.yml`:
- `FRAQ_DIMS` - wymiary (default: 3)
- `FRAQ_SEED` - seed (default: 0)
