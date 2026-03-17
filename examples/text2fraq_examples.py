#!/usr/bin/env python3
"""
text2fraq — Natural Language → Fractal Query examples.

Demonstruje parsowanie NL z użyciem małych modeli lokalnych przez LiteLLM + Ollama:
- Qwen2.5 3B ( Alibaba - szybki, dobry dla instrukcji)
- Llama 3.2 3B (Meta - zbalansowany)
- Phi-3 3.8B (Microsoft - mocny w reasoning)

Przed uruchomieniem:
  1. Zainstaluj Ollama: https://ollama.com
  2. Pobierz modele:
     ollama pull qwen2.5:3b
     ollama pull llama3.2:3b
     ollama pull phi3:3.8b
  3. Skopiuj .env.example → .env i dostosuj
"""

from __future__ import annotations

import os
from dataclasses import dataclass

# Load env before importing fraq
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from fraq import (
    Text2Fraq,
    Text2FraqSimple,
    Text2FraqConfig,
    FraqNode,
    FraqSchema,
    text2query,
    text2fraq,
)


# ═══════════════════════════════════════════════════════════════════════════
# 1. RULE-BASED PARSER (bez LLM — fallback)
# ═══════════════════════════════════════════════════════════════════════════

def example_simple_parser():
    """Text2FraqSimple — deterministyczny parser bez LLM."""
    print("=" * 60)
    print("1. RULE-BASED PARSER (Text2FraqSimple)")
    print("=" * 60)

    parser = Text2FraqSimple()

    queries = [
        "Show temperature and humidity readings",
        "Get 20 sensor samples in CSV format",
        "Stream pressure data as JSON",
        "Active sensors with high temperature",
    ]

    for q in queries:
        result = parser.parse(q)
        print(f"\n  NL: \"{q}\"")
        print(f"  → fields={result.fields}, depth={result.depth}, format={result.format}")
        if result.limit:
            print(f"  → limit={result.limit}")

    print()


# ═══════════════════════════════════════════════════════════════════════════
# 2. LLM PARSER — QWEN2.5 3B (Alibaba)
# ═══════════════════════════════════════════════════════════════════════════

def example_qwen25():
    """Qwen2.5 3B — szybki model zorientowany na instrukcje (CN/EN)."""
    print("=" * 60)
    print("2. LLM PARSER — Qwen2.5 3B (ollama)")
    print("=" * 60)

    config = Text2FraqConfig(
        provider="ollama",
        model="qwen2.5:3b",
        base_url="http://localhost:11434",
        temperature=0.1,
        max_tokens=512,
    )

    try:
        t2f = Text2Fraq(config)

        queries = [
            "Show temperature and humidity for last 10 records",
            "Get me 50 sensor readings in CSV format with depth 3",
            "Stream pressure data as JSONL",
            "Find active sensors where temperature is greater than 0.7",
        ]

        for q in queries:
            print(f"\n  NL: \"{q}\"")
            try:
                parsed = t2f.parse(q)
                print(f"  → fields={parsed.fields}")
                print(f"  → depth={parsed.depth}, format={parsed.format}, limit={parsed.limit}")
            except Exception as e:
                print(f"  → ERROR: {e}")

        # Execute one query
        print("\n  Executing: 'Show 5 temperature readings'")
        try:
            result = t2f.execute("Show 5 temperature readings")
            print(f"  → {str(result)[:200]}...")
        except Exception as e:
            print(f"  → ERROR: {e}")

    except ImportError:
        print("  LiteLLM not installed. Run: pip install litellm")
    except Exception as e:
        print(f"  Ollama error: {e}")
        print("  Make sure Ollama is running and model is pulled: ollama pull qwen2.5:3b")

    print()


# ═══════════════════════════════════════════════════════════════════════════
# 3. LLM PARSER — LLAMA 3.2 3B (Meta)
# ═══════════════════════════════════════════════════════════════════════════

def example_llama32():
    """Llama 3.2 3B — lekki, zbalansowany model multimedialny."""
    print("=" * 60)
    print("3. LLM PARSER — Llama 3.2 3B (ollama)")
    print("=" * 60)

    config = Text2FraqConfig(
        provider="ollama",
        model="llama3.2:3b",
        base_url="http://localhost:11434",
        temperature=0.1,
        max_tokens=512,
    )

    try:
        t2f = Text2Fraq(config)

        queries = [
            "Extract 15 IoT sensor records as YAML",
            "Give me deep analysis with depth 5 on temperature data",
            "Quick overview of humidity in JSON format",
        ]

        for q in queries:
            print(f"\n  NL: \"{q}\"")
            try:
                parsed = t2f.parse(q)
                print(f"  → depth={parsed.depth}, format={parsed.format}, limit={parsed.limit}")
            except Exception as e:
                print(f"  → ERROR: {e}")

    except ImportError:
        print("  LiteLLM not installed. Run: pip install litellm")
    except Exception as e:
        print(f"  Ollama error: {e}")
        print("  Make sure Ollama is running and model is pulled: ollama pull llama3.2:3b")

    print()


# ═══════════════════════════════════════════════════════════════════════════
# 4. LLM PARSER — PHI-3 3.8B (Microsoft)
# ═══════════════════════════════════════════════════════════════════════════

def example_phi3():
    """Phi-3 3.8B — mocny w reasoning, lepszy w złożone logikę."""
    print("=" * 60)
    print("4. LLM PARSER — Phi-3 3.8B (ollama)")
    print("=" * 60)

    config = Text2FraqConfig(
        provider="ollama",
        model="phi3:3.8b",
        base_url="http://localhost:11434",
        temperature=0.1,
        max_tokens=512,
    )

    try:
        t2f = Text2Fraq(config)

        # Complex reasoning queries
        queries = [
            "If temperature > 0.8 and humidity < 40%, show alert status",
            "Generate 100 samples for machine learning training",
            "Create a CSV table with sensor_id, temperature, and active flag for 25 devices",
        ]

        for q in queries:
            print(f"\n  NL: \"{q}\"")
            try:
                parsed = t2f.parse(q)
                print(f"  → fields={parsed.fields}")
                print(f"  → depth={parsed.depth}, format={parsed.format}, limit={parsed.limit}")
            except Exception as e:
                print(f"  → ERROR: {e}")

    except ImportError:
        print("  LiteLLM not installed. Run: pip install litellm")
    except Exception as e:
        print(f"  Ollama error: {e}")
        print("  Make sure Ollama is running and model is pulled: ollama pull phi3:3.8b")

    print()


# ═══════════════════════════════════════════════════════════════════════════
# 5. CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def example_convenience_functions():
    """text2query() i text2fraq() — szybkie funkcje one-liner."""
    print("=" * 60)
    print("5. CONVENIENCE FUNCTIONS")
    print("=" * 60)

    # Bez LLM (fallback)
    print("\n  Using text2query() [rule-based fallback]:")
    parsed = text2query("Show temperature in CSV format")
    print(f"  → Parsed: fields={parsed.fields}, format={parsed.format}")

    print("\n  Using text2fraq() [with execution]:")
    try:
        result = text2fraq("Get 3 temperature readings as JSON")
        print(f"  → Result: {str(result)[:150]}...")
    except Exception as e:
        print(f"  → Fallback to simple parser: {e}")
        # Use simple parser result
        parsed = text2query("Get 3 temperature readings as JSON")
        print(f"  → Parsed (no LLM): {parsed}")

    print()


# ═══════════════════════════════════════════════════════════════════════════
# 6. ENV CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

def example_env_config():
    """Ładowanie konfiguracji z .env."""
    print("=" * 60)
    print("6. ENVIRONMENT CONFIGURATION")
    print("=" * 60)

    print("\n  Current .env settings:")
    config = Text2FraqConfig.from_env()
    print(f"  → Provider: {config.provider}")
    print(f"  → Model: {config.model}")
    print(f"  → Base URL: {config.base_url}")
    print(f"  → Temperature: {config.temperature}")
    print(f"  → Default format: {config.default_format}")
    print(f"  → Default dims: {config.default_dims}")
    print(f"  → Default depth: {config.default_depth}")

    print("\n  To change settings, edit .env file or set environment variables:")
    print("    export LITELLM_MODEL=llama3.2:3b")
    print("    export LITELLM_TEMPERATURE=0.5")
    print()


# ═══════════════════════════════════════════════════════════════════════════
# 7. BENCHMARK / COMPARISON
# ═══════════════════════════════════════════════════════════════════════════

def example_benchmark():
    """Porównanie wszystkich parserów na tych samych zapytaniach."""
    print("=" * 60)
    print("7. PARSER COMPARISON (same queries, different methods)")
    print("=" * 60)

    test_queries = [
        "Show temperature readings",
        "Get 20 samples in CSV",
        "Stream humidity data as JSONL",
    ]

    print("\n  RULE-BASED (Text2FraqSimple):")
    simple = Text2FraqSimple()
    for q in test_queries:
        parsed = simple.parse(q)
        print(f"    '{q[:30]}...' → fmt={parsed.format}, limit={parsed.limit}, depth={parsed.depth}")

    print("\n  LLM-based requires Ollama running. Comparison template:")
    print("    Query                    | Simple    | Qwen2.5 | Llama3.2 | Phi-3")
    print("    -------------------------|-----------|---------|----------|-------")
    print("    'Show temperature'       | json/None | ?       | ?        | ?")
    print("    'Get 20 samples CSV'     | csv/20    | ?       | ?        | ?")
    print()


# ═══════════════════════════════════════════════════════════════════════════
# 8. CUSTOM SCHEMA INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════

def example_custom_schema():
    """Text2Fraq z custom FraqSchema (ERP, IoT, etc.)."""
    print("=" * 60)
    print("8. CUSTOM SCHEMA INTEGRATION")
    print("=" * 60)

    # ERP schema
    root = FraqNode(position=(0.0, 0.0, 0.0, 0.0), seed=42)
    schema = FraqSchema(root=root)
    schema.add_field("invoice_id", "str")
    schema.add_field("amount", "float")
    schema.add_field("client_id", "str")
    schema.add_field("paid", "bool")

    print("\n  ERP Schema fields: invoice_id, amount, client_id, paid")

    # Simple parser na ERP query
    parser = Text2FraqSimple()

    erp_queries = [
        "Show all unpaid invoices with amount > 1000",
        "Get 10 client records in CSV",
        "List paid invoices as JSON",
    ]

    print("\n  Parsing ERP queries:")
    for q in erp_queries:
        parsed = parser.parse(q)
        print(f"    '{q[:40]}...' → {parsed.fields}")

    print()


# ═══════════════════════════════════════════════════════════════════════════
# RUN ALL
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    example_simple_parser()
    example_qwen25()
    example_llama32()
    example_phi3()
    example_convenience_functions()
    example_env_config()
    example_benchmark()
    example_custom_schema()

    print("=" * 60)
    print("Setup instructions:")
    print("=" * 60)
    print("""
1. Install Ollama:     https://ollama.com/download
2. Pull models:
   ollama pull qwen2.5:3b
   ollama pull llama3.2:3b
   ollama pull phi3:3.8b

3. Copy .env.example to .env and adjust:
   cp .env.example .env

4. Install with AI extras:
   pip install -e ".[ai]"

5. Run specific model example by setting in .env:
   LITELLM_MODEL=qwen2.5:3b
   # or
   LITELLM_MODEL=llama3.2:3b
   # or
   LITELLM_MODEL=phi3:3.8b
""")
