"""
Pytest configuration and fixtures for tkaria11y tests.
"""

import pytest
import tkinter as tk
import gc
import os


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "gui: mark test as requiring GUI (may be skipped in headless environments)",
    )


def pytest_collection_modifyitems(config, items):
    """Skip GUI tests if running in headless environment or if GUI creation fails."""
    skip_gui = pytest.mark.skip(reason="GUI not available or unstable")

    # Test if GUI is available
    gui_available = True
    try:
        root = tk.Tk()
        root.destroy()
    except (tk.TclError, ImportError, OSError):
        # GUI not available - could be headless environment or missing display
        gui_available = False

    if not gui_available:
        for item in items:
            if "gui" in item.keywords or any(
                keyword in item.name.lower()
                for keyword in ["app", "theme", "integration"]
            ):
                item.add_marker(skip_gui)


@pytest.fixture(autouse=True)
def cleanup_tkinter():
    """
    Automatically clean up Tkinter resources after each test.
    This prevents test isolation issues with GUI components.
    """
    yield  # Run the test

    # Clean up TTS engine first to prevent Tcl_AsyncDelete warnings
    try:
        from tkaria11y.a11y_engine import tts

        if tts:
            tts.stop()  # Use stop instead of shutdown to avoid thread issues
    except (ImportError, AttributeError, RuntimeError):
        # TTS module may not be available or already cleaned up
        pass

    # Clean up any remaining Tkinter windows
    try:
        # Get all Tk instances and destroy them
        import tkinter as tk

        for obj in gc.get_objects():
            if isinstance(obj, tk.Tk):
                try:
                    obj.quit()  # Exit mainloop if running
                    obj.destroy()
                except (tk.TclError, RuntimeError):
                    pass  # Already destroyed or not initialized

        # Clear any remaining Tcl interpreters
        try:
            tk._default_root = None
        except AttributeError:
            pass

        # Force garbage collection
        gc.collect()

    except (ImportError, AttributeError, tk.TclError, RuntimeError):
        # Ignore cleanup errors - GUI components may already be destroyed
        pass


@pytest.fixture
def tk_root():
    """
    Provide a clean Tk root window for tests that need it.
    Automatically cleaned up after the test.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the window
    yield root
    try:
        root.destroy()
    except tk.TclError:
        pass  # Already destroyed
