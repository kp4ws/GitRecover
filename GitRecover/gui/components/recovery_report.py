"""
Author: Kent Pawson
recovery_report.py summarizes repository status and recovery candidates.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from GitRecover.core.schemas import RecoveryRequest, RemoteSyncStatus, RepoStatus
from GitRecover.gui.colors import GOOD, BAD, WARNING


class RecoveryReport(QDialog):
    view_history_event = Signal()

    def __init__(self, request: RecoveryRequest, parent=None):
        """Initialize the recovery report dialog.

        Parameters:
            request: Recovery request being reported.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setWindowTitle("Recovery Report")
        self.setMinimumWidth(520)

        self.request = request

        self.dangling_commits = []
        for commit in request.history.commit_history:
            if commit.is_dangling:
                self.dangling_commits.append(commit)

        state = request.state
        dangling_count = len(self.dangling_commits)

        findings = []
        if state.status == RepoStatus.REBASE:
            findings.append("WARNING: a Git rebase is currently in progress.")
        elif state.status == RepoStatus.MERGE:
            findings.append("WARNING: a Git merge is currently in progress.")
        elif state.status == RepoStatus.CHERRY_PICK:
            findings.append("WARNING: a Git cherry pick is currently in progress.")

        if state.status == RepoStatus.DIRTY:
            findings.append("WARNING: Uncommitted changes were found in the selected reposiory.")
        if state.status == RepoStatus.DETACHED:
            findings.append("WARNING: HEAD is detached.")
        if dangling_count:
            findings.append(f"Found {dangling_count} possible recovery commit(s) to review below.")

        summary = ""
        color = ""
        if len(findings) > 0:
            summary = " ".join(findings)
            color = WARNING
        else:
            summary = "No issues were found by the current checks." 
            color = ""

        summary_label = QLabel(summary)
        summary_label.setStyleSheet(f"color: {color};")
        summary_label.setWordWrap(True)
        
        candidates_group = QGroupBox("Possible recovery commits")
        candidates_layout = QVBoxLayout(candidates_group)
        if self.dangling_commits:
            #Go through last 5 commits
            for commit in self.dangling_commits[:5]:
                row = QHBoxLayout()
                
                commit_label = QLabel(f"{commit.hash[:12]}  {commit.message} ({commit.date})")
                commit_label.setWordWrap(True)
                
                row.addWidget(commit_label, 1)
                candidates_layout.addLayout(row)

            #If more than 5 commits, notify
            if dangling_count > 5:
                more_candidates_label = QLabel("More candidate(s) are available in History.")
                candidates_layout.addWidget(more_candidates_label)
        else:
            candidates_layout.addWidget(QLabel("No dangling commits identified."))

        context_group = QGroupBox("Repository context")
        details = QFormLayout(context_group)

        details.addRow("Repository:", self._detail_label(request.repo_path, word_wrap=True))
        
        repo_head = self._detail_label(state.current_head[:7])
        details.addRow("HEAD:", repo_head)

        current_branch = self._detail_label("")
        details.addRow("Current branch:", current_branch)
        
        repo_status = self._detail_label(state.status.value)
        details.addRow("Status:", repo_status)
        
        dangling_commits_count = self._detail_label(str(dangling_count))
        details.addRow("Dangling commits:", dangling_commits_count)
        
        remote_sync = self._detail_label(state.remote_sync.display_text, word_wrap=True)
        details.addRow("Remote sync:", remote_sync)

        #TODO: This functionality is copied from home page. If time permitted, look into way to refactor this into cleaner code
        #If empty string, then its in detatched head state
        if state.current_branch != "":
            current_branch.setText(state.current_branch)
            current_branch.setStyleSheet("")
            details.labelForField(current_branch).setStyleSheet("")
            repo_head.setStyleSheet("")
            details.labelForField(repo_head).setStyleSheet("")
        else:
            current_branch.setText("Detatched HEAD")
            current_branch.setStyleSheet(f"color: {WARNING};")
            details.labelForField(current_branch).setStyleSheet(f"color:{WARNING};")
            repo_head.setStyleSheet(f"color: {WARNING};")
            details.labelForField(repo_head).setStyleSheet(f"color: {WARNING};")

        if state.status == RepoStatus.CLEAN:
            repo_status.setStyleSheet(f"color: {GOOD};")
            details.labelForField(repo_status).setStyleSheet(f"color: {GOOD};")
        elif state.status == RepoStatus.DIRTY:
            repo_status.setStyleSheet(f"color: {BAD};")
            details.labelForField(repo_status).setStyleSheet(f"color: {BAD};")
        else:
            repo_status.setStyleSheet(f"color: {WARNING};")
            details.labelForField(repo_status).setStyleSheet(f"color: {WARNING};")

        if len(self.dangling_commits) > 0:
            dangling_commits_count.setStyleSheet(f"color: {BAD}")
            details.labelForField(dangling_commits_count).setStyleSheet(f"color: {BAD};")
        else:
            dangling_commits_count.setStyleSheet(f"color: {GOOD}")
            details.labelForField(dangling_commits_count).setStyleSheet(f"color: {GOOD};")

        if state.remote_sync.status == RemoteSyncStatus.UP_TO_DATE:
            remote_sync.setStyleSheet(f"color: {GOOD};")
            details.labelForField(remote_sync).setStyleSheet(f"color: {GOOD};")
        elif state.remote_sync.status in (RemoteSyncStatus.BEHIND, RemoteSyncStatus.DIVERGED, RemoteSyncStatus.ERROR):
            remote_sync.setStyleSheet(f"color: {BAD};")
            details.labelForField(remote_sync).setStyleSheet(f"color: {BAD};")
        elif state.remote_sync.status != RemoteSyncStatus.NOT_CHECKED:
            remote_sync.setStyleSheet(f"color: {WARNING};")
            details.labelForField(remote_sync).setStyleSheet(f"color: {WARNING};")

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)

        reflogs_button = buttons.addButton("View Reflogs", QDialogButtonBox.ButtonRole.ActionRole)
        reflogs_button.setEnabled(bool(request.history.commit_history))
        reflogs_button.clicked.connect(self._view_history)
        
        copy_button = buttons.addButton("Copy Report", QDialogButtonBox.ButtonRole.ActionRole,)
        copy_button.clicked.connect(lambda: self._copy_report(copy_button))

        layout = QVBoxLayout(self)
        layout.addWidget(summary_label)
        layout.addWidget(candidates_group)
        layout.addWidget(context_group)
        layout.addWidget(buttons)

    def _view_history(self) -> None:
        """Navigate to the history page and close the report."""
        self.view_history_event.emit()
        #Auto close form when going to history page
        self.accept()

    def _copy_report(self, button: QPushButton) -> None:
        """Copy the recovery report to the clipboard.

        Parameters:
            button: Button used to trigger the action.
        """
        state = self.request.state

        dangling_commits_text = ""
        if not self.dangling_commits:
            dangling_commits_text = "No dangling commits identified"

        #Bounded to max 5 iterations
        for commit in self.dangling_commits[:5]:
            dangling_commits_text += f"{commit.hash}: {commit.message} {commit.date}\n"

        branch = ""
        if state.current_branch != "":
            branch = state.current_branch
        else:
            branch = "Detached HEAD"

        report = (
            f"Repository: {self.request.repo_path}\n"
            f"Status: {state.status.value}\n"
            f"Branch: {branch}\n"
            f"HEAD: {state.current_head}\n"
            f"Possible recovery commits:\n{dangling_commits_text}\n"
            f"Remote sync: {state.remote_sync.display_text}\n"
        )

        QGuiApplication.clipboard().setText(report)
        button.setText("Copied")

    def _detail_label(self, text: str, word_wrap: bool = False) -> QLabel:
        """Create a selectable report-detail label.

        Parameters:
            text: Label text.
            word_wrap: Whether text should wrap.

        Returns:
            The configured label.
        """
        label = QLabel(text)
        label.setWordWrap(word_wrap)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        return label
