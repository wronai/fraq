"""Tests for fraq.text2fraq."""

from fraq.query import FraqQuery
from fraq.text2fraq import ParsedQuery, Text2Fraq, Text2FraqConfig, Text2FraqSimple, text2query


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
