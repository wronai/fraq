"""LLM-based text parser for natural language queries."""

from __future__ import annotations

import json
import re
from typing import Any

from fraq.query import FraqExecutor
from fraq.core import FraqNode
from fraq.text2fraq.config import Text2FraqConfig
from fraq.text2fraq.models import ParsedQuery, LLMClient
from fraq.text2fraq.llm_client import LiteLLMClient
from fraq.text2fraq.parser_rules import Text2FraqSimple, _detect_depth, _detect_format, _detect_limit, _word_match


class Text2Fraq:
    """Natural language to fractal query converter (LLM-based)."""

    SYSTEM_PROMPT = """You are a text2fraq parser. Convert natural language to JSON query parameters.

Rules:
1. Extract fields mentioned (temperature, humidity, pressure, sensor_id, active, etc.)
2. Infer data types: float for measurements, str for IDs, bool for flags
3. Determine depth (complexity): simple=1, normal=2-3, complex=5+
4. Detect format from context: "CSV" → csv, "table" → csv, "list" → json, "stream" → jsonl
5. Extract filters: "temperature > 25" → {"temperature": {"gt": 25}}
6. Always return valid JSON

Output format:
{
  "fields": ["temperature:float", "humidity:float", "sensor_id:str"],
  "depth": 3,
  "format": "json",
  "filters": {"temperature": {"gt": 0.5}},
  "dims": 3,
  "limit": 10
}
"""

    def __init__(
        self,
        config: Text2FraqConfig | None = None,
        client: LLMClient | None = None,
    ):
        self.config = config or Text2FraqConfig.from_env()
        self.client = client or LiteLLMClient(self.config)

    def parse(self, text: str) -> ParsedQuery:
        """Parse natural language text to structured query."""
        prompt = f"{self.SYSTEM_PROMPT}\n\nUser query: {text}\n\nJSON output:"
        response = self.client.complete(prompt)
        return self._parse_response(response)

    def _parse_response(self, response: str) -> ParsedQuery:
        """Parse LLM response to ParsedQuery."""
        data = self._extract_structured_response(response)
        direction = data.get("direction")
        parsed_direction = (
            tuple(float(value) for value in direction)
            if isinstance(direction, list)
            else None
        )
        return ParsedQuery(
            fields=data.get("fields", ["value:float"]),
            depth=data.get("depth", self.config.default_depth),
            format=data.get("format", self.config.default_format),
            filters=data.get("filters", {}),
            dims=data.get("dims", self.config.default_dims),
            direction=parsed_direction,
            limit=data.get("limit"),
        )

    def _extract_structured_response(self, response: str) -> dict[str, Any]:
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        return self._fallback_parse(response)

    def _fallback_parse(self, text: str) -> dict[str, Any]:
        """Fallback parsing when JSON extraction fails."""
        text_lower = text.lower()
        return {
            "fields": self._fallback_fields(text_lower),
            "depth": _detect_depth(text_lower, self.config.default_depth),
            "format": _detect_format(text_lower, self.config.default_format),
            "filters": {},
            "limit": _detect_limit(text_lower),
        }

    def _fallback_fields(self, text: str) -> list[str]:
        detected = []
        for field, patterns in Text2FraqSimple.FIELD_PATTERNS.items():
            if any(_word_match(text, pattern) for pattern in patterns):
                detected.append(field)
        return detected or ["value:float"]

    def execute(
        self,
        text: str,
        root: FraqNode | None = None,
    ) -> str | list[dict[str, Any]]:
        """Parse text and execute query immediately."""
        parsed = self.parse(text)
        executor = FraqExecutor(root) if root else FraqExecutor(dims=parsed.dims)
        return executor.execute(parsed.to_fraq_query())
