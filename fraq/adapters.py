"""
Data source adapters.

Each adapter wraps a FraqExecutor and adds source-specific capabilities:
loading root state from disk / HTTP / SQL, persisting zoom results back,
and streaming from live sensors.

All adapters expose the same interface so calling code stays source-agnostic.
"""

from __future__ import annotations

import json
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional
import asyncio
import ipaddress
import socket
import urllib.parse
from collections import deque
from typing import AsyncIterator

from fraq.core import FraqNode, FraqCursor, Vector
from fraq.formats import FormatRegistry
from fraq.query import FraqQuery, FraqExecutor, SourceType


# ---------------------------------------------------------------------------
# Base adapter protocol
# ---------------------------------------------------------------------------


class BaseAdapter(ABC):
    """Interface every data-source adapter must implement."""

    source_type: SourceType

    @abstractmethod
    def load_root(self, uri: str, **opts: Any) -> FraqNode:
        """Materialise a root node from the source."""

    @abstractmethod
    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        """Persist a node (or subtree) back to the source.  Return the path/URI."""

    def execute(self, query: FraqQuery) -> Any:
        """Load root from *query.source_uri*, then run the query."""
        root = self.load_root(query.source_uri, **query.meta)
        return FraqExecutor(root).execute(query)

    def execute_iter(self, query: FraqQuery) -> Iterator[Dict[str, Any]]:
        root = self.load_root(query.source_uri, **query.meta)
        yield from FraqExecutor(root).execute_iter(query)


# ---------------------------------------------------------------------------
# File adapter  (JSON / YAML / CSV on disk)
# ---------------------------------------------------------------------------


class FileAdapter(BaseAdapter):
    """Read/write fractal state from local files.

    Supported formats: json, yaml, csv, jsonl, binary.

    Examples
    --------
    >>> adapter = FileAdapter()
    >>> root = adapter.load_root("gradient_root.json")
    >>> deep = root.zoom(steps=5)
    >>> adapter.save(deep, "deep_data.json")
    """

    source_type = SourceType.FILE

    def load_root(self, uri: str, **opts: Any) -> FraqNode:
        path = Path(uri)
        if not path.exists():
            # Derive a deterministic root from the filename
            seed = int(hashlib.sha256(uri.encode()).hexdigest()[:8], 16)
            dims = opts.get("dims", 3)
            return FraqNode(position=tuple(0.0 for _ in range(dims)), seed=seed)

        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        return self._dict_to_node(data)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        path = Path(uri)
        content = FormatRegistry.serialize(fmt, node.to_dict(max_depth=opts.get("max_depth", 1)))
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return str(path.resolve())

    @staticmethod
    def _dict_to_node(data: Dict[str, Any]) -> FraqNode:
        return FraqNode(
            position=tuple(data.get("position", [0.0, 0.0, 0.0])),
            depth=data.get("depth", 0),
            seed=data.get("seed", 0),
        )


# ---------------------------------------------------------------------------
# HTTP adapter  (REST / GraphQL endpoints)
# ---------------------------------------------------------------------------


class HTTPAdapter(BaseAdapter):
    """Fetch fractal roots from remote HTTP APIs and push results back.

    The adapter does **not** depend on ``requests`` at import time — it
    only needs it when ``load_root`` / ``save`` are actually called, so
    the library stays lightweight.

    URI format
    ----------
    ``https://api.example.com/gradient/root``

    Extra *opts*:
        headers : dict         — custom HTTP headers
        method  : str          — GET (default) or POST
        timeout : int          — seconds (default 30)

    Examples
    --------
    >>> adapter = HTTPAdapter()
    >>> root = adapter.load_root("https://api.gradient.example/root")
    >>> data = root.zoom(steps=20).to_dict()
    """

    source_type = SourceType.HTTP

    def load_root(self, uri: str, **opts: Any) -> FraqNode:
        if not uri:
            return FraqNode(position=(0.0, 0.0, 0.0))
        try:
            import requests  # noqa: lazy import
            method = opts.get("method", "GET")
            headers = opts.get("headers", {})
            timeout = opts.get("timeout", 30)
            resp = requests.request(method, uri, headers=headers, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            return FileAdapter._dict_to_node(data)
        except Exception:
            # Fallback: deterministic root from URI
            seed = int(hashlib.sha256(uri.encode()).hexdigest()[:8], 16)
            return FraqNode(position=(0.0, 0.0, 0.0), seed=seed)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        try:
            import requests  # noqa
            payload = FormatRegistry.serialize(fmt, node.to_dict(max_depth=1))
            headers = opts.get("headers", {"Content-Type": "application/json"})
            timeout = opts.get("timeout", 30)
            resp = requests.post(uri, data=payload, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return uri
        except Exception:
            return ""


# ---------------------------------------------------------------------------
# SQL adapter  (PostgreSQL / SQLite — via mapping)
# ---------------------------------------------------------------------------


class SQLAdapter(BaseAdapter):
    """Map fractal nodes to/from relational tables.

    Instead of requiring a live DB connection the adapter defines the
    *mapping* between SQL rows and fractal coordinates so that the same
    query language works.  A ``row_to_node`` callable transforms a DB row
    dict into a FraqNode.

    Parameters
    ----------
    row_to_node : callable
        ``(row_dict) -> FraqNode``.  Defaults to treating ``value`` as
        seed and the remaining numeric columns as position components.
    table : str
        Table name (informational, used in ``save``).

    Examples
    --------
    >>> adapter = SQLAdapter(table="gradient_nodes")
    >>> root = adapter.load_root("", rows=[{"id": 1, "x": 0.0, "y": 0.0, "value": 0}])
    >>> data = root.zoom(steps=5).to_dict()
    """

    source_type = SourceType.SQL

    def __init__(
        self,
        table: str = "fraq_nodes",
        row_to_node: Optional[Any] = None,
    ):
        self.table = table
        self._row_to_node = row_to_node or self._default_row_to_node

    def load_root(self, uri: str, **opts: Any) -> FraqNode:
        rows = opts.get("rows")
        if rows and len(rows) > 0:
            return self._row_to_node(rows[0])
        # Fallback: derive from table name
        seed = int(hashlib.sha256(self.table.encode()).hexdigest()[:8], 16)
        dims = opts.get("dims", 3)
        return FraqNode(position=tuple(0.0 for _ in range(dims)), seed=seed)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        """Return an INSERT statement (the caller executes it)."""
        d = node.to_dict()
        cols = ", ".join(d.keys())
        vals = ", ".join(repr(v) for v in d.values())
        return f"INSERT INTO {self.table} ({cols}) VALUES ({vals});"

    def generate_sql_function(self, dims: int = 3) -> str:
        """Generate a PostgreSQL function that wraps zoom()."""
        return f"""
CREATE OR REPLACE FUNCTION {self.table}_zoom(
    p_level INT,
    p_direction FLOAT[{dims}]
) RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    -- This is a stub; actual zoom runs in Python via fraq
    SELECT json_build_object(
        'level', p_level,
        'direction', p_direction,
        'table', '{self.table}'
    ) INTO result;
    RETURN result;
END;
$$ LANGUAGE plpgsql;
"""

    @staticmethod
    def _default_row_to_node(row: Dict[str, Any]) -> FraqNode:
        numeric_vals = [v for v in row.values() if isinstance(v, (int, float))]
        pos = tuple(float(v) for v in numeric_vals[:3]) or (0.0, 0.0, 0.0)
        seed = int(numeric_vals[0]) if numeric_vals else 0
        return FraqNode(position=pos, seed=seed)


# ---------------------------------------------------------------------------
# Sensor / IoT adapter
# ---------------------------------------------------------------------------


class SensorAdapter(BaseAdapter):
    """Simulate or consume live sensor data as fractal streams.

    In simulation mode (no URI) the adapter generates infinite deterministic
    sensor readings via the fractal zoom.  With a URI it could connect to
    MQTT / Kafka / serial — the interface is the same.

    Examples
    --------
    >>> adapter = SensorAdapter(base_temp=23.5, sample_hz=10)
    >>> for reading in adapter.stream(depth=3, count=100):
    ...     print(reading)
    """

    source_type = SourceType.SENSOR

    def __init__(
        self,
        base_temp: float = 22.0,
        base_humidity: float = 55.0,
        base_pressure: float = 1013.25,
        sample_hz: float = 10.0,
    ):
        self.base_temp = base_temp
        self.base_humidity = base_humidity
        self.base_pressure = base_pressure
        self.sample_hz = sample_hz

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
        from fraq.generators import SensorStreamGenerator
        gen = SensorStreamGenerator(
            base_temp=self.base_temp,
            base_humidity=self.base_humidity,
            base_pressure=self.base_pressure,
        )
        return FraqNode(position=(0.0, 0.0, 0.0), generator=gen)

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        path = Path(uri)
        content = FormatRegistry.serialize(fmt, node.value)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return str(path)

    def stream(
        self,
        depth: int = 3,
        count: Optional[int] = None,
        direction: Optional[Vector] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Yield sensor readings indefinitely (or up to *count*)."""
        root = self.load_root()
        cursor = FraqCursor(root=root)
        i = 0
        while count is None or i < count:
            cursor.advance(direction)
            yield cursor.current.value
            i += 1


# ---------------------------------------------------------------------------
# File Search Adapter
# ---------------------------------------------------------------------------


class FileSearchAdapter(BaseAdapter):
    """
    Adapter for searching files on disk using fractal patterns.
    
    Maps file system searches to fractal coordinates:
    - Position = file metadata (size, mtime, depth in hierarchy)
    - Seed = hash of file path
    - Children = files in subdirectories
    
    Example:
        adapter = FileSearchAdapter("/home/user/docs", "*.pdf")
        root = adapter.load_root("/home/user/docs")
        # Query for recent PDFs
        results = adapter.search(extension="pdf", limit=10, sort_by="mtime")
    """

    source_type = SourceType.FILE

    def __init__(
        self,
        base_path: str = ".",
        pattern: str = "*",
        recursive: bool = True,
    ):
        self.base_path = Path(base_path).expanduser().resolve()
        self.pattern = pattern
        self.recursive = recursive

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
        """
        Create root node representing the search space.
        URI can be path or empty (uses base_path).
        """
        path = Path(uri).expanduser().resolve() if uri else self.base_path
        
        # Use directory stats as position
        try:
            stat = path.stat()
            position = (
                float(stat.st_size) if path.is_file() else float(stat.st_nlink),
                float(stat.st_mtime),
                float(stat.st_ctime),
            )
            seed = int(stat.st_ino)
        except (OSError, FileNotFoundError):
            position = (0.0, 0.0, 0.0)
            seed = hash(str(path)) % (2**32)

        return FraqNode(
            position=position,
            seed=seed,
            meta={
                "path": str(path),
                "type": "directory" if path.is_dir() else "file",
            },
        )

    def search(
        self,
        extension: str | None = None,
        pattern: str | None = None,
        limit: int = 10,
        sort_by: str = "name",  # name, mtime, size
        newer_than: float | None = None,  # timestamp
        **opts: Any,
    ) -> list[dict[str, Any]]:
        """
        Search files and return as fractal records.
        
        Args:
            extension: File extension (pdf, txt, etc.)
            pattern: Glob pattern
            limit: Max results
            sort_by: Sort field (name, mtime, size)
            newer_than: Only files newer than this timestamp
        
        Returns:
            List of file records with fractal coordinates
        """
        search_pattern = pattern or self.pattern
        if extension and not search_pattern.endswith(f".{extension}"):
            search_pattern = f"*.{extension}"

        # Collect files
        files = []
        if self.recursive:
            iterator = self.base_path.rglob(search_pattern)
        else:
            iterator = self.base_path.glob(search_pattern)

        for path in iterator:
            if not path.is_file():
                continue
                
            try:
                stat = path.stat()
                mtime = stat.st_mtime
                
                # Filter by time if specified
                if newer_than and mtime <= newer_than:
                    continue
                
                # Create fractal representation
                record = {
                    "filename": path.name,
                    "path": str(path),
                    "extension": path.suffix.lstrip(".").lower(),
                    "size": stat.st_size,
                    "mtime": mtime,
                    "ctime": stat.st_ctime,
                    "depth": len(path.relative_to(self.base_path).parts),
                    # Fractal coordinates
                    "fraq_position": (
                        float(stat.st_size) / (1024 * 1024),  # MB
                        float(mtime),
                        float(stat.st_ctime),
                    ),
                    "fraq_seed": hash(str(path)) % (2**32),
                    "fraq_value": hash(str(path)) / (2**32),  # 0-1
                }
                files.append(record)
            except (OSError, PermissionError):
                continue

        # Sort
        if sort_by == "mtime":
            files.sort(key=lambda x: x["mtime"], reverse=True)
        elif sort_by == "size":
            files.sort(key=lambda x: x["size"], reverse=True)
        else:  # name
            files.sort(key=lambda x: x["filename"])

        return files[:limit]

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        """Save search results to file."""
        if "files" in node.meta:
            data = node.meta["files"]
            output = FormatRegistry.serialize(fmt, data)
            path = Path(uri)
            path.write_bytes(output.encode() if isinstance(output, str) else output)
            return str(path)
        return ""

    def stream(
        self,
        extension: str | None = None,
        pattern: str | None = None,
        count: int = 100,
    ) -> Iterator[dict[str, Any]]:
        """Stream file records one by one."""
        search_pattern = pattern or self.pattern
        if extension:
            search_pattern = f"*.{extension}"

        iterator = self.base_path.rglob(search_pattern) if self.recursive else self.base_path.glob(search_pattern)
        
        yielded = 0
        for path in iterator:
            if not path.is_file():
                continue
            try:
                stat = path.stat()
                yield {
                    "filename": path.name,
                    "path": str(path),
                    "extension": path.suffix.lstrip(".").lower(),
                    "size": stat.st_size,
                    "mtime": stat.st_mtime,
                    "fraq_value": hash(str(path)) / (2**32),
                }
                yielded += 1
                if yielded >= count:
                    break
            except (OSError, PermissionError):
                continue


# ---------------------------------------------------------------------------
# Network Adapter — Async LAN scanning
# ---------------------------------------------------------------------------


class NetworkAdapter(BaseAdapter):
    """
    Async adapter for scanning local network devices and services.
    
    Maps network topology to fractal coordinates:
    - Position = (IP octets, latency, port)
    - Seed = hash of (IP + port + service)
    - Children = discovered services on device
    
    Example:
        adapter = NetworkAdapter(network="192.168.1.0/24", ports=[80, 443, 22])
        # Scan network
        results = await adapter.scan_async()
        # Stream results
        async for device in adapter.stream_devices():
            print(device)
    """

    source_type = SourceType.NETWORK

    def __init__(
        self,
        network: str = "192.168.1.0/24",
        ports: list[int] | None = None,
        timeout: float = 1.0,
        max_concurrent: int = 50,
    ):
        self.network = ipaddress.ip_network(network, strict=False)
        self.ports = ports or [80, 443, 22, 8080, 3000]
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self._semaphore = None

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
        """Create root node representing the network."""
        network_str = str(self.network)
        return FraqNode(
            position=(
                float(self.network.network_address),
                float(self.network.prefixlen),
                0.0,
            ),
            seed=hash(network_str) % (2**32),
            meta={
                "network": network_str,
                "ports": self.ports,
                "total_hosts": self.network.num_addresses,
            },
        )

    async def scan_async(
        self,
        ports: list[int] | None = None,
        limit: int = 1000,
    ) -> list[dict[str, Any]]:
        """Async scan network for active devices and services."""
        ports = ports or self.ports
        self._semaphore = asyncio.Semaphore(self.max_concurrent)
        
        tasks = []
        hosts_scanned = 0
        
        for host in self.network.hosts():
            if hosts_scanned >= limit:
                break
            ip_str = str(host)
            for port in ports:
                tasks.append(self._check_port(ip_str, port))
            hosts_scanned += 1
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter successful connections
        devices = [r for r in results if isinstance(r, dict) and r.get("open")]
        
        # Sort by IP
        devices.sort(key=lambda x: ipaddress.ip_address(x["ip"]))
        
        return devices

    async def _check_port(self, ip: str, port: int) -> dict[str, Any]:
        """Check if port is open on host."""
        async with self._semaphore:
            try:
                start_time = asyncio.get_event_loop().time()
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(ip, port),
                    timeout=self.timeout
                )
                latency = (asyncio.get_event_loop().time() - start_time) * 1000
                
                # Try to identify service
                service = self._identify_service(port)
                
                writer.close()
                await writer.wait_closed()
                
                # Create fractal coordinates
                ip_obj = ipaddress.ip_address(ip)
                ip_int = int(ip_obj)
                
                return {
                    "ip": ip,
                    "port": port,
                    "open": True,
                    "service": service,
                    "latency_ms": round(latency, 2),
                    # Fractal coordinates
                    "fraq_position": (
                        float(ip_int % 256) / 256,  # Last octet normalized
                        latency / 1000,  # Latency in seconds
                        float(port) / 65535,  # Port normalized
                    ),
                    "fraq_seed": hash(f"{ip}:{port}") % (2**32),
                    "fraq_value": hash(f"{ip}:{port}") / (2**32),
                }
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
                return {"ip": ip, "port": port, "open": False}
            except Exception as e:
                return {"ip": ip, "port": port, "open": False, "error": str(e)}

    def _identify_service(self, port: int) -> str:
        """Identify service by common port."""
        services = {
            22: "ssh", 80: "http", 443: "https", 21: "ftp",
            25: "smtp", 53: "dns", 110: "pop3", 143: "imap",
            3306: "mysql", 5432: "postgres", 27017: "mongodb",
            6379: "redis", 9200: "elasticsearch", 8080: "http-alt",
            3000: "dev-server", 5000: "flask", 8000: "http-alt",
        }
        return services.get(port, f"port-{port}")

    async def stream_devices(
        self,
        ports: list[int] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """Stream discovered devices asynchronously."""
        ports = ports or self.ports
        self._semaphore = asyncio.Semaphore(self.max_concurrent)
        
        for host in self.network.hosts():
            ip_str = str(host)
            for port in ports:
                result = await self._check_port(ip_str, port)
                if result.get("open"):
                    yield result

    def search(self, **opts: Any) -> list[dict[str, Any]]:
        """Synchronous wrapper for scan_async."""
        return asyncio.run(self.scan_async(**opts))

    def stream(self, count: int = 100, **opts: Any) -> Iterator[dict[str, Any]]:
        """Synchronous wrapper for stream_devices."""
        async def _collect():
            results = []
            async for device in self.stream_devices(**opts):
                results.append(device)
                if len(results) >= count:
                    break
            return results
        
        return iter(asyncio.run(_collect()))

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        """Save scan results to file."""
        if "scan_results" in node.meta:
            data = node.meta["scan_results"]
            output = FormatRegistry.serialize(fmt, data)
            path = Path(uri)
            path.write_bytes(output.encode() if isinstance(output, str) else output)
            return str(path)
        return ""


# ---------------------------------------------------------------------------
# Web Crawler Adapter — Async website crawling
# ---------------------------------------------------------------------------


class WebCrawlerAdapter(BaseAdapter):
    """
    Async adapter for crawling websites and extracting links/content.
    
    Maps web pages to fractal coordinates:
    - Position = (depth in crawl, page size, link count)
    - Seed = hash of URL
    - Children = links to other pages
    
    Example:
        adapter = WebCrawlerAdapter(base_url="https://example.com", max_depth=2)
        # Crawl site
        results = await adapter.crawl_async()
        # Stream pages
        async for page in adapter.stream_pages():
            print(page["url"], page["title"])
    """

    source_type = SourceType.HTTP

    def __init__(
        self,
        base_url: str,
        max_depth: int = 2,
        max_pages: int = 100,
        timeout: float = 10.0,
        respect_robots: bool = True,
    ):
        self.base_url = base_url.rstrip("/")
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.timeout = timeout
        self.respect_robots = respect_robots
        self.visited: set[str] = set()
        self.pages: list[dict[str, Any]] = []
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                headers={"User-Agent": "fraq-crawler/0.2.4"},
            )
        return self._session

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
        """Create root node representing the website."""
        parsed = urllib.parse.urlparse(self.base_url)
        return FraqNode(
            position=(0.0, 0.0, 0.0),
            seed=hash(parsed.netloc) % (2**32),
            meta={
                "base_url": self.base_url,
                "domain": parsed.netloc,
                "max_depth": self.max_depth,
            },
        )

    async def crawl_async(self) -> list[dict[str, Any]]:
        """Async crawl website starting from base_url."""
        self.visited.clear()
        self.pages.clear()
        
        queue: deque[tuple[str, int]] = deque([(self.base_url, 0)])
        
        while queue and len(self.pages) < self.max_pages:
            url, depth = queue.popleft()
            
            if url in self.visited or depth > self.max_depth:
                continue
            
            self.visited.add(url)
            
            page_data = await self._fetch_page(url, depth)
            if page_data:
                self.pages.append(page_data)
                
                # Queue new links
                for link in page_data.get("links", []):
                    if link not in self.visited:
                        queue.append((link, depth + 1))
        
        if self._session and not self._session.closed:
            await self._session.close()
        
        return self.pages

    async def _fetch_page(self, url: str, depth: int) -> dict[str, Any] | None:
        """Fetch and parse single page."""
        try:
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")
                
                # Extract data
                title = soup.title.string if soup.title else "No title"
                links = self._extract_links(soup, url)
                
                # Create fractal coordinates
                return {
                    "url": url,
                    "title": title.strip()[:200],
                    "depth": depth,
                    "size_bytes": len(content),
                    "status": response.status,
                    "links": links,
                    "link_count": len(links),
                    # Fractal coordinates
                    "fraq_position": (
                        float(depth) / self.max_depth,  # Normalized depth
                        float(len(content)) / 100000,  # Size (100KB scale)
                        float(len(links)) / 100,  # Links (100 scale)
                    ),
                    "fraq_seed": hash(url) % (2**32),
                    "fraq_value": hash(url) / (2**32),
                }
        except Exception as e:
            return {"url": url, "error": str(e), "depth": depth}

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        """Extract and normalize links from page."""
        links = []
        base_parsed = urllib.parse.urlparse(base_url)
        
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            
            # Skip non-HTTP links
            if href.startswith(("javascript:", "mailto:", "tel:")):
                continue
            
            # Normalize URL
            full_url = urllib.parse.urljoin(base_url, href)
            parsed = urllib.parse.urlparse(full_url)
            
            # Only same domain
            if parsed.netloc == base_parsed.netloc:
                # Remove fragment
                clean_url = full_url.split("#")[0]
                if clean_url not in links:
                    links.append(clean_url)
        
        return links

    async def stream_pages(self) -> AsyncIterator[dict[str, Any]]:
        """Stream crawled pages asynchronously."""
        self.visited.clear()
        queue: deque[tuple[str, int]] = deque([(self.base_url, 0)])
        pages_yielded = 0
        
        while queue and pages_yielded < self.max_pages:
            url, depth = queue.popleft()
            
            if url in self.visited or depth > self.max_depth:
                continue
            
            self.visited.add(url)
            
            page_data = await self._fetch_page(url, depth)
            if page_data and not page_data.get("error"):
                yield page_data
                pages_yielded += 1
                
                # Queue new links
                for link in page_data.get("links", []):
                    if link not in self.visited:
                        queue.append((link, depth + 1))
        
        if self._session and not self._session.closed:
            await self._session.close()

    def search(self, **opts: Any) -> list[dict[str, Any]]:
        """Synchronous wrapper for crawl_async."""
        return asyncio.run(self.crawl_async())

    def stream(self, count: int = 100, **opts: Any) -> Iterator[dict[str, Any]]:
        """Synchronous wrapper for stream_pages."""
        async def _collect():
            results = []
            async for page in self.stream_pages():
                results.append(page)
                if len(results) >= count:
                    break
            return results
        
        return iter(asyncio.run(_collect()))

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        """Save crawl results to file."""
        if self.pages:
            output = FormatRegistry.serialize(fmt, self.pages)
            path = Path(uri)
            path.write_bytes(output.encode() if isinstance(output, str) else output)
            return str(path)
        return ""


# ---------------------------------------------------------------------------
# Hybrid adapter — merge multiple sources
# ---------------------------------------------------------------------------


class HybridAdapter(BaseAdapter):
    """Combine roots from several adapters into one fractal.

    The merged root's seed is derived from all child seeds, and its
    position is the element-wise mean.

    Examples
    --------
    >>> h = HybridAdapter()
    >>> h.add(FileAdapter(), "local_backup.json")
    >>> h.add(HTTPAdapter(), "https://api.example.com/root")
    >>> merged = h.load_root("")
    """

    source_type = SourceType.HYBRID

    def __init__(self) -> None:
        self._sources: List[tuple[BaseAdapter, str, dict]] = []

    def add(self, adapter: BaseAdapter, uri: str, **opts: Any) -> "HybridAdapter":
        self._sources.append((adapter, uri, opts))
        return self

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
        if not self._sources:
            return FraqNode(position=(0.0, 0.0, 0.0))

        nodes = [a.load_root(u, **o) for a, u, o in self._sources]

        # Merge positions (mean) and seeds (xor)
        dims = max(len(n.position) for n in nodes)
        merged_pos = []
        for i in range(dims):
            vals = [n.position[i] if i < len(n.position) else 0.0 for n in nodes]
            merged_pos.append(sum(vals) / len(vals))

        merged_seed = 0
        for n in nodes:
            merged_seed ^= n.seed

        return FraqNode(
            position=tuple(merged_pos),
            seed=merged_seed,
            meta={"merged_from": len(nodes)},
        )

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        # Delegate to the first adapter that can save
        for adapter, _, _ in self._sources:
            result = adapter.save(node, uri, fmt, **opts)
            if result:
                return result
        return ""


# ---------------------------------------------------------------------------
# Adapter registry
# ---------------------------------------------------------------------------


_ADAPTERS: Dict[SourceType, type] = {
    SourceType.FILE: FileAdapter,
    SourceType.HTTP: HTTPAdapter,
    SourceType.SQL: SQLAdapter,
    SourceType.SENSOR: SensorAdapter,
    SourceType.NETWORK: NetworkAdapter,
    SourceType.HYBRID: HybridAdapter,
    SourceType.MEMORY: BaseAdapter,
}


def get_adapter(source: SourceType, **kwargs: Any) -> BaseAdapter:
    """Factory: return the right adapter for a source type."""
    cls = _ADAPTERS.get(source)
    if cls is None or cls is BaseAdapter:
        # Return a minimal in-memory adapter
        return FileAdapter()
    return cls(**kwargs)  # type: ignore[call-arg]
