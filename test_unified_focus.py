#!/usr/bin/env python3
"""
Test unified focus management for both regular and CustomTkinter widgets
"""

import tkinter as tk
from tkaria11y.app import AccessibleApp
from tkaria11y.widgets import (
    AccessibleButton, AccessibleEntry, AccessibleLabel,
    AccessibleTTKButton, AccessibleTTKEntry, AccessibleTTKLabel,
    AccessibleCTKButton, AccessibleCTKEntry, AccessibleCTKLabel,
    AccessibleFrame, AccessibleTTKFrame, AccessibleCTKFrame,
    CTK_AVAILABLE
)

def test_unified_focus():
    """Test that focus indicators work for all widget types"""
    
    app = AccessibleApp(title="Unified Focus Test", high_contrast=True)
    
    # Create main container
    main_frame = AccessibleFrame(app)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    AccessibleLabel(
        main_frame,
        text="Unified Focus Management Test",
        font=("Arial", 16, "bold"),
        accessible_name="Test Title"
    ).pack(pady=10)
    
    # Instructions
    AccessibleLabel(
        main_frame,
        text="Tab through all widgets below. Each should show a focus indicator.",
        accessible_name="Instructions"
    ).pack(pady=5)
    
    # Regular Tkinter widgets
    tk_frame = AccessibleFrame(main_frame)
    tk_frame.pack(fill="x", pady=10)
    
    AccessibleLabel(tk_frame, text="Regular Tkinter Widgets:", font=("Arial", 12, "bold")).pack()
    AccessibleButton(tk_frame, text="Tkinter Button", accessible_name="Regular Button").pack(pady=2)
    AccessibleEntry(tk_frame, accessible_name="Regular Entry").pack(pady=2)
    
    # TTK widgets
    ttk_frame = AccessibleTTKFrame(main_frame)
    ttk_frame.pack(fill="x", pady=10)
    
    AccessibleTTKLabel(ttk_frame, text="TTK Widgets:", font=("Arial", 12, "bold")).pack()
    AccessibleTTKButton(ttk_frame, text="TTK Button", accessible_name="TTK Button").pack(pady=2)
    AccessibleTTKEntry(ttk_frame, accessible_name="TTK Entry").pack(pady=2)
    
    # CustomTkinter widgets (if available)
    if CTK_AVAILABLE:
        ctk_frame = AccessibleCTKFrame(main_frame, accessible_name="CTK Container")
        ctk_frame.pack(fill="x", pady=10)
        
        AccessibleCTKLabel(ctk_frame, text="CustomTkinter Widgets:", font=("Arial", 12, "bold")).pack()
        AccessibleCTKButton(ctk_frame, text="CTK Button", accessible_name="CTK Button").pack(pady=2)
        AccessibleCTKEntry(ctk_frame, accessible_name="CTK Entry", placeholder_text="CTK Entry").pack(pady=2)
    else:
        AccessibleLabel(main_frame, text="CustomTkinter not available", font=("Arial", 12, "italic")).pack(pady=10)
    
    # Status
    status_frame = AccessibleFrame(main_frame)
    status_frame.pack(fill="x", pady=20)
    
    AccessibleLabel(
        status_frame,
        text="Expected behavior:\n• All widgets should show focus indicators when tabbed to\n• Focus indicators should be consistent across widget types\n• Screen reader should announce each widget",
        justify="left",
        accessible_name="Expected Behavior"
    ).pack()
    
    print("Unified focus test created!")
    print("Tab through widgets to test focus indicators.")
    print("All widget types should show consistent focus indicators.")
    
    app.mainloop()

if __name__ == "__main__":
    test_unified_focus()