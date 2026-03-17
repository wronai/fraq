"""
fraq CLI — quick exploration of fractal data from the terminal.

Usage examples:
    fraq explore --dims 3 --depth 5 --format json
    fraq stream  --dims 2 --count 20 --format csv
    fraq schema  --dims 3 --fields name:str,value:float,flag:bool --depth 2
    fraq files search --ext pdf --limit 10 --sort mtime ~/Documents
    fraq files list --pattern "*.py" --format csv .
    fraq files stat /path/to/file
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List

from fraq.core import FraqCursor, FraqNode, FraqSchema
from fraq.formats import FormatRegistry
from fraq.generators import HashGenerator
from fraq.adapters import FileSearchAdapter


def _make_root(dims: int, seed: int = 0) -> FraqNode:
    pos = tuple(0.0 for _ in range(dims))
    return FraqNode(position=pos, seed=seed, generator=HashGenerator())


def cmd_explore(args: argparse.Namespace) -> None:
    root = _make_root(args.dims, args.seed)
    node = root.zoom(steps=args.depth)
    data = node.to_dict(max_depth=1)
    print(FormatRegistry.serialize(args.format, data))


def cmd_stream(args: argparse.Namespace) -> None:
    root = _make_root(args.dims, args.seed)
    cursor = FraqCursor(root=root)
    records: List[dict] = []
    for _ in range(args.count):
        cursor.advance()
        records.append(cursor.current.to_dict())
    print(FormatRegistry.serialize(args.format, records))


def cmd_schema(args: argparse.Namespace) -> None:
    root = _make_root(args.dims, args.seed)
    schema = FraqSchema(root=root)
    for spec in args.fields.split(","):
        name, _, typ = spec.partition(":")
        schema.add_field(name.strip(), typ.strip() or "float")
    records = list(schema.records(depth=args.depth, branching=args.branching))
    print(FormatRegistry.serialize(args.format, records))


# ---------------------------------------------------------------------------
# File commands
# ---------------------------------------------------------------------------

def cmd_files_search(args: argparse.Namespace) -> None:
    """Search files with natural language or explicit parameters."""
    adapter = FileSearchAdapter(
        base_path=args.path,
        pattern=args.pattern or "*",
        recursive=not args.no_recursive,
    )
    
    results = adapter.search(
        extension=args.ext,
        pattern=args.pattern,
        limit=args.limit,
        sort_by=args.sort,
    )
    
    # Format output
    if args.format == "table":
        # Human-readable table
        print(f"{'Filename':<40} {'Size':>10} {'Modified':>20}")
        print("-" * 72)
        for r in results:
            mtime_str = datetime.fromtimestamp(r['mtime']).strftime('%Y-%m-%d %H:%M')
            size_str = f"{r['size']:,} B" if r['size'] < 1024 else f"{r['size']/1024:.1f} KB"
            print(f"{r['filename']:<40} {size_str:>10} {mtime_str:>20}")
        print(f"\nTotal: {len(results)} files")
    else:
        print(FormatRegistry.serialize(args.format, results))


def cmd_files_list(args: argparse.Namespace) -> None:
    """List files in directory (ls-like)."""
    adapter = FileSearchAdapter(
        base_path=args.path,
        pattern=args.pattern or "*",
        recursive=args.recursive,
    )
    
    results = adapter.search(
        extension=args.ext,
        pattern=args.pattern,
        limit=args.limit,
        sort_by=args.sort,
    )
    
    if args.long:
        # ls -l style
        for r in results:
            mtime_str = datetime.fromtimestamp(r['mtime']).strftime('%b %d %H:%M')
            size_str = f"{r['size']:>10,}"
            print(f"{size_str} {mtime_str} {r['path']}")
    else:
        for r in results:
            print(r['filename'])


def cmd_files_stat(args: argparse.Namespace) -> None:
    """Show file statistics with fractal coordinates."""
    path = Path(args.file).expanduser().resolve()
    
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    
    stat = path.stat()
    
    # Create fractal representation
    record = {
        "filename": path.name,
        "path": str(path),
        "extension": path.suffix.lstrip(".").lower() if path.suffix else "",
        "size": stat.st_size,
        "mtime": stat.st_mtime,
        "ctime": stat.st_ctime,
        "atime": stat.st_atime,
        "fraq_position": (
            float(stat.st_size) / (1024 * 1024),
            float(stat.st_mtime),
            float(stat.st_ctime),
        ),
        "fraq_seed": hash(str(path)) % (2**32),
        "fraq_value": hash(str(path)) / (2**32),
    }
    
    if args.format == "json":
        import json
        print(json.dumps(record, indent=2))
    else:
        print(f"File: {record['path']}")
        print(f"Size: {record['size']:,} bytes ({record['size']/1024:.2f} KB)")
        print(f"Modified: {datetime.fromtimestamp(record['mtime'])}")
        print(f"Fractal seed: {record['fraq_seed']}")
        print(f"Fractal value: {record['fraq_value']:.6f}")


def cmd_nl(args: argparse.Namespace) -> None:
    """Natural language query (requires LLM)."""
    from fraq.text2fraq import Text2Fraq, Text2FraqConfig
    
    config = Text2FraqConfig.from_env()
    t2f = Text2Fraq(config)
    
    # Check if it's a file query (English + Polish keywords)
    file_keywords = [
        # English
        "file", "files", "pdf", "txt", "document", "folder", "directory",
        # Polish
        "plik", "pliki", "plików", "najnowszych", "dokument", "folder", "katalog",
        "pokaż", "znajdź", "lista", "wyświetl", "ostatnio", "utworzone",
    ]
    is_file_query = any(kw in args.query.lower() for kw in file_keywords)
    
    if is_file_query:
        from fraq.text2fraq import FileSearchText2Fraq
        searcher = FileSearchText2Fraq(args.path or ".")
        results = searcher.search(args.query)
        print(searcher.format_results(results, args.format))
    else:
        # Regular fraq query
        result = t2f.execute(args.query)
        if isinstance(result, str):
            print(result)
        else:
            print(FormatRegistry.serialize(args.format, result))


def main(argv: List[str] | None = None) -> None:
    # Shared arguments via parent parser
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--format", "-f", default="json", choices=[*FormatRegistry.available(), "table"])
    shared.add_argument("--dims", "-d", type=int, default=3, help="Hyperspace dimensions")
    shared.add_argument("--seed", "-s", type=int, default=0, help="Root seed")

    parser = argparse.ArgumentParser(prog="fraq", description="Fractal Query Data Library CLI")
    sub = parser.add_subparsers(dest="command")

    p_explore = sub.add_parser("explore", parents=[shared], help="Zoom into the fractal")
    p_explore.add_argument("--depth", type=int, default=3)

    p_stream = sub.add_parser("stream", parents=[shared], help="Stream cursor records")
    p_stream.add_argument("--count", "-n", type=int, default=10)

    p_schema = sub.add_parser("schema", parents=[shared], help="Generate typed records")
    p_schema.add_argument("--fields", required=True, help="Comma-separated name:type pairs")
    p_schema.add_argument("--depth", type=int, default=1)
    p_schema.add_argument("--branching", type=int, default=4)
    
    # Natural language command
    p_nl = sub.add_parser("nl", parents=[shared], help="Natural language query")
    p_nl.add_argument("query", help="Natural language query string")
    p_nl.add_argument("--path", "-p", default=".", help="Base path for file searches")

    # Files subcommand
    p_files = sub.add_parser("files", help="File system operations via fractal queries")
    files_sub = p_files.add_subparsers(dest="files_command")
    
    # files search
    p_files_search = files_sub.add_parser("search", parents=[shared], help="Search files")
    p_files_search.add_argument("path", nargs="?", default=".", help="Directory to search")
    p_files_search.add_argument("--ext", "-e", help="File extension (pdf, txt, py...)")
    p_files_search.add_argument("--pattern", "-p", help="Glob pattern (*.pdf, data*)")
    p_files_search.add_argument("--limit", "-n", type=int, default=10, help="Max results")
    p_files_search.add_argument("--sort", default="mtime", 
                                choices=["name", "mtime", "size"],
                                help="Sort order")
    p_files_search.add_argument("--no-recursive", action="store_true", 
                                help="Don't search subdirectories")
    
    # files list
    p_files_list = files_sub.add_parser("list", help="List files (ls-style)")
    p_files_list.add_argument("path", nargs="?", default=".", help="Directory to list")
    p_files_list.add_argument("--ext", "-e", help="Filter by extension")
    p_files_list.add_argument("--pattern", "-p", help="Glob pattern")
    p_files_list.add_argument("--limit", "-n", type=int, default=50)
    p_files_list.add_argument("--sort", "-s", default="name", choices=["name", "mtime", "size"])
    p_files_list.add_argument("--recursive", "-r", action="store_true", help="List recursively")
    p_files_list.add_argument("--long", "-l", action="store_true", help="Long format")
    p_files_list.add_argument("--format", "-f", default="text", 
                              choices=["text", "json", "csv", "yaml"])
    
    # files stat
    p_files_stat = files_sub.add_parser("stat", help="Show file statistics")
    p_files_stat.add_argument("file", help="File path")
    p_files_stat.add_argument("--format", "-f", default="human", 
                               choices=["human", "json"])

    args = parser.parse_args(argv)

    if args.command == "explore":
        cmd_explore(args)
    elif args.command == "stream":
        cmd_stream(args)
    elif args.command == "schema":
        cmd_schema(args)
    elif args.command == "nl":
        cmd_nl(args)
    elif args.command == "files":
        if args.files_command == "search":
            cmd_files_search(args)
        elif args.files_command == "list":
            cmd_files_list(args)
        elif args.files_command == "stat":
            cmd_files_stat(args)
        else:
            p_files.print_help()
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
