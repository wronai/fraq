"""
Data source adapters.

Each adapter wraps a FraqExecutor and adds source-specific capabilities:
loading root state from disk / HTTP / SQL, persisting zoom results back,
and streaming from live sensors.

All adapters expose the same interface so calling code stays source-agnostic.
"""

from __future__ import annotations

import json
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from fraq.core import FraqNode, FraqCursor, Vector
from fraq.formats import FormatRegistry
from fraq.query import FraqQuery, FraqExecutor, SourceType


# ---------------------------------------------------------------------------
# Base adapter protocol
# ---------------------------------------------------------------------------


class BaseAdapter(ABC):
    """Interface every data-source adapter must implement."""

    source_type: SourceType

    @abstractmethod
    def load_root(self, uri: str, **opts: Any) -> FraqNode:
        """Materialise a root node from the source."""

    @abstractmethod
    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        """Persist a node (or subtree) back to the source.  Return the path/URI."""

    def execute(self, query: FraqQuery) -> Any:
        """Load root from *query.source_uri*, then run the query."""
        root = self.load_root(query.source_uri, **query.meta)
        return FraqExecutor(root).execute(query)

    def execute_iter(self, query: FraqQuery) -> Iterator[Dict[str, Any]]:
        root = self.load_root(query.source_uri, **query.meta)
        yield from FraqExecutor(root).execute_iter(query)


# ---------------------------------------------------------------------------
# File adapter  (JSON / YAML / CSV on disk)
# ---------------------------------------------------------------------------


class FileAdapter(BaseAdapter):
    """Read/write fractal state from local files.

    Supported formats: json, yaml, csv, jsonl, binary.

    Examples
    --------
    >>> adapter = FileAdapter()
    >>> root = adapter.load_root("gradient_root.json")
    >>> deep = root.zoom(steps=5)
    >>> adapter.save(deep, "deep_data.json")
    """

    source_type = SourceType.FILE

    def load_root(self, uri: str, **opts: Any) -> FraqNode:
        path = Path(uri)
        if not path.exists():
            # Derive a deterministic root from the filename
            seed = int(hashlib.sha256(uri.encode()).hexdigest()[:8], 16)
            dims = opts.get("dims", 3)
            return FraqNode(position=tuple(0.0 for _ in range(dims)), seed=seed)

        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        return self._dict_to_node(data)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        path = Path(uri)
        content = FormatRegistry.serialize(fmt, node.to_dict(max_depth=opts.get("max_depth", 1)))
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return str(path.resolve())

    @staticmethod
    def _dict_to_node(data: Dict[str, Any]) -> FraqNode:
        return FraqNode(
            position=tuple(data.get("position", [0.0, 0.0, 0.0])),
            depth=data.get("depth", 0),
            seed=data.get("seed", 0),
        )


# ---------------------------------------------------------------------------
# HTTP adapter  (REST / GraphQL endpoints)
# ---------------------------------------------------------------------------


class HTTPAdapter(BaseAdapter):
    """Fetch fractal roots from remote HTTP APIs and push results back.

    The adapter does **not** depend on ``requests`` at import time — it
    only needs it when ``load_root`` / ``save`` are actually called, so
    the library stays lightweight.

    URI format
    ----------
    ``https://api.example.com/gradient/root``

    Extra *opts*:
        headers : dict         — custom HTTP headers
        method  : str          — GET (default) or POST
        timeout : int          — seconds (default 30)

    Examples
    --------
    >>> adapter = HTTPAdapter()
    >>> root = adapter.load_root("https://api.gradient.example/root")
    >>> data = root.zoom(steps=20).to_dict()
    """

    source_type = SourceType.HTTP

    def load_root(self, uri: str, **opts: Any) -> FraqNode:
        if not uri:
            return FraqNode(position=(0.0, 0.0, 0.0))
        try:
            import requests  # noqa: lazy import
            method = opts.get("method", "GET")
            headers = opts.get("headers", {})
            timeout = opts.get("timeout", 30)
            resp = requests.request(method, uri, headers=headers, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            return FileAdapter._dict_to_node(data)
        except Exception:
            # Fallback: deterministic root from URI
            seed = int(hashlib.sha256(uri.encode()).hexdigest()[:8], 16)
            return FraqNode(position=(0.0, 0.0, 0.0), seed=seed)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        try:
            import requests  # noqa
            payload = FormatRegistry.serialize(fmt, node.to_dict(max_depth=1))
            headers = opts.get("headers", {"Content-Type": "application/json"})
            timeout = opts.get("timeout", 30)
            resp = requests.post(uri, data=payload, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return uri
        except Exception:
            return ""


# ---------------------------------------------------------------------------
# SQL adapter  (PostgreSQL / SQLite — via mapping)
# ---------------------------------------------------------------------------


class SQLAdapter(BaseAdapter):
    """Map fractal nodes to/from relational tables.

    Instead of requiring a live DB connection the adapter defines the
    *mapping* between SQL rows and fractal coordinates so that the same
    query language works.  A ``row_to_node`` callable transforms a DB row
    dict into a FraqNode.

    Parameters
    ----------
    row_to_node : callable
        ``(row_dict) -> FraqNode``.  Defaults to treating ``value`` as
        seed and the remaining numeric columns as position components.
    table : str
        Table name (informational, used in ``save``).

    Examples
    --------
    >>> adapter = SQLAdapter(table="gradient_nodes")
    >>> root = adapter.load_root("", rows=[{"id": 1, "x": 0.0, "y": 0.0, "value": 0}])
    >>> data = root.zoom(steps=5).to_dict()
    """

    source_type = SourceType.SQL

    def __init__(
        self,
        table: str = "fraq_nodes",
        row_to_node: Optional[Any] = None,
    ):
        self.table = table
        self._row_to_node = row_to_node or self._default_row_to_node

    def load_root(self, uri: str, **opts: Any) -> FraqNode:
        rows = opts.get("rows")
        if rows and len(rows) > 0:
            return self._row_to_node(rows[0])
        # Fallback: derive from table name
        seed = int(hashlib.sha256(self.table.encode()).hexdigest()[:8], 16)
        dims = opts.get("dims", 3)
        return FraqNode(position=tuple(0.0 for _ in range(dims)), seed=seed)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        """Return an INSERT statement (the caller executes it)."""
        d = node.to_dict()
        cols = ", ".join(d.keys())
        vals = ", ".join(repr(v) for v in d.values())
        return f"INSERT INTO {self.table} ({cols}) VALUES ({vals});"

    def generate_sql_function(self, dims: int = 3) -> str:
        """Generate a PostgreSQL function that wraps zoom()."""
        return f"""
CREATE OR REPLACE FUNCTION {self.table}_zoom(
    p_level INT,
    p_direction FLOAT[{dims}]
) RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    -- This is a stub; actual zoom runs in Python via fraq
    SELECT json_build_object(
        'level', p_level,
        'direction', p_direction,
        'table', '{self.table}'
    ) INTO result;
    RETURN result;
END;
$$ LANGUAGE plpgsql;
"""

    @staticmethod
    def _default_row_to_node(row: Dict[str, Any]) -> FraqNode:
        numeric_vals = [v for v in row.values() if isinstance(v, (int, float))]
        pos = tuple(float(v) for v in numeric_vals[:3]) or (0.0, 0.0, 0.0)
        seed = int(numeric_vals[0]) if numeric_vals else 0
        return FraqNode(position=pos, seed=seed)


# ---------------------------------------------------------------------------
# Sensor / IoT adapter
# ---------------------------------------------------------------------------


class SensorAdapter(BaseAdapter):
    """Simulate or consume live sensor data as fractal streams.

    In simulation mode (no URI) the adapter generates infinite deterministic
    sensor readings via the fractal zoom.  With a URI it could connect to
    MQTT / Kafka / serial — the interface is the same.

    Examples
    --------
    >>> adapter = SensorAdapter(base_temp=23.5, sample_hz=10)
    >>> for reading in adapter.stream(depth=3, count=100):
    ...     print(reading)
    """

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
        """Yield sensor readings indefinitely (or up to *count*)."""
        root = self.load_root()
        cursor = FraqCursor(root=root)
        i = 0
        while count is None or i < count:
            cursor.advance(direction)
            yield cursor.current.value
            i += 1


# ---------------------------------------------------------------------------
# Hybrid adapter — merge multiple sources
# ---------------------------------------------------------------------------


class HybridAdapter(BaseAdapter):
    """Combine roots from several adapters into one fractal.

    The merged root's seed is derived from all child seeds, and its
    position is the element-wise mean.

    Examples
    --------
    >>> h = HybridAdapter()
    >>> h.add(FileAdapter(), "local_backup.json")
    >>> h.add(HTTPAdapter(), "https://api.example.com/root")
    >>> merged = h.load_root("")
    """

    source_type = SourceType.HYBRID

    def __init__(self) -> None:
        self._sources: List[tuple[BaseAdapter, str, dict]] = []

    def add(self, adapter: BaseAdapter, uri: str, **opts: Any) -> "HybridAdapter":
        self._sources.append((adapter, uri, opts))
        return self

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
        if not self._sources:
            return FraqNode(position=(0.0, 0.0, 0.0))

        nodes = [a.load_root(u, **o) for a, u, o in self._sources]

        # Merge positions (mean) and seeds (xor)
        dims = max(len(n.position) for n in nodes)
        merged_pos = []
        for i in range(dims):
            vals = [n.position[i] if i < len(n.position) else 0.0 for n in nodes]
            merged_pos.append(sum(vals) / len(vals))

        merged_seed = 0
        for n in nodes:
            merged_seed ^= n.seed

        return FraqNode(
            position=tuple(merged_pos),
            seed=merged_seed,
            meta={"merged_from": len(nodes)},
        )

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        # Delegate to the first adapter that can save
        for adapter, _, _ in self._sources:
            result = adapter.save(node, uri, fmt, **opts)
            if result:
                return result
        return ""


# ---------------------------------------------------------------------------
# Adapter registry
# ---------------------------------------------------------------------------


_ADAPTERS: Dict[SourceType, type] = {
    SourceType.FILE: FileAdapter,
    SourceType.HTTP: HTTPAdapter,
    SourceType.SQL: SQLAdapter,
    SourceType.SENSOR: SensorAdapter,
    SourceType.HYBRID: HybridAdapter,
    SourceType.MEMORY: BaseAdapter,  # type: ignore[assignment]
}


def get_adapter(source: SourceType, **kwargs: Any) -> BaseAdapter:
    """Factory: return the right adapter for a source type."""
    cls = _ADAPTERS.get(source)
    if cls is None or cls is BaseAdapter:
        # Return a minimal in-memory adapter
        return FileAdapter()
    return cls(**kwargs)  # type: ignore[call-arg]
