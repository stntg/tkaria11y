#!/usr/bin/env python3
"""
Complete demonstration of tkaria11y migration tool.
This script shows the before/after comparison and runs both versions.
"""

import sys
import tkinter as tk
from pathlib import Path

# Add the parent directory to the path so we can import tkaria11y
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from tkaria11y.widgets import (
        AccessibleLabel,
        AccessibleEntry,
        AccessibleButton,
        AccessibleFrame,
    )

    TKARIA11Y_AVAILABLE = True
except ImportError:
    TKARIA11Y_AVAILABLE = False


def show_before_after_comparison():
    """Show a side-by-side comparison of the migration results"""

    print("🔄 tkaria11y Migration Tool - Complete Demo")
    print("=" * 60)

    print("\n📋 What the migration tool does:")
    print("   • Converts standard tkinter widgets to accessible versions")
    print("   • Adds screen reader support")
    print("   • Enables text-to-speech announcements")
    print("   • Preserves all existing functionality")
    print("   • Adds proper accessibility attributes")

    print("\n🔍 Example Transformation:")
    print("-" * 30)

    print("BEFORE (Standard tkinter):")
    print("```python")
    print("import tkinter as tk")
    print("")
    print("root = tk.Tk()")
    print("label = tk.Label(root, text='Hello World')")
    print("entry = tk.Entry(root)")
    print("button = tk.Button(root, text='Click Me')")
    print("```")

    print("\nAFTER (Accessible tkinter):")
    print("```python")
    print("import tkinter as tk")
    print(
        "from tkaria11y.widgets import AccessibleLabel, AccessibleEntry, AccessibleButton"
    )
    print("")
    print("root = tk.Tk()")
    print(
        "label = AccessibleLabel(root, accessible_name='Hello World', text='Hello World')"
    )
    print("entry = AccessibleEntry(root, accessible_name='Input field')")
    print(
        "button = AccessibleButton(root, accessible_name='Click Me', text='Click Me')"
    )
    print("```")

    print("\n✨ Benefits after migration:")
    print("   ✅ Screen readers can identify all controls")
    print("   ✅ Widgets announce themselves when focused")
    print("   ✅ Better keyboard navigation")
    print("   ✅ Follows accessibility standards")
    print("   ✅ No functionality changes - everything works the same!")

    print("\n🚀 How to use the migration tool:")
    print("   # Migrate a single file:")
    print("   python -m tkaria11y.scripts.migrate myapp.py")
    print("")
    print("   # Migrate entire directory:")
    print("   python -m tkaria11y.scripts.migrate ./my_project/")
    print("")
    print("   # Interactive mode (review each change):")
    print("   python -m tkaria11y.scripts.migrate myapp.py --interactive")


def create_original_app():
    """Original tkinter app"""
    root = tk.Tk()
    root.title("Original App (No Accessibility)")
    root.geometry("300x200")

    tk.Label(root, text="This is the ORIGINAL app", font=("Arial", 12, "bold")).pack(
        pady=10
    )
    tk.Label(root, text="Name:").pack(anchor="w", padx=20)
    tk.Entry(root, width=30).pack(pady=5)

    tk.Label(root, text="Message:").pack(anchor="w", padx=20)
    tk.Entry(root, width=30).pack(pady=5)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Submit", bg="green", fg="white").pack(
        side="left", padx=5
    )
    tk.Button(button_frame, text="Clear", bg="orange").pack(side="left", padx=5)
    tk.Button(
        button_frame, text="Close", bg="red", fg="white", command=root.destroy
    ).pack(side="left", padx=5)

    return root


def create_accessible_app():
    """Migrated accessible app"""
    if not TKARIA11Y_AVAILABLE:
        print(
            "❌ Could not import tkaria11y widgets. Make sure the package is installed."
        )
        return None

    root = tk.Tk()
    root.title("Accessible App (After Migration)")
    root.geometry("300x200")

    AccessibleLabel(
        root,
        accessible_name="This is the ACCESSIBLE app",
        text="This is the ACCESSIBLE app",
        font=("Arial", 12, "bold"),
    ).pack(pady=10)
    AccessibleLabel(root, accessible_name="Name:", text="Name:").pack(
        anchor="w", padx=20
    )
    AccessibleEntry(root, accessible_name="Name input field", width=30).pack(pady=5)

    AccessibleLabel(root, accessible_name="Message:", text="Message:").pack(
        anchor="w", padx=20
    )
    AccessibleEntry(root, accessible_name="Message input field", width=30).pack(pady=5)

    button_frame = AccessibleFrame(root, accessible_name="Button controls")
    button_frame.pack(pady=20)

    AccessibleButton(
        button_frame,
        accessible_name="Submit",
        text="Submit",
        bg="green",
        fg="white",
    ).pack(side="left", padx=5)
    AccessibleButton(
        button_frame, accessible_name="Clear", text="Clear", bg="orange"
    ).pack(side="left", padx=5)
    AccessibleButton(
        button_frame,
        accessible_name="Close",
        text="Close",
        bg="red",
        fg="white",
        command=root.destroy,
    ).pack(side="left", padx=5)

    return root


def run_demo_choice(choice):
    """Handle the demo choice execution"""
    if choice == "1":
        print("🚀 Running original app...")
        app = create_original_app()
        if app:
            app.mainloop()

    elif choice == "2":
        print("🚀 Running accessible app...")
        app = create_accessible_app()
        if app:
            print("💡 Try using Tab to navigate between controls!")
            print("💡 If you have a screen reader, it will announce each control!")
            app.mainloop()

    elif choice == "3":
        print("🚀 Running both apps...")
        original = create_original_app()
        accessible = create_accessible_app()

        if original and accessible:
            # Position windows side by side
            original.geometry("300x200+100+100")
            accessible.geometry("300x200+450+100")

            print(
                "💡 Compare the two apps - they look identical but the right one is accessible!"
            )
            print("💡 Try using Tab to navigate in both windows!")

            # Run both
            original.mainloop()

    elif choice == "4":
        print("👋 Demo skipped.")

    else:
        print("❌ Invalid choice.")


def create_demo_apps():
    """Create both original and migrated versions for comparison"""
    print("\n🎮 Demo Applications")
    print("=" * 30)

    print("Choose which demo to run:")
    print("1. Original tkinter app (no accessibility)")
    print("2. Migrated accessible app")
    print("3. Both apps side by side")
    print("4. Skip demo")

    choice = input("\nEnter your choice (1-4): ").strip()
    run_demo_choice(choice)


def main():
    """Main demonstration function"""
    show_before_after_comparison()

    if (
        input("\n🎮 Would you like to see the demo apps? (y/n): ")
        .lower()
        .startswith("y")
    ):
        create_demo_apps()

    print("\n📚 For more information, check out:")
    print("   • README.md - Complete documentation")
    print("   • migration_example.md - Detailed examples")
    print(
        "   • before_migration.py vs after_before_migration.py - Real migration results"
    )

    print("\n🎉 Thanks for trying tkaria11y!")
    print("Making tkinter applications accessible for everyone! 🌟")


if __name__ == "__main__":
    main()
