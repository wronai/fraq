FROM python:3.11-slim

WORKDIR /app

# Install fraq with all extras
RUN pip install --no-cache-dir \
    fraq[ai] \
    fastapi \
    uvicorn \
    python-multipart

# Copy local fraq if developing (optional)
# COPY . /fraq-local
# RUN pip install /fraq-local[ai]

# Create simple API for docker-compose
COPY > main.py << 'EOF'
from fastapi import FastAPI, Query
from fraq import FileSearchAdapter, FraqNode
from fraq.generators import HashGenerator
import os

app = FastAPI(title="fraq Docker")
DIMS = int(os.getenv("FRAQ_DIMS", "3"))

@app.get("/health")
def health():
    return {"status": "ok", "dims": DIMS}

@app.get("/")
def root():
    return {"service": "fraq", "version": "0.2.2", "dims": DIMS}

@app.get("/files/search")
def files_search(
    path: str = Query("/host/home"),
    ext: str | None = Query(None),
    limit: int = Query(10),
):
    adapter = FileSearchAdapter(base_path=path, recursive=True)
    results = adapter.search(extension=ext, limit=limit, sort_by="mtime")
    return {"count": len(results), "files": results}

@app.get("/explore")
def explore(depth: int = Query(3)):
    root = FraqNode(position=(0.0, 0.0, 0.0), generator=HashGenerator())
    node = root.zoom(steps=depth)
    return node.to_dict(max_depth=1)
EOF

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
