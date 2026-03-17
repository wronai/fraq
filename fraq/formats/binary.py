"""
Binary format serializers.

Provides msgpack-lite and custom binary encoding.
No dependencies on other format modules (one-way import from prepare).
"""

from __future__ import annotations

import struct
from typing import Any

from fraq.formats.prepare import prepare


def to_binary(data: Any, **kw) -> bytes:
    """Minimal tagged binary encoding.
    
    Format per value: 1-byte type tag + payload.
    Tags: 0x01=float64, 0x02=int64, 0x03=utf8 string, 0x04=bool.
    """
    from fraq.formats.prepare import encode_value
    
    if isinstance(data, dict):
        parts = []
        for k, v in data.items():
            parts.append(encode_value(k))
            parts.append(encode_value(v))
        return b"".join(parts)
    return encode_value(data)


def to_msgpack_lite(data: Any, **kw) -> bytes:
    """Ultra-light MessagePack-ish encoding (no external deps)."""
    return mp_encode(prepare(data))


def mp_encode(obj: Any) -> bytes:
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
            parts.append(mp_encode(item))
        return b"".join(parts)
    if isinstance(obj, dict):
        parts = [b"\xdf" + struct.pack("!I", len(obj))]
        for k, v in obj.items():
            parts.append(mp_encode(k))
            parts.append(mp_encode(v))
        return b"".join(parts)
    return mp_encode(str(obj))
