from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

def analyze_text(text):
    sentiment = sentiment_model(text)[0]
    emotion = emotion_model(text)[0]

    return {
        "sentiment_label": sentiment["label"],
        "sentiment_score": sentiment["score"],
        "emotion_label": emotion["label"],
    }
