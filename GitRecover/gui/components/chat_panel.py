
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

class ChatPanel(QWidget):
    def __init__(self, recovery_service, parent=None):
        super().__init__(parent)
        self.recovery_service = recovery_service
        self._create_widgets()

    def _create_widgets(self):
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
        #Add spacing into the messages 
        html_text = text.replace('\n', '<br>')
        
        self.messages.append(
            f"<b>{sender}</b><br>{html_text}<br>"
        )

    def send_message(self):
        text = self.input.text().strip()

        self.add_message("You", text)
        self.input.clear()

        #Disable input while waiting for resposne
        self.input.setEnabled(False)
        self.send_button.setEnabled(False)
        self.add_message("System", "Processing user prompt...")

        worker = Worker(self.recovery_service.handle_chat_message, text)
        worker.signals.result.connect(self.on_llm_response)
        worker.signals.error.connect(self.on_llm_error)
        QThreadPool.globalInstance().start(worker)

    def on_llm_response(self, reply: str):
        self.add_message("Assistant", reply)
        self._reset_inputs()

    def on_llm_error(self, error_msg):
        self.add_message("System", f"Error occurred: {error_msg}")
        self._reset_inputs()

    def _reset_inputs(self):
        self.input.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input.setFocus()