#!/usr/bin/env python3
"""
Inspect CustomTkinter widget structure
"""

import tkinter as tk
from tkaria11y.app import AccessibleApp
from tkaria11y.widgets import AccessibleCTKButton, CTK_AVAILABLE

def inspect_ctk_widget():
    """Inspect the internal structure of CTK widgets"""
    
    if not CTK_AVAILABLE:
        print("CustomTkinter not available")
        return
    
    app = AccessibleApp(title="CTK Widget Inspector")
    
    # Create CTK button
    ctk_button = AccessibleCTKButton(app, text="CTK Button", accessible_name="CTK Button")
    ctk_button.pack(pady=20)
    
    # Show the window to ensure widgets are created
    app.update()
    
    print("CTK Button attributes:")
    for attr in dir(ctk_button):
        if not attr.startswith('__'):
            try:
                value = getattr(ctk_button, attr)
                if hasattr(value, 'winfo_class'):
                    print(f"  {attr}: {value} (Tkinter widget: {value.winfo_class()})")
                elif not callable(value):
                    print(f"  {attr}: {value}")
            except:
                pass
    
    print("\nTrying different focus methods:")
    
    # Try various focus methods
    methods_to_try = [
        ('focus_set', lambda: ctk_button.focus_set()),
        ('focus_force', lambda: ctk_button.focus_force()),
    ]
    
    # Check for internal widgets
    internal_widgets = []
    for attr in ['_canvas', '_entry', '_text_label', '_bg_canvas', '_button_canvas']:
        if hasattr(ctk_button, attr):
            widget = getattr(ctk_button, attr)
            if hasattr(widget, 'focus_set'):
                internal_widgets.append((attr, widget))
                methods_to_try.append((f'{attr}.focus_set', lambda w=widget: w.focus_set()))
                methods_to_try.append((f'{attr}.focus_force', lambda w=widget: w.focus_force()))
    
    print(f"Found internal widgets: {[name for name, _ in internal_widgets]}")
    
    for method_name, method in methods_to_try:
        try:
            print(f"\nTrying {method_name}...")
            method()
            
            # Check what has focus
            current_focus = app.focus_get()
            print(f"  Current focus after {method_name}: {current_focus}")
            
            if current_focus:
                print(f"  Focus widget class: {current_focus.winfo_class()}")
                print(f"  Is CTK button: {current_focus == ctk_button}")
                
                # Check if it's an internal widget
                for internal_name, internal_widget in internal_widgets:
                    if current_focus == internal_widget:
                        print(f"  Focus is on internal widget: {internal_name}")
                        break
            
        except Exception as e:
            print(f"  Error with {method_name}: {e}")
    
    app.destroy()

if __name__ == "__main__":
    inspect_ctk_widget()