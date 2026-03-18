"""
Schema export for interoperability.

.. deprecated::
    fraq.schema_export is deprecated, use fraq.export instead.
"""

from __future__ import annotations

import warnings

warnings.warn(
    "fraq.schema_export is deprecated, use fraq.export instead",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new package
from fraq.export import (
    to_nlp2cmd_schema,
    to_nlp2cmd_actions,
    to_openapi,
    to_graphql,
    to_asyncapi,
    to_proto,
    to_json_schema,
    FRAQ_TO_JSON_SCHEMA,
    FRAQ_TO_PROTO,
    FRAQ_TO_GRAPHQL,
)

__all__ = [
    "to_nlp2cmd_schema",
    "to_nlp2cmd_actions",
    "to_openapi",
    "to_graphql",
    "to_asyncapi",
    "to_proto",
    "to_json_schema",
    "FRAQ_TO_JSON_SCHEMA",
    "FRAQ_TO_PROTO",
    "FRAQ_TO_GRAPHQL",
]
