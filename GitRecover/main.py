import sys
from PySide6.QtWidgets import QApplication
from GitRecover.gui.window import MainWindow


from GitRecover.git.git_cmds import git_log

def main():
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # app.exec()

    git_log()

if __name__ == "__main__":
    main()