#!/usr/bin/env python3
"""
Test file with nested try blocks.
"""

import tkinter as tk
import tkinter.ttk as ttk

from tkaria11y.widgets import AccessibleButton


def some_function():
    try:
        import some_module

        try:
            import customtkinter as ctk
        except ImportError:
            ctk = None
    except ImportError:
        pass


class TestApp:
    def __init__(self):
        self.root = tk.Tk()
        self.button = AccessibleButton(
            self.root, accessible_name="Click Me", text="Click Me"
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TestApp()
    app.run()
