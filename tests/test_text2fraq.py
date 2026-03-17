"""Tests for fraq.text2fraq."""

import importlib

from fraq.query import FraqQuery
from fraq.text2fraq import (
    FileSearchText2Fraq,
    ParsedQuery,
    Text2Fraq,
    Text2FraqConfig,
    Text2FraqSimple,
    text2filesearch,
    text2query,
)

# Import module with different name to avoid conflict with function
text2fraq_mod = importlib.import_module("fraq.text2fraq")


class StubClient:
    def __init__(self, response: str):
        self.response = response

    def complete(self, prompt: str) -> str:
        return self.response


class TestParsedQuery:
    def test_to_fraq_query_maps_filters_direction_and_limit(self):
        parsed = ParsedQuery(
            fields=["temperature:float", "sensor_id:str"],
            depth=4,
            format="csv",
            filters={"temperature": {"gt": 0.7}, "sensor_id": "sensor-1"},
            direction=(0.1, 0.2, 0.7),
            limit=5,
        )

        query = parsed.to_fraq_query()

        assert isinstance(query, FraqQuery)
        assert query.depth == 4
        assert query.direction == (0.1, 0.2, 0.7)
        assert query.format == "csv"
        assert query.limit == 5
        assert len(query.filters) == 2
        assert query.filters[0].field == "temperature"
        assert query.filters[0].op == "gt"
        assert query.filters[0].value == 0.7
        assert query.filters[1].field == "sensor_id"
        assert query.filters[1].op == "eq"
        assert query.filters[1].value == "sensor-1"


class TestText2Fraq:
    def test_parse_json_response(self):
        client = StubClient(
            '{"fields":["temperature:float"],"depth":2,"format":"json","filters":{"temperature":{"gt":0.5}},"dims":4,"direction":[1,0,0],"limit":10}'
        )
        parser = Text2Fraq(Text2FraqConfig(), client=client)

        parsed = parser.parse("Show temperature")

        assert parsed.fields == ["temperature:float"]
        assert parsed.depth == 2
        assert parsed.format == "json"
        assert parsed.filters == {"temperature": {"gt": 0.5}}
        assert parsed.dims == 4
        assert parsed.direction == (1.0, 0.0, 0.0)
        assert parsed.limit == 10

    def test_parse_falls_back_when_response_is_not_json(self):
        client = StubClient("temperature csv 12 records")
        parser = Text2Fraq(Text2FraqConfig(default_depth=3), client=client)

        parsed = parser.parse("Show temperature")

        assert "temperature:float" in parsed.fields
        assert parsed.format == "csv"
        assert parsed.limit == 12


class TestText2FraqSimple:
    def test_rule_based_parse_detects_fields_format_and_limit(self):
        parsed = Text2FraqSimple().parse("Show 20 temperature and humidity samples in CSV")

        assert "temperature:float" in parsed.fields
        assert "humidity:float" in parsed.fields
        assert parsed.format == "csv"
        assert parsed.limit == 20


class TestConvenienceFunctions:
    def test_text2query_uses_simple_parser_without_litellm(self):
        parsed = text2query("Show pressure as YAML")

        assert "pressure:float" in parsed.fields
        assert parsed.format == "yaml"


class StubFileAdapter:
    def __init__(self, results):
        self.results = results
        self.calls = []

    def search(self, **kwargs):
        self.calls.append(kwargs)
        return self.results


class TestFileSearchText2Fraq:
    def test_parse_detects_extension_limit_sort_and_recent_filter(self):
        searcher = FileSearchText2Fraq(".")

        parsed = searcher.parse("list 7 pdf files created recently")

        assert parsed["extension"] == "pdf"
        assert parsed["limit"] == 7
        assert parsed["sort_by"] == "mtime"
        assert parsed["newer_than"] is not None

    def test_search_uses_adapter_with_parsed_arguments(self):
        adapter = StubFileAdapter([{"filename": "report.pdf", "size": 10}])
        searcher = FileSearchText2Fraq(".")
        searcher.adapter = adapter

        results = searcher.search("list 3 pdf files")

        assert results == [{"filename": "report.pdf", "size": 10}]
        assert adapter.calls[0]["extension"] == "pdf"
        assert adapter.calls[0]["limit"] == 3

    def test_format_results_supports_field_projection(self):
        searcher = FileSearchText2Fraq(".")

        output = searcher.format_results(
            [{"filename": "report.pdf", "size": 10, "path": "/tmp/report.pdf"}],
            fmt="json",
            fields=["filename", "size"],
        )

        assert '"filename": "report.pdf"' in output
        assert '"size": 10' in output
        assert '"path"' not in output


class TestText2FileSearchFunction:
    def test_text2filesearch_records_uses_file_searcher(self, monkeypatch):
        adapter = StubFileAdapter([{"filename": "notes.md"}])
        searcher = FileSearchText2Fraq(".")
        searcher.adapter = adapter

        # Patch the class in text2fraq module
        monkeypatch.setattr(
            text2fraq_mod,
            "FileSearchText2Fraq",
            lambda base_path=".": searcher,
        )

        result = text2filesearch("list 1 markdown file", fmt="records")

        assert result == [{"filename": "notes.md"}]
