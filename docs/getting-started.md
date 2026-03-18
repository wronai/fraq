# Getting Started with fraq

## Prerequisites

- Python >=3.10
- pip (or your preferred package manager)

## Installation

```bash
pip install fraq
```

To install from source:

```bash
git clone https://github.com/wronai/fraq
cd fraq
pip install -e .
```

## Quick Start

### Command Line

```bash
# Generate full documentation for your project
fraq ./path/to/your/project

# Preview what would be generated (no file writes)
fraq ./path/to/your/project --dry-run

# Only regenerate README
fraq ./path/to/your/project --readme-only
```

### Python API

```python
from examples.text2fraq.nlp2cmd_integration import build_erp_schema

# Schemat ERP / accounting.
result = build_erp_schema()
```

## What's Next

- 📖 [API Reference](api.md) — Full function and class documentation
- 🏗️ [Architecture](architecture.md) — System design and module relationships
- 📊 [Coverage Report](coverage.md) — Docstring coverage analysis
- 🔗 [Dependency Graph](dependency-graph.md) — Module dependency visualization
