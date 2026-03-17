"""Multi-turn conversation session with context memory."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, List, Optional

from fraq.text2fraq.models import ParsedQuery
from fraq.text2fraq.parser_llm import Text2Fraq
from fraq.text2fraq.config import Text2FraqConfig


@dataclass
class FraqSession:
    """Multi-turn conversation with context memory."""

    history: List[ParsedQuery] = field(default_factory=list)
    context: dict = field(default_factory=dict)
    parser: Text2Fraq = field(default=None)
    max_history: int = 10

    def __post_init__(self):
        if self.parser is None:
            self.parser = Text2Fraq(Text2FraqConfig.from_env())

    def ask(self, text: str) -> Any:
        """Process query with context awareness."""
        # Check if this is a follow-up query
        if self._is_followup(text) and self.history:
            parsed = self._modify_last(text)
        else:
            parsed = self.parser.parse(text)

        # Store in history
        self.history.append(parsed)
        if len(self.history) > self.max_history:
            self.history.pop(0)

        # Update context
        self._update_context(parsed)

        # Execute and return
        return self.parser.execute(text)

    def _is_followup(self, text: str) -> bool:
        """Detect if query is a follow-up to previous."""
        followup_indicators = [
            r"\band\s+",
            r"\bbut\s+",
            r"\bnow\s+",
            r"\bthen\s+",
            r"\balso\s+",
            r"^now\s",
            r"^then\s",
            r"^add\s",
            r"^change\s",
            r"^switch\s",
            r"instead",
            r"as\s+(?:csv|json|yaml|table)",
            r"in\s+(?:csv|json|yaml|table)",
        ]
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in followup_indicators)

    def _modify_last(self, text: str) -> ParsedQuery:
        """Modify last query based on follow-up."""
        last = self.history[-1]
        text_lower = text.lower()

        # Change format
        format_match = re.search(r"(?:as|in|to)\s+(csv|json|yaml|table)", text_lower)
        if format_match:
            new_format = format_match.group(1)
            return ParsedQuery(
                fields=last.fields,
                depth=last.depth,
                format=new_format,
                filters=last.filters,
                dims=last.dims,
                direction=last.direction,
                limit=last.limit,
            )

        # Change limit
        limit_match = re.search(r"(\d+)\s+(?:more|additional|extra)", text_lower)
        if limit_match and last.limit:
            new_limit = last.limit + int(limit_match.group(1))
            return ParsedQuery(
                fields=last.fields,
                depth=last.depth,
                format=last.format,
                filters=last.filters,
                dims=last.dims,
                direction=last.direction,
                limit=new_limit,
            )

        # Add fields
        new_fields = self._detect_new_fields(text_lower)
        if new_fields:
            combined_fields = list(last.fields) + new_fields
            return ParsedQuery(
                fields=combined_fields,
                depth=last.depth,
                format=last.format,
                filters=last.filters,
                dims=last.dims,
                direction=last.direction,
                limit=last.limit,
            )

        # Default: return last query
        return last

    def _detect_new_fields(self, text: str) -> List[str]:
        """Detect new fields mentioned in follow-up."""
        from fraq.text2fraq.parser_rules import Text2FraqSimple

        new_fields = []
        for field, patterns in Text2FraqSimple.FIELD_PATTERNS.items():
            for pattern in patterns:
                if f" {pattern} " in text or f" {pattern}" in text:
                    if field not in new_fields:
                        new_fields.append(field)
                    break
        return new_fields

    def _update_context(self, parsed: ParsedQuery) -> None:
        """Update session context with parsed query info."""
        self.context["last_format"] = parsed.format
        self.context["last_fields"] = parsed.fields
        self.context["last_depth"] = parsed.depth
        if parsed.limit:
            self.context["last_limit"] = parsed.limit

    def get_context_summary(self) -> dict:
        """Get summary of current session context."""
        return {
            "query_count": len(self.history),
            "last_format": self.context.get("last_format", "json"),
            "last_fields": self.context.get("last_fields", []),
            "last_depth": self.context.get("last_depth", 3),
        }

    def clear(self) -> None:
        """Clear session history and context."""
        self.history.clear()
        self.context.clear()
