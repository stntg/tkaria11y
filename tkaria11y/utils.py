# tkaria11y/utils.py

"""
Utility functions:
- configure_focus_traversal: Tab/Shift-Tab wrapping
"""

import tkinter as tk
from typing import Any


def configure_focus_traversal(root: tk.Tk) -> None:
    widgets = root.winfo_children()
    for i, w in enumerate(widgets):
        next_w = widgets[(i + 1) % len(widgets)]
        prev_w = widgets[(i - 1) % len(widgets)]
        w.bind("<Tab>", lambda e, nxt=next_w: (nxt.focus_set(), "break")[1]
              )  # type: ignore[misc]
        w.bind("<Shift-Tab>", lambda e, prv=prev_w: (prv.focus_set(), 
                                                     "break")[1]
              )  # type: ignore[misc]
