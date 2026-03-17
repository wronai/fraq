# System Architecture Analysis

## Overview

- **Project**: fraq
- **Language**: python
- **Files**: 9
- **Lines**: 3428
- **Functions**: 106
- **Classes**: 26
- **Avg CC**: 2.8
- **Critical (CC≥10)**: 3

## Architecture

### fraq/ (10 files, 2339L, 106 functions)

- `text2fraq.py` — 341L, 14 methods, CC↑18
- `formats.py` — 196L, 14 methods, CC↑11
- `query.py` — 219L, 12 methods, CC↑9
- `adapters.py` — 394L, 23 methods, CC↑8
- `core.py` — 360L, 17 methods, CC↑5
- _5 more files_

### root/ (1 files, 14L, 0 functions)

- `project.sh` — 14L, 0 methods, CC↑0

## Key Exports

- **Text2Fraq** (class, CC̄=5.4)
  - `_fallback_parse` CC=18 ⚠ split
- **Text2FraqSimple** (class, CC̄=8.5)
  - `parse` CC=15 ⚠ split
- **FraqFilter** (class, CC̄=9.0)

## Hotspots (High Fan-Out)

- **main** — fan-out=14: Orchestrates 14 calls
- **FileAdapter.load_root** — fan-out=13: Orchestrates 13 calls
- **cmd_schema** — fan-out=11: Orchestrates 11 calls
- **_to_csv** — fan-out=10: Serialise list of flat dicts to CSV.
- **HTTPAdapter.load_root** — fan-out=10: Orchestrates 10 calls
- **SQLAdapter.load_root** — fan-out=10: Orchestrates 10 calls

## Refactoring Priorities

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | Split Text2Fraq._fallback_parse (CC=18 → target CC<10) | medium | low |
| 2 | Split Text2FraqSimple.parse (CC=15 → target CC<10) | medium | low |
| 3 | Break circular dependency: fraq.formats._prepare | medium | low |
| 4 | Break circular dependency: fraq.formats._simple_yaml | medium | low |
| 5 | Break circular dependency: fraq.formats._mp_encode | medium | low |

## Context for LLM

When suggesting changes:
1. Start from hotspots and high-CC functions
2. Follow refactoring priorities above
3. Maintain public API surface — keep backward compatibility
4. Prefer minimal, incremental changes

