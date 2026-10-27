from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QHBoxLayout, QLineEdit, QMessageBox
from PySide6.QtCore import QThreadPool
from pathlib import Path
from GitRecover.workers.worker_thread import Worker
from GitRecover.gui.pages.page import Page
from GitRecover.gui.components.card import Card
from datetime import datetime

if TYPE_CHECKING:
    from GitRecover.gui.window import MainWindow
    from GitRecover.services.recovery_service import RecoveryService

class HomePage(Page):
    def __init__(self, root: MainWindow, recovery_service: RecoveryService):
        super().__init__(root, recovery_service)
        self.main_layout = self._create_widgets()
        self.setLayout(self.main_layout)

    def refresh_UI(self):
        if self.recovery_service.active_session is None:
            self.active_session_label.setText("No active session")
            self.save_recovery_btn.setEnabled(False)
        else:
            self.active_session_label.setText(f"Active Session: {datetime.now()}")
            self.save_recovery_btn.setEnabled(True)
    
    def _create_widgets(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        page_title = QLabel("Home")
        page_title.setStyleSheet("font-size: 26px; font-weight: bold;")
        page_subtitle = QLabel("Create a new recovery request, or import an existing one")
        page_subtitle.setStyleSheet("color: gray; margin-bottom: 10px;")

        #CREATE NEW REQUEST CARD                                
        #Field for selecting the repo
        repo_file_layout = QHBoxLayout()

        repo_label = QLabel("Target Repository")
        cwd = Path.cwd()#By default, set git repo to current directory
        repo_file = QLineEdit(f"{cwd}")
        repo_file.setReadOnly(True)
        repo_file.setStyleSheet("color: gray; font-style: italic;")
        
        repo_browse_btn = QPushButton("Browse")
        repo_browse_btn.setFixedWidth(100)
        repo_browse_btn.clicked.connect(lambda: self.browse_directory(repo_file))
        
        repo_file_layout.addWidget(repo_file)
        repo_file_layout.addWidget(repo_browse_btn)

        prompt_label = QLabel("Enter Details (Optional)")
        prompt_field = QLineEdit()
        prompt_field.setPlaceholderText("")
        prompt_field.setStyleSheet("color: lightgrey;")

        new_recovery_btn = QPushButton("Create Recovery Request")
        new_recovery_btn.setFixedWidth(220)
        new_recovery_btn.clicked.connect(lambda: self._handle_recovery_create(repo_file.text(), prompt_field.text()))

        new_request_card = Card(
            "Create New Request",
            items = [
                repo_label,
                repo_file_layout,
                # prompt_label,
                # prompt_field,
                new_recovery_btn
            ]
        )

        #IMPORT EXISTING REQUEST CARD
        self.existing_recovery_btn = QPushButton("Import Recovery Request")
        self.existing_recovery_btn.setFixedWidth(220)
        self.existing_recovery_btn.clicked.connect(self._handle_recovery_import)

        existing_request_card = Card(
            "Import From File",
            items= [
                self.existing_recovery_btn
            ]
        )

        #ACTIVE REQUEST CARD
        self.active_session_label = QLabel("")
        self.save_recovery_btn = QPushButton("Save To File")
        self.save_recovery_btn.setFixedWidth(220)
        self.save_recovery_btn.clicked.connect(self._handle_recovery_save)
        active_request_card = Card(
            "Active Recovery Request",
            items = [
                self.active_session_label,
                self.save_recovery_btn,
            ]
        )
        
        layout.addWidget(page_title)
        layout.addWidget(page_subtitle)
        layout.addWidget(new_request_card)
        layout.addWidget(existing_request_card)
        layout.addWidget(active_request_card)
        layout.addStretch()

        return layout

    def _handle_recovery_create(self, repo_path: str, user_prompt: str):
        print("creating active session", repo_path, user_prompt)
        self.recovery_service.create_recovery_request(repo_path, user_prompt)
        self.root.notify_UI_refresh(self.recovery_service.active_session)
        # worker = Worker(self.recovery_service.handle_recovery, repo_path, user_prompt)
        # worker.signals.result.connect(self.show_result)
        # QThreadPool.globalInstance().start(worker)

    def _handle_recovery_import(self):
        print("importing recovery session")
        recovery_session_file = self.browse_file()
        self.recovery_service.import_recovery_request(recovery_session_file)
        self.root.notify_UI_refresh(self.recovery_service.active_session)

    def _handle_recovery_save(self):
        pass

    def show_result(self, result):
        dialog_response = QMessageBox(self)
        dialog_response.setWindowTitle("AI Response")
        dialog_response.setText(result)

        ok_btn = dialog_response.exec()
        # if ok_btn == QMessageBox.Ok:
        #     print("okay!")