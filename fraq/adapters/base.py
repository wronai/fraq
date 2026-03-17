"""Base adapter protocol for fraq."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator

from fraq.core import FraqNode
from fraq.query import FraqQuery, FraqExecutor, SourceType


class BaseAdapter(ABC):
    """Interface every data-source adapter must implement."""

    source_type: SourceType

    @abstractmethod
    def load_root(self, uri: str, **opts: Any) -> FraqNode:
        """Materialise a root node from the source."""

    @abstractmethod
    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        """Persist a node (or subtree) back to the source. Return the path/URI."""

    def execute(self, query: FraqQuery) -> Any:
        """Load root from *query.source_uri*, then run the query."""
        root = self.load_root(query.source_uri, **query.meta)
        return FraqExecutor(root).execute(query)

    def execute_iter(self, query: FraqQuery) -> Iterator[Dict[str, Any]]:
        root = self.load_root(query.source_uri, **query.meta)
        yield from FraqExecutor(root).execute_iter(query)
