"""
Author: Kent Pawson
chat_panel.py provides the UI component for chatting with the llm assistant.
"""

from __future__ import annotations

from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextBrowser,
    QLineEdit,
    QPushButton,
)
from GitRecover.workers.worker_thread import Worker

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GitRecover.gui.window import MainWindow

class ChatPanel(QWidget):
    def __init__(self, recovery_service, parent=None):
        """Initialize the chat panel.

        Parameters:
            recovery_service: Service used to send chat messages.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.root: MainWindow = parent
        self.recovery_service = recovery_service
        self._create_widgets()

    def _create_widgets(self):
        """Create the chat message and input widgets."""
        layout = QVBoxLayout(self)
        panel_title = QLabel("Assistant")
        panel_title.setStyleSheet("color: gray;")

        self.messages = QTextBrowser()
        self.messages.setPlaceholderText("Ask questions about your repository...")

        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask Question...")
        self.input.setStyleSheet("color: gray;")
        self.input.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        input_layout.addWidget(self.input)
        input_layout.addWidget(self.send_button)

        layout.addWidget(panel_title)
        layout.addWidget(self.messages, 1)
        layout.addLayout(input_layout)

    def add_message(self, sender: str, text: str):
        """Append a formatted message to the chat history.

        Parameters:
            sender: Name displayed for the message sender.
            text: Message content.
        """
        #Add spacing into the messages 
        html_text = text.replace('\n', '<br>')
        
        self.messages.append(
            f"<b>{sender}</b><br>{html_text}<br>"
        )

    def send_message(self):
        """Send the current input text in the background."""
        if not self.recovery_service.llm_provider.model:
            #TODO: If time permits, add alerts into the system
            print("Model not active, returning from sending message")
            self.input.clear()
            return
        
        text = self.input.text().strip()

        self.add_message("You", text)
        self.input.clear()

        #Disable input while waiting for resposne
        self.input.setEnabled(False)
        self.send_button.setEnabled(False)
        self.add_message("System", "Processing user prompt...")

        self.root.perform_background_task (
            fn=self.recovery_service.handle_chat_message, 
            on_success=self.on_llm_response,
            on_error=self.on_llm_error,
            user_message=text,
            show_progress=False,
        )

    def on_llm_response(self, reply: str):
        """Display a model response and re-enable chat input.

        Parameters:
            reply: Assistant response text.
        """
        self.add_message("Assistant", reply)
        self._reset_inputs()

    def on_llm_error(self, error_msg):
        """Display a model error and re-enable chat input.

        Parameters:
            error_msg: Error description.
        """
        self.add_message("System", f"Error occurred: {error_msg}")
        self._reset_inputs()

    def _reset_inputs(self):
        """Re-enable chat controls after a background response."""
        self.input.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input.setFocus()