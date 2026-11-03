from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QPushButton
from PySide6.QtGui import QBrush, QColor
from GitRecover.core.schemas import GitCommit

class CommitTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(["Hash", "Message", "Author", "Date", "Status", "Type", ""])

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) #Hash
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) #Message
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents) #Author
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) #Date
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) #Status
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) #Structure
        self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents) #Structure Btn

        self.horizontalHeader().setSectionsMovable(True)
        self.verticalHeader().setVisible(False)

        #Make table read only
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def refresh_data(self, commits: list[GitCommit]):
        self.setRowCount(len(commits))

        for row, commit in enumerate(commits):
            commit_hash = QTableWidgetItem(commit.hash[:7])
            commit_message = QTableWidgetItem(commit.message)
            commit_author = QTableWidgetItem(commit.author)
            commit_date = QTableWidgetItem(commit.date)

            #status column
            if commit.is_dangling:
                status_item = QTableWidgetItem("Orphaned")
                status_item.setForeground(QColor.red)
            else:
                status_item = QTableWidgetItem("Active")
                status_item.setForeground(QColor.green)

            #type column
            if len(commit.parents) > 1:
                type_item = QTableWidgetItem("Merge")
                type_item.setForeground(QColor.yellow)
            else:
                type_item = QTableWidgetItem()
            
            self.setItem(row, 0, commit_hash)
            self.setItem(row, 1, commit_message)
            self.setItem(row, 2, commit_author)
            self.setItem(row, 3, commit_date)
            self.setItem(row, 4, status_item),
            self.setItem(row, 5, type_item)

            row_type_btn = QPushButton("Show")
            # row_type_btn.clicked.connect() #TODO connect btn to show commit popup

            self.setCellWidget(row, 6, row_type_btn)