"""HTTP adapter for REST/GraphQL endpoints."""

from __future__ import annotations

import hashlib
from typing import Any

from fraq.core import FraqNode
from fraq.formats import FormatRegistry
from fraq.query import SourceType
from fraq.adapters.base import BaseAdapter
from fraq.adapters.file_adapter import FileAdapter


class HTTPAdapter(BaseAdapter):
    """Fetch fractal roots from remote HTTP APIs."""

    source_type = SourceType.HTTP

    def load_root(self, uri: str, **opts: Any) -> FraqNode:
        if not uri:
            return FraqNode(position=(0.0, 0.0, 0.0))
        try:
            import requests  # noqa: lazy import
            method = opts.get("method", "GET")
            headers = opts.get("headers", {})
            timeout = opts.get("timeout", 30)
            resp = requests.request(method, uri, headers=headers, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            return FileAdapter._dict_to_node(data)
        except Exception:
            seed = int(hashlib.sha256(uri.encode()).hexdigest()[:8], 16)
            return FraqNode(position=(0.0, 0.0, 0.0), seed=seed)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        try:
            import requests  # noqa
            payload = FormatRegistry.serialize(fmt, node.to_dict(max_depth=1))
            headers = opts.get("headers", {"Content-Type": "application/json"})
            timeout = opts.get("timeout", 30)
            resp = requests.post(uri, data=payload, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return uri
        except Exception:
            return ""
