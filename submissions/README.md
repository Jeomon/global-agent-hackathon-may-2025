# Windows-Use:
### AI-Powered Agent that interacts with the Windows Desktop.

## Overview of the Idea
Windows-Use bridges the gap between large language models (LLMs) and the Windows operating system. It enables intelligent agents to interact with Windows UI elements, such as applications, windows, and files, using native system APIs, not traditional computer vision.

## Project Goal
To demonstrate a powerful, lightweight system that allows LLM agents to natively control and interact with Windows system through real-time feedback. The project aims to simplify how agents interact with GUI-based operating systems, without requiring custom models or extensive setup.

## Tech Stack
- Agno
- Gemini (LLM)
- Groq (TTS, STT)
- UIAutomation
- Pydantic
- Pyqt6 (UI)

## Setup & Usage

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

Run one of the following command to run the agent
```python
python gui.py # For GUI mode

python cli.py # For CLI mode
```

## Demo Video Link

https://github.com/user-attachments/assets/eb08adad-9189-4051-83b8-3c8b4bcd4ad5