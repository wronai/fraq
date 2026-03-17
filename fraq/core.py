"""
Core fractal data structures.

The fundamental idea: a FraqNode is a point in an infinite fractal space.
It has a *position* (coordinates in hyperspace) and a *generator* that
deterministically produces child nodes when you zoom in.  Because generation
is deterministic and lazy, the same path always yields the same data — yet
the tree is unbounded.

FraqSchema wraps a root node and gives it a typed envelope (field names,
types, constraints) so the fractal can masquerade as familiar structured
data (JSON objects, Protobuf messages, CSV rows …).

FraqCursor is a stateful iterator that walks the fractal, remembering its
current depth and direction so callers can stream data without holding the
whole tree in memory.
"""

from __future__ import annotations

import hashlib
import math
import struct
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)


# ---------------------------------------------------------------------------
# Vector helpers
# ---------------------------------------------------------------------------

Vector = Tuple[float, ...]


def _vec_add(a: Vector, b: Vector) -> Vector:
    return tuple(x + y for x, y in zip(a, b))


def _vec_scale(v: Vector, s: float) -> Vector:
    return tuple(x * s for x in v)


def _vec_norm(v: Vector) -> float:
    return math.sqrt(sum(x * x for x in v))


def _vec_hash(v: Vector, seed: int = 0) -> int:
    """Deterministic hash of a float vector."""
    # Use bytes representation to avoid struct overflow on large seeds
    raw = hashlib.sha256(f"{seed}:{v}".encode()).digest()
    return int.from_bytes(raw[:16], "big")


# ---------------------------------------------------------------------------
# FraqNode
# ---------------------------------------------------------------------------


@dataclass
class FraqNode:
    """A single point in the infinite fractal data space.

    Parameters
    ----------
    position : Vector
        Coordinates in hyperspace (dimensionality is user-defined).
    depth : int
        Current zoom depth (0 = root).
    seed : int
        Deterministic seed derived from the path taken to reach this node.
    generator : Callable | None
        A callable ``(node) -> scalar_value`` used to produce the node's
        *payload*.  If ``None`` a default hash-based generator is used.
    meta : dict
        Arbitrary metadata attached to the node.
    """

    position: Vector
    depth: int = 0
    seed: int = 0
    generator: Optional[Callable[["FraqNode"], Any]] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    # Lazy child cache – keyed by direction vector
    _children: Dict[Vector, "FraqNode"] = field(
        default_factory=dict, repr=False, compare=False
    )

    # ----- value production ---------------------------------------------------

    @property
    def value(self) -> Any:
        """Materialise the scalar value at this node."""
        if self.generator is not None:
            return self.generator(self)
        # Default: deterministic float in [0, 1)
        return (_vec_hash(self.position, self.seed) % (2**32)) / (2**32)

    # ----- zoom / navigation --------------------------------------------------

    def zoom(
        self,
        direction: Optional[Vector] = None,
        *,
        steps: int = 1,
    ) -> "FraqNode":
        """Zoom into the fractal along *direction* by *steps* levels.

        Parameters
        ----------
        direction : Vector | None
            Unit direction in hyperspace.  Defaults to the last axis
            (e.g. ``(0, 0, …, 1)``).
        steps : int
            How many zoom levels to descend at once.

        Returns
        -------
        FraqNode
            The deepest node reached.
        """
        if direction is None:
            dims = len(self.position)
            direction = tuple(1.0 if i == dims - 1 else 0.0 for i in range(dims))

        node = self
        for _ in range(steps):
            node = node._child(direction)
        return node

    def children(
        self,
        directions: Optional[Sequence[Vector]] = None,
        *,
        branching: int = 4,
    ) -> List["FraqNode"]:
        """Return children in several directions (auto-generated if omitted).

        If *directions* is ``None``, ``branching`` evenly-spaced directions
        in the node's hyperspace are created automatically.
        """
        if directions is None:
            dims = len(self.position)
            directions = []
            for i in range(branching):
                angle = 2 * math.pi * i / branching
                d = tuple(
                    math.cos(angle + j * math.pi / dims) for j in range(dims)
                )
                directions.append(d)
        return [self._child(d) for d in directions]

    # ----- internals ----------------------------------------------------------

    def _child(self, direction: Vector) -> "FraqNode":
        key = direction
        if key not in self._children:
            new_seed = _vec_hash(direction, self.seed)
            scale = 1.0 / (self.depth + 2)  # finer grain at deeper levels
            new_pos = _vec_add(self.position, _vec_scale(direction, scale))
            self._children[key] = FraqNode(
                position=new_pos,
                depth=self.depth + 1,
                seed=new_seed,
                generator=self.generator,
            )
        return self._children[key]

    # ----- dict / serialisation helpers ---------------------------------------

    def to_dict(self, max_depth: int = 0) -> Dict[str, Any]:
        """Snapshot of this node as a plain dict.

        Parameters
        ----------
        max_depth : int
            How many child levels to include (0 = this node only).
        """
        d: Dict[str, Any] = {
            "position": list(self.position),
            "depth": self.depth,
            "seed": self.seed,
            "value": self.value,
        }
        if self.meta:
            d["meta"] = self.meta
        if max_depth > 0 and self._children:
            d["children"] = {
                str(k): v.to_dict(max_depth - 1) for k, v in self._children.items()
            }
        return d

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"FraqNode(pos={self.position}, depth={self.depth}, "
            f"value={self.value:.6f})"
        )


# ---------------------------------------------------------------------------
# FraqSchema — typed envelope over a fractal
# ---------------------------------------------------------------------------


@dataclass
class FieldDef:
    """One field in a FraqSchema."""

    name: str
    type: str = "float"  # float | int | str | bool | bytes | list | dict
    direction: Optional[Vector] = None  # which fractal axis maps to this field
    transform: Optional[Callable[[Any], Any]] = None  # post-processing


@dataclass
class FraqSchema:
    """Typed projection of a fractal into structured records.

    A schema maps *directions* in the fractal space to named, typed fields.
    Iterating the schema at a given depth yields records (dicts) where each
    key corresponds to a field and the value is produced by zooming in the
    field's direction.

    Parameters
    ----------
    root : FraqNode, optional
        Root of the fractal. Auto-created with 3 dimensions if not provided.
    fields : list[FieldDef]
        Field definitions.

    Examples
    --------
    >>> # Auto root - simplest usage
    >>> schema = FraqSchema()
    >>> schema.add_field("temp", "float", transform=lambda v: round(float(v)*40, 1))
    >>> records = list(schema.records(count=10))
    
    >>> # With custom root
    >>> root = FraqNode(position=(0.0, 0.0, 0.0), seed=42)
    >>> schema = FraqSchema(root=root)
    """

    root: FraqNode = field(default_factory=lambda: FraqNode(position=(0.0, 0.0, 0.0)))
    fields: List[FieldDef] = field(default_factory=list)

    def add_field(
        self,
        name: str,
        type: str = "float",
        direction: Optional[Vector] = None,
        transform: Optional[Callable[[Any], Any]] = None,
    ) -> "FraqSchema":
        dims = len(self.root.position)
        if direction is None:
            idx = len(self.fields)
            direction = tuple(
                1.0 if i == idx % dims else 0.0 for i in range(dims)
            )
        self.fields.append(FieldDef(name, type, direction, transform))
        return self  # fluent API

    def record(self, node: Optional[FraqNode] = None) -> Dict[str, Any]:
        """Produce a single record from *node* (defaults to root)."""
        node = node or self.root
        rec: Dict[str, Any] = {}
        for f in self.fields:
            child = node.zoom(f.direction)
            val = child.value
            # Apply transform BEFORE type casting to avoid type conflicts
            if f.transform:
                val = f.transform(val)
            else:
                val = self._cast(val, f.type)
            rec[f.name] = val
        return rec

    def records(
        self,
        depth: Optional[int] = None,
        branching: int = 4,
        count: Optional[int] = None,
        node: Optional[FraqNode] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Yield records by exploring children.
        
        Parameters
        ----------
        depth : int, optional
            Depth level for exploration. Mutually exclusive with count.
        branching : int
            Number of children per node (default 4).
        count : int, optional
            Exact number of records to yield. Easier than calculating depth.
        node : FraqNode, optional
            Starting node (defaults to root).
        
        Examples
        --------
        >>> # Get exactly 100 records (easiest)
        >>> records = list(schema.records(count=100))
        
        >>> # Or use depth for fractal exploration
        >>> records = list(schema.records(depth=3))
        """
        node = node or self.root
        
        # If count specified, use simple iteration (easier API)
        if count is not None:
            yielded = 0
            cursor = FraqCursor(root=node)
            for _ in range(count):
                if yielded >= count:
                    break
                cursor.advance()
                rec = self.record(cursor.current)
                rec['_index'] = yielded  # Add index for reference
                yielded += 1
                yield rec
            return
        
        # Otherwise use depth-based exploration
        depth = depth or 1
        if depth <= 0:
            yield self.record(node)
            return
        for child in node.children(branching=branching):
            yield from self.records(depth - 1, branching, None, child)

    @staticmethod
    def _cast(val: Any, type_name: str) -> Any:
        """Cast value to type. Note: transforms are applied BEFORE this."""
        if type_name == "int":
            return int(float(val))  # Safer - accepts float strings
        if type_name == "str":
            return str(val)  # Simple string conversion
        if type_name == "bool":
            return bool(val) if isinstance(val, (int, float, bool)) else str(val).lower() in ('true', '1', 'yes')
        if type_name == "bytes":
            return struct.pack("!d", float(val))
        return float(val) if type_name == "float" else val


# ---------------------------------------------------------------------------
# FraqCursor — stateful iterator
# ---------------------------------------------------------------------------


@dataclass
class FraqCursor:
    """Stateful walk through the fractal.

    The cursor remembers the path (sequence of directions) taken so far and
    can be serialised / deserialised to resume iteration later.
    """

    root: FraqNode
    path: List[Vector] = field(default_factory=list)
    _current: Optional[FraqNode] = field(default=None, repr=False)

    @property
    def current(self) -> FraqNode:
        if self._current is None:
            node = self.root
            for d in self.path:
                node = node.zoom(d)
            self._current = node
        return self._current

    @property
    def depth(self) -> int:
        return len(self.path)

    def advance(self, direction: Optional[Vector] = None) -> FraqNode:
        """Move one level deeper and return the new node."""
        node = self.current.zoom(direction)
        if direction is None:
            dims = len(self.root.position)
            direction = tuple(1.0 if i == dims - 1 else 0.0 for i in range(dims))
        self.path.append(direction)
        self._current = node
        return node

    def back(self) -> FraqNode:
        """Go up one level."""
        if self.path:
            self.path.pop()
        self._current = None  # force re-walk
        return self.current

    def reset(self) -> FraqNode:
        """Return to root."""
        self.path.clear()
        self._current = None
        return self.current

    def snapshot(self) -> Dict[str, Any]:
        """Serialisable state."""
        return {
            "root_position": list(self.root.position),
            "root_seed": self.root.seed,
            "path": [list(d) for d in self.path],
        }
