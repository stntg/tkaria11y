# examples/minimal_app.py

"""
Minimal example demonstrating tkaria11y accessibility features.

Features demonstrated:
- AccessibleApp with high contrast and dyslexic font
- AccessibleEntry and AccessibleButton with accessible names
- Runtime inspector (press F2)
- Text-to-speech announcements on focus
"""

from tkaria11y import AccessibleApp
from tkaria11y.widgets import AccessibleButton, AccessibleEntry, AccessibleLabel


def main():
    # Create accessible app with accessibility features enabled
    app = AccessibleApp(
        title="tkaria11y Demo",
        high_contrast=True,
        dyslexic_font=True,
        enable_inspector=True,
    )

    # Add a title label
    title = AccessibleLabel(
        app,
        text="Welcome to tkaria11y Demo",
        accessible_name="Application title",
        font=("Arial", 16, "bold"),
    )
    title.pack(pady=10)

    # Add instructions
    instructions = AccessibleLabel(
        app,
        text="Enter your name below and click Greet.\nPress F2 to toggle accessibility inspector.",
        accessible_name="Instructions: Enter your name below and click Greet. Press F2 to toggle accessibility inspector.",
        justify="center",
    )
    instructions.pack(pady=5)

    # Name input field
    entry = AccessibleEntry(
        app,
        accessible_name="Name input field",
        accessible_description="Enter your name here",
        width=30,
    )
    entry.pack(padx=10, pady=5)
    entry.focus_set()  # Set initial focus

    # Greeting button
    def greet():
        name = entry.get().strip()
        if name:
            print(f"Hello, {name}!")
            # You could also use TTS here: speak(f"Hello, {name}!")
        else:
            print("Please enter your name first.")

    btn = AccessibleButton(
        app,
        text="Greet",
        accessible_name="Greet button",
        accessible_description="Click to display greeting",
        command=greet,
    )
    btn.pack(padx=10, pady=10)

    # Status label
    status = AccessibleLabel(
        app,
        text="Ready. Press Tab to navigate between controls.",
        accessible_name="Status: Ready. Press Tab to navigate between controls.",
        fg="gray",
    )
    status.pack(pady=5)

    print("Demo started. Try the following:")
    print("- Tab/Shift-Tab to navigate between controls")
    print("- Focus events will trigger TTS announcements")
    print("- Press F2 to toggle the accessibility inspector")
    print("- High contrast theme and dyslexic font are enabled")

    app.mainloop()


if __name__ == "__main__":
    main()
