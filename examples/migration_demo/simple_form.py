#!/usr/bin/env python3
"""
Simple form example BEFORE migration.
Shows various tkinter widgets that need accessibility improvements.
"""

import tkinter as tk
from tkinter import ttk


def create_form():
    root = tk.Tk()
    root.title("User Registration Form")
    root.geometry("400x500")

    # Title
    title_label = tk.Label(root, text="User Registration", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Main form frame
    form_frame = tk.Frame(root)
    form_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Name field
    tk.Label(form_frame, text="Full Name:").pack(anchor="w", pady=(10, 0))
    name_entry = tk.Entry(form_frame, width=40)
    name_entry.pack(fill="x", pady=(0, 10))

    # Email field
    tk.Label(form_frame, text="Email Address:").pack(anchor="w")
    email_entry = tk.Entry(form_frame, width=40)
    email_entry.pack(fill="x", pady=(0, 10))

    # Age field
    tk.Label(form_frame, text="Age:").pack(anchor="w")
    age_entry = tk.Entry(form_frame, width=10)
    age_entry.pack(anchor="w", pady=(0, 10))

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

    sports_var = tk.BooleanVar()
    music_var = tk.BooleanVar()
    reading_var = tk.BooleanVar()

    tk.Checkbutton(interests_frame, text="Sports", variable=sports_var).pack(anchor="w")
    tk.Checkbutton(interests_frame, text="Music", variable=music_var).pack(anchor="w")
    tk.Checkbutton(interests_frame, text="Reading", variable=reading_var).pack(
        anchor="w"
    )

    # Experience level
    tk.Label(form_frame, text="Experience Level:").pack(anchor="w", pady=(10, 0))
    experience_scale = tk.Scale(form_frame, from_=1, to=10, orient="horizontal")
    experience_scale.pack(fill="x", pady=(0, 10))

    # Country selection
    tk.Label(form_frame, text="Country:").pack(anchor="w")
    countries = ["USA", "Canada", "UK", "Germany", "France", "Japan", "Australia"]
    country_listbox = tk.Listbox(form_frame, height=4)
    for country in countries:
        country_listbox.insert(tk.END, country)
    country_listbox.pack(fill="x", pady=(0, 10))

    # Buttons
    button_frame = tk.Frame(form_frame)
    button_frame.pack(fill="x", pady=20)

    tk.Button(button_frame, text="Submit", bg="green", fg="white").pack(
        side="left", padx=(0, 10)
    )
    tk.Button(button_frame, text="Reset", bg="orange").pack(side="left", padx=(0, 10))
    tk.Button(button_frame, text="Cancel", bg="red", fg="white").pack(side="left")

    return root


if __name__ == "__main__":
    root = create_form()
    root.mainloop()
