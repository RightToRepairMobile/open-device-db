import streamlit as st
import sqlite3
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="Open Device DB", layout="wide", page_icon="🛠️")
st.title("🛠️ Open Device Repair & Info Database")
st.markdown("**Community-powered specs, repair guides, firmware & warnings**")

DB_PATH = "device_database.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Sidebar Filters
st.sidebar.header("🔍 Filters")
brand_filter = st.sidebar.text_input("Brand")
model_filter = st.sidebar.text_input("Model")
min_repair_score = st.sidebar.slider("Min Repairability Score", 0.0, 10.0, 0.0)
tag_filter = st.sidebar.text_input("Tags (comma separated)")

conn = get_connection()

# Build query
query = """
    SELECT id, brand, model_name, model_number, repairability_score, 
           eol_status, tags, last_updated 
    FROM devices
"""
conditions = []
params = []

if brand_filter:
    conditions.append("brand LIKE ?")
    params.append(f"%{brand_filter}%")
if model_filter:
    conditions.append("model_name LIKE ?")
    params.append(f"%{model_filter}%")
if min_repair_score > 0:
    conditions.append("repairability_score >= ?")
    params.append(min_repair_score)
if tag_filter:
    tags = [t.strip() for t in tag_filter.split(",")]
    for tag in tags:
        conditions.append("tags LIKE ?")
        params.append(f"%{tag}%")

if conditions:
    query += " WHERE " + " AND ".join(conditions)

query += " ORDER BY repairability_score DESC, brand"

df = pd.read_sql(query, conn, params=params)

st.dataframe(
    df, 
    use_container_width=True,
    column_config={
        "repairability_score": st.column_config.ProgressColumn("Repair Score", format="%.1f", min_value=0, max_value=10)
    }
)

st.write(f"**{len(df)} devices found**")

# Detailed View
if not df.empty:
    selected_id = st.selectbox("View details for:", df["id"], format_func=lambda x: f"{df[df['id']==x]['brand'].values[0]} {df[df['id']==x]['model_name'].values[0]}")
    
    if selected_id:
        detail = conn.execute("SELECT * FROM devices WHERE id = ?", (selected_id,)).fetchone()
        if detail:
            st.subheader(f"{detail['brand']} {detail['model_name']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.json(json.loads(detail['specs'] or '{}'), expanded=False)
                if detail['red_flags_warnings']:
                    st.warning("⚠️ Red Flags: " + detail['red_flags_warnings'])
            with col2:
                st.write("**Repairability:**", detail['repairability_score'])
                if detail['repair_youtube_links']:
                    st.write("🔧 Repair Videos:", detail['repair_youtube_links'])
                st.write("**Last Updated:**", detail['last_updated'])

# Add New Device (improved)
with st.expander("➕ Add New Device"):
    with st.form("add_device"):
        col1, col2 = st.columns(2)
        with col1:
            brand = st.text_input("Brand*")
            model_name = st.text_input("Model Name*")
            model_number = st.text_input("Model Number")
        with col2:
            release_date = st.date_input("Release Date", value=None)
            repair_score = st.slider("Initial Repairability Score", 0.0, 10.0, 5.0)
        
        if st.form_submit_button("Add Device"):
            if brand and model_name:
                conn.execute("""
                    INSERT INTO devices (brand, model_name, model_number, release_date, repairability_score)
                    VALUES (?, ?, ?, ?, ?)
                """, (brand, model_name, model_number, str(release_date) if release_date else None, repair_score))
                conn.commit()
                st.success(f"✅ {brand} {model_name} added!")
            else:
                st.error("Brand and Model Name required")

conn.close()

st.sidebar.markdown("---")
st.sidebar.info("💡 Run `python populate_agent.py` to auto-fill missing data")
st.caption("Open Device DB • Right to Repair Community Project")
