"""
NLP2CMD schema export.

Export FraqSchema as NLP2CMD command schemas and action registry.
"""

from __future__ import annotations

from typing import Any, Dict, List

from fraq.core import FraqSchema
from fraq.export.common import FRAQ_TO_JSON_SCHEMA


def to_nlp2cmd_schema(
    schema: FraqSchema,
    command_name: str = "fraq",
    version: str = "1.0",
    category: str = "data",
) -> Dict[str, Any]:
    """Export a FraqSchema as an NLP2CMD command schema."""
    parameters = []
    for f in schema.fields:
        parameters.append({
            "name": f.name,
            "type": FRAQ_TO_JSON_SCHEMA.get(f.type, {"type": "string"}).get("type", "string"),
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


def to_nlp2cmd_actions(schema: FraqSchema) -> List[Dict[str, Any]]:
    """Export fraq operations as NLP2CMD ActionRegistry entries."""
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
