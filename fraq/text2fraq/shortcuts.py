"""Convenience functions for text2fraq."""

from __future__ import annotations

from typing import Any, Optional

from fraq.core import FraqNode
from fraq.text2fraq.config import Text2FraqConfig
from fraq.text2fraq.models import ParsedQuery
from fraq.text2fraq.parser_llm import Text2Fraq
from fraq.text2fraq.parser_rules import Text2FraqSimple
from fraq.text2fraq.file_search_parser import FileSearchText2Fraq

try:
    import litellm
    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False


def text2filesearch(
    text: str,
    base_path: str = ".",
    fmt: str = "json",
) -> str | list[dict[str, Any]]:
    """One-liner to search files via natural language."""
    searcher = FileSearchText2Fraq(base_path)
    results = searcher.search(text)
    if fmt == "records":
        return results
    return searcher.format_results(results, fmt)


def text2query(text: str, config: Optional[Text2FraqConfig] = None) -> ParsedQuery:
    """Convert text to ParsedQuery."""
    parser = Text2Fraq(config) if HAS_LITELLM else Text2FraqSimple()
    return parser.parse(text)


def text2fraq(
    text: str,
    config: Optional[Text2FraqConfig] = None,
    root: Optional[FraqNode] = None,
) -> str | list[dict[str, Any]]:
    """Convert text and execute query."""
    parser = Text2Fraq(config) if HAS_LITELLM else Text2FraqSimple()
    return parser.execute(text, root)
