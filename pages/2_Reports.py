import streamlit as st
import pandas as pd
from pathlib import Path

DATA = Path("data/mood_logs.csv")

st.set_page_config(page_title="Reports", page_icon="📁", layout="wide")
st.title("📁 Reports & Insights")

if not DATA.exists():
    st.warning("⚠️ No records found.")
    st.stop()

df = pd.read_csv(DATA)

st.subheader("🧾 Summary Insights")
st.write(f"Total Entries: **{len(df)}**")
st.write(f"Most Frequent Emotion: **{df['emotion_label'].mode()[0]}**")
st.write(f"Average Sentiment Score: **{df['sentiment_score'].mean():.2f}**")

st.subheader("📤 Export Data")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "mood_data.csv")
