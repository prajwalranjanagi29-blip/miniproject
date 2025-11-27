import streamlit as st

def show_latest_entry_summary(df):
    last = df.iloc[-1]
    st.subheader("📝 Latest Entry Summary")
    st.write(f"**Sentiment:** {last['sentiment_label']} ({last['sentiment_score']:.2f})")
    st.write(f"**Emotion:** {last['emotion_label']}")
    with st.expander("Read Entry"):
        st.write(last["text"])

