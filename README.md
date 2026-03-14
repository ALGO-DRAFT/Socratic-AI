# 🦉 Socratic AI Journal

> *A local-first, privacy-preserving cognitive augmentation system for deep self-reflection through AI-powered Socratic questioning.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Local First](https://img.shields.io/badge/Privacy-100%25%20Local-brightgreen)](#privacy--security)

---

## What is Socratic AI Journal?

Socratic AI Journal helps you think more clearly about your own thoughts. You speak your mind, and instead of giving you answers, the AI responds with carefully crafted **Socratic questions** — helping you uncover assumptions, explore contradictions, and arrive at your own insights.

Everything runs **100% locally** on your machine. No data is ever sent to the cloud.

---

## Features

| Feature | Description |
|---------|-------------|
| 🎙️ **Voice Journaling** | Record thoughts via your browser microphone |
| 📝 **Auto Transcription** | Whisper (local) converts speech to text |
| 💭 **Socratic Dialogue** | Llama3 guides reflection through probing questions |
| 📊 **Sentiment Tracking** | VADER-powered emotional trajectory charts |
| 🧠 **Cross-Entry Memory** | AI optionally references your previous entries |
| 🔒 **100% Local** | Zero cloud calls — your data stays on your machine |
| 💾 **Persistent Storage** | SQLite with WAL mode for reliability |

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **FFmpeg** — `brew install ffmpeg` (macOS) / `sudo apt install ffmpeg` (Linux)
- **Ollama** — download at [ollama.com](https://ollama.com)

### Install & Run

```bash
# 1. Clone the repo
git clone https://github.com/ALGO-DRAFT/Socratic-AI.git
cd Socratic-AI/socratic_ai_journal

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Pull the LLM model
ollama pull llama3

# 5. Start Ollama (keep running in a separate terminal)
ollama serve

# 6. Launch the app
streamlit run main.py
```

Open **http://localhost:8501** in your browser.

---

## How It Works

```
You speak → Whisper transcribes → VADER scores sentiment
                                          ↓
                              Saved to local SQLite DB
                                          ↓
                      Llama3 (via Ollama) asks Socratic questions
                                          ↓
                         You reflect, reply, grow 🌱
                                          ↓
                      Plotly charts your emotional trajectory
```

---

## Project Structure

```
Socratic-AI/
├── .gitignore
└── socratic_ai_journal/
    ├── main.py              # Streamlit app entry point
    ├── requirements.txt     # Python dependencies
    ├── .env.example         # Environment config template
    ├── data/
    │   └── journal.db       # SQLite DB (auto-generated, gitignored)
    └── src/
        ├── config.py        # Config & Socratic system prompt
        ├── database.py      # SQLite CRUD operations
        ├── audio.py         # Whisper transcription
        ├── sentiment.py     # VADER sentiment analysis
        ├── llm.py           # Ollama LLM interface
        └── ui/
            └── visuals.py   # Plotly charts
```

---

## Configuration

Copy `.env.example` to `.env` inside `socratic_ai_journal/` and adjust as needed:

```env
OLLAMA_HOST=http://localhost:11434
WHISPER_MODEL=base        # tiny | base | small | medium | large
DB_PATH=data/journal.db
```

---

## Privacy & Security

- ✅ All AI inference runs locally via Ollama
- ✅ Speech-to-text via Whisper (no cloud API)
- ✅ Database stored on your own machine
- ✅ No telemetry, no tracking, no external requests

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Ollama not responding | Run `ollama serve` in a separate terminal |
| Model not found | Run `ollama pull llama3` |
| GPU/CUDA errors | `OLLAMA_NUM_GPU=0 ollama serve` |
| Audio not transcribing | Ensure FFmpeg is installed and in PATH |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | [Streamlit](https://streamlit.io) |
| Speech-to-Text | [OpenAI Whisper](https://github.com/openai/whisper) |
| LLM | [Ollama](https://ollama.com) + Llama3 |
| Sentiment | [VADER](https://github.com/cjhutto/vaderSentiment) |
| Storage | SQLite |
| Visualisation | [Plotly](https://plotly.com) |

---

## Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "feat: your feature"`
4. Push & open a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE) for details.
