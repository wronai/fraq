"""
Text format serializers.

Provides JSON, JSONL, CSV, and YAML serialization.
One-way import from prepare module (no cycles).
"""

from __future__ import annotations

import csv
import io
import json
from typing import Any

from fraq.formats.prepare import prepare


def to_json(data: Any, *, indent: int = 2, **kw) -> str:
    """Serialise to JSON string."""
    return json.dumps(prepare(data), indent=indent, default=str)


def to_jsonl(data: Any, **kw) -> str:
    """Serialise iterable of records to JSON-Lines."""
    if isinstance(data, dict):
        data = [data]
    lines = [json.dumps(prepare(r), default=str) for r in data]
    return "\n".join(lines)


def to_csv(data: Any, **kw) -> str:
    """Serialise list of flat dicts to CSV."""
    if isinstance(data, dict):
        data = [data]
    data = [prepare(r) for r in data]
    if not data:
        return ""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(data[0].keys()))
    writer.writeheader()
    writer.writerows(data)
    return buf.getvalue()


def to_yaml(data: Any, **kw) -> str:
    """Serialise to YAML (simple dumper, no PyYAML dependency)."""
    return simple_yaml(prepare(data))


def simple_yaml(obj: Any, indent: int = 0) -> str:
    """Dead-simple YAML emitter (no dependency)."""
    prefix = "  " * indent
    if isinstance(obj, dict):
        lines = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{prefix}{k}:")
                lines.append(simple_yaml(v, indent + 1))
            else:
                lines.append(f"{prefix}{k}: {v}")
        return "\n".join(lines)
    if isinstance(obj, list):
        lines = []
        for item in obj:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.append(simple_yaml(item, indent + 1))
            else:
                lines.append(f"{prefix}- {item}")
        return "\n".join(lines)
    return f"{prefix}{obj}"
