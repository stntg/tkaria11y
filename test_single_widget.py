#!/usr/bin/env python3
"""Single widget test to isolate Tkinter issues."""

import tkinter as tk
from tkaria11y import AccessibleApp
from tkaria11y.widgets import AccessibleButton


def test_single_widget():
    """Test creating a single accessible widget."""
    try:
        # Create app directly without fixtures
        app = AccessibleApp(title="Single Test")
        app.withdraw()

        # Create a simple widget
        button = AccessibleButton(
            app, text="Test Button", accessible_name="Test button"
        )
        button.pack()

        app.update_idletasks()

        # Verify it works
        assert button.cget("text") == "Test Button"
        assert hasattr(button, "accessible_name")

        # Clean up
        app.destroy()

        print("✅ Single widget test passed!")
        return True

    except Exception as e:
        print(f"❌ Single widget test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys

    success = test_single_widget()
    sys.exit(0 if success else 1)
