"""
FastAPI integration example for fraq.

Run: uvicorn fastapi_example:app --reload
"""

from __future__ import annotations

import asyncio
import json

from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse

from fraq import FraqNode, FraqSchema, FraqQuery, FraqExecutor
from fraq.streaming import async_stream


app = FastAPI(title="Fraq API", version="1.0")


@app.get("/")
def root():
    return {"message": "Fractal Query API", "docs": "/docs"}


@app.get("/query")
def query_data(
    fields: str = Query("temperature:float,humidity:float"),
    depth: int = Query(3, ge=1, le=20),
    fmt: str = Query("json", regex="^(json|csv|yaml|jsonl)$"),
    limit: int = Query(100, ge=1, le=10000),
):
    """Query fractal data with typed fields."""
    q = (
        FraqQuery()
        .zoom(depth)
        .select(*fields.split(","))
        .output(fmt)
        .take(limit)
    )
    result = FraqExecutor(dims=3).execute(q)
    return {"format": fmt, "count": limit, "data": result}


@app.get("/stream")
async def stream_data(
    count: int = Query(100, ge=1, le=10000),
    interval: float = Query(0.1, gt=0),
):
    """Stream fractal records via SSE."""
    async def generate():
        async for record in async_stream(count=count, interval=interval):
            yield f"data: {json.dumps(record)}\n\n"
            await asyncio.sleep(interval)
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/zoom/{depth}")
def zoom(depth: int, direction: str = "0.5,0.5,0.5"):
    """Zoom into fractal at given depth and direction."""
    dir_tuple = tuple(float(x) for x in direction.split(","))
    root = FraqNode(position=(0.0, 0.0, 0.0))
    q = (
        FraqQuery()
        .zoom(depth, direction=dir_tuple)
        .select("value:float")
        .output("json")
    )
    result = FraqExecutor(root).execute(q)
    return {"depth": depth, "direction": dir_tuple, "result": result}


@app.post("/generate")
def generate_data(
    fields: dict,
    count: int = Query(100, ge=1, le=10000),
    seed: int = Query(42, ge=0),
):
    """Generate synthetic data with fraq."""
    from fraq import generate
    
    records = generate(fields, count=count, seed=seed, output="list")
    return {"count": len(records), "data": records}
