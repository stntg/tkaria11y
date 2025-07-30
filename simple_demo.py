#!/usr/bin/env python3
"""
Simple Demo Application for tkaria11y
=====================================

A simplified version focusing on the most commonly used widgets.

Usage:
    python simple_demo.py
"""

import tkinter as tk
from tkaria11y.app import AccessibleApp
from tkaria11y.widgets import (
    AccessibleButton,
    AccessibleEntry,
    AccessibleLabel,
    AccessibleText,
    AccessibleCheckbutton,
    AccessibleRadiobutton,
    AccessibleListbox,
    AccessibleTTKButton,
    AccessibleTTKEntry,
    AccessibleCombobox,
    AccessibleNotebook,
    AccessibleTTKFrame,
)

try:
    import customtkinter as ctk
    from tkaria11y.widgets import (
        AccessibleCTKButton,
        AccessibleCTKEntry,
        AccessibleCTKLabel,
    )

    CTK_AVAILABLE = True
    ctk.set_appearance_mode("system")
except ImportError:
    CTK_AVAILABLE = False


class SimpleDemoApp(AccessibleApp):
    """Simple demo application showcasing essential tkaria11y widgets."""

    def __init__(self):
        super().__init__(title="tkaria11y Simple Demo", high_contrast=True)

        # Set window geometry
        self.geometry("800x600")

        self.create_interface()

    def create_interface(self):
        """Create the main interface."""
        # Create notebook for different widget types
        self.notebook = AccessibleNotebook(self, accessible_name="Widget Demo Tabs")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        self.create_basic_tab()
        self.create_input_tab()
        if CTK_AVAILABLE:
            self.create_ctk_tab()

    def create_basic_tab(self):
        """Create basic widgets tab."""
        basic_frame = AccessibleTTKFrame(self.notebook)
        self.notebook.add(basic_frame, text="Basic Widgets")

        # Title
        AccessibleLabel(
            basic_frame,
            text="Basic Tkinter Widgets Demo",
            font=("Arial", 16, "bold"),
            accessible_name="Basic Widgets Demo Title",
        ).pack(pady=10)

        # Buttons
        button_frame = AccessibleTTKFrame(basic_frame)
        button_frame.pack(pady=10)

        AccessibleButton(
            button_frame,
            text="Say Hello",
            accessible_name="Say Hello Button",
            command=lambda: self.speak("Hello from tkaria11y!"),
        ).pack(side="left", padx=5)

        AccessibleTTKButton(
            button_frame,
            text="TTK Button",
            accessible_name="TTK Style Button",
            command=lambda: self.speak("TTK Button clicked!"),
        ).pack(side="left", padx=5)

        # Selection widgets
        selection_frame = AccessibleTTKFrame(basic_frame)
        selection_frame.pack(pady=10, fill="x", padx=20)

        # Checkbuttons
        AccessibleLabel(
            selection_frame, text="Options:", accessible_name="Checkbox Options Label"
        ).pack(anchor="w")

        self.check_vars = []
        for i, option in enumerate(["Enable notifications", "Auto-save", "Dark mode"]):
            var = tk.BooleanVar()
            self.check_vars.append(var)
            AccessibleCheckbutton(
                selection_frame,
                text=option,
                variable=var,
                accessible_name=f"Checkbox for {option}",
                command=lambda opt=option: self.speak(f"{opt} toggled"),
            ).pack(anchor="w")

        # Radio buttons
        AccessibleLabel(
            selection_frame,
            text="Choose theme:",
            accessible_name="Theme Selection Label",
        ).pack(anchor="w", pady=(10, 0))

        self.theme_var = tk.StringVar(value="Default")
        for theme in ["Default", "High Contrast", "Dark"]:
            AccessibleRadiobutton(
                selection_frame,
                text=theme,
                variable=self.theme_var,
                value=theme,
                accessible_name=f"Theme option {theme}",
                command=lambda: self.speak(f"Selected {self.theme_var.get()} theme"),
            ).pack(anchor="w")

        # List selection
        AccessibleLabel(
            selection_frame,
            text="Select items:",
            accessible_name="List Selection Label",
        ).pack(anchor="w", pady=(10, 0))

        self.listbox = AccessibleListbox(
            selection_frame, height=4, accessible_name="Demo Items List"
        )
        self.listbox.pack(fill="x", pady=5)

        # Populate listbox
        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        for item in items:
            self.listbox.insert("end", item)

        self.listbox.bind("<<ListboxSelect>>", self.on_list_select)

    def create_input_tab(self):
        """Create input widgets tab."""
        input_frame = AccessibleTTKFrame(self.notebook)
        self.notebook.add(input_frame, text="Input Widgets")

        # Title
        AccessibleLabel(
            input_frame,
            text="Input Widgets Demo",
            font=("Arial", 16, "bold"),
            accessible_name="Input Widgets Demo Title",
        ).pack(pady=10)

        # Form-like layout
        form_frame = AccessibleTTKFrame(input_frame)
        form_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Name entry
        AccessibleLabel(
            form_frame, text="Name:", accessible_name="Name Input Label"
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.name_entry = AccessibleEntry(
            form_frame, accessible_name="Name Input Field"
        )
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)

        # Email entry (TTK style)
        AccessibleLabel(
            form_frame, text="Email:", accessible_name="Email Input Label"
        ).grid(row=1, column=0, sticky="w", pady=5)

        self.email_entry = AccessibleTTKEntry(
            form_frame, accessible_name="Email Input Field"
        )
        self.email_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)

        # Category selection
        AccessibleLabel(
            form_frame, text="Category:", accessible_name="Category Selection Label"
        ).grid(row=2, column=0, sticky="w", pady=5)

        self.category_combo = AccessibleCombobox(
            form_frame,
            values=["Personal", "Work", "Education", "Other"],
            accessible_name="Category Selection Dropdown",
        )
        self.category_combo.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=5)
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_select)

        # Comments text area
        AccessibleLabel(
            form_frame, text="Comments:", accessible_name="Comments Input Label"
        ).grid(row=3, column=0, sticky="nw", pady=5)

        self.comments_text = AccessibleText(
            form_frame, height=6, width=40, accessible_name="Comments Text Area"
        )
        self.comments_text.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=5)

        # Buttons
        button_frame = AccessibleTTKFrame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        AccessibleButton(
            button_frame,
            text="Submit",
            accessible_name="Submit Form Button",
            command=self.submit_form,
        ).pack(side="left", padx=5)

        AccessibleButton(
            button_frame,
            text="Clear",
            accessible_name="Clear Form Button",
            command=self.clear_form,
        ).pack(side="left", padx=5)

        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)

    def create_ctk_tab(self):
        """Create CustomTkinter widgets tab."""
        if not CTK_AVAILABLE:
            return

        ctk_frame = AccessibleTTKFrame(self.notebook)
        self.notebook.add(ctk_frame, text="CustomTkinter")

        # Title
        AccessibleCTKLabel(
            ctk_frame,
            text="CustomTkinter Widgets Demo",
            font=("Arial", 16, "bold"),
            accessible_name="CustomTkinter Demo Title",
        ).pack(pady=20)

        # CTK Buttons
        button_frame = tk.Frame(ctk_frame)  # Use regular frame for CTK widgets
        button_frame.pack(pady=10)

        AccessibleCTKButton(
            button_frame,
            text="CTK Button",
            accessible_name="CustomTkinter Button Example",
            command=lambda: self.speak("CustomTkinter button clicked!"),
        ).pack(side="left", padx=10)

        AccessibleCTKButton(
            button_frame,
            text="Disabled CTK",
            accessible_name="Disabled CustomTkinter Button",
            state="disabled",
        ).pack(side="left", padx=10)

        # CTK Input
        input_frame = tk.Frame(ctk_frame)
        input_frame.pack(pady=20, padx=40, fill="x")

        AccessibleCTKLabel(
            input_frame, text="CTK Entry:", accessible_name="CustomTkinter Entry Label"
        ).pack(anchor="w", pady=5)

        self.ctk_entry = AccessibleCTKEntry(
            input_frame,
            placeholder_text="Enter text here...",
            accessible_name="CustomTkinter Entry Field",
        )
        self.ctk_entry.pack(fill="x", pady=5)

        AccessibleCTKButton(
            input_frame,
            text="Get CTK Text",
            accessible_name="Get CustomTkinter Text Button",
            command=self.get_ctk_text,
        ).pack(pady=10)

    def on_list_select(self, event):
        """Handle list selection."""
        selection = event.widget.curselection()
        if selection:
            item = event.widget.get(selection[0])
            self.speak(f"Selected {item}")

    def on_category_select(self, event):
        """Handle category selection."""
        category = event.widget.get()
        self.speak(f"Selected category: {category}")

    def submit_form(self):
        """Handle form submission."""
        name = self.name_entry.get()
        email = self.email_entry.get()
        category = self.category_combo.get()
        comments = self.comments_text.get("1.0", "end-1c")

        if not name:
            self.speak("Please enter a name")
            self.name_entry.focus()
            return

        message = f"Form submitted for {name}"
        if email:
            message += f" with email {email}"
        if category:
            message += f" in category {category}"

        self.speak(message)

    def clear_form(self):
        """Clear the form."""
        self.name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.category_combo.set("")
        self.comments_text.delete("1.0", "end")
        self.speak("Form cleared")
        self.name_entry.focus()

    def get_ctk_text(self):
        """Get text from CTK entry."""
        if CTK_AVAILABLE:
            text = self.ctk_entry.get()
            if text:
                self.speak(f"CTK entry contains: {text}")
            else:
                self.speak("CTK entry is empty")


def main():
    """Main application entry point."""
    try:
        app = SimpleDemoApp()
        app.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
