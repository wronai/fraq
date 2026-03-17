#!/usr/bin/env python3
"""
FastAPI Docker — Uruchomienie bez Docker (opcjonalnie)

Użycie:
    python run.py          # Uruchom serwer lokalnie (bez Docker)
    python run.py --docker # Uruchom przez Docker
"""

import argparse
import subprocess
import sys
import os


def run_local():
    """Uruchom serwer lokalnie (bez Docker)"""
    print("🌀 Uruchamianie FastAPI lokalnie...")
    try:
        import uvicorn
        from main import app
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError:
        print("❌ Brakujące zależności. Zainstaluj:")
        print("   pip install fraq fastapi uvicorn")
        sys.exit(1)


def run_docker():
    """Uruchom przez Docker"""
    print("🐳 Uruchamianie przez Docker...")
    subprocess.run(["docker-compose", "up", "--build", "-d"], check=True)
    print("\n✅ Serwer działa na http://localhost:8000")
    print("\nTestuj:")
    print("  curl http://localhost:8000/health")


def stop_docker():
    """Zatrzymaj Docker"""
    print("🛑 Zatrzymywanie Dockera...")
    subprocess.run(["docker-compose", "down"], check=True)
    print("✅ Zatrzymano")


def test_api():
    """Przetestuj API"""
    import requests
    import json
    
    base = "http://localhost:8000"
    
    print("🧪 Testowanie API...")
    
    # Health
    try:
        r = requests.get(f"{base}/health", timeout=5)
        print(f"✅ Health: {r.json()}")
    except Exception as e:
        print(f"❌ Health failed: {e}")
        return
    
    # Files search
    try:
        r = requests.get(f"{base}/files/search?ext=py&limit=3", timeout=10)
        data = r.json()
        print(f"✅ Files search: {data.get('count', 0)} files found")
    except Exception as e:
        print(f"❌ Files search failed: {e}")
    
    # Explore
    try:
        r = requests.get(f"{base}/explore?depth=2", timeout=10)
        data = r.json()
        print(f"✅ Explore: fractal depth={data.get('depth', 'N/A')}")
    except Exception as e:
        print(f"❌ Explore failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="FastAPI + fraq runner")
    parser.add_argument("--docker", action="store_true", help="Użyj Docker")
    parser.add_argument("--stop", action="store_true", help="Zatrzymaj Docker")
    parser.add_argument("--test", action="store_true", help="Przetestuj API")
    
    args = parser.parse_args()
    
    if args.stop:
        stop_docker()
    elif args.test:
        test_api()
    elif args.docker:
        run_docker()
    else:
        run_local()


if __name__ == "__main__":
    main()
