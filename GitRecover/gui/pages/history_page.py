from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QVBoxLayout, QLabel
from GitRecover.gui.pages.page import Page
from GitRecover.gui.components.commit_table import CommitTable

if TYPE_CHECKING:
    from GitRecover.gui.window import MainWindow
    from GitRecover.services.recovery_service import RecoveryService

class HistoryPage(Page):
    def __init__(self, root: MainWindow, recovery_service: RecoveryService):
        super().__init__(root, recovery_service)

        self.commit_table = CommitTable()

        self.main_layout = self._create_widgets()
        self.setLayout(self.main_layout)

    def refresh_UI(self):
        if self.recovery_service.active_session is None:
            self.commit_table.setRowCount(0)
        else:
            #TODO
            history = self.recovery_service.active_session.git_history

    def _create_widgets(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        page_title = QLabel("History")
        page_title.setStyleSheet("font-size: 26px; font-weight: bold;")
        page_subtitle = QLabel("Displays Git commit history")
        page_subtitle.setStyleSheet("color: gray; margin-bottom: 10px;")

        layout.addWidget(page_title)
        layout.addWidget(page_subtitle)
        layout.addWidget(self.commit_table)
        layout.addStretch()

        return layout