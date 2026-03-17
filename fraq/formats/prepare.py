"""
Data preparation utilities for format serialization.

This module provides pure functions for preparing data before serialization,
ensuring no circular dependencies with serializers.
"""

from __future__ import annotations

import struct
from typing import Any, Iterator


def prepare(obj: Any) -> Any:
    """Recursively convert FraqNode / bytes / tuples for JSON compat."""
    # Import here to avoid circular dependency at module level
    from fraq.core import FraqNode
    
    if isinstance(obj, FraqNode):
        return obj.to_dict()
    if isinstance(obj, bytes):
        return obj.hex()
    if isinstance(obj, tuple):
        return list(obj)
    if isinstance(obj, dict):
        return {str(k): prepare(v) for k, v in obj.items()}
    if isinstance(obj, (list, Iterator)):
        return [prepare(i) for i in obj]
    return obj


def encode_value(v: Any) -> bytes:
    """Encode a single value to binary format.
    
    Format: 1-byte type tag + payload.
    Tags: 0x01=float64, 0x02=int64, 0x03=utf8 string, 0x04=bool.
    """
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
