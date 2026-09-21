from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QStackedWidget, QHBoxLayout, QLineEdit, QMessageBox, QFileDialog
from PySide6.QtCore import QSize, Qt

from GitRecover.ai.ollama_utils import provide_feedback

from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git Recovery Assistant")
        self.setFixedSize(QSize(480, 360))

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
        git_repo_label = QLabel("Selected repository:")
        git_repo_label.setStyleSheet("font-weight: bold;")

        #By default, set git repo to current directory
        cwd = Path.cwd()
        git_repo_file = QLabel(f"{cwd}")
        git_repo_file.setStyleSheet("color: gray; font-style: italic;")

        repo_browse_btn = QPushButton("Browse")
        repo_browse_btn.clicked.connect(lambda: self._handle_browse(git_repo_file))

        # browse_layout.addWidget(git_repo_label)
        browse_layout.addWidget(git_repo_file)
        browse_layout.addWidget(repo_browse_btn)
        browse_layout.addStretch()

        prompt_label = QLabel("Enter details (optional)")
        prompt_field = QLineEdit()

        git_recover_btn = QPushButton("Git Recover")
        git_recover_btn.clicked.connect(lambda: self._handle_git_recover(prompt_field.text()))

        main_layout.addLayout(browse_layout)
        main_layout.addWidget(prompt_label)
        main_layout.addWidget(prompt_field)
        main_layout.addWidget(git_recover_btn)
        main_layout.addStretch()

        return widget

    def _handle_browse(self, file_label: QLabel):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select your Git Repo",
            dir=str(Path.cwd()),
            options=QFileDialog.Option.ShowDirsOnly
        )

        if directory:
            file_label.setText(directory)

    def _handle_git_recover(self, user_message: str):
        ai_response = provide_feedback(user_message)

        dialog_response = QMessageBox(self)
        dialog_response.setWindowTitle("AI Response")
        dialog_response.setText(ai_response)

        ok_btn = dialog_response.exec()
        # if ok_btn == QMessageBox.Ok:
        #     print("okay!")