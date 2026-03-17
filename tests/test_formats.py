"""Tests for fraq.formats — serialisation backends."""

import json
import pytest
from fraq.core import FraqNode
from fraq.formats import FormatRegistry


@pytest.fixture
def sample_data():
    return {"value": 0.42, "depth": 3, "items": [1, 2, 3]}


@pytest.fixture
def sample_records():
    return [
        {"name": "alpha", "score": 0.9},
        {"name": "beta", "score": 0.7},
    ]


class TestFormatRegistry:
    def test_available_formats(self):
        fmts = FormatRegistry.available()
        assert "json" in fmts
        assert "csv" in fmts
        assert "yaml" in fmts
        assert "binary" in fmts
        assert "jsonl" in fmts
        assert "msgpack_lite" in fmts

    def test_unknown_format_raises(self):
        with pytest.raises(KeyError):
            FormatRegistry.get("nonexistent_format_xyz")

    def test_custom_format_registration(self):
        @FormatRegistry.register("test_custom")
        def _custom(data, **kw):
            return f"CUSTOM:{data}"

        result = FormatRegistry.serialize("test_custom", "hello")
        assert result == "CUSTOM:hello"


class TestJsonFormat:
    def test_dict_roundtrip(self, sample_data):
        out = FormatRegistry.serialize("json", sample_data)
        parsed = json.loads(out)
        assert parsed["value"] == 0.42
        assert parsed["depth"] == 3

    def test_fraq_node_serialises(self):
        node = FraqNode(position=(1.0, 2.0))
        out = FormatRegistry.serialize("json", node)
        parsed = json.loads(out)
        assert "position" in parsed
        assert "value" in parsed


class TestJsonlFormat:
    def test_multiple_records(self, sample_records):
        out = FormatRegistry.serialize("jsonl", sample_records)
        lines = out.strip().split("\n")
        assert len(lines) == 2
        assert json.loads(lines[0])["name"] == "alpha"

    def test_single_dict_becomes_one_line(self, sample_data):
        out = FormatRegistry.serialize("jsonl", sample_data)
        lines = out.strip().split("\n")
        assert len(lines) == 1


class TestCsvFormat:
    def test_csv_header_and_rows(self, sample_records):
        out = FormatRegistry.serialize("csv", sample_records)
        lines = out.strip().splitlines()
        assert lines[0].strip() == "name,score"  # header
        assert len(lines) == 3  # header + 2 rows

    def test_empty_list(self):
        out = FormatRegistry.serialize("csv", [])
        assert out == ""


class TestYamlFormat:
    def test_dict_produces_yaml(self, sample_data):
        out = FormatRegistry.serialize("yaml", sample_data)
        assert "value: 0.42" in out
        assert "depth: 3" in out

    def test_list(self):
        out = FormatRegistry.serialize("yaml", [1, 2, 3])
        assert "- 1" in out


class TestBinaryFormat:
    def test_dict_produces_bytes(self, sample_data):
        out = FormatRegistry.serialize("binary", sample_data)
        assert isinstance(out, bytes)
        assert len(out) > 0

    def test_float_tagged(self):
        out = FormatRegistry.serialize("binary", 3.14)
        assert out[0:1] == b"\x01"  # float tag

    def test_string_tagged(self):
        out = FormatRegistry.serialize("binary", "hello")
        assert out[0:1] == b"\x03"  # string tag


class TestMsgpackLiteFormat:
    def test_dict_produces_bytes(self, sample_data):
        out = FormatRegistry.serialize("msgpack_lite", sample_data)
        assert isinstance(out, bytes)
        assert out[0:1] == b"\xdf"  # map header

    def test_list_produces_bytes(self):
        out = FormatRegistry.serialize("msgpack_lite", [1, 2, 3])
        assert isinstance(out, bytes)
        assert out[0:1] == b"\xdd"  # array header
