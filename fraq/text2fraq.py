"""
text2fraq — Natural Language → Fractal Query transformation.

Uses LiteLLM to support multiple LLM providers (Ollama, OpenAI, Anthropic, etc.)
Optimized for small models (qwen2.5:3b, llama3.2:3b, phi3:3.8b) via local Ollama.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any, Protocol

# Lazy import litellm to avoid hard dependency
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

from fraq.core import FraqNode
from fraq.query import FraqExecutor, FraqQuery
from fraq.adapters import FileSearchAdapter


# ... (existing code remains)


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

        # Detect file extension
        extension = None
        for ext, patterns in self.FILE_PATTERNS.items():
            if any(p in text_lower for p in patterns):
                extension = ext
                break

        # Detect limit (number of files)
        limit = 10  # default
        num_match = re.search(r'(\d+)\s*(files?|documents?|items?)?', text_lower)
        if num_match:
            limit = int(num_match.group(1))

        # Detect time constraints
        newer_than = None
        if "today" in text_lower or "recent" in text_lower:
            from datetime import datetime, timedelta
            newer_than = (datetime.now() - timedelta(days=1)).timestamp()
        elif "week" in text_lower or "last week" in text_lower:
            from datetime import datetime, timedelta
            newer_than = (datetime.now() - timedelta(days=7)).timestamp()
        elif "month" in text_lower:
            from datetime import datetime, timedelta
            newer_than = (datetime.now() - timedelta(days=30)).timestamp()

        # Detect sort order
        sort_by = "mtime"  # default to recent
        if "name" in text_lower or "alphabetical" in text_lower:
            sort_by = "name"
        elif "size" in text_lower or "largest" in text_lower:
            sort_by = "size"
        elif "recent" in text_lower or "latest" in text_lower or "newest" in text_lower:
            sort_by = "mtime"

        return {
            "extension": extension,
            "limit": limit,
            "newer_than": newer_than,
            "sort_by": sort_by,
        }

    def search(self, text: str) -> list[dict[str, Any]]:
        """Parse query and execute file search."""
        params = self.parse(text)
        return self.adapter.search(**params)

    def format_results(
        self,
        results: list[dict[str, Any]],
        fmt: str = "json",
        fields: list[str] | None = None,
    ) -> str:
        """Format file search results to specified format."""
        from fraq.formats import FormatRegistry

        if fields:
            # Filter to requested fields
            filtered = []
            for r in results:
                filtered.append({k: r.get(k) for k in fields if k in r})
            results = filtered

        return FormatRegistry.serialize(fmt, results)


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


# Update Text2FraqSimple to handle file queries
class Text2FraqSimple:
    """
    Rule-based text2fraq without LLM (fallback for offline use).

    Useful when LLM is unavailable or for deterministic parsing.
    Now includes file search capabilities.
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
        # File fields
        "filename:str": ["file", "filename", "name"],
        "extension:str": ["extension", "type", "format"],
        "size:int": ["size", "bytes"],
        "mtime:float": ["modified", "mtime", "changed"],
        "path:str": ["path", "location", "directory"],
    }


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
    def from_env(cls) -> Text2FraqConfig:
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
        q = FraqQuery()
        if self.direction:
            q = q.zoom(self.depth, direction=self.direction)
        else:
            q = q.zoom(self.depth)
        q = q.select(*self.fields).output(self.format)
        for field_name, predicate in self.filters.items():
            if isinstance(predicate, dict):
                for op, value in predicate.items():
                    q = q.where(field_name, op, value)
            else:
                q = q.where(field_name, "eq", predicate)
        if self.limit:
            q = q.take(self.limit)
        return q


class LLMClient(Protocol):
    """Protocol for LLM clients."""
    def complete(self, prompt: str) -> str: ...


class LiteLLMClient:
    """LiteLLM client for text completion."""

    def __init__(self, config: Text2FraqConfig | None = None):
        if not HAS_LITELLM:
            raise ImportError("litellm is required. Install: pip install litellm")
        self.config = config or Text2FraqConfig.from_env()
        # Configure litellm
        litellm.api_base = self.config.base_url
        if self.config.api_key:
            litellm.api_key = self.config.api_key

    def complete(self, prompt: str) -> str:
        """Send prompt to LLM and return completion."""
        messages = [{"role": "user", "content": prompt}]
        response = litellm.completion(
            model=f"{self.config.provider}/{self.config.model}",
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            timeout=self.config.timeout,
        )
        return response.choices[0].message.content


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
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
            except json.JSONDecodeError:
                data = self._fallback_parse(response)
        else:
            data = self._fallback_parse(response)

        direction = data.get("direction")
        if isinstance(direction, list):
            direction = tuple(float(value) for value in direction)
        else:
            direction = None

        return ParsedQuery(
            fields=data.get("fields", ["value:float"]),
            depth=data.get("depth", self.config.default_depth),
            format=data.get("format", self.config.default_format),
            filters=data.get("filters", {}),
            dims=data.get("dims", self.config.default_dims),
            direction=direction,
            limit=data.get("limit"),
        )

    def _fallback_parse(self, text: str) -> dict[str, Any]:
        """Fallback parsing when JSON extraction fails."""
        # Simple regex-based extraction
        fields = []
        if "temperature" in text.lower():
            fields.append("temperature:float")
        if "humidity" in text.lower():
            fields.append("humidity:float")
        if "pressure" in text.lower():
            fields.append("pressure:float")
        if "sensor" in text.lower() or "id" in text.lower():
            fields.append("sensor_id:str")
        if "active" in text.lower():
            fields.append("active:bool")

        if not fields:
            fields = ["value:float"]

        # Detect format
        fmt = "json"
        if "csv" in text.lower() or "table" in text.lower():
            fmt = "csv"
        elif "yaml" in text.lower():
            fmt = "yaml"
        elif "stream" in text.lower() or "jsonl" in text.lower():
            fmt = "jsonl"

        # Detect depth from keywords
        depth = self.config.default_depth
        if "deep" in text.lower() or "many" in text.lower():
            depth = 5
        elif "simple" in text.lower() or "shallow" in text.lower():
            depth = 1

        # Detect limit
        limit = None
        num_match = re.search(r'(\d+)\s*(records?|rows?|items?|samples?)', text.lower())
        if num_match:
            limit = int(num_match.group(1))

        return {
            "fields": fields,
            "depth": depth,
            "format": fmt,
            "filters": {},
            "limit": limit,
        }

    def execute(
        self,
        text: str,
        root: FraqNode | None = None,
    ) -> str | list[dict[str, Any]]:
        """Parse text and execute query immediately."""
        parsed = self.parse(text)
        query = parsed.to_fraq_query()
        executor = FraqExecutor(dims=parsed.dims)
        if root:
            executor = FraqExecutor(root)
        return executor.execute(query)


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
    }

    def parse(self, text: str) -> ParsedQuery:
        """Parse using rule-based matching."""
        text_lower = text.lower()

        # Extract fields
        fields = []
        for field, patterns in self.FIELD_PATTERNS.items():
            if any(self._matches_pattern(text_lower, p) for p in patterns):
                fields.append(field)

        if not fields:
            fields = ["value:float"]

        # Detect format
        fmt = "json"
        if "csv" in text_lower or "table" in text_lower:
            fmt = "csv"
        elif "yaml" in text_lower:
            fmt = "yaml"
        elif "stream" in text_lower or "jsonl" in text_lower:
            fmt = "jsonl"

        # Detect depth
        depth = 3
        if "deep" in text_lower or "many" in text_lower:
            depth = 5
        elif "shallow" in text_lower or "simple" in text_lower:
            depth = 1

        # Detect limit
        limit = None
        num_match = re.search(r'(\d+)\b(?:\W+\w+){0,5}?\W+(records?|rows?|items?|samples?)\b', text_lower)
        if num_match:
            limit = int(num_match.group(1))

        return ParsedQuery(
            fields=fields,
            depth=depth,
            format=fmt,
            limit=limit,
        )

    @staticmethod
    def _matches_pattern(text: str, pattern: str) -> bool:
        if len(pattern) == 1:
            return re.search(rf"\b{re.escape(pattern)}\b", text) is not None
        return re.search(rf"\b{re.escape(pattern)}\b", text) is not None

    def execute(
        self,
        text: str,
        root: FraqNode | None = None,
    ) -> str | list[dict[str, Any]]:
        """Parse and execute query."""
        parsed = self.parse(text)
        query = parsed.to_fraq_query()
        executor = FraqExecutor(dims=parsed.dims)
        if root:
            executor = FraqExecutor(root)
        return executor.execute(query)


# Convenience functions
def text2query(text: str, config: Text2FraqConfig | None = None) -> ParsedQuery:
    """Convert text to ParsedQuery."""
    if not HAS_LITELLM:
        parser = Text2FraqSimple()
    else:
        parser = Text2Fraq(config)
    return parser.parse(text)


def text2fraq(
    text: str,
    config: Text2FraqConfig | None = None,
    root: FraqNode | None = None,
) -> str | list[dict[str, Any]]:
    """Convert text and execute query."""
    if not HAS_LITELLM:
        parser = Text2FraqSimple()
    else:
        parser = Text2Fraq(config)
    return parser.execute(text, root)
