# tests/test_app.py

import pytest
import tkinter as tk
from tkaria11y.app import AccessibleApp


def test_accessible_app_creation():
    """Test basic AccessibleApp creation"""
    app = AccessibleApp(title="Test App")
    assert isinstance(app, tk.Tk)
    assert app.title() == "Test App"
    app.destroy()


def test_accessible_app_with_options():
    """Test AccessibleApp with accessibility options"""
    app = AccessibleApp(
        title="Test App", high_contrast=True, dyslexic_font=True, scaling=1.2
    )
    assert isinstance(app, tk.Tk)
    assert app.title() == "Test App"
    app.destroy()


def test_accessible_app_inspector():
    """Test AccessibleApp with inspector enabled"""
    try:
        app = AccessibleApp(enable_inspector=True)
    except tk.TclError as e:
        pytest.skip(f"GUI not available: {e}")
    assert isinstance(app, tk.Tk)
    # Inspector should be created but not necessarily visible
    app.destroy()
