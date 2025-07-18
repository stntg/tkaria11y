#!/usr/bin/env python3
"""
Demonstration of the improved HighContrastTheme.
This shows that the theme applies to ALL widgets, including those created after apply().
"""

import sys
import tkinter as tk
from tkinter import ttk
from pathlib import Path

# Add the parent directory to the path so we can import tkaria11y
sys.path.insert(0, str(Path(__file__).parent.parent))

from tkaria11y.themes import HighContrastTheme
from tkaria11y.widgets import (
    AccessibleButton,
    AccessibleLabel,
    AccessibleEntry,
    AccessibleFrame,
)


class ThemeDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("High Contrast Theme Demo")
        self.root.geometry("600x500")

        self.theme_applied = False
        self.setup_ui()

    def setup_ui(self):
        # Control panel
        control_frame = tk.Frame(self.root, relief="raised", bd=2)
        control_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(
            control_frame, text="Theme Controls:", font=("Arial", 12, "bold")
        ).pack(side="left", padx=5)

        self.theme_btn = tk.Button(
            control_frame,
            text="Apply High Contrast Theme",
            command=self.toggle_theme,
            bg="lightblue",
        )
        self.theme_btn.pack(side="left", padx=5)

        self.add_widgets_btn = tk.Button(
            control_frame,
            text="Add New Widgets",
            command=self.add_new_widgets,
            bg="lightgreen",
        )
        self.add_widgets_btn.pack(side="left", padx=5)

        # Main content area
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Initial widgets
        self.create_initial_widgets()

        # Counter for dynamic widgets
        self.widget_counter = 0

    def create_initial_widgets(self):
        """Create initial set of widgets"""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Theme Demo - Initial Widgets",
            font=("Arial", 14, "bold"),
        )
        title_label.pack(pady=10)

        # Form section
        form_frame = tk.LabelFrame(
            self.main_frame, text="Form Elements", padx=10, pady=10
        )
        form_frame.pack(fill="x", pady=5)

        # Entry with label
        tk.Label(form_frame, text="Name:").pack(anchor="w")
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.pack(anchor="w", pady=2)

        # Text widget
        tk.Label(form_frame, text="Comments:").pack(anchor="w", pady=(10, 0))
        self.text_widget = tk.Text(form_frame, height=3, width=40)
        self.text_widget.pack(anchor="w", pady=2)

        # Buttons section
        button_frame = tk.LabelFrame(self.main_frame, text="Buttons", padx=10, pady=10)
        button_frame.pack(fill="x", pady=5)

        button_row = tk.Frame(button_frame)
        button_row.pack()

        tk.Button(button_row, text="Button 1", bg="red", fg="white").pack(
            side="left", padx=5
        )
        tk.Button(button_row, text="Button 2", bg="green", fg="white").pack(
            side="left", padx=5
        )
        tk.Button(button_row, text="Button 3", bg="blue", fg="white").pack(
            side="left", padx=5
        )

        # Selection widgets
        selection_frame = tk.LabelFrame(
            self.main_frame, text="Selection Widgets", padx=10, pady=10
        )
        selection_frame.pack(fill="x", pady=5)

        # Checkbuttons
        check_frame = tk.Frame(selection_frame)
        check_frame.pack(anchor="w")

        self.check_var1 = tk.BooleanVar()
        self.check_var2 = tk.BooleanVar()

        tk.Checkbutton(check_frame, text="Option 1", variable=self.check_var1).pack(
            side="left", padx=5
        )
        tk.Checkbutton(check_frame, text="Option 2", variable=self.check_var2).pack(
            side="left", padx=5
        )

        # Radio buttons
        radio_frame = tk.Frame(selection_frame)
        radio_frame.pack(anchor="w", pady=5)

        self.radio_var = tk.StringVar(value="option1")
        tk.Radiobutton(
            radio_frame, text="Choice A", variable=self.radio_var, value="option1"
        ).pack(side="left", padx=5)
        tk.Radiobutton(
            radio_frame, text="Choice B", variable=self.radio_var, value="option2"
        ).pack(side="left", padx=5)

        # Scale
        tk.Label(selection_frame, text="Scale:").pack(anchor="w", pady=(10, 0))
        self.scale = tk.Scale(selection_frame, from_=0, to=100, orient="horizontal")
        self.scale.pack(anchor="w", fill="x", pady=2)

        # Listbox
        list_frame = tk.Frame(selection_frame)
        list_frame.pack(anchor="w", pady=5)

        tk.Label(list_frame, text="Listbox:").pack(anchor="w")
        self.listbox = tk.Listbox(list_frame, height=3)
        for i in range(5):
            self.listbox.insert(tk.END, f"Item {i+1}")
        self.listbox.pack(anchor="w")

        # Dynamic widgets area
        self.dynamic_frame = tk.LabelFrame(
            self.main_frame,
            text="Dynamic Widgets (Added After Theme)",
            padx=10,
            pady=10,
        )
        self.dynamic_frame.pack(fill="x", pady=5)

        tk.Label(
            self.dynamic_frame, text="Click 'Add New Widgets' to test dynamic theming"
        ).pack()

    def toggle_theme(self):
        """Toggle high contrast theme on/off"""
        if not self.theme_applied:
            print("🎨 Applying High Contrast Theme...")
            HighContrastTheme.apply(self.root)
            self.theme_btn.config(text="Remove High Contrast Theme")
            self.theme_applied = True
            print("✅ Theme applied! All widgets should now have high contrast colors.")
            print("💡 Try adding new widgets to see if they get themed automatically!")
        else:
            print("🔄 Removing High Contrast Theme...")
            HighContrastTheme.remove(self.root)
            self.theme_btn.config(text="Apply High Contrast Theme")
            self.theme_applied = False
            print("✅ Theme removed! Widgets should return to normal colors.")

    def add_new_widgets(self):
        """Add new widgets to test dynamic theming"""
        self.widget_counter += 1

        # Clear previous dynamic widgets
        for widget in self.dynamic_frame.winfo_children():
            if (
                widget.winfo_class() != "Label"
                or "Click 'Add New Widgets'" not in widget.cget("text")
            ):
                widget.destroy()

        print(f"➕ Adding new widgets (set #{self.widget_counter})...")

        # Add various new widgets
        new_frame = tk.Frame(self.dynamic_frame)
        new_frame.pack(fill="x", pady=5)

        # New label
        tk.Label(new_frame, text=f"New Label #{self.widget_counter}").pack(anchor="w")

        # New entry
        new_entry = tk.Entry(new_frame, width=25)
        new_entry.pack(anchor="w", pady=2)
        new_entry.insert(0, f"New entry #{self.widget_counter}")

        # New buttons
        btn_frame = tk.Frame(new_frame)
        btn_frame.pack(anchor="w", pady=5)

        tk.Button(
            btn_frame, text=f"New Btn {self.widget_counter}A", bg="purple", fg="white"
        ).pack(side="left", padx=2)
        tk.Button(btn_frame, text=f"New Btn {self.widget_counter}B", bg="orange").pack(
            side="left", padx=2
        )

        # New checkbutton
        new_check_var = tk.BooleanVar()
        tk.Checkbutton(
            new_frame, text=f"New Option #{self.widget_counter}", variable=new_check_var
        ).pack(anchor="w", pady=2)

        # New accessible widgets (if theme is applied, these should be themed too)
        if self.theme_applied:
            accessible_frame = AccessibleFrame(
                new_frame, accessible_name="Accessible widgets frame"
            )
            accessible_frame.pack(fill="x", pady=5)

            AccessibleLabel(
                accessible_frame,
                accessible_name=f"Accessible label {self.widget_counter}",
                text=f"Accessible Label #{self.widget_counter}",
            ).pack(anchor="w")

            AccessibleEntry(
                accessible_frame,
                accessible_name=f"Accessible entry {self.widget_counter}",
            ).pack(anchor="w", pady=2)

            AccessibleButton(
                accessible_frame,
                accessible_name=f"Accessible button {self.widget_counter}",
                text=f"Accessible Btn #{self.widget_counter}",
            ).pack(anchor="w", pady=2)

        if self.theme_applied:
            print(
                "✅ New widgets added! They should automatically have high contrast colors."
            )
        else:
            print(
                "✅ New widgets added with normal colors. Apply theme to see them change!"
            )

    def run(self):
        print("🚀 High Contrast Theme Demo")
        print("=" * 40)
        print("This demo shows that the high contrast theme:")
        print("• Applies to ALL existing widgets")
        print("• Automatically themes NEW widgets created after apply()")
        print("• Can be toggled on/off")
        print("• Works with both standard and accessible widgets")
        print()
        print("Instructions:")
        print("1. Click 'Apply High Contrast Theme' to see all widgets change")
        print("2. Click 'Add New Widgets' to test dynamic theming")
        print("3. Click 'Remove High Contrast Theme' to return to normal")
        print()

        self.root.mainloop()


if __name__ == "__main__":
    demo = ThemeDemo()
    demo.run()
