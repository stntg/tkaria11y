#!/usr/bin/env python3
"""
Simple demo to show what the inspector displays.
Press F2 to toggle the inspector window.
"""

from tkaria11y import AccessibleApp
from tkaria11y.widgets import (
    AccessibleButton,
    AccessibleEntry,
    AccessibleLabel,
    AccessibleFrame,
)


def main():
    # Create app with inspector enabled
    app = AccessibleApp(title="Inspector Demo", enable_inspector=True)

    # Create a simple form
    main_frame = AccessibleFrame(app, accessible_name="Main form container")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    title = AccessibleLabel(
        main_frame,
        text="Inspector Demo",
        accessible_name="Page title",
        font=("Arial", 16, "bold"),
    )
    title.pack(pady=(0, 20))

    name_label = AccessibleLabel(
        main_frame, text="Name:", accessible_name="Name field label"
    )
    name_label.pack(anchor="w")

    name_entry = AccessibleEntry(
        main_frame,
        accessible_name="Name input field",
        accessible_description="Enter your full name",
    )
    name_entry.pack(fill="x", pady=(0, 10))

    submit_btn = AccessibleButton(
        main_frame,
        text="Submit",
        accessible_name="Submit button",
        accessible_description="Click to submit the form",
    )
    submit_btn.pack()

    instructions = AccessibleLabel(
        main_frame,
        text="Press F2 to toggle inspector\nTab to navigate between controls",
        accessible_name="Usage instructions",
        justify="center",
        fg="blue",
    )
    instructions.pack(pady=(20, 0))

    print("Inspector Demo started!")
    print("\nWhat the inspector should show:")
    print("- AccessibleApp (root window)")
    print('  - AccessibleFrame [region] "Main form container"')
    print('    - AccessibleLabel [label] "Page title"')
    print('    - AccessibleLabel [label] "Name field label"')
    print('    - AccessibleEntry [textbox] "Name input field"')
    print('    - AccessibleButton [button] "Submit button"')
    print('    - AccessibleLabel [label] "Usage instructions"')
    print("\nPress F2 to open inspector and verify this structure!")

    # Focus the entry field
    name_entry.focus_set()

    app.mainloop()


if __name__ == "__main__":
    main()
