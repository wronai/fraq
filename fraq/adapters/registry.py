"""Adapter registry and factory."""

from __future__ import annotations

from typing import Any, Dict, Type

from fraq.query import SourceType
from fraq.adapters.base import BaseAdapter
from fraq.adapters.file_adapter import FileAdapter
from fraq.adapters.http_adapter import HTTPAdapter
from fraq.adapters.sql_adapter import SQLAdapter
from fraq.adapters.sensor_adapter import SensorAdapter
from fraq.adapters.hybrid_adapter import HybridAdapter


_ADAPTERS: Dict[SourceType, Type[BaseAdapter]] = {
    SourceType.FILE: FileAdapter,
    SourceType.HTTP: HTTPAdapter,
    SourceType.SQL: SQLAdapter,
    SourceType.SENSOR: SensorAdapter,
    SourceType.HYBRID: HybridAdapter,
    SourceType.MEMORY: BaseAdapter,
}


def get_adapter(source: SourceType, **kwargs: Any) -> BaseAdapter:
    """Factory: return the right adapter for a source type."""
    cls = _ADAPTERS.get(source)
    if cls is None or cls is BaseAdapter:
        return FileAdapter()
    return cls(**kwargs)
