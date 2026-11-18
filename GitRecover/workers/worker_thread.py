"""
Author: Kent Pawson
worker_thread.py runs application tasks in a background Qt worker.
"""

from PySide6.QtCore import QRunnable, Slot
from GitRecover.workers.worker_signal import WorkerSignals

import traceback
import sys

class Worker(QRunnable):
    """Run a function in a Qt thread-pool worker."""
    def __init__(self, fn, *args, **kwargs):
        """Initialize the worker.

        Parameters:
            fn: Function to execute.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
        """
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.thread_id = kwargs.get("thread_id", 0)

    @Slot()
    def run(self):
        """Execute the worker function and emit its result or error."""
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
