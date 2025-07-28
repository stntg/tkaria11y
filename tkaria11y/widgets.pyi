# tkaria11y/widgets.pyi
# Type stubs for tkaria11y widgets module

from typing import Any, Dict, List, Optional, Union, Callable, Tuple
import tkinter as tk
from tkinter import ttk

# Base accessible widget mixin
class AccessibleMixin:
    accessible_name: Optional[str]
    accessible_description: Optional[str]
    accessible_role: Optional[str]
    accessible_value: Optional[str]
    live_region: Optional[str]

    def __init__(
        self,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...
    def get_accessibility_info(self) -> Dict[str, Any]: ...
    def set_accessible_name(self, name: str) -> None: ...
    def set_accessible_description(self, description: str) -> None: ...
    def set_accessible_role(self, role: str) -> None: ...
    def set_accessible_value(self, value: str) -> None: ...
    def set_live_region(self, live_region: str) -> None: ...
    def announce_to_screen_reader(self, message: str, priority: str = ...) -> None: ...
    def update_accessibility_state(self) -> None: ...

# Standard Tkinter accessible widgets
class AccessibleButton(AccessibleMixin, tk.Button):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleEntry(AccessibleMixin, tk.Entry):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleText(AccessibleMixin, tk.Text):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleLabel(AccessibleMixin, tk.Label):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleCheckbutton(AccessibleMixin, tk.Checkbutton):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleRadiobutton(AccessibleMixin, tk.Radiobutton):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleScale(AccessibleMixin, tk.Scale):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleListbox(AccessibleMixin, tk.Listbox):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleFrame(AccessibleMixin, tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleLabelFrame(AccessibleMixin, tk.LabelFrame):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleCanvas(AccessibleMixin, tk.Canvas):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleScrollbar(AccessibleMixin, tk.Scrollbar):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleMenu(AccessibleMixin, tk.Menu):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleMenubutton(AccessibleMixin, tk.Menubutton):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleOptionMenu(AccessibleMixin, tk.OptionMenu):
    def __init__(
        self,
        parent: tk.Widget,
        variable: tk.Variable,
        value: str,
        *values: str,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleSpinbox(AccessibleMixin, tk.Spinbox):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessiblePanedWindow(AccessibleMixin, tk.PanedWindow):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleToplevel(AccessibleMixin, tk.Toplevel):
    def __init__(
        self,
        parent: Optional[tk.Widget] = ...,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

# TTK accessible widgets
class AccessibleTTKButton(AccessibleMixin, ttk.Button):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKEntry(AccessibleMixin, ttk.Entry):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKLabel(AccessibleMixin, ttk.Label):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKCheckbutton(AccessibleMixin, ttk.Checkbutton):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKRadiobutton(AccessibleMixin, ttk.Radiobutton):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKScale(AccessibleMixin, ttk.Scale):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...
    def identify(self, x: int, y: int) -> str: ...  # type: ignore[override]

class AccessibleTTKFrame(AccessibleMixin, ttk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKLabelFrame(AccessibleMixin, ttk.LabelFrame):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleNotebook(AccessibleMixin, ttk.Notebook):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKNotebook(AccessibleMixin, ttk.Notebook):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleCombobox(AccessibleMixin, ttk.Combobox):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKCombobox(AccessibleMixin, ttk.Combobox):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTreeview(AccessibleMixin, ttk.Treeview):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKProgressbar(AccessibleMixin, ttk.Progressbar):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKSeparator(AccessibleMixin, ttk.Separator):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKSizegrip(AccessibleMixin, ttk.Sizegrip):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKSpinbox(AccessibleMixin, ttk.Spinbox):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleTTKPanedWindow(AccessibleMixin, ttk.PanedWindow):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        accessible_value: Optional[str] = ...,
        live_region: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...

# Specialized accessible widgets
class AccessibleDialog(AccessibleToplevel):
    def __init__(
        self,
        parent: Optional[tk.Widget] = ...,
        title: str = ...,
        modal: bool = ...,
        *,
        accessible_name: Optional[str] = ...,
        accessible_description: Optional[str] = ...,
        accessible_role: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...
    def show(self) -> Any: ...
    def destroy(self) -> None: ...

class AccessibleMessageBox(AccessibleDialog):
    def __init__(
        self,
        parent: Optional[tk.Widget] = ...,
        title: str = ...,
        message: str = ...,
        message_type: str = ...,
        buttons: List[str] = ...,
        default_button: int = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleFileDialog(AccessibleDialog):
    def __init__(
        self,
        parent: Optional[tk.Widget] = ...,
        title: str = ...,
        initialdir: str = ...,
        filetypes: List[Tuple[str, str]] = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleColorChooser(AccessibleDialog):
    def __init__(
        self,
        parent: Optional[tk.Widget] = ...,
        title: str = ...,
        initialcolor: str = ...,
        **kwargs: Any
    ) -> None: ...

class AccessibleFontChooser(AccessibleDialog):
    def __init__(
        self,
        parent: Optional[tk.Widget] = ...,
        title: str = ...,
        initialfont: Tuple[str, int, str] = ...,
        **kwargs: Any
    ) -> None: ...

# Utility functions for widget creation
def create_accessible_widget(
    widget_class: type,
    parent: tk.Widget,
    accessible_name: str,
    accessible_description: Optional[str] = ...,
    accessible_role: Optional[str] = ...,
    **kwargs: Any
) -> tk.Widget: ...
def enhance_widget_accessibility(
    widget: tk.Widget,
    accessible_name: str,
    accessible_description: Optional[str] = ...,
    accessible_role: Optional[str] = ...,
) -> None: ...
def get_widget_accessibility_info(widget: tk.Widget) -> Dict[str, Any]: ...
def validate_widget_accessibility(widget: tk.Widget) -> List[str]: ...
def auto_generate_accessible_name(widget: tk.Widget) -> str: ...
def auto_generate_accessible_description(widget: tk.Widget) -> str: ...
def auto_detect_widget_role(widget: tk.Widget) -> str: ...

# Widget factory functions
def accessible_button(
    parent: tk.Widget, text: str, accessible_name: Optional[str] = ..., **kwargs: Any
) -> AccessibleButton: ...
def accessible_entry(
    parent: tk.Widget, accessible_name: str, **kwargs: Any
) -> AccessibleEntry: ...
def accessible_label(
    parent: tk.Widget, text: str, accessible_name: Optional[str] = ..., **kwargs: Any
) -> AccessibleLabel: ...
def accessible_checkbutton(
    parent: tk.Widget, text: str, accessible_name: Optional[str] = ..., **kwargs: Any
) -> AccessibleCheckbutton: ...
def accessible_radiobutton(
    parent: tk.Widget, text: str, accessible_name: Optional[str] = ..., **kwargs: Any
) -> AccessibleRadiobutton: ...
def accessible_scale(
    parent: tk.Widget, accessible_name: str, **kwargs: Any
) -> AccessibleScale: ...
def accessible_listbox(
    parent: tk.Widget, accessible_name: str, **kwargs: Any
) -> AccessibleListbox: ...
def accessible_frame(
    parent: tk.Widget, accessible_name: Optional[str] = ..., **kwargs: Any
) -> AccessibleFrame: ...

# Constants
WIDGET_ROLE_MAPPING: Dict[str, str]
DEFAULT_ACCESSIBLE_ROLES: Dict[type, str]
ARIA_PROPERTIES: List[str]
WCAG_GUIDELINES: Dict[str, str]

__all__: List[str]
