"""File search adapter for filesystem queries - refactored with Port/Adapter pattern.

This module separates:
- FileSystemPort: I/O operations (stat, glob, read)
- FileSearchAdapter: Pure business logic (filtering, sorting, limiting)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Protocol, runtime_checkable

from fraq.core import FraqNode
from fraq.formats import FormatRegistry
from fraq.query import SourceType
from fraq.adapters.base import BaseAdapter


@runtime_checkable
class FileSystemPort(Protocol):
    """Port for filesystem I/O operations."""
    
    def stat(self, path: Path) -> Optional[Dict[str, Any]]:
        """Get file stats. Returns None if file doesn't exist or no permission."""
        ...
    
    def list_files(
        self, 
        base_path: Path, 
        pattern: str, 
        recursive: bool
    ) -> Iterator[Path]:
        """List files matching pattern. Yields Path objects."""
        ...
    
    def is_file(self, path: Path) -> bool:
        """Check if path is a file."""
        ...
    
    def write_bytes(self, path: Path, data: bytes) -> None:
        """Write bytes to file."""
        ...


class RealFileSystem(FileSystemPort):
    """Real filesystem implementation of FileSystemPort."""
    
    def stat(self, path: Path) -> Optional[Dict[str, Any]]:
        try:
            st = path.stat()
            return {
                "st_size": st.st_size,
                "st_mtime": st.st_mtime,
                "st_ctime": st.st_ctime,
                "st_ino": st.st_ino,
                "st_nlink": st.st_nlink,
            }
        except (OSError, FileNotFoundError, PermissionError):
            return None
    
    def list_files(
        self, 
        base_path: Path, 
        pattern: str, 
        recursive: bool
    ) -> Iterator[Path]:
        iterator = base_path.rglob(pattern) if recursive else base_path.glob(pattern)
        for path in iterator:
            yield path
    
    def is_file(self, path: Path) -> bool:
        return path.is_file()
    
    def write_bytes(self, path: Path, data: bytes) -> None:
        path.write_bytes(data)


class FileSearchAdapter(BaseAdapter):
    """Adapter for searching files on disk using fractal patterns.
    
    Uses Port/Adapter pattern - all I/O goes through FileSystemPort.
    Business logic is pure and testable without filesystem.
    """

    source_type = SourceType.FILE

    def __init__(
        self,
        base_path: str = ".",
        pattern: str = "*",
        recursive: bool = True,
        fs: Optional[FileSystemPort] = None,
    ):
        self.base_path = Path(base_path).expanduser().resolve()
        self.pattern = pattern
        self.recursive = recursive
        self._fs = fs or RealFileSystem()  # Default to real filesystem

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
        path = Path(uri).expanduser().resolve() if uri else self.base_path
        
        # I/O isolated to FileSystemPort
        stat = self._fs.stat(path)
        
        if stat:
            position = (
                float(stat["st_size"]) if self._fs.is_file(path) else float(stat["st_nlink"]),
                float(stat["st_mtime"]),
                float(stat["st_ctime"]),
            )
            seed = int(stat["st_ino"])
        else:
            position = (0.0, 0.0, 0.0)
            seed = hash(str(path)) % (2**32)

        return FraqNode(
            position=position,
            seed=seed,
            meta={
                "path": str(path),
                "type": "directory" if not self._fs.is_file(path) else "file",
            },
        )

    # -------------------------------------------------------------------------
    # Pure business logic (no I/O)
    # -------------------------------------------------------------------------
    
    def _build_glob(self, extension: Optional[str], pattern: Optional[str]) -> str:
        """Build glob pattern from extension and pattern parameters. Pure logic."""
        search_pattern = pattern or self.pattern
        if extension and not search_pattern.endswith(f".{extension}"):
            search_pattern = f"*.{extension}"
        return search_pattern

    def _file_to_record(
        self, 
        path: Path, 
        stat: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Convert file path and stats to record dict. Pure logic."""
        return {
            "filename": path.name,
            "path": str(path),
            "extension": path.suffix.lstrip(".").lower(),
            "size": stat["st_size"],
            "mtime": stat["st_mtime"],
            "ctime": stat["st_ctime"],
            "depth": len(path.relative_to(self.base_path).parts),
            "fraq_position": (
                float(stat["st_size"]) / (1024 * 1024),
                float(stat["st_mtime"]),
                float(stat["st_ctime"]),
            ),
            "fraq_seed": hash(str(path)) % (2**32),
            "fraq_value": hash(str(path)) / (2**32),
        }

    def _sort_and_limit(
        self,
        files: List[Dict[str, Any]],
        sort_by: str,
        limit: int,
    ) -> List[Dict[str, Any]]:
        """Sort files and apply limit. Pure logic."""
        if sort_by == "mtime":
            files.sort(key=lambda x: x["mtime"], reverse=True)
        elif sort_by == "size":
            files.sort(key=lambda x: x["size"], reverse=True)
        else:
            files.sort(key=lambda x: x["filename"])
        return files[:limit]

    def _filter_by_time(
        self,
        records: List[Dict[str, Any]],
        newer_than: Optional[float],
    ) -> List[Dict[str, Any]]:
        """Filter records by modification time. Pure logic."""
        if newer_than is None:
            return records
        return [r for r in records if r["mtime"] > newer_than]

    # -------------------------------------------------------------------------
    # I/O orchestration (uses FileSystemPort)
    # -------------------------------------------------------------------------

    def _collect_files(
        self,
        glob_pattern: str,
        newer_than: Optional[float],
    ) -> List[Dict[str, Any]]:
        """Iterate filesystem and collect matching files. I/O via FileSystemPort."""
        files: List[Dict[str, Any]] = []
        
        for path in self._fs.list_files(self.base_path, glob_pattern, self.recursive):
            if not self._fs.is_file(path):
                continue
            
            stat = self._fs.stat(path)
            if stat is None:
                continue
            
            # Filter by time before creating record (optimization)
            if newer_than and stat["st_mtime"] <= newer_than:
                continue
            
            record = self._file_to_record(path, stat)
            files.append(record)
        
        return files

    def search(
        self,
        extension: Optional[str] = None,
        pattern: Optional[str] = None,
        limit: int = 10,
        sort_by: str = "name",
        newer_than: Optional[float] = None,
        **opts: Any,
    ) -> List[Dict[str, Any]]:
        """Search files - orchestrates I/O and applies pure logic."""
        search_pattern = self._build_glob(extension, pattern)
        files = self._collect_files(search_pattern, newer_than)
        return self._sort_and_limit(files, sort_by, limit)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        """Save node data to file."""
        if "files" in node.meta:
            data = node.meta["files"]
            output = FormatRegistry.serialize(fmt, data)
            path = Path(uri)
            self._fs.write_bytes(path, output.encode() if isinstance(output, str) else output)
            return str(path)
        return ""

    def stream(
        self,
        extension: Optional[str] = None,
        pattern: Optional[str] = None,
        count: int = 100,
    ) -> Iterator[Dict[str, Any]]:
        """Stream files lazily."""
        search_pattern = pattern or self.pattern
        if extension:
            search_pattern = f"*.{extension}"

        yielded = 0
        for path in self._fs.list_files(self.base_path, search_pattern, self.recursive):
            if not self._fs.is_file(path):
                continue
            
            stat = self._fs.stat(path)
            if stat is None:
                continue
            
            yield {
                "filename": path.name,
                "path": str(path),
                "extension": path.suffix.lstrip(".").lower(),
                "size": stat["st_size"],
                "mtime": stat["st_mtime"],
                "fraq_value": hash(str(path)) / (2**32),
            }
            
            yielded += 1
            if yielded >= count:
                break
