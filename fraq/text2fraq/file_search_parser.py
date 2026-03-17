"""Natural language file search parser."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Any, List, Optional

from fraq.formats import FormatRegistry
from fraq.adapters.file_search import FileSearchAdapter


_FILE_LIMIT_PATTERN = re.compile(r"(\d+)\s*(files?|documents?|items?)?")


class FileSearchText2Fraq:
    """Natural language to file search converter."""

    FILE_PATTERNS: dict[str, list[str]] = {
        "pdf": ["pdf", "acpdf", "portable document"],
        "txt": ["txt", "text", "plain text"],
        "csv": ["csv", "comma separated"],
        "json": ["json", "javascript object"],
        "yaml": ["yaml", "yml"],
        "docx": ["docx", "word", "microsoft word"],
        "xlsx": ["xlsx", "excel", "spreadsheet"],
        "py": ["py", "python", "python script"],
        "js": ["js", "javascript"],
        "ts": ["ts", "typescript"],
        "html": ["html", "htm", "web page"],
        "xml": ["xml"],
        "zip": ["zip", "archive"],
        "png": ["png", "image", "picture"],
        "jpg": ["jpg", "jpeg", "image", "picture"],
        "md": ["md", "markdown", "documentation"],
    }

    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.adapter = FileSearchAdapter(base_path=base_path, recursive=True)

    def parse(self, text: str) -> dict[str, Any]:
        """Parse natural language file query to search parameters."""
        text_lower = text.lower()
        return {
            "extension": self._detect_extension(text_lower),
            "limit": self._detect_limit(text_lower),
            "newer_than": self._detect_newer_than(text_lower),
            "sort_by": self._detect_sort_by(text_lower),
        }

    def _detect_extension(self, text: str) -> Optional[str]:
        for extension, patterns in self.FILE_PATTERNS.items():
            if any(pattern in text for pattern in patterns):
                return extension
        return None

    def _detect_limit(self, text: str) -> int:
        match = _FILE_LIMIT_PATTERN.search(text)
        return int(match.group(1)) if match else 10

    def _detect_newer_than(self, text: str) -> Optional[float]:
        if "today" in text or "recent" in text:
            return (datetime.now() - timedelta(days=1)).timestamp()
        if "week" in text or "last week" in text:
            return (datetime.now() - timedelta(days=7)).timestamp()
        if "month" in text:
            return (datetime.now() - timedelta(days=30)).timestamp()
        return None

    def _detect_sort_by(self, text: str) -> str:
        if "name" in text or "alphabetical" in text:
            return "name"
        if "size" in text or "largest" in text:
            return "size"
        return "mtime"

    def search(self, text: str) -> List[dict[str, Any]]:
        """Parse query and execute file search."""
        return self.adapter.search(**self.parse(text))

    def format_results(
        self,
        results: List[dict[str, Any]],
        fmt: str = "json",
        fields: Optional[List[str]] = None,
    ) -> str:
        """Format file search results to specified format."""
        if fields:
            results = [{key: record.get(key) for key in fields if key in record} for record in results]
        return FormatRegistry.serialize(fmt, results)
