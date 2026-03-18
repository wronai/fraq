"""
OpenAPI 3.0 schema export.

Generate OpenAPI 3.0 specifications from FraqSchema.
"""

from __future__ import annotations

from typing import Any, Dict, List

from fraq.core import FraqSchema
from fraq.export.common import FRAQ_TO_JSON_SCHEMA


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
        properties[f.name] = FRAQ_TO_JSON_SCHEMA.get(f.type, {"type": "string"})
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
