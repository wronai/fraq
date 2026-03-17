#!/usr/bin/env python3
"""
Przykłady użycia NetworkAdapter i WebCrawlerAdapter

NetworkAdapter - skanowanie sieci LAN
WebCrawlerAdapter - crawling stron WWW
"""

import asyncio
from fraq import NetworkAdapter, WebCrawlerAdapter


def example_network_scan_sync():
    """Przykład 1: Synchroniczne skanowanie sieci"""
    print("=" * 60)
    print("1. SYNCHRONICZNE SKANOWANIE SIECI")
    print("=" * 60)
    
    # Stwórz adapter dla sieci 192.168.1.0/24
    adapter = NetworkAdapter(
        network="192.168.1.0/24",
        ports=[80, 443, 22, 8080],
        timeout=1.0,
        max_concurrent=50,
    )
    
    print(f"Skanowanie: {adapter.network}")
    print(f"Porty: {adapter.ports}")
    print(f"Hostów w sieci: {adapter.network.num_addresses - 2}")
    print()
    
    # Synchroniczne skanowanie
    results = adapter.search(limit=50)
    
    print(f"Znaleziono {len(results)} otwartych portów:")
    for device in results[:10]:  # Pokaż pierwsze 10
        print(f"  {device['ip']}:{device['port']} ({device['service']}) - {device['latency_ms']}ms")
        print(f"    fraq_value: {device['fraq_value']:.6f}")
    print()


async def example_network_scan_async():
    """Przykład 2: Asynchroniczne skanowanie ze streamingiem"""
    print("=" * 60)
    print("2. ASYNCHRONICZNE SKANOWANIE ZE STREAMINGIEM")
    print("=" * 60)
    
    adapter = NetworkAdapter(
        network="127.0.0.1/24",  # Localhost dla testów
        ports=[8000, 8001, 22],
        timeout=0.5,
    )
    
    print("Streamowanie wyników w czasie rzeczywistym:")
    count = 0
    async for device in adapter.stream_devices():
        print(f"  🔍 {device['ip']}:{device['port']} ({device['service']})")
        count += 1
        if count >= 5:  # Zatrzymaj po 5 znaleziskach
            break
    print(f"\nZnaleziono {count} urządzeń\n")


def example_web_crawl_sync():
    """Przykład 3: Synchroniczny crawling strony"""
    print("=" * 60)
    print("3. SYNCHRONICZNY CRAWLING STRONY")
    print("=" * 60)
    
    # Stwórz adapter dla crawlowania
    adapter = WebCrawlerAdapter(
        base_url="https://httpbin.org",  # Testowa strona
        max_depth=1,
        max_pages=10,
        timeout=10.0,
    )
    
    print(f"Crawlowanie: {adapter.base_url}")
    print(f"Max głębokość: {adapter.max_depth}")
    print()
    
    # Synchroniczne crawlowanie
    results = adapter.search()
    
    print(f"Znaleziono {len(results)} stron:")
    for page in results:
        print(f"  📄 {page['url']}")
        print(f"     Tytuł: {page.get('title', 'N/A')[:50]}")
        print(f"     Głębokość: {page['depth']}, Rozmiar: {page['size_bytes']} bytes")
        print(f"     fraq_value: {page['fraq_value']:.6f}")
    print()


async def example_web_crawl_async():
    """Przykład 4: Asynchroniczne crawlowanie ze streamingiem"""
    print("=" * 60)
    print("4. ASYNCHRONICZNE CRAWLOWANIE ZE STREAMINGIEM")
    print("=" * 60)
    
    adapter = WebCrawlerAdapter(
        base_url="https://httpbin.org/html",
        max_depth=1,
        max_pages=5,
        timeout=10.0,
    )
    
    print("Streamowanie stron w czasie rzeczywistym:")
    count = 0
    async for page in adapter.stream_pages():
        print(f"  📄 {page['url']}")
        print(f"     Status: {page['status']}, Tytuł: {page.get('title', 'N/A')[:40]}")
        count += 1
    print(f"\nPrzecrawlowano {count} stron\n")


def example_fractal_coordinates():
    """Przykład 5: Fraktalne koordynaty dla sieci i web"""
    print("=" * 60)
    print("5. FRAKTALNE KOORDYNATY")
    print("=" * 60)
    
    # Sieć
    net_adapter = NetworkAdapter(network="192.168.1.0/24")
    root = net_adapter.load_root()
    print(f"Sieć {net_adapter.network}:")
    print(f"  Position: {root.position}")
    print(f"  Seed: {root.seed}")
    print()
    
    # Web
    web_adapter = WebCrawlerAdapter(base_url="https://example.com")
    root = web_adapter.load_root()
    print(f"Strona {web_adapter.base_url}:")
    print(f"  Position: {root.position}")
    print(f"  Seed: {root.seed}")
    print(f"  Domain: {root.meta['domain']}")
    print()


def example_streaming_comparison():
    """Przykład 6: Porównanie streaming vs batch"""
    print("=" * 60)
    print("6. PORÓWNANIE STREAMING VS BATCH")
    print("=" * 60)
    
    adapter = NetworkAdapter(
        network="127.0.0.1/24",
        ports=[8000, 8001],
        timeout=0.5,
    )
    
    # Batch (wszytsko naraz)
    print("Batch (search):")
    import time
    start = time.time()
    results = adapter.search(limit=10)
    elapsed = time.time() - start
    print(f"  Czas: {elapsed:.2f}s, Wyniki: {len(results)}")
    
    # Streaming (przychodzą stopniowo)
    print("\nStreaming (stream):")
    start = time.time()
    streamed = list(adapter.stream(count=10))
    elapsed = time.time() - start
    print(f"  Czas: {elapsed:.2f}s, Wyniki: {len(streamed)}")
    print()


async def main():
    """Uruchom wszystkie przykłady"""
    print("\n" + "=" * 60)
    print("FRAQ - Network & Web Crawling Examples")
    print("=" * 60)
    print()
    
    # Przykłady synchroniczne
    example_network_scan_sync()
    example_web_crawl_sync()
    example_fractal_coordinates()
    example_streaming_comparison()
    
    # Przykłady asynchroniczne
    await example_network_scan_async()
    await example_web_crawl_async()
    
    print("=" * 60)
    print("Koniec przykładów")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
