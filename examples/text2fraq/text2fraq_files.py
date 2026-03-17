#!/usr/bin/env python3
"""
text2fraq — Wyszukiwanie plików przez LLM (qwen2.5)

Przykład: "Podaj listę 10 plików pdf, które zostały ostatnio utworzone"
→ LLM parsuje zapytanie → FileSearchAdapter wyszukuje pliki

Wymaga: ollama z modelem qwen2.5:3b (lub qwen2.5-coder:3b)
"""

from __future__ import annotations

import os
import sys
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from fraq import (
    Text2Fraq,
    Text2FraqConfig,
    FileSearchText2Fraq,
    text2filesearch,
    FileSearchAdapter,
)


def example_pdf_search_rule_based():
    """Wyszukiwanie PDF bez LLM - rule based."""
    print("=" * 60)
    print("1. WYSZUKIWANIE PDF - RULE BASED (bez LLM)")
    print("=" * 60)

    # Szukaj w katalogu domowym lub bieżącym
    base_path = os.path.expanduser("~/github/wronai/fraq")
    if not os.path.exists(base_path):
        base_path = "."

    searcher = FileSearchText2Fraq(base_path)

    # Różne zapytania naturalne
    queries = [
        "list 10 pdf files",
        "show recent python files",
        "find 5 markdown files",
        "show txt files from last week",
    ]

    for q in queries:
        print(f"\n  Query: \"{q}\"")
        parsed = searcher.parse(q)
        print(f"  → extension={parsed['extension']}, limit={parsed['limit']}, sort_by={parsed['sort_by']}")

        # Wykonaj wyszukiwanie
        results = searcher.search(q)
        print(f"  → Znaleziono {len(results)} plików:")
        for r in results[:3]:
            print(f"     - {r['filename']} ({r['size']} bytes)")
        if len(results) > 3:
            print(f"     ... i {len(results) - 3} więcej")

    print()


def example_pdf_search_with_llm():
    """Wyszukiwanie PDF z użyciem LLM (qwen2.5)."""
    print("=" * 60)
    print("2. WYSZUKIWANIE PDF Z LLM (qwen2.5:3b)")
    print("=" * 60)

    base_path = os.path.expanduser("~/github/wronai/fraq")
    if not os.path.exists(base_path):
        base_path = "."

    # Konfiguracja LLM
    config = Text2FraqConfig(
        provider="ollama",
        model="qwen2.5:3b",
        base_url="http://localhost:11434",
        temperature=0.1,
        max_tokens=256,
    )

    try:
        t2f = Text2Fraq(config)
        searcher = FileSearchText2Fraq(base_path)

        # Zapytanie po polsku - jak użytkownik prosił
        polish_queries = [
            "Podaj listę 10 plików pdf, które zostały ostatnio utworzone",
            "Znajdź 5 najnowszych plików python",
            "Pokaż wszystkie pliki markdown",
            "Lista plików txt z ostatniego tygodnia",
        ]

        print("\n  Zapytania w języku polskim:")
        for q in polish_queries:
            print(f"\n  NL: \"{q}\"")
            try:
                # Najpierw spróbuj zrozumieć przez LLM
                # Ale FileSearchText2Fraq działa rule-based
                parsed = searcher.parse(q)
                print(f"  → extension={parsed['extension']}, limit={parsed['limit']}")

                # Jeśli rozpoznano rozszerzenie, wyszukaj
                if parsed['extension']:
                    results = searcher.search(q)
                    print(f"  → Znaleziono {len(results)} plików:")
                    for r in results[:3]:
                        mtime_str = datetime.fromtimestamp(r['mtime']).strftime('%Y-%m-%d %H:%M')
                        print(f"     - {r['filename']} ({r['size']} b, {mtime_str})")
                else:
                    print("  → Nie rozpoznano typu pliku, używam fallback...")
                    # Fallback - szukaj wszystkich plików
                    results = searcher.adapter.search(limit=parsed['limit'])
                    for r in results[:3]:
                        print(f"     - {r['filename']}")

            except Exception as e:
                print(f"  → ERROR: {e}")

    except ImportError:
        print("  LiteLLM niezainstalowany. Instaluj: pip install litellm")
    except Exception as e:
        print(f"  Błąd Ollama: {e}")
        print("  Upewnij się, że ollama jest uruchomiona i model qwen2.5:3b jest pobrany")

    print()


def example_convenience_function():
    """Użycie funkcji text2filesearch."""
    print("=" * 60)
    print("3. FUNKCJA text2filesearch() - one-liner")
    print("=" * 60)

    base_path = os.path.expanduser("~/github/wronai/fraq")
    if not os.path.exists(base_path):
        base_path = "."

    print(f"\n  Szukam w: {base_path}")

    # Przykłady użycia
    examples = [
        ("list 10 pdf files", base_path, "json"),
        ("show 5 py files", base_path, "csv"),
    ]

    for query, path, fmt in examples:
        print(f"\n  Query: \"{query}\" (format={fmt})")
        try:
            result = text2filesearch(query, path, fmt)
            if isinstance(result, str):
                print(f"  → {result[:300]}...")
            else:
                print(f"  → {len(result)} records")
                for r in result[:2]:
                    print(f"     {r.get('filename', 'N/A')}")
        except Exception as e:
            print(f"  → ERROR: {e}")

    print()


def example_file_search_adapter_direct():
    """Bezpośrednie użycie FileSearchAdapter."""
    print("=" * 60)
    print("4. BEZPOŚREDNIE UŻYCIE FileSearchAdapter")
    print("=" * 60)

    base_path = os.path.expanduser("~/github/wronai/fraq")
    if not os.path.exists(base_path):
        base_path = "."

    adapter = FileSearchAdapter(base_path=base_path, recursive=True)

    print(f"\n  Szukanie w: {base_path}")

    # Różne wyszukiwania
    searches = [
        {"extension": "py", "limit": 5, "sort_by": "name"},
        {"extension": "md", "limit": 3, "sort_by": "mtime"},
        {"pattern": "*.toml", "limit": 5},
    ]

    for params in searches:
        print(f"\n  Search params: {params}")
        results = adapter.search(**params)
        print(f"  → Znaleziono {len(results)}:")
        for r in results:
            size_kb = r['size'] / 1024
            print(f"     - {r['filename']} ({size_kb:.1f} KB, depth={r['depth']})")

    print()


def example_llm_file_intent():
    """Rozpoznawanie intencji plikowych przez LLM."""
    print("=" * 60)
    print("5. LLM ROZPOZNAJE INTENCJĘ PLIKOWĄ")
    print("=" * 60)

    config = Text2FraqConfig(
        provider="ollama",
        model="qwen2.5:3b",
        base_url="http://localhost:11434",
        temperature=0.1,
    )

    try:
        t2f = Text2Fraq(config)

        # LLM powinien zrozumieć intencję wyszukiwania plików
        file_intent_queries = [
            "Chcę znaleźć wszystkie dokumenty PDF w folderze",
            "Pokaż mi najnowsze pliki tekstowe",
            "Potrzebuję listy plików python z tego projektu",
            "Znajdź duże pliki graficzne (png, jpg)",
        ]

        print("\n  LLM parsuje intencję:")
        for q in file_intent_queries:
            print(f"\n  NL: \"{q}\"")
            try:
                # LLM parsuje do struktury
                parsed = t2f.parse(q)
                print(f"  → fields: {parsed.fields}")
                print(f"  → format: {parsed.format}, limit: {parsed.limit}")
            except Exception as e:
                print(f"  → ERROR: {e}")

    except Exception as e:
        print(f"  Błąd: {e}")

    print()


# ═══════════════════════════════════════════════════════════════════════════
# RUN ALL
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    example_pdf_search_rule_based()
    example_pdf_search_with_llm()
    example_convenience_function()
    example_file_search_adapter_direct()
    example_llm_file_intent()

    print("=" * 60)
    print("PODSUMOWANIE")
    print("=" * 60)
    print("""
1. FileSearchText2Fraq - rule-based parser dla zapytań o pliki
   Rozpoznaje: rozszerzenia (pdf, txt, py, md...), liczby, czas (recent, today, week)

2. FileSearchAdapter - adapter do wyszukiwania plików z metadanymi
   Zwraca: filename, path, size, mtime, fraq_position, fraq_seed, fraq_value

3. text2filesearch() - one-liner do wyszukiwania plików

4. Integracja z LLM (qwen2.5:3b):
   - LLM może parsować zapytania naturalne (np. po polsku)
   - FileSearchText2Fraq wykonuje wyszukiwanie
   - Wyniki w formacie JSON/CSV/YAML

Przykład użycia z Twoim zapytaniem:
    >>> text2filesearch(
    ...     "Podaj listę 10 plików pdf, które zostały ostatnio utworzone",
    ...     "/ścieżka/do/folderu"
    ... )
""")
