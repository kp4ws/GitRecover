from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QStackedWidget, QHBoxLayout, QTextEdit, QMessageBox
from PySide6.QtCore import QSize, Qt

from GitRecover.ai.ollama_utils import provide_feedback

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git Recovery Assistant")
        self.setFixedSize(QSize(400, 300))

        self.app_pages = QStackedWidget()

        page_one = self._page_one()

        self.app_pages.addWidget(page_one)

        self.app_pages.setCurrentWidget(page_one)
        self.setCentralWidget(self.app_pages)
        self.show()

    def _page_one(self):
        widget = QWidget()
        main_layout = QVBoxLayout(widget)

        browse_layout = QHBoxLayout()
        git_repo_label = QLabel("Git repo to be recovered: ___________________")
        repo_browse_btn = QPushButton("Browse")
        browse_layout.addWidget(git_repo_label)
        browse_layout.addWidget(repo_browse_btn)

        text_area = QTextEdit()

        git_recover_btn = QPushButton("Git Recover")
        git_recover_btn.clicked.connect(lambda: self._handle_git_recover(text_area.toPlainText()))

        main_layout.addLayout(browse_layout)
        main_layout.addWidget(text_area)
        main_layout.addWidget(git_recover_btn)
        return widget

    def _handle_git_recover(self, user_message: str):
        ai_response = provide_feedback(user_message)

        dialog_response = QMessageBox(self)
        dialog_response.setWindowTitle("AI Response")
        dialog_response.setText(ai_response)

        ok_btn = dialog_response.exec()
        if ok_btn == QMessageBox.Ok:
            print("okay!")