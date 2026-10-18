from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QVBoxLayout, QLabel
from GitRecover.gui.pages.page import Page

if TYPE_CHECKING:
    from GitRecover.gui.window import MainWindow
    from GitRecover.services.recovery_service import RecoveryService

class HistoryPage(Page):
    def __init__(self, root: MainWindow, recovery_engine: RecoveryService):
        super().__init__(root, recovery_engine)
        self.main_layout = self._create_widgets()
        self.setLayout(self.main_layout)

    def _create_widgets(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("History Page: Keeps a list of response history"))

        return main_layout