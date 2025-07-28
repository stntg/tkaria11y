# tkaria11y.mixins.pyi
# Type stubs for tkaria11y.mixins

from typing import Any, Dict, List, Optional, Union, Callable, Tuple, Type, Set
import tkinter as tk
from tkinter import ttk
from enum import Enum
from abc import ABC, abstractmethod

class ARIAProperty(Enum):
    AUTOCOMPLETE = "autocomplete"
    CHECKED = "checked"
    DISABLED = "disabled"
    EXPANDED = "expanded"
    HASPOPUP = "haspopup"
    HIDDEN = "hidden"
    INVALID = "invalid"
    LABEL = "label"
    LEVEL = "level"
    MULTILINE = "multiline"
    MULTISELECTABLE = "multiselectable"
    ORIENTATION = "orientation"
    PLACEHOLDER = "placeholder"
    PRESSED = "pressed"
    READONLY = "readonly"
    REQUIRED = "required"
    SELECTED = "selected"
    SORT = "sort"
    VALUEMAX = "valuemax"
    VALUEMIN = "valuemin"
    VALUENOW = "valuenow"
    VALUETEXT = "valuetext"
    MODAL = "modal"
    ATOMIC = "atomic"
    BUSY = "busy"
    LIVE = "live"
    RELEVANT = "relevant"
    DROPEFFECT = "dropeffect"
    GRABBED = "grabbed"
    ACTIVEDESCENDANT = "activedescendant"
    COLCOUNT = "colcount"
    COLINDEX = "colindex"
    COLSPAN = "colspan"
    CONTROLS = "controls"
    DESCRIBEDBY = "describedby"
    DETAILS = "details"
    ERRORMESSAGE = "errormessage"
    FLOWTO = "flowto"
    LABELLEDBY = "labelledby"
    OWNS = "owns"
    POSINSET = "posinset"
    ROWCOUNT = "rowcount"
    ROWINDEX = "rowindex"
    ROWSPAN = "rowspan"
    SETSIZE = "setsize"

class ARIARole(Enum):
    BUTTON = "button"
    CHECKBOX = "checkbox"
    GRIDCELL = "gridcell"
    LINK = "link"
    MENUITEM = "menuitem"
    MENUITEMCHECKBOX = "menuitemcheckbox"
    MENUITEMRADIO = "menuitemradio"
    OPTION = "option"
    PROGRESSBAR = "progressbar"
    RADIO = "radio"
    SCROLLBAR = "scrollbar"
    SEARCHBOX = "searchbox"
    SEPARATOR = "separator"
    SLIDER = "slider"
    SPINBUTTON = "spinbutton"
    SWITCH = "switch"
    TAB = "tab"
    TABPANEL = "tabpanel"
    TEXTBOX = "textbox"
    TREEITEM = "treeitem"
    COMBOBOX = "combobox"
    GRID = "grid"
    LISTBOX = "listbox"
    MENU = "menu"
    MENUBAR = "menubar"
    RADIOGROUP = "radiogroup"
    TABLIST = "tablist"
    TREE = "tree"
    TREEGRID = "treegrid"
    APPLICATION = "application"
    ARTICLE = "article"
    CELL = "cell"
    COLUMNHEADER = "columnheader"
    DEFINITION = "definition"
    DIRECTORY = "directory"
    DOCUMENT = "document"
    FEED = "feed"
    FIGURE = "figure"
    GROUP = "group"
    HEADING = "heading"
    IMG = "img"
    LIST = "list"
    LISTITEM = "listitem"
    MATH = "math"
    NONE = "none"
    NOTE = "note"
    PRESENTATION = "presentation"
    ROW = "row"
    ROWGROUP = "rowgroup"
    ROWHEADER = "rowheader"
    TABLE = "table"
    TERM = "term"
    TOOLBAR = "toolbar"
    TOOLTIP = "tooltip"
    BANNER = "banner"
    COMPLEMENTARY = "complementary"
    CONTENTINFO = "contentinfo"
    FORM = "form"
    MAIN = "main"
    NAVIGATION = "navigation"
    REGION = "region"
    SEARCH = "search"
    ALERT = "alert"
    LOG = "log"
    MARQUEE = "marquee"
    STATUS = "status"
    TIMER = "timer"
    ALERTDIALOG = "alertdialog"
    DIALOG = "dialog"

class AccessibleMixin:
    """"""

    def __init__(
        self,
        *args: Any,
        accessible_name: str = ...,
        accessible_role: str = ...,
        accessible_description: str = ...,
        accessible_value: str = ...,
        live_region: str = ...,
        **kwargs: Any
    ) -> None: ...
    def add_focus_callback(self: Any, callback: Callable) -> None: ...
    def add_state_change_callback(self: Any, callback: Callable) -> None: ...
    def announce(self: Any, message: str, priority: str = ...) -> None: ...
    def get_accessibility_info(self: Any) -> Dict: ...
    def get_aria_property(self: Any, property: ARIAProperty) -> Any: ...
    def is_accessible(self: Any) -> bool: ...
    def remove_focus_callback(self: Any, callback: Callable) -> None: ...
    def remove_keyboard_shortcut(self: Any, key: str) -> None: ...
    def remove_state_change_callback(self: Any, callback: Callable) -> None: ...
    def set_accessible_description(self: Any, description: str) -> None: ...
    def set_accessible_name(self: Any, name: str) -> None: ...
    def set_accessible_role(self: Any, role: str) -> None: ...
    def set_accessible_value(self: Any, value: str) -> None: ...
    def set_aria_property(self: Any, property: ARIAProperty, value: Any) -> None: ...
    def set_compliance_level(self: Any, level: str) -> None: ...
    def set_keyboard_shortcut(self: Any, key: str, callback: Callable) -> None: ...
    def set_live_region(self: Any, live_type: str) -> None: ...
    def validate_accessibility_compliance(self: Any) -> List: ...

class BrailleMixin:
    """"""

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def get_braille_text(self: Any) -> str: ...
    def set_braille_text(self: Any, text: str) -> None: ...

class ComprehensiveAccessibilityMixin(AccessibleMixin, BrailleMixin, HighContrastMixin):
    """"""

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def add_focus_callback(self: Any, callback: Callable) -> None: ...
    def add_state_change_callback(self: Any, callback: Callable) -> None: ...
    def announce(self: Any, message: str, priority: str = ...) -> None: ...
    def get_accessibility_info(self: Any) -> Dict: ...
    def get_aria_property(self: Any, property: ARIAProperty) -> Any: ...
    def get_braille_text(self: Any) -> str: ...
    def get_comprehensive_accessibility_report(self: Any) -> Dict: ...
    def get_contrast_ratio(self: Any) -> float: ...
    def is_accessible(self: Any) -> bool: ...
    def is_contrast_compliant(self: Any) -> bool: ...
    def remove_focus_callback(self: Any, callback: Callable) -> None: ...
    def remove_keyboard_shortcut(self: Any, key: str) -> None: ...
    def remove_state_change_callback(self: Any, callback: Callable) -> None: ...
    def set_accessible_description(self: Any, description: str) -> None: ...
    def set_accessible_name(self: Any, name: str) -> None: ...
    def set_accessible_role(self: Any, role: str) -> None: ...
    def set_accessible_value(self: Any, value: str) -> None: ...
    def set_aria_property(self: Any, property: ARIAProperty, value: Any) -> None: ...
    def set_braille_text(self: Any, text: str) -> None: ...
    def set_compliance_level(self: Any, level: str) -> None: ...
    def set_keyboard_shortcut(self: Any, key: str, callback: Callable) -> None: ...
    def set_live_region(self: Any, live_type: str) -> None: ...
    def validate_accessibility_compliance(self: Any) -> List: ...

class HighContrastMixin:
    """"""

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def get_contrast_ratio(self: Any) -> float: ...
    def is_contrast_compliant(self: Any) -> bool: ...

def announce(message: str, priority: str = ...) -> None: ...
def calculate_contrast_ratio(color1: str, color2: str) -> float: ...
def get_default_role(widget: tk.Widget) -> ARIARole: ...
def is_screen_reader_active() -> bool: ...
def set_accessible_description(widget: tk.Widget, description: str) -> None: ...
def set_accessible_name(widget: tk.Widget, name: str) -> None: ...
def set_accessible_role(widget: tk.Widget, role: str) -> None: ...
def set_accessible_state(widget: tk.Widget, state: str, value: bool) -> None: ...
def set_accessible_value(widget: tk.Widget, value: str) -> None: ...
def speak(text: str, priority: str = ..., interrupt: bool = ...) -> None: ...
def validate_aria_compliance(
    widget: tk.Widget, role: ARIARole, properties: Dict[str, Any]
) -> List[str]: ...
def validate_contrast_ratio(
    foreground: str, background: str, level: str = ..., size: str = ...
) -> bool: ...
