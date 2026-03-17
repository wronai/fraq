#!/usr/bin/env python3
"""
fraq — Przykłady integracji w aplikacjach.

FastAPI, Streamlit, Flask, Django, CLI, WebSocket, gRPC, Kafka.
"""

from __future__ import annotations

import json
from dataclasses import dataclass


def example_fastapi_app():
    """
    FastAPI application with fraq endpoints.
    Run: uvicorn fastapi_app:app --reload
    """
    print("=" * 60)
    print("1. FASTAPI INTEGRATION (code template)")
    print("=" * 60)

    code = '''
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fraq import FraqNode, FraqSchema, FraqQuery, FraqExecutor
from fraq.streaming import async_stream
import asyncio

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
    q = FraqQuery().zoom(depth).select(*fields.split(",")).output(fmt).take(limit)
    result = FraqExecutor(dims=3).execute(q)
    return {"format": fmt, "count": limit, "data": result}

@app.get("/stream")
async def stream_data(
    count: int = Query(100, ge=1, le=10000),
    interval: float = Query(0.1, gt=0),
):
    async def generate():
        async for record in async_stream(count=count, interval=interval):
            yield f"data: {json.dumps(record)}\\n\\n"
            await asyncio.sleep(interval)
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/zoom/{depth}")
def zoom(depth: int, direction: str = "0.5,0.5,0.5"):
    dir_tuple = tuple(float(x) for x in direction.split(","))
    root = FraqNode(position=(0.0, 0.0, 0.0))
    q = FraqQuery().zoom(depth, direction=dir_tuple).select("value:float").output("json")
    result = FraqExecutor(root).execute(q)
    return {"depth": depth, "direction": dir_tuple, "result": result}
'''
    print(code)
    print("\n  Endpoints:")
    print("    GET /query?fields=temperature:float&depth=3&format=json")
    print("    GET /stream?count=100&interval=0.1  # SSE")
    print("    GET /zoom/5?direction=0.1,0.2,0.7")
    print()


def example_streamlit_app():
    """
    Streamlit dashboard for fraq visualization.
    Run: streamlit run streamlit_app.py
    """
    print("=" * 60)
    print("2. STREAMLIT INTEGRATION (code template)")
    print("=" * 60)

    code = '''
import streamlit as st
import pandas as pd
from fraq import query, FraqQuery, FraqExecutor, SensorAdapter

st.set_page_config(page_title="Fraq Dashboard", layout="wide")
st.title("🌀 Fraq Data Explorer")

# Sidebar controls
with st.sidebar:
    st.header("Query Parameters")
    dims = st.slider("Dimensions", 2, 10, 3)
    depth = st.slider("Depth", 1, 10, 3)
    limit = st.slider("Limit", 10, 1000, 100)
    fmt = st.selectbox("Format", ["json", "csv", "yaml"])

# Query execution
if st.button("Generate Data"):
    with st.spinner("Generating fractal data..."):
        result = query(
            depth=depth,
            fields=["value:float", "depth:int", "seed:int"],
            format=fmt,
            limit=limit,
            dims=dims,
        )

    # Display results
    if fmt == "json":
        data = json.loads(result)
        df = pd.DataFrame(data)
        st.dataframe(df)
        st.line_chart(df["value"])
    else:
        st.text(result[:1000])

# Sensor simulation tab
tab1, tab2 = st.tabs(["Fractal Data", "Sensor Stream"])

with tab2:
    adapter = SensorAdapter(base_temp=23.5)
    readings = list(adapter.stream(count=50))
    df_sensor = pd.DataFrame(readings)
    st.line_chart(df_sensor[["temperature", "humidity"]])
'''
    print(code)
    print("\n  Features: sliders for dims/depth/limit, live charts, sensor simulation")
    print()


def example_flask_app():
    """
    Flask application with fraq blueprints.
    """
    print("=" * 60)
    print("3. FLASK INTEGRATION (code template)")
    print("=" * 60)

    code = '''
from flask import Flask, request, jsonify, Response
from fraq import query, text2fraq
from fraq.text2fraq import Text2FraqSimple

app = Flask(__name__)

@app.route("/api/v1/query", methods=["GET", "POST"])
def api_query():
    if request.method == "POST":
        data = request.get_json()
        nl_query = data.get("query", "")
        # Natural language to fraq
        result = text2fraq(nl_query)
        return jsonify({"query": nl_query, "result": result})
    else:
        # Direct parameters
        depth = request.args.get("depth", 3, type=int)
        fields = request.args.get("fields", "value:float").split(",")
        fmt = request.args.get("format", "json")
        limit = request.args.get("limit", 100, type=int)
        result = query(depth=depth, fields=fields, format=fmt, limit=limit)
        return Response(result, mimetype=f"application/{fmt}")

@app.route("/api/v1/nl/<path:text>")
def natural_language(text):
    """GET /api/v1/nl/show temperature readings as CSV"""
    parser = Text2FraqSimple()
    parsed = parser.parse(text.replace("/", " "))
    result = parsed.to_fraq_query()
    return jsonify({
        "parsed": {
            "fields": parsed.fields,
            "depth": parsed.depth,
            "format": parsed.format,
        },
        "result": result
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''
    print(code)
    print("\n  Endpoints:")
    print("    POST /api/v1/query {\"query\": \"show temperature in csv\"}")
    print("    GET  /api/v1/nl/show temperature readings")
    print()


def example_cli_chat():
    """
    Interactive CLI chatbot with fraq + text2fraq.
    """
    print("=" * 60)
    print("4. CLI CHATBOT (code template)")
    print("=" * 60)

    code = '''
import cmd
from fraq import text2fraq, Text2FraqSimple

class FraqShell(cmd.Cmd):
    intro = "🌀 Fraq Interactive Shell. Type 'help' or '?' to list commands.\\n"
    prompt = "fraq> "

    def __init__(self):
        super().__init__()
        self.parser = Text2FraqSimple()
        self.default_dims = 3

    def do_query(self, arg):
        """Execute natural language query: query show temperature"""
        if not arg:
            print("Usage: query <natural language>")
            return
        try:
            result = text2fraq(arg)
            print(result[:500])
        except Exception as e:
            print(f"Error: {e}")

    def do_raw(self, arg):
        """Execute raw fraq query: raw depth=3 fields=temperature:float format=csv"""
        from fraq import query
        params = dict(p.split("=") for p in arg.split())
        result = query(**params)
        print(result[:500])

    def do_set(self, arg):
        """Set default: set dims=5"""
        if arg.startswith("dims="):
            self.default_dims = int(arg.split("=")[1])
            print(f"Default dims set to {self.default_dims}")

    def do_exit(self, arg):
        return True

if __name__ == "__main__":
    FraqShell().cmdloop()
'''
    print(code)
    print("\n  Commands: query <nl>, raw <params>, set <key=value>, exit")
    print()


def example_websocket_server():
    """
    WebSocket server for real-time fraq streaming.
    """
    print("=" * 60)
    print("5. WEBSOCKET SERVER (code template - websockets)")
    print("=" * 60)

    code = '''
import asyncio
import websockets
import json
from fraq.streaming import async_stream

async def handler(websocket):
    async for message in websocket:
        data = json.loads(message)
        action = data.get("action")

        if action == "stream":
            count = data.get("count", 100)
            interval = data.get("interval", 0.1)

            async for record in async_stream(count=count, interval=interval):
                await websocket.send(json.dumps(record))

        elif action == "query":
            from fraq import query
            result = query(
                depth=data.get("depth", 3),
                fields=data.get("fields", ["value:float"]),
                format=data.get("format", "json"),
                limit=data.get("limit", 100),
            )
            await websocket.send(result)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
'''
    print(code)
    print("\n  WebSocket: ws://localhost:8765")
    print("  Actions: {\"action\": \"stream\", \"count\": 100}")
    print("           {\"action\": \"query\", \"depth\": 3, \"fields\": [\"temperature:float\"]}")
    print()


def example_kafka_producer():
    """
    Kafka producer/consumer with fraq streams.
    """
    print("=" * 60)
    print("6. KAFKA INTEGRATION (code template - aiokafka)")
    print("=" * 60)

    code = '''
import asyncio
import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from fraq.streaming import async_stream

KAFKA_TOPIC = "fraq.sensors"
KAFKA_BOOTSTRAP = "localhost:9092"

async def producer():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)
    await producer.start()

    try:
        async for record in async_stream(count=10000, interval=0.1):
            await producer.send(
                KAFKA_TOPIC,
                json.dumps(record).encode()
            )
    finally:
        await producer.stop()

async def consumer():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="fraq-processors",
    )
    await consumer.start()

    try:
        async for msg in consumer:
            data = json.loads(msg.value)
            # Process: alert if value > threshold
            if data.get("value", 0) > 0.8:
                print(f"ALERT: High value detected: {data}")
    finally:
        await consumer.stop()

# Run: asyncio.run(producer()) or asyncio.run(consumer())
'''
    print(code)
    print("\n  Producer: streams fraq data to Kafka topic")
    print("  Consumer: processes records with alerting")
    print()


def example_grpc_service():
    """
    gRPC service definition and implementation.
    """
    print("=" * 60)
    print("7. GRPC SERVICE (code template)")
    print("=" * 60)

    proto = '''
// fraq.proto
syntax = "proto3";

service FraqService {
  rpc Query(QueryRequest) returns (QueryResponse);
  rpc Stream(StreamRequest) returns (stream Record);
}

message QueryRequest {
  int32 depth = 1;
  repeated string fields = 2;
  string format = 3;
  int32 limit = 4;
}

message QueryResponse {
  string data = 1;
  int32 count = 2;
}

message StreamRequest {
  int32 count = 1;
  float interval = 2;
}

message Record {
  double value = 1;
  int32 depth = 2;
  repeated double position = 3;
}
'''
    print("Proto definition:")
    print(proto)

    impl = '''
# grpc_server.py
from concurrent import futures
import grpc
from fraq import query
from fraq.streaming import async_stream
import fraq_pb2
import fraq_pb2_grpc

class FraqServicer(fraq_pb2_grpc.FraqServiceServicer):
    def Query(self, request, context):
        result = query(
            depth=request.depth,
            fields=request.fields,
            format=request.format,
            limit=request.limit,
        )
        return fraq_pb2.QueryResponse(data=result, count=request.limit)

    async def Stream(self, request, context):
        async for record in async_stream(
            count=request.count,
            interval=request.interval
        ):
            yield fraq_pb2.Record(
                value=record["value"],
                depth=record["depth"],
                position=record.get("position", []),
            )

def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    fraq_pb2_grpc.add_FraqServiceServicer_to_server(FraqServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()
'''
    print("Implementation:")
    print(impl)
    print()


def example_jupyter_notebook():
    """
    Jupyter notebook cells for interactive exploration.
    """
    print("=" * 60)
    print("8. JUPYTER NOTEBOOK (code cells)")
    print("=" * 60)

    cells = '''
# Cell 1: Setup
import pandas as pd
import matplotlib.pyplot as plt
from fraq import query, FraqSchema, FraqNode, SensorAdapter

# Cell 2: Generate fractal data
result = query(
    depth=5,
    fields=["value:float", "depth:int"],
    format="json",
    limit=200,
    dims=3,
)
df = pd.DataFrame(result)
df.head()

# Cell 3: Visualize
df.plot(x="depth", y="value", kind="scatter", figsize=(10, 6))
plt.title("Fractal Values by Depth")
plt.show()

# Cell 4: Sensor simulation
adapter = SensorAdapter(base_temp=23.5)
sensor_df = pd.DataFrame(adapter.stream(count=100))
sensor_df[["temperature", "humidity"]].plot(figsize=(10, 6))
plt.title("Sensor Readings")
plt.show()

# Cell 5: Interactive widget
from ipywidgets import interact, IntSlider

@interact(depth=IntSlider(min=1, max=10, value=3))
def explore(depth):
    r = query(depth=depth, fields=["value:float"], limit=50)
    df = pd.DataFrame(r)
    return df["value"].describe()
'''
    print(cells)
    print("\n  Cells: setup → generate → visualize → sensor → interactive")
    print()


def example_celery_task():
    """
    Celery background tasks for fraq processing.
    """
    print("=" * 60)
    print("9. CELERY BACKGROUND TASKS (code template)")
    print("=" * 60)

    code = '''
from celery import Celery
from fraq import query, FraqSchema

app = Celery("fraq", broker="redis://localhost:6379/0")

@app.task
def generate_fractal_dataset(task_id: str, params: dict):
    """Background task to generate large fractal dataset."""
    result = query(
        depth=params.get("depth", 5),
        fields=params.get("fields", ["value:float"]),
        format=params.get("format", "json"),
        limit=params.get("limit", 10000),
        dims=params.get("dims", 3),
    )
    # Save to storage
    with open(f"/data/{task_id}.{params['format']}", "w") as f:
        f.write(result)
    return {"task_id": task_id, "records": params["limit"]}

@app.task
def process_sensor_stream(count: int, threshold: float):
    """Process sensor stream with alerting."""
    from fraq import SensorAdapter
    adapter = SensorAdapter()
    alerts = []
    for reading in adapter.stream(count=count):
        if reading["temperature"] > threshold:
            alerts.append(reading)
    return {"processed": count, "alerts": len(alerts)}

# Usage:
# generate_fractal_dataset.delay("task-123", {"depth": 5, "limit": 100000})
'''
    print(code)
    print("\n  Tasks: generate_fractal_dataset, process_sensor_stream")
    print("  Broker: Redis, Result: file storage / alerts")
    print()


# ═══════════════════════════════════════════════════════════════════════════
# RUN ALL
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    example_fastapi_app()
    example_streamlit_app()
    example_flask_app()
    example_cli_chat()
    example_websocket_server()
    example_kafka_producer()
    example_grpc_service()
    example_jupyter_notebook()
    example_celery_task()

    print("=" * 60)
    print("Dependencies for each integration:")
    print("=" * 60)
    print("""
FastAPI:     pip install fastapi uvicorn
Streamlit:   pip install streamlit pandas
Flask:       pip install flask
WebSocket:   pip install websockets
Kafka:       pip install aiokafka
gRPC:        pip install grpcio grpcio-tools
Celery:      pip install celery redis
Jupyter:     pip install jupyter ipywidgets pandas matplotlib

All at once: pip install fastapi uvicorn streamlit flask websockets aiokafka grpcio celery redis jupyter ipywidgets pandas matplotlib
""")
