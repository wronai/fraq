"""LLM client implementations."""

from __future__ import annotations

try:
    import litellm
    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False

from fraq.text2fraq.config import Text2FraqConfig
from fraq.text2fraq.models import LLMClient


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
