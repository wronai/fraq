#!/bin/bash
#===============================================================================
# fraq - Przykłady użycia w shellu
#===============================================================================
# Uruchom: chmod +x bash_examples.sh && ./bash_examples.sh
#===============================================================================

set -e

echo "=========================================="
echo "fraq - Shell Examples"
echo "=========================================="
echo ""

#-------------------------------------------------------------------------------
# 1. CLI - Podstawowe komendy
#-------------------------------------------------------------------------------

echo "=== 1. CLI - Podstawowe komendy ==="
echo ""

# Explore - eksploracja fraktala
echo "# Eksploracja fraktala (depth=3)"
echo "fraq explore --depth 3 --format json"
fraq explore --depth 3 --format json 2>/dev/null | head -20 || echo "  (wymaga instalacji fraq)"
echo ""

# Stream - strumieniowanie danych
echo "# Strumieniowanie 5 rekordów"
echo "fraq stream --count 5 --format csv"
fraq stream --count 5 --format csv 2>/dev/null || echo "  (wymaga instalacji fraq)"
echo ""

# Schema - generowanie schematu
echo "# Generowanie schematu z polami"
echo "fraq schema --fields 'name:str,value:float,active:bool' --depth 2"
fraq schema --fields 'name:str,value:float,active:bool' --depth 2 2>/dev/null | head -10 || echo "  (wymaga instalacji fraq)"
echo ""

#-------------------------------------------------------------------------------
# 2. CLI - Wyszukiwanie plików
#-------------------------------------------------------------------------------

echo "=== 2. CLI - Wyszukiwanie plików ==="
echo ""

# Wyszukiwanie plików PDF
echo "# Wyszukaj 10 PDFów w katalogu domowym"
echo "fraq files search --ext pdf --limit 10 ~"
fraq files search --ext pdf --limit 10 ~ 2>/dev/null | head -5 || echo "  (wymaga instalacji fraq)"
echo ""

# Wyszukiwanie Python files
echo "# Wyszukaj pliki Python"
echo "fraq files search --ext py --limit 5 ."
fraq files search --ext py --limit 5 . 2>/dev/null | head -5 || echo "  (wymaga instalacji fraq)"
echo ""

# Statystyki pliku
echo "# Statystyki pliku"
echo "fraq files stat README.md"
fraq files stat README.md 2>/dev/null || echo "  (wymaga instalacji fraq)"
echo ""

#-------------------------------------------------------------------------------
# 3. CLI - Natural Language
#-------------------------------------------------------------------------------

echo "=== 3. CLI - Natural Language ==="
echo ""

# NL - wyszukiwanie w języku naturalnym
echo "# Pokaż 5 najnowszych plików PDF"
echo "fraq nl 'pokaż 5 najnowszych plików pdf'"
fraq nl 'pokaż 5 najnowszych plików pdf' 2>/dev/null | head -5 || echo "  (wymaga instalacji fraq z [ai])"
echo ""

echo "# Pokaż pliki Python w folderze domowym"
echo "fraq nl 'pokaż pliki python w folderze domowym'"
fraq nl 'pokaż pliki python w folderze domowym' 2>/dev/null | head -5 || echo "  (wymaga instalacji fraq z [ai])"
echo ""

#-------------------------------------------------------------------------------
# 4. Python - One-linery
#-------------------------------------------------------------------------------

echo "=== 4. Python - One-linery ==="
echo ""

echo "# Generowanie danych JSON"
echo 'python3 -c "from fraq import query; import json; print(json.dumps(query(count=3, fmt=\"json\"), indent=2))"'
echo ""

echo "# Stream wartości"
echo 'python3 -c "from fraq import FraqNode; n = FraqNode((0.0, 0.0)); [print(f\"{i}: {n.zoom(steps=i).value:.4f}\") for i in range(5)]"'
echo ""

echo "# Wyszukiwanie plików"
echo 'python3 -c "from fraq.text2fraq import FileSearchText2Fraq; s = FileSearchText2Fraq(\".\"); print(s.format_results(s.search(\"5 python files\")))"'
echo ""

#-------------------------------------------------------------------------------
# 5. Docker
#-------------------------------------------------------------------------------

echo "=== 5. Docker ==="
echo ""

echo "# Uruchom API w Docker"
echo "cd examples/fastapi-docker && ./run.sh up"
echo ""

echo "# Test API"
echo "curl 'http://localhost:8000/files/search?ext=pdf&limit=5'"
echo ""

echo "# CLI w Docker"
echo "cd examples/cli-docker && ./run.sh fraq explore --depth 3"
echo ""

#-------------------------------------------------------------------------------
# 6. API (curl)
#-------------------------------------------------------------------------------

echo "=== 6. API (curl) ==="
echo ""

echo "# Health check"
echo "curl -s http://localhost:8000/ | python3 -m json.tool"
echo ""

echo "# Explore endpoint"
echo "curl -s 'http://localhost:8000/explore?depth=3&format=json' | head -20"
echo ""

echo "# File search endpoint"
echo "curl -s 'http://localhost:8000/files/search?ext=py&limit=5' | head -10"
echo ""

#-------------------------------------------------------------------------------
# 7. Przykłady z katalogu examples/
#-------------------------------------------------------------------------------

echo "=== 7. Przykłady z katalogu examples/ ==="
echo ""

echo "# Basic examples"
echo "PYTHONPATH=/home/tom/github/wronai/fraq python3 examples/basic/query_examples.py"
echo "PYTHONPATH=/home/tom/github/wronai/fraq python3 examples/basic/applications.py"
echo ""

echo "# Database"
echo "PYTHONPATH=/home/tom/github/wronai/fraq python3 examples/database/sqlite_examples.py"
echo ""

echo "# AI/ML"
echo "PYTHONPATH=/home/tom/github/wronai/fraq python3 examples/ai_ml/training_data.py"
echo ""

echo "# IoT"
echo "PYTHONPATH=/home/tom/github/wronai/fraq python3 examples/iot/sensor_examples.py"
echo ""

echo "# Streaming"
echo "PYTHONPATH=/home/tom/github/wronai/fraq python3 examples/streaming/sse_examples.py"
echo ""

echo "# ETL"
echo "PYTHONPATH=/home/tom/github/wronai/fraq python3 examples/etl/pipeline_examples.py"
echo ""

echo "# Testing"
echo "PYTHONPATH=/home/tom/github/wronai/fraq python3 examples/testing/test_fixtures.py"
echo ""

#-------------------------------------------------------------------------------
# 8. Skróty (shortcuts)
#-------------------------------------------------------------------------------

echo "=== 8. Skróty (shortcuts) ==="
echo ""

echo "# text2fraq - szybkie zapytanie"
echo 'python3 -c "from fraq.text2fraq import text2query; print(text2query(\"show 10 sensor readings\"))"'
echo ""

echo "# text2filesearch - szybkie wyszukiwanie"
echo 'python3 -c "from fraq.text2fraq import text2filesearch; print(text2filesearch(\"find pdf files\"))"'
echo ""

echo "=========================================="
echo "Done! Więcej w examples/README.md"
echo "=========================================="
