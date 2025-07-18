#!/usr/bin/env python3
"""
Robust theme test to verify that the improved theming system works correctly.
Tests both application and removal of themes to ensure no areas are missed.
"""

import sys
from pathlib import Path
import tkinter as tk

# Add the parent directory to the path so we can import tkaria11y
sys.path.insert(0, str(Path(__file__).parent.parent))

from tkaria11y.themes import HighContrastTheme


class RobustThemeTest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Robust Theme Test - Complete Coverage")
        self.root.geometry("700x600")

        # Set distinctive initial colors to make theming obvious
        self.root.configure(bg="#f0f0f0")  # Light gray

        self.theme_applied = False
        self.widget_counter = 0
        self.setup_ui()

    def setup_ui(self):
        """Set up comprehensive UI with all widget types"""

        # Header with controls
        header_frame = tk.Frame(self.root, bg="#e0e0e0", relief="raised", bd=2)
        header_frame.pack(fill="x", padx=5, pady=5)

        title_label = tk.Label(
            header_frame,
            text="🔍 Robust Theme Test - Complete Coverage",
            font=("Arial", 14, "bold"),
            bg="#e0e0e0",
            fg="darkblue",
        )
        title_label.pack(pady=5)

        # Control buttons
        control_frame = tk.Frame(header_frame, bg="#e0e0e0")
        control_frame.pack(pady=5)

        self.theme_btn = tk.Button(
            control_frame,
            text="🎨 Apply High Contrast",
            command=self.toggle_theme,
            font=("Arial", 11, "bold"),
            bg="lightblue",
            fg="black",
            padx=10,
        )
        self.theme_btn.pack(side="left", padx=5)

        self.add_btn = tk.Button(
            control_frame,
            text="➕ Add Widgets",
            command=self.add_widgets,
            font=("Arial", 11, "bold"),
            bg="lightgreen",
            fg="black",
            padx=10,
        )
        self.add_btn.pack(side="left", padx=5)

        self.inspect_btn = tk.Button(
            control_frame,
            text="🔍 Inspect Colors",
            command=self.inspect_colors,
            font=("Arial", 11, "bold"),
            bg="orange",
            fg="black",
            padx=10,
        )
        self.inspect_btn.pack(side="left", padx=5)

        # Status display
        self.status_label = tk.Label(
            header_frame,
            text="Status: Normal theme - Look for light gray backgrounds",
            font=("Arial", 10, "italic"),
            bg="lightyellow",
            fg="darkred",
            pady=3,
        )
        self.status_label.pack(fill="x", padx=10, pady=5)

        # Create comprehensive widget showcase
        self.create_comprehensive_showcase()

        # Dynamic widgets area
        self.dynamic_frame = tk.LabelFrame(
            self.root,
            text="🔄 Dynamic Widgets Area",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="black",
            padx=10,
            pady=5,
        )
        self.dynamic_frame.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(
            self.dynamic_frame,
            text="Click 'Add Widgets' to test dynamic theming",
            bg="#f0f0f0",
            fg="darkblue",
            font=("Arial", 10),
        ).pack(pady=5)

    def create_comprehensive_showcase(self):
        """Create showcase with ALL widget types"""

        # Main showcase container
        showcase_frame = tk.Frame(self.root, bg="#f0f0f0", relief="sunken", bd=2)
        showcase_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create multiple sections to test different widget types
        sections = [
            ("📝 Input Widgets", self.create_input_widgets),
            ("🔘 Button Widgets", self.create_button_widgets),
            ("☑️ Selection Widgets", self.create_selection_widgets),
            ("📊 Display Widgets", self.create_display_widgets),
            ("🎛️ Container Widgets", self.create_container_widgets),
        ]

        for section_title, create_func in sections:
            section_frame = tk.LabelFrame(
                showcase_frame,
                text=section_title,
                font=("Arial", 10, "bold"),
                bg="#f0f0f0",
                fg="darkgreen",
                padx=5,
                pady=5,
            )
            section_frame.pack(fill="x", padx=5, pady=2)
            create_func(section_frame)

    def create_input_widgets(self, parent):
        """Create input widgets"""
        content_frame = tk.Frame(parent, bg="#f0f0f0")
        content_frame.pack(fill="x", padx=5, pady=5)

        # Entry widgets
        tk.Label(content_frame, text="Name:", bg="#f0f0f0", fg="black").pack(anchor="w")
        self.name_entry = tk.Entry(content_frame, width=30, bg="white", fg="black")
        self.name_entry.pack(anchor="w", pady=2)
        self.name_entry.insert(0, "Test entry widget")

        # Text widget
        tk.Label(content_frame, text="Comments:", bg="#f0f0f0", fg="black").pack(
            anchor="w", pady=(10, 0)
        )
        self.text_widget = tk.Text(
            content_frame, height=3, width=40, bg="white", fg="black"
        )
        self.text_widget.pack(anchor="w", pady=2)
        self.text_widget.insert(
            "1.0",
            "This is a text widget.\nIt should be themed completely.\nNo areas should be missed!",
        )

        # Spinbox
        tk.Label(content_frame, text="Number:", bg="#f0f0f0", fg="black").pack(
            anchor="w", pady=(10, 0)
        )
        self.spinbox = tk.Spinbox(
            content_frame, from_=0, to=100, width=10, bg="white", fg="black"
        )
        self.spinbox.pack(anchor="w", pady=2)

    def create_button_widgets(self, parent):
        """Create button widgets"""
        content_frame = tk.Frame(parent, bg="#f0f0f0")
        content_frame.pack(fill="x", padx=5, pady=5)

        button_row = tk.Frame(content_frame, bg="#f0f0f0")
        button_row.pack(anchor="w")

        # Various buttons with different colors
        colors = [
            ("Red", "red", "white"),
            ("Green", "green", "white"),
            ("Blue", "blue", "white"),
            ("Yellow", "yellow", "black"),
            ("Purple", "purple", "white"),
        ]

        for text, bg, fg in colors:
            btn = tk.Button(
                button_row,
                text=text,
                bg=bg,
                fg=fg,
                font=("Arial", 9),
                command=lambda t=text: self.button_clicked(t),
            )
            btn.pack(side="left", padx=2)

        # Menubutton
        self.menubutton = tk.Menubutton(
            content_frame, text="Menu ▼", bg="lightcyan", fg="black"
        )
        self.menubutton.pack(anchor="w", pady=5)

        menu = tk.Menu(self.menubutton, tearoff=0, bg="white", fg="black")
        menu.add_command(
            label="Option 1", command=lambda: self.menu_clicked("Option 1")
        )
        menu.add_command(
            label="Option 2", command=lambda: self.menu_clicked("Option 2")
        )
        menu.add_separator()
        menu.add_command(label="Exit", command=lambda: self.menu_clicked("Exit"))
        self.menubutton.config(menu=menu)

    def create_selection_widgets(self, parent):
        """Create selection widgets"""
        content_frame = tk.Frame(parent, bg="#f0f0f0")
        content_frame.pack(fill="x", padx=5, pady=5)

        # Checkbuttons
        check_frame = tk.Frame(content_frame, bg="#f0f0f0")
        check_frame.pack(anchor="w")

        tk.Label(
            check_frame,
            text="Options:",
            bg="#f0f0f0",
            fg="black",
            font=("Arial", 9, "bold"),
        ).pack(anchor="w")

        self.check_vars = []
        options = ["Enable feature A", "Enable feature B", "Enable feature C"]
        for option in options:
            var = tk.BooleanVar()
            self.check_vars.append(var)
            cb = tk.Checkbutton(
                check_frame,
                text=option,
                variable=var,
                bg="#f0f0f0",
                fg="black",
                selectcolor="white",
                font=("Arial", 9),
            )
            cb.pack(anchor="w")

        # Radio buttons
        radio_frame = tk.Frame(content_frame, bg="#f0f0f0")
        radio_frame.pack(anchor="w", pady=(10, 0))

        tk.Label(
            radio_frame,
            text="Choose one:",
            bg="#f0f0f0",
            fg="black",
            font=("Arial", 9, "bold"),
        ).pack(anchor="w")

        self.radio_var = tk.StringVar(value="option1")
        radio_options = [
            ("Option 1", "option1"),
            ("Option 2", "option2"),
            ("Option 3", "option3"),
        ]
        for text, value in radio_options:
            rb = tk.Radiobutton(
                radio_frame,
                text=text,
                variable=self.radio_var,
                value=value,
                bg="#f0f0f0",
                fg="black",
                selectcolor="white",
                font=("Arial", 9),
            )
            rb.pack(anchor="w")

        # Scale
        scale_frame = tk.Frame(content_frame, bg="#f0f0f0")
        scale_frame.pack(anchor="w", pady=(10, 0))

        tk.Label(
            scale_frame,
            text="Volume:",
            bg="#f0f0f0",
            fg="black",
            font=("Arial", 9, "bold"),
        ).pack(anchor="w")
        self.scale = tk.Scale(
            scale_frame,
            from_=0,
            to=100,
            orient="horizontal",
            bg="#f0f0f0",
            fg="black",
            troughcolor="white",
            font=("Arial", 8),
        )
        self.scale.pack(anchor="w", fill="x", pady=2)
        self.scale.set(50)

    def create_display_widgets(self, parent):
        """Create display widgets"""
        content_frame = tk.Frame(parent, bg="#f0f0f0")
        content_frame.pack(fill="x", padx=5, pady=5)

        display_row = tk.Frame(content_frame, bg="#f0f0f0")
        display_row.pack(fill="x")

        # Listbox
        list_frame = tk.Frame(display_row, bg="#f0f0f0")
        list_frame.pack(side="left", anchor="nw", padx=(0, 10))

        tk.Label(
            list_frame,
            text="Items:",
            bg="#f0f0f0",
            fg="black",
            font=("Arial", 9, "bold"),
        ).pack(anchor="w")

        # Listbox with scrollbar
        listbox_frame = tk.Frame(list_frame, bg="#f0f0f0")
        listbox_frame.pack(anchor="w")

        self.listbox = tk.Listbox(
            listbox_frame, height=4, width=15, bg="white", fg="black", font=("Arial", 9)
        )
        scrollbar = tk.Scrollbar(listbox_frame, bg="#d0d0d0")

        self.listbox.pack(side="left")
        scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7"]
        for item in items:
            self.listbox.insert(tk.END, item)

        # Canvas
        canvas_frame = tk.Frame(display_row, bg="#f0f0f0")
        canvas_frame.pack(side="left", anchor="nw")

        tk.Label(
            canvas_frame,
            text="Canvas:",
            bg="#f0f0f0",
            fg="black",
            font=("Arial", 9, "bold"),
        ).pack(anchor="w")
        self.canvas = tk.Canvas(
            canvas_frame, width=150, height=80, bg="white", relief="sunken", bd=1
        )
        self.canvas.pack(anchor="w", pady=2)

        # Draw some shapes
        self.canvas.create_rectangle(10, 10, 50, 30, fill="red", outline="darkred")
        self.canvas.create_oval(60, 10, 100, 30, fill="blue", outline="darkblue")
        self.canvas.create_text(75, 50, text="Canvas", font=("Arial", 10), fill="black")
        self.canvas.create_line(10, 65, 140, 65, fill="green", width=2)

    def create_container_widgets(self, parent):
        """Create container widgets"""
        content_frame = tk.Frame(parent, bg="#f0f0f0")
        content_frame.pack(fill="x", padx=5, pady=5)

        # Nested frames with different backgrounds
        frame1 = tk.Frame(content_frame, bg="#e8e8e8", relief="raised", bd=1)
        frame1.pack(fill="x", pady=2)

        tk.Label(
            frame1,
            text="Frame 1 (should be themed)",
            bg="#e8e8e8",
            fg="black",
            font=("Arial", 9),
        ).pack(padx=5, pady=2)

        frame2 = tk.Frame(frame1, bg="#d8d8d8", relief="sunken", bd=1)
        frame2.pack(fill="x", padx=5, pady=2)

        tk.Label(
            frame2,
            text="Nested Frame 2 (should also be themed)",
            bg="#d8d8d8",
            fg="black",
            font=("Arial", 9),
        ).pack(padx=5, pady=2)

        # PanedWindow
        paned = tk.PanedWindow(content_frame, orient="horizontal", bg="#f0f0f0")
        paned.pack(fill="x", pady=5)

        pane1 = tk.Frame(paned, bg="#f8f8f8", width=100, height=50)
        pane2 = tk.Frame(paned, bg="#e8f8e8", width=100, height=50)

        tk.Label(pane1, text="Pane 1", bg="#f8f8f8", fg="black").pack(expand=True)
        tk.Label(pane2, text="Pane 2", bg="#e8f8e8", fg="black").pack(expand=True)

        paned.add(pane1)
        paned.add(pane2)

    def toggle_theme(self):
        """Toggle high contrast theme"""
        if not self.theme_applied:
            print("🎨 APPLYING High Contrast Theme...")
            print("👀 Watch for complete transformation:")
            print("   • Main window: light gray → BLACK")
            print("   • All frames: various grays → BLACK")
            print("   • All widgets: various colors → BLACK backgrounds")
            print("   • All text: various colors → WHITE")

            HighContrastTheme.apply(self.root)
            self.theme_btn.config(text="🔄 Remove High Contrast")
            self.status_label.config(
                text="Status: HIGH CONTRAST - Everything should be BLACK with WHITE text"
            )
            self.theme_applied = True

            print("✅ High contrast theme APPLIED!")
            print("🔍 Check: Are there ANY areas that are not black?")

        else:
            print("🔄 REMOVING High Contrast Theme...")
            print("👀 Watch everything return to original colors:")
            print("   • Main window: BLACK → light gray")
            print("   • All frames: BLACK → various grays")
            print("   • All widgets: BLACK → original colors")
            print("   • All text: WHITE → original colors")

            HighContrastTheme.remove(self.root)
            self.theme_btn.config(text="🎨 Apply High Contrast")
            self.status_label.config(
                text="Status: Normal theme - Back to original light gray backgrounds"
            )
            self.theme_applied = False

            print("✅ High contrast theme REMOVED!")
            print("🔍 Check: Are there ANY areas still black?")

    def add_widgets(self):
        """Add new widgets to test dynamic theming"""
        self.widget_counter += 1

        print(f"➕ Adding dynamic widget set #{self.widget_counter}...")

        # Create new frame for this set
        widget_frame = tk.Frame(self.dynamic_frame, bg="#f0f0f0", relief="groove", bd=2)
        widget_frame.pack(fill="x", padx=5, pady=3)

        tk.Label(
            widget_frame,
            text=f"🆕 Dynamic Set #{self.widget_counter}",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            fg="darkblue",
        ).pack(anchor="w", padx=5, pady=2)

        content = tk.Frame(widget_frame, bg="#f0f0f0")
        content.pack(fill="x", padx=10, pady=5)

        # Various new widgets
        tk.Label(
            content, text=f"Label #{self.widget_counter}:", bg="#f0f0f0", fg="black"
        ).pack(anchor="w")

        new_entry = tk.Entry(content, width=30, bg="white", fg="black")
        new_entry.pack(anchor="w", pady=2)
        new_entry.insert(0, f"Dynamic entry #{self.widget_counter}")

        # New buttons
        btn_frame = tk.Frame(content, bg="#f0f0f0")
        btn_frame.pack(anchor="w", pady=5)

        for i, (color, bg) in enumerate(
            [("Red", "red"), ("Green", "green"), ("Blue", "blue")]
        ):
            tk.Button(
                btn_frame,
                text=f"{color} #{self.widget_counter}",
                bg=bg,
                fg="white",
                font=("Arial", 8),
                command=lambda c=color, n=self.widget_counter: self.dynamic_button_clicked(
                    c, n
                ),
            ).pack(side="left", padx=2)

        # New frame with different background
        nested_frame = tk.Frame(content, bg="#e0e0e0", relief="raised", bd=1)
        nested_frame.pack(fill="x", pady=5)

        tk.Label(
            nested_frame,
            text=f"Nested frame #{self.widget_counter} - should be themed too!",
            bg="#e0e0e0",
            fg="black",
            font=("Arial", 9),
        ).pack(padx=5, pady=2)

        theme_status = "HIGH CONTRAST" if self.theme_applied else "normal"
        print(f"✅ Dynamic widgets added with {theme_status} appearance!")

        if self.theme_applied:
            print("🎯 These new widgets should automatically be BLACK!")
        else:
            print("💡 Apply theme to see them change instantly!")

    def inspect_colors(self):
        """Inspect current colors of various widgets"""
        print("\n🔍 COLOR INSPECTION:")
        print("=" * 40)

        widgets_to_inspect = [
            ("Root window", self.root),
            ("Name entry", self.name_entry),
            ("Text widget", self.text_widget),
            ("Status label", self.status_label),
            ("Listbox", self.listbox),
            ("Canvas", self.canvas),
        ]

        for name, widget in widgets_to_inspect:
            try:
                bg = widget.cget("bg")
                fg = widget.cget("fg") if "fg" in widget.configure() else "N/A"
                print(f"{name:15}: bg={bg:15} fg={fg}")
            except (tk.TclError, AttributeError):
                print(f"{name:15}: Unable to inspect")

        print("=" * 40)

        if self.theme_applied:
            print("✅ HIGH CONTRAST: All backgrounds should be 'black'")
            print("✅ HIGH CONTRAST: All foregrounds should be 'white'")
        else:
            print("ℹ️  NORMAL: Backgrounds should be various light colors")
            print("ℹ️  NORMAL: Foregrounds should be various dark colors")

        print()

    # Event handlers
    def button_clicked(self, color):
        print(f"🔘 {color} button clicked!")

    def dynamic_button_clicked(self, color, number):
        print(f"🔘 Dynamic {color} button #{number} clicked!")

    def menu_clicked(self, option):
        print(f"📋 Menu option '{option}' selected!")

    def run(self):
        """Run the robust test"""
        print("🚀 Robust Theme Test - Complete Coverage")
        print("=" * 50)
        print()
        print("This test addresses your concerns about incomplete theming:")
        print("❌ Problem: Some areas not being themed correctly")
        print("❌ Problem: Some areas remaining themed when disabled")
        print("✅ Solution: Comprehensive theming system")
        print()
        print("🎯 What to test:")
        print("   1. Click '🎨 Apply High Contrast'")
        print("      → EVERYTHING should turn black with white text")
        print("      → Check ALL areas - no light colors should remain")
        print()
        print("   2. Click '➕ Add Widgets'")
        print("      → New widgets should be black immediately")
        print()
        print("   3. Click '🔍 Inspect Colors'")
        print("      → See exact color values of widgets")
        print()
        print("   4. Click '🔄 Remove High Contrast'")
        print("      → EVERYTHING should return to original colors")
        print("      → Check ALL areas - no black should remain")
        print()
        print("🔍 Look for these specific issues:")
        print("   • Frames that don't change color")
        print("   • Nested widgets that are missed")
        print("   • Scrollbars that aren't themed")
        print("   • Canvas backgrounds")
        print("   • Menu colors")
        print("   • Any 'stuck' colors when toggling")
        print()

        self.root.mainloop()


if __name__ == "__main__":
    test = RobustThemeTest()
    test.run()
