#!/usr/bin/env python3
"""
Test the enhanced CustomTkinter wrappers
"""

import tkinter as tk
from tkaria11y.app import AccessibleApp
from tkaria11y.widgets import (
    AccessibleButton, AccessibleEntry,
    AccessibleCTKButton, AccessibleCTKEntry,
    CTK_AVAILABLE
)
from tkaria11y.focus_manager import get_focus_manager

def test_enhanced_ctk():
    """Test the enhanced CTK wrappers"""
    
    if not CTK_AVAILABLE:
        print("CustomTkinter not available")
        return
    
    app = AccessibleApp(title="Enhanced CTK Test", high_contrast=True)
    focus_manager = get_focus_manager(app)
    
    # Create test widgets
    print("Creating widgets...")
    
    # Regular widgets
    regular_button = AccessibleButton(app, text="Regular Button", accessible_name="Regular Button")
    regular_button.pack(pady=5)
    
    regular_entry = AccessibleEntry(app, accessible_name="Regular Entry")
    regular_entry.pack(pady=5)
    
    # Enhanced CTK widgets
    ctk_button = AccessibleCTKButton(
        app, 
        text="Enhanced CTK Button", 
        accessible_name="Enhanced CTK Button",
        accessible_description="This is an enhanced CustomTkinter button with proper focus handling",
        command=lambda: print("Enhanced CTK Button clicked!")
    )
    ctk_button.pack(pady=5)
    
    ctk_entry = AccessibleCTKEntry(
        app,
        accessible_name="Enhanced CTK Entry",
        accessible_description="This is an enhanced CustomTkinter entry field",
        placeholder_text="Type here..."
    )
    ctk_entry.pack(pady=5)
    
    # Add debug callbacks
    def debug_focus_change(widget):
        widget_name = getattr(widget, 'accessible_name', widget.__class__.__name__)
        print(f"Focus changed to: {widget_name}")
    
    # Add callbacks to all widgets
    for widget in [regular_button, regular_entry, ctk_button, ctk_entry]:
        if hasattr(widget, 'add_focus_callback'):
            widget.add_focus_callback(debug_focus_change)
        else:
            focus_manager.add_focus_callback(widget, lambda w=widget: debug_focus_change(w))
    
    print(f"Registered widgets: {len(focus_manager._focus_order)}")
    for i, widget in enumerate(focus_manager._focus_order):
        widget_name = getattr(widget, 'accessible_name', widget.__class__.__name__)
        print(f"  {i+1}. {widget.__class__.__name__} - {widget_name}")
    
    # Instructions
    instructions = tk.Label(
        app,
        text="Instructions:\n• Tab through widgets\n• Press Space/Enter on buttons\n• Check console for focus messages\n• Look for focus indicators",
        justify="left",
        bg=app.cget('bg')
    )
    instructions.pack(pady=20)
    
    print("\nEnhanced CTK Test Started!")
    print("Tab through widgets to test focus management.")
    print("Enhanced CTK widgets should have proper focus handling and announcements.")
    
    # Set initial focus
    if focus_manager._focus_order:
        focus_manager._focus_order[0].focus_set()
    
    app.mainloop()

if __name__ == "__main__":
    test_enhanced_ctk()