"""
fraq - Fractal Query Data Library

Model data as infinite, self-similar fractal structures in hyperspace.
Each zoom level reveals procedurally generated detail — data exists only
virtually and materializes on demand via lazy evaluation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

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

# IFS - Iterated Function System (fractal generator)
from fraq.ifs import (
    IFSGenerator,
    AffineTransform,
    OrganizationalMapper,
    NetworkMapper,
    create_ifs,
)

# NEW: High-level API (moved to api.py for cleaner structure)
from fraq.api import generate, stream, quick_schema

__version__ = "0.2.15"

# Public API list - used for lazy loading and IDE support
__all__ = [
    # Core
    "FraqNode", "FraqSchema", "FraqCursor",
    "FormatRegistry",
    "HashGenerator", "FibonacciGenerator", "PerlinGenerator", "SensorStreamGenerator",
    "FraqQuery", "FraqExecutor", "FraqFilter", "SourceType", "query",
    # IFS - Iterated Function System
    "IFSGenerator", "AffineTransform", "OrganizationalMapper", "NetworkMapper", "create_ifs",
    # Simplified API
    "generate", "stream", "quick_schema",
    # Lazy-loaded from types
    "FilePath", "GlobPattern", "FileExtension",
    "FormatName", "MimeType",
    "NLQuery", "QueryFilter",
    "ZoomDepth", "RecordLimit", "BranchingFactor", "Dimensions", "Seed",
    "HostAddress", "PortNumber", "NetworkCidr", "TimeoutSeconds",
    "FieldName", "SchemaVersion",
    # Lazy-loaded from adapters (core only - Network/WebCrawler moved to optional)
    "FileAdapter", "HTTPAdapter", "SQLAdapter", "SensorAdapter", "HybridAdapter",
    "FileSearchAdapter", "get_adapter",
    # Note: NetworkAdapter and WebCrawlerAdapter available via:
    #   from fraq.adapters import NetworkAdapter, WebCrawlerAdapter
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
    # Note: NetworkAdapter, WebCrawlerAdapter moved to fraq.adapters directly
    "get_adapter": "fraq.adapters",
    # schema_export (now fraq.export)
    "to_nlp2cmd_schema": "fraq.export",
    "to_nlp2cmd_actions": "fraq.export",
    "to_openapi": "fraq.export",
    "to_graphql": "fraq.export",
    "to_asyncapi": "fraq.export",
    "to_proto": "fraq.export",
    "to_json_schema": "fraq.export",
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
    from fraq.export import (
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
