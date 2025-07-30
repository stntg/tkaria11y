# tests/test_integration.py

"""Integration tests to verify all components work together"""

import pytest
import tkinter as tk
from tkaria11y import AccessibleApp, speak
from tkaria11y.widgets import AccessibleButton, AccessibleEntry, AccessibleLabel
from tkaria11y.themes import HighContrastTheme


def test_full_app_integration():
    """Test that all components work together in a complete app"""
    # Create app with all features
    app = AccessibleApp(
        title="Integration Test", high_contrast=True, dyslexic_font=True, scaling=1.0
    )

    # Create various widgets
    label = AccessibleLabel(app, text="Test Label", accessible_name="Test label widget")

    entry = AccessibleEntry(
        app,
        accessible_name="Test input field",
        accessible_description="Enter test data here",
    )

    button = AccessibleButton(
        app,
        text="Submit",
        accessible_name="Submit button",
        accessible_description="Click to submit the form",
    )

    # Verify all widgets have correct attributes
    assert label.accessible_name == "Test label widget"
    assert label.accessible_role == "label"

    assert entry.accessible_name == "Test input field"
    assert entry.accessible_role == "textbox"
    assert entry.accessible_description == "Enter test data here"

    assert button.accessible_name == "Submit button"
    assert button.accessible_role == "button"
    assert button.accessible_description == "Click to submit the form"

    # Verify inheritance
    assert isinstance(label, tk.Label)
    assert isinstance(entry, tk.Entry)
    assert isinstance(button, tk.Button)

    app.destroy()


def test_theme_integration():
    """Test theme integration with widgets"""
    try:
        app = AccessibleApp()
    except tk.TclError as e:
        pytest.skip(f"GUI not available: {e}")

    # Create widgets
    AccessibleButton(app, text="Test", accessible_name="Test button")
    AccessibleEntry(app, accessible_name="Test entry")

    # Apply theme
    HighContrastTheme.apply(app)
    app.update()

    # Verify theme was applied (at least no errors)
    # Note: Actual color checking might be system-dependent

    app.destroy()


def test_tts_integration():
    """Test TTS integration (without actually speaking)"""
    # This tests that the TTS system can be called without errors
    speak("Test message")

    # Test with widgets
    try:
        app = AccessibleApp()
    except tk.TclError as e:
        pytest.skip(f"GUI not available: {e}")
    button = AccessibleButton(app, accessible_name="Test button")

    # Simulate focus event (this would normally trigger TTS)
    event = type("Event", (), {"widget": button})()
    button._on_focus_in(event)

    app.destroy()


def test_entry_point_integration():
    """Test that entry points work"""
    # Test the stub generator entry point
    from tkaria11y.scripts.generate_stubs import main

    # Should not raise an error
    main()


def test_package_metadata():
    """Test package metadata is accessible"""
    import tkaria11y

    assert hasattr(tkaria11y, "__version__")
    assert tkaria11y.__version__ == "0.0.1"


def test_widget_factory_completeness():
    """Test that the widget factory creates all expected widgets"""
    from tkaria11y.widgets import _WIDGET_MAP, __all__

    # Check that __all__ contains all expected widgets
    expected_widgets = [f"Accessible{name}" for name in _WIDGET_MAP.keys()]

    for widget_name in expected_widgets:
        assert widget_name in __all__

    # Check that we can import all widgets
    import tkaria11y.widgets as widgets_module

    for widget_name in expected_widgets:
        assert hasattr(widgets_module, widget_name)
        widget_class = getattr(widgets_module, widget_name)
        assert callable(widget_class)


def test_accessibility_features_integration():
    """Test that accessibility features work together"""
    app = AccessibleApp(
        high_contrast=True,
        dyslexic_font=True,
        enable_inspector=False,  # Don't create inspector window in tests
    )

    # Create a form-like structure
    title = AccessibleLabel(app, text="Login Form", accessible_name="Login form title")
    username_label = AccessibleLabel(
        app, text="Username:", accessible_name="Username label"
    )
    username_entry = AccessibleEntry(app, accessible_name="Username input")
    password_label = AccessibleLabel(
        app, text="Password:", accessible_name="Password label"
    )
    password_entry = AccessibleEntry(app, show="*", accessible_name="Password input")
    submit_btn = AccessibleButton(app, text="Login", accessible_name="Login button")

    # Pack widgets
    title.pack()
    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    submit_btn.pack()

    # Test that all widgets are properly configured
    widgets = [
        title,
        username_label,
        username_entry,
        password_label,
        password_entry,
        submit_btn,
    ]

    for widget in widgets:
        assert hasattr(widget, "accessible_name")
        assert hasattr(widget, "accessible_role")
        assert hasattr(widget, "accessible_description")
        assert widget.accessible_name != ""  # All should have names

    app.destroy()
