# 🪟Windows-Use

### AI Agent that interacts with the Windows Desktop just like a human.

##  Overview
Windows-Use bridges the gap between large language models (LLMs) and the Windows operating system. It enables intelligent agents to interact with Windows UI elements, such as applications, windows, and files, using native system APIs rather than traditional computer vision.

## 📜 Project Goal
To demonstrate a powerful, lightweight system that allows LLM agents to natively control and interact with the Windows system through real-time feedback. The project aims to simplify how agents interact with GUI-based operating systems, without requiring custom models or extensive setup.

## 🧑🏾‍💻Tech Stack

- **AI Framework:** Agno
- **LLM:** Google Gemini 2.0 Flash / Claude Sonnet 4.0 (paid tier is preferred to surpass RPM limit)
- **TTS:** Groq playai-tts
- **STT:** Groq whisper-large-v3
- **UI:** Pyqt6

## 🏗️ Setup & Usage

Clone the repository:
```bash
git clone <url>
cd Windows-Use
```

Set up virtual environment and dependencies:
```bash
python -m venv .venv
pip install -r requirements.txt
```

Convert `.env-example` to `.env`
```plaintext
GROQ_API_KEY='<api_key_here>'
GOOGLE_API_KEY='<api_key_here>'
```

Run one of the following commands to run the agent
```bash
python gui.py # For GUI mode

python cli.py # For CLI mode
```

**⚠️CAUTION:** Agent interacts directly with your Windows OS to perform actions. While the agent is designed to act intelligently and safely, it can make mistakes that might disrupt system behaviour or cause unintended changes. 

## 🎥Demo Video

https://github.com/user-attachments/assets/00c37245-b0dd-4b71-9904-1c0373f286a6