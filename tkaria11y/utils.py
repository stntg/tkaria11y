# tkaria11y/utils.py

"""
Utility functions:
- configure_focus_traversal: Tab/Shift-Tab wrapping
"""

import tkinter as tk
from typing import Any, Callable


def configure_focus_traversal(root: tk.Tk) -> None:
    widgets = root.winfo_children()
    for i, w in enumerate(widgets):
        next_w = widgets[(i + 1) % len(widgets)]
        prev_w = widgets[(i - 1) % len(widgets)]

        def make_tab_handler(
            next_widget: tk.Widget,
        ) -> Callable[[tk.Event[Any]], str]:
            def handler(event: tk.Event[Any]) -> str:
                next_widget.focus_set()
                return "break"
            return handler

        def make_shift_tab_handler(
            prev_widget: tk.Widget,
        ) -> Callable[[tk.Event[Any]], str]:
            def handler(event: tk.Event[Any]) -> str:
                prev_widget.focus_set()
                return "break"
            return handler

        w.bind("<Tab>", make_tab_handler(next_w))
        w.bind("<Shift-Tab>", make_shift_tab_handler(prev_w))
