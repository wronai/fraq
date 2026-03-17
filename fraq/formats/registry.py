"""
Format registry - clean registry without serialization logic.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional


class FormatRegistry:
    """Registry of serialisation backends."""

    _formats: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str, fn: Optional[Callable] = None):
        """Register a formatter. Can be used as a decorator."""
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
