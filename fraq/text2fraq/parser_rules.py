"""Rule-based text parser without LLM (fallback for offline use)."""

from __future__ import annotations

import re
from typing import Any

from fraq.query import FraqExecutor
from fraq.core import FraqNode
from fraq.text2fraq.models import ParsedQuery


_LIMIT_PATTERN = re.compile(r"(\d+)\b(?:\W+\w+){0,5}?\W+(records?|rows?|items?|samples?)\b")


def _word_match(text: str, pattern: str) -> bool:
    return re.search(rf"\b{re.escape(pattern)}\b", text) is not None


def _detect_format(text: str, default: str = "json") -> str:
    if "csv" in text or "table" in text:
        return "csv"
    if "yaml" in text:
        return "yaml"
    if "stream" in text or "jsonl" in text:
        return "jsonl"
    return default


def _detect_depth(text: str, default: int = 3) -> int:
    if "deep" in text or "many" in text:
        return 5
    if "shallow" in text or "simple" in text:
        return 1
    return default


def _detect_limit(text: str) -> int | None:
    match = _LIMIT_PATTERN.search(text)
    return int(match.group(1)) if match else None


class Text2FraqSimple:
    """Rule-based text2fraq without LLM (fallback for offline use)."""

    FIELD_PATTERNS: dict[str, list[str]] = {
        "temperature:float": ["temperature", "temp"],
        "humidity:float": ["humidity", "moisture"],
        "pressure:float": ["pressure", "barometric"],
        "sensor_id:str": ["sensor", "id", "device"],
        "active:bool": ["active", "enabled", "on", "running"],
        "value:float": ["value", "reading", "measurement"],
        "timestamp:int": ["time", "timestamp", "date"],
        "x:float": ["x", "horizontal"],
        "y:float": ["y", "vertical"],
        "z:float": ["z", "depth"],
        "filename:str": ["file", "filename", "name"],
        "extension:str": ["extension", "type", "format"],
        "size:int": ["size", "bytes"],
        "mtime:float": ["modified", "mtime", "changed"],
        "path:str": ["path", "location", "directory"],
    }

    def parse(self, text: str) -> ParsedQuery:
        """Parse using rule-based matching."""
        text_lower = text.lower()
        return ParsedQuery(
            fields=self._detect_fields(text_lower),
            depth=_detect_depth(text_lower),
            format=_detect_format(text_lower),
            limit=_detect_limit(text_lower),
        )

    def _detect_fields(self, text: str) -> list[str]:
        fields = []
        for field, patterns in self.FIELD_PATTERNS.items():
            if any(self._matches_pattern(text, pattern) for pattern in patterns):
                fields.append(field)
        return fields or ["value:float"]

    @staticmethod
    def _matches_pattern(text: str, pattern: str) -> bool:
        return _word_match(text, pattern)

    def execute(
        self,
        text: str,
        root: FraqNode | None = None,
    ) -> str | list[dict[str, Any]]:
        """Parse and execute query."""
        parsed = self.parse(text)
        executor = FraqExecutor(root) if root else FraqExecutor(dims=parsed.dims)
        return executor.execute(parsed.to_fraq_query())
