import whisper
import streamlit as st
import tempfile
import os
from src.config import WHISPER_MODEL_SIZE

@st.cache_resource
def load_whisper_model():
    """
    Loads the Whisper model into memory. 
    Cached to prevent reloading on every interaction.
    """
    print(f"Loading Whisper model: {WHISPER_MODEL_SIZE}...")
    return whisper.load_model(WHISPER_MODEL_SIZE)

def transcribe_audio(audio_file) -> str:
    """
    Transcribes audio file to text.
    Handles the UploadedFile to TempFile conversion for FFmpeg compatibility.
    """
    model = load_whisper_model()
    
    # Create a temp file to store the audio bytes
    # delete=False is necessary to ensure the file exists when Whisper tries to open it
    # Use .webm suffix since browser audio is typically WebM format
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
        temp_audio.write(audio_file.getvalue())
        temp_audio.flush()  # Ensure data is written to disk
        temp_audio_path = temp_audio.name
    
    try:
        # Transcribe using the file path 
        print(f"Transcribing file: {temp_audio_path}")
        result = model.transcribe(temp_audio_path)
        text = result["text"]
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        st.error(f"Transcription Failed: {str(e)}")
        text = ""
    finally:
        # Cleanup: Remove the temp file to save disk space
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            
    return text.strip()