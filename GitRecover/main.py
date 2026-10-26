import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThreadPool
from GitRecover.gui.window import MainWindow
from GitRecover.services.recovery_service import RecoveryService
from GitRecover.ai.llm_provider import LLMProvider
from qt_material import apply_stylesheet

def main():
    app = QApplication(sys.argv)
    
    QThreadPool.globalInstance().setMaxThreadCount(1)

    llm_provider = LLMProvider()
    recovery_service = RecoveryService(llm_provider)
    window = MainWindow(recovery_service)

    apply_stylesheet(app, theme="dark_lightgreen.xml")
    window.show()
    
    app.exec()

if __name__ == "__main__":
    main()