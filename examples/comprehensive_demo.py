# examples/comprehensive_demo.py

"""
Comprehensive demo showcasing all tkaria11y features:
- All available accessible widgets
- High contrast theme
- Dyslexic font support
- Runtime inspector
- TTS announcements
- Keyboard navigation
"""

from tkaria11y import AccessibleApp, speak
from tkaria11y.widgets import (
    AccessibleButton,
    AccessibleEntry,
    AccessibleLabel,
    AccessibleCheckbutton,
    AccessibleRadiobutton,
    AccessibleScale,
    AccessibleListbox,
    AccessibleFrame,
)
from tkaria11y.themes import HighContrastTheme
import tkinter as tk


def main():
    # Create accessible app with all features
    app = AccessibleApp(
        title="tkaria11y Comprehensive Demo",
        high_contrast=True,
        dyslexic_font=True,
        enable_inspector=True,
        scaling=1.1,
    )

    # Main container
    main_frame = AccessibleFrame(
        app, accessible_name="Main application frame", padx=20, pady=20
    )
    main_frame.pack(fill="both", expand=True)

    # Title
    title = AccessibleLabel(
        main_frame,
        text="tkaria11y Feature Demo",
        accessible_name="Application title: tkaria11y Feature Demo",
        font=("Arial", 18, "bold"),
    )
    title.pack(pady=(0, 20))

    # Instructions
    instructions = AccessibleLabel(
        main_frame,
        text="This demo showcases accessibility features.\nPress F2 to toggle inspector, Tab to navigate.",
        accessible_name="Instructions: This demo showcases accessibility features. Press F2 to toggle inspector, Tab to navigate.",
        justify="center",
    )
    instructions.pack(pady=(0, 20))

    # Form section
    form_frame = AccessibleFrame(
        main_frame,
        accessible_name="Form section",
        relief="groove",
        bd=2,
        padx=15,
        pady=15,
    )
    form_frame.pack(fill="x", pady=(0, 20))

    # Name field
    name_label = AccessibleLabel(
        form_frame, text="Name:", accessible_name="Name field label"
    )
    name_label.pack(anchor="w")

    name_entry = AccessibleEntry(
        form_frame,
        accessible_name="Name input field",
        accessible_description="Enter your full name here",
        width=30,
    )
    name_entry.pack(anchor="w", pady=(0, 10))

    # Email field
    email_label = AccessibleLabel(
        form_frame, text="Email:", accessible_name="Email field label"
    )
    email_label.pack(anchor="w")

    email_entry = AccessibleEntry(
        form_frame,
        accessible_name="Email input field",
        accessible_description="Enter your email address",
        width=30,
    )
    email_entry.pack(anchor="w", pady=(0, 10))

    # Checkboxes
    checkbox_frame = AccessibleFrame(form_frame, accessible_name="Preferences section")
    checkbox_frame.pack(anchor="w", pady=(0, 10))

    newsletter_var = tk.BooleanVar()
    newsletter_cb = AccessibleCheckbutton(
        checkbox_frame,
        text="Subscribe to newsletter",
        variable=newsletter_var,
        accessible_name="Subscribe to newsletter checkbox",
        accessible_description="Check to receive our newsletter",
    )
    newsletter_cb.pack(anchor="w")

    updates_var = tk.BooleanVar()
    updates_cb = AccessibleCheckbutton(
        checkbox_frame,
        text="Receive product updates",
        variable=updates_var,
        accessible_name="Receive product updates checkbox",
    )
    updates_cb.pack(anchor="w")

    # Radio buttons
    radio_frame = AccessibleFrame(
        form_frame, accessible_name="Contact preference section"
    )
    radio_frame.pack(anchor="w", pady=(0, 10))

    contact_label = AccessibleLabel(
        radio_frame,
        text="Preferred contact method:",
        accessible_name="Contact preference label",
    )
    contact_label.pack(anchor="w")

    contact_var = tk.StringVar(value="email")

    email_radio = AccessibleRadiobutton(
        radio_frame,
        text="Email",
        variable=contact_var,
        value="email",
        accessible_name="Email contact preference",
    )
    email_radio.pack(anchor="w")

    phone_radio = AccessibleRadiobutton(
        radio_frame,
        text="Phone",
        variable=contact_var,
        value="phone",
        accessible_name="Phone contact preference",
    )
    phone_radio.pack(anchor="w")

    # Scale widget
    scale_frame = AccessibleFrame(form_frame, accessible_name="Rating section")
    scale_frame.pack(anchor="w", pady=(0, 10))

    scale_label = AccessibleLabel(
        scale_frame,
        text="Rate our service (1-10):",
        accessible_name="Service rating label",
    )
    scale_label.pack(anchor="w")

    rating_scale = AccessibleScale(
        scale_frame,
        from_=1,
        to=10,
        orient="horizontal",
        accessible_name="Service rating slider",
        accessible_description="Use arrow keys or drag to select rating from 1 to 10",
    )
    rating_scale.pack(anchor="w")

    # Controls section
    controls_frame = AccessibleFrame(main_frame, accessible_name="Controls section")
    controls_frame.pack(fill="x", pady=(0, 20))

    # Buttons
    button_frame = AccessibleFrame(controls_frame, accessible_name="Action buttons")
    button_frame.pack()

    def submit_form():
        name = name_entry.get()
        email = email_entry.get()
        newsletter = newsletter_var.get()
        updates = updates_var.get()
        contact_pref = contact_var.get()
        rating = rating_scale.get()

        message = f"Form submitted! Name: {name}, Email: {email}, Newsletter: {newsletter}, Updates: {updates}, Contact: {contact_pref}, Rating: {rating}"
        print(message)
        speak("Form submitted successfully!")
        result_label.config(text="Form submitted successfully!")

    def clear_form():
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        newsletter_var.set(False)
        updates_var.set(False)
        contact_var.set("email")
        rating_scale.set(5)
        result_label.config(text="Form cleared")
        speak("Form cleared")

    def toggle_theme():
        HighContrastTheme.apply(app)
        speak("High contrast theme applied")

    submit_btn = AccessibleButton(
        button_frame,
        text="Submit",
        command=submit_form,
        accessible_name="Submit form button",
        accessible_description="Click to submit the form data",
        bg="green",
        fg="white",
    )
    submit_btn.pack(side="left", padx=(0, 10))

    clear_btn = AccessibleButton(
        button_frame,
        text="Clear",
        command=clear_form,
        accessible_name="Clear form button",
        accessible_description="Click to clear all form fields",
    )
    clear_btn.pack(side="left", padx=(0, 10))

    theme_btn = AccessibleButton(
        button_frame,
        text="Apply Theme",
        command=toggle_theme,
        accessible_name="Apply high contrast theme button",
        accessible_description="Click to apply high contrast theme",
    )
    theme_btn.pack(side="left")

    # Result display
    result_label = AccessibleLabel(
        main_frame,
        text="Ready to use. Press Tab to navigate between controls.",
        accessible_name="Status message",
        fg="blue",
    )
    result_label.pack(pady=(20, 0))

    # Listbox example
    list_frame = AccessibleFrame(main_frame, accessible_name="Example list section")
    list_frame.pack(fill="x", pady=(20, 0))

    list_label = AccessibleLabel(
        list_frame, text="Example items:", accessible_name="Example items list label"
    )
    list_label.pack(anchor="w")

    example_listbox = AccessibleListbox(
        list_frame,
        accessible_name="Example items list",
        accessible_description="List of example items, use arrow keys to navigate",
        height=4,
    )
    example_listbox.pack(anchor="w", fill="x")

    # Populate listbox
    items = [
        "Accessibility Feature 1",
        "Screen Reader Support",
        "Keyboard Navigation",
        "High Contrast Theme",
        "TTS Announcements",
    ]
    for item in items:
        example_listbox.insert(tk.END, item)

    # Set initial focus
    name_entry.focus_set()

    print("Comprehensive demo started!")
    print("Features demonstrated:")
    print("- All accessible widget types")
    print("- High contrast theme")
    print("- Dyslexic font support")
    print("- TTS announcements on focus")
    print("- Keyboard navigation (Tab/Shift-Tab)")
    print("- Runtime inspector (F2)")
    print("- ARIA-style metadata")

    app.mainloop()


if __name__ == "__main__":
    main()
