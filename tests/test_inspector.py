"""
Tests for the accessibility inspector utility.
"""

import pytest
import tkinter as tk
from tkaria11y import AccessibleApp
from tkaria11y.widgets import AccessibleButton
from tkaria11y.utils_inspector import launch_inspector


def test_inspector_creation():
    """Test that inspector can be created and destroyed without errors"""
    try:
        app = AccessibleApp()
    except tk.TclError as e:
        pytest.skip(f"GUI not available: {e}")

    # Launch inspector
    inspector = launch_inspector(app)

    # Verify inspector exists
    assert inspector.winfo_exists()
    assert inspector.title() == "A11y Inspector"

    # Clean up
    inspector.destroy()
    app.destroy()


def test_inspector_focus_handling():
    """Test that inspector handles focus events without crashing"""
    try:
        app = AccessibleApp()
    except tk.TclError as e:
        pytest.skip(f"GUI not available: {e}")

    # Create a widget
    button = AccessibleButton(app, text="Test", accessible_name="Test button")
    button.pack()

    # Launch inspector
    inspector = launch_inspector(app)

    # Simulate focus events
    button.focus_set()
    app.update()

    # Destroy inspector while focus events might still be active
    inspector.destroy()

    # Focus again - this should not crash
    button.focus_set()
    app.update()

    # Clean up
    app.destroy()


def test_inspector_with_accessible_app():
    """Test inspector integration with AccessibleApp"""
    try:
        app = AccessibleApp(enable_inspector=True)
    except tk.TclError as e:
        pytest.skip(f"GUI not available: {e}")

    # Add some widgets
    button = AccessibleButton(app, text="Test", accessible_name="Test button")
    button.pack()

    # Focus the button
    button.focus_set()
    app.update()

    # This should not raise any exceptions
    app.destroy()
