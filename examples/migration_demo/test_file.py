#!/usr/bin/env python3
"""Test file for migration demonstration"""

import tkinter as tk
from tkaria11y.widgets import AccessibleEntry, AccessibleButton, AccessibleLabel


def create_simple_app():
    """Create a simple test application with accessible widgets."""
    root = tk.Tk()
    root.title("Test App")

    # Simple widgets
    label = AccessibleLabel(root, accessible_name="Hello World", text="Hello World")
    entry = AccessibleEntry(root)
    button = AccessibleButton(root, accessible_name="Click Me", text="Click Me")

    label.pack()
    entry.pack()
    button.pack()

    return root


if __name__ == "__main__":
    app = create_simple_app()
    app.mainloop()
