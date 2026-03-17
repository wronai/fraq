"""
FastAPI + fraq Docker example
Minimal REST API for fractal queries and file search
"""

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import os

from fraq import FileSearchAdapter, FraqNode, FraqExecutor, FraqQuery
from fraq.generators import HashGenerator
from fraq.formats import FormatRegistry

app = FastAPI(title="fraq Docker API", version="0.2.2")

# Config from env
FRAQ_DIMS = int(os.getenv("FRAQ_DIMS", "3"))
FRAQ_SEED = int(os.getenv("FRAQ_SEED", "0"))


@app.get("/")
def root():
    return {"service": "fraq-docker", "version": "0.2.2", "dims": FRAQ_DIMS}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/explore")
def explore(
    depth: int = Query(3, ge=1, le=20),
    dims: int = Query(FRAQ_DIMS, ge=1, le=10),
    format: str = Query("json"),
):
    """Explore fractal structure"""
    pos = tuple(0.0 for _ in range(dims))
    root = FraqNode(position=pos, seed=FRAQ_SEED, generator=HashGenerator())
    node = root.zoom(steps=depth)
    data = node.to_dict(max_depth=1)
    return JSONResponse(content=data)


@app.get("/files/search")
def files_search(
    path: str = Query("/host/home", description="Directory to search"),
    ext: str | None = Query(None, description="File extension"),
    limit: int = Query(10, ge=1, le=1000),
    sort: str = Query("mtime", regex="^(name|mtime|size)$"),
):
    """Search files with fractal metadata"""
    try:
        adapter = FileSearchAdapter(base_path=path, recursive=True)
        results = adapter.search(extension=ext, limit=limit, sort_by=sort)
        return {"path": path, "count": len(results), "files": results}
    except Exception as e:
        return {"error": str(e)}


@app.get("/files/stat/{file_path:path}")
def files_stat(file_path: str):
    """Get file statistics with fractal coordinates"""
    from pathlib import Path
    from datetime import datetime
    
    path = Path(file_path)
    if not path.exists():
        return {"error": "File not found"}
    
    stat = path.stat()
    return {
        "filename": path.name,
        "path": str(path.absolute()),
        "size": stat.st_size,
        "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "fraq": {
            "seed": hash(str(path)) % (2**32),
            "value": hash(str(path)) / (2**32),
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
