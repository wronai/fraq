"""
FraqQL — Unified Query Language for fractal data across sources.

Provides a single query interface regardless of whether data comes from
disk, web APIs, databases, sensors, or hybrid combinations.  Each query
is a *path* through the fractal described by a direction, depth, optional
filters, and an output format.

The query is intentionally source-agnostic: the same FraqQuery works
against a local file, a REST endpoint, a PostgreSQL table, or a live
sensor stream — only the *adapter* changes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple

from fraq.core import FraqNode, FraqSchema, FraqCursor, FieldDef, Vector
from fraq.formats import FormatRegistry


# ---------------------------------------------------------------------------
# Query DSL
# ---------------------------------------------------------------------------


class SourceType(str, Enum):
    """Known data source families."""
    FILE = "file"
    HTTP = "http"
    SQL = "sql"
    SENSOR = "sensor"
    HYBRID = "hybrid"
    MEMORY = "memory"


@dataclass
class FraqFilter:
    """Post-zoom predicate on a record field."""
    field: str
    op: str  # eq | ne | gt | lt | gte | lte | contains | regex
    value: Any

    def matches(self, record: Dict[str, Any]) -> bool:
        val = record.get(self.field)
        if val is None:
            return False
        if self.op == "eq":
            return val == self.value
        if self.op == "ne":
            return val != self.value
        if self.op == "gt":
            return val > self.value
        if self.op == "lt":
            return val < self.value
        if self.op == "gte":
            return val >= self.value
        if self.op == "lte":
            return val <= self.value
        if self.op == "contains":
            return self.value in str(val)
        return False


@dataclass
class FraqQuery:
    """Declarative query against fractal data.

    Parameters
    ----------
    direction : Vector | None
        Zoom direction in hyperspace.
    depth : int
        How many zoom levels to descend.
    branching : int
        Branching factor when generating multiple records.
    fields : list[tuple[str, str]]
        ``(name, type)`` pairs for schema projection.
    filters : list[FraqFilter]
        Post-zoom predicates.
    format : str
        Output serialisation format.
    limit : int | None
        Maximum number of records to return.
    source : SourceType
        Hint about where data originates.
    source_uri : str
        URI or path to the data source.
    meta : dict
        Extra adapter-specific options.
    """

    direction: Optional[Vector] = None
    depth: int = 1
    branching: int = 4
    fields: List[Tuple[str, str]] = field(default_factory=list)
    filters: List[FraqFilter] = field(default_factory=list)
    format: str = "json"
    limit: Optional[int] = None
    source: SourceType = SourceType.MEMORY
    source_uri: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)

    # --- fluent builder API ---

    def zoom(self, depth: int, direction: Optional[Vector] = None) -> "FraqQuery":
        self.depth = depth
        if direction is not None:
            self.direction = direction
        return self

    def select(self, *specs: str) -> "FraqQuery":
        """Add fields, e.g. ``q.select("name:str", "value:float")``."""
        for s in specs:
            name, _, typ = s.partition(":")
            self.fields.append((name.strip(), typ.strip() or "float"))
        return self

    def where(self, field: str, op: str, value: Any) -> "FraqQuery":
        self.filters.append(FraqFilter(field, op, value))
        return self

    def output(self, fmt: str) -> "FraqQuery":
        self.format = fmt
        return self

    def take(self, n: int) -> "FraqQuery":
        self.limit = n
        return self

    def from_source(self, source: SourceType, uri: str = "", **kw: Any) -> "FraqQuery":
        self.source = source
        self.source_uri = uri
        self.meta.update(kw)
        return self


# ---------------------------------------------------------------------------
# Query Executor
# ---------------------------------------------------------------------------


class FraqExecutor:
    """Execute a FraqQuery against a root node.

    The executor builds a FraqSchema from the query's field list, iterates
    records, applies filters, enforces the limit, and serialises the result.
    """

    def __init__(self, root: Optional[FraqNode] = None, dims: int = 3):
        self.root = root or FraqNode(position=tuple(0.0 for _ in range(dims)))

    def execute(self, query: FraqQuery) -> Any:
        """Run *query* and return serialised output."""
        records = list(self._iter_records(query))
        if query.format == "records":
            return records
        return FormatRegistry.serialize(query.format, records)

    def execute_iter(self, query: FraqQuery) -> Iterator[Dict[str, Any]]:
        """Lazily yield filtered records (no serialisation)."""
        yield from self._iter_records(query)

    def _iter_records(self, query: FraqQuery) -> Iterator[Dict[str, Any]]:
        # Navigate to starting node
        start = self.root
        if query.direction is not None:
            start = start.zoom(query.direction, steps=max(1, query.depth // 2))

        # Build schema
        schema = FraqSchema(root=start)
        for name, typ in query.fields:
            schema.add_field(name, typ)

        # If no fields were specified, add a default "value" field
        if not schema.fields:
            schema.add_field("value", "float")

        count = 0
        for rec in schema.records(depth=query.depth, branching=query.branching):
            if all(f.matches(rec) for f in query.filters):
                yield rec
                count += 1
                if query.limit is not None and count >= query.limit:
                    return


# ---------------------------------------------------------------------------
# Convenience: query() one-liner
# ---------------------------------------------------------------------------


def query(
    depth: int = 1,
    direction: Optional[Vector] = None,
    fields: Optional[List[str]] = None,
    format: str = "json",
    limit: Optional[int] = None,
    dims: int = 3,
    seed: int = 0,
    **filters: Any,
) -> Any:
    """One-shot fractal query.

    Examples
    --------
    >>> from fraq.query import query
    >>> query(depth=2, fields=["temp:float", "id:str"], format="csv", limit=10)
    """
    root = FraqNode(position=tuple(0.0 for _ in range(dims)), seed=seed)
    q = FraqQuery(direction=direction, depth=depth, format=format, limit=limit)
    for spec in (fields or []):
        q.select(spec)
    for k, v in filters.items():
        q.where(k, "eq", v)
    return FraqExecutor(root).execute(q)
