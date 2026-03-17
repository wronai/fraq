#!/usr/bin/env python3
"""
WebSocket Docker — Uruchomienie i testowanie

Użycie:
    python run.py           # Uruchom przez Docker
    python run.py --local   # Uruchom lokalnie
    python run.py --test    # Przetestuj WebSocket
"""

import argparse
import subprocess
import sys
import asyncio
import websockets
import json


def run_docker():
    """Uruchom przez Docker"""
    print("🐳 Uruchamianie WebSocket w Docker...")
    subprocess.run(["docker-compose", "up", "--build", "-d"], check=True)
    print("\n✅ WebSocket: ws://localhost:8001")


def stop_docker():
    """Zatrzymaj Docker"""
    subprocess.run(["docker-compose", "down"], check=True)
    print("✅ Zatrzymano")


def run_local():
    """Uruchom lokalnie"""
    print("🌀 Uruchamianie lokalnie...")
    try:
        import uvicorn
        from main import app
        uvicorn.run(app, host="0.0.0.0", port=8001)
    except ImportError as e:
        print(f"❌ Błąd: {e}")
        print("Zainstaluj: pip install fraq fastapi uvicorn websockets")
        sys.exit(1)


async def test_websocket():
    """Przetestuj WebSocket"""
    uri = "ws://localhost:8001/ws/stream"
    
    print(f"🧪 Testowanie {uri}...")
    
    try:
        async with websockets.connect(uri) as ws:
            # Test ping
            await ws.send(json.dumps({"action": "ping"}))
            response = await ws.recv()
            print(f"✅ Ping: {response}")
            
            # Test stream
            await ws.send(json.dumps({"action": "stream", "count": 3, "interval": 0.1}))
            for i in range(3):
                response = await ws.recv()
                data = json.loads(response)
                print(f"✅ Stream {i}: value={data.get('value', 'N/A'):.4f}")
                
    except Exception as e:
        print(f"❌ Błąd: {e}")


def main():
    parser = argparse.ArgumentParser(description="WebSocket Docker runner")
    parser.add_argument("--local", action="store_true", help="Uruchom lokalnie")
    parser.add_argument("--stop", action="store_true", help="Zatrzymaj Docker")
    parser.add_argument("--test", action="store_true", help="Przetestuj WebSocket")
    
    args = parser.parse_args()
    
    if args.stop:
        stop_docker()
    elif args.test:
        asyncio.run(test_websocket())
    elif args.local:
        run_local()
    else:
        run_docker()


if __name__ == "__main__":
    main()
