"""
Async streaming for fraq.

Provides ``async for`` iteration over fractal data — ideal for real-time
sensor feeds, SSE endpoints, and Kafka/NATS producers.
"""

from __future__ import annotations

import asyncio
from typing import Any, AsyncIterator, Dict, Optional

from fraq.core import FraqNode, FraqCursor, FraqSchema, Vector
from fraq.query import FraqQuery, FraqExecutor


class AsyncFraqStream:
    """Async generator that yields fractal records at a controlled rate.

    Parameters
    ----------
    root : FraqNode
        Starting node.
    interval : float
        Seconds between yields (1/sample_hz).
    direction : Vector | None
        Zoom direction per tick.
    schema : FraqSchema | None
        If provided, each yield is a typed record; otherwise raw node dict.
    """

    def __init__(
        self,
        root: Optional[FraqNode] = None,
        interval: float = 0.1,
        direction: Optional[Vector] = None,
        schema: Optional[FraqSchema] = None,
        dims: int = 3,
    ):
        self.root = root or FraqNode(position=tuple(0.0 for _ in range(dims)))
        self.interval = interval
        self.direction = direction
        self.schema = schema
        self._cursor = FraqCursor(root=self.root)
        self._running = False

    async def __aiter__(self) -> AsyncIterator[Dict[str, Any]]:
        self._running = True
        while self._running:
            self._cursor.advance(self.direction)
            node = self._cursor.current
            if self.schema:
                yield self.schema.record(node)
            else:
                yield node.to_dict()
            await asyncio.sleep(self.interval)

    def stop(self) -> None:
        self._running = False

    @property
    def depth(self) -> int:
        return self._cursor.depth


async def async_query(
    query: FraqQuery,
    root: Optional[FraqNode] = None,
    dims: int = 3,
) -> list[Dict[str, Any]]:
    """Run a FraqQuery asynchronously (useful in async frameworks)."""
    executor = FraqExecutor(root=root, dims=dims)
    # Offload to thread pool for CPU-bound generation
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: list(executor.execute_iter(query)))


async def async_stream(
    root: Optional[FraqNode] = None,
    count: int = 10,
    interval: float = 0.1,
    direction: Optional[Vector] = None,
    dims: int = 3,
) -> AsyncIterator[Dict[str, Any]]:
    """Convenience async generator with a count limit."""
    stream = AsyncFraqStream(root=root, interval=interval, direction=direction, dims=dims)
    i = 0
    async for record in stream:
        yield record
        i += 1
        if i >= count:
            stream.stop()
            break
