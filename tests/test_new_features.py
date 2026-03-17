"""Tests for text2fraq new features: ModelRouter and FraqSession."""

from __future__ import annotations

import pytest

from fraq.text2fraq.router import ModelRouter
from fraq.text2fraq.session import FraqSession
from fraq.text2fraq.models import ParsedQuery


class TestModelRouter:
    """Test suite for ModelRouter."""

    def test_routes_simple_query_to_small_model(self):
        router = ModelRouter()
        model = router.route("find temperature")
        assert model == "ollama/qwen2.5:0.5b"

    def test_routes_complex_query_to_large_model(self):
        router = ModelRouter()
        model = router.route("generate complex schema with nested structures")
        assert model == "ollama/qwen2.5:7b"

    def test_routes_medium_query_to_medium_model(self):
        router = ModelRouter()
        model = router.route("search files with filters and sorting")
        assert model == "ollama/qwen2.5:3b"

    def test_estimate_complexity_short_text_low(self):
        router = ModelRouter()
        score = router._estimate_complexity("hi")
        assert score < 0.3

    def test_estimate_complexity_technical_terms_high(self):
        router = ModelRouter()
        score = router._estimate_complexity("generate advanced schema structure")
        assert score > 0.3

    def test_get_config_for_small_model(self):
        router = ModelRouter()
        config = router.get_config_for_model("ollama/qwen2.5:0.5b")
        assert config["max_tokens"] == 256
        assert config["timeout"] == 10

    def test_get_config_for_large_model(self):
        router = ModelRouter()
        config = router.get_config_for_model("ollama/qwen2.5:7b")
        assert config["max_tokens"] == 1024
        assert config["timeout"] == 60

    def test_custom_routes(self):
        custom = {"tiny": "ollama/phi3:mini", "huge": "ollama/llama3:70b"}
        router = ModelRouter()
        router.ROUTES = custom
        assert router.ROUTES["tiny"] == "ollama/phi3:mini"


class TestFraqSession:
    """Test suite for FraqSession."""

    def test_session_initializes_empty(self):
        session = FraqSession()
        assert len(session.history) == 0
        assert len(session.context) == 0

    def test_session_max_history_default(self):
        session = FraqSession()
        assert session.max_history == 10

    def test_detects_followup_with_and(self):
        session = FraqSession()
        assert session._is_followup("and show as csv") is True

    def test_detects_followup_with_now(self):
        session = FraqSession()
        assert session._is_followup("now as table") is True

    def test_detects_non_followup(self):
        session = FraqSession()
        assert session._is_followup("find pdf files") is False

    def test_detects_new_fields_in_followup(self):
        session = FraqSession()
        fields = session._detect_new_fields("add temperature and humidity")
        assert "temperature:float" in fields
        assert "humidity:float" in fields

    def test_clear_empties_history(self):
        session = FraqSession()
        # Manually add to history
        session.history.append(
            ParsedQuery(fields=["test"], depth=3, format="json")
        )
        session.clear()
        assert len(session.history) == 0

    def test_get_context_summary_returns_dict(self):
        session = FraqSession()
        summary = session.get_context_summary()
        assert "query_count" in summary
        assert "last_format" in summary

    def test_update_context_stores_format(self):
        session = FraqSession()
        parsed = ParsedQuery(fields=["x"], depth=3, format="csv")
        session._update_context(parsed)
        assert session.context["last_format"] == "csv"
