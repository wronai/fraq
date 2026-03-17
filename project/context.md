# System Architecture Analysis

## Overview

- **Project**: fraq
- **Language**: python
- **Files**: 27
- **Lines**: 5958
- **Functions**: 237
- **Classes**: 46
- **Avg CC**: 3.0
- **Critical (CC≥10)**: 8

## Architecture

### fraq/ (10 files, 3333L, 156 functions)

- `cli.py` — 405L, 14 methods, CC↑13
- `adapters.py` — 970L, 47 methods, CC↑12
- `formats.py` — 196L, 14 methods, CC↑11
- `query.py` — 220L, 12 methods, CC↑9
- `text2fraq.py` — 434L, 31 methods, CC↑6
- _5 more files_

### fraq/adapters/ (11 files, 839L, 47 functions)

- `file_search.py` — 145L, 5 methods, CC↑12
- `web_crawler.py` — 179L, 10 methods, CC↑11
- `hybrid_adapter.py` — 51L, 4 methods, CC↑8
- `network.py` — 156L, 9 methods, CC↑8
- `sql_adapter.py` — 64L, 5 methods, CC↑6
- _6 more files_

### fraq/text2fraq/ (7 files, 458L, 31 functions)

- `file_search_parser.py` — 91L, 8 methods, CC↑6
- `parser_rules.py` — 93L, 8 methods, CC↑6
- `models.py` — 41L, 2 methods, CC↑5
- `parser_llm.py` — 109L, 7 methods, CC↑5
- `llm_client.py` — 35L, 2 methods, CC↑4
- _2 more files_

### root/ (2 files, 66L, 3 functions)

- `main_websocket.py` — 52L, 3 methods, CC↑5
- `project.sh` — 14L, 0 methods, CC↑0

## Key Exports

- **FileSearchAdapter** (class, CC̄=5.8)
- **FileSearchAdapter** (class, CC̄=5.8)
- **FraqFilter** (class, CC̄=9.0)
- **ParsedQuery** (class, CC̄=5.0)
- **ParsedQuery** (class, CC̄=5.0)

## Hotspots (High Fan-Out)

- **main** — fan-out=35: Orchestrates 35 calls
- **cmd_files_stat** — fan-out=14: Show file statistics with fractal coordinates.
- **FileSearchAdapter.search** — fan-out=14: Search files and return as fractal records.

Args:
    extension: File extension
- **FileSearchAdapter.search** — fan-out=14: Orchestrates 14 calls
- **NetworkAdapter._check_port** — fan-out=14: Orchestrates 14 calls
- **FileAdapter.load_root** — fan-out=13: Orchestrates 13 calls
- **NetworkAdapter._check_port** — fan-out=13: Check if port is open on host.

## Refactoring Priorities

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | Split god module fraq/adapters.py (970L, 9 classes) | high | high |
| 2 | Break circular dependency: fraq.formats._prepare | medium | low |
| 3 | Break circular dependency: fraq.formats._simple_yaml | medium | low |
| 4 | Break circular dependency: fraq.formats._mp_encode | medium | low |
| 5 | Reduce main fan-out (currently 35) | medium | medium |

## Context for LLM

When suggesting changes:
1. Start from hotspots and high-CC functions
2. Follow refactoring priorities above
3. Maintain public API surface — keep backward compatibility
4. Prefer minimal, incremental changes

