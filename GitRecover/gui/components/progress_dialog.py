from PySide6.QtWidgets import QProgressDialog
from PySide6.QtCore import Qt

class ProgressDialog(QProgressDialog):
    def __init__(self, title="Initializing Recovery Session", text="Initializing...", parent=None):
        super().__init__(text, None, 0, 100, parent)

        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModal)

        self.setMinimumDuration(0)
        self.setAutoClose(True)
        self.setAutoReset(True)

        self._apply_styles()

    def update_progress(self, value: int, message: str = ""):
        self.setValue(value)
        if message:
            self.setLabelText(message)

    def _apply_styles(self):
        self.setStyleSheet("""
        """)