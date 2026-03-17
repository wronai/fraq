#!/usr/bin/env python3
"""
Fullstack Docker — Uruchomienie i zarządzanie stackiem

Użycie:
    python run.py           # Uruchom stack
    python run.py --test    # Przetestuj
    python run.py --stop    # Zatrzymaj
    python run.py --local   # Uruchom lokalnie (bez Docker)
"""

import argparse
import subprocess
import sys
import time


def run_docker():
    """Uruchom przez Docker Compose"""
    print("🐳 Uruchamianie stacku...")
    subprocess.run(["docker-compose", "up", "--build", "-d"], check=True)
    print("\n✅ Stack działa:")
    print("  API:       http://localhost:8000")
    print("  WebSocket: ws://localhost:8001")
    print("  Frontend:  http://localhost:8501")


def stop_docker():
    """Zatrzymaj stack"""
    print("🛑 Zatrzymywanie...")
    subprocess.run(["docker-compose", "down"], check=True)
    print("✅ Zatrzymano")


def test_stack():
    """Przetestuj stack"""
    import requests
    
    print("🧪 Testowanie...")
    time.sleep(2)
    
    # Test API
    try:
        r = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ API: {r.json()}")
    except Exception as e:
        print(f"❌ API: {e}")
    
    # Test Frontend
    try:
        r = requests.get("http://localhost:8501", timeout=5)
        print(f"✅ Frontend: HTTP {r.status_code}")
    except Exception as e:
        print(f"❌ Frontend: {e}")


def main():
    parser = argparse.ArgumentParser(description="Fullstack Docker runner")
    parser.add_argument("--stop", action="store_true", help="Zatrzymaj")
    parser.add_argument("--test", action="store_true", help="Przetestuj")
    parser.add_argument("--logs", action="store_true", help="Pokaż logi")
    
    args = parser.parse_args()
    
    if args.stop:
        stop_docker()
    elif args.test:
        test_stack()
    elif args.logs:
        subprocess.run(["docker-compose", "logs", "-f"])
    else:
        run_docker()


if __name__ == "__main__":
    main()
