"""Tests for fraq.streaming — AsyncFraqStream, async_query, async_stream."""

import asyncio
import pytest
from fraq.core import FraqNode, FraqSchema
from fraq.query import FraqQuery
from fraq.streaming import AsyncFraqStream, async_query, async_stream


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


class TestAsyncFraqStream:
    def test_stream_with_count(self):
        async def run():
            stream = AsyncFraqStream(interval=0.001, dims=2)
            results = []
            i = 0
            async for record in stream:
                results.append(record)
                i += 1
                if i >= 5:
                    stream.stop()
                    break
            return results

        results = asyncio.run(run())
        assert len(results) == 5
        assert "value" in results[0]

    def test_stream_with_schema(self):
        async def run():
            root = FraqNode(position=(0.0, 0.0))
            schema = FraqSchema(root=root)
            schema.add_field("x", "float")
            schema.add_field("y", "int")
            stream = AsyncFraqStream(root=root, interval=0.001, schema=schema)
            results = []
            async for record in stream:
                results.append(record)
                if len(results) >= 3:
                    stream.stop()
                    break
            return results

        results = asyncio.run(run())
        assert len(results) == 3
        assert "x" in results[0]
        assert "y" in results[0]

    def test_depth_increases(self):
        async def run():
            stream = AsyncFraqStream(interval=0.001, dims=2)
            async for _ in stream:
                if stream.depth >= 3:
                    stream.stop()
                    break
            return stream.depth

        depth = asyncio.run(run())
        assert depth >= 3


class TestAsyncQuery:
    def test_basic_query(self):
        async def run():
            q = FraqQuery(depth=1, branching=3, format="records")
            q.select("v:float")
            return await async_query(q, dims=2)

        results = asyncio.run(run())
        assert len(results) == 3
        assert "v" in results[0]


class TestAsyncStreamFunction:
    def test_stream_count(self):
        async def run():
            results = []
            async for record in async_stream(count=5, interval=0.001, dims=2):
                results.append(record)
            return results

        results = asyncio.run(run())
        assert len(results) == 5
