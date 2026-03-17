"""Multi-model router for LLM query routing based on complexity."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelRouter:
    """Route queries to the best model based on complexity."""

    ROUTES: dict[str, str] = None

    def __post_init__(self):
        if self.ROUTES is None:
            self.ROUTES = {
                "simple_search": "ollama/qwen2.5:0.5b",   # fast, simple
                "complex_query": "ollama/qwen2.5:3b",       # balanced
                "schema_generation": "ollama/qwen2.5:7b",   # accurate
            }

    def route(self, text: str) -> str:
        """Select best model based on query complexity."""
        complexity = self._estimate_complexity(text)
        if complexity < 0.3:
            return self.ROUTES["simple_search"]
        elif complexity < 0.7:
            return self.ROUTES["complex_query"]
        return self.ROUTES["schema_generation"]

    def _estimate_complexity(self, text: str) -> float:
        """Estimate query complexity (0.0 - 1.0)."""
        score = 0.0
        text_lower = text.lower()

        # Length factor (longer = more complex)
        word_count = len(text.split())
        score += min(word_count / 20, 0.3)

        # Technical terms increase complexity
        technical_terms = [
            "schema", "generate", "create", "define", "structure",
            "complex", "advanced", "sophisticated", "detailed",
        ]
        for term in technical_terms:
            if term in text_lower:
                score += 0.1

        # Multiple conditions increase complexity
        condition_indicators = ["and", "or", "but", "where", "with"]
        for indicator in condition_indicators:
            if f" {indicator} " in text_lower:
                score += 0.05

        # File operations with filters
        if any(x in text_lower for x in ["pdf", "txt", "json", "csv"]):
            score += 0.1
        if any(x in text_lower for x in ["sort", "filter", "limit", "recent"]):
            score += 0.1

        return min(score, 1.0)

    def get_config_for_model(self, model: str) -> dict:
        """Get recommended config for model."""
        base_configs = {
            "ollama/qwen2.5:0.5b": {
                "temperature": 0.1,
                "max_tokens": 256,
                "timeout": 10,
            },
            "ollama/qwen2.5:3b": {
                "temperature": 0.1,
                "max_tokens": 512,
                "timeout": 30,
            },
            "ollama/qwen2.5:7b": {
                "temperature": 0.05,
                "max_tokens": 1024,
                "timeout": 60,
            },
        }
        return base_configs.get(model, {
            "temperature": 0.1,
            "max_tokens": 512,
            "timeout": 30,
        })
