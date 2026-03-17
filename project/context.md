# System Architecture Analysis

## Overview

- **Project**: fraq
- **Language**: python
- **Files**: 8
- **Lines**: 3078
- **Functions**: 92
- **Classes**: 20
- **Avg CC**: 2.7
- **Critical (CC≥10)**: 1

## Architecture

### fraq/ (9 files, 1989L, 92 functions)

- `formats.py` — 196L, 14 methods, CC↑11
- `query.py` — 219L, 12 methods, CC↑9
- `adapters.py` — 394L, 23 methods, CC↑8
- `core.py` — 360L, 17 methods, CC↑5
- `schema_export.py` — 476L, 7 methods, CC↑5
- _4 more files_

### root/ (1 files, 14L, 0 functions)

- `project.sh` — 14L, 0 methods, CC↑0

## Key Exports

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
| 1 | Break circular dependency: fraq.formats._prepare | medium | low |
| 2 | Break circular dependency: fraq.formats._simple_yaml | medium | low |
| 3 | Break circular dependency: fraq.formats._mp_encode | medium | low |

## Context for LLM

When suggesting changes:
1. Start from hotspots and high-CC functions
2. Follow refactoring priorities above
3. Maintain public API surface — keep backward compatibility
4. Prefer minimal, incremental changes

