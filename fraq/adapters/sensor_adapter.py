"""Sensor/IoT adapter for live data streams."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterator, Optional

from fraq.core import FraqNode, FraqCursor, Vector
from fraq.formats import FormatRegistry
from fraq.query import SourceType
from fraq.adapters.base import BaseAdapter


class SensorAdapter(BaseAdapter):
    """Simulate or consume live sensor data as fractal streams."""

    source_type = SourceType.SENSOR

    def __init__(
        self,
        base_temp: float = 22.0,
        base_humidity: float = 55.0,
        base_pressure: float = 1013.25,
        sample_hz: float = 10.0,
    ):
        self.base_temp = base_temp
        self.base_humidity = base_humidity
        self.base_pressure = base_pressure
        self.sample_hz = sample_hz

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
        from fraq.generators import SensorStreamGenerator
        gen = SensorStreamGenerator(
            base_temp=self.base_temp,
            base_humidity=self.base_humidity,
            base_pressure=self.base_pressure,
        )
        return FraqNode(position=(0.0, 0.0, 0.0), generator=gen)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        path = Path(uri)
        content = FormatRegistry.serialize(fmt, node.value)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return str(path)

    def stream(
        self,
        depth: int = 3,
        count: Optional[int] = None,
        direction: Optional[Vector] = None,
    ) -> Iterator[Dict[str, Any]]:
        root = self.load_root()
        cursor = FraqCursor(root=root)
        i = 0
        while count is None or i < count:
            cursor.advance(direction)
            yield cursor.current.value
            i += 1
