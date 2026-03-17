"""Configuration for text2fraq."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


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
