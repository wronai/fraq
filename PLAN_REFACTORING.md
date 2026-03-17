# Plan Refaktoryzacji - Network & Web Crawling

## 1. Architektura Rozszerzenia

### 1.1 Nowe Adaptery

```
fraq/adapters.py
├── BaseAdapter (istniejący)
├── FileAdapter (istniejący)
├── HTTPAdapter (istniejący)
├── FileSearchAdapter (istniejący)
├── NetworkAdapter ⭐ NOWY
│   ├── scan_async() - async skanowanie sieci
│   ├── stream_devices() - streaming wyników
│   └── _check_port() - sprawdzanie portu
└── WebCrawlerAdapter ⭐ NOWY
    ├── crawl_async() - async crawling strony
    ├── stream_pages() - streaming stron
    └── _fetch_page() - pobieranie strony
```

### 1.2 Fraktalne Koordynaty

**NetworkAdapter:**
- `position = (IP_octet_normalized, latency_seconds, port_normalized)`
- `seed = hash(f"{ip}:{port}")`
- `value = hash(...) / 2^32`

**WebCrawlerAdapter:**
- `position = (depth_normalized, page_size_100KB, link_count_100)`
- `seed = hash(url)`
- `value = hash(url) / 2^32`

## 2. API i CLI

### 2.1 Nowe Komendy CLI

```bash
# Network scanning
fraq network scan --network 192.168.1.0/24 --ports 80,443,22
fraq network scan -n 10.0.0.0/24 -p 22,3389 -t 2.0 --format json

# Web crawling
fraq web crawl https://example.com --depth 2 --max-pages 50
fraq web crawl https://docs.python.org -d 3 -n 100 -f csv
```

### 2.2 Programmatic API

```python
# Synchroniczne
from fraq import NetworkAdapter, WebCrawlerAdapter

# Network
net = NetworkAdapter(network="192.168.1.0/24", ports=[80, 443])
results = net.search(limit=100)  # batch

# Web
crawler = WebCrawlerAdapter(base_url="https://example.com", max_depth=2)
pages = crawler.search()  # batch

# Asynchroniczne + Streaming
async for device in net.stream_devices():
    print(device)  # real-time

async for page in crawler.stream_pages():
    print(page)  # real-time
```

## 3. Zależności

### 3.1 Wymagane Biblioteki

Dodaj do `pyproject.toml` w sekcji `[project.optional-dependencies]`:

```toml
[project.optional-dependencies]
ai = ["litellm>=1.0", "python-dotenv"]
network = ["aiohttp>=3.8", "beautifulsoup4>=4.11"]
web = ["aiohttp>=3.8", "beautifulsoup4>=4.11"]
full = ["litellm", "python-dotenv", "aiohttp", "beautifulsoup4", "fastapi", "uvicorn"]
```

### 3.2 Opcjonalne Importy

```python
# W adapters.py - graceful fallback
try:
    import aiohttp
    import bs4  # beautifulsoup4
    HAS_ASYNC_WEB = True
except ImportError:
    HAS_ASYNC_WEB = False
```

## 4. Implementacja Async

### 4.1 Pattern: Async z Semaphore

```python
class NetworkAdapter:
    def __init__(self, max_concurrent=50):
        self._semaphore = asyncio.Semaphore(max_concurrent)
    
    async def _check_port(self, ip, port):
        async with self._semaphore:
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(ip, port),
                    timeout=self.timeout
                )
                # ... process
            except asyncio.TimeoutError:
                return None
```

### 4.2 Pattern: Streaming Results

```python
async def stream_devices(self):
    """Yield results as they come in."""
    tasks = []
    for host in self.network.hosts():
        for port in self.ports:
            tasks.append(self._check_port(host, port))
    
    # Process as completed
    for coro in asyncio.as_completed(tasks):
        result = await coro
        if result and result.get("open"):
            yield result
```

## 5. REST API Endpoints (opcjonalnie)

### 5.1 FastAPI Integration

```python
@app.get("/network/scan")
async def network_scan(
    network: str = Query("192.168.1.0/24"),
    ports: str = Query("80,443,22"),
):
    adapter = NetworkAdapter(network, ports.split(","))
    return {"scanning": network, "task_id": create_task(adapter.scan_async)}

@app.get("/web/crawl")
async def web_crawl(
    url: str = Query(...),
    depth: int = Query(2),
):
    adapter = WebCrawlerAdapter(url, max_depth=depth)
    return {"crawling": url, "task_id": create_task(adapter.crawl_async)}

@app.websocket("/ws/network")
async def ws_network_scan(websocket: WebSocket):
    adapter = NetworkAdapter(...)
    async for device in adapter.stream_devices():
        await websocket.send_json(device)
```

## 6. Testy

### 6.1 Unit Tests

```python
def test_network_adapter_load_root():
    adapter = NetworkAdapter("192.168.1.0/24")
    root = adapter.load_root()
    assert root.meta["network"] == "192.168.1.0/24"
    assert root.meta["total_hosts"] == 256

def test_web_crawler_extract_links():
    adapter = WebCrawlerAdapter("https://example.com")
    soup = BeautifulSoup('<a href="/page">link</a>', "html.parser")
    links = adapter._extract_links(soup, "https://example.com")
    assert links == ["https://example.com/page"]
```

### 6.2 Async Tests

```python
@pytest.mark.asyncio
async def test_network_scan_async():
    adapter = NetworkAdapter("127.0.0.1/30", ports=[8000])
    results = await adapter.scan_async(limit=2)
    assert isinstance(results, list)

@pytest.mark.asyncio
async def test_web_crawl_stream():
    adapter = WebCrawlerAdapter("https://httpbin.org/html", max_pages=1)
    pages = []
    async for page in adapter.stream_pages():
        pages.append(page)
        break
    assert len(pages) > 0
```

## 7. Docker Support

### 7.1 Network Scanning w Docker

```dockerfile
# Wymagane uprawnienia dla skanowania sieci
RUN apt-get update && apt-get install -y iputils-ping netcat
```

```yaml
# docker-compose.yml
services:
  fraq-network:
    build: .
    cap_add:
      - NET_RAW  # Required for ping
    network_mode: host  # Dostęp do host network
```

### 7.2 Web Crawling w Docker

```yaml
services:
  fraq-web:
    build: .
    environment:
      - CRAWL_USER_AGENT=fraq-crawler/0.2.4
      - CRAWL_DELAY=1.0  # Rate limiting
```

## 8. Przykłady Użycia

Zobacz `examples/network_web_examples.py`:

1. Synchroniczne skanowanie sieci
2. Asynchroniczne skanowanie ze streamingiem
3. Synchroniczny crawling
4. Asynchroniczny crawling ze streamingiem
5. Fraktalne koordynaty
6. Porównanie batch vs streaming

## 9. Roadmap

### Faza 1 (zrobione)
- ✅ NetworkAdapter
- ✅ WebCrawlerAdapter
- ✅ CLI commands
- ✅ Podstawowe przykłady

### Faza 2 (opcjonalnie)
- 🔄 REST API endpoints
- 🔄 WebSocket streaming
- 🔄 Docker compose dla network/web
- 🔄 NL integration ("przeskanuj sieć", "crawlej stronę")

### Faza 3 (opcjonalnie)
- 🔄 Rate limiting dla web crawler
- 🔄 Robots.txt respect
- 🔄 Proxy support
- 🔄 VPN/Tor support dla network

## 10. Dokumentacja

- `examples/network_web_examples.py` - przykłady użycia
- `README.md` - update o nowe funkcje
- `CLI_CURL_GUIDE.md` - nowe komendy CLI

## Podsumowanie Zmian

**Pliki zmienione:**
- `fraq/adapters.py` - +420 linii (NetworkAdapter, WebCrawlerAdapter)
- `fraq/query.py` - +1 linia (SourceType.NETWORK)
- `fraq/cli.py` - +100 linii (nowe komendy)
- `fraq/__init__.py` - eksporty

**Nowe pliki:**
- `examples/network_web_examples.py` - przykłady
- `PLAN_REFACTORING.md` - ten dokument

**Testy:** 141 testów przechodzi ✅
