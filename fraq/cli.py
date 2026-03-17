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
    if _is_file_query(args.query):
        _run_nl_file_query(args.query, args.path or ".", args.format)
        return
    _run_nl_fraq_query(args.query, args.format)


def _is_file_query(query: str) -> bool:
    file_keywords = [
        "file", "files", "pdf", "txt", "document", "folder", "directory",
        "plik", "pliki", "plików", "najnowszych", "dokument", "folder", "katalog",
        "pokaż", "znajdź", "lista", "wyświetl", "ostatnio", "utworzone",
    ]
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in file_keywords)


def _run_nl_file_query(query: str, base_path: str, fmt: str) -> None:
    from fraq.text2fraq import FileSearchText2Fraq

    searcher = FileSearchText2Fraq(base_path)
    results = searcher.search(query)
    print(searcher.format_results(results, fmt))


def _run_nl_fraq_query(query: str, fmt: str) -> None:
    from fraq.text2fraq import Text2Fraq, Text2FraqConfig

    config = Text2FraqConfig.from_env()
    result = Text2Fraq(config).execute(query)
    if isinstance(result, str):
        print(result)
    else:
        print(FormatRegistry.serialize(fmt, result))


def cmd_network_scan(args: argparse.Namespace) -> None:
    """Scan network for devices."""
    from fraq import NetworkAdapter
    
    ports = [int(p.strip()) for p in args.ports.split(",")]
    adapter = NetworkAdapter(
        network=args.network,
        ports=ports,
        timeout=args.timeout,
    )
    
    print(f"🔍 Scanning network {args.network}...")
    print(f"   Ports: {ports}")
    print(f"   Timeout: {args.timeout}s")
    print()
    
    results = adapter.search(limit=args.limit)
    
    if not results:
        print("No devices found.")
        return
    
    if args.format == "table":
        print(f"{'IP':<16} {'Port':<6} {'Service':<15} {'Latency':<10} {'fraq_value'}")
        print("-" * 60)
        for device in results:
            print(f"{device['ip']:<16} {device['port']:<6} {device['service']:<15} "
                  f"{device['latency_ms']:<10} {device['fraq_value']:.6f}")
    elif args.format == "json":
        import json
        print(json.dumps(results, indent=2))
    elif args.format == "csv":
        print("ip,port,service,latency_ms,fraq_value")
        for device in results:
            print(f"{device['ip']},{device['port']},{device['service']},"
                  f"{device['latency_ms']},{device['fraq_value']}")
    
    print(f"\nFound {len(results)} open ports.")


def cmd_web_crawl(args: argparse.Namespace) -> None:
    """Crawl website."""
    from fraq import WebCrawlerAdapter
    
    adapter = WebCrawlerAdapter(
        base_url=args.url,
        max_depth=args.depth,
        max_pages=args.max_pages,
        timeout=args.timeout,
    )
    
    print(f"🕷️  Crawling {args.url}...")
    print(f"   Max depth: {args.depth}")
    print(f"   Max pages: {args.max_pages}")
    print()
    
    results = adapter.search()
    
    if not results:
        print("No pages found.")
        return
    
    if args.format == "table":
        print(f"{'URL':<50} {'Title':<30} {'Depth':<6} {'Size'}")
        print("-" * 100)
        for page in results:
            title = page.get('title', 'N/A')[:30]
            print(f"{page['url']:<50} {title:<30} {page['depth']:<6} {page['size_bytes']}")
    elif args.format == "json":
        import json
        print(json.dumps(results, indent=2))
    elif args.format == "csv":
        print("url,title,depth,size_bytes")
        for page in results:
            title = page.get('title', '').replace(',', ' ')
            print(f"{page['url']},{title},{page['depth']},{page['size_bytes']}")
    
    print(f"\nCrawled {len(results)} pages.")


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

    # Network subcommand
    p_network = sub.add_parser("network", help="Network scanning operations")
    network_sub = p_network.add_subparsers(dest="network_command")
    
    # network scan
    p_network_scan = network_sub.add_parser("scan", help="Scan network for devices")
    p_network_scan.add_argument("--network", "-n", default="192.168.1.0/24",
                                help="Network CIDR (e.g., 192.168.1.0/24)")
    p_network_scan.add_argument("--ports", "-p", default="80,443,22",
                                help="Comma-separated ports to scan")
    p_network_scan.add_argument("--timeout", "-t", type=float, default=1.0,
                                help="Connection timeout in seconds")
    p_network_scan.add_argument("--limit", "-l", type=int, default=100,
                                help="Max hosts to scan")
    p_network_scan.add_argument("--format", "-f", default="table",
                                choices=["table", "json", "csv"])
    
    # Web subcommand
    p_web = sub.add_parser("web", help="Web crawling operations")
    web_sub = p_web.add_subparsers(dest="web_command")
    
    # web crawl
    p_web_crawl = web_sub.add_parser("crawl", help="Crawl website")
    p_web_crawl.add_argument("url", help="Base URL to crawl")
    p_web_crawl.add_argument("--depth", "-d", type=int, default=2,
                             help="Max crawl depth")
    p_web_crawl.add_argument("--max-pages", "-n", type=int, default=50,
                             help="Max pages to crawl")
    p_web_crawl.add_argument("--timeout", "-t", type=float, default=10.0,
                             help="Request timeout")
    p_web_crawl.add_argument("--format", "-f", default="table",
                             choices=["table", "json", "csv"])

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
    elif args.command == "network":
        if args.network_command == "scan":
            cmd_network_scan(args)
        else:
            p_network.print_help()
            sys.exit(1)
    elif args.command == "web":
        if args.web_command == "crawl":
            cmd_web_crawl(args)
        else:
            p_web.print_help()
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
