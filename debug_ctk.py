#!/usr/bin/env python3
"""
Debug CustomTkinter widget visibility issues
"""

import tkinter as tk
import customtkinter as ctk
from tkaria11y.app import AccessibleApp
from tkaria11y.widgets import AccessibleFrame, AccessibleLabel, AccessibleNotebook

def test_ctk_widgets():
    """Test CustomTkinter widgets in different configurations"""
    
    app = AccessibleApp(title="CTK Debug Test", high_contrast=True)
    
    # Create notebook
    notebook = AccessibleNotebook(app, accessible_name="Test Notebook")
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Test 1: CTK widgets in regular Tkinter frame
    frame1 = AccessibleFrame(notebook)
    notebook.add(frame1, text="CTK in Tkinter Frame")
    
    AccessibleLabel(frame1, text="CTK widgets in Tkinter Frame:", font=("Arial", 12, "bold")).pack(pady=5)
    
    container1 = AccessibleFrame(frame1)
    container1.pack(fill="both", expand=True, padx=20, pady=20)
    
    ctk_frame1 = ctk.CTkFrame(container1)
    ctk_frame1.pack(fill="both", expand=True)
    
    ctk.CTkLabel(ctk_frame1, text="CTK Label Test 1").pack(pady=10)
    ctk.CTkButton(ctk_frame1, text="CTK Button Test 1").pack(pady=10)
    ctk.CTkEntry(ctk_frame1, placeholder_text="CTK Entry Test 1").pack(pady=10)
    
    # Test 2: Direct CTK widgets
    frame2 = AccessibleFrame(notebook)
    notebook.add(frame2, text="Direct CTK")
    
    AccessibleLabel(frame2, text="Direct CTK widgets:", font=("Arial", 12, "bold")).pack(pady=5)
    
    # Try direct CTK widgets
    try:
        ctk_direct = ctk.CTkFrame(frame2)
        ctk_direct.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(ctk_direct, text="Direct CTK Label").pack(pady=10)
        ctk.CTkButton(ctk_direct, text="Direct CTK Button").pack(pady=10)
    except Exception as e:
        AccessibleLabel(frame2, text=f"Error with direct CTK: {e}").pack(pady=10)
    
    # Test 3: Regular Tkinter widgets for comparison
    frame3 = AccessibleFrame(notebook)
    notebook.add(frame3, text="Regular Tkinter")
    
    AccessibleLabel(frame3, text="Regular Tkinter widgets:", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(frame3, text="Regular Tkinter Label").pack(pady=10)
    tk.Button(frame3, text="Regular Tkinter Button").pack(pady=10)
    tk.Entry(frame3).pack(pady=10)
    
    print("Debug test created. Check if CTK widgets are visible.")
    app.mainloop()

if __name__ == "__main__":
    test_ctk_widgets()