from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.embedder.google import GeminiEmbedder
from agno.models.google.gemini import Gemini
from agno.memory.v2.memory import Memory
from uiautomation import GetScreenSize
from tools import WindowsTools
from dotenv import load_dotenv
from agno.agent import Agent
from textwrap import dedent
from getpass import getuser
from pathlib import Path
import platform
import os

load_dotenv()
google_key = os.getenv('GOOGLE_API_KEY')

model=Gemini(id='gemini-2.0-flash',api_key=google_key,temperature=0.5)
embedder=GeminiEmbedder(id='models/embedding-001',api_key=google_key)
memory=Memory(model=model,db=SqliteMemoryDb(table_name="memories", db_file='./database/memories.db'))
tools=[WindowsTools()]

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

query=input('Enter your query: ')
agent.print_response(query,stream=True)