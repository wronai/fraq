"""
Output format registry.

Serialise FraqNode trees and schema records into concrete formats.
New formats can be registered at runtime.
"""

from __future__ import annotations

import csv
import io
import json
import struct
from typing import Any, Callable, Dict, Iterator, List, Optional

from fraq.core import FraqNode, FraqSchema


class FormatRegistry:
    """Registry of serialisation backends."""

    _formats: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str, fn: Optional[Callable] = None):
        """Register a formatter.  Can be used as a decorator."""
        if fn is not None:
            cls._formats[name] = fn
            return fn

        def decorator(f: Callable) -> Callable:
            cls._formats[name] = f
            return f

        return decorator

    @classmethod
    def get(cls, name: str) -> Callable:
        if name not in cls._formats:
            raise KeyError(f"Unknown format '{name}'. Available: {list(cls._formats)}")
        return cls._formats[name]

    @classmethod
    def available(cls) -> List[str]:
        return list(cls._formats.keys())

    @classmethod
    def serialize(cls, name: str, data: Any, **kwargs) -> Any:
        return cls.get(name)(data, **kwargs)


# ---------------------------------------------------------------------------
# Built-in formats
# ---------------------------------------------------------------------------


@FormatRegistry.register("json")
def _to_json(data: Any, *, indent: int = 2, **kw) -> str:
    """Serialise to JSON string."""
    return json.dumps(_prepare(data), indent=indent, default=str)


@FormatRegistry.register("jsonl")
def _to_jsonl(data: Any, **kw) -> str:
    """Serialise iterable of records to JSON-Lines."""
    if isinstance(data, dict):
        data = [data]
    lines = [json.dumps(_prepare(r), default=str) for r in data]
    return "\n".join(lines)


@FormatRegistry.register("csv")
def _to_csv(data: Any, **kw) -> str:
    """Serialise list of flat dicts to CSV."""
    if isinstance(data, dict):
        data = [data]
    data = [_prepare(r) for r in data]
    if not data:
        return ""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(data[0].keys()))
    writer.writeheader()
    writer.writerows(data)
    return buf.getvalue()


@FormatRegistry.register("yaml")
def _to_yaml(data: Any, **kw) -> str:
    """Serialise to YAML (simple dumper, no PyYAML dependency)."""
    return _simple_yaml(_prepare(data))


@FormatRegistry.register("binary")
def _to_binary(data: Any, **kw) -> bytes:
    """Minimal tagged binary encoding.

    Format per value: 1-byte type tag + payload.
    Tags: 0x01=float64, 0x02=int64, 0x03=utf8 string, 0x04=bool.
    """
    if isinstance(data, dict):
        parts = []
        for k, v in data.items():
            parts.append(_encode_value(k))
            parts.append(_encode_value(v))
        return b"".join(parts)
    return _encode_value(data)


@FormatRegistry.register("msgpack_lite")
def _to_msgpack_lite(data: Any, **kw) -> bytes:
    """Ultra-light MessagePack-ish encoding (no external deps)."""
    return _mp_encode(_prepare(data))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _prepare(obj: Any) -> Any:
    """Recursively convert FraqNode / bytes / tuples for JSON compat."""
    if isinstance(obj, FraqNode):
        return obj.to_dict()
    if isinstance(obj, bytes):
        return obj.hex()
    if isinstance(obj, tuple):
        return list(obj)
    if isinstance(obj, dict):
        return {str(k): _prepare(v) for k, v in obj.items()}
    if isinstance(obj, (list, Iterator)):
        return [_prepare(i) for i in obj]
    return obj


def _simple_yaml(obj: Any, indent: int = 0) -> str:
    """Dead-simple YAML emitter (no dependency)."""
    prefix = "  " * indent
    if isinstance(obj, dict):
        lines = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{prefix}{k}:")
                lines.append(_simple_yaml(v, indent + 1))
            else:
                lines.append(f"{prefix}{k}: {v}")
        return "\n".join(lines)
    if isinstance(obj, list):
        lines = []
        for item in obj:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.append(_simple_yaml(item, indent + 1))
            else:
                lines.append(f"{prefix}- {item}")
        return "\n".join(lines)
    return f"{prefix}{obj}"


def _encode_value(v: Any) -> bytes:
    if isinstance(v, float):
        return b"\x01" + struct.pack("!d", v)
    if isinstance(v, int):
        return b"\x02" + struct.pack("!q", v)
    if isinstance(v, str):
        raw = v.encode("utf-8")
        return b"\x03" + struct.pack("!I", len(raw)) + raw
    if isinstance(v, bool):
        return b"\x04" + (b"\x01" if v else b"\x00")
    return b"\x03" + struct.pack("!I", 0)


def _mp_encode(obj: Any) -> bytes:
    """Minimal msgpack-ish encoder."""
    if obj is None:
        return b"\xc0"
    if isinstance(obj, bool):
        return b"\xc3" if obj else b"\xc2"
    if isinstance(obj, int):
        return b"\xd3" + struct.pack("!q", obj)
    if isinstance(obj, float):
        return b"\xcb" + struct.pack("!d", obj)
    if isinstance(obj, str):
        raw = obj.encode("utf-8")
        return b"\xdb" + struct.pack("!I", len(raw)) + raw
    if isinstance(obj, (list, tuple)):
        parts = [b"\xdd" + struct.pack("!I", len(obj))]
        for item in obj:
            parts.append(_mp_encode(item))
        return b"".join(parts)
    if isinstance(obj, dict):
        parts = [b"\xdf" + struct.pack("!I", len(obj))]
        for k, v in obj.items():
            parts.append(_mp_encode(k))
            parts.append(_mp_encode(v))
        return b"".join(parts)
    return _mp_encode(str(obj))
