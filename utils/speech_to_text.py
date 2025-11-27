import whisper

def transcribe_audio_file(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]
