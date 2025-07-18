#!/usr/bin/env python3
"""
Complete example showing the improved high contrast theming system.
Demonstrates that themes apply to ALL widgets, including those created after apply().
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import tkaria11y
sys.path.insert(0, str(Path(__file__).parent.parent))

from tkaria11y import AccessibleApp
from tkaria11y.widgets import (
    AccessibleButton,
    AccessibleLabel,
    AccessibleEntry,
    AccessibleFrame,
)
import tkinter as tk


class CompleteThemeExample:
    def __init__(self):
        # Create AccessibleApp with theme controls
        self.app = AccessibleApp(
            title="Complete Theme Example",
            high_contrast=False,  # Start without theme
            enable_inspector=True,  # Enable inspector for debugging
        )
        self.app.geometry("700x600")

        self.setup_ui()
        self.widget_counter = 0

    def setup_ui(self):
        """Set up the complete UI"""

        # Header with theme controls
        header_frame = AccessibleFrame(self.app, accessible_name="Theme controls")
        header_frame.pack(fill="x", padx=10, pady=5)

        AccessibleLabel(
            header_frame,
            accessible_name="Complete Theme Example",
            text="Complete Theme Example - All Widgets Get Themed!",
            font=("Arial", 16, "bold"),
        ).pack(pady=10)

        # Theme control buttons
        control_frame = AccessibleFrame(header_frame, accessible_name="Control buttons")
        control_frame.pack(fill="x", pady=5)

        self.theme_btn = AccessibleButton(
            control_frame,
            accessible_name="Toggle high contrast theme",
            text="Enable High Contrast",
            command=self.toggle_theme,
            bg="lightblue",
            font=("Arial", 10, "bold"),
        )
        self.theme_btn.pack(side="left", padx=5)

        self.font_btn = AccessibleButton(
            control_frame,
            accessible_name="Toggle dyslexic font",
            text="Enable Dyslexic Font",
            command=self.toggle_font,
            bg="lightgreen",
            font=("Arial", 10, "bold"),
        )
        self.font_btn.pack(side="left", padx=5)

        self.add_widgets_btn = AccessibleButton(
            control_frame,
            accessible_name="Add new widgets to test dynamic theming",
            text="Add New Widgets",
            command=self.add_dynamic_widgets,
            bg="orange",
            font=("Arial", 10, "bold"),
        )
        self.add_widgets_btn.pack(side="left", padx=5)

        # Status label
        self.status_label = AccessibleLabel(
            header_frame,
            accessible_name="Current theme status",
            text="Status: Normal theme, System font",
            font=("Arial", 10, "italic"),
        )
        self.status_label.pack(pady=5)

        # Main content area with various widgets
        self.create_widget_showcase()

        # Dynamic widgets area
        self.dynamic_frame = AccessibleFrame(
            self.app, accessible_name="Dynamic widgets area", relief="groove", bd=2
        )
        self.dynamic_frame.pack(fill="both", expand=True, padx=10, pady=5)

        AccessibleLabel(
            self.dynamic_frame,
            accessible_name="Dynamic widgets section title",
            text="Dynamic Widgets (Created After Theme Applied)",
            font=("Arial", 12, "bold"),
        ).pack(pady=5)

        AccessibleLabel(
            self.dynamic_frame,
            accessible_name="Instructions for dynamic widgets",
            text="Click 'Add New Widgets' to test that new widgets get themed automatically",
            font=("Arial", 10),
        ).pack(pady=2)

    def create_widget_showcase(self):
        """Create a showcase of all widget types"""

        # Main showcase frame
        showcase_frame = AccessibleFrame(
            self.app, accessible_name="Widget showcase", relief="sunken", bd=2
        )
        showcase_frame.pack(fill="both", expand=True, padx=10, pady=5)

        AccessibleLabel(
            showcase_frame,
            accessible_name="Widget showcase title",
            text="Widget Showcase - All These Get Themed",
            font=("Arial", 12, "bold"),
        ).pack(pady=5)

        # Create notebook-like sections
        sections = [
            ("Input Widgets", self.create_input_section),
            ("Button Widgets", self.create_button_section),
            ("Selection Widgets", self.create_selection_section),
            ("Display Widgets", self.create_display_section),
        ]

        for section_name, create_func in sections:
            section_frame = AccessibleFrame(
                showcase_frame,
                accessible_name=f"{section_name} section",
                relief="raised",
                bd=1,
            )
            section_frame.pack(fill="x", padx=5, pady=2)

            AccessibleLabel(
                section_frame,
                accessible_name=f"{section_name} section title",
                text=section_name,
                font=("Arial", 11, "bold"),
                bg="lightgray",
            ).pack(fill="x", pady=2)

            create_func(section_frame)

    def create_input_section(self, parent):
        """Create input widgets section"""
        frame = AccessibleFrame(parent, accessible_name="Input widgets")
        frame.pack(fill="x", padx=10, pady=5)

        # Entry widgets
        AccessibleLabel(frame, accessible_name="Name field label", text="Name:").pack(
            anchor="w"
        )
        self.name_entry = AccessibleEntry(
            frame, accessible_name="Name input field", width=30
        )
        self.name_entry.pack(anchor="w", pady=2)

        AccessibleLabel(frame, accessible_name="Email field label", text="Email:").pack(
            anchor="w", pady=(10, 0)
        )
        self.email_entry = AccessibleEntry(
            frame, accessible_name="Email input field", width=30
        )
        self.email_entry.pack(anchor="w", pady=2)

        # Text widget
        AccessibleLabel(
            frame, accessible_name="Comments field label", text="Comments:"
        ).pack(anchor="w", pady=(10, 0))
        self.text_widget = tk.Text(frame, height=3, width=40)
        self.text_widget.pack(anchor="w", pady=2)
        self.text_widget.insert("1.0", "This is a text widget that will be themed too!")

    def create_button_section(self, parent):
        """Create button widgets section"""
        frame = AccessibleFrame(parent, accessible_name="Button widgets")
        frame.pack(fill="x", padx=10, pady=5)

        button_row = AccessibleFrame(frame, accessible_name="Button row")
        button_row.pack(anchor="w")

        colors = [
            ("Red", "red", "white"),
            ("Green", "green", "white"),
            ("Blue", "blue", "white"),
            ("Purple", "purple", "white"),
        ]

        for text, bg, fg in colors:
            AccessibleButton(
                button_row,
                accessible_name=f"{text} button",
                text=f"{text} Button",
                bg=bg,
                fg=fg,
                command=lambda t=text: self.button_clicked(t),
            ).pack(side="left", padx=5, pady=2)

    def create_selection_section(self, parent):
        """Create selection widgets section"""
        frame = AccessibleFrame(parent, accessible_name="Selection widgets")
        frame.pack(fill="x", padx=10, pady=5)

        # Checkbuttons
        check_frame = AccessibleFrame(frame, accessible_name="Checkbutton group")
        check_frame.pack(anchor="w", pady=2)

        AccessibleLabel(
            check_frame, accessible_name="Checkbutton group label", text="Options:"
        ).pack(anchor="w")

        self.check_vars = []
        for i, option in enumerate(["Option A", "Option B", "Option C"]):
            var = tk.BooleanVar()
            self.check_vars.append(var)
            tk.Checkbutton(
                check_frame,
                text=option,
                variable=var,
                command=lambda: self.selection_changed("checkbox"),
            ).pack(anchor="w")

        # Radio buttons
        radio_frame = AccessibleFrame(frame, accessible_name="Radio button group")
        radio_frame.pack(anchor="w", pady=(10, 2))

        AccessibleLabel(
            radio_frame, accessible_name="Radio button group label", text="Choose one:"
        ).pack(anchor="w")

        self.radio_var = tk.StringVar(value="choice1")
        for choice in ["Choice 1", "Choice 2", "Choice 3"]:
            tk.Radiobutton(
                radio_frame,
                text=choice,
                variable=self.radio_var,
                value=choice.lower().replace(" ", ""),
                command=lambda: self.selection_changed("radio"),
            ).pack(anchor="w")

        # Scale
        scale_frame = AccessibleFrame(frame, accessible_name="Scale widget")
        scale_frame.pack(anchor="w", pady=(10, 2))

        AccessibleLabel(
            scale_frame, accessible_name="Scale label", text="Volume:"
        ).pack(anchor="w")
        self.scale = tk.Scale(
            scale_frame,
            from_=0,
            to=100,
            orient="horizontal",
            command=lambda v: self.scale_changed(v),
        )
        self.scale.pack(anchor="w", fill="x", pady=2)

    def create_display_section(self, parent):
        """Create display widgets section"""
        frame = AccessibleFrame(parent, accessible_name="Display widgets")
        frame.pack(fill="x", padx=10, pady=5)

        # Listbox
        list_frame = AccessibleFrame(frame, accessible_name="Listbox widget")
        list_frame.pack(anchor="w", pady=2)

        AccessibleLabel(
            list_frame, accessible_name="Listbox label", text="Items:"
        ).pack(anchor="w")
        self.listbox = tk.Listbox(list_frame, height=4, width=30)
        for i in range(8):
            self.listbox.insert(tk.END, f"List Item {i+1}")
        self.listbox.pack(anchor="w", pady=2)
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.listbox_selected())

        # Canvas (for drawing)
        canvas_frame = AccessibleFrame(frame, accessible_name="Canvas widget")
        canvas_frame.pack(anchor="w", pady=(10, 2))

        AccessibleLabel(
            canvas_frame, accessible_name="Canvas label", text="Canvas:"
        ).pack(anchor="w")
        self.canvas = tk.Canvas(canvas_frame, width=200, height=100, bg="white")
        self.canvas.pack(anchor="w", pady=2)

        # Draw something on canvas
        self.canvas.create_rectangle(10, 10, 50, 50, fill="red", outline="black")
        self.canvas.create_oval(60, 10, 100, 50, fill="blue", outline="black")
        self.canvas.create_text(130, 30, text="Canvas", font=("Arial", 12))

    def toggle_theme(self):
        """Toggle high contrast theme"""
        new_state = self.app.toggle_high_contrast()

        if new_state:
            self.theme_btn.config(text="Disable High Contrast")
            print("🎨 High contrast theme ENABLED")
        else:
            self.theme_btn.config(text="Enable High Contrast")
            print("🔄 High contrast theme DISABLED")

        self.update_status()

    def toggle_font(self):
        """Toggle dyslexic font"""
        new_state = self.app.toggle_dyslexic_font()

        if new_state:
            self.font_btn.config(text="Disable Dyslexic Font")
            print("📝 Dyslexic font ENABLED")
        else:
            self.font_btn.config(text="Enable Dyslexic Font")
            print("🔄 Dyslexic font DISABLED")

        self.update_status()

    def add_dynamic_widgets(self):
        """Add new widgets dynamically to test theming"""
        self.widget_counter += 1

        print(f"➕ Adding dynamic widget set #{self.widget_counter}")

        # Create a new frame for this set of widgets
        widget_set_frame = AccessibleFrame(
            self.dynamic_frame,
            accessible_name=f"Dynamic widget set {self.widget_counter}",
            relief="ridge",
            bd=1,
        )
        widget_set_frame.pack(fill="x", padx=5, pady=2)

        AccessibleLabel(
            widget_set_frame,
            accessible_name=f"Dynamic set {self.widget_counter} title",
            text=f"Dynamic Widget Set #{self.widget_counter}",
            font=("Arial", 10, "bold"),
        ).pack(anchor="w", padx=5, pady=2)

        # Add various widgets
        content_frame = AccessibleFrame(
            widget_set_frame, accessible_name=f"Content frame {self.widget_counter}"
        )
        content_frame.pack(fill="x", padx=10, pady=2)

        # Entry
        AccessibleLabel(
            content_frame,
            accessible_name=f"Dynamic entry label {self.widget_counter}",
            text=f"Dynamic Entry #{self.widget_counter}:",
        ).pack(anchor="w")
        dynamic_entry = AccessibleEntry(
            content_frame, accessible_name=f"Dynamic entry {self.widget_counter}"
        )
        dynamic_entry.pack(anchor="w", pady=1)
        dynamic_entry.insert(0, f"This is dynamic entry #{self.widget_counter}")

        # Buttons
        btn_frame = AccessibleFrame(
            content_frame, accessible_name=f"Dynamic button frame {self.widget_counter}"
        )
        btn_frame.pack(anchor="w", pady=5)

        for i, (color, bg) in enumerate(
            [("Red", "red"), ("Green", "green"), ("Blue", "blue")]
        ):
            AccessibleButton(
                btn_frame,
                accessible_name=f"Dynamic {color} button {self.widget_counter}",
                text=f"{color} #{self.widget_counter}",
                bg=bg,
                fg="white",
                command=lambda c=color, n=self.widget_counter: self.dynamic_button_clicked(
                    c, n
                ),
            ).pack(side="left", padx=2)

        # Checkbutton
        dynamic_check_var = tk.BooleanVar()
        tk.Checkbutton(
            content_frame,
            text=f"Dynamic Option #{self.widget_counter}",
            variable=dynamic_check_var,
            command=lambda: print(f"Dynamic checkbox #{self.widget_counter} toggled"),
        ).pack(anchor="w", pady=2)

        # If theme is enabled, these should automatically be themed
        theme_status = "themed" if self.app.is_high_contrast_enabled() else "normal"
        print(f"✅ Dynamic widgets added with {theme_status} appearance")

    def update_status(self):
        """Update the status label"""
        theme_status = (
            "High Contrast" if self.app.is_high_contrast_enabled() else "Normal"
        )
        font_status = (
            "Dyslexic Font" if self.app.is_dyslexic_font_enabled() else "System Font"
        )

        self.status_label.config(text=f"Status: {theme_status} theme, {font_status}")

    # Event handlers
    def button_clicked(self, color):
        print(f"🔘 {color} button clicked!")

    def dynamic_button_clicked(self, color, number):
        print(f"🔘 Dynamic {color} button #{number} clicked!")

    def selection_changed(self, widget_type):
        print(f"☑️ {widget_type} selection changed")

    def scale_changed(self, value):
        print(f"🎚️ Scale changed to: {value}")

    def listbox_selected(self):
        selection = self.listbox.curselection()
        if selection:
            item = self.listbox.get(selection[0])
            print(f"📋 Listbox selected: {item}")

    def run(self):
        """Run the application"""
        print("🚀 Complete Theme Example")
        print("=" * 50)
        print("This example demonstrates:")
        print("• High contrast theme applies to ALL widgets")
        print("• New widgets created AFTER theme application are automatically themed")
        print("• Theme can be toggled on/off dynamically")
        print("• Dyslexic font can be toggled independently")
        print("• Works with both standard tkinter and accessible widgets")
        print()
        print("Try this:")
        print("1. Click 'Enable High Contrast' - see ALL widgets change color")
        print("2. Click 'Add New Widgets' - new widgets are automatically themed")
        print("3. Click 'Enable Dyslexic Font' - see font change")
        print("4. Press F2 to show/hide the accessibility inspector")
        print()

        self.app.mainloop()


if __name__ == "__main__":
    example = CompleteThemeExample()
    example.run()
