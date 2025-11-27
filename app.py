import datetime as dt
from pathlib import Path
import pandas as pd
import streamlit as st

from utils.speech_to_text import transcribe_audio_file
from utils.emotion_analyzer import analyze_text
from utils.visualizer import show_latest_entry_summary

DATA_PATH = Path("data/mood_logs.csv")


def load_logs():
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    return pd.DataFrame(columns=["timestamp", "text", "sentiment_label", "sentiment_score", "emotion_label"])


def save_logs(df):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)


def main():
    st.set_page_config(
        page_title="AI Mood Tracker", page_icon="🧠", layout="wide"
    )

    st.markdown("<h1 style='text-align:center;'>AI Mood Tracker 💬</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:gray;'>Journal your day — AI will detect sentiment & emotion</p>", unsafe_allow_html=True)

    df = load_logs()

    st.markdown("### 🔹 Choose Input Method")
    input_mode = st.radio("", ["Text Journal", "Voice Upload"])

    user_text = ""

    if input_mode == "Text Journal":
        user_text = st.text_area("Write your thoughts for today:", height=260, placeholder="Today I felt...")
    else:
        audio = st.file_uploader("Upload voice note (mp3/wav/m4a)", type=["mp3", "wav", "m4a"])
        if audio:
            with st.spinner("Transcribing voice..."):
                try:
                    user_text = transcribe_audio_file(audio)
                    st.success("Transcription complete!")
                    st.text_area("Transcribed text:", value=user_text, height=250)
                except Exception as e:
                    st.error(f"❌ Transcription failed: {e}")

    st.markdown("---")

    if st.button("🔍 Analyze & Save Entry", use_container_width=True):
        if not user_text.strip():
            st.warning("Please write or upload something first!")
        else:
            with st.spinner("Analyzing mood using AI..."):
                result = analyze_text(user_text)

            st.success("Entry analyzed successfully!")
            col1, col2 = st.columns(2)
            col1.metric("Sentiment", f"{result['sentiment_label']} ({result['sentiment_score']:.2f})")
            col2.metric("Emotion", result["emotion_label"])

            new_row = {
                "timestamp": dt.datetime.now(),
                "text": user_text,
                "sentiment_label": result["sentiment_label"],
                "sentiment_score": result["sentiment_score"],
                "emotion_label": result["emotion_label"],
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_logs(df)

            show_latest_entry_summary(df)

    st.info("Visit the sidebar for Dashboard 📊, Reports 📁 and History 📅")


if __name__ == "__main__":
    main()
