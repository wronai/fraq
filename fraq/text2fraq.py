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

from fraq import FraqQuery, FraqExecutor, FraqNode


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
        q = q.zoom(self.depth)
        if self.direction:
            q = q.zoom(self.depth, direction=self.direction)
        q = q.select(*self.fields).output(self.format)
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

        return ParsedQuery(
            fields=data.get("fields", ["value:float"]),
            depth=data.get("depth", self.config.default_depth),
            format=data.get("format", self.config.default_format),
            filters=data.get("filters", {}),
            dims=data.get("dims", self.config.default_dims),
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
            if any(p in text_lower for p in patterns):
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
        import re
        num_match = re.search(r'(\d+)\s*(records?|rows?|items?|samples?)', text_lower)
        if num_match:
            limit = int(num_match.group(1))

        return ParsedQuery(
            fields=fields,
            depth=depth,
            format=fmt,
            limit=limit,
        )

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
