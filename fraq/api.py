"""
High-level API for fraq - simplified convenience functions.

This module provides the main user-facing API for fraq.
All functions are pure (no side effects) and deterministic.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterator, List, Literal, Optional, Union

from fraq.core import FraqNode, FraqSchema, FraqCursor

# Output format types for DataFrame export
DataFrameOutput = Literal["list", "polars", "pandas", "arrow", "records"]


class TypeTransformRegistry:
    """Registry for type transform factories. Reduces CC from 10 to ≤3."""
    
    _transforms: Dict[str, Callable[[str, str], Optional[Callable[[Any], Any]]]] = {}
    
    @classmethod
    def register(cls, type_name: str, factory: Callable[[str, str], Optional[Callable[[Any], Any]]]) -> None:
        cls._transforms[type_name] = factory
    
    @classmethod
    def resolve(cls, name: str, type_spec: str) -> tuple[str, Optional[Callable[[Any], Any]]]:
        """Resolve type spec to (base_type, transform). CC≤3"""
        if ':' not in type_spec:
            return type_spec, cls._default_transform(name, type_spec)
        
        base_type, spec = type_spec.split(':', 1)
        factory = cls._transforms.get(base_type)
        
        if factory:
            transform = factory(name, spec)
        else:
            transform = cls._default_transform(name, spec)
        
        return base_type, transform
    
    @classmethod
    def _default_transform(cls, name: str, spec: str) -> Optional[Callable[[Any], Any]]:
        """Default transform for ID patterns. CC≤2"""
        if 'id' in name.lower() or name.endswith('_id'):
            return lambda v, n=name: f"{n[:3].upper()}-{int(float(v)*10000):06d}"
        return None


def _faker_factory(name: str, spec: str) -> Optional[Callable[[Any], Any]]:
    """Factory for Faker transforms. CC≤2"""
    from fraq.providers.faker_provider import generate_with_faker
    full_spec = f"faker:{spec}"
    return lambda v, fs=full_spec: generate_with_faker(fs, seed=int(float(v) * 10000))


def _float_factory(name: str, spec: str) -> Optional[Callable[[Any], Any]]:
    """Factory for float range transforms. CC≤3"""
    if '-' not in spec:
        return None
    try:
        min_val, max_val = map(float, spec.split('-'))
        return lambda v, min_v=min_val, max_v=max_val: round(min_v + float(v) * (max_v - min_v), 2)
    except ValueError:
        return None


def _int_factory(name: str, spec: str) -> Optional[Callable[[Any], Any]]:
    """Factory for int range transforms. CC≤3"""
    if '-' not in spec:
        return None
    try:
        min_val, max_val = map(float, spec.split('-'))
        return lambda v, min_v=min_val, max_v=max_val: int(min_v + float(v) * (max_v - min_v))
    except ValueError:
        return None


# Register factories
TypeTransformRegistry.register('faker', _faker_factory)
TypeTransformRegistry.register('float', _float_factory)
TypeTransformRegistry.register('int', _int_factory)


def _fields_to_schema(fields: Dict[str, str], seed: Optional[int] = None) -> FraqSchema:
    """Convert field specifications to FraqSchema.
    
    Pure function - no side effects, deterministic.
    Uses TypeTransformRegistry for modular transform resolution.
    """
    root = FraqNode(position=(0.0, 0.0, 0.0), seed=seed or 42)
    schema = FraqSchema(root=root)
    
    for name, type_spec in fields.items():
        base_type, transform = TypeTransformRegistry.resolve(name, type_spec)
        schema.add_field(name, base_type, transform=transform)
    
    return schema


def _parse_transform(name: str, type_spec: str) -> Optional[Callable[[Any], Any]]:
    """Parse type specification and return transform function.
    
    Refactored to use TypeTransformRegistry. CC≤3 (was 10).
    """
    _, transform = TypeTransformRegistry.resolve(name, type_spec)
    return transform


def _generate_records(schema: FraqSchema, count: int) -> Iterator[Dict[str, Any]]:
    """Generate records from schema."""
    yield from schema.records(count=count)


def generate(
    fields: Dict[str, str],
    count: int = 10,
    seed: Optional[int] = None,
    output: DataFrameOutput = "list",
) -> Union[List[Dict[str, Any]], Any]:
    """Generate records with simple field specification.
    
    This is the EASIEST way to create fractal data. No schema setup needed.
    
    Parameters
    ----------
    fields : dict
        Field names and types. Types: 'float', 'int', 'str', 'bool'.
        Can include transform hints: 'temp:float:0-100' for 0-100 range.
        Can use Faker: 'faker:name' for realistic names.
    count : int
        Number of records to generate.
    seed : int, optional
        Random seed for reproducibility.
    output : str
        Output format: 'list' (default), 'polars', 'pandas', 'arrow', 'records'.
        'polars' returns pl.DataFrame, 'pandas' returns pd.DataFrame,
        'arrow' returns pa.Table, 'records' returns iterator.
    
    Returns
    -------
    list[dict] or DataFrame or Table or Iterator
        Generated records in requested format.
    
    Examples
    --------
    >>> records = generate({
    ...     'temp': 'float:10-40',
    ...     'humidity': 'float:0-100',
    ...     'sensor_id': 'str',
    ... }, count=100)
    
    >>> # Export to Polars DataFrame
    >>> df = generate({'temp': 'float:0-100'}, count=1000, output='polars')
    
    >>> # With Faker for realistic data
    >>> df = generate({
    ...     'name': 'faker:name',
    ...     'email': 'faker:email',
    ... }, count=100, output='pandas')
    """
    schema = _fields_to_schema(fields, seed)
    records = list(_generate_records(schema, count))
    
    if output == "list":
        return records
    elif output == "records":
        return iter(records)
    elif output == "polars":
        return _to_polars(records)
    elif output == "pandas":
        return _to_pandas(records)
    elif output == "arrow":
        return _to_arrow(records)
    else:
        raise ValueError(f"Unknown output format: {output}. Use: list, polars, pandas, arrow, records")


@dataclass
class StreamConfig:
    """Configuration for stream()."""
    fields: Dict[str, str]
    count: Optional[int]
    interval: float
    
    def build_schema(self) -> FraqSchema:
        """Build FraqSchema from fields. CC≤3"""
        schema = FraqSchema()
        for name, type_spec in self.fields.items():
            base_type, transform = TypeTransformRegistry.resolve(name, type_spec)
            schema.add_field(name, base_type, transform=transform)
        return schema


def _build_stream_config(
    fields: Optional[Dict[str, str]] = None,
    count: Optional[int] = None,
    interval: float = 0.0,
) -> StreamConfig:
    """Build stream configuration. CC≤2"""
    return StreamConfig(
        fields=fields or {'value': 'float'},
        count=count,
        interval=interval,
    )


def _stream_records(
    schema: FraqSchema,
    config: StreamConfig,
) -> Iterator[Dict[str, Any]]:
    """Generate records with throttling. CC≤4"""
    yielded = 0
    max_records = config.count or float('inf')
    
    for record in schema.records(count=max_records):
        if config.count and yielded >= config.count:
            break
        if config.interval > 0:
            time.sleep(config.interval)
        yielded += 1
        yield record


def stream(
    fields: Optional[Dict[str, str]] = None,
    count: Optional[int] = None,
    interval: float = 0.0,
) -> Iterator[Dict[str, Any]]:
    """Stream records lazily. Like generate() but returns iterator.
    
    Parameters
    ----------
    fields : dict, optional
        Field specification (same as generate()).
    count : int, optional
        Max records (None = infinite).
    interval : float
        Delay between records (for throttling).
    
    Examples
    --------
    >>> for record in stream({'temp': 'float:0-50'}, count=1000):
    ...     process(record)
    """
    config = _build_stream_config(fields, count, interval)
    schema = config.build_schema()
    yield from _stream_records(schema, config)


def quick_schema(*fields: str) -> FraqSchema:
    """Create schema from simple field names. Auto-detects types.
    
    Examples
    --------
    >>> schema = quick_schema('temp', 'humidity', 'pressure')
    >>> records = list(schema.records(count=10))
    
    >>> # With type hints
    >>> schema = quick_schema('temp:float', 'count:int', 'name:str')
    """
    schema = FraqSchema()
    
    for field_spec in fields:
        parts = field_spec.split(':')
        name = parts[0]
        type_name = parts[1] if len(parts) > 1 else 'float'
        
        # Auto-transform for common patterns
        transform = None
        if 'id' in name.lower():
            transform = lambda v, n=name: f"{n[:3].upper()}-{int(float(v)*1000):04d}"
        elif name in ('temp', 'temperature'):
            transform = lambda v: round(10 + float(v) * 30, 1)  # 10-40°C
        elif name in ('humidity', 'humi'):
            transform = lambda v: round(float(v) * 100, 1)  # 0-100%
        
        schema.add_field(name, type_name, transform=transform)
    
    return schema


def _to_polars(records: List[Dict[str, Any]]) -> Any:
    """Convert records to Polars DataFrame.
    
    Lazy import to avoid hard dependency.
    """
    try:
        import polars as pl
    except ImportError:
        raise ImportError(
            "Polars not installed. Install with: pip install fraq[polars]"
        )
    
    if not records:
        return pl.DataFrame()
    
    return pl.DataFrame(records)


def _to_pandas(records: List[Dict[str, Any]]) -> Any:
    """Convert records to Pandas DataFrame.
    
    Lazy import to avoid hard dependency.
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "Pandas not installed. Install with: pip install fraq[pandas]"
        )
    
    if not records:
        return pd.DataFrame()
    
    return pd.DataFrame(records)


def _to_arrow(records: List[Dict[str, Any]]) -> Any:
    """Convert records to PyArrow Table.
    
    Lazy import to avoid hard dependency.
    """
    try:
        import pyarrow as pa
    except ImportError:
        raise ImportError(
            "PyArrow not installed. Install with: pip install fraq[arrow]"
        )
    
    if not records:
        return pa.table({})
    
    # Convert list of dicts to columnar format
    columns = list(records[0].keys())
    data = {col: [r.get(col) for r in records] for col in columns}
    return pa.table(data)


__all__ = [
    'generate',
    'stream',
    'quick_schema',
    '_fields_to_schema',
    '_parse_transform',
    '_generate_records',
    '_to_polars',
    '_to_pandas',
    '_to_arrow',
    'DataFrameOutput',
]
