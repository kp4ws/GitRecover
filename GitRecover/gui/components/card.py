from PySide6.QtWidgets import QVBoxLayout, QWidget, QLayout, QGroupBox

class Card(QGroupBox):
    def __init__(self, title, items):
        super().__init__()
        self.setTitle(title)
        self._create_widgets(items)
        self._apply_styles()

    def _create_widgets(self, items):
        self.setObjectName("card")
        layout = QVBoxLayout(self)

        for item in items:
            if isinstance(item, QWidget):
                layout.addWidget(item)
            elif isinstance(item, QLayout):
                layout.addLayout(item)
            else:
                print("Unsupported widget type")

    def _apply_styles(self):
        self.setStyleSheet("""
        """)