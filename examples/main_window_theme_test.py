#!/usr/bin/env python3
"""
Test to specifically demonstrate that the main window/frame gets properly themed.
This is crucial for accessibility - the entire application background should be high contrast.
"""

import sys
from pathlib import Path
import tkinter as tk

# Add the parent directory to the path so we can import tkaria11y
sys.path.insert(0, str(Path(__file__).parent.parent))

from tkaria11y.themes import HighContrastTheme


class MainWindowThemeTest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Window Theme Test")
        self.root.geometry("600x500")

        # Set initial background to make the difference obvious
        self.root.configure(bg="lightgray")

        self.theme_applied = False
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI to test main window theming"""

        # Title
        title_label = tk.Label(
            self.root,
            text="Main Window Theme Test",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="black",
            pady=10,
        )
        title_label.pack(fill="x", padx=10, pady=10)

        # Explanation
        explanation = tk.Label(
            self.root,
            text="This test shows that the MAIN WINDOW background gets themed for accessibility.\n"
            "Look at the gray areas around the widgets - they should turn black when themed.",
            font=("Arial", 11),
            bg="white",
            fg="black",
            justify="left",
            wraplength=550,
        )
        explanation.pack(fill="x", padx=10, pady=5)

        # Control button
        self.theme_btn = tk.Button(
            self.root,
            text="Apply High Contrast Theme",
            command=self.toggle_theme,
            font=("Arial", 12, "bold"),
            bg="lightblue",
            fg="black",
            pady=5,
        )
        self.theme_btn.pack(pady=20)

        # Create some content with spacing to show main window background
        content_frame = tk.Frame(self.root, bg="white", relief="raised", bd=2)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            content_frame,
            text="Content Area",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black",
        ).pack(pady=10)

        # Form elements
        form_frame = tk.Frame(content_frame, bg="white")
        form_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(form_frame, text="Name:", bg="white", fg="black").pack(anchor="w")
        self.name_entry = tk.Entry(form_frame, width=30, font=("Arial", 11))
        self.name_entry.pack(anchor="w", pady=2)

        tk.Label(form_frame, text="Email:", bg="white", fg="black").pack(
            anchor="w", pady=(10, 0)
        )
        self.email_entry = tk.Entry(form_frame, width=30, font=("Arial", 11))
        self.email_entry.pack(anchor="w", pady=2)

        # Buttons
        button_frame = tk.Frame(content_frame, bg="white")
        button_frame.pack(pady=20)

        tk.Button(
            button_frame, text="Submit", bg="green", fg="white", font=("Arial", 10)
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame, text="Cancel", bg="red", fg="white", font=("Arial", 10)
        ).pack(side="left", padx=5)

        # Status area at bottom
        self.status_frame = tk.Frame(self.root, bg="lightgray", relief="sunken", bd=1)
        self.status_frame.pack(fill="x", side="bottom")

        self.status_label = tk.Label(
            self.status_frame,
            text="Status: Normal theme - Notice the gray background around widgets",
            font=("Arial", 10),
            bg="lightgray",
            fg="black",
            anchor="w",
            padx=10,
            pady=5,
        )
        self.status_label.pack(fill="x")

        # Instructions
        instructions = tk.Label(
            self.root,
            text="👀 LOOK FOR: The gray areas around widgets should turn BLACK when themed.\n"
            "This ensures the entire application has consistent high contrast colors.",
            font=("Arial", 10, "italic"),
            bg="lightyellow",
            fg="darkblue",
            justify="center",
            pady=5,
        )
        instructions.pack(fill="x", padx=10, pady=5, side="bottom")

    def toggle_theme(self):
        """Toggle the high contrast theme"""
        if not self.theme_applied:
            print("🎨 Applying High Contrast Theme to ENTIRE APPLICATION...")
            print("👀 Watch the main window background change from gray to black!")

            HighContrastTheme.apply(self.root)

            self.theme_btn.config(text="Remove High Contrast Theme")
            self.status_label.config(
                text="Status: HIGH CONTRAST theme - Main window background is now BLACK"
            )
            self.theme_applied = True

            print("✅ Theme applied!")
            print("🔍 Key accessibility improvements:")
            print("   • Main window background: gray → BLACK")
            print("   • All widget backgrounds: various → BLACK")
            print("   • All text: various → WHITE")
            print("   • Selection highlights: default → YELLOW")
            print("   • Entire application has consistent high contrast!")

        else:
            print("🔄 Removing High Contrast Theme...")
            print("👀 Watch everything return to normal colors!")

            HighContrastTheme.remove(self.root)

            self.theme_btn.config(text="Apply High Contrast Theme")
            self.status_label.config(
                text="Status: Normal theme - Back to original colors"
            )
            self.theme_applied = False

            print("✅ Theme removed!")
            print("🔍 Everything should be back to normal colors")

    def run(self):
        """Run the test"""
        print("🚀 Main Window Theme Test")
        print("=" * 50)
        print()
        print("This test specifically demonstrates that the HIGH CONTRAST THEME")
        print("applies to the MAIN WINDOW BACKGROUND for proper accessibility.")
        print()
        print("🎯 What to look for:")
        print("   • BEFORE: Gray background around widgets")
        print("   • AFTER: BLACK background around widgets")
        print("   • This ensures the entire app has consistent high contrast")
        print()
        print("🔍 Why this matters for accessibility:")
        print("   • Users with visual impairments need consistent high contrast")
        print("   • The main window background is part of the visual interface")
        print("   • Partial theming creates confusing mixed contrast levels")
        print("   • Complete theming provides a unified accessible experience")
        print()
        print("📋 Instructions:")
        print("   1. Notice the current gray background around widgets")
        print("   2. Click 'Apply High Contrast Theme'")
        print("   3. See how the ENTIRE window becomes black with white text")
        print("   4. This is proper accessibility theming!")
        print()

        self.root.mainloop()


if __name__ == "__main__":
    test = MainWindowThemeTest()
    test.run()
