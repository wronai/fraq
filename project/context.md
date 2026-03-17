# System Architecture Analysis

## Overview

- **Project**: fraq
- **Language**: python
- **Files**: 38
- **Lines**: 7433
- **Functions**: 261
- **Classes**: 53
- **Avg CC**: 3.1
- **Critical (CC≥10)**: 10

## Architecture

### fraq/ (14 files, 3459L, 121 functions)

- `inference.py` — 347L, 10 methods, CC↑16
- `benchmarks.py` — 263L, 8 methods, CC↑11
- `api.py` — 189L, 6 methods, CC↑10
- `query.py` — 220L, 12 methods, CC↑9
- `cli.py` — 467L, 24 methods, CC↑8
- _9 more files_

### fraq/adapters/ (11 files, 1017L, 64 functions)

- `web_crawler.py` — 204L, 12 methods, CC↑10
- `hybrid_adapter.py` — 51L, 4 methods, CC↑8
- `file_search.py` — 268L, 18 methods, CC↑7
- `sql_adapter.py` — 64L, 5 methods, CC↑6
- `network.py` — 186L, 11 methods, CC↑5
- _6 more files_

### fraq/formats/ (5 files, 294L, 14 functions)

- `binary.py` — 62L, 3 methods, CC↑11
- `prepare.py` — 47L, 2 methods, CC↑8
- `text.py` — 71L, 5 methods, CC↑7
- `registry.py` — 40L, 4 methods, CC↑2
- `__init__.py` — 74L, 0 methods, CC↑0

### fraq/providers/ (2 files, 212L, 13 functions)

- `faker_provider.py` — 177L, 13 methods, CC↑6
- `__init__.py` — 35L, 0 methods, CC↑0

### fraq/text2fraq/ (10 files, 835L, 46 functions)

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

- **FractalAnalyzer** (class, CC̄=11.8)
  - `box_counting_dimension` CC=16 ⚠ split
  - `detect_hierarchy` CC=15 ⚠ split
  - `analyze_correlations` CC=15 ⚠ split
- **FraqFilter** (class, CC̄=9.0)
- **FraqSchema** (class, CC̄=5.8)
- **ParsedQuery** (class, CC̄=5.0)

## Hotspots (High Fan-Out)

- **FileSearchText2Fraq._collect_files_filtered** — fan-out=16: Collect files with exclusion filtering.
- **FractalAnalyzer.detect_hierarchy** — fan-out=14: Detect hierarchical structure in data.

Analyzes parent-child relationships to f
- **FractalAnalyzer.box_counting_dimension** — fan-out=13: Calculate box-counting dimension of value distribution.

True fractals have non-
- **FileAdapter.load_root** — fan-out=13: Orchestrates 13 calls
- **ws_stream** — fan-out=13: WebSocket endpoint for streaming fractal data.
- **_parse_transform** — fan-out=12: Parse type specification and return transform function.

Handles: range hints (f
- **WebCrawlerAdapter.crawl_async** — fan-out=12: Crawl website and return all pages.

## Refactoring Priorities

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | Split FractalAnalyzer.box_counting_dimension (CC=16 → target CC<10) | medium | low |
| 2 | Split FractalAnalyzer.detect_hierarchy (CC=15 → target CC<10) | medium | low |
| 3 | Split FractalAnalyzer.analyze_correlations (CC=15 → target CC<10) | medium | low |
| 4 | Break circular dependency: fraq.formats.prepare.prepare | medium | low |
| 5 | Break circular dependency: fraq.formats.binary.mp_encode | medium | low |
| 6 | Break circular dependency: fraq.formats.text.simple_yaml | medium | low |
| 7 | Reduce FileSearchText2Fraq._collect_files_filtered fan-out (currently 16) | medium | medium |

## Context for LLM

When suggesting changes:
1. Start from hotspots and high-CC functions
2. Follow refactoring priorities above
3. Maintain public API surface — keep backward compatibility
4. Prefer minimal, incremental changes

