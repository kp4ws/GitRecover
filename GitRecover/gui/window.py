from __future__ import annotations
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QHBoxLayout, QWidget, QSplitter
from PySide6.QtCore import Qt
from GitRecover.services.recovery_service import RecoveryService
from GitRecover.gui.pages.home_page import HomePage
from GitRecover.gui.pages.history_page import HistoryPage
from GitRecover.gui.pages.status_page import StatusPage
from GitRecover.gui.components.sidebar import Sidebar
from GitRecover.gui.components.chat_panel import ChatPanel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GitRecover.services.recovery_service import RecoveryService

class MainWindow(QMainWindow):
    def __init__(self, recovery_service: RecoveryService):
        super().__init__()
        self.setWindowTitle("Git Recover v.0.1.0")
        self.resize(1280, 720)

        self.pages = QStackedWidget()
        self.home_page = HomePage(self, recovery_service)
        self.history_page = HistoryPage(self, recovery_service)
        self.status_page = StatusPage(self, recovery_service)

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.history_page)
        self.pages.addWidget(self.status_page)

        self.navigation_items = [
            ("Home", 0),
            ("History", 1),
            ("Status", 2),
        ]

        self.main_widget = self._create_main_widget(recovery_service)
        self.setCentralWidget(self.main_widget)

        self._apply_styles()
        self.notify_UI_refresh()
        self.navigate_to(0)

    def _create_main_widget(self, recovery_service: RecoveryService) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar(self.navigation_items)
        self.sidebar.navigation_requested.connect(self.navigate_to)

        #TODO: Determine if there's a cleaner way of implementing the chat panel
        self.chat_panel = ChatPanel(recovery_service)

        self.ui_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.ui_splitter.addWidget(self.pages)
        self.ui_splitter.addWidget(self.chat_panel)

        self.ui_splitter.setStretchFactor(0, 3)
        self.ui_splitter.setStretchFactor(1, 2)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.ui_splitter, 1)

        return widget

    def navigate_to(self, page_index: int):
        self.pages.setCurrentIndex(page_index)

    def notify_UI_refresh(self, active_session=False):
        if active_session:
            self.chat_panel.setEnabled(True)
        else:
            self.chat_panel.setDisabled(True)

        for i in range(self.pages.count()):
            page = self.pages.widget(i)
            page.refresh_UI()

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