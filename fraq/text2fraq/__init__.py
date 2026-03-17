"""fraq text2fraq package - natural language to fractal query transformation.

Simplified architecture: Direct LiteLLM usage without custom routing.
LiteLLM handles model routing internally.
"""

from __future__ import annotations

from fraq.text2fraq.config import Text2FraqConfig
from fraq.text2fraq.models import ParsedQuery, LLMClient
from fraq.text2fraq.llm_client import LiteLLMClient, HAS_LITELLM
from fraq.text2fraq.parser_rules import Text2FraqSimple
from fraq.text2fraq.parser_llm import Text2Fraq
from fraq.text2fraq.file_search_parser import FileSearchText2Fraq
from fraq.text2fraq.shortcuts import text2fraq, text2query, text2filesearch
from fraq.text2fraq.session import FraqSession

__all__ = [
    "Text2FraqConfig",
    "ParsedQuery",
    "LLMClient",
    "LiteLLMClient",
    "HAS_LITELLM",
    "Text2FraqSimple",
    "Text2Fraq",
    "FileSearchText2Fraq",
    "text2fraq",
    "text2query",
    "text2filesearch",
    "FraqSession",
]
