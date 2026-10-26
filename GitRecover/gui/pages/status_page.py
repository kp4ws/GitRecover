from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QVBoxLayout, QLabel
from GitRecover.gui.pages.page import Page

if TYPE_CHECKING:
    from GitRecover.gui.window import MainWindow
    from GitRecover.services.recovery_service import RecoveryService

class StatusPage(Page):
    def __init__(self, root: MainWindow, recovery_service: RecoveryService):
        super().__init__(root, recovery_service)
        self.main_layout = self._create_widgets()
        self.setLayout(self.main_layout)

    def refresh_view(self):
        pass

    def _create_widgets(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()

        page_title = QLabel("Status")
        page_title.setStyleSheet("font-size: 26px; font-weight: bold;")
        page_subtitle = QLabel("Keeps a list of repo details")
        page_subtitle.setStyleSheet("color: gray; margin-bottom: 10px;")

        main_layout.addWidget(page_title)
        main_layout.addWidget(page_subtitle)
        main_layout.addStretch()

        return main_layout