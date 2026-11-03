from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QHBoxLayout, QLineEdit, QMessageBox
from pathlib import Path
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
        else:
            self.active_request_card.show()
            self.active_session_label.setText(f"Active Session: {datetime.now()}")

            state = self.recovery_service.active_session.repository_state

            self.repo_status.setText(f"Repository Status: {state.status}") 
            self.repo_head.setText(f"Current HEAD: {state.current_head[:7]}")
            self.current_branch.setText(f"Current Branch: {state.current_branch}")
    
    def _create_widgets(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        page_title = QLabel("Home")
        page_title.setStyleSheet("font-size: 26px; font-weight: bold;")
        page_subtitle = QLabel("Displays repository health")
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

        new_recovery_btn = QPushButton("Create Recovery Request")
        new_recovery_btn.setFixedWidth(220)
        new_recovery_btn.clicked.connect(lambda: self._handle_recovery_create(repo_file.text()))

        new_request_card = Card(
            "Create New Request",
            items = [
                repo_label,
                repo_file_layout,
                new_recovery_btn
            ]
        )

        #REPOSITORY HEALTH CARD
        #REPO Labels
        #TODO: Add styling to the labels
        self.active_session_label = QLabel("")
        self.repo_status = QLabel()
        self.repo_head = QLabel()
        self.current_branch = QLabel()

        self.active_request_card = Card(
            "Repository Health",
            items = [
                self.active_session_label,
                self.repo_status,
                self.repo_head,
                self.current_branch,
            ]
        )
        
        layout.addWidget(page_title)
        layout.addWidget(page_subtitle)
        layout.addWidget(new_request_card)
        # layout.addWidget(existing_request_card)
        layout.addWidget(self.active_request_card)
        layout.addStretch()

        return layout

    def _handle_recovery_create(self, repo_path: str):
        print("creating recovery request")

        self.perform_background_task (
            fn=self.recovery_service.create_recovery_request, 
            on_success=self._on_request_created,
            title="Creating Recovery Session",
            text="Analyzing Git Repository...",
            repo_path=repo_path
        )

    def _on_request_created(self, result):
        print("on recovery request created")
        self.root.notify_UI_refresh(self.recovery_service.active_session)