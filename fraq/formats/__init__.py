"""
Format serialization package - refactored to eliminate cycles.

Structure:
- registry.py: FormatRegistry (clean, no serialization logic)
- prepare.py: Data preparation utilities (_prepare, _encode_value)
- text.py: Text serializers (JSON, CSV, YAML, JSONL)
- binary.py: Binary serializers (binary, msgpack_lite)

All serializers import from prepare.py (one-way dependency).
"""

from __future__ import annotations

# Registry
from fraq.formats.registry import FormatRegistry

# Preparation utilities
from fraq.formats.prepare import prepare, encode_value

# Text serializers
from fraq.formats.text import to_json, to_jsonl, to_csv, to_yaml, simple_yaml

# Binary serializers
from fraq.formats.binary import to_binary, to_msgpack_lite, mp_encode

# Register all built-in formats
FormatRegistry.register("json", to_json)
FormatRegistry.register("jsonl", to_jsonl)
FormatRegistry.register("csv", to_csv)
FormatRegistry.register("yaml", to_yaml)
FormatRegistry.register("binary", to_binary)
FormatRegistry.register("msgpack_lite", to_msgpack_lite)

# Backward compatibility aliases
_prepare = prepare
_encode_value = encode_value
_simple_yaml = simple_yaml
_mp_encode = mp_encode
_to_json = to_json
_to_jsonl = to_jsonl
_to_csv = to_csv
_to_yaml = to_yaml
_to_binary = to_binary
_to_msgpack_lite = to_msgpack_lite

__all__ = [
    # Registry
    "FormatRegistry",
    # Preparation
    "prepare",
    "encode_value",
    # Text
    "to_json",
    "to_jsonl", 
    "to_csv",
    "to_yaml",
    "simple_yaml",
    # Binary
    "to_binary",
    "to_msgpack_lite",
    "mp_encode",
    # Backward compatibility
    "_prepare",
    "_encode_value",
    "_simple_yaml",
    "_mp_encode",
    "_to_json",
    "_to_jsonl",
    "_to_csv",
    "_to_yaml",
    "_to_binary",
    "_to_msgpack_lite",
]
