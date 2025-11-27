import pandas as pd
import streamlit as st
import altair as alt
from pathlib import Path

DATA = Path("data/mood_logs.csv")


st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Analytics Dashboard")


if not DATA.exists():
    st.warning("No data available. Add journal entries on Home page.")
    st.stop()

df = pd.read_csv(DATA)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date


# Sentiment score time trend
trend = alt.Chart(df).mark_line(point=True).encode(
    x="date",
    y="sentiment_score",
    color="emotion_label"
).properties(height=350, title="Sentiment Score Over Time")

st.altair_chart(trend, use_container_width=True)


# Emotion distribution
emotion_counts = df["emotion_label"].value_counts().reset_index()
emotion_counts.columns = ["emotion", "count"]

emotion_chart = alt.Chart(emotion_counts).mark_bar().encode(
    x="emotion",
    y="count",
    color="emotion"
).properties(height=350, title="Emotion Breakdown")

st.altair_chart(emotion_chart, use_container_width=True)
