# tkaria11y.accessibility_validator.pyi
# Type stubs for tkaria11y.accessibility_validator

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

class AccessibilityIssue:
    """Represents an accessibility issue"""

    auto_fixable: bool
    recommendation: str
    wcag_criterion: str
    widget: None
    widget_class: str
    widget_path: str

    def __init__(
        self: Any,
        severity: IssueSeverity,
        category: ValidationCategory,
        title: str,
        description: str,
        widget: Optional = ...,
        widget_class: str = ...,
        widget_path: str = ...,
        recommendation: str = ...,
        wcag_criterion: str = ...,
        auto_fixable: bool = ...,
    ) -> None: ...

class AccessibilityTester:
    """Interactive accessibility testing tools"""

    def __init__(self: Any, root: Tk) -> Any: ...
    def run_full_audit(self: Any) -> Dict: ...
    def test_keyboard_navigation(self: Any) -> List: ...
    def test_screen_reader_compatibility(self: Any) -> Dict: ...

class AccessibilityValidator:
    """Comprehensive accessibility validator"""

    def __init__(self: Any, compliance_level: ValidationLevel = ...) -> Any: ...
    def auto_fix_issues(self: Any, root: Tk) -> int: ...
    def generate_report(self: Any) -> Dict: ...
    def validate_application(self: Any, root: Tk) -> List: ...

class Any:
    """Special type indicating an unconstrained type."""

    def __init__(self: Any, args: Any, kwargs: Any) -> Any: ...

class Enum:
    """"""

    ...

class IssueSeverity(Enum):
    CRITICAL: str
    HIGH: str
    MEDIUM: str
    LOW: str
    INFO: str

class ValidationCategory(Enum):
    PERCEIVABLE: str
    OPERABLE: str
    UNDERSTANDABLE: str
    ROBUST: str

class ValidationLevel(Enum):
    A: str
    AA: str
    AAA: str

def auto_fix_accessibility_issues(root: Tk) -> int: ...
def calculate_contrast_ratio(color1: str, color2: str) -> float: ...
def dataclass(
    cls: Any = ...,
    init: Any = ...,
    repr: Any = ...,
    eq: Any = ...,
    order: Any = ...,
    unsafe_hash: Any = ...,
    frozen: Any = ...,
    match_args: Any = ...,
    kw_only: Any = ...,
    slots: Any = ...,
    weakref_slot: Any = ...,
) -> Any: ...
def is_screen_reader_active() -> bool: ...
def run_accessibility_audit(root: Tk) -> Dict: ...
def test_keyboard_navigation(root: Tk) -> List: ...
def test_screen_reader_compatibility(root: Tk) -> Dict: ...

threading: Any
time: Any
tk: Any

def validate_accessibility(
    root: Tk, compliance_level: ValidationLevel = ...
) -> Dict: ...
def validate_aria_compliance(
    widget: Widget, role: ARIARole, properties: Dict
) -> List: ...
def validate_contrast_ratio(
    foreground: str, background: str, level: str = ..., size: str = ...
) -> bool: ...
def validate_keyboard_navigation(widget: Widget) -> List: ...
