# System Architecture Analysis

## Overview

- **Project**: fraq
- **Language**: python
- **Files**: 10
- **Lines**: 4507
- **Functions**: 157
- **Classes**: 30
- **Avg CC**: 2.9
- **Critical (CC≥10)**: 4

## Architecture

### fraq/ (10 files, 3204L, 154 functions)

- `adapters.py` — 969L, 47 methods, CC↑12
- `formats.py` — 196L, 14 methods, CC↑11
- `cli.py` — 280L, 12 methods, CC↑9
- `query.py` — 220L, 12 methods, CC↑9
- `text2fraq.py` — 434L, 31 methods, CC↑6
- _5 more files_

### root/ (2 files, 66L, 3 functions)

- `main_websocket.py` — 52L, 3 methods, CC↑5
- `project.sh` — 14L, 0 methods, CC↑0

## Key Exports

- **FileSearchAdapter** (class, CC̄=5.8)
- **FraqFilter** (class, CC̄=9.0)
- **ParsedQuery** (class, CC̄=5.0)

## Hotspots (High Fan-Out)

- **main** — fan-out=25: Orchestrates 25 calls
- **cmd_files_stat** — fan-out=14: Show file statistics with fractal coordinates.
- **FileSearchAdapter.search** — fan-out=14: Search files and return as fractal records.

Args:
    extension: File extension
- **FileAdapter.load_root** — fan-out=13: Orchestrates 13 calls
- **NetworkAdapter._check_port** — fan-out=13: Check if port is open on host.
- **ws_stream** — fan-out=11: Orchestrates 11 calls
- **cmd_schema** — fan-out=11: Orchestrates 11 calls

## Refactoring Priorities

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | Split god module fraq/adapters.py (969L, 9 classes) | high | high |
| 2 | Break circular dependency: fraq.formats._prepare | medium | low |
| 3 | Break circular dependency: fraq.formats._simple_yaml | medium | low |
| 4 | Break circular dependency: fraq.formats._mp_encode | medium | low |
| 5 | Reduce main fan-out (currently 25) | medium | medium |

## Context for LLM

When suggesting changes:
1. Start from hotspots and high-CC functions
2. Follow refactoring priorities above
3. Maintain public API surface — keep backward compatibility
4. Prefer minimal, incremental changes

