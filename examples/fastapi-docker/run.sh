#!/bin/bash
#===============================================================================
# FastAPI Docker — Skrypt uruchamiający
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🌀 FastAPI + fraq Docker Example"
echo "=================================="

# Sprawdź czy Docker jest zainstalowany
if ! command -v docker &> /dev/null; then
    echo "❌ Docker nie jest zainstalowany"
    exit 1
fi

# Sprawdź czy docker-compose jest dostępny
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
        echo "🚀 Uruchamianie serwera..."
        $COMPOSE up --build -d
        echo ""
        echo "✅ Serwer działa na http://localhost:8000"
        echo ""
        echo "Dostępne endpointy:"
        echo "  curl http://localhost:8000/health"
        echo "  curl 'http://localhost:8000/files/search?ext=pdf&limit=5'"
        echo "  curl 'http://localhost:8000/explore?depth=3'"
        ;;
    down|stop)
        echo "🛑 Zatrzymywanie serwera..."
        $COMPOSE down
        echo "✅ Serwer zatrzymany"
        ;;
    logs)
        echo "📋 Logi serwera:"
        $COMPOSE logs -f
        ;;
    test)
        echo "🧪 Testowanie API..."
        sleep 2
        echo "Health:"
        curl -s http://localhost:8000/health | jq . 2>/dev/null || curl -s http://localhost:8000/health
        echo ""
        echo "Files search:"
        curl -s 'http://localhost:8000/files/search?ext=py&limit=3' | jq . 2>/dev/null | head -20 || curl -s 'http://localhost:8000/files/search?ext=py&limit=3'
        ;;
    bash|shell)
        echo "🐚 Otwieranie shell w kontenerze..."
        $COMPOSE exec fraq-api bash
        ;;
    build)
        echo "🔨 Budowanie obrazu..."
        $COMPOSE build --no-cache
        ;;
    *)
        echo "Użycie: $0 {up|down|logs|test|bash|build}"
        echo ""
        echo "Komendy:"
        echo "  up     - Uruchom serwer (domyślnie)"
        echo "  down   - Zatrzymaj serwer"
        echo "  logs   - Pokaż logi"
        echo "  test   - Przetestuj API"
        echo "  bash   - Shell w kontenerze"
        echo "  build  - Przebuduj obraz"
        exit 1
        ;;
esac
