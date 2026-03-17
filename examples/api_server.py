#!/usr/bin/env python3
"""
fraq REST API + WebSocket Server

Kompletny serwer z endpointami dla:
- Fractal queries (explore, stream, schema)
- File search (REST + WebSocket streaming)
- Natural language via text2fraq

Uruchomienie:
    pip install fastapi uvicorn
    uvicorn api_server:app --host 0.0.0.0 --port 8000

Lub:
    python api_server.py
"""

from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator

try:
    from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
    from fastapi.responses import JSONResponse, StreamingResponse
    from fastapi.middleware.cors import CORSMiddleware
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    print("FastAPI not installed. Run: pip install fastapi uvicorn")
    raise SystemExit(1)

from fraq import (
    FraqNode,
    FraqSchema,
    FraqQuery,
    FraqExecutor,
    FileSearchAdapter,
    FormatRegistry,
    HashGenerator,
)
from fraq.streaming import async_stream
from fraq.text2fraq import (
    Text2Fraq,
    Text2FraqConfig,
    FileSearchText2Fraq,
    HAS_LITELLM,
)


# ---------------------------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """App lifespan manager."""
    print("🌀 fraq API starting...")
    yield
    print("🌀 fraq API shutting down...")


app = FastAPI(
    title="fraq API",
    description="Fractal Query Data Library - REST + WebSocket API",
    version="0.2.1",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Health & Info
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    """API info."""
    return {
        "name": "fraq API",
        "version": "0.2.1",
        "endpoints": {
            "fractal": ["/explore", "/stream", "/query", "/schema"],
            "files": ["/files/search", "/files/list", "/files/stat/{path}"],
            "websocket": ["/ws/files", "/ws/stream"],
            "nl": ["/nl"],
        },
    }


@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok", "litellm": HAS_LITELLM}


# ---------------------------------------------------------------------------
# Fractal Endpoints
# ---------------------------------------------------------------------------

@app.get("/explore")
def explore(
    depth: int = Query(3, ge=1, le=20),
    dims: int = Query(3, ge=1, le=10),
    seed: int = Query(0),
    format: str = Query("json", regex="^(json|yaml|csv)$"),
):
    """Zoom into fractal at given depth."""
    pos = tuple(0.0 for _ in range(dims))
    root = FraqNode(position=pos, seed=seed, generator=HashGenerator())
    node = root.zoom(steps=depth)
    data = node.to_dict(max_depth=1)
    
    content = FormatRegistry.serialize(format, data)
    media_type = f"application/{format}" if format != "csv" else "text/csv"
    return StreamingResponse(
        iter([content]),
        media_type=media_type,
        headers={"X-Fractal-Depth": str(depth)},
    )


@app.get("/stream")
def stream(
    count: int = Query(10, ge=1, le=10000),
    dims: int = Query(3, ge=1, le=10),
    format: str = Query("jsonl", regex="^(json|jsonl|csv)$"),
):
    """Stream cursor records."""
    pos = tuple(0.0 for _ in range(dims))
    root = FraqNode(position=pos, generator=HashGenerator())
    cursor = root.cursor()
    
    records = []
    for _ in range(count):
        cursor.advance()
        records.append({
            "value": cursor.current.value,
            "depth": cursor.depth,
            "position": cursor.current.position,
        })
    
    if format == "jsonl":
        lines = "\n".join(json.dumps(r) for r in records)
        return StreamingResponse(iter([lines]), media_type="application/x-ndjson")
    
    content = FormatRegistry.serialize(format, records)
    return StreamingResponse(iter([content]), media_type=f"application/{format}")


@app.get("/query")
def query_data(
    fields: str = Query("value:float"),
    depth: int = Query(3, ge=1, le=20),
    format: str = Query("json", regex="^(json|csv|yaml|jsonl)$"),
    limit: int = Query(100, ge=1, le=10000),
    dims: int = Query(3, ge=1, le=10),
):
    """Execute fractal query with typed fields."""
    pos = tuple(0.0 for _ in range(dims))
    root = FraqNode(position=pos)
    
    field_list = [f.strip() for f in fields.split(",")]
    q = FraqQuery().zoom(depth).select(*field_list).output(format).take(limit)
    result = FraqExecutor(root).execute(q)
    
    return StreamingResponse(
        iter([result] if isinstance(result, str) else [json.dumps(result)]),
        media_type=f"application/{format}",
    )


@app.get("/schema")
def schema_records(
    fields: str = Query(..., description="Comma-separated name:type"),
    depth: int = Query(2, ge=1, le=10),
    branching: int = Query(3, ge=1, le=10),
    format: str = Query("json"),
    dims: int = Query(3),
):
    """Generate typed schema records."""
    pos = tuple(0.0 for _ in range(dims))
    root = FraqNode(position=pos)
    schema = FraqSchema(root=root)
    
    for spec in fields.split(","):
        name, _, typ = spec.partition(":")
        schema.add_field(name.strip(), typ.strip() or "float")
    
    records = list(schema.records(depth=depth, branching=branching))
    content = FormatRegistry.serialize(format, records)
    
    return StreamingResponse(iter([content]), media_type=f"application/{format}")


# ---------------------------------------------------------------------------
# File Endpoints (REST)
# ---------------------------------------------------------------------------

@app.get("/files/search")
def files_search(
    path: str = Query(".", description="Base directory path"),
    ext: str | None = Query(None, description="File extension (pdf, txt, py...)"),
    pattern: str | None = Query(None, description="Glob pattern (*.pdf)"),
    limit: int = Query(10, ge=1, le=1000),
    sort: str = Query("mtime", regex="^(name|mtime|size)$"),
    recursive: bool = Query(True),
    format: str = Query("json", regex="^(json|csv|yaml)$"),
):
    """Search files with fractal metadata."""
    try:
        adapter = FileSearchAdapter(
            base_path=path,
            pattern=pattern or "*",
            recursive=recursive,
        )
        results = adapter.search(
            extension=ext,
            pattern=pattern,
            limit=limit,
            sort_by=sort,
        )
        
        content = FormatRegistry.serialize(format, results)
        return StreamingResponse(
            iter([content]),
            media_type=f"application/{format}",
            headers={"X-Total-Results": str(len(results))},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files/list")
def files_list(
    path: str = Query("."),
    ext: str | None = Query(None),
    limit: int = Query(50, ge=1, le=1000),
    sort: str = Query("name"),
    recursive: bool = Query(False),
):
    """List files (ls-style)."""
    try:
        adapter = FileSearchAdapter(base_path=path, recursive=recursive)
        results = adapter.search(extension=ext, limit=limit, sort_by=sort)
        return {
            "path": path,
            "count": len(results),
            "files": [r["filename"] for r in results],
            "details": results,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files/stat/{file_path:path}")
def files_stat(file_path: str):
    """Get file statistics with fractal coordinates."""
    path = Path(file_path).expanduser()
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    
    stat = path.stat()
    return {
        "filename": path.name,
        "path": str(path.absolute()),
        "extension": path.suffix.lstrip(".").lower() if path.suffix else "",
        "size": stat.st_size,
        "size_human": f"{stat.st_size / 1024:.2f} KB" if stat.st_size < 1024*1024 else f"{stat.st_size / (1024*1024):.2f} MB",
        "mtime": stat.st_mtime,
        "mtime_human": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "ctime": stat.st_ctime,
        "atime": stat.st_atime,
        "fraq": {
            "position": [
                float(stat.st_size) / (1024 * 1024),
                float(stat.st_mtime),
                float(stat.st_ctime),
            ],
            "seed": hash(str(path)) % (2**32),
            "value": hash(str(path)) / (2**32),
        }
    }


# ---------------------------------------------------------------------------
# Natural Language Endpoint
# ---------------------------------------------------------------------------

@app.post("/nl")
def natural_language(
    query: str,
    path: str = Query("."),
    format: str = Query("json"),
):
    """Process natural language query (requires LLM)."""
    if not HAS_LITELLM:
        raise HTTPException(status_code=503, detail="LLM not available. Install: pip install litellm")
    
    # Check if file query
    file_keywords = ["file", "files", "pdf", "txt", "document", "folder", "directory", "plik"]
    is_file_query = any(kw in query.lower() for kw in file_keywords)
    
    try:
        if is_file_query:
            searcher = FileSearchText2Fraq(path)
            results = searcher.search(query)
            return {"query": query, "type": "files", "results": results}
        else:
            config = Text2FraqConfig.from_env()
            t2f = Text2Fraq(config)
            result = t2f.execute(query)
            return {"query": query, "type": "fractal", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# WebSocket Endpoints
# ---------------------------------------------------------------------------

@app.websocket("/ws/stream")
async def ws_stream(websocket: WebSocket):
    """WebSocket streaming of fractal data."""
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_json()
            action = msg.get("action", "stream")
            
            if action == "stream":
                count = msg.get("count", 10)
                interval = msg.get("interval", 0.1)
                
                async for record in async_stream(count=count, interval=interval):
                    await websocket.send_json(record)
                    await asyncio.sleep(interval)
                    
            elif action == "ping":
                await websocket.send_json({"pong": True})
                
    except WebSocketDisconnect:
        print("WS client disconnected")


@app.websocket("/ws/files")
async def ws_files(websocket: WebSocket):
    """WebSocket for file search streaming."""
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_json()
            action = msg.get("action")
            
            if action == "search":
                path = msg.get("path", ".")
                ext = msg.get("ext")
                pattern = msg.get("pattern")
                limit = msg.get("limit", 10)
                
                adapter = FileSearchAdapter(base_path=path, recursive=True)
                
                # Stream results one by one
                for record in adapter.stream(extension=ext, pattern=pattern, count=limit):
                    await websocket.send_json(record)
                    await asyncio.sleep(0.01)  # Small delay for flow control
                    
                await websocket.send_json({"done": True, "count": limit})
                
            elif action == "stat":
                file_path = msg.get("file")
                path = Path(file_path).expanduser()
                if path.exists():
                    stat = path.stat()
                    await websocket.send_json({
                        "file": str(path),
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                    })
                else:
                    await websocket.send_json({"error": "File not found"})
                    
    except WebSocketDisconnect:
        print("WS files client disconnected")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
