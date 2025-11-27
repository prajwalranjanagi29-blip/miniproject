import streamlit as st
import pandas as pd
from pathlib import Path

DATA = Path("data/mood_logs.csv")

st.set_page_config(page_title="History", page_icon="📅", layout="wide")
st.title("📅 Journal History")

if not DATA.exists():
    st.warning("No data found.")
    st.stop()

df = pd.read_csv(DATA)
df["timestamp"] = pd.to_datetime(df["timestamp"])

st.dataframe(df, use_container_width=True)

if st.button("🗑️ Delete All Entries", type="primary"):
    DATA.unlink()
    st.success("All entries deleted. Restart app.")
    st.experimental_rerun()

