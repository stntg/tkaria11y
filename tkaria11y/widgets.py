# tkaria11y/widgets.py

"""
Key Points:
You get AccessibleButton, AccessibleEntry, etc., in tka11y.widgets.
Developers simply from tka11y.widgets import AccessibleButton
This file defines accessible versions of common Tkinter widgets.
The mapping is defined by a dictionary at the top of this module.

Dynamic factory: create Accessible<Button/Entry/...> classes
based on _WIDGET_MAP.
"""

import tkinter as tk
from .mixins import AccessibleMixin

_WIDGET_MAP = {
    "Button": ("button", tk.Button),
    "Entry": ("textbox", tk.Entry),
    "Label": ("label", tk.Label),
    "Checkbutton": ("checkbox", tk.Checkbutton),
    "Radiobutton": ("radio", tk.Radiobutton),
    "Scale": ("slider", tk.Scale),
    "Listbox": ("listbox", tk.Listbox),
    "Frame": ("region", tk.Frame),
}

__all__ = []

for name, (role, base) in _WIDGET_MAP.items():
    cls_name = f"Accessible{name}"

    # Create a closure to capture the role variable
    def make_init(widget_role):
        def __init__(self, master=None, *, accessible_name="", **kw):
            super(self.__class__, self).__init__(
                master,
                accessible_name=accessible_name,
                accessible_role=widget_role,
                **kw,
            )

        return __init__

    Wrapper = type(cls_name, (AccessibleMixin, base), {"__init__": make_init(role)})
    globals()[cls_name] = Wrapper
    __all__.append(cls_name)
