# 🦉 Socratic AI Journal

streamlit run main.py

A Local-First Cognitive Augmentation System for deep self-reflection using AI-powered Socratic questioning.

## Features

- 🎙️ **Voice Recording**: Capture your thoughts via audio
- 📝 **Automatic Transcription**: Whisper-powered speech-to-text
- 💭 **Socratic Dialogue**: AI-powered critical thinking questions
- 📊 **Sentiment Analysis**: Track your emotional trajectory over time
- 🔒 **Local-First**: All data stays on your machine
- 💾 **Persistent Storage**: SQLite database with WAL mode

## Prerequisites

1. **Python 3.10+**
2. **FFmpeg** (for audio processing)
3. **Ollama** (for local LLM inference)

## Installation

```bash
# Install system dependencies
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the LLM model
ollama pull llama3

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Ensure Ollama is running
ollama serve

# Run the application
streamlit run main.py
```

## Project Structure

```
socratic_ai_journal/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── data/
│   └── journal.db         # SQLite database (auto-generated)
└── src/
    ├── config.py          # Configuration constants
    ├── database.py        # Database operations
    ├── audio.py           # Whisper transcription
    ├── sentiment.py       # VADER sentiment analysis
    ├── llm.py             # Ollama interface
    └── ui/
        └── visuals.py     # Plotly visualizations
```

## System Architecture

1. **Acoustic Capture**: Browser-based audio recording
2. **Signal Transduction**: Whisper-based transcription
3. **Semantic Analysis**: VADER sentiment scoring
4. **Cognitive Processing**: Ollama-powered Socratic questioning
5. **State Persistence**: SQLite with WAL mode

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or submit a pull request.