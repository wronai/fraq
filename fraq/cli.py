"""
fraq CLI — quick exploration of fractal data from the terminal.

Usage examples:
    fraq explore --dims 3 --depth 5 --format json
    fraq stream  --dims 2 --count 20 --format csv
    fraq schema  --dims 3 --fields name:str,value:float,flag:bool --depth 2
"""

from __future__ import annotations

import argparse
import sys
from typing import List

from fraq.core import FraqCursor, FraqNode, FraqSchema
from fraq.formats import FormatRegistry
from fraq.generators import HashGenerator


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


def main(argv: List[str] | None = None) -> None:
    # Shared arguments via parent parser
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--format", "-f", default="json", choices=FormatRegistry.available())
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

    args = parser.parse_args(argv)

    if args.command == "explore":
        cmd_explore(args)
    elif args.command == "stream":
        cmd_stream(args)
    elif args.command == "schema":
        cmd_schema(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
