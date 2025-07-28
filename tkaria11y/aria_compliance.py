# tkaria11y/aria_compliance.py

"""
ARIA compliance module providing complete ARIA role mappings, properties,
and validation for full WCAG 2.1 compliance.
"""

from typing import Dict, Set, List, Optional, Any, Tuple
import tkinter as tk
from enum import Enum


class ARIARole(Enum):
    """Complete ARIA roles enumeration"""

    # Widget roles
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

    # Composite roles
    COMBOBOX = "combobox"
    GRID = "grid"
    LISTBOX = "listbox"
    MENU = "menu"
    MENUBAR = "menubar"
    RADIOGROUP = "radiogroup"
    TABLIST = "tablist"
    TREE = "tree"
    TREEGRID = "treegrid"

    # Document structure roles
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

    # Landmark roles
    BANNER = "banner"
    COMPLEMENTARY = "complementary"
    CONTENTINFO = "contentinfo"
    FORM = "form"
    MAIN = "main"
    NAVIGATION = "navigation"
    REGION = "region"
    SEARCH = "search"

    # Live region roles
    ALERT = "alert"
    LOG = "log"
    MARQUEE = "marquee"
    STATUS = "status"
    TIMER = "timer"

    # Window roles
    ALERTDIALOG = "alertdialog"
    DIALOG = "dialog"


class ARIAProperty(Enum):
    """ARIA properties and states"""

    # Widget attributes
    AUTOCOMPLETE = "aria-autocomplete"
    CHECKED = "aria-checked"
    DISABLED = "aria-disabled"
    EXPANDED = "aria-expanded"
    HASPOPUP = "aria-haspopup"
    HIDDEN = "aria-hidden"
    INVALID = "aria-invalid"
    LABEL = "aria-label"
    LEVEL = "aria-level"
    MULTILINE = "aria-multiline"
    MULTISELECTABLE = "aria-multiselectable"
    ORIENTATION = "aria-orientation"
    PLACEHOLDER = "aria-placeholder"
    PRESSED = "aria-pressed"
    READONLY = "aria-readonly"
    REQUIRED = "aria-required"
    SELECTED = "aria-selected"
    SORT = "aria-sort"
    VALUEMAX = "aria-valuemax"
    VALUEMIN = "aria-valuemin"
    VALUENOW = "aria-valuenow"
    VALUETEXT = "aria-valuetext"

    # Dialog attributes
    MODAL = "aria-modal"

    # Live region attributes
    ATOMIC = "aria-atomic"
    BUSY = "aria-busy"
    LIVE = "aria-live"
    RELEVANT = "aria-relevant"

    # Drag and drop attributes
    DROPEFFECT = "aria-dropeffect"
    GRABBED = "aria-grabbed"

    # Relationship attributes
    ACTIVEDESCENDANT = "aria-activedescendant"
    COLCOUNT = "aria-colcount"
    COLINDEX = "aria-colindex"
    COLSPAN = "aria-colspan"
    CONTROLS = "aria-controls"
    DESCRIBEDBY = "aria-describedby"
    DETAILS = "aria-details"
    ERRORMESSAGE = "aria-errormessage"
    FLOWTO = "aria-flowto"
    LABELLEDBY = "aria-labelledby"
    OWNS = "aria-owns"
    POSINSET = "aria-posinset"
    ROWCOUNT = "aria-rowcount"
    ROWINDEX = "aria-rowindex"
    ROWSPAN = "aria-rowspan"
    SETSIZE = "aria-setsize"


# Widget class to ARIA role mapping
WIDGET_ARIA_MAPPING: Dict[str, ARIARole] = {
    # Standard Tkinter widgets
    "Button": ARIARole.BUTTON,
    "Entry": ARIARole.TEXTBOX,
    "Label": ARIARole.NONE,  # Labels are typically presentation
    "Text": ARIARole.TEXTBOX,
    "Checkbutton": ARIARole.CHECKBOX,
    "Radiobutton": ARIARole.RADIO,
    "Scale": ARIARole.SLIDER,
    "Scrollbar": ARIARole.SCROLLBAR,
    "Listbox": ARIARole.LISTBOX,
    "Menu": ARIARole.MENU,
    "Menubutton": ARIARole.BUTTON,
    "Frame": ARIARole.GROUP,
    "LabelFrame": ARIARole.GROUP,
    "Toplevel": ARIARole.DIALOG,
    "Canvas": ARIARole.IMG,
    "Message": ARIARole.NONE,
    "Spinbox": ARIARole.SPINBUTTON,
    "PanedWindow": ARIARole.GROUP,
    # TTK widgets
    "ttk.Button": ARIARole.BUTTON,
    "ttk.Entry": ARIARole.TEXTBOX,
    "ttk.Label": ARIARole.NONE,
    "ttk.Checkbutton": ARIARole.CHECKBOX,
    "ttk.Radiobutton": ARIARole.RADIO,
    "ttk.Scale": ARIARole.SLIDER,
    "ttk.Scrollbar": ARIARole.SCROLLBAR,
    "ttk.Frame": ARIARole.GROUP,
    "ttk.LabelFrame": ARIARole.GROUP,
    "ttk.Notebook": ARIARole.TABLIST,
    "ttk.Progressbar": ARIARole.PROGRESSBAR,
    "ttk.Separator": ARIARole.SEPARATOR,
    "ttk.Sizegrip": ARIARole.NONE,
    "ttk.Treeview": ARIARole.TREE,
    "ttk.Combobox": ARIARole.COMBOBOX,
    "ttk.Spinbox": ARIARole.SPINBUTTON,
    # CustomTkinter widgets (when available)
    "CTkButton": ARIARole.BUTTON,
    "CTkEntry": ARIARole.TEXTBOX,
    "CTkLabel": ARIARole.NONE,
    "CTkCheckBox": ARIARole.CHECKBOX,
    "CTkRadioButton": ARIARole.RADIO,
    "CTkSlider": ARIARole.SLIDER,
    "CTkScrollbar": ARIARole.SCROLLBAR,
    "CTkFrame": ARIARole.GROUP,
    "CTkTabview": ARIARole.TABLIST,
    "CTkProgressBar": ARIARole.PROGRESSBAR,
    "CTkSwitch": ARIARole.SWITCH,
    "CTkComboBox": ARIARole.COMBOBOX,
    "CTkTextbox": ARIARole.TEXTBOX,
    "CTkScrollableFrame": ARIARole.GROUP,
    "CTkToplevel": ARIARole.DIALOG,
}


# Required properties for each role
ROLE_REQUIRED_PROPERTIES: Dict[ARIARole, Set[ARIAProperty]] = {
    ARIARole.BUTTON: set(),
    ARIARole.CHECKBOX: {ARIAProperty.CHECKED},
    ARIARole.RADIO: {ARIAProperty.CHECKED},
    ARIARole.TEXTBOX: set(),
    ARIARole.SLIDER: {
        ARIAProperty.VALUEMIN,
        ARIAProperty.VALUEMAX,
        ARIAProperty.VALUENOW,
    },
    ARIARole.PROGRESSBAR: {
        ARIAProperty.VALUEMIN,
        ARIAProperty.VALUEMAX,
        ARIAProperty.VALUENOW,
    },
    ARIARole.SPINBUTTON: {
        ARIAProperty.VALUEMIN,
        ARIAProperty.VALUEMAX,
        ARIAProperty.VALUENOW,
    },
    ARIARole.COMBOBOX: {ARIAProperty.EXPANDED},
    ARIARole.LISTBOX: set(),
    ARIARole.TREE: set(),
    ARIARole.TABLIST: set(),
    ARIARole.TAB: {ARIAProperty.SELECTED},
    ARIARole.TABPANEL: set(),
    ARIARole.DIALOG: set(),
    ARIARole.ALERTDIALOG: set(),
}


# Supported properties for each role
ROLE_SUPPORTED_PROPERTIES: Dict[ARIARole, Set[ARIAProperty]] = {
    ARIARole.BUTTON: {
        ARIAProperty.DISABLED,
        ARIAProperty.EXPANDED,
        ARIAProperty.HASPOPUP,
        ARIAProperty.PRESSED,
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
    },
    ARIARole.CHECKBOX: {
        ARIAProperty.CHECKED,
        ARIAProperty.DISABLED,
        ARIAProperty.INVALID,
        ARIAProperty.READONLY,
        ARIAProperty.REQUIRED,
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
    },
    ARIARole.RADIO: {
        ARIAProperty.CHECKED,
        ARIAProperty.DISABLED,
        ARIAProperty.INVALID,
        ARIAProperty.READONLY,
        ARIAProperty.REQUIRED,
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
        ARIAProperty.POSINSET,
        ARIAProperty.SETSIZE,
    },
    ARIARole.TEXTBOX: {
        ARIAProperty.AUTOCOMPLETE,
        ARIAProperty.DISABLED,
        ARIAProperty.INVALID,
        ARIAProperty.MULTILINE,
        ARIAProperty.PLACEHOLDER,
        ARIAProperty.READONLY,
        ARIAProperty.REQUIRED,
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
    },
    ARIARole.SLIDER: {
        ARIAProperty.VALUEMIN,
        ARIAProperty.VALUEMAX,
        ARIAProperty.VALUENOW,
        ARIAProperty.VALUETEXT,
        ARIAProperty.ORIENTATION,
        ARIAProperty.DISABLED,
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
    },
    ARIARole.PROGRESSBAR: {
        ARIAProperty.VALUEMIN,
        ARIAProperty.VALUEMAX,
        ARIAProperty.VALUENOW,
        ARIAProperty.VALUETEXT,
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
    },
    ARIARole.LISTBOX: {
        ARIAProperty.MULTISELECTABLE,
        ARIAProperty.ORIENTATION,
        ARIAProperty.DISABLED,
        ARIAProperty.EXPANDED,
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
        ARIAProperty.ACTIVEDESCENDANT,
    },
    ARIARole.COMBOBOX: {
        ARIAProperty.EXPANDED,
        ARIAProperty.HASPOPUP,
        ARIAProperty.DISABLED,
        ARIAProperty.INVALID,
        ARIAProperty.READONLY,
        ARIAProperty.REQUIRED,
        ARIAProperty.AUTOCOMPLETE,
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
        ARIAProperty.ACTIVEDESCENDANT,
    },
    ARIARole.TREE: {
        ARIAProperty.MULTISELECTABLE,
        ARIAProperty.ORIENTATION,
        ARIAProperty.DISABLED,
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
        ARIAProperty.ACTIVEDESCENDANT,
    },
    ARIARole.TABLIST: {
        ARIAProperty.ORIENTATION,
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
        ARIAProperty.ACTIVEDESCENDANT,
    },
    ARIARole.TAB: {
        ARIAProperty.SELECTED,
        ARIAProperty.DISABLED,
        ARIAProperty.EXPANDED,
        ARIAProperty.HASPOPUP,
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
        ARIAProperty.POSINSET,
        ARIAProperty.SETSIZE,
    },
    ARIARole.TABPANEL: {
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
    },
    ARIARole.DIALOG: {
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
        ARIAProperty.MODAL,
    },
    ARIARole.GROUP: {
        ARIAProperty.LABEL,
        ARIAProperty.DESCRIBEDBY,
        ARIAProperty.LABELLEDBY,
    },
}


class ARIAValidator:
    """Validates ARIA compliance for widgets"""

    @staticmethod
    def validate_widget(
        widget: tk.Widget, role: ARIARole, properties: Dict[ARIAProperty, Any]
    ) -> List[str]:
        """Validate ARIA compliance for a widget"""
        errors = []

        # Check required properties
        required = ROLE_REQUIRED_PROPERTIES.get(role, set())
        for prop in required:
            if prop not in properties:
                errors.append(
                    f"Missing required property {prop.value} for role {role.value}"
                )

        # Check supported properties
        supported = ROLE_SUPPORTED_PROPERTIES.get(role, set())
        for prop in properties:
            if prop not in supported:
                errors.append(
                    f"Property {prop.value} not supported for role {role.value}"
                )

        # Validate property values
        for prop, value in properties.items():
            validation_error = ARIAValidator._validate_property_value(prop, value)
            if validation_error:
                errors.append(validation_error)

        return errors

    @staticmethod
    def _validate_property_value(prop: ARIAProperty, value: Any) -> Optional[str]:
        """Validate individual property values"""
        if prop == ARIAProperty.CHECKED:
            if value not in ["true", "false", "mixed"]:
                return f"Invalid value for {prop.value}: must be 'true', 'false', or 'mixed'"

        elif prop == ARIAProperty.EXPANDED:
            if value not in ["true", "false", "undefined"]:
                return f"Invalid value for {prop.value}: must be 'true', 'false', or 'undefined'"

        elif prop == ARIAProperty.SELECTED:
            if value not in ["true", "false", "undefined"]:
                return f"Invalid value for {prop.value}: must be 'true', 'false', or 'undefined'"

        elif prop == ARIAProperty.DISABLED:
            if value not in ["true", "false"]:
                return f"Invalid value for {prop.value}: must be 'true' or 'false'"

        elif prop == ARIAProperty.HIDDEN:
            if value not in ["true", "false"]:
                return f"Invalid value for {prop.value}: must be 'true' or 'false'"

        elif prop == ARIAProperty.INVALID:
            if value not in ["true", "false", "grammar", "spelling"]:
                return f"Invalid value for {prop.value}: must be 'true', 'false', 'grammar', or 'spelling'"

        elif prop == ARIAProperty.LIVE:
            if value not in ["off", "polite", "assertive"]:
                return f"Invalid value for {prop.value}: must be 'off', 'polite', or 'assertive'"

        elif prop == ARIAProperty.ORIENTATION:
            if value not in ["horizontal", "vertical", "undefined"]:
                return f"Invalid value for {prop.value}: must be 'horizontal', 'vertical', or 'undefined'"

        elif prop == ARIAProperty.SORT:
            if value not in ["ascending", "descending", "none", "other"]:
                return f"Invalid value for {prop.value}: must be 'ascending', 'descending', 'none', or 'other'"

        elif prop in [
            ARIAProperty.VALUEMIN,
            ARIAProperty.VALUEMAX,
            ARIAProperty.VALUENOW,
        ]:
            try:
                float(value)
            except (ValueError, TypeError):
                return f"Invalid value for {prop.value}: must be a number"

        elif prop in [
            ARIAProperty.LEVEL,
            ARIAProperty.POSINSET,
            ARIAProperty.SETSIZE,
            ARIAProperty.COLCOUNT,
            ARIAProperty.COLINDEX,
            ARIAProperty.COLSPAN,
            ARIAProperty.ROWCOUNT,
            ARIAProperty.ROWINDEX,
            ARIAProperty.ROWSPAN,
        ]:
            try:
                int(value)
            except (ValueError, TypeError):
                return f"Invalid value for {prop.value}: must be an integer"

        return None


def get_default_role(widget: tk.Misc) -> ARIARole:
    """Get the default ARIA role for a widget"""
    widget_class = widget.winfo_class()
    return WIDGET_ARIA_MAPPING.get(widget_class, ARIARole.NONE)


def get_required_properties(role: ARIARole) -> Set[ARIAProperty]:
    """Get required properties for an ARIA role"""
    return ROLE_REQUIRED_PROPERTIES.get(role, set())


def get_supported_properties(role: ARIARole) -> Set[ARIAProperty]:
    """Get supported properties for an ARIA role"""
    return ROLE_SUPPORTED_PROPERTIES.get(role, set())


def validate_aria_compliance(
    widget: tk.Widget, role: ARIARole, properties: Dict[ARIAProperty, Any]
) -> List[str]:
    """Validate ARIA compliance for a widget"""
    return ARIAValidator.validate_widget(widget, role, properties)


# Contrast ratio validation for WCAG compliance
def calculate_contrast_ratio(color1: str, color2: str) -> float:
    """Calculate contrast ratio between two colors"""

    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join([c * 2 for c in hex_color])
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )

    def get_luminance(rgb: Tuple[int, int, int]) -> float:
        """Calculate relative luminance"""

        def normalize(c: int) -> float:
            c_float = c / 255.0
            if c_float <= 0.03928:
                return c_float / 12.92
            else:
                return float(pow((c_float + 0.055) / 1.055, 2.4))

        r, g, b = rgb
        return 0.2126 * normalize(r) + 0.7152 * normalize(g) + 0.0722 * normalize(b)

    try:
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)

        lum1 = get_luminance(rgb1)
        lum2 = get_luminance(rgb2)

        # Ensure lighter color is in numerator
        if lum1 > lum2:
            return (lum1 + 0.05) / (lum2 + 0.05)
        else:
            return (lum2 + 0.05) / (lum1 + 0.05)
    except (ValueError, TypeError):
        return 1.0  # Return minimum ratio on error


def validate_contrast_ratio(
    foreground: str, background: str, level: str = "AA", size: str = "normal"
) -> bool:
    """Validate contrast ratio meets WCAG requirements"""
    ratio = calculate_contrast_ratio(foreground, background)

    if level == "AAA":
        if size == "large":
            return ratio >= 4.5
        else:
            return ratio >= 7.0
    else:  # AA level
        if size == "large":
            return ratio >= 3.0
        else:
            return ratio >= 4.5


# Font size validation for accessibility
def validate_font_size(font_size: int, unit: str = "pt") -> bool:
    """Validate font size meets accessibility requirements"""
    if unit == "pt":
        return font_size >= 12  # Minimum 12pt for accessibility
    elif unit == "px":
        return font_size >= 16  # Minimum 16px for accessibility
    else:
        return True  # Unknown unit, assume valid


# Keyboard navigation validation
def validate_keyboard_navigation(widget: tk.Misc) -> List[str]:
    """Validate keyboard navigation compliance"""
    errors = []

    # Check if widget can receive focus
    try:
        takefocus = widget.cget("takefocus")
        if takefocus == 0:
            errors.append("Widget cannot receive keyboard focus")
    except tk.TclError:
        # Widget doesn't support takefocus
        pass

    # Check for keyboard event bindings
    bindings = widget.bind()
    keyboard_events = [
        "<Key>",
        "<KeyPress>",
        "<KeyRelease>",
        "<Return>",
        "<space>",
        "<Tab>",
        "<Shift-Tab>",
        "<Up>",
        "<Down>",
        "<Left>",
        "<Right>",
    ]

    has_keyboard_binding = any(event in str(bindings) for event in keyboard_events)

    widget_class = widget.winfo_class()
    interactive_widgets = [
        "Button",
        "Entry",
        "Text",
        "Checkbutton",
        "Radiobutton",
        "Scale",
        "Listbox",
        "Scrollbar",
        "Spinbox",
    ]

    if widget_class in interactive_widgets and not has_keyboard_binding:
        errors.append("Interactive widget lacks keyboard event bindings")

    return errors
