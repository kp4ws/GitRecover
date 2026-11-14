from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout
from pathlib import Path
from GitRecover.gui.pages.page import Page
from GitRecover.gui.components.card import Card
from GitRecover.gui.components.recovery_report import RecoveryReport
from GitRecover.gui.colors import GOOD, BAD, WARNING
from GitRecover.core.schemas import RemoteSyncStatus, RepoStatus
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
            self.session.setText("No Active Session")
            self.repo_path.setText("")
            self.repo_head.setText("")
            self.current_branch.setText("")
            self.repo_status.setText("")
            self.dangling_commits.setText("")
            self.remote_sync.setText("")
        else:
            request = self.recovery_service.active_session
            state = request.state
            
            self.session.setText(f"Active Session: {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}")
            self.repo_path.setText(request.repo_path)
            self.repo_head.setText(state.current_head[:7])

            #If empty string, then its in detatched head state
            if state.current_branch != "":
                self.current_branch.setText(state.current_branch)
                self.current_branch.setStyleSheet("")
                self.health_form.labelForField(self.current_branch).setStyleSheet("")
                self.repo_head.setStyleSheet("")
                self.health_form.labelForField(self.repo_head).setStyleSheet("")
            else:
                self.current_branch.setText("Detatched HEAD")
                self.current_branch.setStyleSheet(f"color: {WARNING};")
                self.health_form.labelForField(self.current_branch).setStyleSheet(f"color:{WARNING};")
                self.repo_head.setStyleSheet(f"color: {WARNING};")
                self.health_form.labelForField(self.repo_head).setStyleSheet(f"color: {WARNING};")

            if state.status == RepoStatus.CLEAN:
                self.repo_status.setStyleSheet(f"color: {GOOD};")
                self.health_form.labelForField(self.repo_status).setStyleSheet(f"color: {GOOD};")
            elif state.status == RepoStatus.DIRTY:
                self.repo_status.setStyleSheet(f"color: {BAD};")
                self.health_form.labelForField(self.repo_status).setStyleSheet(f"color: {BAD};")
            else:
                self.repo_status.setStyleSheet(f"color: {WARNING};")
                self.health_form.labelForField(self.repo_status).setStyleSheet(f"color: {WARNING};")
                            
            self.repo_status.setText(state.status.value)

            dangling_hashes = []
            for commit in request.history.commit_history:
                if commit.is_dangling:
                    dangling_hashes.append(commit.hash)

            if len(dangling_hashes) > 0:
                self.dangling_commits.setStyleSheet(f"color: {BAD}")
                self.health_form.labelForField(self.dangling_commits).setStyleSheet(f"color: {BAD};")
                                 
            else:
                self.dangling_commits.setStyleSheet(f"color: {GOOD}")
                self.health_form.labelForField(self.dangling_commits).setStyleSheet(f"color: {GOOD};")

            self.dangling_commits.setText(str(len(dangling_hashes)))

            if state.remote_sync.status == RemoteSyncStatus.UP_TO_DATE:
                self.remote_sync.setStyleSheet(f"color: {GOOD};")
                self.health_form.labelForField(self.remote_sync).setStyleSheet(f"color: {GOOD};")
            elif state.remote_sync.status in (RemoteSyncStatus.BEHIND, RemoteSyncStatus.DIVERGED, RemoteSyncStatus.ERROR):
                self.remote_sync.setStyleSheet(f"color: {BAD};")
                self.health_form.labelForField(self.remote_sync).setStyleSheet(f"color: {BAD};")
            else:
                self.remote_sync.setStyleSheet(f"color: {WARNING};")
                self.health_form.labelForField(self.remote_sync).setStyleSheet(f"color: {WARNING};")

            self.remote_sync.setText(state.remote_sync.display_text)
            self.active_request_card.show()
    
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
        self.session = QLabel("")
        self.session.setStyleSheet("margin-bottom: 10px; font-weight: bold;")
        self.health_form = QFormLayout()
        self.repo_path = QLabel("")
        self.repo_status = QLabel("")
        self.repo_head = QLabel("")
        self.current_branch = QLabel("")
        self.dangling_commits = QLabel("")
        self.remote_sync = QLabel("")

        self.health_form.addRow("Repository:", self.repo_path)
        self.health_form.addRow("HEAD:", self.repo_head)
        self.health_form.addRow("Current branch:", self.current_branch)
        self.health_form.addRow("Status:", self.repo_status)
        self.health_form.addRow("Dangling commits:", self.dangling_commits)
        self.health_form.addRow("Remote sync:", self.remote_sync)

        self.active_request_card = Card(
            "Repository Health", 
            items=[self.session, self.health_form]
        )
        
        layout.addWidget(page_title)
        layout.addWidget(page_subtitle)
        layout.addWidget(new_request_card)
        layout.addWidget(self.active_request_card)
        layout.addStretch()

        return layout

    def _handle_recovery_create(self, repo_path: str):
        self.root.perform_background_task (
            fn=self.recovery_service.create_recovery_request, 
            on_success=self._on_request_created,
            title="Creating Recovery Session",
            text="Analyzing Git Repository...",
            show_progress=True,
            repo_path=repo_path
        )

    def _on_request_created(self, result):
        request = result or self.recovery_service.active_session
        if request is None:
            print("Warning: Recovery Request returning null")
            return
        
        self.root.notify_UI_refresh(request)

        recovery_report = RecoveryReport(request, self)
        recovery_report.view_history_event.connect(lambda: self.root.navigate_to(1))

        #TODO Consider adding AI suggestion to recovery report

        recovery_report.exec()