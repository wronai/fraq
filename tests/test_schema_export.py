"""Tests for fraq.schema_export — NLP2CMD, OpenAPI, GraphQL, AsyncAPI, Proto, JSON Schema."""

import json
import pytest
from fraq.core import FraqNode, FraqSchema
from fraq.schema_export import (
    to_nlp2cmd_schema,
    to_nlp2cmd_actions,
    to_openapi,
    to_graphql,
    to_asyncapi,
    to_proto,
    to_json_schema,
)


@pytest.fixture
def sample_schema():
    root = FraqNode(position=(0.0, 0.0, 0.0))
    schema = FraqSchema(root=root)
    schema.add_field("temperature", "float")
    schema.add_field("sensor_id", "str")
    schema.add_field("active", "bool")
    schema.add_field("reading_count", "int")
    return schema


class TestNLP2CMDSchema:
    def test_structure(self, sample_schema):
        result = to_nlp2cmd_schema(sample_schema, command_name="fraq_sensor")
        assert result["command"] == "fraq_sensor"
        assert result["version"] == "1.0"
        assert "parameters" in result
        assert "templates" in result
        assert "examples" in result

    def test_field_parameters(self, sample_schema):
        result = to_nlp2cmd_schema(sample_schema)
        param_names = [p["name"] for p in result["parameters"]]
        assert "temperature" in param_names
        assert "sensor_id" in param_names
        assert "depth" in param_names  # always included
        assert "format" in param_names

    def test_templates(self, sample_schema):
        result = to_nlp2cmd_schema(sample_schema)
        assert len(result["templates"]) >= 3
        assert any("--fields" in t for t in result["templates"])

    def test_examples(self, sample_schema):
        result = to_nlp2cmd_schema(sample_schema)
        assert len(result["examples"]) >= 2
        for ex in result["examples"]:
            assert "input" in ex
            assert "command" in ex

    def test_json_serializable(self, sample_schema):
        result = to_nlp2cmd_schema(sample_schema)
        serialized = json.dumps(result)
        assert len(serialized) > 0


class TestNLP2CMDActions:
    def test_four_actions(self, sample_schema):
        actions = to_nlp2cmd_actions(sample_schema)
        assert len(actions) == 4
        names = [a["name"] for a in actions]
        assert "fraq_zoom" in names
        assert "fraq_query" in names
        assert "fraq_stream" in names
        assert "fraq_save" in names

    def test_action_parameters(self, sample_schema):
        actions = to_nlp2cmd_actions(sample_schema)
        zoom = next(a for a in actions if a["name"] == "fraq_zoom")
        param_names = [p["name"] for p in zoom["parameters"]]
        assert "depth" in param_names
        assert "direction" in param_names

    def test_query_includes_schema_fields(self, sample_schema):
        actions = to_nlp2cmd_actions(sample_schema)
        query_action = next(a for a in actions if a["name"] == "fraq_query")
        param_names = [p["name"] for p in query_action["parameters"]]
        assert "temperature" in param_names
        assert "sensor_id" in param_names


class TestOpenAPI:
    def test_structure(self, sample_schema):
        spec = to_openapi(sample_schema)
        assert spec["openapi"] == "3.0.3"
        assert "paths" in spec
        assert "components" in spec

    def test_endpoints(self, sample_schema):
        spec = to_openapi(sample_schema)
        paths = spec["paths"]
        assert "/api/fraq/zoom" in paths
        assert "/api/fraq/query" in paths
        assert "/api/fraq/stream" in paths

    def test_record_schema(self, sample_schema):
        spec = to_openapi(sample_schema)
        record = spec["components"]["schemas"]["FraqRecord"]
        assert "temperature" in record["properties"]
        assert record["properties"]["temperature"]["type"] == "number"

    def test_custom_base_path(self, sample_schema):
        spec = to_openapi(sample_schema, base_path="/v2/data")
        assert "/v2/data/zoom" in spec["paths"]


class TestGraphQL:
    def test_type_definition(self, sample_schema):
        gql = to_graphql(sample_schema)
        assert "type FraqRecord {" in gql
        assert "temperature: Float!" in gql
        assert "sensor_id: String!" in gql
        assert "active: Boolean!" in gql
        assert "reading_count: Int!" in gql

    def test_query_type(self, sample_schema):
        gql = to_graphql(sample_schema)
        assert "type Query {" in gql
        assert "zoom(" in gql
        assert "query(" in gql
        assert "stream(" in gql

    def test_custom_type_name(self, sample_schema):
        gql = to_graphql(sample_schema, type_name="SensorReading")
        assert "type SensorReading {" in gql


class TestAsyncAPI:
    def test_structure(self, sample_schema):
        spec = to_asyncapi(sample_schema)
        assert spec["asyncapi"] == "3.0.0"
        assert "channels" in spec
        assert "components" in spec

    def test_channels(self, sample_schema):
        spec = to_asyncapi(sample_schema)
        assert "fraq/stream" in spec["channels"]
        assert "fraq/zoomed" in spec["channels"]

    def test_record_schema(self, sample_schema):
        spec = to_asyncapi(sample_schema)
        record = spec["components"]["schemas"]["FraqRecord"]
        assert "temperature" in record["properties"]


class TestProto:
    def test_message_fields(self, sample_schema):
        proto = to_proto(sample_schema)
        assert 'syntax = "proto3";' in proto
        assert "double temperature = 1;" in proto
        assert "string sensor_id = 2;" in proto
        assert "bool active = 3;" in proto
        assert "int64 reading_count = 4;" in proto

    def test_service(self, sample_schema):
        proto = to_proto(sample_schema)
        assert "service FraqService {" in proto
        assert "rpc Zoom" in proto
        assert "rpc Stream" in proto

    def test_zoom_request(self, sample_schema):
        proto = to_proto(sample_schema)
        assert "message ZoomRequest {" in proto
        assert "int32 depth = 1;" in proto

    def test_custom_package(self, sample_schema):
        proto = to_proto(sample_schema, package="my.sensors")
        assert "package my.sensors;" in proto


class TestJSONSchema:
    def test_structure(self, sample_schema):
        js = to_json_schema(sample_schema)
        assert js["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert js["type"] == "object"
        assert "properties" in js
        assert "required" in js

    def test_fields(self, sample_schema):
        js = to_json_schema(sample_schema)
        assert "temperature" in js["properties"]
        assert js["properties"]["temperature"]["type"] == "number"
        assert "temperature" in js["required"]

    def test_json_serializable(self, sample_schema):
        js = to_json_schema(sample_schema)
        assert len(json.dumps(js)) > 0
