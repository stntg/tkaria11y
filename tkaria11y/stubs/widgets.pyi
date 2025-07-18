import tkinter as tk

__all__ = [
    "AccessibleButton",
    "AccessibleEntry",
    "AccessibleLabel",
    "AccessibleCheckbutton",
    "AccessibleRadiobutton",
    "AccessibleScale",
    "AccessibleListbox",
    "AccessibleFrame",
]

class AccessibleButton(tk.Button):
    def __init__(self, master=None, *, accessible_name: str = "", **kw) -> None: ...

    accessible_name: str
    accessible_role: str
    accessible_description: str

class AccessibleEntry(tk.Entry):
    def __init__(self, master=None, *, accessible_name: str = "", **kw) -> None: ...

    accessible_name: str
    accessible_role: str
    accessible_description: str

class AccessibleLabel(tk.Label):
    def __init__(self, master=None, *, accessible_name: str = "", **kw) -> None: ...

    accessible_name: str
    accessible_role: str
    accessible_description: str

class AccessibleCheckbutton(tk.Checkbutton):
    def __init__(self, master=None, *, accessible_name: str = "", **kw) -> None: ...

    accessible_name: str
    accessible_role: str
    accessible_description: str

class AccessibleRadiobutton(tk.Radiobutton):
    def __init__(self, master=None, *, accessible_name: str = "", **kw) -> None: ...

    accessible_name: str
    accessible_role: str
    accessible_description: str

class AccessibleScale(tk.Scale):
    def __init__(self, master=None, *, accessible_name: str = "", **kw) -> None: ...

    accessible_name: str
    accessible_role: str
    accessible_description: str

class AccessibleListbox(tk.Listbox):
    def __init__(self, master=None, *, accessible_name: str = "", **kw) -> None: ...

    accessible_name: str
    accessible_role: str
    accessible_description: str

class AccessibleFrame(tk.Frame):
    def __init__(self, master=None, *, accessible_name: str = "", **kw) -> None: ...

    accessible_name: str
    accessible_role: str
    accessible_description: str
