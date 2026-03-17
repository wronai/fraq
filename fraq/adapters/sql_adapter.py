"""SQL adapter for PostgreSQL/SQLite databases."""

from __future__ import annotations

import hashlib
from typing import Any, Dict, Optional

from fraq.core import FraqNode
from fraq.query import SourceType
from fraq.adapters.base import BaseAdapter


class SQLAdapter(BaseAdapter):
    """Map fractal nodes to/from relational tables."""

    source_type = SourceType.SQL

    def __init__(
        self,
        table: str = "fraq_nodes",
        row_to_node: Optional[Any] = None,
    ):
        self.table = table
        self._row_to_node = row_to_node or self._default_row_to_node

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
        rows = opts.get("rows")
        if rows and len(rows) > 0:
            return self._row_to_node(rows[0])
        seed = int(hashlib.sha256(self.table.encode()).hexdigest()[:8], 16)
        dims = opts.get("dims", 3)
        return FraqNode(position=tuple(0.0 for _ in range(dims)), seed=seed)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        d = node.to_dict()
        cols = ", ".join(d.keys())
        vals = ", ".join(repr(v) for v in d.values())
        return f"INSERT INTO {self.table} ({cols}) VALUES ({vals});"

    def generate_sql_function(self, dims: int = 3) -> str:
        return f"""
CREATE OR REPLACE FUNCTION {self.table}_zoom(
    p_level INT,
    p_direction FLOAT[{dims}]
) RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'level', p_level,
        'direction', p_direction,
        'table', '{self.table}'
    ) INTO result;
    RETURN result;
END;
$$ LANGUAGE plpgsql;
"""

    @staticmethod
    def _default_row_to_node(row: Dict[str, Any]) -> FraqNode:
        numeric_vals = [v for v in row.values() if isinstance(v, (int, float))]
        pos = tuple(float(v) for v in numeric_vals[:3]) or (0.0, 0.0, 0.0)
        seed = int(numeric_vals[0]) if numeric_vals else 0
        return FraqNode(position=pos, seed=seed)
