#!/usr/bin/env python3
"""
Test CTK button focus specifically
"""

import tkinter as tk
from tkaria11y.app import AccessibleApp
from tkaria11y.widgets import AccessibleCTKButton, AccessibleButton, CTK_AVAILABLE
from tkaria11y.focus_manager import get_focus_manager

def test_ctk_button_focus():
    """Test CTK button focus specifically"""
    
    if not CTK_AVAILABLE:
        print("CustomTkinter not available")
        return
    
    app = AccessibleApp(title="CTK Button Focus Test")
    focus_manager = get_focus_manager(app)
    
    # Create a regular button and CTK button
    regular_button = AccessibleButton(app, text="Regular Button", accessible_name="Regular Button")
    regular_button.pack(pady=10)
    
    ctk_button = AccessibleCTKButton(app, text="CTK Button", accessible_name="CTK Button")
    ctk_button.pack(pady=10)
    
    print("Widgets created:")
    print(f"Regular button registered: {regular_button in focus_manager._focus_order}")
    print(f"CTK button registered: {ctk_button in focus_manager._focus_order}")
    
    # Show the window
    app.update()
    
    print("\nTesting focus navigation:")
    
    # Test focusing each widget manually
    print("1. Focusing regular button...")
    try:
        regular_button.focus_set()
        current_focus = app.focus_get()
        print(f"   Current focus: {current_focus}")
        print(f"   Is regular button: {current_focus == regular_button}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("2. Focusing CTK button...")
    try:
        focus_manager._focus_ctk_widget(ctk_button)
        current_focus = app.focus_get()
        print(f"   Current focus: {current_focus}")
        print(f"   Is CTK button: {current_focus == ctk_button}")
        
        # Check if it's an internal widget
        if hasattr(ctk_button, '_text_label') and current_focus == ctk_button._text_label:
            print("   Focus is on CTK button's text label")
        elif hasattr(ctk_button, '_canvas') and current_focus == ctk_button._canvas:
            print("   Focus is on CTK button's canvas")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("3. Testing focus manager navigation...")
    try:
        # Set focus to first widget
        focus_manager._current_focus_index = 0
        success = focus_manager.focus_next()
        print(f"   focus_next() returned: {success}")
        
        current_focus = app.focus_get()
        print(f"   Current focus after focus_next: {current_focus}")
        
        # Try again
        success = focus_manager.focus_next()
        print(f"   Second focus_next() returned: {success}")
        
        current_focus = app.focus_get()
        print(f"   Current focus after second focus_next: {current_focus}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    app.destroy()

if __name__ == "__main__":
    test_ctk_button_focus()