"""Hub type aliases for fraq - improves type clarity in public APIs.

These are NewType aliases that provide semantic meaning to primitive types
without runtime overhead. Use them in function signatures to make
the code more self-documenting.

Example:
    def search_files(pattern: GlobPattern, limit: RecordLimit) -> list[FilePath]:
        ...
"""

from typing import NewType

# File system types
FilePath = NewType("FilePath", str)
GlobPattern = NewType("GlobPattern", str)
FileExtension = NewType("FileExtension", str)

# Format and serialization types
FormatName = NewType("FormatName", str)
MimeType = NewType("MimeType", str)

# Query types
NLQuery = NewType("NLQuery", str)
QueryFilter = NewType("QueryFilter", str)

# Fractal dimension types
ZoomDepth = NewType("ZoomDepth", int)
RecordLimit = NewType("RecordLimit", int)
BranchingFactor = NewType("BranchingFactor", int)
Dimensions = NewType("Dimensions", int)
Seed = NewType("Seed", int)

# Network types
HostAddress = NewType("HostAddress", str)
PortNumber = NewType("PortNumber", int)
NetworkCidr = NewType("NetworkCidr", str)
TimeoutSeconds = NewType("TimeoutSeconds", float)

# Data types
FieldName = NewType("FieldName", str)
SchemaVersion = NewType("SchemaVersion", str)
