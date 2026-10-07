from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QFileDialog, QLabel

if TYPE_CHECKING:
    from GitRecover.gui.window import MainWindow

class Page(QWidget):
    def __init__(self, root: MainWindow):
        super().__init__()
        self.root = root

    def _handle_browse(self, file_label: QLabel):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select your Git Repo",
            dir=str(Path.cwd()),
            options=QFileDialog.Option.ShowDirsOnly
        )

        if directory:
            file_label.setText(directory)