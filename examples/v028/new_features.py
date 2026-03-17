"""Examples of new fraq v0.3.0 features.

ModelRouter - intelligent model selection
FraqSession - multi-turn conversations
FastAPI server - production API
"""

from __future__ import annotations


def example_model_router():
    """Example: ModelRouter routes queries to optimal models."""
    from fraq.text2fraq import ModelRouter

    router = ModelRouter()

    # Simple queries get fast, small model
    query1 = "find pdf files"
    model1 = router.route(query1)
    print(f"'{query1}' → {model1}")
    # Output: 'find pdf files' → ollama/qwen2.5:0.5b

    # Medium complexity gets balanced model
    query2 = "search recent documents with filters"
    model2 = router.route(query2)
    print(f"'{query2}' → {model2}")
    # Output: 'search recent documents with filters' → ollama/qwen2.5:3b

    # Complex schema generation gets large model
    query3 = "generate complex nested schema with relationships"
    model3 = router.route(query3)
    print(f"'{query3}' → {model3}")
    # Output: 'generate complex nested schema with relationships' → ollama/qwen2.5:7b

    # Get config for selected model
    config = router.get_config_for_model(model3)
    print(f"Config: {config}")
    # Output: Config: {'temperature': 0.05, 'max_tokens': 1024, 'timeout': 60}


def example_fraq_session():
    """Example: FraqSession for multi-turn conversations."""
    from fraq.text2fraq import FraqSession

    # Create session
    session = FraqSession(max_history=5)

    # First query
    result1 = session.ask("find 10 pdf files created last week")
    print(f"Query 1: {len(session.history)} items in history")

    # Follow-up: change format (reuses last query)
    result2 = session.ask("show as csv")
    print(f"Query 2: format changed to csv")

    # Another follow-up: add more results
    result3 = session.ask("show 20 more files")
    print(f"Query 3: limit increased")

    # Check context
    summary = session.get_context_summary()
    print(f"Context: {summary}")

    # Clear session
    session.clear()
    print(f"After clear: {len(session.history)} items")


def example_fastapi_server():
    """Example: Running FastAPI server."""
    print("""
    # Install dependencies
    pip install fastapi uvicorn pydantic

    # Run server
    uvicorn fraq.server:app --reload

    # Or from Python
    from fraq.server import app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Endpoints:
    # POST /nl          - Natural language query with session
    # GET  /files/search - Search files
    # POST /files/search - Search files (POST)
    # GET  /files/nl     - NL file search
    # WS   /stream       - WebSocket streaming
    # GET  /health       - Health check
    # DELETE /sessions/{id} - Clear session

    # Example curl:
    curl -X POST http://localhost:8000/nl \\
        -H "Content-Type: application/json" \\
        -d '{"query": "find pdf files", "path": "/docs"}'
    """)


def example_combined_usage():
    """Example: Combining all features."""
    from fraq.text2fraq import ModelRouter, FraqSession, Text2FraqConfig

    # Setup router and session
    router = ModelRouter()
    session = FraqSession()

    # Route query to best model
    query = "generate schema for sensor data"
    model = router.route(query)
    print(f"Routed to: {model}")

    # Configure parser with routed model
    config = Text2FraqConfig.from_env()
    config.model = model.split("/")[1]

    # Update session and execute
    from fraq.text2fraq.parser_llm import Text2Fraq
    session.parser = Text2Fraq(config)
    result = session.ask(query)

    print(f"Result: {result[:100]}...")
    print(f"Session history: {len(session.history)} queries")


if __name__ == "__main__":
    print("=" * 50)
    print("Example 1: ModelRouter")
    print("=" * 50)
    example_model_router()

    print("\n" + "=" * 50)
    print("Example 2: FraqSession")
    print("=" * 50)
    example_fraq_session()

    print("\n" + "=" * 50)
    print("Example 3: FastAPI Server")
    print("=" * 50)
    example_fastapi_server()

    print("\n" + "=" * 50)
    print("Example 4: Combined Usage")
    print("=" * 50)
    example_combined_usage()
