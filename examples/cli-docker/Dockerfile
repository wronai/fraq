FROM python:3.11-slim

WORKDIR /app

# Install fraq with all dependencies
RUN pip install --no-cache-dir \
    fraq[ai] \
    fastapi \
    uvicorn

# Default command shows help
CMD ["fraq", "--help"]
