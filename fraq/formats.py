"""
Output format registry - BACKWARD COMPATIBILITY SHIM.

This module re-exports from fraq.formats package for backward compatibility.
New code should import directly from fraq.formats.

Example:
    # Old (still works):
    from fraq.formats import FormatRegistry, _to_json
    
    # New (recommended):
    from fraq.formats import FormatRegistry, to_json
"""

from __future__ import annotations

# Re-export everything from the new package structure
from fraq.formats import (
    FormatRegistry,
    prepare,
    encode_value,
    to_json,
    to_jsonl,
    to_csv,
    to_yaml,
    simple_yaml,
    to_binary,
    to_msgpack_lite,
    mp_encode,
    # Backward compatibility aliases
    _prepare,
    _encode_value,
    _simple_yaml,
    _mp_encode,
    _to_json,
    _to_jsonl,
    _to_csv,
    _to_yaml,
    _to_binary,
    _to_msgpack_lite,
)

__all__ = [
    "FormatRegistry",
    "prepare",
    "encode_value",
    "to_json",
    "to_jsonl",
    "to_csv",
    "to_yaml",
    "simple_yaml",
    "to_binary",
    "to_msgpack_lite",
    "mp_encode",
    # Backward compatibility
    "_prepare",
    "_encode_value",
    "_simple_yaml",
    "_mp_encode",
    "_to_json",
    "_to_jsonl",
    "_to_csv",
    "_to_yaml",
    "_to_binary",
    "_to_msgpack_lite",
]
