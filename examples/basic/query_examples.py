#!/usr/bin/env python3
"""
fraq examples — Query różnych źródeł danych.

Pokazuje jak ten sam FraqQuery działa niezależnie od źródła:
dysk, HTTP, SQL, sensory, hybrid.
"""

from fraq import (
    FraqNode, FraqSchema, FraqQuery, FraqExecutor, SourceType,
    FileAdapter, HTTPAdapter, SQLAdapter, SensorAdapter, HybridAdapter,
    FormatRegistry, query,
)


# ═══════════════════════════════════════════════════════════════════════════
# 1. DANE NA DYSKU (JSON / Parquet / CSV)
# ═══════════════════════════════════════════════════════════════════════════

def example_disk_json():
    """Query na lokalnym pliku JSON."""
    adapter = FileAdapter()

    # Zapisz root na dysk
    root = FraqNode(position=(0.0, 0.0, 0.0), seed=42)
    adapter.save(root, "/tmp/fraq_root.json")

    # Wczytaj i query
    loaded = adapter.load_root("/tmp/fraq_root.json")
    q = (
        FraqQuery()
        .zoom(5, direction=(0.1, 0.2, 0.7))
        .select("temperature:float", "sensor_id:str", "active:bool")
        .where("temperature", "gt", 0.3)
        .output("json")
        .take(10)
    )
    result = FraqExecutor(loaded).execute(q)
    print("=== Disk JSON ===")
    print(result[:200], "...\n")


def example_disk_csv():
    """Eksport do CSV — dla ERP / accounting workflows."""
    q = (
        FraqQuery()
        .zoom(3)
        .select("invoice_id:str", "amount:float", "vat:float", "paid:bool")
        .output("csv")
        .take(20)
    )
    result = FraqExecutor(dims=4).execute(q)
    print("=== Disk CSV (invoices) ===")
    print(result[:300], "...\n")


def example_disk_yaml():
    """YAML output — dla Kubernetes configs / IoT dashboards."""
    result = query(
        depth=2,
        fields=["name:str", "cpu_usage:float", "memory_mb:int", "healthy:bool"],
        format="yaml",
        limit=5,
        dims=4,
    )
    print("=== Disk YAML (k8s pods) ===")
    print(result[:300], "...\n")


# ═══════════════════════════════════════════════════════════════════════════
# 2. DANE Z INTERNETU (REST API)
# ═══════════════════════════════════════════════════════════════════════════

def example_http_api():
    """Query zdalne API — z fallbackiem na deterministyczny root."""
    adapter = HTTPAdapter()
    # W produkcji: root = adapter.load_root("https://api.gradient.example/root")
    # Tu: fallback na deterministyczny root z URL
    root = adapter.load_root("https://api.gradient.example/root")

    q = (
        FraqQuery()
        .zoom(10, direction=(1.0, 0.0, 0.0))
        .select("price:float", "symbol:str", "volume:int")
        .output("jsonl")
        .take(5)
    )
    result = FraqExecutor(root).execute(q)
    print("=== HTTP API (market data) ===")
    print(result[:200], "...\n")


# ═══════════════════════════════════════════════════════════════════════════
# 3. BAZA DANYCH (PostgreSQL / SQLite)
# ═══════════════════════════════════════════════════════════════════════════

def example_sql_query():
    """Query z mapowaniem SQL rows → fractal nodes."""
    adapter = SQLAdapter(table="gradient_nodes")

    # Symuluj rows z bazy danych
    db_rows = [
        {"id": 1, "x": 0.0, "y": 0.0, "z": 0.0, "value": 1000.0},
        {"id": 2, "x": 1.0, "y": 0.5, "z": 0.3, "value": 2500.0},
    ]
    root = adapter.load_root("", rows=db_rows)

    q = (
        FraqQuery()
        .zoom(5, direction=(0.0, 1.0, 0.0))  # kierunek: finanse
        .select("invoice_total:float", "client_id:str", "status:bool")
        .output("json")
        .take(10)
    )
    result = FraqExecutor(root).execute(q)
    print("=== SQL (invoices from DB) ===")
    print(result[:200], "...\n")

    # Wygeneruj PostgreSQL function
    sql_func = adapter.generate_sql_function(dims=3)
    print("=== Generated SQL function ===")
    print(sql_func[:200], "...\n")


def example_sql_custom_mapping():
    """Custom row→node mapping dla geolokalizacji."""
    def geo_mapper(row):
        return FraqNode(
            position=(row["lat"], row["lon"], row.get("alt", 0.0)),
            seed=row["station_id"],
        )

    adapter = SQLAdapter(table="weather_stations", row_to_node=geo_mapper)
    root = adapter.load_root("", rows=[
        {"station_id": 101, "lat": 54.35, "lon": 18.65, "alt": 10.0},
    ])

    q = FraqQuery().zoom(3).select("temp:float", "wind:float", "rain:bool").output("json").take(5)
    result = FraqExecutor(root).execute(q)
    print("=== SQL Custom Mapping (weather) ===")
    print(result[:200], "...\n")


# ═══════════════════════════════════════════════════════════════════════════
# 4. SENSORY / IoT (RPi / ESP32)
# ═══════════════════════════════════════════════════════════════════════════

def example_sensor_stream():
    """Nieskończony sensor stream — deterministyczny, zero storage."""
    adapter = SensorAdapter(base_temp=23.5, base_humidity=60.0, sample_hz=10)

    print("=== Sensor Stream (10 readings) ===")
    for i, reading in enumerate(adapter.stream(depth=3, count=10)):
        print(f"  [{i}] temp={reading['temperature']:.1f}°C "
              f"humidity={reading['humidity']:.1f}% "
              f"pressure={reading['pressure']:.1f}hPa")
    print()


def example_sensor_to_formats():
    """Sensor data → różne formaty eksportu."""
    adapter = SensorAdapter(base_temp=22.0)
    readings = list(adapter.stream(count=5))

    for fmt in ("json", "csv", "yaml"):
        output = FormatRegistry.serialize(fmt, readings)
        print(f"=== Sensor → {fmt.upper()} ===")
        print(str(output)[:150], "...\n")


# ═══════════════════════════════════════════════════════════════════════════
# 5. HYBRID (Web + Lokalne + Sensory)
# ═══════════════════════════════════════════════════════════════════════════

def example_hybrid_merge():
    """Merge wielu źródeł w jeden fractal."""
    hybrid = HybridAdapter()
    hybrid.add(FileAdapter(), "local_backup.json")      # fallback to deterministic
    hybrid.add(HTTPAdapter(), "https://api.example.com") # fallback to deterministic
    hybrid.add(SensorAdapter(base_temp=25.0), "")

    merged = hybrid.load_root()
    print(f"=== Hybrid Merged Root ===")
    print(f"  position: {merged.position}")
    print(f"  seed: {merged.seed}")
    print(f"  merged_from: {merged.meta.get('merged_from', 0)} sources")

    q = (
        FraqQuery()
        .zoom(5)
        .select("value:float", "source_id:str")
        .output("json")
        .take(8)
    )
    result = FraqExecutor(merged).execute(q)
    print(result[:200], "...\n")


# ═══════════════════════════════════════════════════════════════════════════
# 6. ONE-LINER query() — najprostsze użycie
# ═══════════════════════════════════════════════════════════════════════════

def example_oneliners():
    """Szybkie query bez budowania obiektów."""
    # JSON
    print("=== One-liner JSON ===")
    print(query(depth=2, fields=["x:float", "y:float"], limit=4, dims=2)[:150])
    print()

    # CSV
    print("=== One-liner CSV ===")
    print(query(depth=1, fields=["name:str", "score:float"], format="csv", limit=5, dims=2)[:150])
    print()

    # Binary
    print("=== One-liner Binary ===")
    data = query(depth=1, fields=["val:float"], format="binary", limit=1, dims=2)
    print(f"  {len(data)} bytes: {data[:20]}...")
    print()


# ═══════════════════════════════════════════════════════════════════════════
# RUN ALL
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    example_disk_json()
    example_disk_csv()
    example_disk_yaml()
    example_http_api()
    example_sql_query()
    example_sql_custom_mapping()
    example_sensor_stream()
    example_sensor_to_formats()
    example_hybrid_merge()
    example_oneliners()
