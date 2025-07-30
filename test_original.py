#!/usr/bin/env python3
"""
Test file for migration script - all widget types.
"""

import tkinter as tk
import tkinter.ttk as ttk
try:
    import customtkinter as ctk
from tkaria11y.widgets import (AccessibleButton, AccessibleCTKButton,
    AccessibleCTKEntry, AccessibleCombobox, AccessibleEntry, AccessibleLabel,
    AccessibleTTKButton, AccessibleTTKEntry
)
except ImportError:
    ctk = None

class TestApp:
    def __init__(self):
        self.root = tk.Tk()
        
        # Standard tkinter widgets
        self.button = AccessibleButton(self.root, accessible_name="Click Me", text="Click Me")
        self.entry = AccessibleEntry(self.root)  # TODO: Add accessible_name parameter
        self.label = AccessibleLabel(self.root, text="Hello")
        
        # TTK widgets
        self.ttk_button = AccessibleTTKButton(self.root, accessible_name="TTK Button", text="TTK Button")
        self.ttk_entry = AccessibleTTKEntry(self.root)  # TODO: Add accessible_name parameter
        self.ttk_combobox = AccessibleCombobox(self.root)
        
        # CustomTkinter widgets (if available)
        if ctk:
            self.ctk_button = AccessibleCTKButton(self.root, accessible_name="CTK Button", text="CTK Button")
            self.ctk_entry = AccessibleCTKEntry(self.root)  # TODO: Add accessible_name parameter
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TestApp()
    app.run()