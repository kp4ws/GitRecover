import sys
from PySide6.QtWidgets import QApplication
from GitRecover.gui.window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()

if __name__ == "__main__":
    main()