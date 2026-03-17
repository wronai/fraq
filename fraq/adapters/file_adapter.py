"""File adapter for local JSON/YAML/CSV files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict

from fraq.core import FraqNode
from fraq.formats import FormatRegistry
from fraq.query import SourceType
from fraq.adapters.base import BaseAdapter


class FileAdapter(BaseAdapter):
    """Read/write fractal state from local files."""

    source_type = SourceType.FILE

    def load_root(self, uri: str, **opts: Any) -> FraqNode:
        path = Path(uri)
        if not path.exists():
            seed = int(hashlib.sha256(uri.encode()).hexdigest()[:8], 16)
            dims = opts.get("dims", 3)
            return FraqNode(position=tuple(0.0 for _ in range(dims)), seed=seed)

        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        return self._dict_to_node(data)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        path = Path(uri)
        content = FormatRegistry.serialize(fmt, node.to_dict(max_depth=opts.get("max_depth", 1)))
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return str(path.resolve())

    @staticmethod
    def _dict_to_node(data: Dict[str, Any]) -> FraqNode:
        return FraqNode(
            position=tuple(data.get("position", [0.0, 0.0, 0.0])),
            depth=data.get("depth", 0),
            seed=data.get("seed", 0),
        )
