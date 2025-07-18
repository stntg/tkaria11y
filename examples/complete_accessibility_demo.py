#!/usr/bin/env python3
"""
Complete accessibility demonstration showing:
1. Main window theming (your key question!)
2. All widget types themed
3. Dynamic widget creation with automatic theming
4. AccessibleApp integration
5. Real accessibility benefits
"""

import sys
from pathlib import Path
import tkinter as tk

# Add the parent directory to the path so we can import tkaria11y
sys.path.insert(0, str(Path(__file__).parent.parent))

from tkaria11y import AccessibleApp
from tkaria11y.widgets import (
    AccessibleButton,
    AccessibleLabel,
    AccessibleEntry,
    AccessibleFrame,
)
from tkaria11y.themes import HighContrastTheme


class CompleteAccessibilityDemo:
    def __init__(self):
        # Create AccessibleApp - this is the recommended way
        self.app = AccessibleApp(
            title="Complete Accessibility Demo",
            high_contrast=False,  # Start normal, then demonstrate theming
            enable_inspector=False,  # Disable to avoid TTS issues in demo
        )
        self.app.geometry("800x700")

        # Set initial background to make theming difference obvious
        self.app.configure(bg="lightgray")

        self.setup_ui()
        self.widget_counter = 0

    def setup_ui(self):
        """Set up comprehensive UI to test all aspects of theming"""

        # Header section
        header_frame = tk.Frame(self.app, bg="white", relief="raised", bd=2)
        header_frame.pack(fill="x", padx=5, pady=5)

        title_label = tk.Label(
            header_frame,
            text="🌟 Complete Accessibility Demo 🌟",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="darkblue",
            pady=10,
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Demonstrating that HIGH CONTRAST themes the ENTIRE APPLICATION",
            font=("Arial", 12, "italic"),
            bg="white",
            fg="darkgreen",
            pady=5,
        )
        subtitle_label.pack()

        # Control panel
        control_frame = tk.Frame(header_frame, bg="white")
        control_frame.pack(pady=10)

        self.theme_btn = tk.Button(
            control_frame,
            text="🎨 Enable High Contrast",
            command=self.toggle_theme,
            font=("Arial", 12, "bold"),
            bg="lightblue",
            fg="black",
            padx=10,
            pady=5,
        )
        self.theme_btn.pack(side="left", padx=5)

        self.add_widgets_btn = tk.Button(
            control_frame,
            text="➕ Add New Widgets",
            command=self.add_dynamic_widgets,
            font=("Arial", 12, "bold"),
            bg="lightgreen",
            fg="black",
            padx=10,
            pady=5,
        )
        self.add_widgets_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(
            control_frame,
            text="🔄 Reset Demo",
            command=self.reset_demo,
            font=("Arial", 12, "bold"),
            bg="orange",
            fg="black",
            padx=10,
            pady=5,
        )
        self.reset_btn.pack(side="left", padx=5)

        # Status display
        self.status_label = tk.Label(
            header_frame,
            text="Status: Normal theme - Notice the GRAY main window background",
            font=("Arial", 11, "bold"),
            bg="lightyellow",
            fg="darkred",
            pady=5,
        )
        self.status_label.pack(fill="x", padx=10, pady=5)

        # Main content area - comprehensive widget showcase
        self.create_widget_showcase()

        # Dynamic widgets area
        self.dynamic_frame = tk.LabelFrame(
            self.app,
            text="🔄 Dynamic Widgets (Created After Theme Applied)",
            font=("Arial", 12, "bold"),
            bg="lightgray",
            fg="black",
            padx=10,
            pady=10,
        )
        self.dynamic_frame.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(
            self.dynamic_frame,
            text="👆 Click 'Add New Widgets' to test that new widgets get themed automatically",
            font=("Arial", 10, "italic"),
            bg="lightgray",
            fg="darkblue",
        ).pack(pady=5)

    def create_widget_showcase(self):
        """Create comprehensive showcase of all widget types"""

        # Main showcase container
        showcase_frame = tk.Frame(self.app, bg="lightgray", relief="sunken", bd=2)
        showcase_frame.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(
            showcase_frame,
            text="📋 Widget Showcase - All These Should Be Themed",
            font=("Arial", 14, "bold"),
            bg="lightgray",
            fg="darkblue",
        ).pack(pady=5)

        # Create sections for different widget types
        self.create_input_section(showcase_frame)
        self.create_button_section(showcase_frame)
        self.create_selection_section(showcase_frame)
        self.create_display_section(showcase_frame)

    def create_input_section(self, parent):
        """Input widgets section"""
        section_frame = tk.LabelFrame(
            parent,
            text="📝 Input Widgets",
            font=("Arial", 11, "bold"),
            bg="lightgray",
            fg="black",
            padx=10,
            pady=5,
        )
        section_frame.pack(fill="x", padx=5, pady=2)

        # Regular tkinter widgets
        tk.Label(section_frame, text="Name:", bg="lightgray").pack(anchor="w")
        self.name_entry = tk.Entry(section_frame, width=30, font=("Arial", 10))
        self.name_entry.pack(anchor="w", pady=2)
        self.name_entry.insert(0, "Regular Entry widget")

        tk.Label(section_frame, text="Comments:", bg="lightgray").pack(
            anchor="w", pady=(10, 0)
        )
        self.text_widget = tk.Text(
            section_frame, height=3, width=50, font=("Arial", 10)
        )
        self.text_widget.pack(anchor="w", pady=2)
        self.text_widget.insert(
            "1.0",
            "This is a Text widget that should be themed.\nNotice how it gets high contrast colors!",
        )

        # Accessible widgets
        AccessibleLabel(
            section_frame,
            accessible_name="Email field label",
            text="Email (Accessible):",
        ).pack(anchor="w", pady=(10, 0))
        self.email_entry = AccessibleEntry(
            section_frame, accessible_name="Email input field", width=30
        )
        self.email_entry.pack(anchor="w", pady=2)
        self.email_entry.insert(0, "Accessible Entry widget")

    def create_button_section(self, parent):
        """Button widgets section"""
        section_frame = tk.LabelFrame(
            parent,
            text="🔘 Button Widgets",
            font=("Arial", 11, "bold"),
            bg="lightgray",
            fg="black",
            padx=10,
            pady=5,
        )
        section_frame.pack(fill="x", padx=5, pady=2)

        button_row = tk.Frame(section_frame, bg="lightgray")
        button_row.pack(anchor="w", pady=5)

        # Regular buttons with different colors
        colors = [
            ("Red Button", "red", "white"),
            ("Green Button", "green", "white"),
            ("Blue Button", "blue", "white"),
            ("Purple Button", "purple", "white"),
        ]

        for text, bg, fg in colors:
            tk.Button(
                button_row,
                text=text,
                bg=bg,
                fg=fg,
                font=("Arial", 9),
                command=lambda t=text: self.button_clicked(t),
            ).pack(side="left", padx=2)

        # Accessible button
        AccessibleButton(
            section_frame,
            accessible_name="Accessible button example",
            text="🌟 Accessible Button",
            font=("Arial", 10, "bold"),
            bg="gold",
            fg="black",
            command=lambda: self.button_clicked("Accessible"),
        ).pack(anchor="w", pady=5)

    def create_selection_section(self, parent):
        """Selection widgets section"""
        section_frame = tk.LabelFrame(
            parent,
            text="☑️ Selection Widgets",
            font=("Arial", 11, "bold"),
            bg="lightgray",
            fg="black",
            padx=10,
            pady=5,
        )
        section_frame.pack(fill="x", padx=5, pady=2)

        # Checkbuttons
        check_frame = tk.Frame(section_frame, bg="lightgray")
        check_frame.pack(anchor="w", pady=2)

        tk.Label(
            check_frame, text="Options:", bg="lightgray", font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.check_vars = []
        for i, option in enumerate(["Enable notifications", "Auto-save", "Dark mode"]):
            var = tk.BooleanVar()
            self.check_vars.append(var)
            tk.Checkbutton(
                check_frame,
                text=option,
                variable=var,
                bg="lightgray",
                font=("Arial", 9),
                command=lambda: self.selection_changed("checkbox"),
            ).pack(anchor="w")

        # Radio buttons
        radio_frame = tk.Frame(section_frame, bg="lightgray")
        radio_frame.pack(anchor="w", pady=(10, 2))

        tk.Label(
            radio_frame,
            text="Theme preference:",
            bg="lightgray",
            font=("Arial", 10, "bold"),
        ).pack(anchor="w")

        self.radio_var = tk.StringVar(value="auto")
        for choice, value in [("Auto", "auto"), ("Light", "light"), ("Dark", "dark")]:
            tk.Radiobutton(
                radio_frame,
                text=choice,
                variable=self.radio_var,
                value=value,
                bg="lightgray",
                font=("Arial", 9),
                command=lambda: self.selection_changed("radio"),
            ).pack(anchor="w")

        # Scale
        scale_frame = tk.Frame(section_frame, bg="lightgray")
        scale_frame.pack(anchor="w", pady=(10, 2))

        tk.Label(
            scale_frame, text="Volume:", bg="lightgray", font=("Arial", 10, "bold")
        ).pack(anchor="w")
        self.scale = tk.Scale(
            scale_frame,
            from_=0,
            to=100,
            orient="horizontal",
            bg="lightgray",
            font=("Arial", 9),
            command=lambda v: self.scale_changed(v),
        )
        self.scale.pack(anchor="w", fill="x", pady=2)
        self.scale.set(50)

    def create_display_section(self, parent):
        """Display widgets section"""
        section_frame = tk.LabelFrame(
            parent,
            text="📊 Display Widgets",
            font=("Arial", 11, "bold"),
            bg="lightgray",
            fg="black",
            padx=10,
            pady=5,
        )
        section_frame.pack(fill="x", padx=5, pady=2)

        display_row = tk.Frame(section_frame, bg="lightgray")
        display_row.pack(fill="x", pady=5)

        # Listbox
        list_frame = tk.Frame(display_row, bg="lightgray")
        list_frame.pack(side="left", anchor="nw", padx=(0, 10))

        tk.Label(
            list_frame, text="Items:", bg="lightgray", font=("Arial", 10, "bold")
        ).pack(anchor="w")
        self.listbox = tk.Listbox(list_frame, height=4, width=20, font=("Arial", 9))
        items = [
            "Document 1",
            "Document 2",
            "Image.jpg",
            "Video.mp4",
            "Spreadsheet.xlsx",
        ]
        for item in items:
            self.listbox.insert(tk.END, item)
        self.listbox.pack(anchor="w", pady=2)
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.listbox_selected())

        # Canvas
        canvas_frame = tk.Frame(display_row, bg="lightgray")
        canvas_frame.pack(side="left", anchor="nw")

        tk.Label(
            canvas_frame, text="Canvas:", bg="lightgray", font=("Arial", 10, "bold")
        ).pack(anchor="w")
        self.canvas = tk.Canvas(
            canvas_frame, width=200, height=100, bg="white", relief="sunken", bd=1
        )
        self.canvas.pack(anchor="w", pady=2)

        # Draw some shapes
        self.canvas.create_rectangle(
            10, 10, 60, 40, fill="red", outline="darkred", width=2
        )
        self.canvas.create_oval(
            70, 10, 120, 40, fill="blue", outline="darkblue", width=2
        )
        self.canvas.create_text(
            100, 60, text="Canvas Graphics", font=("Arial", 10), fill="black"
        )
        self.canvas.create_line(10, 80, 190, 80, fill="green", width=3)

    def toggle_theme(self):
        """Toggle high contrast theme"""
        if not self.app.is_high_contrast_enabled():
            print("🎨 ENABLING High Contrast Theme...")
            print("👀 Watch the ENTIRE application change:")
            print("   • Main window: lightgray → BLACK")
            print("   • All widgets: various colors → BLACK backgrounds")
            print("   • All text: various colors → WHITE")
            print("   • This is COMPLETE accessibility theming!")

            self.app.enable_high_contrast()
            self.theme_btn.config(text="🔄 Disable High Contrast")
            self.status_label.config(
                text="Status: HIGH CONTRAST - Main window and ALL widgets are now BLACK!"
            )

            print("✅ High contrast theme ENABLED!")
            print("💡 Now try adding new widgets - they'll be themed automatically!")

        else:
            print("🔄 DISABLING High Contrast Theme...")
            print("👀 Watch everything return to normal colors!")

            self.app.disable_high_contrast()
            self.theme_btn.config(text="🎨 Enable High Contrast")
            self.status_label.config(
                text="Status: Normal theme - Back to original colors"
            )

            print("✅ High contrast theme DISABLED!")
            print("🔍 Everything should be back to normal colors")

    def add_dynamic_widgets(self):
        """Add new widgets to test dynamic theming"""
        self.widget_counter += 1

        print(f"➕ Adding dynamic widget set #{self.widget_counter}...")

        # Create new frame for this set
        widget_set_frame = tk.Frame(
            self.dynamic_frame, relief="ridge", bd=2, bg="lightgray"
        )
        widget_set_frame.pack(fill="x", padx=5, pady=3)

        tk.Label(
            widget_set_frame,
            text=f"🆕 Dynamic Widget Set #{self.widget_counter}",
            font=("Arial", 11, "bold"),
            bg="lightgray",
            fg="darkblue",
        ).pack(anchor="w", padx=5, pady=2)

        content_frame = tk.Frame(widget_set_frame, bg="lightgray")
        content_frame.pack(fill="x", padx=10, pady=5)

        # Various new widgets
        tk.Label(
            content_frame, text=f"Dynamic Label #{self.widget_counter}:", bg="lightgray"
        ).pack(anchor="w")

        new_entry = tk.Entry(content_frame, width=40, font=("Arial", 10))
        new_entry.pack(anchor="w", pady=2)
        new_entry.insert(
            0, f"This is dynamic entry #{self.widget_counter} - should be themed!"
        )

        # New buttons
        btn_frame = tk.Frame(content_frame, bg="lightgray")
        btn_frame.pack(anchor="w", pady=5)

        for i, (color, bg) in enumerate(
            [("Red", "red"), ("Green", "green"), ("Blue", "blue")]
        ):
            tk.Button(
                btn_frame,
                text=f"{color} #{self.widget_counter}",
                bg=bg,
                fg="white",
                font=("Arial", 9),
                command=lambda c=color, n=self.widget_counter: self.dynamic_button_clicked(
                    c, n
                ),
            ).pack(side="left", padx=2)

        # New checkbutton
        new_check_var = tk.BooleanVar()
        tk.Checkbutton(
            content_frame,
            text=f"Dynamic option #{self.widget_counter}",
            variable=new_check_var,
            bg="lightgray",
            font=("Arial", 9),
        ).pack(anchor="w", pady=2)

        # New accessible widgets
        AccessibleLabel(
            content_frame,
            accessible_name=f"Accessible dynamic label {self.widget_counter}",
            text=f"🌟 Accessible Dynamic Label #{self.widget_counter}",
        ).pack(anchor="w", pady=2)

        AccessibleButton(
            content_frame,
            accessible_name=f"Accessible dynamic button {self.widget_counter}",
            text=f"🌟 Accessible Btn #{self.widget_counter}",
            bg="gold",
            fg="black",
            font=("Arial", 9),
            command=lambda n=self.widget_counter: self.accessible_button_clicked(n),
        ).pack(anchor="w", pady=2)

        theme_status = (
            "HIGH CONTRAST" if self.app.is_high_contrast_enabled() else "normal"
        )
        print(f"✅ Dynamic widgets added with {theme_status} appearance!")

        if self.app.is_high_contrast_enabled():
            print("🎯 Notice: New widgets automatically have BLACK backgrounds!")
        else:
            print("💡 Apply high contrast theme to see them change instantly!")

    def reset_demo(self):
        """Reset the demo to initial state"""
        print("🔄 Resetting demo...")

        # Clear dynamic widgets
        for widget in self.dynamic_frame.winfo_children():
            if not isinstance(widget, tk.Label) or "Click" not in widget.cget("text"):
                widget.destroy()

        # Reset counter
        self.widget_counter = 0

        # Disable theme if enabled
        if self.app.is_high_contrast_enabled():
            self.app.disable_high_contrast()
            self.theme_btn.config(text="🎨 Enable High Contrast")
            self.status_label.config(
                text="Status: Normal theme - Demo reset to initial state"
            )

        print("✅ Demo reset complete!")

    # Event handlers
    def button_clicked(self, button_type):
        print(f"🔘 {button_type} button clicked!")

    def dynamic_button_clicked(self, color, number):
        print(f"🔘 Dynamic {color} button #{number} clicked!")

    def accessible_button_clicked(self, number):
        print(f"🌟 Accessible dynamic button #{number} clicked!")

    def selection_changed(self, widget_type):
        print(f"☑️ {widget_type} selection changed")

    def scale_changed(self, value):
        print(f"🎚️ Volume scale changed to: {value}")

    def listbox_selected(self):
        selection = self.listbox.curselection()
        if selection:
            item = self.listbox.get(selection[0])
            print(f"📋 Listbox selected: {item}")

    def run(self):
        """Run the complete demo"""
        print("🚀 Complete Accessibility Demo")
        print("=" * 60)
        print()
        print("This demo answers your key question:")
        print("❓ 'Should the main window/frame also have the theme applied?'")
        print("✅ ANSWER: YES! And this demo proves it works correctly!")
        print()
        print("🎯 What this demo shows:")
        print("   • Main window background gets themed (gray → black)")
        print("   • ALL widget types get themed consistently")
        print("   • NEW widgets created after theming are auto-themed")
        print("   • Complete accessibility compliance")
        print("   • Easy toggle on/off functionality")
        print()
        print("🔍 Try this sequence:")
        print("   1. Notice the current GRAY main window background")
        print("   2. Click '🎨 Enable High Contrast'")
        print("   3. See the ENTIRE window turn BLACK with white text")
        print("   4. Click '➕ Add New Widgets'")
        print("   5. Notice new widgets are automatically BLACK too!")
        print("   6. Click '🔄 Disable High Contrast' to return to normal")
        print()
        print("🌟 This is how accessibility theming should work!")
        print()

        self.app.mainloop()


if __name__ == "__main__":
    demo = CompleteAccessibilityDemo()
    demo.run()
