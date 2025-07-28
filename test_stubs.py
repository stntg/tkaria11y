#!/usr/bin/env python3
"""
Simple test to verify stub files work correctly
"""

import tkaria11y
from tkaria11y import widgets, mixins, themes, utils


def test_basic_imports():
    """Test that basic imports work"""
    # Test main module
    app = tkaria11y.AccessibleApp(title="Test App")

    # Test widgets
    button = widgets.AccessibleButton(app, text="Test")

    # Test mixins
    from tkaria11y.mixins import ARIARole, ARIAProperty

    # Test themes
    font_manager = themes.AccessibilityFontManager(app)

    print("✓ All imports successful!")
    app.destroy()


if __name__ == "__main__":
    test_basic_imports()
