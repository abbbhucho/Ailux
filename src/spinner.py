# spinner.py
import sys
import threading
import itertools
import time

class Spinner:
    """
    Simple thread-based CLI spinner.
    Usage:
        spinner = Spinner("Starting AILUX...")
        spinner.start()
        do_work()
        spinner.stop()
    Or use as a context manager:
        with Spinner("Starting AILUX..."):
            do_work()
    """
    def __init__(self, text="Loading", delay=0.08):
        self.text = text
        self.delay = delay
        self._running = False
        self._thread = None
        # characters to create a rotating-pipe effect:
        self._spin_chars = itertools.cycle(["|", "/", "-", "\\"])

    def _run(self):
        # keep printing spinner until stopped
        while self._running:
            ch = next(self._spin_chars)
            out = f"\r{ch} {self.text}"
            # write and flush without newline; \r returns to line start
            sys.stdout.write(out)
            sys.stdout.flush()
            time.sleep(self.delay)
        # clear the line when done
        sys.stdout.write("\r" + " " * (len(self.text) + 4) + "\r")
        sys.stdout.flush()

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        if not self._running:
            return
        self._running = False
        # wait briefly for thread to finish
        if self._thread:
            self._thread.join(timeout=1)
            self._thread = None

    # Context manager support
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()