#!/usr/bin/env python3
"""
Debug CustomTkinter focus issues
"""

import tkinter as tk
from tkaria11y.app import AccessibleApp
from tkaria11y.widgets import AccessibleCTKButton, CTK_AVAILABLE
from tkaria11y.focus_manager import get_focus_manager

def debug_ctk_focus():
    """Debug CTK button focus issues"""
    
    if not CTK_AVAILABLE:
        print("CustomTkinter not available")
        return
    
    app = AccessibleApp(title="CTK Focus Debug")
    focus_manager = get_focus_manager(app)
    
    # Create CTK button
    ctk_button = AccessibleCTKButton(app, text="CTK Button", accessible_name="CTK Button")
    ctk_button.pack(pady=20)
    
    print("CTK Button created")
    print(f"Widget class: {ctk_button.__class__.__name__}")
    print(f"Widget module: {ctk_button.__class__.__module__}")
    
    # Check if it's registered
    print(f"Registered in focus manager: {ctk_button in focus_manager._focus_order}")
    
    # Check if it's considered focusable by different methods
    print(f"_is_focusable_widget: {focus_manager._is_focusable_widget(ctk_button)}")
    print(f"_is_widget_focusable: {focus_manager._is_widget_focusable(ctk_button)}")
    
    # Check widget properties
    print("\nWidget properties:")
    try:
        print(f"  winfo_exists: {ctk_button.winfo_exists()}")
        print(f"  winfo_viewable: {ctk_button.winfo_viewable()}")
    except Exception as e:
        print(f"  Error checking basic properties: {e}")
    
    try:
        takefocus = ctk_button.cget("takefocus")
        print(f"  takefocus: {takefocus}")
    except Exception as e:
        print(f"  takefocus error: {e}")
    
    try:
        state = ctk_button.cget("state")
        print(f"  state: {state}")
    except Exception as e:
        print(f"  state error: {e}")
    
    # Try to focus the widget manually
    print("\nTrying to focus widget manually...")
    try:
        ctk_button.focus_set()
        print("  focus_set() succeeded")
        
        # Check if it actually has focus
        focused = app.focus_get()
        print(f"  Current focus: {focused}")
        print(f"  Focus is CTK button: {focused == ctk_button}")
    except Exception as e:
        print(f"  focus_set() error: {e}")
    
    app.destroy()

if __name__ == "__main__":
    debug_ctk_focus()