"""
Author: Kent Pawson
progress_dialog.py displays progress for background recovery tasks.
"""

from PySide6.QtWidgets import QProgressDialog
from PySide6.QtCore import Qt

class ProgressDialog(QProgressDialog):
    def __init__(self, title="Initializing Recovery Session", text="Initializing...", parent=None):
        """Initialize the progress dialog.

        Parameters:
            title: Dialog title.
            text: Initial progress text.
            parent: Optional parent widget.
        """
        super().__init__(text, None, 0, 100, parent)

        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModal)

        self.setMinimumDuration(0)
        self.setAutoClose(True)
        self.setAutoReset(True)

        self._apply_styles()

    def update_progress(self, value: int, message: str = ""):
        """Update the progress value and optional message.

        Parameters:
            value: Progress percentage.
            message: Optional progress description.
        """
        self.setValue(value)
        if message:
            self.setLabelText(message)

    def _apply_styles(self):
        """Apply dialog-specific styles."""
        self.setStyleSheet("""
        """)