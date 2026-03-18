"""
Protobuf / gRPC schema export.

Generate .proto file from FraqSchema.
"""

from __future__ import annotations

from fraq.core import FraqSchema
from fraq.export.common import FRAQ_TO_PROTO


def to_proto(
    schema: FraqSchema,
    package: str = "fraq",
    message_name: str = "FraqRecord",
) -> str:
    """Generate a .proto file."""
    lines = [
        'syntax = "proto3";',
        f"package {package};",
        "",
        f"message {message_name} {{",
    ]
    for i, f in enumerate(schema.fields, start=1):
        proto_type = FRAQ_TO_PROTO.get(f.type, "string")
        lines.append(f"  {proto_type} {f.name} = {i};")
    lines.append("}")

    lines.append("")
    lines.append("message ZoomRequest {")
    lines.append("  int32 depth = 1;")
    lines.append("  repeated double direction = 2;")
    lines.append("  string format = 3;")
    lines.append("  int32 limit = 4;")
    lines.append("}")

    lines.append("")
    lines.append("message ZoomResponse {")
    lines.append(f"  repeated {message_name} records = 1;")
    lines.append("  int32 total = 2;")
    lines.append("}")

    lines.append("")
    lines.append("message StreamRequest {")
    lines.append("  int32 count = 1;")
    lines.append("  repeated double direction = 2;")
    lines.append("}")

    lines.append("")
    lines.append(f"service FraqService {{")
    lines.append(f"  rpc Zoom(ZoomRequest) returns (ZoomResponse);")
    lines.append(f"  rpc Stream(StreamRequest) returns (stream {message_name});")
    lines.append("}")

    return "\n".join(lines)
