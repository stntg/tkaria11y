#!/usr/bin/env python3
"""
Simple test to demonstrate the improved high contrast theming.
Shows that themes apply to ALL widgets, including those created after apply().
"""

import sys
from pathlib import Path
import tkinter as tk

# Add the parent directory to the path so we can import tkaria11y
sys.path.insert(0, str(Path(__file__).parent.parent))

from tkaria11y.themes import HighContrastTheme


class SimpleThemeTest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Theme Test")
        self.root.geometry("500x400")

        self.theme_applied = False
        self.widget_counter = 0

        self.setup_ui()

    def setup_ui(self):
        """Set up the UI"""

        # Control panel
        control_frame = tk.Frame(self.root, relief="raised", bd=2)
        control_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(
            control_frame, text="Theme Test Controls:", font=("Arial", 12, "bold")
        ).pack(side="left", padx=5)

        self.theme_btn = tk.Button(
            control_frame,
            text="Apply High Contrast",
            command=self.toggle_theme,
            bg="lightblue",
            font=("Arial", 10, "bold"),
        )
        self.theme_btn.pack(side="left", padx=5)

        self.add_btn = tk.Button(
            control_frame,
            text="Add New Widgets",
            command=self.add_widgets,
            bg="lightgreen",
            font=("Arial", 10, "bold"),
        )
        self.add_btn.pack(side="left", padx=5)

        # Initial widgets section
        initial_frame = tk.LabelFrame(
            self.root, text="Initial Widgets (Created Before Theme)", padx=10, pady=10
        )
        initial_frame.pack(fill="x", padx=10, pady=5)

        # Various initial widgets
        tk.Label(initial_frame, text="Name:").pack(anchor="w")
        self.name_entry = tk.Entry(initial_frame, width=30)
        self.name_entry.pack(anchor="w", pady=2)

        tk.Label(initial_frame, text="Comments:").pack(anchor="w", pady=(10, 0))
        self.text_widget = tk.Text(initial_frame, height=3, width=40)
        self.text_widget.pack(anchor="w", pady=2)
        self.text_widget.insert("1.0", "This text widget should be themed too!")

        # Buttons
        btn_frame = tk.Frame(initial_frame)
        btn_frame.pack(anchor="w", pady=5)

        tk.Button(btn_frame, text="Red Button", bg="red", fg="white").pack(
            side="left", padx=2
        )
        tk.Button(btn_frame, text="Green Button", bg="green", fg="white").pack(
            side="left", padx=2
        )
        tk.Button(btn_frame, text="Blue Button", bg="blue", fg="white").pack(
            side="left", padx=2
        )

        # Selection widgets
        selection_frame = tk.Frame(initial_frame)
        selection_frame.pack(anchor="w", pady=5)

        self.check_var = tk.BooleanVar()
        tk.Checkbutton(selection_frame, text="Check me", variable=self.check_var).pack(
            side="left", padx=5
        )

        self.radio_var = tk.StringVar(value="option1")
        tk.Radiobutton(
            selection_frame, text="Option 1", variable=self.radio_var, value="option1"
        ).pack(side="left", padx=5)
        tk.Radiobutton(
            selection_frame, text="Option 2", variable=self.radio_var, value="option2"
        ).pack(side="left", padx=5)

        # Scale and Listbox
        misc_frame = tk.Frame(initial_frame)
        misc_frame.pack(anchor="w", pady=5)

        tk.Label(misc_frame, text="Scale:").pack(anchor="w")
        self.scale = tk.Scale(misc_frame, from_=0, to=100, orient="horizontal")
        self.scale.pack(anchor="w", fill="x", pady=2)

        tk.Label(misc_frame, text="Listbox:").pack(anchor="w", pady=(10, 0))
        self.listbox = tk.Listbox(misc_frame, height=3)
        for i in range(5):
            self.listbox.insert(tk.END, f"Item {i+1}")
        self.listbox.pack(anchor="w", pady=2)

        # Dynamic widgets section
        self.dynamic_frame = tk.LabelFrame(
            self.root, text="Dynamic Widgets (Created After Theme)", padx=10, pady=10
        )
        self.dynamic_frame.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(
            self.dynamic_frame, text="Click 'Add New Widgets' to test dynamic theming"
        ).pack()

    def toggle_theme(self):
        """Toggle the high contrast theme"""
        if not self.theme_applied:
            print("🎨 Applying High Contrast Theme...")
            HighContrastTheme.apply(self.root)
            self.theme_btn.config(text="Remove High Contrast")
            self.theme_applied = True
            print(
                "✅ Theme applied! All existing widgets should now have high contrast colors."
            )
            print(
                "💡 Now try adding new widgets - they should be themed automatically!"
            )
        else:
            print("🔄 Removing High Contrast Theme...")
            HighContrastTheme.remove(self.root)
            self.theme_btn.config(text="Apply High Contrast")
            self.theme_applied = False
            print("✅ Theme removed! Widgets should return to normal colors.")

    def add_widgets(self):
        """Add new widgets to test dynamic theming"""
        self.widget_counter += 1

        print(f"➕ Adding new widget set #{self.widget_counter}...")

        # Clear previous dynamic widgets (except the instruction label)
        for widget in self.dynamic_frame.winfo_children():
            if isinstance(
                widget, tk.Label
            ) and "Click 'Add New Widgets'" in widget.cget("text"):
                continue
            widget.destroy()

        # Create new frame for this set
        new_frame = tk.Frame(self.dynamic_frame, relief="groove", bd=2)
        new_frame.pack(fill="x", pady=5)

        tk.Label(
            new_frame,
            text=f"Dynamic Widget Set #{self.widget_counter}",
            font=("Arial", 11, "bold"),
        ).pack(pady=5)

        # Add various new widgets
        tk.Label(new_frame, text=f"Dynamic Label #{self.widget_counter}").pack(
            anchor="w", padx=10
        )

        new_entry = tk.Entry(new_frame, width=25)
        new_entry.pack(anchor="w", padx=10, pady=2)
        new_entry.insert(0, f"Dynamic entry #{self.widget_counter}")

        # New buttons with different colors
        btn_frame = tk.Frame(new_frame)
        btn_frame.pack(anchor="w", padx=10, pady=5)

        colors = [
            ("Purple", "purple", "white"),
            ("Orange", "orange", "black"),
            ("Teal", "teal", "white"),
        ]
        for text, bg, fg in colors:
            tk.Button(
                btn_frame, text=f"{text} #{self.widget_counter}", bg=bg, fg=fg
            ).pack(side="left", padx=2)

        # New selection widgets
        selection_frame = tk.Frame(new_frame)
        selection_frame.pack(anchor="w", padx=10, pady=2)

        new_check_var = tk.BooleanVar()
        tk.Checkbutton(
            selection_frame,
            text=f"New Check #{self.widget_counter}",
            variable=new_check_var,
        ).pack(side="left", padx=5)

        new_radio_var = tk.StringVar(value="new1")
        tk.Radiobutton(
            selection_frame,
            text=f"New Radio A #{self.widget_counter}",
            variable=new_radio_var,
            value="new1",
        ).pack(side="left", padx=5)
        tk.Radiobutton(
            selection_frame,
            text=f"New Radio B #{self.widget_counter}",
            variable=new_radio_var,
            value="new2",
        ).pack(side="left", padx=5)

        # New scale
        tk.Label(new_frame, text=f"New Scale #{self.widget_counter}:").pack(
            anchor="w", padx=10, pady=(10, 0)
        )
        new_scale = tk.Scale(new_frame, from_=0, to=50, orient="horizontal")
        new_scale.pack(anchor="w", fill="x", padx=10, pady=2)

        # New text widget
        tk.Label(new_frame, text=f"New Text Widget #{self.widget_counter}:").pack(
            anchor="w", padx=10, pady=(10, 0)
        )
        new_text = tk.Text(new_frame, height=2, width=30)
        new_text.pack(anchor="w", padx=10, pady=2)
        new_text.insert("1.0", f"This is dynamic text widget #{self.widget_counter}")

        if self.theme_applied:
            print(
                "✅ New widgets added! They should automatically have high contrast colors."
            )
            print("🔍 Notice how they match the theme without any additional code!")
        else:
            print("✅ New widgets added with normal colors.")
            print("💡 Apply the theme to see them change instantly!")

    def run(self):
        """Run the test"""
        print("🚀 Simple High Contrast Theme Test")
        print("=" * 40)
        print()
        print("This test demonstrates that the improved high contrast theme:")
        print("✅ Applies to ALL existing widgets when enabled")
        print("✅ Automatically themes NEW widgets created after apply()")
        print("✅ Uses Tkinter's option database for persistent theming")
        print("✅ Can be toggled on/off dynamically")
        print("✅ Works with all standard tkinter widget types")
        print()
        print("Instructions:")
        print("1. Click 'Apply High Contrast' - watch ALL widgets change color")
        print("2. Click 'Add New Widgets' - see new widgets get themed automatically")
        print("3. Click 'Remove High Contrast' - everything returns to normal")
        print("4. Try adding widgets before and after applying the theme")
        print()

        self.root.mainloop()


if __name__ == "__main__":
    test = SimpleThemeTest()
    test.run()
