from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QVBoxLayout, QLabel
from GitRecover.gui.pages.page import Page
from GitRecover.gui.components.card import Card

if TYPE_CHECKING:
    from GitRecover.gui.window import MainWindow
    from GitRecover.services.recovery_service import RecoveryService

class StatusPage(Page):
    def __init__(self, root: MainWindow, recovery_service: RecoveryService):
        super().__init__(root, recovery_service)
        self.main_layout = self._create_widgets()
        self.setLayout(self.main_layout)

    def refresh_UI(self):
        if self.recovery_service.active_session is None:
            self.repo_status_card.hide()
        else:
            state = self.recovery_service.active_session.repository_state
            self.repo_status.setText(f"Repository Status: {state.status}") 
            self.repo_head.setText(f"Current HEAD: {state.current_head}")
            self.current_branch.setText(f"Current Branch: {state.current_branch}")
            
            self.repo_status_card.show()

    def _create_widgets(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        page_title = QLabel("Status")
        page_title.setStyleSheet("font-size: 26px; font-weight: bold;")
        page_subtitle = QLabel("Keeps a list of repo details")
        page_subtitle.setStyleSheet("color: gray; margin-bottom: 10px;")

        #STATUS CARD
        self.repo_status = QLabel()
        self.repo_head = QLabel()
        self.current_branch = QLabel()

        self.repo_status_card = Card(
            "Repository Health",
            items = [
                self.repo_status,
                self.repo_head,
                self.current_branch,
            ]
        )
        
        layout.addWidget(page_title)
        layout.addWidget(page_subtitle)
        layout.addWidget(self.repo_status_card)
        layout.addStretch()

        return layout