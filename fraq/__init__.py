"""
fraq - Fractal Query Data Library

Model data as infinite, self-similar fractal structures in hyperspace.
Each zoom level reveals procedurally generated detail — data exists only
virtually and materializes on demand via lazy evaluation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator, List, Optional, Dict

# Core modules - no cyclic dependencies
from fraq.core import FraqNode, FraqSchema, FraqCursor
from fraq.formats import FormatRegistry
from fraq.generators import (
    HashGenerator,
    FibonacciGenerator,
    PerlinGenerator,
    SensorStreamGenerator,
)
from fraq.query import FraqQuery, FraqExecutor, FraqFilter, SourceType, query

__version__ = "0.2.11"

# ============================================================================
# NEW: Simplified convenience functions for easier example creation
# ============================================================================

def generate(
    fields: Dict[str, str],
    count: int = 10,
    seed: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Generate records with simple field specification.
    
    This is the EASIEST way to create fractal data. No schema setup needed.
    
    Parameters
    ----------
    fields : dict
        Field names and types. Types: 'float', 'int', 'str', 'bool'.
        Can include transform hints: 'temp:float:0-100' for 0-100 range.
    count : int
        Number of records to generate.
    seed : int, optional
        Random seed for reproducibility.
    
    Returns
    -------
    list[dict]
        Generated records.
    
    Examples
    --------
    >>> # Simple sensor data
    >>> records = generate({
    ...     'temp': 'float',
    ...     'humidity': 'float',
    ...     'sensor_id': 'str',
    ... }, count=100)
    
    >>> # With transforms (range hints)
    >>> records = generate({
    ...     'temp': 'float:10-40',      # 10-40°C range
    ...     'humidity': 'float:0-100',   # 0-100% range
    ...     'id': 'str',
    ... }, count=50)
    """
    root = FraqNode(position=(0.0, 0.0, 0.0), seed=seed or 42)
    schema = FraqSchema(root=root)
    
    for name, type_spec in fields.items():
        # Parse type and optional range
        parts = type_spec.split(':')
        type_name = parts[0]
        
        # Check for range hint (e.g., 'float:10-40')
        transform = None
        if len(parts) >= 2 and '-' in parts[1]:
            range_part = parts[1]
            try:
                min_val, max_val = map(float, range_part.split('-'))
                if type_name == 'float':
                    transform = lambda v, min_v=min_val, max_v=max_val: round(min_v + float(v) * (max_v - min_v), 2)
                elif type_name == 'int':
                    transform = lambda v, min_v=min_val, max_v=max_val: int(min_v + float(v) * (max_v - min_v))
            except ValueError:
                pass  # Invalid range, ignore
        
        # Special handling for ID-like strings
        if type_name == 'str' and ('id' in name.lower() or name.endswith('_id')):
            transform = lambda v, n=name: f"{n[:3].upper()}-{int(float(v)*10000):06d}"
        
        schema.add_field(name, type_name, transform=transform)
    
    return list(schema.records(count=count))


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
    >>> # Stream sensor data
    >>> for record in stream({'temp': 'float:0-50', 'humidity': 'float:0-100'}):
    ...     print(record)
    
    >>> # Limited stream
    >>> for record in stream({'value': 'float'}, count=1000):
    ...     process(record)
    """
    import time
    
    fields = fields or {'value': 'float'}
    schema = FraqSchema()
    
    for name, type_spec in fields.items():
        parts = type_spec.split(':')
        type_name = parts[0]
        
        transform = None
        if len(parts) >= 2 and '-' in parts[1]:
            min_val, max_val = map(float, parts[1].split('-'))
            transform = lambda v, min_v=min_val, max_v=max_val: min_v + float(v) * (max_v - min_v)
        
        schema.add_field(name, type_name, transform=transform)
    
    yielded = 0
    for record in schema.records(count=count or float('inf')):
        if count and yielded >= count:
            break
        if interval > 0:
            time.sleep(interval)
        yielded += 1
        yield record


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


# Public API list - used for lazy loading and IDE support
__all__ = [
    # Core
    "FraqNode", "FraqSchema", "FraqCursor",
    "FormatRegistry",
    "HashGenerator", "FibonacciGenerator", "PerlinGenerator", "SensorStreamGenerator",
    "FraqQuery", "FraqExecutor", "FraqFilter", "SourceType", "query",
    # NEW: Simplified functions
    "generate", "stream", "quick_schema",
    # Lazy-loaded from types
    "FilePath", "GlobPattern", "FileExtension",
    "FormatName", "MimeType",
    "NLQuery", "QueryFilter",
    "ZoomDepth", "RecordLimit", "BranchingFactor", "Dimensions", "Seed",
    "HostAddress", "PortNumber", "NetworkCidr", "TimeoutSeconds",
    "FieldName", "SchemaVersion",
    # Lazy-loaded from adapters
    "FileAdapter", "HTTPAdapter", "SQLAdapter", "SensorAdapter", "HybridAdapter",
    "FileSearchAdapter", "NetworkAdapter", "WebCrawlerAdapter", "get_adapter",
    # Lazy-loaded from schema_export
    "to_nlp2cmd_schema", "to_nlp2cmd_actions",
    "to_openapi", "to_graphql", "to_asyncapi", "to_proto", "to_json_schema",
    # Lazy-loaded from text2fraq
    "Text2Fraq", "Text2FraqSimple", "Text2FraqConfig", "ParsedQuery",
    "text2query", "text2fraq", "FileSearchText2Fraq", "text2filesearch",
]

# Lazy loading registry - maps names to their import paths
_LAZY_IMPORTS: dict[str, str] = {
    # types
    "FilePath": "fraq.types",
    "GlobPattern": "fraq.types",
    "FileExtension": "fraq.types",
    "FormatName": "fraq.types",
    "MimeType": "fraq.types",
    "NLQuery": "fraq.types",
    "QueryFilter": "fraq.types",
    "ZoomDepth": "fraq.types",
    "RecordLimit": "fraq.types",
    "BranchingFactor": "fraq.types",
    "Dimensions": "fraq.types",
    "Seed": "fraq.types",
    "HostAddress": "fraq.types",
    "PortNumber": "fraq.types",
    "NetworkCidr": "fraq.types",
    "TimeoutSeconds": "fraq.types",
    "FieldName": "fraq.types",
    "SchemaVersion": "fraq.types",
    # adapters
    "FileAdapter": "fraq.adapters",
    "HTTPAdapter": "fraq.adapters",
    "SQLAdapter": "fraq.adapters",
    "SensorAdapter": "fraq.adapters",
    "HybridAdapter": "fraq.adapters",
    "FileSearchAdapter": "fraq.adapters",
    "NetworkAdapter": "fraq.adapters",
    "WebCrawlerAdapter": "fraq.adapters",
    "get_adapter": "fraq.adapters",
    # schema_export
    "to_nlp2cmd_schema": "fraq.schema_export",
    "to_nlp2cmd_actions": "fraq.schema_export",
    "to_openapi": "fraq.schema_export",
    "to_graphql": "fraq.schema_export",
    "to_asyncapi": "fraq.schema_export",
    "to_proto": "fraq.schema_export",
    "to_json_schema": "fraq.schema_export",
    # text2fraq
    "Text2Fraq": "fraq.text2fraq",
    "Text2FraqSimple": "fraq.text2fraq",
    "Text2FraqConfig": "fraq.text2fraq",
    "ParsedQuery": "fraq.text2fraq",
    "text2query": "fraq.text2fraq",
    "text2fraq": "fraq.text2fraq",
    "FileSearchText2Fraq": "fraq.text2fraq",
    "text2filesearch": "fraq.text2fraq",
}


def __getattr__(name: str) -> object:
    """Lazy load modules to break circular dependencies."""
    if name in _LAZY_IMPORTS:
        module_path = _LAZY_IMPORTS[name]
        module = __import__(module_path, fromlist=[name])
        return getattr(module, name)
    raise AttributeError(f"module 'fraq' has no attribute '{name}'")


# TYPE_CHECKING imports for IDE autocomplete
if TYPE_CHECKING:
    from fraq.types import (
        FilePath, GlobPattern, FileExtension,
        FormatName, MimeType,
        NLQuery, QueryFilter,
        ZoomDepth, RecordLimit, BranchingFactor, Dimensions, Seed,
        HostAddress, PortNumber, NetworkCidr, TimeoutSeconds,
        FieldName, SchemaVersion,
    )
    from fraq.adapters import (
        FileAdapter,
        HTTPAdapter,
        SQLAdapter,
        SensorAdapter,
        HybridAdapter,
        FileSearchAdapter,
        NetworkAdapter,
        WebCrawlerAdapter,
        get_adapter,
    )
    from fraq.schema_export import (
        to_nlp2cmd_schema,
        to_nlp2cmd_actions,
        to_openapi,
        to_graphql,
        to_asyncapi,
        to_proto,
        to_json_schema,
    )
    from fraq.text2fraq import (
        Text2Fraq,
        Text2FraqSimple,
        Text2FraqConfig,
        ParsedQuery,
        text2query,
        text2fraq,
        FileSearchText2Fraq,
        text2filesearch,
    )
