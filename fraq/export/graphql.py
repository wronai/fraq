"""
GraphQL schema export.

Generate GraphQL type definitions from FraqSchema.
"""

from __future__ import annotations

from fraq.core import FraqSchema
from fraq.export.common import FRAQ_TO_GRAPHQL


def to_graphql(schema: FraqSchema, type_name: str = "FraqRecord") -> str:
    """Generate a GraphQL schema definition."""
    lines = [f"type {type_name} {{"]
    for f in schema.fields:
        gql_type = FRAQ_TO_GRAPHQL.get(f.type, "String")
        lines.append(f"  {f.name}: {gql_type}!")
    lines.append("}")

    lines.append("")
    lines.append("type FraqNode {")
    lines.append("  value: Float!")
    lines.append("  depth: Int!")
    lines.append("  position: [Float!]!")
    lines.append(f"  children: [{type_name}!]")
    lines.append("}")

    lines.append("")
    lines.append("type Query {")
    lines.append(f"  zoom(depth: Int!, direction: [Float!]): FraqNode!")
    lines.append(f"  query(depth: Int, fields: [String!], limit: Int): [{type_name}!]!")
    lines.append(f"  stream(count: Int!, direction: [Float!]): [{type_name}!]!")
    lines.append("}")

    return "\n".join(lines)
