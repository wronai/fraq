#!/bin/bash
#===============================================================================
# CLI Docker — Skrypt uruchamiający
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🌀 CLI + fraq Docker Example"
echo "============================"

# Sprawdź czy Docker jest zainstalowany
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

# Domyślna komenda
CMD="${@:-fraq --help}"

echo "🐳 Uruchamianie: $CMD"
echo ""

# Uruchom z zamontowanym /home
$COMPOSE run --rm fraq-cli $CMD
