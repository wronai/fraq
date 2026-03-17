"""FastAPI server for fraq - production-ready API.

Install optional dependencies:
    pip install fastapi uvicorn pydantic

Run server:
    python -m fraq.server
    # or
    uvicorn fraq.server:app --reload
"""

from __future__ import annotations

from typing import Any, List, Optional

try:
    from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
    from pydantic import BaseModel
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    # Dummy classes for type checking
    class FastAPI:  # type: ignore
        def __init__(self, **kwargs): pass
    class HTTPException(Exception):  # type: ignore
        pass
    class WebSocket:  # type: ignore
        pass
    class WebSocketDisconnect(Exception):  # type: ignore
        pass
    class BaseModel:  # type: ignore
        pass

try:
    from fraq.text2fraq import Text2Fraq, Text2FraqConfig, FileSearchText2Fraq
    from fraq.text2fraq.router import ModelRouter
    from fraq.text2fraq.session import FraqSession
    from fraq.adapters.file_search import FileSearchAdapter
except ImportError:
    # Allow import of module even without dependencies
    pass

if not HAS_FASTAPI:
    # Create dummy app for import
    app = FastAPI()
else:
    app = FastAPI(
        title="fraq API",
        description="Fractal Query Data Library - Natural Language to Structured Data",
        version="0.2.8",
    )

    # In-memory session store (use Redis in production)
    sessions: dict[str, FraqSession] = {}


class NLQueryRequest(BaseModel):
    """Natural language query request."""
    query: str
    path: str = "."
    session_id: Optional[str] = None


class NLQueryResponse(BaseModel):
    """Natural language query response."""
    result: Any
    session_id: Optional[str] = None
    model_used: Optional[str] = None


class FilesSearchRequest(BaseModel):
    """File search request."""
    extension: Optional[str] = None
    pattern: Optional[str] = None
    limit: int = 10
    sort_by: str = "name"
    path: str = "."


@app.post("/nl", response_model=NLQueryResponse)
async def natural_language(query: NLQueryRequest) -> NLQueryResponse:
    """Natural language → fraq result with session support."""
    # Get or create session
    session_id = query.session_id
    if session_id and session_id in sessions:
        session = sessions[session_id]
    else:
        session = FraqSession()
        session_id = f"sess_{len(sessions)}"
        sessions[session_id] = session

    # Route to appropriate model based on complexity
    router = ModelRouter()
    model = router.route(query.query)
    config = Text2FraqConfig.from_env()
    config.model = model.split("/")[1] if "/" in model else model

    # Update session parser with routed model
    session.parser = Text2Fraq(config)

    # Execute query
    result = session.ask(query.query)

    return NLQueryResponse(
        result=result,
        session_id=session_id,
        model_used=model,
    )


@app.get("/files/search")
async def files_search(
    ext: Optional[str] = None,
    pattern: Optional[str] = None,
    limit: int = 10,
    sort_by: str = "name",
    path: str = ".",
) -> List[dict]:
    """Search files with fractal coordinates."""
    adapter = FileSearchAdapter(base_path=path)
    return adapter.search(
        extension=ext,
        pattern=pattern,
        limit=limit,
        sort_by=sort_by,
    )


@app.post("/files/search")
async def files_search_post(request: FilesSearchRequest) -> List[dict]:
    """Search files with POST request."""
    adapter = FileSearchAdapter(base_path=request.path)
    return adapter.search(
        extension=request.extension,
        pattern=request.pattern,
        limit=request.limit,
        sort_by=request.sort_by,
    )


@app.get("/files/nl")
async def files_nl(query: str, path: str = ".") -> str:
    """Natural language file search."""
    searcher = FileSearchText2Fraq(base_path=path)
    results = searcher.search(query)
    return searcher.format_results(results, "json")


@app.websocket("/stream")
async def ws_stream(websocket: WebSocket):
    """WebSocket endpoint for streaming fractal data."""
    await websocket.accept()
    try:
        from fraq.core import FraqCursor, FraqNode
        from fraq.generators import HashGenerator

        root = FraqNode(
            position=(0.0, 0.0, 0.0),
            seed=0,
            generator=HashGenerator(),
        )
        cursor = FraqCursor(root=root)

        count = 0
        while True:
            # Receive command from client
            data = await websocket.receive_json()
            cmd = data.get("cmd", "next")

            if cmd == "next":
                steps = data.get("steps", 1)
                for _ in range(steps):
                    cursor.advance()
                    count += 1
                    await websocket.send_json({
                        "index": count,
                        "position": cursor.current.position,
                        "value": cursor.current.value,
                    })
            elif cmd == "stop":
                break
            elif cmd == "zoom":
                depth = data.get("depth", 3)
                node = root.zoom(steps=depth)
                await websocket.send_json({
                    "zoom_depth": depth,
                    "data": node.to_dict(),
                })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.2.8",
        "sessions_active": len(sessions),
    }


@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str) -> dict:
    """Clear a conversation session."""
    if session_id in sessions:
        del sessions[session_id]
        return {"status": "cleared", "session_id": session_id}
    raise HTTPException(status_code=404, detail="Session not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
