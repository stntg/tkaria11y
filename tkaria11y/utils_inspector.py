# tkaria11y/utils_inspector.py

"""
Runtime Widget Inspector:
Shows widget tree, metadata, and highlights focused widget.
"""

import tkinter as tk
from tkinter import ttk


def launch_inspector(root: tk.Tk) -> tk.Toplevel:
    insp = tk.Toplevel(root)
    insp.title("A11y Inspector")
    insp.geometry("300x400")

    tree = ttk.Treeview(insp)
    tree.pack(fill="both", expand=True)
    tree.heading("#0", text='Widget Tree [role] "accessible_name"')

    def populate(parent: str, widget: tk.Misc) -> None:
        # Skip the inspector window itself to avoid confusion
        if widget == insp:
            return

        role = getattr(widget, "accessible_role", "")
        name = getattr(widget, "accessible_name", "")

        # Format the display text more clearly
        if role and name:
            label = f'{widget.__class__.__name__} [{role}] "{name}"'
        elif role:
            label = f"{widget.__class__.__name__} [{role}]"
        elif name:
            label = f'{widget.__class__.__name__} "{name}"'
        else:
            label = f"{widget.__class__.__name__}"

        wid = tree.insert(parent, "end", text=label, iid=str(id(widget)))
        for child in widget.winfo_children():
            populate(wid, child)

    def refresh_tree() -> None:
        """Refresh the widget tree"""
        tree.delete(*tree.get_children())
        populate("", root)

    # Schedule initial population with a small delay to ensure widgets are created
    def initial_populate() -> None:
        refresh_tree()
        # Also expand the root node by default
        if tree.get_children():
            tree.item(tree.get_children()[0], open=True)

    root.after(100, initial_populate)  # 100ms delay should be enough

    # Add refresh button
    refresh_btn = tk.Button(insp, text="Refresh", command=refresh_tree)
    refresh_btn.pack(side="bottom", pady=5)

    highlight = tk.Canvas(root, bd=0, highlightthickness=2, highlightbackground="red")

    def on_focus(e: tk.Event) -> None:
        try:
            w = e.widget
            # Check if highlight canvas still exists
            if not highlight.winfo_exists():
                return

            highlight.place_forget()
            x, y = w.winfo_rootx(), w.winfo_rooty()
            w_, h_ = w.winfo_width(), w.winfo_height()
            highlight.place(x=x, y=y, width=w_, height=h_)

            # Only try to select if the tree still exists and the item exists in it
            try:
                if tree.winfo_exists():
                    item_id = str(id(w))
                    if tree.exists(item_id):
                        tree.selection_set(item_id)
                        tree.see(item_id)
            except tk.TclError:
                # Tree or item no longer exists, ignore
                pass
        except (tk.TclError, AttributeError):
            # Widget destroyed or other error, ignore
            pass

    # Store the callback reference for cleanup
    focus_callback = on_focus

    def cleanup() -> None:
        """Clean up bindings when inspector is destroyed"""
        try:
            root.unbind_all("<FocusIn>")
            highlight.destroy()
        except (tk.TclError, AttributeError):
            pass

    # Bind cleanup to inspector destruction
    def on_close() -> None:
        cleanup()
        insp.destroy()

    insp.protocol("WM_DELETE_WINDOW", on_close)

    root.bind_all("<FocusIn>", focus_callback, add="+")
    root.bind_all(
        "<F2>",
        lambda e: insp.deiconify() if not insp.winfo_viewable() else insp.withdraw(),
    )

    return insp


""" Integrating this inspector you would typically do the following, in the AccessibleApp constructor:

from .utils_inspector import launch_inspector

class AccessibleApp(tk.Tk):
    def __init__(self, *args, enable_inspector=False, **kw):
        super().__init__(*args, **kw)
        if enable_inspector:
            launch_inspector(self)

usage:

    app = AccessibleApp(enable_inspector=True)
    # Press F2 to show/hide the inspector.

TODO:
1. Hook generate_stubs.py into your pyproject.toml or CI pipeline
2. Refine the inspector: add an editable panel to tweak accessible_* attributes on the fly
3. Extend highlighting to include hover events (<Enter>) and custom style guides
4. Write tests to ensure your stub generator and inspector cover all _WIDGET_MAP entries

With automated stubs and a live inspector, your framework is as ergonomic to develop against as it is potent for end-users.

"""
