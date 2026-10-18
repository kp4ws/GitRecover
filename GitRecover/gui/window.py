from __future__ import annotations
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QFrame, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import QSize
from GitRecover.services.recovery_service import RecoveryService
from GitRecover.gui.pages.console_page import ConsolePage
from GitRecover.gui.pages.history_page import HistoryPage
from GitRecover.gui.components.sidebar import Sidebar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GitRecover.services.recovery_service import RecoveryService

class MainWindow(QMainWindow):
    def __init__(self, recovery_engine: RecoveryService):
        super().__init__()
        self.setWindowTitle("Git Recovery Assistant")
        self.resize(1000, 650)

        self.pages = QStackedWidget()
        self.home_page = ConsolePage(self, recovery_engine)
        self.test_page = HistoryPage(self, recovery_engine)
        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.test_page)

        self.navigation_items = [
            ("Console", 0),
            ("History", 1), #TODO: Determine which pages the app should have
        ]

        self.main_widget = self._create_main_widget()
        self.setCentralWidget(self.main_widget)

        self._apply_styles()
        self.navigate_to(0)

    def _create_main_widget(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar(self.navigation_items)
        self.sidebar.navigation_requested.connect(self.navigate_to)
        
        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)

        return widget

    def navigate_to(self, page_index: int):
        self.pages.setCurrentIndex(page_index)

    def _apply_styles(self):
        self.setStyleSheet("""
            QFrame#sidebar {
                border-right: 1px solid palette(mid);
            }

            QLabel#sidebarTitle {
                font-size: 20px;
                font-weight: bold;
                padding: 4px;
            }
        """)