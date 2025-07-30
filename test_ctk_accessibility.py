#!/usr/bin/env python3
"""
Test the new CustomTkinter accessibility system
"""

import tkinter as tk
from tkaria11y.app import AccessibleApp

try:
    from tkaria11y.widgets import (
        AccessibleCTKFrame,
        AccessibleCTKButton,
        AccessibleCTKEntry,
        AccessibleCTKLabel,
        AccessibleCTKCheckBox,
        AccessibleCTKSlider,
        CTK_AVAILABLE
    )
    from tkaria11y.ctk_focus_manager import get_ctk_focus_manager
except ImportError as e:
    print(f"Import error: {e}")
    CTK_AVAILABLE = False

def test_ctk_accessibility():
    """Test CustomTkinter accessibility features"""
    
    if not CTK_AVAILABLE:
        print("CustomTkinter not available or accessibility system not working")
        return
    
    app = AccessibleApp(title="CTK Accessibility Test", high_contrast=True)
    
    # Create main frame
    main_frame = AccessibleCTKFrame(
        app,
        accessible_name="Main Container",
        accessible_description="Container for CustomTkinter accessibility test"
    )
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    title = AccessibleCTKLabel(
        main_frame,
        text="CustomTkinter Accessibility Test",
        accessible_name="Test Title",
        font=("Arial", 16, "bold")
    )
    title.pack(pady=10)
    
    # Button
    button = AccessibleCTKButton(
        main_frame,
        text="Test Button",
        accessible_name="Accessibility Test Button",
        accessible_description="Click to test button accessibility",
        command=lambda: print("Button clicked!")
    )
    button.pack(pady=10)
    
    # Entry
    entry = AccessibleCTKEntry(
        main_frame,
        placeholder_text="Type here...",
        accessible_name="Test Entry Field",
        accessible_description="Text input field for testing"
    )
    entry.pack(pady=10)
    
    # Checkbox
    checkbox = AccessibleCTKCheckBox(
        main_frame,
        text="Test Checkbox",
        accessible_name="Accessibility Test Checkbox",
        accessible_description="Checkbox for testing state changes"
    )
    checkbox.pack(pady=10)
    
    # Slider
    slider = AccessibleCTKSlider(
        main_frame,
        from_=0,
        to=100,
        accessible_name="Test Slider",
        accessible_description="Slider for testing value changes"
    )
    slider.pack(pady=10)
    
    # Instructions
    instructions = AccessibleCTKLabel(
        main_frame,
        text="Instructions:\n• Tab through widgets to test focus\n• Use widgets to test announcements\n• Check for focus indicators",
        accessible_name="Test Instructions",
        justify="left"
    )
    instructions.pack(pady=20)
    
    # Get CTK focus manager for this window
    ctk_focus_manager = get_ctk_focus_manager(app)
    
    print("CustomTkinter accessibility test created!")
    print("Expected features:")
    print("- Focus indicators on CTK widgets")
    print("- Screen reader announcements")
    print("- Keyboard navigation")
    print("- State change notifications")
    
    app.mainloop()

if __name__ == "__main__":
    test_ctk_accessibility()