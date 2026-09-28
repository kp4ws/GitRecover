from PySide6.QtCore import QObject, Signal

class WorkerSignals(QObject):

    finished = Signal(int)
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(tuple)