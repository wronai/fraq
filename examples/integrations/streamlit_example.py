"""
Streamlit dashboard for fraq visualization.

Run: streamlit run streamlit_example.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from fraq import generate, FraqSchema


st.set_page_config(page_title="Fraq Dashboard", layout="wide")
st.title("🌀 Fraq Data Explorer")


# Sidebar controls
with st.sidebar:
    st.header("Query Parameters")
    dims = st.slider("Dimensions", 2, 10, 3)
    depth = st.slider("Depth", 1, 10, 3)
    limit = st.slider("Limit", 10, 1000, 100)
    fmt = st.selectbox("Format", ["json", "csv", "yaml"])
    
    st.header("Fields")
    temp_range = st.slider("Temperature range", 0.0, 100.0, (10.0, 40.0))
    humidity_range = st.slider("Humidity range", 0.0, 100.0, (30.0, 80.0))


# Query execution
if st.button("Generate Data"):
    with st.spinner("Generating fractal data..."):
        fields = {
            'temperature': f'float:{temp_range[0]}-{temp_range[1]}',
            'humidity': f'float:{humidity_range[0]}-{humidity_range[1]}',
            'sensor_id': 'str',
        }
        records = generate(fields, count=limit, seed=42)
        df = pd.DataFrame(records)
    
    st.success(f"Generated {len(records)} records")
    
    # Display as table
    st.subheader("Data Preview")
    st.dataframe(df.head(20))
    
    # Statistics
    st.subheader("Statistics")
    st.write(df.describe())
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Temperature Distribution")
        st.line_chart(df['temperature'])
    
    with col2:
        st.subheader("Humidity Distribution")
        st.line_chart(df['humidity'])
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="fraq_data.csv",
        mime="text/csv"
    )
