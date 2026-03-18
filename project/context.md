# System Architecture Analysis

## Overview

- **Project**: fraq
- **Language**: python
- **Files**: 47
- **Lines**: 9108
- **Functions**: 289
- **Classes**: 59
- **Avg CC**: 2.8
- **Critical (CC≥10)**: 2

## Architecture

### fraq/ (14 files, 3646L, 128 functions)

- `benchmarks.py` — 263L, 8 methods, CC↑11
- `cli.py` — 477L, 24 methods, CC↑9
- `query.py` — 220L, 12 methods, CC↑9
- `core.py` — 412L, 17 methods, CC↑8
- `server.py` — 217L, 7 methods, CC↑8
- _9 more files_

### fraq/adapters/ (9 files, 621L, 41 functions)

- `hybrid_adapter.py` — 51L, 4 methods, CC↑8
- `file_search.py` — 268L, 18 methods, CC↑7
- `sql_adapter.py` — 64L, 5 methods, CC↑6
- `file_adapter.py` — 47L, 3 methods, CC↑3
- `http_adapter.py` — 46L, 2 methods, CC↑3
- _4 more files_

### fraq/export/ (8 files, 512L, 7 functions)

- `nlp2cmd.py` — 138L, 2 methods, CC↑5
- `asyncapi.py` — 67L, 1 methods, CC↑2
- `graphql.py` — 36L, 1 methods, CC↑2
- `json_schema.py` — 32L, 1 methods, CC↑2
- `openapi.py` — 116L, 1 methods, CC↑2
- _3 more files_

### fraq/formats/ (5 files, 332L, 22 functions)

- `prepare.py` — 47L, 2 methods, CC↑8
- `text.py` — 71L, 5 methods, CC↑7
- `binary.py` — 100L, 11 methods, CC↑3
- `registry.py` — 40L, 4 methods, CC↑2
- `__init__.py` — 74L, 0 methods, CC↑0

### fraq/inference/ (5 files, 587L, 29 functions)

- `correlation.py` — 98L, 4 methods, CC↑8
- `dimension.py` — 126L, 8 methods, CC↑7
- `hierarchy.py` — 130L, 7 methods, CC↑5
- `schema.py` — 109L, 5 methods, CC↑5
- `__init__.py` — 124L, 5 methods, CC↑2

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

- **FraqFilter** (class, CC̄=9.0)
- **FraqSchema** (class, CC̄=5.8)
- **CorrelationAnalyzer** (class, CC̄=5.2)
- **ParsedQuery** (class, CC̄=5.0)

## Hotspots (High Fan-Out)

- **FileSearchText2Fraq._collect_files_filtered** — fan-out=16: Collect files with exclusion filtering.
- **FileAdapter.load_root** — fan-out=13: Orchestrates 13 calls
- **ws_stream** — fan-out=13: WebSocket endpoint for streaming fractal data.
- **ws_stream** — fan-out=11: Orchestrates 11 calls
- **cmd_schema** — fan-out=11: Orchestrates 11 calls
- **_dispatch_command** — fan-out=10: 10-way dispatch
- **HTTPAdapter.load_root** — fan-out=10: Orchestrates 10 calls

## Refactoring Priorities

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | Break circular dependency: fraq.formats.prepare.prepare | medium | low |
| 2 | Break circular dependency: fraq.formats.text.simple_yaml | medium | low |
| 3 | Reduce FileSearchText2Fraq._collect_files_filtered fan-out (currently 16) | medium | medium |

## Context for LLM

When suggesting changes:
1. Start from hotspots and high-CC functions
2. Follow refactoring priorities above
3. Maintain public API surface — keep backward compatibility
4. Prefer minimal, incremental changes

