#!/usr/bin/env python3
"""
App integration examples have moved to examples/integrations/

The examples from this file are now available as separate modules:
- examples/integrations/fastapi_example.py     - FastAPI REST API with SSE
- examples/integrations/flask_example.py       - Flask web API
- examples/integrations/streamlit_example.py   - Interactive dashboard
- examples/integrations/websocket_example.py    - WebSocket server/client
- examples/integrations/grpc_example.py        - gRPC with protobuf
- examples/integrations/kafka_example.py       - Kafka streaming
- examples/integrations/jupyter_example.py     - Jupyter notebooks
- examples/integrations/cli_chat_example.py    - Interactive CLI

This file is deprecated and will be removed in v0.4.
"""

import warnings

warnings.warn(
    "examples/basic/app_integrations.py is deprecated. "
    "Use examples/integrations/*.py instead",
    DeprecationWarning,
    stacklevel=2
)

# Redirect imports to new location
try:
    from fraq.examples.integrations.fastapi_example import app as fastapi_app
    from fraq.examples.integrations.flask_example import app as flask_app
except ImportError:
    pass

if __name__ == "__main__":
    print("=" * 60)
    print("⚠️  DEPRECATED: examples/basic/app_integrations.py")
    print("=" * 60)
    print()
    print("Examples have moved to examples/integrations/:")
    print()
    print("  fastapi_example.py      - FastAPI with streaming")
    print("  flask_example.py        - Flask API")
    print("  streamlit_example.py    - Dashboard")
    print("  websocket_example.py    - WebSocket chat")
    print("  grpc_example.py         - gRPC/Protobuf")
    print("  kafka_example.py        - Kafka streaming")
    print("  jupyter_example.py      - Notebooks")
    print("  cli_chat_example.py     - Interactive CLI")
    print()
    print("See each file for usage instructions.")
    print("=" * 60)
