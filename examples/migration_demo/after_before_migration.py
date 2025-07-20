#!/usr/bin/env python3
"""
Example tkinter application BEFORE migration to tkaria11y.
This shows a typical tkinter app that needs accessibility improvements.
"""

import tkinter as tk
from tkinter import messagebox
from tkaria11y.widgets import (
    AccessibleButton,
    AccessibleLabel,
    AccessibleFrame,
    AccessibleEntry,
)


class SimpleCalculatorApp:
    """Simple calculator application using accessible tkaria11y widgets."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Calculator")
        self.root.geometry("300x400")

        # Variables
        self.result_var = tk.StringVar()
        self.result_var.set("0")

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface with accessible widgets."""
        # Result display
        result_frame = AccessibleFrame(self.root)
        result_frame.pack(fill="x", padx=10, pady=10)

        result_label = AccessibleLabel(
            result_frame, accessible_name="Result:", text="Result:"
        )
        result_label.pack(anchor="w")

        self.result_entry = AccessibleEntry(
            result_frame,
            textvariable=self.result_var,
            state="readonly",
            font=("Arial", 14),
        )
        self.result_entry.pack(fill="x", pady=5)

        # Input section
        input_frame = AccessibleFrame(self.root)
        input_frame.pack(fill="x", padx=10, pady=5)

        AccessibleLabel(
            input_frame, accessible_name="Enter number:", text="Enter number:"
        ).pack(anchor="w")
        self.number_entry = AccessibleEntry(input_frame)
        self.number_entry.pack(fill="x", pady=5)

        # Operation buttons
        button_frame = AccessibleFrame(self.root)
        button_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Row 1
        row1 = AccessibleFrame(button_frame)
        row1.pack(fill="x", pady=2)

        AccessibleButton(
            row1,
            accessible_name="Add",
            text="Add",
            command=lambda: self.calculate("add"),
        ).pack(side="left", fill="x", expand=True, padx=2)
        AccessibleButton(
            row1,
            accessible_name="Subtract",
            text="Subtract",
            command=lambda: self.calculate("subtract"),
        ).pack(side="left", fill="x", expand=True, padx=2)

        # Row 2
        row2 = AccessibleFrame(button_frame)
        row2.pack(fill="x", pady=2)

        AccessibleButton(
            row2,
            accessible_name="Multiply",
            text="Multiply",
            command=lambda: self.calculate("multiply"),
        ).pack(side="left", fill="x", expand=True, padx=2)
        AccessibleButton(
            row2,
            accessible_name="Divide",
            text="Divide",
            command=lambda: self.calculate("divide"),
        ).pack(side="left", fill="x", expand=True, padx=2)

        # Row 3
        row3 = AccessibleFrame(button_frame)
        row3.pack(fill="x", pady=2)

        AccessibleButton(
            row3, accessible_name="Clear", text="Clear", command=self.clear
        ).pack(side="left", fill="x", expand=True, padx=2)
        AccessibleButton(
            row3, accessible_name="Exit", text="Exit", command=self.root.quit
        ).pack(side="left", fill="x", expand=True, padx=2)

        # Status bar
        self.status_label = AccessibleLabel(
            self.root,
            accessible_name="Ready",
            text="Ready",
            relief="sunken",
            anchor="w",
        )
        self.status_label.pack(side="bottom", fill="x")

    def calculate(self, operation):
        """Perform calculation based on the given operation."""
        try:
            current_result = float(self.result_var.get())
            new_number = float(self.number_entry.get())

            result = 0  # Initialize result variable
            if operation == "add":
                result = current_result + new_number
            elif operation == "subtract":
                result = current_result - new_number
            elif operation == "multiply":
                result = current_result * new_number
            elif operation == "divide":
                if new_number == 0:
                    messagebox.showerror("Error", "Cannot divide by zero!")
                    return
                result = current_result / new_number

            self.result_var.set(str(result))
            self.number_entry.delete(0, tk.END)
            self.status_label.config(text=f"Performed {operation}")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            self.status_label.config(text="Error: Invalid input")

    def clear(self):
        """Clear the calculator display and input."""
        self.result_var.set("0")
        self.number_entry.delete(0, tk.END)
        self.status_label.config(text="Cleared")

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = SimpleCalculatorApp()
    app.run()
