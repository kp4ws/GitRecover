from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtCore import QSize, QThreadPool
from GitRecover.git.recovery_service import RecoveryService
from GitRecover.gui.pages.home import HomePage 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git Recovery Assistant")
        self.setFixedSize(QSize(480, 360))

        self.thread_pool = QThreadPool()
        self.repo_manager = RecoveryService()

        self.app_pages = QStackedWidget()

        self.home_page = HomePage(self)

        self.app_pages.addWidget(self.home_page)

        self.app_pages.setCurrentWidget(self.home_page)
        self.setCentralWidget(self.app_pages)
        self.show()