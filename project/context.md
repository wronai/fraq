# System Architecture Analysis

## Overview

- **Project**: fraq
- **Language**: python
- **Files**: 9
- **Lines**: 4063
- **Functions**: 121
- **Classes**: 28
- **Avg CC**: 3.2
- **Critical (CC≥10)**: 5

## Architecture

### fraq/ (10 files, 2889L, 121 functions)

- `text2fraq.py` — 518L, 20 methods, CC↑18
- `adapters.py` — 577L, 28 methods, CC↑12
- `formats.py` — 196L, 14 methods, CC↑11
- `cli.py` — 274L, 9 methods, CC↑9
- `query.py` — 219L, 12 methods, CC↑9
- _5 more files_

### root/ (1 files, 14L, 0 functions)

- `project.sh` — 14L, 0 methods, CC↑0

## Key Exports

- **FileSearchText2Fraq** (class, CC̄=6.0)
  - `parse` CC=17 ⚠ split
- **Text2FraqSimple** (class, CC̄=6.3)
  - `parse` CC=15 ⚠ split
- **ParsedQuery** (class, CC̄=6.0)
- **Text2Fraq** (class, CC̄=5.8)
  - `_fallback_parse` CC=18 ⚠ split
- **FileSearchAdapter** (class, CC̄=5.8)
- **FraqFilter** (class, CC̄=9.0)

## Hotspots (High Fan-Out)

- **main** — fan-out=25: Orchestrates 25 calls
- **cmd_files_stat** — fan-out=14: Show file statistics with fractal coordinates.
- **FileSearchAdapter.search** — fan-out=14: Search files and return as fractal records.

Args:
    extension: File extension
- **FileAdapter.load_root** — fan-out=13: Orchestrates 13 calls
- **cmd_schema** — fan-out=11: Orchestrates 11 calls
- **cmd_nl** — fan-out=11: Natural language query (requires LLM).
- **FileSearchAdapter.load_root** — fan-out=11: Create root node representing the search space.
URI can be path or empty (uses b

## Refactoring Priorities

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | Split god module fraq/text2fraq.py (518L, 7 classes) | high | high |
| 2 | Split god module fraq/adapters.py (577L, 7 classes) | high | high |
| 3 | Split FileSearchText2Fraq.parse (CC=17 → target CC<10) | medium | low |
| 4 | Split Text2Fraq._fallback_parse (CC=18 → target CC<10) | medium | low |
| 5 | Split Text2FraqSimple.parse (CC=15 → target CC<10) | medium | low |
| 6 | Break circular dependency: fraq.formats._prepare | medium | low |
| 7 | Break circular dependency: fraq.formats._simple_yaml | medium | low |
| 8 | Break circular dependency: fraq.formats._mp_encode | medium | low |
| 9 | Reduce main fan-out (currently 25) | medium | medium |

## Context for LLM

When suggesting changes:
1. Start from hotspots and high-CC functions
2. Follow refactoring priorities above
3. Maintain public API surface — keep backward compatibility
4. Prefer minimal, incremental changes

