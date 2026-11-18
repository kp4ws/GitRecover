"""
Author: Kent Pawson
page.py provides shared behavior and navigation for application pages.
"""

from __future__ import annotations

from pathlib import Path
from abc import abstractmethod
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QFileDialog, QLabel

if TYPE_CHECKING:
    from GitRecover.gui.window import MainWindow
    from GitRecover.services.recovery_service import RecoveryService

class Page(QWidget):
    def __init__(self, root: MainWindow, recovery_service: RecoveryService):
        """Initialize a page.

        Parameters:
            root: Main application window.
            recovery_service: Shared recovery service.
        """
        super().__init__()
        self.root = root
        self.recovery_service = recovery_service

    def browse_directory(self, file_label: QLabel) -> None:
        """Open a directory chooser and place the selected path in a label.

        Parameters:
            file_label: Label that receives the selected directory.
        """
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select your Git Repo",
            dir=str(Path.cwd()),
            options=QFileDialog.Option.ShowDirsOnly
        )

        if directory:
            file_label.setText(directory)

    def browse_file(self) -> str | None:
        """Open a file chooser for a recovery-session file.

        Returns:
            The selected path or None.
        """
        default_dir = Path.cwd() / "data"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select recovery session",
            dir=str(default_dir),
            filter="JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            return file_path
        return None

    @abstractmethod
    def refresh_UI(self):
        """Refresh the page from the active recovery session."""
        pass