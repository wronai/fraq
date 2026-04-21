# fraq — Architecture

> 118 modules | 257 functions | 133 classes | CC̄=2.6 | critical:0 | cycles:0

## Ecosystem Pipeline

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

## DOQL Application Declaration (`app.doql.less`)

```less
app {
  name: fraq;
  version: 0.2.14;
}

interface[type="cli"] {
  framework: click;
}

workflow[name="install"] {
  trigger: manual;
  step-1: run cmd=pip install -e .;
}

workflow[name="dev"] {
  trigger: manual;
  step-1: run cmd=pip install -e ".[dev]";
}

workflow[name="build"] {
  trigger: manual;
  step-1: run cmd=python -m build;
}

workflow[name="test"] {
  trigger: manual;
  step-1: run cmd=pytest -q;
}

workflow[name="lint"] {
  trigger: manual;
  step-1: run cmd=ruff check .;
}

workflow[name="fmt"] {
  trigger: manual;
  step-1: run cmd=ruff format .;
}

workflow[name="clean"] {
  trigger: manual;
  step-1: run cmd=rm -rf build/ dist/ *.egg-info;
}

workflow[name="help"] {
  trigger: manual;
  step-1: run cmd=task --list;
}

deploy {
  target: pip;
}

environment[name="local"] {
  runtime: python;
}
```

## Source Modules

- `fraq.api`
- `fraq.benchmarks`
- `fraq.cli`
- `fraq.core`
- `fraq.dataframes`
- `fraq.formats`
- `fraq.generators`
- `fraq.ifs`
- `fraq.inference`
- `fraq.query`
- `fraq.schema_export`
- `fraq.server`
- `fraq.streaming`
- `fraq.testing`
- `fraq.types`

## Interfaces

### CLI Entry Points

- `fraq`

## Code Analysis Summary

### `project/map.toon.yaml`

```
# fraq | 118f 14002L | python:109,shell:8,less:1 | 2026-04-21
# stats: 257 func | 133 cls | 118 mod | CC̄=2.6 | critical:0 | cycles:0
# alerts[5]: CC example_pdf_search_with_llm=9; CC cmd_network_scan=9; CC cmd_web_crawl=8; CC _dispatch_command=8; CC prepare=8
# hotspots[5]: query_data fan=18; ws_files fan=16; schema_records fan=15; stream fan=14; files_stat fan=14
# evolution: baseline
```

### Call Graph Summary

*184 nodes · 176 edges · 50 modules · CC̄=2.8*

#### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `generate` *(in fraq.inference.schema.InferredSchema)* | 4 | 40 | 6 | **46** |
| `to_proto` *(in fraq.export.proto)* | 2 | 2 | 27 | **29** |
| `_build_files_parsers` *(in fraq.cli)* | 1 | 1 | 22 | **23** |
| `example_full_nlp2cmd_workflow` *(in examples.text2fraq.nlp2cmd_integration)* | 3 | 0 | 19 | **19** |
| `prepare` *(in fraq.formats.prepare)* | 8 | 7 | 12 | **19** |
| `example_streaming_comparison` *(in examples.network.network_web_examples)* | 1 | 1 | 18 | **19** |
| `simple_yaml` *(in fraq.formats.text)* | 7 | 3 | 15 | **18** |
| `to_graphql` *(in fraq.export.graphql)* | 2 | 1 | 17 | **18** |

### Design Patterns

| Pattern | Where | Benefit |
|---------|-------|---------|
| **Port/Adapter** | `FileSearchAdapter` | I/O separated from business logic, 80%+ pure functions |
| **Pipeline** | `generate()` | 3 steps: `_fields_to_schema` → `_parse_transform` → `_generate_records` |
| **Registry** | `formats/` | Dynamic format registration, no cycles |
| **Command** | `cli.py` | Subparsers split by domain (core, files, network, web) |

### Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Cyclomatic Complexity (avg) | ≤ 2.5 | In progress |
| Circular dependencies | 0 | ✅ Achieved (formats/) |
| Pure functions in adapters | ≥ 80% | ✅ Achieved (FileSearchAdapter) |
| Test coverage | ≥ 95% | ✅ 96% (159 tests) |
