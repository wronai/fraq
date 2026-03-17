"""
Fullstack - Streamlit Frontend
"""
import streamlit as st
import requests
import json
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")
WS_URL = os.getenv("WS_URL", "ws://localhost:8001")

st.set_page_config(page_title="fraq UI", layout="wide")

st.title("🌀 fraq — Fractal Query Data Library")

# Sidebar
st.sidebar.header("Konfiguracja")
path = st.sidebar.text_input("Ścieżka", "/data")
ext_filter = st.sidebar.text_input("Rozszerzenie", "py")
limit = st.sidebar.slider("Limit", 1, 100, 10)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Wyszukiwanie plików", "🌐 API REST", "ℹ️ Info"])

with tab1:
    st.subheader("Wyszukiwanie plików")
    if st.button("Szukaj"):
        try:
            resp = requests.get(f"{API_URL}/files/search", params={
                "path": path, "ext": ext_filter or None, "limit": limit
            })
            data = resp.json()
            if data.get("files"):
                st.write(f"Znaleziono {data['count']} plików:")
                for f in data["files"]:
                    st.code(f"{f['filename']} ({f['size']} bytes)")
            else:
                st.warning("Brak wyników")
        except Exception as e:
            st.error(f"Błąd: {e}")

with tab2:
    st.subheader("Test API")
    st.code(f"GET {API_URL}/health", language="bash")
    try:
        health = requests.get(f"{API_URL}/health").json()
        st.json(health)
    except Exception as e:
        st.error(f"API niedostępne: {e}")

with tab3:
    st.subheader("API Endpoints")
    st.markdown("""
    - `GET /health` — Health check
    - `GET /explore?depth=3` — Eksploracja fraktala
    - `GET /files/search?ext=pdf&limit=10` — Wyszukiwanie plików
    - `WS /ws/stream` — WebSocket streaming
    """)
    st.info(f"API URL: {API_URL}")
    st.info(f"WebSocket URL: {WS_URL}")
