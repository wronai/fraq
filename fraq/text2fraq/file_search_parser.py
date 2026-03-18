"""Natural language file search parser."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, List, Optional, Set

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

    # Patterns that indicate user's home directory
    HOME_PATTERNS: list[str] = [
        "home", "user folder", "user directory", "katalog domowy",
        "folder użytkownika", "folder domowy", "folder usera",
        "w domu", "użytkownika", "usera", "domowy",
        "documents", "downloads", "desktop", "pulpit",
    ]

    # Directories to exclude from search
    EXCLUDED_DIRS: Set[str] = {
        ".venv", "venv", "env", ".env",
        "node_modules", "__pycache__", ".git",
        ".tox", ".pytest_cache", ".mypy_cache",
        "build", "dist", "target", "*.egg-info",
        "site-packages", "lib", "lib64",
    }

    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.adapter: Optional[FileSearchAdapter] = None

    def _detect_path(self, text: str) -> str:
        """Detect if query refers to a specific location."""
        text_lower = text.lower()
        if any(pattern in text_lower for pattern in self.HOME_PATTERNS):
            return str(Path.home())
        return self.base_path

    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded from search."""
        for part in path.parts:
            if part in self.EXCLUDED_DIRS:
                return True
            # Handle wildcards like *.egg-info
            for excluded in self.EXCLUDED_DIRS:
                if excluded.startswith("*") and part.endswith(excluded[1:]):
                    return True
        return False

    def _collect_files(
        self,
        base_path: str,
        extension: Optional[str],
    ) -> List[Path]:
        """Collect raw file paths with exclusion filtering. CC≤4"""
        path = Path(base_path).expanduser().resolve()
        pattern = f"*.{extension}" if extension else "*"
        
        files: List[Path] = []
        try:
            for file_path in path.rglob(pattern):
                if not file_path.is_file():
                    continue
                if self._should_exclude(file_path):
                    continue
                files.append(file_path)
        except (OSError, PermissionError):
            pass
        return files

    def _apply_filters(
        self,
        files: List[Path],
        base_path: Path,
        newer_than: Optional[float],
    ) -> List[dict[str, Any]]:
        """Apply date filters and build file info. CC≤3"""
        result: List[dict[str, Any]] = []
        for file_path in files:
            try:
                stat = file_path.stat()
                mtime = stat.st_mtime
                if newer_than and mtime <= newer_than:
                    continue
                
                result.append({
                    "filename": file_path.name,
                    "path": str(file_path),
                    "extension": file_path.suffix.lstrip(".").lower(),
                    "size": stat.st_size,
                    "mtime": mtime,
                    "ctime": stat.st_ctime,
                    "depth": len(file_path.relative_to(base_path).parts),
                    "fraq_position": (
                        float(stat.st_size) / (1024 * 1024),
                        float(mtime),
                        float(stat.st_ctime),
                    ),
                    "fraq_seed": hash(str(file_path)) % (2**32),
                    "fraq_value": hash(str(file_path)) / (2**32),
                })
            except (OSError, PermissionError):
                continue
        return result

    def _sort_and_limit(
        self,
        files: List[dict[str, Any]],
        sort_by: str,
        limit: int,
    ) -> List[dict[str, Any]]:
        """Sort and limit results. CC≤3"""
        if sort_by == "mtime":
            files.sort(key=lambda x: x["mtime"], reverse=True)
        elif sort_by == "size":
            files.sort(key=lambda x: x["size"], reverse=True)
        else:
            files.sort(key=lambda x: x["filename"])
        return files[:limit]

    def _collect_files_filtered(
        self,
        base_path: str,
        extension: Optional[str],
        limit: int,
        sort_by: str,
        newer_than: Optional[float],
    ) -> List[dict[str, Any]]:
        """Orchestrate: collect → filter → sort/limit. CC≤3"""
        path = Path(base_path).expanduser().resolve()
        
        # Step 1: Collect
        raw_files = self._collect_files(base_path, extension)
        
        # Step 2: Apply filters
        filtered = self._apply_filters(raw_files, path, newer_than)
        
        # Step 3: Sort and limit
        return self._sort_and_limit(filtered, sort_by, limit)

    def parse(self, text: str) -> dict[str, Any]:
        """Parse natural language file query to search parameters."""
        text_lower = text.lower()
        return {
            "extension": self._detect_extension(text_lower),
            "limit": self._detect_limit(text_lower),
            "newer_than": self._detect_newer_than(text_lower),
            "sort_by": self._detect_sort_by(text_lower),
            "path": self._detect_path(text_lower),
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
        params = self.parse(text)
        # Use injected adapter if available (for testing), otherwise use default
        if self.adapter is not None:
            return self.adapter.search(
                extension=params["extension"],
                limit=params["limit"],
                sort_by=params["sort_by"],
            )
        return self._collect_files_filtered(
            base_path=params["path"],
            extension=params["extension"],
            limit=params["limit"],
            sort_by=params["sort_by"],
            newer_than=params["newer_than"],
        )

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
