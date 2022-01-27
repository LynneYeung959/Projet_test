import threading
import signal as sig

from .client import Client, ThreadClient, signal_handler

# Signal handler to catch crtl+c from client
sig.signal(sig.SIGINT, signal_handler)
signal_thread = threading.Event()

# Starting threads
ThreadClient().start()
signal_thread.wait()