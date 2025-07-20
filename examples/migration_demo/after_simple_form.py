#!/usr/bin/env python3
"""
Simple form example BEFORE migration.
Shows various tkinter widgets that need accessibility improvements.
"""

import tkinter as tk
from tkaria11y.widgets import (
    AccessibleEntry,
    AccessibleScale,
    AccessibleButton,
    AccessibleRadiobutton,
    AccessibleFrame,
    AccessibleCheckbutton,
    AccessibleLabel,
    AccessibleListbox,
)


def create_form():
    """Create and return a user registration form with accessible widgets."""
    main_window = tk.Tk()
    main_window.title("User Registration Form")
    main_window.geometry("400x500")

    # Title
    AccessibleLabel(
        main_window,
        accessible_name="User Registration",
        text="User Registration",
        font=("Arial", 16, "bold"),
    ).pack(pady=10)

    # Main form frame
    form_frame = AccessibleFrame(main_window)
    form_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Name field
    AccessibleLabel(form_frame, accessible_name="Full Name:", text="Full Name:").pack(
        anchor="w", pady=(10, 0)
    )
    AccessibleEntry(form_frame, width=40).pack(fill="x", pady=(0, 10))

    # Email field
    AccessibleLabel(
        form_frame, accessible_name="Email Address:", text="Email Address:"
    ).pack(anchor="w")
    AccessibleEntry(form_frame, width=40).pack(fill="x", pady=(0, 10))

    # Age field
    AccessibleLabel(form_frame, accessible_name="Age:", text="Age:").pack(anchor="w")
    AccessibleEntry(form_frame, width=10).pack(anchor="w", pady=(0, 10))

    # Gender selection
    AccessibleLabel(form_frame, accessible_name="Gender:", text="Gender:").pack(
        anchor="w"
    )
    gender_frame = AccessibleFrame(form_frame)
    gender_frame.pack(anchor="w", pady=(0, 10))

    gender_var = tk.StringVar(value="male")
    AccessibleRadiobutton(
        gender_frame,
        accessible_name="Male",
        text="Male",
        variable=gender_var,
        value="male",
    ).pack(side="left")
    AccessibleRadiobutton(
        gender_frame,
        accessible_name="Female",
        text="Female",
        variable=gender_var,
        value="female",
    ).pack(side="left", padx=(10, 0))
    AccessibleRadiobutton(
        gender_frame,
        accessible_name="Other",
        text="Other",
        variable=gender_var,
        value="other",
    ).pack(side="left", padx=(10, 0))

    # Interests checkboxes
    AccessibleLabel(form_frame, accessible_name="Interests:", text="Interests:").pack(
        anchor="w", pady=(10, 0)
    )
    interests_frame = AccessibleFrame(form_frame)
    interests_frame.pack(anchor="w", pady=(0, 10))

    # Create interest checkboxes with variables
    for interest, var in [
        ("Sports", tk.BooleanVar()),
        ("Music", tk.BooleanVar()),
        ("Reading", tk.BooleanVar()),
    ]:
        AccessibleCheckbutton(
            interests_frame, accessible_name=interest, text=interest, variable=var
        ).pack(anchor="w")

    # Experience level
    AccessibleLabel(
        form_frame, accessible_name="Experience Level:", text="Experience Level:"
    ).pack(anchor="w", pady=(10, 0))
    AccessibleScale(form_frame, from_=1, to=10, orient="horizontal").pack(
        fill="x", pady=(0, 10)
    )

    # Country selection
    AccessibleLabel(form_frame, accessible_name="Country:", text="Country:").pack(
        anchor="w"
    )
    country_listbox = AccessibleListbox(form_frame, height=4)
    for country in ["USA", "Canada", "UK", "Germany", "France", "Japan", "Australia"]:
        country_listbox.insert(tk.END, country)
    country_listbox.pack(fill="x", pady=(0, 10))

    # Buttons
    button_frame = AccessibleFrame(form_frame)
    button_frame.pack(fill="x", pady=20)

    for text, color_config in [
        ("Submit", {"bg": "green", "fg": "white"}),
        ("Reset", {"bg": "orange"}),
        ("Cancel", {"bg": "red", "fg": "white"}),
    ]:
        AccessibleButton(
            button_frame, accessible_name=text, text=text, **color_config
        ).pack(side="left", padx=(0, 10))

    return main_window


if __name__ == "__main__":
    root = create_form()
    root.mainloop()
