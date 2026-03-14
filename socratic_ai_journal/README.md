# 🦉 Socratic AI Journal

A **local-first, privacy-preserving cognitive augmentation system** for deep self-reflection through AI-powered Socratic questioning. Record your thoughts via voice, engage in meaningful AI dialogue, and track your emotional journey — all processed entirely on your machine.

---

## Features

| Feature | Description |
|---------|-------------|
| 🎙️ **Voice Journaling** | Record thoughts via browser microphone |
| 📝 **Auto Transcription** | Whisper-powered speech-to-text (runs locally) |
| 💭 **Socratic Dialogue** | Llama3 asks probing questions to deepen reflection |
| 📊 **Sentiment Tracking** | VADER-powered emotional trajectory charts |
| 🧠 **Cross-Entry Memory** | AI optionally references your previous entries |
| 🔒 **100% Local** | Zero external API calls — data never leaves your machine |
| 💾 **Persistent Storage** | SQLite database with WAL mode |

---

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| Python 3.10+ | Runtime | [python.org](https://python.org) |
| FFmpeg | Audio processing by Whisper | `brew install ffmpeg` (macOS) / `sudo apt install ffmpeg` (Linux) |
| Ollama | Local LLM inference | [ollama.com](https://ollama.com) |

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ALGO-DRAFT/Socratic-AI.git
cd Socratic-AI/socratic_ai_journal
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull the LLM model

```bash
ollama pull llama3
```

### 5. Configure environment (optional)

```bash
cp .env.example .env
# Edit .env to customise Ollama host, Whisper model size, or DB path
```

### 6. Start Ollama (keep this running in a separate terminal)

```bash
ollama serve
```

### 7. Launch the app

```bash
streamlit run main.py
```

Open **http://localhost:8501** in your browser.

---

## Usage

1. Click **"Create New Entry"** in the main area
2. Hit **Record Entry**, speak your thoughts, then **Stop**
3. Review the auto-transcribed text
4. Toggle **"Use Previous Entries for Context"** if desired
5. Click **"Save & Start Chat"** — the AI responds with Socratic questions
6. Reply via **voice** or **text** to continue the dialogue
7. Watch your **Emotional Trajectory** chart update in real time

---

## Project Structure

```
Socratic-AI/
├── .gitignore
└── socratic_ai_journal/
    ├── main.py              # Streamlit app entry point
    ├── requirements.txt     # Python dependencies
    ├── .env.example         # Environment variable template
    ├── data/
    │   └── journal.db       # SQLite database (auto-generated, gitignored)
    └── src/
        ├── config.py        # Configuration & Socratic system prompt
        ├── database.py      # SQLite CRUD operations
        ├── audio.py         # Whisper transcription
        ├── sentiment.py     # VADER sentiment analysis
        ├── llm.py           # Ollama LLM interface
        └── ui/
            └── visuals.py   # Plotly sentiment charts
```

---

## Architecture

```
Browser mic → WebM audio → FFmpeg → Whisper (local)
                                          ↓
                                    Text transcript
                                          ↓
                          VADER sentiment + SQLite storage
                                          ↓
                         Ollama (llama3) Socratic response
                                          ↓
                          Streamlit UI ← Plotly charts
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Ollama not responding | Run `ollama serve` in a separate terminal |
| Model not found | Run `ollama pull llama3` |
| GPU/CUDA errors | Use CPU mode: `OLLAMA_NUM_GPU=0 ollama serve` |
| Audio not transcribing | Ensure FFmpeg is installed and in PATH |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | [Streamlit](https://streamlit.io) |
| Speech-to-Text | [OpenAI Whisper](https://github.com/openai/whisper) |
| LLM | [Ollama](https://ollama.com) + Llama3 |
| Sentiment | [VADER](https://github.com/cjhutto/vaderSentiment) |
| Database | SQLite (WAL mode) |
| Visualisation | [Plotly](https://plotly.com) |

---

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "feat: description"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

MIT License — see [LICENSE](../LICENSE) for details.