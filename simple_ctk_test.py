#!/usr/bin/env python3
"""
Simple CustomTkinter test without TTS
"""

import tkinter as tk
import customtkinter as ctk
from tkaria11y.app import AccessibleApp
from tkaria11y.widgets import AccessibleFrame, AccessibleLabel, AccessibleNotebook

def simple_test():
    """Simple test without TTS"""
    
    app = AccessibleApp(title="Simple CTK Test", high_contrast=True)
    
    # Create notebook
    notebook = AccessibleNotebook(app, accessible_name="Test Notebook")
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Tab 1: Regular widgets
    frame1 = AccessibleFrame(notebook)
    notebook.add(frame1, text="Regular Widgets")
    
    AccessibleLabel(frame1, text="Regular Tkinter widgets work fine:", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(frame1, text="Regular Button", command=lambda: print("Regular button clicked")).pack(pady=5)
    tk.Entry(frame1).pack(pady=5)
    tk.Label(frame1, text="Regular Label").pack(pady=5)
    
    # Tab 2: CustomTkinter widgets
    frame2 = AccessibleFrame(notebook)
    notebook.add(frame2, text="CustomTkinter Widgets")
    
    AccessibleLabel(frame2, text="CustomTkinter widgets:", font=("Arial", 12, "bold")).pack(pady=10)
    
    # Container for CTK widgets
    container = AccessibleFrame(frame2)
    container.pack(fill="both", expand=True, padx=20, pady=20)
    
    # CTK Frame
    ctk_frame = ctk.CTkFrame(container)
    ctk_frame.pack(fill="both", expand=True)
    
    # CTK widgets
    ctk.CTkLabel(ctk_frame, text="CustomTkinter Label").pack(pady=10)
    ctk.CTkButton(ctk_frame, text="CustomTkinter Button", command=lambda: print("CTK button clicked")).pack(pady=10)
    ctk.CTkEntry(ctk_frame, placeholder_text="CustomTkinter Entry").pack(pady=10)
    
    print("Simple test created. Check widget visibility.")
    print("If CTK widgets are not visible, there's a compatibility issue.")
    
    app.mainloop()

if __name__ == "__main__":
    simple_test()