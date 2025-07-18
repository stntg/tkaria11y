#!/usr/bin/env python3
"""
Example tkinter application BEFORE migration to tkaria11y.
This shows a typical tkinter app that needs accessibility improvements.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class SimpleCalculatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Calculator")
        self.root.geometry("300x400")

        # Variables
        self.result_var = tk.StringVar()
        self.result_var.set("0")

        self.setup_ui()

    def setup_ui(self):
        # Result display
        result_frame = tk.Frame(self.root)
        result_frame.pack(fill="x", padx=10, pady=10)

        result_label = tk.Label(result_frame, text="Result:")
        result_label.pack(anchor="w")

        self.result_entry = tk.Entry(
            result_frame,
            textvariable=self.result_var,
            state="readonly",
            font=("Arial", 14),
        )
        self.result_entry.pack(fill="x", pady=5)

        # Input section
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Enter number:").pack(anchor="w")
        self.number_entry = tk.Entry(input_frame)
        self.number_entry.pack(fill="x", pady=5)

        # Operation buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Row 1
        row1 = tk.Frame(button_frame)
        row1.pack(fill="x", pady=2)

        tk.Button(row1, text="Add", command=lambda: self.calculate("add")).pack(
            side="left", fill="x", expand=True, padx=2
        )
        tk.Button(
            row1, text="Subtract", command=lambda: self.calculate("subtract")
        ).pack(side="left", fill="x", expand=True, padx=2)

        # Row 2
        row2 = tk.Frame(button_frame)
        row2.pack(fill="x", pady=2)

        tk.Button(
            row2, text="Multiply", command=lambda: self.calculate("multiply")
        ).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(row2, text="Divide", command=lambda: self.calculate("divide")).pack(
            side="left", fill="x", expand=True, padx=2
        )

        # Row 3
        row3 = tk.Frame(button_frame)
        row3.pack(fill="x", pady=2)

        tk.Button(row3, text="Clear", command=self.clear).pack(
            side="left", fill="x", expand=True, padx=2
        )
        tk.Button(row3, text="Exit", command=self.root.quit).pack(
            side="left", fill="x", expand=True, padx=2
        )

        # Status bar
        self.status_label = tk.Label(
            self.root, text="Ready", relief="sunken", anchor="w"
        )
        self.status_label.pack(side="bottom", fill="x")

    def calculate(self, operation):
        try:
            current_result = float(self.result_var.get())
            new_number = float(self.number_entry.get())

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
        self.result_var.set("0")
        self.number_entry.delete(0, tk.END)
        self.status_label.config(text="Cleared")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SimpleCalculatorApp()
    app.run()
