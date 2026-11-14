from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from GitRecover.core.schemas import GitCommit

class CommitDetails(QDialog):
    def __init__(self, commit: GitCommit, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Commit Details")          
        self.setMinimumWidth(500)
        
        details = QFormLayout()
        details.addRow("Hash:", self._detail_label(commit.hash))

        if commit.reflog_action:
            action_type = commit.reflog_action.partition(":")[0].strip()
            details.addRow("Action:", self._detail_label(action_type, word_wrap=True))

        details.addRow("Message:", self._detail_label(commit.message, word_wrap=True))
        details.addRow("Author:", self._detail_label(commit.author))
        details.addRow("Date:", self._detail_label(commit.date))

        if commit.is_dangling:
            details.addRow("Status:", self._detail_label("Dangling"))
        else:
            details.addRow("Status:", self._detail_label("Active"))
        
        if len(commit.parents) > 1:
            details.addRow("Type", self._detail_label("Merge Commit"))
        else:
            details.addRow("Type", self._detail_label("Regular Commit"))

        if commit.parents:
            details.addRow("Parents:", self._detail_label("\n".join(commit.parents), word_wrap=True))
        else:
            details.addRow("Parents:", self._detail_label("None"))

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        
        copy_button = buttons.addButton("Copy Details", QDialogButtonBox.ButtonRole.ActionRole)
        copy_button.clicked.connect(lambda: self._copy_commit_details(commit, copy_button))

        layout = QVBoxLayout(self)
        layout.addLayout(details)
        layout.addWidget(buttons)

    def _copy_commit_details(self, commit: GitCommit, button: QPushButton) -> None:
        #TODO this functionality is repeated, consider refactoring code to make this cleaner
        if commit.is_dangling:
            status = "Dangling"
        else:
            status = "Active"

        if len(commit.parents) > 1:
            commit_type = "Merge Commit"
        else:
            commit_type = "Regular Commit"

        if commit.parents:
            parents = ", ".join(commit.parents)
        else:
            parents = "None"
        
        details = (
            f"Hash: {commit.hash}\n"
            f"Reflog Action: {commit.reflog_action}\n"
            f"Message: {commit.message}\n"
            f"Author: {commit.author}\n"
            f"Date: {commit.date}\n"
            f"Status: {status}\n"
            f"Type: {commit_type}\n"
            f"Parents: {parents}"
        )
        
        QGuiApplication.clipboard().setText(details)
        button.setText("Copied")

    def _detail_label(self, text: str, word_wrap: bool = False) -> QLabel:
        label = QLabel(text)
        label.setWordWrap(word_wrap)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        return label