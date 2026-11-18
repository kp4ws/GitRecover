"""
Author: Kent Pawson
worker_signal.py defines signals used to communicate background worker progress and results.
"""

from PySide6.QtCore import QObject, Signal

class WorkerSignals(QObject):

    finished = Signal(int)
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int, str)