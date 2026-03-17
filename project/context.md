# System Architecture Analysis

## Overview

- **Project**: fraq
- **Language**: python
- **Files**: 29
- **Lines**: 5691
- **Functions**: 196
- **Classes**: 35
- **Avg CC**: 3.1
- **Critical (CC≥10)**: 6

## Architecture

### fraq/ (10 files, 2532L, 93 functions)

- `__init__.py` — 310L, 4 methods, CC↑11
- `formats.py` — 196L, 14 methods, CC↑11
- `query.py` — 220L, 12 methods, CC↑9
- `cli.py` — 449L, 18 methods, CC↑8
- `core.py` — 412L, 17 methods, CC↑8
- _5 more files_

### fraq/adapters/ (11 files, 914L, 54 functions)

- `web_crawler.py` — 204L, 12 methods, CC↑10
- `file_search.py` — 165L, 8 methods, CC↑8
- `hybrid_adapter.py` — 51L, 4 methods, CC↑8
- `sql_adapter.py` — 64L, 5 methods, CC↑6
- `network.py` — 186L, 11 methods, CC↑5
- _6 more files_

### fraq/text2fraq/ (10 files, 831L, 46 functions)

- `file_search_parser.py` — 200L, 11 methods, CC↑11
- `router.py` — 88L, 4 methods, CC↑9
- `parser_rules.py` — 93L, 8 methods, CC↑6
- `session.py` — 149L, 8 methods, CC↑6
- `models.py` — 41L, 2 methods, CC↑5
- _5 more files_

### root/ (2 files, 66L, 3 functions)

- `main_websocket.py` — 52L, 3 methods, CC↑5
- `project.sh` — 14L, 0 methods, CC↑0

## Key Exports

- **FraqFilter** (class, CC̄=9.0)
- **FraqSchema** (class, CC̄=5.8)
- **ParsedQuery** (class, CC̄=5.0)

## Hotspots (High Fan-Out)

- **_parse_args** — fan-out=21: Parse command line arguments.
- **generate** — fan-out=16: Generate records with simple field specification.

This is the EASIEST way to cr
- **FileSearchText2Fraq._collect_files_filtered** — fan-out=16: Collect files with exclusion filtering.
- **FileAdapter.load_root** — fan-out=13: Orchestrates 13 calls
- **ws_stream** — fan-out=13: WebSocket endpoint for streaming fractal data.
- **WebCrawlerAdapter.crawl_async** — fan-out=12: Crawl website and return all pages.
- **FileSearchAdapter._collect_files** — fan-out=12: Iterate filesystem and collect matching files.

## Refactoring Priorities

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | Break circular dependency: fraq.formats._prepare | medium | low |
| 2 | Break circular dependency: fraq.formats._simple_yaml | medium | low |
| 3 | Break circular dependency: fraq.formats._mp_encode | medium | low |
| 4 | Reduce _parse_args fan-out (currently 21) | medium | medium |
| 5 | Reduce generate fan-out (currently 16) | medium | medium |
| 6 | Reduce FileSearchText2Fraq._collect_files_filtered fan-out (currently 16) | medium | medium |

## Context for LLM

When suggesting changes:
1. Start from hotspots and high-CC functions
2. Follow refactoring priorities above
3. Maintain public API surface — keep backward compatibility
4. Prefer minimal, incremental changes

