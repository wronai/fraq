#!/usr/bin/env python3
"""
fraq text2fraq — Natural language → fractal query examples.

Setup:
    pip install -e ".[ai]"
    ollama pull qwen2.5:3b
    ollama pull llama3.2:3b
    ollama pull phi3:3.8b
    cp .env.example .env

Usage:
    python examples/text2fraq_examples.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from fraq import (
    FileSearchAdapter,
    FileSearchText2Fraq,
    Text2Fraq,
    Text2FraqConfig,
    Text2FraqSimple,
    text2filesearch,
    text2fraq,
    text2query,
)


def _print_header(title: str) -> None:
    print("=" * 72)
    print(title)
    print("=" * 72)


def _print_parsed_query(query: str, parsed) -> None:
    print(f'  "{query}"')
    print(
        f"    → fields={parsed.fields} depth={parsed.depth} "
        f"format={parsed.format} limit={parsed.limit}"
    )
    if parsed.filters:
        print(f"    → filters={parsed.filters}")


def _print_file_params(query: str, params: dict[str, object]) -> None:
    print(f'  "{query}"')
    print(
        f"    → extension={params.get('extension')} limit={params.get('limit')} "
        f"sort={params.get('sort_by')} recent={params.get('newer_than') is not None}"
    )


def example_simple_parser() -> None:
    """Rule-based parser — zero dependencies, works offline."""
    _print_header("1. RULE-BASED PARSER")
    simple = Text2FraqSimple()
    file_search = FileSearchText2Fraq(".")

    fraq_queries = [
        "stream 50 sensor readings",
        "show temperature data",
        "show 20 humidity samples in csv",
        "deep pressure analysis",
    ]
    file_queries = [
        "podaj 10 ostatnich plików PDF",
        "find 5 python files",
        "list 20 recent markdown files",
        "largest 3 csv files",
    ]

    print("=== Parsed Fraq queries ===")
    for query in fraq_queries:
        _print_parsed_query(query, simple.parse(query))

    print("\n=== Parsed file-search queries ===")
    for query in file_queries:
        _print_file_params(query, file_search.parse(query))
    print()


def example_qwen25() -> None:
    """qwen2.5:3b — good balance for Polish/English prompts."""
    _print_header("2. LLM PARSER — qwen2.5:3b")
    config = Text2FraqConfig(
        provider="ollama",
        model="qwen2.5:3b",
        base_url="http://localhost:11434",
        temperature=0.1,
        max_tokens=512,
    )

    queries = [
        "show 100 temperature readings as csv",
        "find active sensors with temperature greater than 0.7",
        "stream pressure data as jsonl",
    ]

    try:
        parser = Text2Fraq(config=config)
        for query in queries:
            _print_parsed_query(query, parser.parse(query))
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()


def example_llama32() -> None:
    """llama3.2:3b — alternative lightweight model."""
    _print_header("3. LLM PARSER — llama3.2:3b")
    config = Text2FraqConfig(
        provider="ollama",
        model="llama3.2:3b",
        base_url="http://localhost:11434",
        temperature=0.1,
        max_tokens=512,
    )

    try:
        parser = Text2Fraq(config=config)
        _print_parsed_query("extract 15 sensor records as yaml", parser.parse("extract 15 sensor records as yaml"))
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()


def example_phi3() -> None:
    """phi3:3.8b — stronger reasoning-oriented option."""
    _print_header("4. LLM PARSER — phi3:3.8b")
    config = Text2FraqConfig(
        provider="ollama",
        model="phi3:3.8b",
        base_url="http://localhost:11434",
        temperature=0.1,
        max_tokens=512,
    )

    try:
        parser = Text2Fraq(config=config)
        _print_parsed_query(
            "create a csv table with sensor_id temperature and active flag for 25 devices",
            parser.parse("create a csv table with sensor_id temperature and active flag for 25 devices"),
        )
    except Exception as exc:
        print(f"  ERROR: {exc}")
    print()


def example_convenience_functions() -> None:
    """One-liner functions — simplest possible API."""
    _print_header("5. CONVENIENCE FUNCTIONS")

    parsed = text2query("stream 30 pressure readings")
    print(f"  text2query → depth={parsed.depth} format={parsed.format} limit={parsed.limit}")

    file_results = text2filesearch("find 5 python files", base_path=".", fmt="records")
    print(f"  text2filesearch → {len(file_results)} files found")
    for record in file_results[:3]:
        print(f"    {record['filename']} ({record['size']} bytes)")

    try:
        result = text2fraq("show 5 temperature readings in json")
        print(f"  text2fraq → {type(result).__name__}, {len(str(result))} chars")
    except Exception as exc:
        print(f"  text2fraq → ERROR: {exc}")
    print()


def example_file_search_direct() -> None:
    """FileSearchAdapter — search real files on disk."""
    _print_header("6. FILE SEARCH ADAPTER")
    adapter = FileSearchAdapter(base_path=".", recursive=True)

    py_files = adapter.search(extension="py", limit=5, sort_by="mtime")
    print("  .py files (5 most recent):")
    for file_record in py_files[:5]:
        print(
            f"    {file_record['filename']:35} "
            f"{file_record['size']:>8} bytes"
        )

    test_files = adapter.search(pattern="test_*.py", limit=5)
    print("\n  test_*.py files:")
    for file_record in test_files:
        print(f"    {file_record['filename']}")

    csv_output = text2filesearch("show 3 markdown files", base_path=".", fmt="csv")
    print("\n  markdown files as CSV:")
    print(f"    {str(csv_output)[:200]}...")
    print()


def example_env_config() -> None:
    """Load config from .env file."""
    _print_header("7. .env CONFIGURATION")
    config = Text2FraqConfig.from_env()
    print(f"  provider:     {config.provider}")
    print(f"  model:        {config.model}")
    print(f"  base_url:     {config.base_url}")
    print(f"  temperature:  {config.temperature}")
    print(f"  max_tokens:   {config.max_tokens}")
    print(f"  default_fmt:  {config.default_format}")
    print(f"  default_dims: {config.default_dims}")
    print(f"  default_depth:{config.default_depth}")
    print()


def example_full_pipeline() -> None:
    """Full pipeline NL → parse → execute / file search."""
    _print_header("8. FULL PIPELINE")

    nl_query = "show 10 temperature readings in csv"
    parsed = Text2FraqSimple().parse(nl_query)
    _print_parsed_query(nl_query, parsed)

    try:
        result = text2fraq(nl_query)
        print(f"  execute → {str(result)[:200]}...")
    except Exception as exc:
        print(f"  execute → ERROR: {exc}")

    file_query = "podaj listę 10 plików PDF, które zostały ostatnio utworzone"
    file_search = FileSearchText2Fraq(".")
    params = file_search.parse(file_query)
    _print_file_params(file_query, params)
    results = file_search.search(file_query)
    print(f"  file search → {len(results)} results")
    for record in results[:3]:
        print(f"    {record.get('filename', '?')} — {record.get('size', 0)} bytes")
    print()


if __name__ == "__main__":
    example_simple_parser()
    example_convenience_functions()
    example_file_search_direct()
    example_env_config()
    example_full_pipeline()

    print("Uncomment below when Ollama is running with pulled models:")
    print("  # example_qwen25()")
    print("  # example_llama32()")
    print("  # example_phi3()")
