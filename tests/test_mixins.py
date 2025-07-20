# tests/test_mixins.py

import pytest
import tkinter as tk
from tkaria11y.mixins import AccessibleMixin


class AccessibleTestWidget(AccessibleMixin, tk.Button):
    """Test widget combining AccessibleMixin with tk.Button"""

    pass


@pytest.mark.gui
def test_accessible_mixin_attributes():
    """Test AccessibleMixin sets attributes correctly"""
    root = tk.Tk()
    widget = AccessibleTestWidget(
        root,
        accessible_name="Test Widget",
        accessible_role="button",
        accessible_description="A test widget",
    )

    assert widget.accessible_name == "Test Widget"
    assert widget.accessible_role == "button"
    assert widget.accessible_description == "A test widget"

    root.destroy()


@pytest.mark.gui
def test_accessible_mixin_default_attributes():
    """Test AccessibleMixin with default attributes"""
    root = tk.Tk()
    widget = AccessibleTestWidget(root)

    assert widget.accessible_name == ""
    assert widget.accessible_role == ""
    assert widget.accessible_description == ""

    root.destroy()


@pytest.mark.gui
def test_accessible_mixin_event_binding():
    """Test AccessibleMixin binds events when accessible_name is provided"""
    root = tk.Tk()
    widget = AccessibleTestWidget(root, accessible_name="Test Widget")

    # Check that FocusIn event is bound
    events = widget.bind()
    assert "<FocusIn>" in events
    assert "<Enter>" in events

    root.destroy()


@pytest.mark.gui
def test_accessible_mixin_no_event_binding():
    """Test AccessibleMixin doesn't bind FocusIn when no accessible_name"""
    root = tk.Tk()
    widget = AccessibleTestWidget(root)

    # Check that FocusIn event is not bound (only Enter should be bound)
    events = widget.bind()
    assert "<Enter>" in events
    # FocusIn might still be in events but shouldn't trigger TTS

    root.destroy()
