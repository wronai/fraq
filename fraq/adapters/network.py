"""Network adapter for LAN scanning."""

from __future__ import annotations

import asyncio
import ipaddress
from collections import deque
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional

from fraq.core import FraqNode
from fraq.formats import FormatRegistry
from fraq.query import SourceType
from fraq.adapters.base import BaseAdapter


class NetworkAdapter(BaseAdapter):
    """Async adapter for scanning local network devices and services."""

    source_type = SourceType.NETWORK

    def __init__(
        self,
        network: str = "192.168.1.0/24",
        ports: Optional[List[int]] = None,
        timeout: float = 1.0,
        max_concurrent: int = 50,
    ):
        self.network = ipaddress.ip_network(network, strict=False)
        self.ports = ports or [80, 443, 22, 8080, 3000]
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self._semaphore: Optional[asyncio.Semaphore] = None

    def load_root(self, uri: str = "", **opts: Any) -> FraqNode:
        network_str = str(self.network)
        return FraqNode(
            position=(
                float(int(self.network.network_address)),
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
        ports: Optional[List[int]] = None,
        limit: int = 1000,
    ) -> List[Dict[str, Any]]:
        """Pure pipeline: plan → IO → parse."""
        targets = self._plan_scan(ports, limit)
        self._semaphore = asyncio.Semaphore(self.max_concurrent)

        tasks = [self._check_port_io(ip, port) for ip, port in targets]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        devices = [
            r for r in results
            if isinstance(r, dict) and r.get("open")
        ]
        devices.sort(key=lambda x: ipaddress.ip_address(x["ip"]))
        return devices

    def _plan_scan(
        self,
        ports: Optional[List[int]] = None,
        limit: int = 1000,
    ) -> List[tuple[str, int]]:
        """Plan scan targets - pure function."""
        ports = ports or self.ports
        targets: List[tuple[str, int]] = []
        hosts_scanned = 0

        for host in self.network.hosts():
            if hosts_scanned >= limit:
                break
            ip_str = str(host)
            for port in ports:
                targets.append((ip_str, port))
            hosts_scanned += 1

        return targets

    def _parse_result(
        self,
        ip: str,
        port: int,
        is_open: bool,
        latency_ms: Optional[float] = None,
        error: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Parse scan result into structured data - pure function."""
        base = {"ip": ip, "port": port, "open": is_open}

        if not is_open:
            if error:
                base["error"] = error
            return base

        service = self._identify_service(port)
        ip_obj = ipaddress.ip_address(ip)
        ip_int = int(ip_obj)

        return {
            **base,
            "service": service,
            "latency_ms": round(latency_ms, 2) if latency_ms else 0.0,
            "fraq_position": (
                float(ip_int % 256) / 256,
                (latency_ms or 0.0) / 1000,
                float(port) / 65535,
            ),
            "fraq_seed": hash(f"{ip}:{port}") % (2**32),
            "fraq_value": hash(f"{ip}:{port}") / (2**32),
        }

    async def _check_port_io(self, ip: str, port: int) -> Dict[str, Any]:
        """Check if port is open - IO operation only."""
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.max_concurrent)
        async with self._semaphore:
            try:
                start_time = asyncio.get_event_loop().time()
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(ip, port),
                    timeout=self.timeout
                )
                latency = (asyncio.get_event_loop().time() - start_time) * 1000
                writer.close()
                await writer.wait_closed()
                return self._parse_result(ip, port, True, latency_ms=latency)
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
                return self._parse_result(ip, port, False)
            except Exception as e:
                return self._parse_result(ip, port, False, error=str(e))

    def _identify_service(self, port: int) -> str:
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
        ports: Optional[List[int]] = None,
    ) -> AsyncIterator[Dict[str, Any]]:
        """Stream devices with pure pipeline."""
        targets = self._plan_scan(ports, limit=1000)
        self._semaphore = asyncio.Semaphore(self.max_concurrent)

        for ip, port in targets:
            result = await self._check_port_io(ip, port)
            if result.get("open"):
                yield result

    def search(self, **opts: Any) -> List[Dict[str, Any]]:
        return asyncio.run(self.scan_async(**opts))

    def stream(self, count: int = 100, **opts: Any) -> Iterator[Dict[str, Any]]:
        async def _collect():
            results = []
            async for device in self.stream_devices(**opts):
                results.append(device)
                if len(results) >= count:
                    break
            return results
        return iter(asyncio.run(_collect()))

    def save(self, node: FraqNode, uri: str, fmt: str = "json", **opts: Any) -> str:
        if "scan_results" in node.meta:
            data = node.meta["scan_results"]
            output = FormatRegistry.serialize(fmt, data)
            from pathlib import Path
            path = Path(uri)
            path.write_bytes(output.encode() if isinstance(output, str) else output)
            return str(path)
        return ""
