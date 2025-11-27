import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

CSV_FILE = "mood_logs.csv"

st.set_page_config(page_title="AI Mood Tracker", layout="centered")

# Load / Create CSV
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["timestamp", "mood"])
    df.to_csv(CSV_FILE, index=False)

# UI Header
st.markdown("""
<h1 style='text-align:center;'>AI Mood Tracker</h1>
<p style='text-align:center;'>Track your moods daily and understand your emotional pattern.</p>
<hr>
""", unsafe_allow_html=True)

# Input
mood_text = st.text_area("📝 How are you feeling today?", "")

# Save Mood
if st.button("Save Mood"):
    if mood_text.strip() == "":
        st.error("Please write your mood before saving.")
    else:
        new_row = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "mood": mood_text}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success("Mood saved successfully!")

# Display Mood Logs
st.subheader("📚 Mood History")
if len(df) > 0:
    st.dataframe(df[::-1], use_container_width=True)
else:
    st.info("No moods logged yet.")

# Analytics
st.subheader("📊 Mood Analytics")
if len(df) > 0:
    df["date_only"] = pd.to_datetime(df["timestamp"]).dt.date
    fig = px.bar(df, x="date_only", y=df.index, color="mood",
                 labels={"y": "Number of Entries", "date_only": "Date"})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Add moods to see insights.")

# Clear Data
if st.button("❌ Clear All Data"):
    df = pd.DataFrame(columns=["timestamp", "mood"])
    df.to_csv(CSV_FILE, index=False)
    st.warning("All mood entries deleted!")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Developed with ❤️ using Streamlit</p>", unsafe_allow_html=True)
