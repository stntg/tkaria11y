#!/usr/bin/env python3
"""
Simple form example BEFORE migration.
Shows various tkinter widgets that need accessibility improvements.
"""

import tkinter as tk


def create_form():
    """Create and return a user registration form with standard tkinter widgets."""
    main_window = tk.Tk()
    main_window.title("User Registration Form")
    main_window.geometry("400x500")

    # Title
    tk.Label(main_window, text="User Registration", font=("Arial", 16, "bold")).pack(
        pady=10
    )

    # Main form frame
    form_frame = tk.Frame(main_window)
    form_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Name field
    tk.Label(form_frame, text="Full Name:").pack(anchor="w", pady=(10, 0))
    tk.Entry(form_frame, width=40).pack(fill="x", pady=(0, 10))

    # Email field
    tk.Label(form_frame, text="Email Address:").pack(anchor="w")
    tk.Entry(form_frame, width=40).pack(fill="x", pady=(0, 10))

    # Age field
    tk.Label(form_frame, text="Age:").pack(anchor="w")
    tk.Entry(form_frame, width=10).pack(anchor="w", pady=(0, 10))

    # Gender selection
    tk.Label(form_frame, text="Gender:").pack(anchor="w")
    gender_frame = tk.Frame(form_frame)
    gender_frame.pack(anchor="w", pady=(0, 10))

    gender_var = tk.StringVar(value="male")
    tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="male").pack(
        side="left"
    )
    tk.Radiobutton(
        gender_frame, text="Female", variable=gender_var, value="female"
    ).pack(side="left", padx=(10, 0))
    tk.Radiobutton(gender_frame, text="Other", variable=gender_var, value="other").pack(
        side="left", padx=(10, 0)
    )

    # Interests checkboxes
    tk.Label(form_frame, text="Interests:").pack(anchor="w", pady=(10, 0))
    interests_frame = tk.Frame(form_frame)
    interests_frame.pack(anchor="w", pady=(0, 10))

    # Create interest checkboxes with variables
    for interest, var in [
        ("Sports", tk.BooleanVar()),
        ("Music", tk.BooleanVar()),
        ("Reading", tk.BooleanVar()),
    ]:
        tk.Checkbutton(interests_frame, text=interest, variable=var).pack(anchor="w")

    # Experience level
    tk.Label(form_frame, text="Experience Level:").pack(anchor="w", pady=(10, 0))
    tk.Scale(form_frame, from_=1, to=10, orient="horizontal").pack(
        fill="x", pady=(0, 10)
    )

    # Country selection
    tk.Label(form_frame, text="Country:").pack(anchor="w")
    country_listbox = tk.Listbox(form_frame, height=4)
    for country in ["USA", "Canada", "UK", "Germany", "France", "Japan", "Australia"]:
        country_listbox.insert(tk.END, country)
    country_listbox.pack(fill="x", pady=(0, 10))

    # Buttons
    button_frame = tk.Frame(form_frame)
    button_frame.pack(fill="x", pady=20)

    for text, color_config in [
        ("Submit", {"bg": "green", "fg": "white"}),
        ("Reset", {"bg": "orange"}),
        ("Cancel", {"bg": "red", "fg": "white"}),
    ]:
        tk.Button(button_frame, text=text, **color_config).pack(
            side="left", padx=(0, 10)
        )

    return main_window


if __name__ == "__main__":
    root = create_form()
    root.mainloop()
