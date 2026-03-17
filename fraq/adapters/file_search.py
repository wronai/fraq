"""File search adapter for filesystem queries."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from fraq.core import FraqNode
from fraq.formats import FormatRegistry
from fraq.query import SourceType
from fraq.adapters.base import BaseAdapter


class FileSearchAdapter(BaseAdapter):
    """Adapter for searching files on disk using fractal patterns."""

    source_type = SourceType.FILE

    def __init__(
        self,
        base_path: str = ".",
        pattern: str = "*",
        recursive: bool = True,
    ):
        self.base_path = Path(base_path).expanduser().resolve()
        self.pattern = pattern
        self.recursive = recursive

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
        path = Path(uri).expanduser().resolve() if uri else self.base_path
        try:
            stat = path.stat()
            position = (
                float(stat.st_size) if path.is_file() else float(stat.st_nlink),
                float(stat.st_mtime),
                float(stat.st_ctime),
            )
            seed = int(stat.st_ino)
        except (OSError, FileNotFoundError):
            position = (0.0, 0.0, 0.0)
            seed = hash(str(path)) % (2**32)

        return FraqNode(
            position=position,
            seed=seed,
            meta={
                "path": str(path),
                "type": "directory" if path.is_dir() else "file",
            },
        )

    def _build_glob(self, extension: Optional[str], pattern: Optional[str]) -> str:
        """Build glob pattern from extension and pattern parameters."""
        search_pattern = pattern or self.pattern
        if extension and not search_pattern.endswith(f".{extension}"):
            search_pattern = f"*.{extension}"
        return search_pattern

    def _collect_files(
        self,
        glob_pattern: str,
        newer_than: Optional[float],
    ) -> List[Dict[str, Any]]:
        """Iterate filesystem and collect matching files."""
        files: List[Dict[str, Any]] = []
        iterator = self.base_path.rglob(glob_pattern) if self.recursive else self.base_path.glob(glob_pattern)

        for path in iterator:
            if not path.is_file():
                continue
            try:
                stat = path.stat()
                mtime = stat.st_mtime
                if newer_than and mtime <= newer_than:
                    continue

                record = {
                    "filename": path.name,
                    "path": str(path),
                    "extension": path.suffix.lstrip(".").lower(),
                    "size": stat.st_size,
                    "mtime": mtime,
                    "ctime": stat.st_ctime,
                    "depth": len(path.relative_to(self.base_path).parts),
                    "fraq_position": (
                        float(stat.st_size) / (1024 * 1024),
                        float(mtime),
                        float(stat.st_ctime),
                    ),
                    "fraq_seed": hash(str(path)) % (2**32),
                    "fraq_value": hash(str(path)) / (2**32),
                }
                files.append(record)
            except (OSError, PermissionError):
                continue
        return files

    def _sort_and_limit(
        self,
        files: List[Dict[str, Any]],
        sort_by: str,
        limit: int,
    ) -> List[Dict[str, Any]]:
        """Sort files and apply limit."""
        if sort_by == "mtime":
            files.sort(key=lambda x: x["mtime"], reverse=True)
        elif sort_by == "size":
            files.sort(key=lambda x: x["size"], reverse=True)
        else:
            files.sort(key=lambda x: x["filename"])
        return files[:limit]

    def search(
        self,
        extension: Optional[str] = None,
        pattern: Optional[str] = None,
        limit: int = 10,
        sort_by: str = "name",
        newer_than: Optional[float] = None,
        **opts: Any,
    ) -> List[Dict[str, Any]]:
        search_pattern = self._build_glob(extension, pattern)
        files = self._collect_files(search_pattern, newer_than)
        return self._sort_and_limit(files, sort_by, limit)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        if "files" in node.meta:
            data = node.meta["files"]
            output = FormatRegistry.serialize(fmt, data)
            path = Path(uri)
            path.write_bytes(output.encode() if isinstance(output, str) else output)
            return str(path)
        return ""

    def stream(
        self,
        extension: Optional[str] = None,
        pattern: Optional[str] = None,
        count: int = 100,
    ) -> Iterator[Dict[str, Any]]:
        search_pattern = pattern or self.pattern
        if extension:
            search_pattern = f"*.{extension}"

        iterator = self.base_path.rglob(search_pattern) if self.recursive else self.base_path.glob(search_pattern)

        yielded = 0
        for path in iterator:
            if not path.is_file():
                continue
            try:
                stat = path.stat()
                yield {
                    "filename": path.name,
                    "path": str(path),
                    "extension": path.suffix.lstrip(".").lower(),
                    "size": stat.st_size,
                    "mtime": stat.st_mtime,
                    "fraq_value": hash(str(path)) / (2**32),
                }
                yielded += 1
                if yielded >= count:
                    break
            except (OSError, PermissionError):
                continue
