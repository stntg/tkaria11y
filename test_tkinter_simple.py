#!/usr/bin/env python3
"""Simple test to check if Tkinter works in test environment."""

import tkinter as tk
import sys
import os


def test_tkinter_basic():
    """Test basic Tkinter functionality."""
    print("Python version:", sys.version)
    print("Platform:", sys.platform)

    # Check environment variables
    print("TCL_LIBRARY:", os.environ.get("TCL_LIBRARY", "Not set"))
    print("TK_LIBRARY:", os.environ.get("TK_LIBRARY", "Not set"))

    try:
        root = tk.Tk()
        root.withdraw()  # Hide the window
        print("✅ Tkinter root created successfully")

        # Test basic widget creation
        label = tk.Label(root, text="Test")
        print("✅ Widget created successfully")

        root.destroy()
        print("✅ Tkinter test completed successfully")
        return True

    except Exception as e:
        print(f"❌ Tkinter test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_tkinter_basic()
    sys.exit(0 if success else 1)
