"""Web crawler adapter for async website crawling."""

from __future__ import annotations

import asyncio
import urllib.parse
from collections import deque
from pathlib import Path
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Set

try:
    import aiohttp
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

from fraq.core import FraqNode
from fraq.formats import FormatRegistry
from fraq.query import SourceType
from fraq.adapters.base import BaseAdapter


class WebCrawlerAdapter(BaseAdapter):
    """Async adapter for crawling websites and extracting links/content."""

    source_type = SourceType.HTTP

    def __init__(
        self,
        base_url: str,
        max_depth: int = 2,
        max_pages: int = 100,
        timeout: float = 10.0,
        respect_robots: bool = True,
    ):
        if not HAS_DEPS:
            raise ImportError("WebCrawlerAdapter requires 'aiohttp' and 'beautifulsoup4'")
        self.base_url = base_url.rstrip("/")
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.timeout = timeout
        self.respect_robots = respect_robots
        self.visited: Set[str] = set()
        self.pages: List[Dict[str, Any]] = []
        self._session: Optional[Any] = None

    async def _get_session(self) -> Any:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(
                timeout=timeout,
                headers={"User-Agent": "fraq-crawler/0.2.4"},
            )
        return self._session

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
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

    async def crawl_async(self) -> List[Dict[str, Any]]:
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
                for link in page_data.get("links", []):
                    if link not in self.visited:
                        queue.append((link, depth + 1))

        if self._session and not self._session.closed:
            await self._session.close()

        return self.pages

    async def _fetch_page(self, url: str, depth: int) -> Optional[Dict[str, Any]]:
        try:
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")
                title = soup.title.string if soup.title else "No title"
                links = self._extract_links(soup, url)

                return {
                    "url": url,
                    "title": title.strip()[:200],
                    "depth": depth,
                    "size_bytes": len(content),
                    "status": response.status,
                    "links": links,
                    "link_count": len(links),
                    "fraq_position": (
                        float(depth) / self.max_depth,
                        float(len(content)) / 100000,
                        float(len(links)) / 100,
                    ),
                    "fraq_seed": hash(url) % (2**32),
                    "fraq_value": hash(url) / (2**32),
                }
        except Exception as e:
            return {"url": url, "error": str(e), "depth": depth}

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        links = []
        base_parsed = urllib.parse.urlparse(base_url)

        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if href.startswith(("javascript:", "mailto:", "tel:")):
                continue
            full_url = urllib.parse.urljoin(base_url, href)
            parsed = urllib.parse.urlparse(full_url)
            if parsed.netloc == base_parsed.netloc:
                clean_url = full_url.split("#")[0]
                if clean_url not in links:
                    links.append(clean_url)
        return links

    async def stream_pages(self) -> AsyncIterator[Dict[str, Any]]:
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
                for link in page_data.get("links", []):
                    if link not in self.visited:
                        queue.append((link, depth + 1))

        if self._session and not self._session.closed:
            await self._session.close()

    def search(self, **opts: Any) -> List[Dict[str, Any]]:
        return asyncio.run(self.crawl_async())

    def stream(self, count: int = 100, **opts: Any) -> Iterator[Dict[str, Any]]:
        async def _collect():
            results = []
            async for page in self.stream_pages():
                results.append(page)
                if len(results) >= count:
                    break
            return results
        return iter(asyncio.run(_collect()))

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        if self.pages:
            output = FormatRegistry.serialize(fmt, self.pages)
            path = Path(uri)
            path.write_bytes(output.encode() if isinstance(output, str) else output)
            return str(path)
        return ""
