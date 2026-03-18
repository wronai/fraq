"""
Common type mappings for schema export.
"""

from __future__ import annotations

from typing import Any, Dict


# JSON Schema type mappings
FRAQ_TO_JSON_SCHEMA: Dict[str, Dict[str, Any]] = {
    "float": {"type": "number", "format": "double"},
    "int": {"type": "integer", "format": "int64"},
    "str": {"type": "string"},
    "bool": {"type": "boolean"},
    "bytes": {"type": "string", "format": "byte"},
    "list": {"type": "array", "items": {"type": "string"}},
    "dict": {"type": "object"},
}

# Protobuf type mappings
FRAQ_TO_PROTO: Dict[str, str] = {
    "float": "double",
    "int": "int64",
    "str": "string",
    "bool": "bool",
    "bytes": "bytes",
}

# GraphQL type mappings
FRAQ_TO_GRAPHQL: Dict[str, str] = {
    "float": "Float",
    "int": "Int",
    "str": "String",
    "bool": "Boolean",
    "bytes": "String",
}
