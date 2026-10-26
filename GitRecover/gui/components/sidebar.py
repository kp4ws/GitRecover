from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal

class Sidebar(QFrame):
    navigation_requested = Signal(int)

    def __init__(self, navigation_items: list[tuple[str, int]], title: str = "GitRecover"):
        super().__init__()
        self._create_widgets(navigation_items, title)
        self._apply_styles()

    def _create_widgets(self, navigation_items: list[tuple[str, int]], title: str):
        self.setObjectName("sidebar")
        self.setFixedWidth(210)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 12)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("sidebarTitle")
        layout.addWidget(title_label)
        layout.addSpacing(20)

        for label, index in navigation_items:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, i=index: self.navigation_requested.emit(i))

            layout.addWidget(btn)

        layout.addStretch()

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