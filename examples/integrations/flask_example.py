"""
Flask integration example for fraq.

Run: flask --app flask_example run
"""

from __future__ import annotations

import json

from flask import Flask, jsonify, request, Response

from fraq import generate, stream, FraqSchema


app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "Fraq Flask API", "version": "1.0"})


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """Generate fractal data."""
    data = request.get_json() or {}
    fields = data.get("fields", {"value": "float"})
    count = data.get("count", 100)
    seed = data.get("seed", 42)
    
    records = generate(fields, count=count, seed=seed)
    return jsonify({"count": len(records), "data": records})


@app.route("/api/stream")
def api_stream():
    """Stream fractal data."""
    count = request.args.get("count", 100, type=int)
    interval = request.args.get("interval", 0.1, type=float)
    
    def generate_stream():
        for record in stream({"value": "float"}, count=count, interval=interval):
            yield f"data: {json.dumps(record)}\n\n"
    
    return Response(generate_stream(), mimetype="text/event-stream")


@app.route("/api/schema", methods=["GET", "POST"])
def api_schema():
    """Get or create schema."""
    if request.method == "POST":
        data = request.get_json() or {}
        fields = data.get("fields", {})
        
        schema = FraqSchema()
        for name, type_spec in fields.items():
            schema.add_field(name, type_spec)
        
        return jsonify({
            "fields": [f.name for f in schema.fields],
            "field_count": len(schema.fields),
        })
    
    return jsonify({"message": "Use POST to create schema"})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "fraq-flask"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
