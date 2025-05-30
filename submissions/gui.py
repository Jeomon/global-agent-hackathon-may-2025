from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.embedder.google import GeminiEmbedder
from agno.models.google.gemini import Gemini
from agno.tools.crawl4ai import Crawl4aiTools
from agno.memory.v2.memory import Memory
from src.speech.speech_to_text import STT
from src.speech.text_to_speech import TTS
from uiautomation import GetScreenSize
from tools import WindowsTools
from dotenv import load_dotenv
from agno.agent import Agent
from textwrap import dedent
from getpass import getuser
from ui import launch_ui
from pathlib import Path
from groq import Groq
import platform
import os

load_dotenv()
google_key = os.getenv('GOOGLE_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')

model=Gemini(id='gemini-2.0-flash',api_key=google_key,temperature=0.3)
embedder=GeminiEmbedder(id='models/embedding-001',api_key=google_key)
memory=Memory(model=model,db=SqliteMemoryDb(table_name="memories", db_file='./database/memories.db'))
tools=[WindowsTools(),Crawl4aiTools()]

with open('./prompt/system.md') as f:
    system_message=dedent(f.read())

width, height = GetScreenSize()
parameters={
    'os':platform.system(),
    'home_dir':Path.home().as_posix(),
    'user':getuser(),
    'resolution':f'{width}x{height}'
}

agent=Agent(name='Windows-Use',model=model,memory=memory,system_message=system_message.format(**parameters),
tools=tools,enable_agentic_memory=True,add_history_to_messages=True,enable_user_memories=True,
markdown=True)

client=Groq(api_key=groq_api_key)
tts=TTS(client=client)
stt=STT(client=client)

launch_ui(agent=agent,tts=tts,stt=stt)