"""
AsyncAPI 3.0 schema export.

Generate AsyncAPI 3.0 specifications for streaming channels.
"""

from __future__ import annotations

from typing import Any, Dict

from fraq.core import FraqSchema
from fraq.export.common import FRAQ_TO_JSON_SCHEMA


def to_asyncapi(
    schema: FraqSchema,
    title: str = "Fraq Streams",
    version: str = "1.0.0",
) -> Dict[str, Any]:
    """Generate an AsyncAPI 3.0 specification for streaming channels."""
    properties: Dict[str, Any] = {}
    for f in schema.fields:
        properties[f.name] = FRAQ_TO_JSON_SCHEMA.get(f.type, {"type": "string"})

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
