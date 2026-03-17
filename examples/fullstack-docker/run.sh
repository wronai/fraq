#!/bin/bash
#===============================================================================
# Fullstack Docker — Skrypt uruchamiający
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🌀 Fullstack fraq Docker Example"
echo "================================"
echo ""
echo "Stack: API (8000) + WebSocket (8001) + Frontend (8501)"
echo ""

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
        echo "🚀 Uruchamianie stacku..."
        $COMPOSE up --build -d
        echo ""
        echo "✅ Usługi działają:"
        echo "  📡 API:       http://localhost:8000"
        echo "  ⚡ WebSocket: ws://localhost:8001"
        echo "  🎨 Frontend:  http://localhost:8501"
        echo ""
        echo "Testuj:"
        echo "  curl http://localhost:8000/health"
        echo "  curl 'http://localhost:8000/files/search?ext=pdf&limit=5'"
        ;;
    down|stop)
        echo "🛑 Zatrzymywanie stacku..."
        $COMPOSE down
        echo "✅ Zatrzymano"
        ;;
    logs)
        $COMPOSE logs -f
        ;;
    ps|status)
        $COMPOSE ps
        ;;
    test)
        echo "🧪 Testowanie stacku..."
        sleep 3
        echo "API:"
        curl -s http://localhost:8000/health 2>/dev/null | jq . || curl -s http://localhost:8000/health
        echo ""
        echo "Frontend:"
        curl -s http://localhost:8501 2>/dev/null | head -1 || echo "Frontend not ready"
        ;;
    bash|shell)
        SERVICE="${2:-api}"
        $COMPOSE exec $SERVICE bash
        ;;
    build)
        $COMPOSE build --no-cache
        ;;
    *)
        echo "Użycie: $0 {up|down|logs|ps|test|bash|build}"
        echo ""
        echo "Komendy:"
        echo "  up     - Uruchom cały stack"
        echo "  down   - Zatrzymaj stack"
        echo "  logs   - Pokaż logi"
        echo "  ps     - Status usług"
        echo "  test   - Przetestuj endpointy"
        echo "  bash   - Shell w kontenerze (np. bash api)"
        echo "  build  - Przebuduj obrazy"
        exit 1
        ;;
esac
