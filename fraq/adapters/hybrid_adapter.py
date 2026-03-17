"""Hybrid adapter for merging multiple sources."""

from __future__ import annotations

from typing import Any, List, Tuple

from fraq.core import FraqNode
from fraq.query import SourceType
from fraq.adapters.base import BaseAdapter


class HybridAdapter(BaseAdapter):
    """Combine roots from several adapters into one fractal."""

    source_type = SourceType.HYBRID

    def __init__(self) -> None:
        self._sources: List[Tuple[BaseAdapter, str, dict]] = []

    def add(self, adapter: BaseAdapter, uri: str, **opts: Any) -> "HybridAdapter":
        self._sources.append((adapter, uri, opts))
        return self

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
        if not self._sources:
            return FraqNode(position=(0.0, 0.0, 0.0))

        nodes = [a.load_root(u, **o) for a, u, o in self._sources]

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
        for adapter, _, _ in self._sources:
            result = adapter.save(node, uri, fmt, **opts)
            if result:
                return result
        return ""
