# tkaria11y/widgets.py

"""
Comprehensive accessible widget implementations for Tkinter, TTK, and CustomTkinter.
Provides full WCAG 2.1 compliance with ARIA roles, properties, and platform integration.
"""

import tkinter as tk
import tkinter.ttk as ttk
from typing import Dict, Tuple, Type, Optional, List
from .mixins import AccessibleMixin
from .aria_compliance import get_default_role

# Try to import CustomTkinter if available
try:
    import customtkinter as ctk

    CUSTOMTKINTER_AVAILABLE = True
except ImportError:
    CUSTOMTKINTER_AVAILABLE = False

    # Create dummy classes for type hints
    class ctk:
        class CTkButton:
            pass

        class CTkEntry:
            pass

        class CTkLabel:
            pass

        class CTkCheckBox:
            pass

        class CTkRadioButton:
            pass

        class CTkSlider:
            pass

        class CTkScrollbar:
            pass

        class CTkFrame:
            pass

        class CTkTabview:
            pass

        class CTkProgressBar:
            pass

        class CTkSwitch:
            pass

        class CTkComboBox:
            pass

        class CTkTextbox:
            pass

        class CTkScrollableFrame:
            pass

        class CTkToplevel:
            pass


# Complete widget mapping for all supported widget types
_WIDGET_MAP: Dict[str, Tuple[str, Type[tk.Widget]]] = {
    # Standard Tkinter widgets
    "Button": ("button", tk.Button),
    "Entry": ("textbox", tk.Entry),
    "Label": ("none", tk.Label),  # Labels are typically presentational
    "Text": ("textbox", tk.Text),
    "Checkbutton": ("checkbox", tk.Checkbutton),
    "Radiobutton": ("radio", tk.Radiobutton),
    "Scale": ("slider", tk.Scale),
    "Scrollbar": ("scrollbar", tk.Scrollbar),
    "Listbox": ("listbox", tk.Listbox),
    "Menu": ("menu", tk.Menu),
    "Menubutton": ("button", tk.Menubutton),
    "Frame": ("group", tk.Frame),
    "LabelFrame": ("group", tk.LabelFrame),
    "Toplevel": ("dialog", tk.Toplevel),
    "Canvas": ("img", tk.Canvas),
    "Message": ("none", tk.Message),
    "Spinbox": ("spinbutton", tk.Spinbox),
    "PanedWindow": ("group", tk.PanedWindow),
    # TTK widgets
    "TTKButton": ("button", ttk.Button),
    "TTKEntry": ("textbox", ttk.Entry),
    "TTKLabel": ("none", ttk.Label),
    "TTKCheckbutton": ("checkbox", ttk.Checkbutton),
    "TTKRadiobutton": ("radio", ttk.Radiobutton),
    "TTKScale": ("slider", ttk.Scale),
    "TTKScrollbar": ("scrollbar", ttk.Scrollbar),
    "TTKFrame": ("group", ttk.Frame),
    "TTKLabelFrame": ("group", ttk.LabelFrame),
    "TTKNotebook": ("tablist", ttk.Notebook),
    "TTKProgressbar": ("progressbar", ttk.Progressbar),
    "TTKSeparator": ("separator", ttk.Separator),
    "TTKSizegrip": ("none", ttk.Sizegrip),
    "TTKTreeview": ("tree", ttk.Treeview),
    "TTKCombobox": ("combobox", ttk.Combobox),
    "TTKSpinbox": ("spinbutton", ttk.Spinbox),
    "TTKPanedWindow": ("group", ttk.PanedWindow),
}

# Add CustomTkinter widgets if available
if CUSTOMTKINTER_AVAILABLE:
    _WIDGET_MAP.update(
        {
            "CTKButton": ("button", ctk.CTkButton),
            "CTKEntry": ("textbox", ctk.CTkEntry),
            "CTKLabel": ("none", ctk.CTkLabel),
            "CTKCheckBox": ("checkbox", ctk.CTkCheckBox),
            "CTKRadioButton": ("radio", ctk.CTkRadioButton),
            "CTKSlider": ("slider", ctk.CTkSlider),
            "CTKScrollbar": ("scrollbar", ctk.CTkScrollbar),
            "CTKFrame": ("group", ctk.CTkFrame),
            "CTKTabview": ("tablist", ctk.CTkTabview),
            "CTKProgressBar": ("progressbar", ctk.CTkProgressBar),
            "CTKSwitch": ("switch", ctk.CTkSwitch),
            "CTKComboBox": ("combobox", ctk.CTkComboBox),
            "CTKTextbox": ("textbox", ctk.CTkTextbox),
            "CTKScrollableFrame": ("group", ctk.CTkScrollableFrame),
            "CTKToplevel": ("dialog", ctk.CTkToplevel),
        }
    )

__all__ = []

# Create accessible widget classes dynamically
for name, (role, base) in _WIDGET_MAP.items():
    cls_name = f"Accessible{name}"

    # Create a closure to capture the role variable
    def make_init(widget_role: str, base_class: Type[tk.Widget]):
        def __init__(self, master=None, *, accessible_name: str = "", **kw):
            # Use user-provided accessible_role if present, otherwise use default
            role = kw.pop("accessible_role", widget_role)

            # Validate accessible_name for certain widgets
            if widget_role in ["button", "checkbox", "radio"] and not accessible_name:
                # Try to get text from widget configuration
                text = kw.get("text", "")
                if text:
                    accessible_name = text
                elif widget_role == "button":
                    raise ValueError(
                        f"accessible_name is required for {widget_role} widgets"
                    )

            super(self.__class__, self).__init__(
                master,
                accessible_name=accessible_name,
                accessible_role=role,
                **kw,
            )

        return __init__

    # Create the accessible widget class
    Wrapper = type(
        cls_name, (AccessibleMixin, base), {"__init__": make_init(role, base)}
    )

    globals()[cls_name] = Wrapper
    __all__.append(cls_name)


# Specialized accessible widgets with enhanced functionality
class AccessibleNotebook(AccessibleMixin, ttk.Notebook):
    """Accessible Notebook with tab navigation and announcements"""

    def __init__(self, master=None, *, accessible_name: str = "Notebook", **kw):
        role = kw.pop("accessible_role", "tablist")
        super().__init__(
            master,
            accessible_name=accessible_name,
            accessible_role=role,
            **kw,
        )

        # Bind tab selection events
        self.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        # Set up keyboard navigation
        self.bind("<Left>", self._previous_tab)
        self.bind("<Right>", self._next_tab)
        self.bind("<Home>", self._first_tab)
        self.bind("<End>", self._last_tab)

    def _on_tab_changed(self, event):
        """Handle tab change events"""
        current_tab = self.select()
        if current_tab:
            tab_text = self.tab(current_tab, "text")
            from .a11y_engine import speak

            speak(f"Selected tab: {tab_text}")

    def _previous_tab(self, event):
        """Navigate to previous tab"""
        current = self.index(self.select())
        if current > 0:
            self.select(current - 1)
        return "break"

    def _next_tab(self, event):
        """Navigate to next tab"""
        current = self.index(self.select())
        if current < self.index("end") - 1:
            self.select(current + 1)
        return "break"

    def _first_tab(self, event):
        """Navigate to first tab"""
        if self.index("end") > 0:
            self.select(0)
        return "break"

    def _last_tab(self, event):
        """Navigate to last tab"""
        last_index = self.index("end") - 1
        if last_index >= 0:
            self.select(last_index)
        return "break"


class AccessibleTreeview(AccessibleMixin, ttk.Treeview):
    """Accessible Treeview with enhanced keyboard navigation"""

    def __init__(self, master=None, *, accessible_name: str = "Tree", **kw):
        role = kw.pop("accessible_role", "tree")
        super().__init__(
            master,
            accessible_name=accessible_name,
            accessible_role=role,
            **kw,
        )

        # Bind selection events
        self.bind("<<TreeviewSelect>>", self._on_selection_changed)
        self.bind("<<TreeviewOpen>>", self._on_item_opened)
        self.bind("<<TreeviewClose>>", self._on_item_closed)

        # Enhanced keyboard navigation
        self.bind("<Return>", self._activate_item)
        self.bind("<space>", self._toggle_item)
        self.bind("<Left>", self._collapse_or_parent)
        self.bind("<Right>", self._expand_or_child)
        self.bind("<Home>", self._first_item)
        self.bind("<End>", self._last_item)

    def _on_selection_changed(self, event):
        """Handle selection change events"""
        selection = self.selection()
        if selection:
            item = selection[0]
            text = self.item(item, "text")
            values = self.item(item, "values")

            # Announce item with context
            announcement = f"Selected: {text}"
            if values:
                announcement += f", {', '.join(str(v) for v in values)}"

            from .a11y_engine import speak

            speak(announcement)

    def _on_item_opened(self, event):
        """Handle item open events"""
        from .a11y_engine import speak

        speak("Expanded")

    def _on_item_closed(self, event):
        """Handle item close events"""
        from .a11y_engine import speak

        speak("Collapsed")

    def _activate_item(self, event):
        """Activate selected item"""
        selection = self.selection()
        if selection:
            item = selection[0]
            if self.get_children(item):
                # Toggle expansion for items with children
                if self.item(item, "open"):
                    self.item(item, open=False)
                else:
                    self.item(item, open=True)
        return "break"

    def _toggle_item(self, event):
        """Toggle item expansion"""
        return self._activate_item(event)

    def _collapse_or_parent(self, event):
        """Collapse item or move to parent"""
        selection = self.selection()
        if selection:
            item = selection[0]
            if self.item(item, "open") and self.get_children(item):
                # Collapse if expanded
                self.item(item, open=False)
            else:
                # Move to parent
                parent = self.parent(item)
                if parent:
                    self.selection_set(parent)
                    self.focus(parent)
        return "break"

    def _expand_or_child(self, event):
        """Expand item or move to first child"""
        selection = self.selection()
        if selection:
            item = selection[0]
            children = self.get_children(item)
            if children:
                if not self.item(item, "open"):
                    # Expand if collapsed
                    self.item(item, open=True)
                else:
                    # Move to first child
                    self.selection_set(children[0])
                    self.focus(children[0])
        return "break"

    def _first_item(self, event):
        """Move to first item"""
        children = self.get_children()
        if children:
            self.selection_set(children[0])
            self.focus(children[0])
        return "break"

    def _last_item(self, event):
        """Move to last visible item"""

        def get_last_visible(item):
            children = self.get_children(item)
            if children and self.item(item, "open"):
                return get_last_visible(children[-1])
            return item

        children = self.get_children()
        if children:
            last_item = get_last_visible(children[-1])
            self.selection_set(last_item)
            self.focus(last_item)
        return "break"


class AccessibleCombobox(AccessibleMixin, ttk.Combobox):
    """Accessible Combobox with enhanced announcements"""

    def __init__(self, master=None, *, accessible_name: str = "Combobox", **kw):
        role = kw.pop("accessible_role", "combobox")
        super().__init__(
            master,
            accessible_name=accessible_name,
            accessible_role=role,
            **kw,
        )

        # Bind events
        self.bind("<<ComboboxSelected>>", self._on_selection_changed)
        self.bind("<KeyPress>", self._on_key_press)

        # Set ARIA properties
        self._set_aria_properties()

    def _set_aria_properties(self):
        """Set ARIA properties for combobox"""
        from .platform_adapter import set_accessible_state

        set_accessible_state(self, "expanded", False)
        set_accessible_state(self, "haspopup", True)

    def _on_selection_changed(self, event):
        """Handle selection change events"""
        current_value = self.get()
        from .a11y_engine import speak

        speak(f"Selected: {current_value}")

    def _on_key_press(self, event):
        """Handle key press events for announcements"""
        if event.keysym in ["Up", "Down"]:
            # Announce current value after arrow key navigation
            self.after(10, self._announce_current_value)

    def _announce_current_value(self):
        """Announce current value"""
        current_value = self.get()
        if current_value:
            from .a11y_engine import speak

            speak(current_value)


# Add specialized widgets to __all__
__all__.extend(["AccessibleNotebook", "AccessibleTreeview", "AccessibleCombobox"])


# Widget validation and enhancement functions
def validate_widget_accessibility(widget: tk.Widget) -> List[str]:
    """Validate accessibility compliance of a widget"""
    from .aria_compliance import validate_aria_compliance, ARIAProperty

    errors = []

    # Check if widget has accessible name
    if hasattr(widget, "accessible_name"):
        if not widget.accessible_name:
            widget_class = widget.winfo_class()
            if widget_class in ["Button", "Checkbutton", "Radiobutton"]:
                errors.append("Interactive widget missing accessible_name")
    else:
        errors.append("Widget missing AccessibleMixin")

    # Check ARIA compliance if widget has ARIA properties
    if hasattr(widget, "accessible_role"):
        role = get_default_role(widget)
        properties = {}

        # Collect ARIA properties
        if hasattr(widget, "accessible_name") and widget.accessible_name:
            properties[ARIAProperty.LABEL] = widget.accessible_name

        if hasattr(widget, "accessible_description") and widget.accessible_description:
            properties[ARIAProperty.DESCRIBEDBY] = widget.accessible_description

        # Validate ARIA compliance
        aria_errors = validate_aria_compliance(widget, role, properties)
        errors.extend(aria_errors)

    return errors


def enhance_widget_accessibility(
    widget: tk.Widget,
    accessible_name: Optional[str] = None,
    accessible_description: Optional[str] = None,
    accessible_role: Optional[str] = None,
) -> None:
    """Enhance accessibility of an existing widget"""
    from .platform_adapter import (
        set_accessible_name,
        set_accessible_description,
        set_accessible_role,
    )

    # Set platform-specific accessibility properties
    if accessible_name:
        set_accessible_name(widget, accessible_name)

    if accessible_description:
        set_accessible_description(widget, accessible_description)

    if accessible_role:
        set_accessible_role(widget, accessible_role)

    # Add focus event for TTS
    if accessible_name:

        def speak_on_focus(event):
            from .a11y_engine import speak

            announcement = accessible_name
            if accessible_description:
                announcement += f", {accessible_description}"
            speak(announcement)

        widget.bind("<FocusIn>", speak_on_focus, add="+")


def create_accessible_widget(widget_type: str, master=None, **kwargs) -> tk.Widget:
    """Factory function to create accessible widgets"""
    accessible_name = kwargs.pop("accessible_name", "")

    # Map widget type to accessible class
    class_name = f"Accessible{widget_type}"

    if class_name in globals():
        widget_class = globals()[class_name]
        return widget_class(master, accessible_name=accessible_name, **kwargs)
    else:
        raise ValueError(f"Unknown accessible widget type: {widget_type}")


# Utility functions for widget discovery and enhancement
def discover_widgets(root: tk.Widget) -> List[tk.Widget]:
    """Discover all widgets in a widget hierarchy"""
    widgets = []

    def _collect_widgets(widget):
        widgets.append(widget)
        try:
            for child in widget.winfo_children():
                _collect_widgets(child)
        except tk.TclError:
            # Widget was destroyed
            pass

    _collect_widgets(root)
    return widgets


def enhance_existing_widgets(root: tk.Widget) -> None:
    """Enhance accessibility of existing widgets in a hierarchy"""
    widgets = discover_widgets(root)

    for widget in widgets:
        # Skip if already accessible
        if hasattr(widget, "accessible_name"):
            continue

        # Get default role and name
        role = get_default_role(widget)
        name = ""

        # Try to get name from widget text
        try:
            text = widget.cget("text")
            if text:
                name = text
        except tk.TclError:
            pass

        # Enhance widget if it needs accessibility
        if role.value != "none" and name:
            enhance_widget_accessibility(widget, name, role=role.value)


# Import CustomTkinter accessible widgets from dedicated module
try:
    # Import enhanced CTK widgets (wrappers with better functionality)
    from .ctk_wrappers import AccessibleCTKButton, AccessibleCTKEntry, CTK_AVAILABLE

    # Import remaining CTK widgets from old system
    from .ctk_widgets import (
        AccessibleCTKFrame,
        AccessibleCTKLabel,
        AccessibleCTKCheckBox,
        AccessibleCTKRadioButton,
        AccessibleCTKSlider,
        AccessibleCTKTabview,
        AccessibleCTKScrollableFrame,
    )

    # Add CTK widgets to __all__
    if CTK_AVAILABLE:
        __all__.extend(
            [
                "AccessibleCTKFrame",
                "AccessibleCTKButton",
                "AccessibleCTKEntry",
                "AccessibleCTKLabel",
                "AccessibleCTKCheckBox",
                "AccessibleCTKRadioButton",
                "AccessibleCTKSlider",
                "AccessibleCTKTabview",
                "AccessibleCTKScrollableFrame",
            ]
        )

except ImportError:
    # CTK widgets not available
    CTK_AVAILABLE = False
