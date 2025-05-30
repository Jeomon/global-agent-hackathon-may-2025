from PyQt6.QtCore import QThread, pyqtSignal
from agno.agent import Agent
import sys
import os
sys.path.append(os.path.dirname(__file__))
from src.speech.speech_to_text import STT
from src.speech.text_to_speech import TTS

class STTThread(QThread):
    stt_finished = pyqtSignal(str)
    def __init__(self, stt:STT=None):
        super().__init__()
        self.stt = stt

    def run(self):
        response = self.stt.process_audio()
        self.stt_finished.emit(response.text)

class TTSThread(QThread):
    tts_finished = pyqtSignal(str)
    def __init__(self, tts:TTS=None, text:str=''):
        super().__init__()
        self.tts = tts
        self.text=text

    def run(self):
        self.tts.invoke(self.text)
        self.tts_finished.emit("Operation Finished")

class AgentThread(QThread):
    agent_finished = pyqtSignal(str)
    def __init__(self, agent:Agent=None,query:str=''):
        super().__init__()
        self.agent = agent
        self.query=query

    def run(self):
        response=self.agent.run(self.query)
        content=response.get_content_as_string()
        self.agent_finished.emit(content.strip())