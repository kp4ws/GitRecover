import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThreadPool
from GitRecover.gui.window import MainWindow
from GitRecover.services.recovery_service import RecoveryService
from qt_material import apply_stylesheet

def main():
    recovery_engine = RecoveryService()
    
    QThreadPool.globalInstance().setMaxThreadCount(1)

    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_lightgreen.xml")
    window = MainWindow(recovery_engine)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()