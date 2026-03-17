#!/bin/bash
#===============================================================================
# fraq - Uproszczone przykłady NLP/text2fraq w bash
#===============================================================================
# Uruchom: chmod +x nlp_examples.sh && ./nlp_examples.sh
#===============================================================================

set -e

echo "=========================================="
echo "fraq - NLP / Natural Language Examples"
echo "=========================================="
echo ""

#-------------------------------------------------------------------------------
# 1. Basic - Zapytania fraktalne (bez schema, bez root)
#-------------------------------------------------------------------------------

echo "=== 1. Basic Queries (fraq nl) ==="
echo ""

# Generowanie danych przez NL
echo "# Generuj 10 rekordów sensorów"
echo "fraq nl 'generuj 10 rekordów sensorów z temperaturą i wilgotnością'"
fraq nl 'generuj 10 rekordów sensorów z temperaturą i wilgotnością' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

# Eksploracja fraktala
echo "# Eksploruj fraktal głębokość 3"
echo "fraq nl 'pokaż fraktal głębokość 3 w formacie json'"
fraq nl 'pokaż fraktal głębokość 3 w formacie json' 2>/dev/null | head -10 || echo "  (wymaga: pip install fraq[ai])"
echo ""

# Strumień danych
echo "# Strumień 20 wartości"
echo "fraq nl 'strumień 20 wartości csv'"
fraq nl 'strumień 20 wartości csv' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

#-------------------------------------------------------------------------------
# 2. Database - Zapytania SQL/DB przez NL
#-------------------------------------------------------------------------------

echo "=== 2. Database (NL → SQL) ==="
echo ""

echo "# Generuj dane do SQLite"
echo "fraq nl 'generuj 50 rekordów do sqlite tabela sensors'"
fraq nl 'generuj 50 rekordów do sqlite tabela sensors' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Eksportuj do PostgreSQL"
echo "fraq nl 'eksportuj dane do postgresql funkcja fraq_zoom'"
fraq nl 'eksportuj dane do postgresql funkcja fraq_zoom' 2>/dev/null || echo "  (wymaga: pip install fraq[ai])"
echo ""

#-------------------------------------------------------------------------------
# 3. AI/ML - Generowanie datasetów przez NL
#-------------------------------------------------------------------------------

echo "=== 3. AI/ML (NL → Datasets) ==="
echo ""

echo "# Dataset klasyfikacji binarnej"
echo "fraq nl 'generuj dataset klasyfikacji 100 próbek 3 cechy'"
fraq nl 'generuj dataset klasyfikacji 100 próbek 3 cechy' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Dataset regresji (ceny domów)"
echo "fraq nl 'generuj dataset regresji ceny domów 50 rekordów'"
fraq nl 'generuj dataset regresji ceny domów 50 rekordów' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Time-series forecasting"
echo "fraq nl 'generuj time-series 7 dni godzinowe wartości'"
fraq nl 'generuj time-series 7 dni godzinowe wartości' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

#-------------------------------------------------------------------------------
# 4. IoT - Sensory przez NL
#-------------------------------------------------------------------------------

echo "=== 4. IoT (NL → Sensor Data) ==="
echo ""

echo "# Generuj odczyty sensorów"
echo "fraq nl 'generuj odczyty 3 sensorów temperatura wilgotność ciśnienie'"
fraq nl 'generuj odczyty 3 sensorów temperatura wilgotność ciśnienie' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Payloady MQTT"
echo "fraq nl 'generuj 5 payloadów mqtt topics factory sensors'"
fraq nl 'generuj 5 payloadów mqtt topics factory sensors' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Health monitoring urządzeń"
echo "fraq nl 'monitoruj health 20 urządzeń iot battery signal'"
fraq nl 'monitoruj health 20 urządzeń iot battery signal' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

#-------------------------------------------------------------------------------
# 5. Streaming - Strumieniowanie przez NL
#-------------------------------------------------------------------------------

echo "=== 5. Streaming (NL → SSE/WebSocket) ==="
echo ""

echo "# Generuj SSE events"
echo "fraq nl 'generuj 10 sse events sensor readings json'"
fraq nl 'generuj 10 sse events sensor readings json' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Kafka streaming"
echo "fraq nl 'kafka producer topic user-events 100 messages'"
fraq nl 'kafka producer topic user-events 100 messages' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

#-------------------------------------------------------------------------------
# 6. ETL - Pipelines przez NL
#-------------------------------------------------------------------------------

echo "=== 6. ETL (NL → Data Pipelines) ==="
echo ""

echo "# Multi-source extraction"
echo "fraq nl 'etl extract json api csv database 50 records unified schema'"
fraq nl 'etl extract json api csv database 50 records unified schema' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Data transformation"
echo "fraq nl 'transform sensor raw temp humidity to processed'"
fraq nl 'transform sensor raw temp humidity to processed' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Data validation"
echo "fraq nl 'validate 100 transactions amount account_id quality check'"
fraq nl 'validate 100 transactions amount account_id quality check' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Pipeline orchestration"
echo "fraq nl 'pipeline etl extract transform load 5 stages customers'"
fraq nl 'pipeline etl extract transform load 5 stages customers' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

#-------------------------------------------------------------------------------
# 7. Testing - Mock data przez NL
#-------------------------------------------------------------------------------

echo "=== 7. Testing (NL → Fixtures) ==="
echo ""

echo "# Unit test fixtures"
echo "fraq nl 'generuj 5 test users dataclass user_id name email age active'"
fraq nl 'generuj 5 test users dataclass user_id name email age active' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Mock API responses"
echo "fraq nl 'mock api response products endpoint 3 items json'"
fraq nl 'mock api response products endpoint 3 items json' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Load testing data"
echo "fraq nl 'generuj 1000 load test payloads requests endpoints distribution'"
fraq nl 'generuj 1000 load test payloads requests endpoints distribution' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

#-------------------------------------------------------------------------------
# 8. File Search - Wyszukiwanie plików przez NL
#-------------------------------------------------------------------------------

echo "=== 8. File Search (NL → Files) ==="
echo ""

echo "# Pokaż 10 najnowszych plików PDF w domu"
echo "fraq nl 'pokaż 10 najnowszych plików pdf w folderze domowym'"
fraq nl 'pokaż 10 najnowszych plików pdf w folderze domowym' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Znajdź pliki Python"
echo "fraq nl 'znajdź 5 plików python w katalogu domowym'"
fraq nl 'znajdź 5 plików python w katalogu domowym' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# Pokaż dokumenty markdown z ostatniego tygodnia"
echo "fraq nl 'pokaż dokumenty markdown z ostatniego tygodnia'"
fraq nl 'pokaż dokumenty markdown z ostatniego tygodnia' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

#-------------------------------------------------------------------------------
# 9. Python One-linery z text2fraq
#-------------------------------------------------------------------------------

echo "=== 9. Python One-linery (text2fraq) ==="
echo ""

echo "# Bezpośrednie użycie text2fraq"
echo 'python3 -c "from fraq.text2fraq import text2fraq; print(text2fraq(\"show 5 sensor readings\"))"'
echo ""

echo "# text2filesearch"
echo 'python3 -c "from fraq.text2fraq import text2filesearch; print(text2filesearch(\"find 10 pdf files in home\", \"~\"))"'
echo ""

echo "# text2query"
echo 'python3 -c "from fraq.text2fraq import text2query; q = text2query(\"show temperature humidity\"); print(q.to_fraq_query())"'
echo ""

#-------------------------------------------------------------------------------
# 10. Kombinacje z innych przykładów
#-------------------------------------------------------------------------------

echo "=== 10. Kombinacje (NL → Różne formaty) ==="
echo ""

echo "# JSON output"
echo "fraq nl 'generuj 5 rekordów json format sensor data'"
fraq nl 'generuj 5 rekordów json format sensor data' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# CSV output"
echo "fraq nl 'generuj 10 rekordów csv format transactions'"
fraq nl 'generuj 10 rekordów csv format transactions' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "# YAML output"
echo "fraq nl 'generuj 3 rekordów yaml format config'"
fraq nl 'generuj 3 rekordów yaml format config' 2>/dev/null | head -5 || echo "  (wymaga: pip install fraq[ai])"
echo ""

echo "=========================================="
echo "Done! Wszystkie przykłady używają NLP."
echo "Instalacja: pip install fraq[ai]"
echo "=========================================="
