from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "alerts.db"

st.set_page_config(page_title="AI IDS Dashboard", layout="wide")
st.title("AI-Powered Intrusion Detection Dashboard")

if DB_PATH.exists():
    with sqlite3.connect(DB_PATH) as connection:
        alerts = pd.read_sql_query(
            """
            SELECT id, event_type, category, confidence, source_ip, details, risk_score, created_at
            FROM alerts
            ORDER BY id DESC
            LIMIT 25
            """,
            connection,
        )
    if not alerts.empty:
        st.subheader("Recent alerts")
        st.dataframe(alerts, width="stretch")
        st.subheader("Alert counts by category")
        counts = alerts["category"].value_counts().rename_axis("category").reset_index(name="count")
        st.bar_chart(counts.set_index("category")["count"])
    else:
        st.info("No intrusion alerts have been logged yet.")
else:
    st.info("The alert database is not ready. Run the API or training pipeline first.")
