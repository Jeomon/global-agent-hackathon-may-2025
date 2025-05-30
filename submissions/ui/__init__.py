from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QTextEdit, QGraphicsDropShadowEffect, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtGui import QIcon, QColor, QCursor, QKeyEvent, QTextCharFormat
from ui.thread import STTThread,TTSThread,AgentThread
from PyQt6.QtWidgets import QMessageBox, QFrame
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtCore import QTimer
from ui.utils import resource_path
from agno.agent import Agent
import sys
import os
import re
import ctypes
sys.path.append(os.path.dirname(__file__))
from src.speech.speech_to_text import STT
from src.speech.text_to_speech import TTS

class ChatUI(QWidget):
    def __init__(self,agent:Agent=None,stt:STT=None,tts:TTS=None):
        """Initialize the chat UI."""
        self.agent=agent
        self.stt=stt
        self.tts=tts
        self.is_recording=False
        self.stt_thread=None
        self.tts_thread=None
        self.agent_thread=None
        super().__init__()

        self.setWindowTitle("Windows-Use")
        self.setFixedSize(470, 80)  # ✅ Set window size slightly larger for shadow effect
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # ✅ Move to top center
        screen = QApplication.primaryScreen().size()
        x = (screen.width() - self.width()) // 2
        y = -8  # Keep close to top
        self.move(x, y)

        # ✅ Create the main container (with rounded borders)
        self.container = QWidget(self)
        self.container.setFixedSize(450, 45)  # ✅ Slightly smaller than window for padding

        # ✅ Apply Drop Shadow to the container
        self.add_shadow()

        # ✅ Layout inside the container
        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)  # ✅ No margins
        layout.setSpacing(0)  # ✅ No spacing between widgets

        # ✅ Mic Button
        self.mic_button = QPushButton()
        self.mic_button.setFixedSize(40, 45)
        self.mic_button.setIcon(QIcon(resource_path("./ui/assets/mic.svg")))
        self.mic_button.setStyleSheet("""
            QPushButton {
                background-color: #E2E8F0;
                border: none;
                border-top-left-radius: 5px;
                border-bottom-left-radius: 5px;
            }
            QPushButton:hover {
                background-color: #CBD5E1;
            }
        """)
        self.mic_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.mic_button.clicked.connect(self.on_mic_clicked)

        # ✅ Text Input (No border, No extra padding)
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("How can I help you?")
        self.text_input.setFixedHeight(45)
        self.text_input.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.text_input.setStyleSheet("""
            QTextEdit {
                background-color: #F1F5F9;
                border: none;
                font-size: 16px;
                font-family: 'Segoe UI', sans-serif;
                color: #1E293B;
                padding: 6px;
                margin: 0;
                outline: none;
            }
            QTextEdit:focus {
                outline: none;
            }
        """)
        self.text_input.textChanged.connect(self.on_text_changed)
        # Override keyPressEvent for the existing QTextEdit instance
        self.text_input.keyPressEvent = self.handle_press

        # ✅ Send Button
        self.send_button = QPushButton()
        self.send_button.setFixedSize(40, 45)
        self.send_button.setIcon(QIcon(resource_path("./ui/assets/send.svg")))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #E2E8F0;
                border: none;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QPushButton:hover {
                background-color: #CBD5E1;
            }
        """)
        self.send_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.send_button.clicked.connect(self.on_send_clicked)

        # ✅ Add widgets inside the container
        layout.addWidget(self.mic_button)
        layout.addWidget(self.text_input, 1)  # Expand text input
        layout.addWidget(self.send_button)

        # ✅ Center container inside main window
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)  # ✅ Space for shadow
        main_layout.addWidget(self.container)

    def handle_press(self,event:QKeyEvent):
        if (event.key() == Qt.Key.Key_Return and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
            self.on_send_clicked()
        else:
            QTextEdit.keyPressEvent(self.text_input, event)  # Call default behavior for other keys

    def add_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 30))  # Black shadow with opacity
        self.container.setGraphicsEffect(shadow)  # ✅ Apply shadow to container
    
    def on_mic_clicked(self):
        if self.stt is None:
            return None
        if not self.is_recording:
            self.is_recording=True
            self.update_style(self.mic_button,"background-color","#CBD5E1")
            self.stt.start_recording()
            self.text_input.setPlaceholderText('Listening...')
            self.send_button.setDisabled(True)
            self.text_input.setDisabled(True)
        else:
            self.is_recording=False
            self.update_style(self.mic_button,"background-color","#E2E8F0")
            self.stt.stop_recording()
            self.stt_thread=STTThread(stt=self.stt)
            self.stt_thread.start()
            self.stt_thread.stt_finished.connect(self.on_stt_finished)
            self.text_input.setPlaceholderText('Processing...')

    def on_stt_finished(self,content:str):
        content=content.strip()
        self.text_input.setDisabled(False)
        if len(content):
            self.text_input.setText(content)
            self.send_button.setDisabled(False)
        else:
            self.send_button.setDisabled(True)

    def on_text_changed(self):
        if len(self.text_input.toPlainText().strip()):
            self.send_button.setDisabled(False)
        else:
            self.text_input.setPlaceholderText('How can I help you?')
            self.send_button.setDisabled(True)

    def on_send_clicked(self):
        query=self.text_input.toPlainText().strip()
        if not query:
            return None
        self.text_input.setText('')
        self.text_input.setPlaceholderText('Executing Task...')
        self.mic_button.setDisabled(True)
        self.text_input.setDisabled(True)
        self.agent_thread=AgentThread(agent=self.agent,query=query)
        self.agent_thread.agent_finished.connect(self.on_agent_finished)
        self.agent_thread.start()
        self.send_button.setDisabled(True)

    def on_agent_finished(self,content:str):
        if self.tts is not None:
            self.text_input.setPlaceholderText('Responding...')
            self.tts_thread=TTSThread(self.tts,content)
            self.tts_thread.tts_finished.connect(self.on_tts_finished)
            self.tts_thread.start()
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle("System Agent: Response")
            msg.setText(content)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.show()
            QTimer.singleShot(0, lambda: msg.move(650, 190))
        self.text_input.setPlaceholderText("How can I help you?")
        self.text_input.setDisabled(False)
        self.send_button.setDisabled(True)
        self.mic_button.setDisabled(False)

    def on_tts_finished(self,content:str):
        self.text_input.setPlaceholderText("How can I help you?")

    def update_style(self,widget:QWidget, property_name:str, new_value:str):
        """Update a specific CSS property without removing others."""
        style = widget.styleSheet()
        
        # Check if the property exists
        if f"{property_name}:" in style:
            # Replace the existing property
            updated_style = re.sub(f"{property_name}:.*?;", f"{property_name}: {new_value};", style)
        else:
            # Append new property
            updated_style = style + f"\n{property_name}: {new_value};"

        widget.setStyleSheet(updated_style)
        
def launch_ui(agent:Agent=None,stt:STT=None,tts:TTS=None):
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.mycompany.pyqtapp")
    app = QApplication(sys.argv)
    icon = QIcon(resource_path("./ui/assets/icon_transparent.ico"))
    app.setWindowIcon(icon)
    window = ChatUI(agent=agent,stt=stt,tts=tts)
    window.show()
    app.exec()