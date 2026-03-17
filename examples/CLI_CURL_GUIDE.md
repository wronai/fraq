# fraq CLI & REST API — Kompletna dokumentacja

Obsługa fraq w 100% przez **CLI shell** i **curl** — bez potrzeby pisania kodu Python.

## 📦 Instalacja

```bash
pip install fraq[ai]          # z LLM (text2fraq)
pip install fastapi uvicorn   # dla REST API
```

---

## 🖥️ CLI — Command Line Interface

### Podstawowe komendy fraktalne

```bash
# Eksploracja fraktala
fraq explore --depth 3 --dims 3 --format json
fraq explore --depth 5 --dims 2 --format yaml

# Streaming rekordów
fraq stream --count 10 --dims 3 --format csv
fraq stream --count 100 --format jsonl

# Generowanie schematu z typami
fraq schema --fields 'name:str,value:float,active:bool' --depth 2
fraq schema --fields 'invoice_id:str,amount:float,date:str' --depth 3 --format csv
```

### Wyszukiwanie plików (FileSearchAdapter)

```bash
# Wyszukaj 10 plików PDF, sortuj po dacie
fraq files search --ext pdf --limit 10 --sort mtime ~/Documents

# Wyszukaj pliki Python w formie tabeli
fraq files search --pattern '*.py' --limit 20 --format table .

# Listuj pliki (ls-style)
fraq files list --long --limit 50 .
fraq files list --ext md --recursive

# Statystyki pliku z koordynatami fraktalnymi
fraq files stat README.md
fraq files stat /path/to/file.pdf --format json
```

### Natural Language (wymaga LLM)

```bash
# Zapytania naturalne po angielsku
fraq nl "show 10 temperature readings"
fraq nl "find all pdf files from last week"

# Zapytania po polsku
fraq nl "pokaż 10 plików pdf"
fraq nl "znajdź najnowsze dokumenty"
fraq nl "podaj listę plików python"
```

---

## 🌐 REST API via curl

### Uruchomienie serwera

```bash
cd examples
uvicorn api_server:app --host 0.0.0.0 --port 8000

# Sprawdź czy działa
curl http://localhost:8000/health
```

### Endpointy fraktalne

```bash
# Health check
curl -s http://localhost:8000/health | jq .

# Eksploracja
curl -s 'http://localhost:8000/explore?depth=3&dims=3&format=json' | jq .
curl -s 'http://localhost:8000/explore?depth=2&dims=2&format=yaml'

# Streaming
curl -s 'http://localhost:8000/stream?count=5&format=json' | jq .
curl -s 'http://localhost:8000/stream?count=100&format=csv'

# Query z polami
curl -s 'http://localhost:8000/query?fields=temperature:float,humidity:float&depth=3&limit=10' | jq .

# Schema
curl -s 'http://localhost:8000/schema?fields=id:str,value:float&depth=2' | jq .
```

### Endpointy plików

```bash
# Wyszukaj pliki
curl -s 'http://localhost:8000/files/search?path=.&ext=py&limit=10' | jq .
curl -s 'http://localhost:8000/files/search?ext=pdf&limit=5&sort=mtime' | jq -r '.[].filename'

# Listuj pliki
curl -s 'http://localhost:8000/files/list?path=.&limit=20' | jq .

# Statystyki pliku
curl -s 'http://localhost:8000/files/stat/README.md' | jq .
curl -s 'http://localhost:8000/files/stat/fraq/cli.py' | jq '.fraq'

# Różne formaty
curl -s 'http://localhost:8000/files/search?ext=py&format=csv'
curl -s 'http://localhost:8000/files/search?ext=md&format=yaml'
```

### Natural Language via API

```bash
# Zapytanie NL (file search)
curl -s -X POST 'http://localhost:8000/nl?query=list+10+pdf+files' | jq .

# Po polsku (URL-encoded)
curl -s -X POST 'http://localhost:8000/nl?query=podaj%20list%C4%99%20plik%C3%B3w%20pdf' | jq .
curl -s -X POST 'http://localhost:8000/nl?query=znajdź+najnowsze+dokumenty' | jq .
```

---

## ⚡ WebSocket

### Wyszukiwanie plików w czasie rzeczywistym

```bash
# Połącz się przez wscat
wscat -c 'ws://localhost:8000/ws/files'

# Wyślij zapytanie:
> {"action": "search", "path": ".", "ext": "py", "limit": 10}

# Streamuj wyniki jeden po drugim
> {"action": "search", "path": "/var/log", "pattern": "*.log", "limit": 100}

# Statystyki pojedynczego pliku
> {"action": "stat", "file": "README.md"}
```

### Streaming fraktalny

```bash
wscat -c 'ws://localhost:8000/ws/stream'

# Streamuj rekordy
> {"action": "stream", "count": 50, "interval": 0.1}

# Ping
> {"action": "ping"}
```

### websocat (alternatywa)

```bash
# Wyszukaj pliki
websocat ws://localhost:8000/ws/files << 'EOF'
{"action": "search", "ext": "py", "limit": 5}
EOF

# Streamuj fraktal
websocat ws://localhost:8000/ws/stream << 'EOF'
{"action": "stream", "count": 10, "interval": 0.5}
EOF
```

---

## 🔧 Praktyczne skrypty bash

### Znajdź 10 najnowszych plików PDF

```bash
#!/bin/bash
API="http://localhost:8000"

curl -s "$API/files/search?ext=pdf&limit=10&sort=mtime" | \
  jq -r '.[] | [.filename, .size, .mtime] | @tsv' | \
  while IFS=$'\t' read -r name size mtime; do
    echo "$(date -d @$mtime '+%Y-%m-%d %H:%M')  $(numfmt --to=iec $size)  $name"
  done
```

### Backup metadanych plików

```bash
#!/bin/bash
SOURCE_DIR="${1:-.}"
BACKUP_FILE="fraq-backup-$(date +%Y%m%d-%H%M%S).json"
API="http://localhost:8000"

echo "Backing up metadata from $SOURCE_DIR..."

# Pobierz wszystkie pliki (limit 10000)
curl -s "$API/files/search?path=$SOURCE_DIR&limit=10000" | \
  jq '.details' > "$BACKUP_FILE"

echo "Backup saved: $BACKUP_FILE ($(wc -l < $BACKUP_FILE) records)"
```

### Porównaj dwa katalogi

```bash
#!/bin/bash
DIR1="$1"
DIR2="$2"
API="http://localhost:8000"

echo "Comparing $DIR1 vs $DIR2..."

META1=$(curl -s "$API/files/search?path=$DIR1&limit=1000" | jq -r '.[].filename' | sort)
META2=$(curl -s "$API/files/search?path=$DIR2&limit=1000" | jq -r '.[].filename' | sort)

echo "Files only in $DIR1:"
comm -23 <(echo "$META1") <(echo "$META2")

echo ""
echo "Files only in $DIR2:"
comm -13 <(echo "$META1") <(echo "$META2")
```

### Monitoruj nowe pliki (co 60 sekund)

```bash
#!/bin/bash
WATCH_DIR="${1:-.}"
API="http://localhost:8000"
LAST_CHECK=$(date +%s)

echo "Monitoring $WATCH_DIR for new files..."

while true; do
  sleep 60
  
  # Pobierz pliki nowsze niż ostatni check
  NEW_FILES=$(curl -s "$API/files/search?path=$WATCH_DIR&newer_than=$LAST_CHECK")
  COUNT=$(echo "$NEW_FILES" | jq 'length')
  
  if [ "$COUNT" -gt 0 ]; then
    echo "$(date '+%H:%M:%S') - $COUNT new files:"
    echo "$NEW_FILES" | jq -r '.[].filename'
  fi
  
  LAST_CHECK=$(date +%s)
done
```

### Konwertuj wyniki do różnych formatów

```bash
#!/bin/bash
# JSON → CSV via fraq API
API="http://localhost:8000"

echo "Getting CSV..."
curl -s "$API/files/search?path=.&ext=py&format=csv" > python-files.csv

echo "Getting YAML..."
curl -s "$API/files/search?path=.&ext=md&format=yaml" > markdown-files.yaml

echo "Getting TSV..."
curl -s "$API/files/search?path=.&limit=100&format=json" | \
  jq -r '.[] | [.filename, .size, .mtime] | @tsv' > files.tsv
```

---

## 📋 Szybka referencja

### CLI commands

| Komenda | Opis |
|---------|------|
| `fraq explore` | Eksploruj fraktal |
| `fraq stream` | Streamuj rekordy |
| `fraq schema` | Generuj schemat |
| `fraq nl` | Natural language query |
| `fraq files search` | Wyszukaj pliki |
| `fraq files list` | Listuj pliki |
| `fraq files stat` | Statystyki pliku |

### API endpoints

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/health` | GET | Status serwera |
| `/explore` | GET | Eksploracja fraktala |
| `/stream` | GET | Streaming rekordów |
| `/query` | GET | Query z polami |
| `/files/search` | GET | Wyszukaj pliki |
| `/files/list` | GET | Listuj pliki |
| `/files/stat/{path}` | GET | Statystyki pliku |
| `/nl` | POST | Natural language |
| `/ws/files` | WS | WebSocket files |
| `/ws/stream` | WS | WebSocket fractal |

### Parametry files/search

| Parametr | Typ | Opis |
|----------|-----|------|
| `path` | string | Katalog bazowy |
| `ext` | string | Rozszerzenie (pdf, py, md...) |
| `pattern` | string | Glob pattern (*.py) |
| `limit` | int | Max wyników (1-1000) |
| `sort` | string | `name`, `mtime`, `size` |
| `format` | string | `json`, `csv`, `yaml` |
| `recursive` | bool | Szukaj w podkatalogach |

---

## 🚀 Start w 5 minut

```bash
# 1. Instalacja
pip install fraq[ai] fastapi uvicorn

# 2. Start API server
cd examples
uvicorn api_server:app --port 8000 &

# 3. Test CLI
fraq files search --ext py --limit 5 .

# 4. Test API
curl 'http://localhost:8000/files/search?ext=py&limit=5' | jq .

# 5. Test WebSocket
wscat -c 'ws://localhost:8000/ws/files'
> {"action": "search", "ext": "py", "limit": 10}
```

---

## 📚 Więcej przykładów

Zobacz pełne przykłady w `examples/bash_examples.sh`:

```bash
chmod +x examples/bash_examples.sh
./examples/bash_examples.sh
```

---

**fraq v0.2.1** — Fractal Query Data Library
