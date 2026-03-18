"""
JSON Schema export.

Generate JSON Schema for validation from FraqSchema.
"""

from __future__ import annotations

from typing import Any, Dict, List

from fraq.core import FraqSchema
from fraq.export.common import FRAQ_TO_JSON_SCHEMA


def to_json_schema(
    schema: FraqSchema,
    title: str = "FraqRecord",
) -> Dict[str, Any]:
    """Generate a JSON Schema for validation."""
    properties: Dict[str, Any] = {}
    required: List[str] = []
    for f in schema.fields:
        properties[f.name] = FRAQ_TO_JSON_SCHEMA.get(f.type, {"type": "string"})
        required.append(f.name)

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "type": "object",
        "properties": properties,
        "required": required,
    }
