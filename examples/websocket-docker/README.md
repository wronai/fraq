# WebSocket + fraq w Docker

WebSocket server do streamingu danych fraktalnych i plików w czasie rzeczywistym.

## Szybki start

```bash
cd examples/websocket-docker
docker-compose up --build

# WebSocket dostępny na ws://localhost:8001/ws
```

## Testowanie

### websocat (zalecane)
```bash
# Zainstaluj websocat
sudo apt install websocat

# Streamuj fraktal
websocat ws://localhost:8001/ws/stream
{"action": "stream", "count": 10, "interval": 0.5}

# Wyszukaj pliki
websocat ws://localhost:8001/ws/files
{"action": "search", "path": "/data", "ext": "py", "limit": 5}
```

### wscat (Node.js)
```bash
npm install -g wscat
wscat -c ws://localhost:8001/ws/stream
```

## Endpointy WebSocket

- `/ws/stream` - streaming fraktalny
- `/ws/files` - streaming wyszukiwania plików

## Przykłady wiadomości

```json
// Stream fraktala
{"action": "stream", "count": 50, "interval": 0.1}

// Ping
{"action": "ping"}

// Search files
{"action": "search", "path": "/data", "ext": "pdf", "limit": 10}

// File stat
{"action": "stat", "file": "/data/README.md"}
```
