"""Data models for text2fraq."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from fraq.query import FraqQuery


@dataclass
class ParsedQuery:
    """Parsed natural language query."""

    fields: list[str]
    depth: int
    format: str
    filters: dict[str, Any] = field(default_factory=dict)
    dims: int = 3
    direction: tuple[float, ...] | None = None
    limit: int | None = None

    def to_fraq_query(self) -> FraqQuery:
        """Convert to FraqQuery object."""
        query = FraqQuery().zoom(self.depth, direction=self.direction)
        query = query.select(*self.fields).output(self.format)
        for field_name, predicate in self.filters.items():
            if isinstance(predicate, dict):
                for op, value in predicate.items():
                    query = query.where(field_name, op, value)
            else:
                query = query.where(field_name, "eq", predicate)
        if self.limit:
            query = query.take(self.limit)
        return query


class LLMClient(Protocol):
    """Protocol for LLM clients."""

    def complete(self, prompt: str) -> str: ...
