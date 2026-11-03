from PySide6.QtCore import QRunnable, Slot
from GitRecover.workers.worker_signal import WorkerSignals

import traceback
import sys

class Worker(QRunnable):
    """Worker thread"""
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.thread_id = kwargs.get("thread_id", 0)

    @Slot()
    def run(self):
        def report_progress(value: int, message: str = ""):
            self.signals.progress.emit(value, message)
        try:
            result = self.fn(*self.args, **self.kwargs, progress_callback=report_progress)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit(self.thread_id)
