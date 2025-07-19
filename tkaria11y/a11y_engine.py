# tkaria11y/a11y_engine.py

"""
Accessible A11y Engine:
Background TTS queue using pyttsx3, with lazy init, voice/rate/volume controls.
"""

import threading
import queue
import atexit

# import weakref
import pyttsx3
from typing import Optional, List
import tkinter as tk


class TTSEngine:
    def __init__(
        self,
        rate: int = 150,
        volume: float = 1.0,
        voice_id: Optional[str] = None,
    ):
        self._engine: Optional[pyttsx3.Engine] = None
        self._rate = rate
        self._volume = volume
        self._voice_id = voice_id

        self._queue: "queue.Queue[Optional[str]]" = queue.Queue()
        self._thread: Optional[threading.Thread] = None
        self._started = False
        self._shutdown_requested = False
        self._lock = threading.Lock()
        self._main_thread_id = threading.get_ident()

        # Register shutdown handler
        atexit.register(self.shutdown)

    def _init_engine(self) -> None:
        """Initialize the TTS engine with error handling - must be called from
        main thread"""
        if threading.get_ident() != self._main_thread_id:
            return  # Don't initialize from worker thread

        try:
            if self._engine is None:
                self._engine = pyttsx3.init()
                self._engine.setProperty("rate", self._rate)
                self._engine.setProperty("volume", self._volume)
                if self._voice_id:
                    self._engine.setProperty("voice", self._voice_id)
        except (ImportError, RuntimeError, OSError):
            # If engine initialization fails, set to None to prevent further attempts
            self._engine = None

    def _process_tts_queue(self) -> None:
        """Process TTS queue on main thread using Tkinter's after method"""
        if self._shutdown_requested:
            return

        try:
            # Process all pending items in the queue
            while not self._queue.empty() and not self._shutdown_requested:
                try:
                    text = self._queue.get_nowait()
                    if text is None:
                        return  # Shutdown signal

                    # Initialize engine if needed (on main thread)
                    if self._engine is None:
                        self._init_engine()

                    # Only proceed if engine was successfully initialized
                    if self._engine is not None:
                        try:
                            self._engine.say(text)
                            self._engine.runAndWait()
                        except (RuntimeError, OSError, AttributeError):
                            # Ignore TTS errors to prevent crashes
                            pass

                    self._queue.task_done()
                except queue.Empty:
                    break
                except (RuntimeError, AttributeError):
                    # Break on serious errors that indicate engine failure
                    break

        except (RuntimeError, AttributeError, OSError):
            # Thread or engine errors - stop processing
            pass

        # Schedule next processing if not shutting down
        if not self._shutdown_requested:
            try:
                # Try to get the root window to schedule the next call
                root = getattr(tk, "_default_root", None)
                if root and root.winfo_exists():
                    root.after(50, self._process_tts_queue)  # Check every 50ms
            except (tk.TclError, AttributeError):
                # No root window available, fall back to threading
                pass

    def speak(self, text: str) -> None:
        """Add text to the TTS queue"""
        if self._shutdown_requested:
            return

        with self._lock:
            if not self._started and not self._shutdown_requested:
                self._started = True
                # Start processing on main thread using Tkinter's after method
                try:
                    root = getattr(tk, "_default_root", None)
                    if root and root.winfo_exists():
                        root.after(10, self._process_tts_queue)
                except (tk.TclError, AttributeError):
                    # No Tkinter root available, skip TTS
                    return

        if not self._shutdown_requested:
            self._queue.put(text)

    def stop(self) -> None:
        """Stop the TTS engine"""
        self._shutdown_requested = True

        # Clear the queue
        try:
            while not self._queue.empty():
                self._queue.get_nowait()
                self._queue.task_done()
        except (queue.Empty, AttributeError):
            # Queue may be empty or already destroyed
            pass

        # Stop the engine if it exists
        if self._engine:
            try:
                self._engine.stop()
            except (RuntimeError, AttributeError):
                # Engine may already be stopped or destroyed
                pass

    def shutdown(self) -> None:
        """Shutdown the TTS engine safely"""
        if not self._shutdown_requested:
            self.stop()

        # Clean up the engine reference to prevent Tcl_AsyncDelete warnings
        # Only clean up from main thread
        if threading.get_ident() == self._main_thread_id and self._engine:
            try:
                self._engine = None
            except AttributeError:
                # Engine reference may already be cleared
                pass

    def set_rate(self, rate: int) -> None:
        """Set the speech rate"""
        self._rate = rate
        if self._engine and not self._shutdown_requested:
            try:
                self._engine.setProperty("rate", rate)
            except (RuntimeError, AttributeError):
                # Engine may not support rate setting or be destroyed
                pass

    def set_volume(self, volume: float) -> None:
        """Set the speech volume"""
        self._volume = volume
        if self._engine and not self._shutdown_requested:
            try:
                self._engine.setProperty("volume", volume)
            except (RuntimeError, AttributeError):
                # Engine may not support volume setting or be destroyed
                pass

    def list_voices(self) -> List[str]:
        """List available voices"""
        try:
            temp = pyttsx3.init()
            voices = temp.getProperty("voices")
            result = [v.id for v in voices] if voices else []
            # Clean up temporary engine
            try:
                temp.stop()
                del temp
            except (RuntimeError, AttributeError):
                # Temporary engine cleanup failed
                pass
            return result
        except (ImportError, RuntimeError, OSError):
            # TTS engine not available or failed to initialize
            return []

    def set_voice(self, voice_id: str) -> None:
        """Set the voice to use"""
        self._voice_id = voice_id
        if self._engine and not self._shutdown_requested:
            try:
                self._engine.setProperty("voice", voice_id)
            except (RuntimeError, AttributeError):
                # Engine may not support voice setting or be destroyed
                pass


# Global singleton
tts = TTSEngine()


def speak(text: str) -> None:
    """Shortcut to tts.speak"""
    tts.speak(text)


def shutdown_tts() -> None:
    """Shutdown the global TTS instance"""
    if tts:
        tts.shutdown()
