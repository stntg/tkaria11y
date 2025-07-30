#!/usr/bin/env python3
"""
Comprehensive test file for migration script.
Tests all supported widget types: tkinter, ttk, and customtkinter.
"""

import tkinter as tk
import tkinter.ttk as ttk
try:
    import customtkinter as ctk
from tkaria11y.widgets import AccessibleButton, AccessibleCTKButton
    AccessibleCTKCheckBox, AccessibleCTKComboBox, AccessibleCTKEntry
    AccessibleCTKFrame, AccessibleCTKLabel, AccessibleCTKProgressBar
    AccessibleCTKRadioButton, AccessibleCTKSlider, AccessibleCTKSwitch
    AccessibleCTKTextbox, AccessibleCheckbutton, AccessibleCombobox, AccessibleEntry
    AccessibleFrame, AccessibleLabel, AccessibleListbox, AccessibleNotebook
    AccessibleRadiobutton, AccessibleScale, AccessibleSpinbox
    AccessibleTTKProgressbar, AccessibleTTKSeparator, AccessibleText
    AccessibleTreeview
except ImportError:
    ctk = None

class ComprehensiveTestApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Comprehensive Widget Test")
        
        # Standard tkinter widgets
        self.tk_button = AccessibleButton(self.root, accessible_name="TK Button", text="TK Button")
        self.tk_entry = AccessibleEntry(self.root)  # TODO: Add accessible_name parameter  # TODO: Add accessible_name parameter
        self.tk_label = AccessibleLabel(self.root, text="TK Label")
        self.tk_checkbutton = AccessibleCheckbutton(self.root, accessible_name="TK Checkbox", text="TK Checkbox")
        self.tk_radiobutton = AccessibleRadiobutton(self.root, accessible_name="TK Radio", text="TK Radio")
        self.tk_scale = AccessibleScale(self.root, from_=0, to=100)  # TODO: Add accessible_name parameter  # TODO: Add accessible_name parameter
        self.tk_listbox = AccessibleListbox(self.root)  # TODO: Add accessible_name parameter  # TODO: Add accessible_name parameter
        self.tk_frame = AccessibleFrame(self.root)
        self.tk_text = AccessibleText(self.root)
        self.tk_spinbox = AccessibleSpinbox(self.root, from_=0, to=100)
        
        # TTK widgets
        self.ttk_button = ttk.AccessibleButton(self.root, accessible_name="TTK Button", text="TTK Button")
        self.ttk_entry = ttk.AccessibleEntry(self.root)  # TODO: Add accessible_name parameter  # TODO: Add accessible_name parameter
        self.ttk_label = ttk.AccessibleLabel(self.root, text="TTK Label")
        self.ttk_checkbutton = ttk.AccessibleCheckbutton(self.root, accessible_name="TTK Checkbox", text="TTK Checkbox")
        self.ttk_radiobutton = ttk.AccessibleRadiobutton(self.root, accessible_name="TTK Radio", text="TTK Radio")
        self.ttk_scale = ttk.AccessibleScale(self.root, from_=0, to=100)  # TODO: Add accessible_name parameter  # TODO: Add accessible_name parameter
        self.ttk_frame = ttk.AccessibleFrame(self.root)
        self.ttk_notebook = AccessibleNotebook(self.root)
        self.ttk_progressbar = AccessibleTTKProgressbar(self.root)
        self.ttk_combobox = AccessibleCombobox(self.root)
        self.ttk_treeview = AccessibleTreeview(self.root)
        self.ttk_separator = AccessibleTTKSeparator(self.root)
        
        # CustomTkinter widgets (if available)
        if ctk:
            self.ctk_button = AccessibleCTKButton(self.root, accessible_name="CTK Button", text="CTK Button")
            self.ctk_entry = AccessibleCTKEntry(self.root)  # TODO: Add accessible_name parameter  # TODO: Add accessible_name parameter
            self.ctk_label = AccessibleCTKLabel(self.root, text="CTK Label")
            self.ctk_checkbox = AccessibleCTKCheckBox(self.root, text="CTK Checkbox")
            self.ctk_radiobutton = AccessibleCTKRadioButton(self.root, accessible_name="CTK Radio", text="CTK Radio")
            self.ctk_slider = AccessibleCTKSlider(self.root, from_=0, to=100)
            self.ctk_frame = AccessibleCTKFrame(self.root)
            self.ctk_progressbar = AccessibleCTKProgressBar(self.root)
            self.ctk_combobox = AccessibleCTKComboBox(self.root)
            self.ctk_textbox = AccessibleCTKTextbox(self.root)
            self.ctk_switch = AccessibleCTKSwitch(self.root, text="CTK Switch")
        
        # Direct imports (without prefix)
        button_direct = AccessibleButton(self.root, accessible_name="Direct Button", text="Direct Button")
        entry_direct = AccessibleEntry(self.root)  # TODO: Add accessible_name parameter
        label_direct = AccessibleLabel(self.root, text="Direct Label")
        
        # Widgets without text parameter (should get TODO comments)
        self.entry_no_text = AccessibleEntry(self.root)  # TODO: Add accessible_name parameter  # TODO: Add accessible_name parameter
        self.scale_no_text = AccessibleScale(self.root, from_=0, to=100)  # TODO: Add accessible_name parameter  # TODO: Add accessible_name parameter
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ComprehensiveTestApp()
    app.run()