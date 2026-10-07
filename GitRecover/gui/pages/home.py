from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QMessageBox
from pathlib import Path
from GitRecover.workers.worker_thread import Worker
from GitRecover.gui.pages.page import Page

if TYPE_CHECKING:
    from GitRecover.gui.window import MainWindow

class HomePage(Page):
    def __init__(self, root: MainWindow):
        super().__init__(root)
        self._create_widgets()

    def _create_widgets(self):
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
        git_recover_btn.clicked.connect(lambda: self._handle_git_recover(git_repo_file.text(), prompt_field.text()))

        main_layout.addLayout(browse_layout)
        main_layout.addWidget(prompt_label)
        main_layout.addWidget(prompt_field)
        main_layout.addWidget(git_recover_btn)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def _handle_git_recover(self, git_repo: str, user_prompt: str):
        worker = Worker(self.root.repo_manager.handle_recovery, git_repo, user_prompt)
        worker.signals.result.connect(self.show_result)
        self.root.thread_pool.start(worker)

    def show_result(self, result):
        dialog_response = QMessageBox(self)
        dialog_response.setWindowTitle("AI Response")
        dialog_response.setText(result)

        ok_btn = dialog_response.exec()
        # if ok_btn == QMessageBox.Ok:
        #     print("okay!")