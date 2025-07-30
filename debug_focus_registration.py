#!/usr/bin/env python3
"""
Debug script to check which widgets are being registered for focus management
"""

import tkinter as tk
from tkaria11y.app import AccessibleApp
from tkaria11y.widgets import (
    AccessibleButton, AccessibleEntry, AccessibleLabel, AccessibleFrame,
    AccessibleCTKButton, AccessibleCTKEntry, AccessibleCTKLabel, AccessibleCTKFrame,
    CTK_AVAILABLE
)
from tkaria11y.focus_manager import get_focus_manager

def debug_focus_registration():
    """Debug which widgets get registered for focus management"""
    
    app = AccessibleApp(title="Focus Registration Debug")
    
    # Get focus manager
    focus_manager = get_focus_manager(app)
    
    print("Creating widgets and checking focus registration...")
    print("=" * 50)
    
    # Create various widgets
    widgets = []
    
    # Frame (should NOT be focusable)
    frame = AccessibleFrame(app, accessible_name="Test Frame")
    frame.pack(pady=5)
    widgets.append(("Frame", frame))
    
    # Label (should NOT be focusable)
    label = AccessibleLabel(frame, text="Test Label", accessible_name="Test Label")
    label.pack(pady=2)
    widgets.append(("Label", label))
    
    # Button (should be focusable)
    button = AccessibleButton(frame, text="Test Button", accessible_name="Test Button")
    button.pack(pady=2)
    widgets.append(("Button", button))
    
    # Entry (should be focusable)
    entry = AccessibleEntry(frame, accessible_name="Test Entry")
    entry.pack(pady=2)
    widgets.append(("Entry", entry))
    
    if CTK_AVAILABLE:
        # CTK Frame (should NOT be focusable)
        ctk_frame = AccessibleCTKFrame(frame, accessible_name="CTK Frame")
        ctk_frame.pack(pady=5)
        widgets.append(("CTK Frame", ctk_frame))
        
        # CTK Label (should NOT be focusable)
        ctk_label = AccessibleCTKLabel(ctk_frame, text="CTK Label", accessible_name="CTK Label")
        ctk_label.pack(pady=2)
        widgets.append(("CTK Label", ctk_label))
        
        # CTK Button (should be focusable)
        ctk_button = AccessibleCTKButton(ctk_frame, text="CTK Button", accessible_name="CTK Button")
        ctk_button.pack(pady=2)
        widgets.append(("CTK Button", ctk_button))
        
        # CTK Entry (should be focusable)
        ctk_entry = AccessibleCTKEntry(ctk_frame, accessible_name="CTK Entry")
        ctk_entry.pack(pady=2)
        widgets.append(("CTK Entry", ctk_entry))
    
    # Check which widgets are registered
    print("Widget Registration Status:")
    print("-" * 30)
    
    for widget_name, widget in widgets:
        is_focusable = focus_manager._is_focusable_widget(widget)
        is_registered = widget in focus_manager._focus_order
        
        status = "✓" if is_registered else "✗"
        focusable_status = "focusable" if is_focusable else "non-focusable"
        
        print(f"{status} {widget_name:<12} - {focusable_status}")
    
    print("\nRegistered widgets in focus order:")
    for i, widget in enumerate(focus_manager._focus_order):
        widget_class = widget.__class__.__name__
        widget_name = getattr(widget, 'accessible_name', 'unnamed')
        print(f"  {i+1}. {widget_class} - {widget_name}")
    
    print(f"\nTotal registered widgets: {len(focus_manager._focus_order)}")
    print("\nExpected: Only interactive widgets (Button, Entry, CTK Button, CTK Entry) should be registered")
    
    # Don't start mainloop for debugging
    app.destroy()

if __name__ == "__main__":
    debug_focus_registration()