# tkaria11y.aria_compliance.pyi
# Type stubs for tkaria11y.aria_compliance

from typing import Any, Dict, List, Optional, Union, Callable, Tuple, Type, Set
import tkinter as tk
from tkinter import ttk
from enum import Enum
from abc import ABC, abstractmethod

class ARIAProperty(Enum):
    AUTOCOMPLETE: str
    CHECKED: str
    DISABLED: str
    EXPANDED: str
    HASPOPUP: str
    HIDDEN: str
    INVALID: str
    LABEL: str
    LEVEL: str
    MULTILINE: str
    MULTISELECTABLE: str
    ORIENTATION: str
    PLACEHOLDER: str
    PRESSED: str
    READONLY: str
    REQUIRED: str
    SELECTED: str
    SORT: str
    VALUEMAX: str
    VALUEMIN: str
    VALUENOW: str
    VALUETEXT: str
    MODAL: str
    ATOMIC: str
    BUSY: str
    LIVE: str
    RELEVANT: str
    DROPEFFECT: str
    GRABBED: str
    ACTIVEDESCENDANT: str
    COLCOUNT: str
    COLINDEX: str
    COLSPAN: str
    CONTROLS: str
    DESCRIBEDBY: str
    DETAILS: str
    ERRORMESSAGE: str
    FLOWTO: str
    LABELLEDBY: str
    OWNS: str
    POSINSET: str
    ROWCOUNT: str
    ROWINDEX: str
    ROWSPAN: str
    SETSIZE: str

class ARIARole(Enum):
    BUTTON: str
    CHECKBOX: str
    GRIDCELL: str
    LINK: str
    MENUITEM: str
    MENUITEMCHECKBOX: str
    MENUITEMRADIO: str
    OPTION: str
    PROGRESSBAR: str
    RADIO: str
    SCROLLBAR: str
    SEARCHBOX: str
    SEPARATOR: str
    SLIDER: str
    SPINBUTTON: str
    SWITCH: str
    TAB: str
    TABPANEL: str
    TEXTBOX: str
    TREEITEM: str
    COMBOBOX: str
    GRID: str
    LISTBOX: str
    MENU: str
    MENUBAR: str
    RADIOGROUP: str
    TABLIST: str
    TREE: str
    TREEGRID: str
    APPLICATION: str
    ARTICLE: str
    CELL: str
    COLUMNHEADER: str
    DEFINITION: str
    DIRECTORY: str
    DOCUMENT: str
    FEED: str
    FIGURE: str
    GROUP: str
    HEADING: str
    IMG: str
    LIST: str
    LISTITEM: str
    MATH: str
    NONE: str
    NOTE: str
    PRESENTATION: str
    ROW: str
    ROWGROUP: str
    ROWHEADER: str
    TABLE: str
    TERM: str
    TOOLBAR: str
    TOOLTIP: str
    BANNER: str
    COMPLEMENTARY: str
    CONTENTINFO: str
    FORM: str
    MAIN: str
    NAVIGATION: str
    REGION: str
    SEARCH: str
    ALERT: str
    LOG: str
    MARQUEE: str
    STATUS: str
    TIMER: str
    ALERTDIALOG: str
    DIALOG: str

class ARIAValidator:
    """Validates ARIA compliance for widgets"""

    def __init__(self: Any, args: Any, kwargs: Any) -> Any: ...
    def validate_widget(widget: Widget, role: ARIARole, properties: Dict) -> List: ...

class Any:
    """Special type indicating an unconstrained type."""

    def __init__(self: Any, args: Any, kwargs: Any) -> Any: ...

class Enum:
    """"""

    ...

ROLE_REQUIRED_PROPERTIES: Dict[str, Any]
ROLE_SUPPORTED_PROPERTIES: Dict[str, Any]
WIDGET_ARIA_MAPPING: Dict[str, Any]

def calculate_contrast_ratio(color1: str, color2: str) -> float: ...
def get_default_role(widget: Widget) -> ARIARole: ...
def get_required_properties(role: ARIARole) -> Set: ...
def get_supported_properties(role: ARIARole) -> Set: ...

tk: Any

def validate_aria_compliance(
    widget: Widget, role: ARIARole, properties: Dict
) -> List: ...
def validate_contrast_ratio(
    foreground: str, background: str, level: str = ..., size: str = ...
) -> bool: ...
def validate_font_size(font_size: int, unit: str = ...) -> bool: ...
def validate_keyboard_navigation(widget: Widget) -> List: ...
