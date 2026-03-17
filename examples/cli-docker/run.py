#!/usr/bin/env python3
"""
CLI Docker — Wrapper do uruchamiania fraq CLI w Dockerze

Użycie:
    python run.py files search --ext pdf --limit 10 /data
    python run.py nl "pokaż 10 plików"
    python run.py --local explore --depth 5  # lokalnie, bez Docker
"""

import argparse
import subprocess
import sys
import os


def run_in_docker(args_list):
    """Uruchom fraq CLI w Docker"""
    cmd = ["docker-compose", "run", "--rm", "fraq-cli"] + args_list
    
    print(f"🐳 Docker: {' '.join(cmd)}")
    print("")
    
    result = subprocess.run(cmd)
    return result.returncode


def run_local(args_list):
    """Uruchom fraq CLI lokalnie"""
    cmd = ["fraq"] + args_list
    
    print(f"🌀 Local: {' '.join(cmd)}")
    print("")
    
    result = subprocess.run(cmd)
    return result.returncode


def main():
    # Parsuj argumenty - przekaż wszystko do fraq
    parser = argparse.ArgumentParser(
        description="CLI Docker wrapper",
        add_help=False
    )
    parser.add_argument("--local", action="store_true", help="Uruchom lokalnie (bez Docker)")
    parser.add_argument("--docker", action="store_true", help="Wymuś Docker")
    
    # Znajdź --local/--docker przed przekazaniem reszty
    args, remaining = parser.parse_known_args()
    
    # Jeśli nie ma argumentów, pokaż help
    if not remaining:
        remaining = ["--help"]
    
    # Uruchom
    if args.local:
        return run_local(remaining)
    else:
        return run_in_docker(remaining)


if __name__ == "__main__":
    sys.exit(main())
