#!/usr/bin/env python3
"""
Test focus navigation and indicators
"""

import tkinter as tk
from tkaria11y.app import AccessibleApp
from tkaria11y.widgets import (
    AccessibleButton, AccessibleEntry, AccessibleLabel,
    AccessibleTTKButton, AccessibleTTKEntry, 
    AccessibleCTKButton, AccessibleCTKEntry,
    CTK_AVAILABLE
)
from tkaria11y.focus_manager import get_focus_manager

def test_focus_navigation():
    """Test focus navigation with debug output"""
    
    app = AccessibleApp(title="Focus Navigation Test", high_contrast=True)
    
    # Get focus manager
    focus_manager = get_focus_manager(app)
    
    # Create test widgets
    AccessibleLabel(app, text="Focus Navigation Test", font=("Arial", 16, "bold")).pack(pady=10)
    
    # Regular Tkinter widgets
    AccessibleLabel(app, text="Regular Tkinter:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
    btn1 = AccessibleButton(app, text="Button 1", accessible_name="Button 1")
    btn1.pack(pady=2)
    
    entry1 = AccessibleEntry(app, accessible_name="Entry 1")
    entry1.pack(pady=2)
    
    # TTK widgets
    AccessibleLabel(app, text="TTK Widgets:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
    ttk_btn = AccessibleTTKButton(app, text="TTK Button", accessible_name="TTK Button")
    ttk_btn.pack(pady=2)
    
    ttk_entry = AccessibleTTKEntry(app, accessible_name="TTK Entry")
    ttk_entry.pack(pady=2)
    
    # CustomTkinter widgets
    if CTK_AVAILABLE:
        AccessibleLabel(app, text="CustomTkinter:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        ctk_btn = AccessibleCTKButton(app, text="CTK Button", accessible_name="CTK Button")
        ctk_btn.pack(pady=2)
        
        ctk_entry = AccessibleCTKEntry(app, accessible_name="CTK Entry", placeholder_text="CTK Entry")
        ctk_entry.pack(pady=2)
    
    # Add debug callback to track focus changes
    def debug_focus_change(widget):
        print(f"Focus changed to: {widget.__class__.__name__} - {getattr(widget, 'accessible_name', 'unnamed')}")
    
    # Add callbacks to all registered widgets
    for widget in focus_manager._focus_order:
        focus_manager.add_focus_callback(widget, lambda w=widget: debug_focus_change(w))
    
    # Instructions
    AccessibleLabel(
        app, 
        text="Instructions:\n• Press Tab to navigate forward\n• Press Shift+Tab to navigate backward\n• Watch console for focus change messages\n• Look for yellow focus indicators",
        justify="left"
    ).pack(pady=20)
    
    print("Focus Navigation Test Started")
    print(f"Registered widgets: {len(focus_manager._focus_order)}")
    for i, widget in enumerate(focus_manager._focus_order):
        print(f"  {i+1}. {widget.__class__.__name__} - {getattr(widget, 'accessible_name', 'unnamed')}")
    print("\nPress Tab to navigate between widgets...")
    
    # Set initial focus
    if focus_manager._focus_order:
        focus_manager._focus_order[0].focus_set()
    
    app.mainloop()

if __name__ == "__main__":
    test_focus_navigation()