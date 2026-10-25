from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QMessageBox
from PySide6.QtCore import QThreadPool
from pathlib import Path
from GitRecover.workers.worker_thread import Worker
from GitRecover.gui.pages.page import Page

if TYPE_CHECKING:
    from GitRecover.gui.window import MainWindow
    from GitRecover.services.recovery_service import RecoveryService

class ConsolePage(Page):
    def __init__(self, root: MainWindow, recovery_engine: RecoveryService):
        super().__init__(root, recovery_engine)
        self.main_layout = self._create_widgets()
        self.setLayout(self.main_layout)

    def _create_widgets(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        browse_layout = QHBoxLayout()

        #By default, set git repo to current directory
        cwd = Path.cwd()
        repo_filepath_label = QLabel(f"{cwd}")
        repo_filepath_label.setStyleSheet("color: gray; font-style: italic;")

        repo_browse_btn = QPushButton("Browse Git Repo")
        repo_browse_btn.clicked.connect(lambda: self._handle_browse(repo_filepath_label))

        # browse_layout.addWidget(repo_path_label)
        browse_layout.addWidget(repo_filepath_label)
        browse_layout.addWidget(repo_browse_btn)
        browse_layout.addStretch()

        prompt_field = QLineEdit()
        prompt_field.setPlaceholderText("Enter details (optional) ...")
        prompt_field.setStyleSheet("color: lightgrey;")

        git_recover_btn = QPushButton("Submit Recovery Request")
        git_recover_btn.clicked.connect(lambda: self._handle_git_recover(repo_filepath_label.text(), prompt_field.text()))

        layout.addLayout(browse_layout)
        layout.addWidget(prompt_field)
        layout.addWidget(git_recover_btn)
        layout.addStretch()

        return layout

    def _handle_git_recover(self, repo_path: str, user_prompt: str):
        worker = Worker(self.recovery_engine.handle_recovery, repo_path, user_prompt)
        worker.signals.result.connect(self.show_result)
        QThreadPool.globalInstance().start(worker)

    def show_result(self, result):
        dialog_response = QMessageBox(self)
        dialog_response.setWindowTitle("AI Response")
        dialog_response.setText(result)

        ok_btn = dialog_response.exec()
        # if ok_btn == QMessageBox.Ok:
        #     print("okay!")