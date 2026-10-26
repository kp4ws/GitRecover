from __future__ import annotations

from pathlib import Path
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QFileDialog, QLabel

if TYPE_CHECKING:
    from GitRecover.gui.window import MainWindow
    from GitRecover.services.recovery_service import RecoveryService

class Page(QWidget):
    def __init__(self, root: MainWindow, recovery_service: RecoveryService):
        super().__init__()
        self.root = root
        self.recovery_service = recovery_service

    def browse_directory(self, file_label: QLabel) -> None:
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select your Git Repo",
            dir=str(Path.cwd()),
            options=QFileDialog.Option.ShowDirsOnly
        )

        if directory:
            file_label.setText(directory)

    def browse_file(self) -> str | None:
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
        pass