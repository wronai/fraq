"""Tests for fraq.query — FraqQuery, FraqExecutor, FraqFilter."""

import json
import pytest
from fraq.core import FraqNode
from fraq.query import FraqQuery, FraqExecutor, FraqFilter, SourceType, query


class TestFraqFilter:
    def test_eq(self):
        f = FraqFilter("x", "eq", 5)
        assert f.matches({"x": 5})
        assert not f.matches({"x": 6})

    def test_gt(self):
        f = FraqFilter("x", "gt", 0.5)
        assert f.matches({"x": 0.9})
        assert not f.matches({"x": 0.3})

    def test_lt(self):
        f = FraqFilter("x", "lt", 10)
        assert f.matches({"x": 5})
        assert not f.matches({"x": 15})

    def test_contains(self):
        f = FraqFilter("name", "contains", "abc")
        assert f.matches({"name": "xabcx"})
        assert not f.matches({"name": "xyz"})

    def test_missing_field(self):
        f = FraqFilter("missing", "eq", 1)
        assert not f.matches({"other": 1})

    def test_ne(self):
        f = FraqFilter("x", "ne", 5)
        assert f.matches({"x": 6})
        assert not f.matches({"x": 5})

    def test_gte_lte(self):
        assert FraqFilter("x", "gte", 5).matches({"x": 5})
        assert FraqFilter("x", "gte", 5).matches({"x": 6})
        assert not FraqFilter("x", "gte", 5).matches({"x": 4})
        assert FraqFilter("x", "lte", 5).matches({"x": 5})


class TestFraqQuery:
    def test_fluent_builder(self):
        q = FraqQuery()
        result = q.zoom(5, (1.0, 0.0, 0.0)).select("a:float", "b:int").where("a", "gt", 0.5).output("csv").take(10)
        assert result is q
        assert q.depth == 5
        assert len(q.fields) == 2
        assert len(q.filters) == 1
        assert q.format == "csv"
        assert q.limit == 10

    def test_from_source(self):
        q = FraqQuery().from_source(SourceType.FILE, "/data/root.json", dims=3)
        assert q.source == SourceType.FILE
        assert q.source_uri == "/data/root.json"
        assert q.meta["dims"] == 3


class TestFraqExecutor:
    def test_basic_execute_json(self):
        root = FraqNode(position=(0.0, 0.0, 0.0))
        q = FraqQuery(depth=1, branching=3)
        q.select("val:float")
        result = FraqExecutor(root).execute(q)
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) == 3
        assert "val" in data[0]

    def test_execute_with_limit(self):
        root = FraqNode(position=(0.0, 0.0))
        q = FraqQuery(depth=2, branching=4, limit=5)
        q.select("x:float")
        result = FraqExecutor(root).execute(q)
        data = json.loads(result)
        assert len(data) == 5

    def test_execute_with_filter(self):
        root = FraqNode(position=(0.0, 0.0, 0.0))
        q = FraqQuery(depth=1, branching=10, limit=100)
        q.select("value:float")
        q.where("value", "gt", 0.5)
        records = list(FraqExecutor(root).execute_iter(q))
        assert all(r["value"] > 0.5 for r in records)

    def test_execute_no_fields_adds_default(self):
        root = FraqNode(position=(0.0, 0.0))
        q = FraqQuery(depth=1, branching=2)
        result = FraqExecutor(root).execute(q)
        data = json.loads(result)
        assert "value" in data[0]

    def test_execute_records_format(self):
        root = FraqNode(position=(0.0, 0.0))
        q = FraqQuery(depth=1, branching=2, format="records")
        q.select("v:float")
        result = FraqExecutor(root).execute(q)
        assert isinstance(result, list)
        assert isinstance(result[0], dict)

    def test_execute_csv_format(self):
        root = FraqNode(position=(0.0, 0.0))
        q = FraqQuery(depth=1, branching=2, format="csv")
        q.select("a:float", "b:int")
        result = FraqExecutor(root).execute(q)
        assert "a,b" in result


class TestQueryFunction:
    def test_basic_query(self):
        result = query(depth=1, fields=["x:float"], format="records", dims=2, limit=4)
        assert isinstance(result, list)
        assert len(result) == 4
        assert "x" in result[0]

    def test_query_csv(self):
        result = query(depth=1, fields=["a:float", "b:int"], format="csv", dims=2, limit=3)
        assert "a,b" in result
