"""
Schema export for interoperability.

Refactored package - schema_export.py split into focused modules.
"""

from __future__ import annotations

from fraq.export.common import FRAQ_TO_JSON_SCHEMA, FRAQ_TO_PROTO, FRAQ_TO_GRAPHQL
from fraq.export.nlp2cmd import to_nlp2cmd_schema, to_nlp2cmd_actions
from fraq.export.openapi import to_openapi
from fraq.export.graphql import to_graphql
from fraq.export.asyncapi import to_asyncapi
from fraq.export.proto import to_proto
from fraq.export.json_schema import to_json_schema

__all__ = [
    # Type mappings
    'FRAQ_TO_JSON_SCHEMA',
    'FRAQ_TO_PROTO',
    'FRAQ_TO_GRAPHQL',
    # Export functions
    'to_nlp2cmd_schema',
    'to_nlp2cmd_actions',
    'to_openapi',
    'to_graphql',
    'to_asyncapi',
    'to_proto',
    'to_json_schema',
]
