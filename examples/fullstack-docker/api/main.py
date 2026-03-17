"""
Fullstack - API service
"""
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from fraq import FileSearchAdapter, FraqNode
from fraq.generators import HashGenerator

app = FastAPI(title="fraq Fullstack API")


@app.get("/")
def root():
    return {"service": "api", "version": "0.2.2"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/explore")
def explore(depth: int = Query(3)):
    root = FraqNode(position=(0.0, 0.0, 0.0), generator=HashGenerator())
    node = root.zoom(steps=depth)
    return JSONResponse(content=node.to_dict(max_depth=1))


@app.get("/files/search")
def files_search(
    path: str = Query("/data"),
    ext: str | None = Query(None),
    limit: int = Query(10),
):
    adapter = FileSearchAdapter(base_path=path, recursive=True)
    results = adapter.search(extension=ext, limit=limit, sort_by="mtime")
    return {"count": len(results), "files": results}
