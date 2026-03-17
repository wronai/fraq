"""Tests for fraq.adapters — FileAdapter, SQLAdapter, SensorAdapter, HybridAdapter."""

import json
import pytest
from pathlib import Path
from fraq.core import FraqNode
from fraq.query import FraqQuery, SourceType
from fraq.adapters import (
    FileAdapter, HTTPAdapter, SQLAdapter, SensorAdapter, HybridAdapter, get_adapter,
)


class TestFileAdapter:
    def test_load_nonexistent_deterministic(self):
        adapter = FileAdapter()
        root = adapter.load_root("nonexistent_abc.json")
        assert isinstance(root, FraqNode)
        # Same filename → same seed
        root2 = adapter.load_root("nonexistent_abc.json")
        assert root.seed == root2.seed

    def test_save_and_load_roundtrip(self, tmp_path):
        adapter = FileAdapter()
        node = FraqNode(position=(1.0, 2.0, 3.0), seed=42)
        path = str(tmp_path / "test_node.json")
        adapter.save(node, path)

        loaded = adapter.load_root(path)
        assert loaded.position == (1.0, 2.0, 3.0)

    def test_save_binary(self, tmp_path):
        adapter = FileAdapter()
        node = FraqNode(position=(0.0,), seed=1)
        path = str(tmp_path / "test_node.bin")
        adapter.save(node, path, fmt="binary", max_depth=0)
        assert Path(path).exists()

    def test_execute_query(self, tmp_path):
        adapter = FileAdapter()
        node = FraqNode(position=(0.0, 0.0, 0.0))
        path = str(tmp_path / "root.json")
        adapter.save(node, path)

        q = FraqQuery(depth=1, branching=2, format="records")
        q.select("v:float")
        q.source_uri = path
        result = adapter.execute(q)
        assert isinstance(result, list)
        assert len(result) == 2


class TestHTTPAdapter:
    def test_load_empty_uri_fallback(self):
        adapter = HTTPAdapter()
        root = adapter.load_root("")
        assert root.position == (0.0, 0.0, 0.0)

    def test_load_bad_url_fallback(self):
        adapter = HTTPAdapter()
        root = adapter.load_root("https://this-does-not-exist-99999.example.com/root")
        assert isinstance(root, FraqNode)

    def test_save_bad_url(self):
        adapter = HTTPAdapter()
        node = FraqNode(position=(0.0,))
        result = adapter.save(node, "https://this-does-not-exist-99999.example.com/save")
        assert result == ""


class TestSQLAdapter:
    def test_load_from_rows(self):
        adapter = SQLAdapter(table="sensors")
        rows = [{"id": 1, "x": 1.0, "y": 2.0, "z": 3.0}]
        root = adapter.load_root("", rows=rows)
        # Default mapper takes first 3 numeric values: id=1, x=1.0, y=2.0
        assert root.position == (1.0, 1.0, 2.0)

    def test_load_no_rows_fallback(self):
        adapter = SQLAdapter(table="invoices")
        root = adapter.load_root("")
        assert isinstance(root, FraqNode)
        # Deterministic from table name
        root2 = adapter.load_root("")
        assert root.seed == root2.seed

    def test_save_returns_insert(self):
        adapter = SQLAdapter(table="fraq_data")
        node = FraqNode(position=(0.0, 0.0), seed=7)
        sql = adapter.save(node, "")
        assert sql.startswith("INSERT INTO fraq_data")

    def test_generate_sql_function(self):
        adapter = SQLAdapter(table="gradient_nodes")
        sql = adapter.generate_sql_function(dims=3)
        assert "CREATE OR REPLACE FUNCTION" in sql
        assert "gradient_nodes_zoom" in sql

    def test_custom_row_to_node(self):
        def custom(row):
            return FraqNode(position=(row["lat"], row["lon"]), seed=row["id"])
        adapter = SQLAdapter(row_to_node=custom)
        root = adapter.load_root("", rows=[{"id": 42, "lat": 54.35, "lon": 18.65}])
        assert root.position == (54.35, 18.65)
        assert root.seed == 42


class TestSensorAdapter:
    def test_load_root(self):
        adapter = SensorAdapter(base_temp=25.0)
        root = adapter.load_root()
        assert root.generator is not None

    def test_stream_count(self):
        adapter = SensorAdapter()
        readings = list(adapter.stream(depth=2, count=5))
        assert len(readings) == 5
        assert "temperature" in readings[0]
        assert "humidity" in readings[0]

    def test_stream_deterministic(self):
        a1 = SensorAdapter(base_temp=20.0)
        a2 = SensorAdapter(base_temp=20.0)
        r1 = list(a1.stream(count=3))
        r2 = list(a2.stream(count=3))
        assert r1 == r2

    def test_save(self, tmp_path):
        adapter = SensorAdapter()
        root = adapter.load_root()
        path = str(tmp_path / "sensor.json")
        adapter.save(root, path)
        assert Path(path).exists()


class TestHybridAdapter:
    def test_merge_two_file_sources(self, tmp_path):
        fa = FileAdapter()
        n1 = FraqNode(position=(1.0, 0.0, 0.0), seed=10)
        n2 = FraqNode(position=(0.0, 1.0, 0.0), seed=20)
        p1 = str(tmp_path / "a.json")
        p2 = str(tmp_path / "b.json")
        fa.save(n1, p1)
        fa.save(n2, p2)

        hybrid = HybridAdapter()
        hybrid.add(FileAdapter(), p1)
        hybrid.add(FileAdapter(), p2)
        merged = hybrid.load_root()

        assert merged.meta["merged_from"] == 2
        # Position is mean
        assert merged.position[0] == pytest.approx(0.5)
        assert merged.position[1] == pytest.approx(0.5)

    def test_empty_hybrid(self):
        hybrid = HybridAdapter()
        root = hybrid.load_root()
        assert root.position == (0.0, 0.0, 0.0)


class TestGetAdapter:
    def test_file(self):
        a = get_adapter(SourceType.FILE)
        assert isinstance(a, FileAdapter)

    def test_sensor(self):
        a = get_adapter(SourceType.SENSOR, base_temp=30.0)
        assert isinstance(a, SensorAdapter)

    def test_memory_fallback(self):
        a = get_adapter(SourceType.MEMORY)
        assert isinstance(a, FileAdapter)
