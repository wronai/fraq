"""
Schema export for interoperability.

Generate schema definitions from FraqSchema in formats understood by:
- NLP2CMD (command schemas + action registry)
- OpenAPI 3.0  (REST API spec)
- GraphQL      (type definitions)
- AsyncAPI 3.0 (streaming channels)
- gRPC / Protobuf (.proto file)
- JSON Schema  (generic validation)

This allows fraq's infinite fractal data to be consumed by any
standards-compliant client without knowing about fractals at all.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from fraq.core import FraqSchema, FieldDef


# ---------------------------------------------------------------------------
# Type mapping
# ---------------------------------------------------------------------------

_FRAQ_TO_JSON_SCHEMA = {
    "float": {"type": "number", "format": "double"},
    "int": {"type": "integer", "format": "int64"},
    "str": {"type": "string"},
    "bool": {"type": "boolean"},
    "bytes": {"type": "string", "format": "byte"},
    "list": {"type": "array", "items": {"type": "string"}},
    "dict": {"type": "object"},
}

_FRAQ_TO_PROTO = {
    "float": "double",
    "int": "int64",
    "str": "string",
    "bool": "bool",
    "bytes": "bytes",
}

_FRAQ_TO_GRAPHQL = {
    "float": "Float",
    "int": "Int",
    "str": "String",
    "bool": "Boolean",
    "bytes": "String",
}


# ---------------------------------------------------------------------------
# NLP2CMD integration
# ---------------------------------------------------------------------------


def to_nlp2cmd_schema(
    schema: FraqSchema,
    command_name: str = "fraq",
    version: str = "1.0",
    category: str = "data",
) -> Dict[str, Any]:
    """Export a FraqSchema as an NLP2CMD command schema.

    The output matches the ``command_schemas/*.json`` format expected by
    NLP2CMD's ``SchemaRegistry``, including parameters, templates, and
    example commands.

    Returns
    -------
    dict
        NLP2CMD-compatible command schema.
    """
    parameters = []
    for f in schema.fields:
        parameters.append({
            "name": f.name,
            "type": _FRAQ_TO_JSON_SCHEMA.get(f.type, {"type": "string"}).get("type", "string"),
            "required": True,
            "description": f"Fractal field '{f.name}' (type: {f.type})",
        })

    # Always include zoom parameters
    parameters.extend([
        {
            "name": "depth",
            "type": "integer",
            "required": False,
            "description": "Zoom depth into the fractal (default: 1)",
        },
        {
            "name": "direction",
            "type": "array",
            "required": False,
            "description": "Zoom direction vector in hyperspace",
        },
        {
            "name": "format",
            "type": "string",
            "required": False,
            "description": "Output format: json, csv, yaml, binary, jsonl, msgpack_lite",
        },
        {
            "name": "limit",
            "type": "integer",
            "required": False,
            "description": "Maximum number of records to return",
        },
    ])

    field_names = [f.name for f in schema.fields]
    field_list = ",".join(f"{f.name}:{f.type}" for f in schema.fields)

    templates = [
        f"fraq query --fields \"{field_list}\" --depth {{depth}}",
        f"fraq query --fields \"{field_list}\" --format {{format}}",
        f"fraq zoom --depth {{depth}} --direction {{direction}}",
        "fraq stream --count {limit}",
    ]

    return {
        "command": command_name,
        "version": version,
        "description": f"Query fractal data with fields: {', '.join(field_names)}",
        "category": category,
        "parameters": parameters,
        "templates": templates,
        "examples": [
            {
                "input": f"Show all {field_names[0] if field_names else 'data'} at depth 3",
                "command": f'fraq query --fields "{field_list}" --depth 3 --format json',
            },
            {
                "input": f"Stream 100 records as CSV",
                "command": f'fraq stream --count 100 --format csv --fields "{field_list}"',
            },
            {
                "input": f"Zoom into direction [1,0,0] at depth 5",
                "command": 'fraq zoom --depth 5 --direction "[1,0,0]" --format json',
            },
        ],
    }


def to_nlp2cmd_actions(
    schema: FraqSchema,
) -> List[Dict[str, Any]]:
    """Export fraq operations as NLP2CMD ActionRegistry entries.

    Each action corresponds to a core fraq operation (zoom, query, stream,
    schema) and includes parameter schemas for validation.
    """
    field_params = [
        {"name": f.name, "type": f.type, "required": False}
        for f in schema.fields
    ]

    return [
        {
            "name": "fraq_zoom",
            "description": "Zoom into the fractal at a given depth and direction",
            "parameters": [
                {"name": "depth", "type": "int", "required": True},
                {"name": "direction", "type": "list", "required": False},
                {"name": "format", "type": "str", "required": False, "default": "json"},
            ],
        },
        {
            "name": "fraq_query",
            "description": "Query fractal data with typed fields and filters",
            "parameters": [
                *field_params,
                {"name": "depth", "type": "int", "required": False, "default": 1},
                {"name": "limit", "type": "int", "required": False},
                {"name": "format", "type": "str", "required": False, "default": "json"},
            ],
        },
        {
            "name": "fraq_stream",
            "description": "Stream records from the fractal cursor",
            "parameters": [
                {"name": "count", "type": "int", "required": True},
                {"name": "direction", "type": "list", "required": False},
                {"name": "format", "type": "str", "required": False, "default": "json"},
            ],
        },
        {
            "name": "fraq_save",
            "description": "Save fractal data to a target (file, HTTP, SQL)",
            "parameters": [
                {"name": "uri", "type": "str", "required": True},
                {"name": "format", "type": "str", "required": False, "default": "json"},
                {"name": "source", "type": "str", "required": False, "default": "file"},
            ],
        },
    ]


# ---------------------------------------------------------------------------
# OpenAPI 3.0
# ---------------------------------------------------------------------------


def to_openapi(
    schema: FraqSchema,
    title: str = "Fraq Fractal API",
    version: str = "1.0.0",
    base_path: str = "/api/fraq",
) -> Dict[str, Any]:
    """Generate an OpenAPI 3.0 specification."""
    properties: Dict[str, Any] = {}
    required: List[str] = []
    for f in schema.fields:
        properties[f.name] = _FRAQ_TO_JSON_SCHEMA.get(f.type, {"type": "string"})
        required.append(f.name)

    return {
        "openapi": "3.0.3",
        "info": {"title": title, "version": version},
        "paths": {
            f"{base_path}/zoom": {
                "get": {
                    "summary": "Zoom into the fractal",
                    "parameters": [
                        {"name": "depth", "in": "query", "schema": {"type": "integer"}, "required": True},
                        {"name": "direction", "in": "query", "schema": {"type": "string"}, "description": "JSON array of floats"},
                        {"name": "format", "in": "query", "schema": {"type": "string", "enum": ["json", "csv", "yaml", "binary"]}, "required": False},
                    ],
                    "responses": {
                        "200": {
                            "description": "Fractal data at requested depth",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/FraqRecord"}}},
                        }
                    },
                }
            },
            f"{base_path}/query": {
                "post": {
                    "summary": "Query fractal data with filters",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/FraqQuery"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Array of matching records",
                            "content": {
                                "application/json": {
                                    "schema": {"type": "array", "items": {"$ref": "#/components/schemas/FraqRecord"}}
                                }
                            },
                        }
                    },
                }
            },
            f"{base_path}/stream": {
                "get": {
                    "summary": "Stream fractal records via SSE",
                    "parameters": [
                        {"name": "count", "in": "query", "schema": {"type": "integer"}},
                        {"name": "direction", "in": "query", "schema": {"type": "string"}},
                    ],
                    "responses": {
                        "200": {
                            "description": "Server-Sent Events stream",
                            "content": {"text/event-stream": {}},
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "FraqRecord": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
                "FraqQuery": {
                    "type": "object",
                    "properties": {
                        "depth": {"type": "integer", "default": 1},
                        "direction": {"type": "array", "items": {"type": "number"}},
                        "fields": {"type": "array", "items": {"type": "string"}},
                        "filters": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {"type": "string"},
                                    "op": {"type": "string", "enum": ["eq", "ne", "gt", "lt", "gte", "lte", "contains"]},
                                    "value": {},
                                },
                            },
                        },
                        "format": {"type": "string", "default": "json"},
                        "limit": {"type": "integer"},
                    },
                },
            }
        },
    }


# ---------------------------------------------------------------------------
# GraphQL
# ---------------------------------------------------------------------------


def to_graphql(schema: FraqSchema, type_name: str = "FraqRecord") -> str:
    """Generate a GraphQL schema definition."""
    lines = [f"type {type_name} {{"]
    for f in schema.fields:
        gql_type = _FRAQ_TO_GRAPHQL.get(f.type, "String")
        lines.append(f"  {f.name}: {gql_type}!")
    lines.append("}")

    lines.append("")
    lines.append("type FraqNode {")
    lines.append("  value: Float!")
    lines.append("  depth: Int!")
    lines.append("  position: [Float!]!")
    lines.append(f"  children: [{type_name}!]")
    lines.append("}")

    lines.append("")
    lines.append("type Query {")
    lines.append(f"  zoom(depth: Int!, direction: [Float!]): FraqNode!")
    lines.append(f"  query(depth: Int, fields: [String!], limit: Int): [{type_name}!]!")
    lines.append(f"  stream(count: Int!, direction: [Float!]): [{type_name}!]!")
    lines.append("}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# AsyncAPI 3.0
# ---------------------------------------------------------------------------


def to_asyncapi(
    schema: FraqSchema,
    title: str = "Fraq Streams",
    version: str = "1.0.0",
) -> Dict[str, Any]:
    """Generate an AsyncAPI 3.0 specification for streaming channels."""
    properties: Dict[str, Any] = {}
    for f in schema.fields:
        properties[f.name] = _FRAQ_TO_JSON_SCHEMA.get(f.type, {"type": "string"})

    return {
        "asyncapi": "3.0.0",
        "info": {"title": title, "version": version},
        "channels": {
            "fraq/stream": {
                "address": "fraq/{direction}/stream",
                "messages": {
                    "fraqRecord": {
                        "name": "FraqRecord",
                        "contentType": "application/json",
                        "payload": {
                            "$ref": "#/components/schemas/FraqRecord",
                        },
                    }
                },
            },
            "fraq/zoomed": {
                "address": "fraq/zoomed/{depth}",
                "messages": {
                    "zoomedNode": {
                        "payload": {"$ref": "#/components/schemas/FraqNode"},
                    }
                },
            },
        },
        "components": {
            "schemas": {
                "FraqRecord": {
                    "type": "object",
                    "properties": properties,
                },
                "FraqNode": {
                    "type": "object",
                    "properties": {
                        "value": {"type": "number"},
                        "depth": {"type": "integer"},
                        "position": {"type": "array", "items": {"type": "number"}},
                        "children": {"type": "object"},
                    },
                },
            }
        },
    }


# ---------------------------------------------------------------------------
# gRPC / Protobuf
# ---------------------------------------------------------------------------


def to_proto(
    schema: FraqSchema,
    package: str = "fraq",
    message_name: str = "FraqRecord",
) -> str:
    """Generate a .proto file."""
    lines = [
        'syntax = "proto3";',
        f"package {package};",
        "",
        f"message {message_name} {{",
    ]
    for i, f in enumerate(schema.fields, start=1):
        proto_type = _FRAQ_TO_PROTO.get(f.type, "string")
        lines.append(f"  {proto_type} {f.name} = {i};")
    lines.append("}")

    lines.append("")
    lines.append("message ZoomRequest {")
    lines.append("  int32 depth = 1;")
    lines.append("  repeated double direction = 2;")
    lines.append("  string format = 3;")
    lines.append("  int32 limit = 4;")
    lines.append("}")

    lines.append("")
    lines.append("message ZoomResponse {")
    lines.append(f"  repeated {message_name} records = 1;")
    lines.append("  int32 total = 2;")
    lines.append("}")

    lines.append("")
    lines.append("message StreamRequest {")
    lines.append("  int32 count = 1;")
    lines.append("  repeated double direction = 2;")
    lines.append("}")

    lines.append("")
    lines.append(f"service FraqService {{")
    lines.append(f"  rpc Zoom(ZoomRequest) returns (ZoomResponse);")
    lines.append(f"  rpc Stream(StreamRequest) returns (stream {message_name});")
    lines.append("}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON Schema
# ---------------------------------------------------------------------------


def to_json_schema(
    schema: FraqSchema,
    title: str = "FraqRecord",
) -> Dict[str, Any]:
    """Generate a JSON Schema for validation."""
    properties: Dict[str, Any] = {}
    required: List[str] = []
    for f in schema.fields:
        properties[f.name] = _FRAQ_TO_JSON_SCHEMA.get(f.type, {"type": "string"})
        required.append(f.name)

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "type": "object",
        "properties": properties,
        "required": required,
    }
