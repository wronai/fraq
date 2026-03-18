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
    """Minimal msgpack-ish encoder using lookup table.
    
    Refactored: CC 11→2 (was if/elif chain, now dispatch table).
    """
    encoder = _ENCODERS.get(type(obj))
    if encoder:
        return encoder(obj)
    return _encode_fallback(obj)


# Type-specific encoders (CC≤2 each)
def _encode_none(obj: None) -> bytes:
    return b"\xc0"


def _encode_bool(obj: bool) -> bytes:
    return b"\xc3" if obj else b"\xc2"


def _encode_int(obj: int) -> bytes:
    return b"\xd3" + struct.pack("!q", obj)


def _encode_float(obj: float) -> bytes:
    return b"\xcb" + struct.pack("!d", obj)


def _encode_str(obj: str) -> bytes:
    raw = obj.encode("utf-8")
    return b"\xdb" + struct.pack("!I", len(raw)) + raw


def _encode_list(obj: list | tuple) -> bytes:
    parts = [b"\xdd" + struct.pack("!I", len(obj))]
    for item in obj:
        parts.append(mp_encode(item))
    return b"".join(parts)


def _encode_dict(obj: dict) -> bytes:
    parts = [b"\xdf" + struct.pack("!I", len(obj))]
    for k, v in obj.items():
        parts.append(mp_encode(k))
        parts.append(mp_encode(v))
    return b"".join(parts)


def _encode_fallback(obj: Any) -> bytes:
    return _encode_str(str(obj))


# Lookup table: type → encoder function
_ENCODERS: dict[type, Callable[[Any], bytes]] = {
    type(None): _encode_none,
    bool: _encode_bool,
    int: _encode_int,
    float: _encode_float,
    str: _encode_str,
    list: _encode_list,
    tuple: _encode_list,
    dict: _encode_dict,
}
