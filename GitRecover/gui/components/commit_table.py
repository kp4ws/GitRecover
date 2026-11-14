from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
)
from GitRecover.core.schemas import GitCommit
from GitRecover.gui.colors import GOOD, BAD
from GitRecover.gui.components.commit_details import CommitDetails

class CommitTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(["Hash", "Action", "Message", "Author", "Date", "Status", ""])

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) #Hash
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) #Action
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) #Message
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) #Author
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) #Date
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) #Status
        self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents) #Details button

        self.horizontalHeader().setSectionsMovable(True)
        self.horizontalHeader().setMinimumSectionSize(110)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(45)

        #Make table read only
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)

    def refresh_data(self, commits: list[GitCommit]):
        self.setRowCount(len(commits))

        for row, commit in enumerate(commits):
            commit_hash = QTableWidgetItem(commit.hash[:7])
            commit_message = QTableWidgetItem(commit.message)
            commit_author = QTableWidgetItem(commit.author)
            commit_date = QTableWidgetItem(commit.date)

            #status column
            if commit.is_dangling:
                status_text = "Orphaned"
                status_color = BAD
            else:
                status_text = "Active"
                status_color = GOOD

            action_type = commit.reflog_action.partition(":")[0].strip() or "Not recorded"
            action = QTableWidgetItem(action_type)

            self.setItem(row, 0, commit_hash)
            self.setItem(row, 1, action)
            self.setItem(row, 2, commit_message)
            self.setItem(row, 3, commit_author)
            self.setItem(row, 4, commit_date)

            #Adds coloring to status column
            self.setCellWidget(row, 5, self._colored_label(status_text, status_color))

            details_btn = QPushButton("Details")
            details_btn.clicked.connect(lambda checked=False, selected_commit=commit: self._on_view_clicked(selected_commit))
            self.setCellWidget(row, 6, details_btn)

    def _on_view_clicked(self, commit: GitCommit):
        dialog = CommitDetails(commit, self)
        dialog.exec()

    def _colored_label(self, text: str, color: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(f"color: {color}; background: transparent;")
        return label