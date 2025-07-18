#!/usr/bin/env python3
"""
Simple form example BEFORE migration.
Shows various tkinter widgets that need accessibility improvements.
"""

import tkinter as tk
from tkinter import ttk
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
    root = tk.Tk()
    root.title("User Registration Form")
    root.geometry("400x500")

    # Title
    title_label = AccessibleLabel(
        root,
        accessible_name="User Registration",
        text="User Registration",
        font=("Arial", 16, "bold"),
    )
    title_label.pack(pady=10)

    # Main form frame
    form_frame = AccessibleFrame(root)
    form_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Name field
    AccessibleLabel(form_frame, accessible_name="Full Name:", text="Full Name:").pack(
        anchor="w", pady=(10, 0)
    )
    name_entry = AccessibleEntry(form_frame, width=40)
    name_entry.pack(fill="x", pady=(0, 10))

    # Email field
    AccessibleLabel(
        form_frame, accessible_name="Email Address:", text="Email Address:"
    ).pack(anchor="w")
    email_entry = AccessibleEntry(form_frame, width=40)
    email_entry.pack(fill="x", pady=(0, 10))

    # Age field
    AccessibleLabel(form_frame, accessible_name="Age:", text="Age:").pack(anchor="w")
    age_entry = AccessibleEntry(form_frame, width=10)
    age_entry.pack(anchor="w", pady=(0, 10))

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

    sports_var = tk.BooleanVar()
    music_var = tk.BooleanVar()
    reading_var = tk.BooleanVar()

    AccessibleCheckbutton(
        interests_frame, accessible_name="Sports", text="Sports", variable=sports_var
    ).pack(anchor="w")
    AccessibleCheckbutton(
        interests_frame, accessible_name="Music", text="Music", variable=music_var
    ).pack(anchor="w")
    AccessibleCheckbutton(
        interests_frame, accessible_name="Reading", text="Reading", variable=reading_var
    ).pack(anchor="w")

    # Experience level
    AccessibleLabel(
        form_frame, accessible_name="Experience Level:", text="Experience Level:"
    ).pack(anchor="w", pady=(10, 0))
    experience_scale = AccessibleScale(form_frame, from_=1, to=10, orient="horizontal")
    experience_scale.pack(fill="x", pady=(0, 10))

    # Country selection
    AccessibleLabel(form_frame, accessible_name="Country:", text="Country:").pack(
        anchor="w"
    )
    countries = ["USA", "Canada", "UK", "Germany", "France", "Japan", "Australia"]
    country_listbox = AccessibleListbox(form_frame, height=4)
    for country in countries:
        country_listbox.insert(tk.END, country)
    country_listbox.pack(fill="x", pady=(0, 10))

    # Buttons
    button_frame = AccessibleFrame(form_frame)
    button_frame.pack(fill="x", pady=20)

    AccessibleButton(
        button_frame, accessible_name="Submit", text="Submit", bg="green", fg="white"
    ).pack(side="left", padx=(0, 10))
    AccessibleButton(
        button_frame, accessible_name="Reset", text="Reset", bg="orange"
    ).pack(side="left", padx=(0, 10))
    AccessibleButton(
        button_frame, accessible_name="Cancel", text="Cancel", bg="red", fg="white"
    ).pack(side="left")

    return root


if __name__ == "__main__":
    root = create_form()
    root.mainloop()
