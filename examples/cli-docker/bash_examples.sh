#!/bin/bash
#===============================================================================
# fraq — Kompletne przykłady użycia via CLI i curl
#===============================================================================
# Ten skrypt pokazuje wszystkie możliwości fraq przez:
# 1. CLI (fraq command)
# 2. REST API (curl)
# 3. WebSocket (wscat lub websocat)
#===============================================================================

set -e

# Kolory dla czytelności
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Konfiguracja
API_URL="${FRAQ_API_URL:-http://localhost:8000}"
TEST_DIR="${FRAQ_TEST_DIR:-.}"

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║              fraq — Przykłady użycia bash/curl                   ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

#===============================================================================
# SEKCJA 1: CLI — Command Line Interface
#===============================================================================

echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN} 1. CLI — Fractal Commands${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${YELLOW}# 1.1 Podstawowe eksplorowanie fraktala${NC}"
echo "$ fraq explore --depth 3 --dims 3 --format json"
fraq explore --depth 3 --dims 3 --format json 2>/dev/null | head -20 || echo "(fraq not installed, skip)"

echo -e "\n${YELLOW}# 1.2 Streaming rekordów${NC}"
echo "$ fraq stream --count 5 --dims 2 --format csv"
fraq stream --count 5 --dims 2 --format csv 2>/dev/null || echo "(skip)"

echo -e "\n${YELLOW}# 1.3 Generowanie schematu z typami${NC}"
echo "$ fraq schema --fields 'name:str,value:float,active:bool' --depth 2"
fraq schema --fields 'name:str,value:float,active:bool' --depth 2 --format json 2>/dev/null | head -30 || echo "(skip)"

echo -e "\n${YELLOW}# 1.4 Natural language query (z LLM)${NC}"
echo "$ fraq nl 'show 10 temperature readings'"
echo "# lub po polsku:"
echo "$ fraq nl 'pokaż 10 odczytów temperatury'"

#===============================================================================
# SEKCJA 2: CLI — File Commands
#===============================================================================

echo -e "\n${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN} 2. CLI — File Commands${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${YELLOW}# 2.1 Wyszukiwanie plików PDF${NC}"
echo "$ fraq files search --ext pdf --limit 10 --sort mtime ~/Documents"
fraq files search --ext pdf --limit 5 --sort mtime "$TEST_DIR" 2>/dev/null || echo "(skip)"

echo -e "\n${YELLOW}# 2.2 Wyszukiwanie z patternem${NC}"
echo "$ fraq files search --pattern '*.py' --limit 10 --format table ."
fraq files search --pattern '*.py' --limit 5 --format table "$TEST_DIR" 2>/dev/null || echo "(skip)"

echo -e "\n${YELLOW}# 2.3 Listowanie plików (ls-style)${NC}"
echo "$ fraq files list --long --limit 10 ."
fraq files list --long --limit 5 "$TEST_DIR" 2>/dev/null || echo "(skip)"

echo -e "\n${YELLOW}# 2.4 Statystyki pliku${NC}"
echo "$ fraq files stat README.md"
fraq files stat README.md 2>/dev/null || echo "(skip)"

echo -e "\n${YELLOW}# 2.5 Recursive search${NC}"
echo "$ fraq files search --ext md --recursive --limit 10 ."
fraq files search --ext md --limit 5 "$TEST_DIR" 2>/dev/null || echo "(skip)"

#===============================================================================
# SEKCJA 3: REST API via curl
#===============================================================================

echo -e "\n${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN} 3. REST API — curl${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"

# Sprawdź czy API działa
echo -e "\n${YELLOW}# 3.0 Health check${NC}"
echo "$ curl -s $API_URL/health | jq ."
curl -s "$API_URL/health" 2>/dev/null | jq . 2>/dev/null || echo '{"status": "API not running"}'

echo -e "\n${YELLOW}# 3.1 Fractal explore${NC}"
echo "$ curl -s '$API_URL/explore?depth=3&dims=3&format=json' | jq ."
curl -s "$API_URL/explore?depth=2&dims=2&format=json" 2>/dev/null | jq . 2>/dev/null | head -20 || echo "(API not available)"

echo -e "\n${YELLOW}# 3.2 Stream records${NC}"
echo "$ curl -s '$API_URL/stream?count=5&format=json' | jq ."
curl -s "$API_URL/stream?count=3&format=json" 2>/dev/null | jq . 2>/dev/null | head -20 || echo "(skip)"

echo -e "\n${YELLOW}# 3.3 Query with fields${NC}"
echo "$ curl -s '$API_URL/query?fields=temperature:float,humidity:float&depth=3&limit=5' | jq ."
curl -s "$API_URL/query?fields=temperature:float&depth=2&limit=3" 2>/dev/null | jq . 2>/dev/null | head -20 || echo "(skip)"

echo -e "\n${YELLOW}# 3.4 Schema generation${NC}"
echo "$ curl -s '$API_URL/schema?fields=invoice_id:str,amount:float&depth=2' | jq ."
curl -s "$API_URL/schema?fields=name:str,value:float&depth=1" 2>/dev/null | jq . 2>/dev/null | head -20 || echo "(skip)"

#===============================================================================
# SEKCJA 4: REST API — File Endpoints
#===============================================================================

echo -e "\n${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN} 4. REST API — File Operations${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${YELLOW}# 4.1 Search files${NC}"
echo "$ curl -s '$API_URL/files/search?path=.&ext=py&limit=5' | jq ."
curl -s "$API_URL/files/search?path=.&limit=3" 2>/dev/null | jq . 2>/dev/null | head -30 || echo "(skip)"

echo -e "\n${YELLOW}# 4.2 Search PDF files${NC}"
echo "$ curl -s '$API_URL/files/search?ext=pdf&limit=10&sort=mtime' | jq '.files[]'"
curl -s "$API_URL/files/search?ext=md&limit=3" 2>/dev/null | jq . 2>/dev/null | head -20 || echo "(skip)"

echo -e "\n${YELLOW}# 4.3 List files${NC}"
echo "$ curl -s '$API_URL/files/list?path=.&limit=10' | jq ."
curl -s "$API_URL/files/list?path=.&limit=5" 2>/dev/null | jq . 2>/dev/null | head -20 || echo "(skip)"

echo -e "\n${YELLOW}# 4.4 File statistics${NC}"
echo "$ curl -s '$API_URL/files/stat/README.md' | jq ."
curl -s "$API_URL/files/stat/README.md" 2>/dev/null | jq . 2>/dev/null || echo "(skip)"

echo -e "\n${YELLOW}# 4.5 CSV format${NC}"
echo "$ curl -s '$API_URL/files/search?ext=py&format=csv'"
curl -s "$API_URL/files/search?limit=3&format=csv" 2>/dev/null | head -5 || echo "(skip)"

echo -e "\n${YELLOW}# 4.6 YAML format${NC}"
echo "$ curl -s '$API_URL/files/search?ext=md&format=yaml' | head -20"
curl -s "$API_URL/files/search?limit=3&format=yaml" 2>/dev/null | head -10 || echo "(skip)"

#===============================================================================
# SEKCJA 5: Natural Language via API
#===============================================================================

echo -e "\n${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN} 5. REST API — Natural Language${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${YELLOW}# 5.1 NL query (file search)${NC}"
echo "$ curl -s -X POST '$API_URL/nl?query=list+10+pdf+files' | jq ."
curl -s -X POST "$API_URL/nl?query=list+pdf+files" 2>/dev/null | jq . 2>/dev/null | head -30 || echo "(requires LLM)"

echo -e "\n${YELLOW}# 5.2 NL query po polsku${NC}"
echo "$ curl -s -X POST '$API_URL/nl?query=podaj+listę+plików+pdf' | jq ."
echo "# URL-encoded: podaj%20list%C4%99%20plik%C3%B3w%20pdf"

#===============================================================================
# SEKCJA 6: WebSocket
#===============================================================================

echo -e "\n${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN} 6. WebSocket${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${YELLOW}# 6.1 WebSocket file streaming (wscat)${NC}"
echo "$ wscat -c 'ws://localhost:8000/ws/files'"
echo '> {"action": "search", "path": ".", "ext": "py", "limit": 5}'
echo ""
echo "# Albo via websocat:"
echo "$ echo '{\"action\":\"search\",\"path\":\".\",\"limit\":5}' | websocat ws://localhost:8000/ws/files"

echo -e "\n${YELLOW}# 6.2 WebSocket fractal streaming${NC}"
echo "$ wscat -c 'ws://localhost:8000/ws/stream'"
echo '> {"action": "stream", "count": 10, "interval": 0.5}'

#===============================================================================
# SEKCJA 7: Praktyczne skrypty
#===============================================================================

echo -e "\n${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN} 7. Praktyczne skrypty bash${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${YELLOW}# 7.1 Znajdź 10 najnowszych plików PDF i wyświetl jako tabela${NC}"
cat << 'EOF'
#!/bin/bash
API="http://localhost:8000"
curl -s "$API/files/search?ext=pdf&limit=10&sort=mtime&format=json" | \
  jq -r '.[] | [.filename, .size, .mtime] | @tsv' | \
  while IFS=$'\t' read -r name size mtime; do
    echo "$(date -d @$mtime '+%Y-%m-%d %H:%M')  $(numfmt --to=iec $size)  $name"
  done
EOF

echo -e "\n${YELLOW}# 7.2 Monitoruj nowe pliki w czasie rzeczywistym (WebSocket)${NC}"
cat << 'EOF'
#!/bin/bash
# Monitorowanie nowych plików
websocat ws://localhost:8000/ws/files << 'WS'
{"action": "search", "path": "/var/log", "pattern": "*.log", "limit": 100}
WS
EOF

echo -e "\n${YELLOW}# 7.3 Backup metadanych plików${NC}"
cat << 'EOF'
#!/bin/bash
# Zapisz metadane wszystkich plików do fraq
SOURCE_DIR="$1"
BACKUP_FILE="file-metadata-$(date +%Y%m%d).json"

curl -s "http://localhost:8000/files/search?path=$SOURCE_DIR&limit=1000" | \
  jq '.details' > "$BACKUP_FILE"

echo "Backup saved: $BACKUP_FILE"
EOF

echo -e "\n${YELLOW}# 7.4 Wyszukiwanie z paginacją${NC}"
cat << 'EOF'
#!/bin/bash
# Pobierz wszystkie pliki strona po stronie
PAGE=0
LIMIT=50
while true; do
  RESULTS=$(curl -s "http://localhost:8000/files/search?limit=$LIMIT&offset=$((PAGE*LIMIT))")
  COUNT=$(echo "$RESULTS" | jq 'length')
  [ "$COUNT" -eq 0 ] && break
  echo "$RESULTS" | jq -r '.[].filename'
  PAGE=$((PAGE+1))
done
EOF

echo -e "\n${YELLOW}# 7.5 Porównaj dwa katalogi via fraq${NC}"
cat << 'EOF'
#!/bin/bash
# Porównaj strukturę dwóch katalogów
DIR1="$1"
DIR2="$2"

API="http://localhost:8000"
META1=$(curl -s "$API/files/search?path=$DIR1&limit=1000")
META2=$(curl -s "$API/files/search?path=$DIR2&limit=1000")

echo "Files only in $DIR1:"
comm -23 <(echo "$META1" | jq -r '.[].filename' | sort) \
          <(echo "$META2" | jq -r '.[].filename' | sort)
EOF

#===============================================================================
# SEKCJA 8: One-linery
#===============================================================================

echo -e "\n${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN} 8. One-linery (CLI + curl)${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${YELLOW}# 8.1 Szybkie wyszukiwanie${NC}"
echo "$ fraq files search --ext pdf --limit 5 -f table"

echo -e "\n${YELLOW}# 8.2 Największe pliki${NC}"
echo "$ fraq files search --limit 20 --sort size | jq -r '.[] | \"\\(.size)\\t\\(.filename)\"' | sort -rn | head"

echo -e "\n${YELLOW}# 8.3 Pliki zmodyfikowane dzisiaj${NC}"
echo "$ curl -s '$API_URL/files/search?newer_than=$(date +%s -d today)' | jq '.[].filename'"

echo -e "\n${YELLOW}# 8.4 Konwersja wyników do CSV${NC}"
echo "$ fraq files search --ext py --format csv > python-files.csv"

echo -e "\n${YELLOW}# 8.5 Pobierz i przetwórz przez jq${NC}"
echo "$ curl -s '$API_URL/files/search?ext=md' | jq -r '.[] | select(.size > 1000) | .filename'"

#===============================================================================
# Podsumowanie
#===============================================================================

echo -e "\n${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN} Podsumowanie${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"

cat << 'EOF'

📁 FILE SEARCH VIA CLI:
   fraq files search --ext pdf --limit 10 ~/Documents
   fraq files list --long .
   fraq files stat README.md
   fraq nl "pokaż 10 plików pdf"

🌐 FILE SEARCH VIA REST API:
   curl $API/files/search?ext=pdf&limit=10
   curl $API/files/list?path=.&limit=50
   curl $API/files/stat/README.md
   curl -X POST $API/nl?query=list+pdf+files

⚡ WEBSOCKET STREAMING:
   wscat -c ws://localhost:8000/ws/files
   > {"action": "search", "ext": "py", "limit": 100}

🔧 INSTALL:
   pip install fraq[ai]
   pip install fastapi uvicorn
   
   # Start API server:
   cd examples && uvicorn api_server:app --host 0.0.0.0 --port 8000

📚 DOCS:
   API docs: http://localhost:8000/docs
   fraq help: fraq --help
   files help: fraq files --help

EOF

echo -e "${BLUE}Gotowe!${NC}"
