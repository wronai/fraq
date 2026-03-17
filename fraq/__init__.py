"""
fraq - Fractal Query Data Library

Model data as infinite, self-similar fractal structures in hyperspace.
Each zoom level reveals procedurally generated detail — data exists only
virtually and materializes on demand via lazy evaluation.
"""

from fraq.core import FraqNode, FraqSchema, FraqCursor
from fraq.formats import FormatRegistry
from fraq.generators import (
    HashGenerator,
    FibonacciGenerator,
    PerlinGenerator,
    SensorStreamGenerator,
)
from fraq.query import FraqQuery, FraqExecutor, FraqFilter, SourceType, query
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

__version__ = "0.2.5"
__all__ = [
    "FraqNode", "FraqSchema", "FraqCursor",
    "FormatRegistry",
    "HashGenerator", "FibonacciGenerator", "PerlinGenerator", "SensorStreamGenerator",
    "FraqQuery", "FraqExecutor", "FraqFilter", "SourceType", "query",
    "FileAdapter", "HTTPAdapter", "SQLAdapter", "SensorAdapter", "HybridAdapter", "FileSearchAdapter",
    "NetworkAdapter", "WebCrawlerAdapter",
    "get_adapter",
    "to_nlp2cmd_schema", "to_nlp2cmd_actions",
    "to_openapi", "to_graphql", "to_asyncapi", "to_proto", "to_json_schema",
    "Text2Fraq", "Text2FraqSimple", "Text2FraqConfig", "ParsedQuery", "text2query", "text2fraq",
    "FileSearchText2Fraq", "text2filesearch",
]
