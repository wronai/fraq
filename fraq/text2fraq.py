"""
text2fraq — Natural Language → Fractal Query transformation.

Uses LiteLLM to support multiple LLM providers (Ollama, OpenAI, Anthropic, etc.)
Optimized for small models (qwen2.5:3b, llama3.2:3b, phi3:3.8b) via local Ollama.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Any, Protocol

try:
    import litellm

    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from fraq.adapters import FileSearchAdapter
from fraq.core import FraqNode
from fraq.formats import FormatRegistry
from fraq.query import FraqExecutor, FraqQuery

_LIMIT_PATTERN = re.compile(r"(\d+)\b(?:\W+\w+){0,5}?\W+(records?|rows?|items?|samples?)\b")
_FILE_LIMIT_PATTERN = re.compile(r"(\d+)\s*(files?|documents?|items?)?")


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


@dataclass
class Text2FraqConfig:
    """Configuration for text2fraq."""

    provider: str = "ollama"
    model: str = "qwen2.5:3b"
    api_key: str = ""
    base_url: str = "http://localhost:11434"
    temperature: float = 0.1
    max_tokens: int = 512
    timeout: int = 30
    default_format: str = "json"
    default_dims: int = 3
    default_depth: int = 3

    @classmethod
    def from_env(cls) -> "Text2FraqConfig":
        """Load config from environment variables."""
        return cls(
            provider=os.getenv("LITELLM_PROVIDER", "ollama"),
            model=os.getenv("LITELLM_MODEL", "qwen2.5:3b"),
            api_key=os.getenv("LITELLM_API_KEY", ""),
            base_url=os.getenv("LITELLM_BASE_URL", "http://localhost:11434"),
            temperature=float(os.getenv("LITELLM_TEMPERATURE", "0.1")),
            max_tokens=int(os.getenv("LITELLM_MAX_TOKENS", "512")),
            timeout=int(os.getenv("LITELLM_TIMEOUT", "30")),
            default_format=os.getenv("TEXT2FRAQ_DEFAULT_FORMAT", "json"),
            default_dims=int(os.getenv("TEXT2FRAQ_DEFAULT_DIMS", "3")),
            default_depth=int(os.getenv("TEXT2FRAQ_DEFAULT_DEPTH", "3")),
        )


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


class LiteLLMClient:
    """LiteLLM client for text completion."""

    def __init__(self, config: Text2FraqConfig | None = None):
        if not HAS_LITELLM:
            raise ImportError("litellm is required. Install: pip install litellm")
        self.config = config or Text2FraqConfig.from_env()
        litellm.api_base = self.config.base_url
        if self.config.api_key:
            litellm.api_key = self.config.api_key

    def complete(self, prompt: str) -> str:
        """Send prompt to LLM and return completion."""
        response = litellm.completion(
            model=f"{self.config.provider}/{self.config.model}",
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            timeout=self.config.timeout,
        )
        return response.choices[0].message.content


class FileSearchText2Fraq:
    """
    Natural language to file search converter.

    Converts queries like "list 10 PDF files created recently" to file searches.
    Works with Text2Fraq for combined queries.

    Examples:
        >>> fs = FileSearchText2Fraq("/home/user/documents")
        >>> results = fs.search("show me 10 pdf files created last week")
        >>> results = fs.search("list all txt files in current directory")
    """

    FILE_PATTERNS: dict[str, list[str]] = {
        "pdf": ["pdf", "acpdf", "portable document"],
        "txt": ["txt", "text", "plain text"],
        "csv": ["csv", "comma separated"],
        "json": ["json", "javascript object"],
        "yaml": ["yaml", "yml"],
        "docx": ["docx", "word", "microsoft word"],
        "xlsx": ["xlsx", "excel", "spreadsheet"],
        "py": ["py", "python", "python script"],
        "js": ["js", "javascript"],
        "ts": ["ts", "typescript"],
        "html": ["html", "htm", "web page"],
        "xml": ["xml"],
        "zip": ["zip", "archive"],
        "png": ["png", "image", "picture"],
        "jpg": ["jpg", "jpeg", "image", "picture"],
        "md": ["md", "markdown", "documentation"],
    }

    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.adapter = FileSearchAdapter(base_path=base_path, recursive=True)

    def parse(self, text: str) -> dict[str, Any]:
        """Parse natural language file query to search parameters."""
        text_lower = text.lower()
        return {
            "extension": self._detect_extension(text_lower),
            "limit": self._detect_limit(text_lower),
            "newer_than": self._detect_newer_than(text_lower),
            "sort_by": self._detect_sort_by(text_lower),
        }

    def _detect_extension(self, text: str) -> str | None:
        for extension, patterns in self.FILE_PATTERNS.items():
            if any(pattern in text for pattern in patterns):
                return extension
        return None

    def _detect_limit(self, text: str) -> int:
        match = _FILE_LIMIT_PATTERN.search(text)
        return int(match.group(1)) if match else 10

    def _detect_newer_than(self, text: str) -> float | None:
        if "today" in text or "recent" in text:
            return (datetime.now() - timedelta(days=1)).timestamp()
        if "week" in text or "last week" in text:
            return (datetime.now() - timedelta(days=7)).timestamp()
        if "month" in text:
            return (datetime.now() - timedelta(days=30)).timestamp()
        return None

    def _detect_sort_by(self, text: str) -> str:
        if "name" in text or "alphabetical" in text:
            return "name"
        if "size" in text or "largest" in text:
            return "size"
        return "mtime"

    def search(self, text: str) -> list[dict[str, Any]]:
        """Parse query and execute file search."""
        return self.adapter.search(**self.parse(text))

    def format_results(
        self,
        results: list[dict[str, Any]],
        fmt: str = "json",
        fields: list[str] | None = None,
    ) -> str:
        """Format file search results to specified format."""
        if fields:
            results = [{key: record.get(key) for key in fields if key in record} for record in results]
        return FormatRegistry.serialize(fmt, results)


class Text2Fraq:
    """
    Natural language to fractal query converter.

    Examples:
        >>> t2f = Text2Fraq()  # Uses env config
        >>> query = t2f.parse("Show temperature readings for last 10 days")
        >>> result = t2f.execute("Show active sensors with humidity > 60%")
    """

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


class Text2FraqSimple:
    """
    Rule-based text2fraq without LLM (fallback for offline use).

    Useful when LLM is unavailable or for deterministic parsing.
    """

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


def text2filesearch(
    text: str,
    base_path: str = ".",
    fmt: str = "json",
) -> str | list[dict[str, Any]]:
    """
    One-liner to search files via natural language.

    Examples:
        >>> text2filesearch("list 10 pdf files")
        >>> text2filesearch("show recent txt files in /home/user", "/home/user", "csv")
    """
    searcher = FileSearchText2Fraq(base_path)
    results = searcher.search(text)
    if fmt == "records":
        return results
    return searcher.format_results(results, fmt)


def text2query(text: str, config: Text2FraqConfig | None = None) -> ParsedQuery:
    """Convert text to ParsedQuery."""
    parser = Text2Fraq(config) if HAS_LITELLM else Text2FraqSimple()
    return parser.parse(text)


def text2fraq(
    text: str,
    config: Text2FraqConfig | None = None,
    root: FraqNode | None = None,
) -> str | list[dict[str, Any]]:
    """Convert text and execute query."""
    parser = Text2Fraq(config) if HAS_LITELLM else Text2FraqSimple()
    return parser.execute(text, root)
