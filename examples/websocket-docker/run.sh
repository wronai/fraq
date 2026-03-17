#!/bin/bash
#===============================================================================
# WebSocket Docker — Skrypt uruchamiający
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🌀 WebSocket + fraq Docker Example"
echo "==================================="

if ! command -v docker &> /dev/null; then
    echo "❌ Docker nie jest zainstalowany"
    exit 1
fi

if command -v docker-compose &> /dev/null; then
    COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE="docker compose"
else
    echo "❌ docker-compose nie jest zainstalowany"
    exit 1
fi

case "${1:-up}" in
    up|start)
        echo "🚀 Uruchamianie WebSocket server..."
        $COMPOSE up --build -d
        echo ""
        echo "✅ WebSocket działa na ws://localhost:8001"
        echo ""
        echo "Testowanie:"
        echo "  websocat ws://localhost:8001/ws/stream"
        echo '  > {"action": "stream", "count": 10}'
        ;;
    down|stop)
        echo "🛑 Zatrzymywanie..."
        $COMPOSE down
        echo "✅ Zatrzymano"
        ;;
    logs)
        $COMPOSE logs -f
        ;;
    test)
        echo "🧪 Testowanie WebSocket..."
        if command -v websocat &> /dev/null; then
            echo '{"action": "stream", "count": 3}' | websocat ws://localhost:8001/ws/stream
        else
            echo "❌ Zainstaluj websocat: sudo apt install websocat"
        fi
        ;;
    bash)
        $COMPOSE exec fraq-websocket bash
        ;;
    *)
        echo "Użycie: $0 {up|down|logs|test|bash}"
        exit 1
        ;;
esac
