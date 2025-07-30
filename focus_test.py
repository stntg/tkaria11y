#!/usr/bin/env python3
"""
Test focus indicator on different widget types
"""

import tkinter as tk
from tkaria11y.app import AccessibleApp
from tkaria11y.widgets import AccessibleButton, AccessibleEntry, AccessibleLabel

def test_focus():
    """Test focus indicator on different widgets"""
    
    app = AccessibleApp(title="Focus Test", high_contrast=True)
    
    # Regular Tkinter widgets
    AccessibleLabel(app, text="Regular Accessible Widgets:", font=("Arial", 12, "bold")).pack(pady=10)
    
    AccessibleButton(app, text="Accessible Button 1", accessible_name="Test Button 1").pack(pady=5)
    AccessibleEntry(app, accessible_name="Test Entry 1").pack(pady=5)
    AccessibleButton(app, text="Accessible Button 2", accessible_name="Test Button 2").pack(pady=5)
    
    # Regular Tkinter widgets (non-accessible)
    AccessibleLabel(app, text="Regular Tkinter Widgets:", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Button(app, text="Regular Button 1").pack(pady=5)
    tk.Entry(app).pack(pady=5)
    tk.Button(app, text="Regular Button 2").pack(pady=5)
    
    print("Focus test created. Tab through widgets to see focus indicator.")
    print("Expected: Yellow focus indicator should appear on all widgets when focused.")
    
    app.mainloop()

if __name__ == "__main__":
    test_focus()