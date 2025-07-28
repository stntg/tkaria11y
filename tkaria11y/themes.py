# tkaria11y/themes.py

"""
Theme utilities for accessibility:
- HighContrastTheme: Apply high-contrast colors
- set_dyslexic_font: Apply dyslexic-friendly fonts
"""

import tkinter as tk
from typing import Dict, List, Optional, Any, Tuple
import weakref


class HighContrastTheme:
    """High contrast theme for better visibility"""

    COLORS = {
        "bg": "black",
        "fg": "white",
        "select_bg": "yellow",
        "select_fg": "black",
        "active_bg": "white",
        "active_fg": "black",
        "insert_bg": "white",  # Cursor color
        "disabled_fg": "gray",
        "disabled_bg": "#333333",
    }

    # Standard system colors for restoration
    STANDARD_COLORS = {
        "bg": "SystemButtonFace",
        "fg": "SystemButtonText",
        "select_bg": "SystemHighlight",
        "select_fg": "SystemHighlightText",
        "active_bg": "SystemButtonFace",
        "active_fg": "SystemButtonText",
        "insert_bg": "SystemWindowText",
        "disabled_fg": "SystemGrayText",
        "disabled_bg": "SystemButtonFace",
    }

    # Track which roots have the theme applied
    _themed_roots: weakref.WeakSet = weakref.WeakSet()
    # Store original option database values for restoration
    _original_options: Dict[tk.Tk, Dict[str, str]] = {}

    @classmethod
    def apply(cls, root: tk.Tk) -> None:
        """Apply high contrast theme to root and all current/future children"""
        if root in cls._themed_roots:
            return  # Already themed

        # Store original option database values for restoration
        cls._store_original_options(root)

        # Set default colors using Tkinter's option database
        # This ensures ALL widgets created after this call will use these colors
        cls._set_option_database(root)

        # Apply to the root window itself first
        cls._apply_to_root_window(root)

        # Apply to all existing widgets
        cls._apply_to_all_widgets(root)

        # Track this root as themed
        cls._themed_roots.add(root)

        # Set up automatic theming for new widgets
        cls._setup_auto_theming(root)

    @classmethod
    def _store_original_options(cls, root: tk.Tk) -> None:
        """Store original option database values for restoration"""
        if root not in cls._original_options:
            cls._original_options[root] = {}

            # Try to get current option values (may not exist)
            options_to_store = [
                "*Background",
                "*Foreground",
                "*selectBackground",
                "*selectForeground",
                "*activeBackground",
                "*activeForeground",
                "*insertBackground",
                "*disabledForeground",
                "*disabledBackground",
            ]

            for option in options_to_store:
                try:
                    # Map option names to standard colors
                    color_key = cls._get_color_key_for_option(option)
                    if color_key:
                        cls._original_options[root][option] = cls.STANDARD_COLORS[
                            color_key
                        ]
                except (KeyError, AttributeError, tk.TclError):
                    # Skip if option doesn't exist or can't be accessed
                    pass

    @classmethod
    def _get_color_key_for_option(cls, option: str) -> str:
        """Map option name to color key"""
        option_lower = option.lower()
        is_background = "background" in option

        # Define mapping for special cases
        special_mappings = {
            "select": ("select_bg", "select_fg"),
            "active": ("active_bg", "active_fg"),
            "disabled": ("disabled_bg", "disabled_fg"),
        }

        # Check special cases first
        for key, (bg_color, fg_color) in special_mappings.items():
            if key in option_lower:
                return bg_color if is_background else fg_color

        # Handle insert case
        if "insert" in option_lower:
            return "insert_bg"

        # Handle basic cases
        if is_background:
            return "bg"
        if "foreground" in option:
            return "fg"

        return ""

    @classmethod
    def _apply_to_root_window(cls, root: tk.Tk) -> None:
        """Apply theme specifically to the root window"""
        try:
            # Set root window background
            root.configure(bg=cls.COLORS["bg"])

            # Set the default palette for the entire application
            try:
                root.tk.call("tk_setPalette", cls.COLORS["bg"])
            except tk.TclError:
                pass

        except tk.TclError:
            pass

    @classmethod
    def _apply_to_all_widgets(cls, root: tk.Tk) -> None:
        """Apply theme to all widgets in the application"""
        # Apply to root first
        cls._apply_to_widget(root)

        # Then apply to all children recursively
        cls._apply_to_children(root)

        # Force update
        root.update_idletasks()

    @classmethod
    def _set_option_database(cls, root: tk.Tk) -> None:
        """Set default colors in Tkinter's option database"""
        # Clear any existing options first
        try:
            root.option_clear()
        except tk.TclError:
            # Option database may not be available or already cleared
            pass

        # General widget defaults - these apply to ALL widgets
        root.option_add("*Background", cls.COLORS["bg"], "startupFile")
        root.option_add("*Foreground", cls.COLORS["fg"], "startupFile")
        root.option_add("*selectBackground", cls.COLORS["select_bg"], "startupFile")
        root.option_add("*selectForeground", cls.COLORS["select_fg"], "startupFile")
        root.option_add("*activeBackground", cls.COLORS["active_bg"], "startupFile")
        root.option_add("*activeForeground", cls.COLORS["active_fg"], "startupFile")
        root.option_add("*insertBackground", cls.COLORS["insert_bg"], "startupFile")
        root.option_add("*disabledForeground", cls.COLORS["disabled_fg"], "startupFile")
        root.option_add("*disabledBackground", cls.COLORS["disabled_bg"], "startupFile")

        # Main window (Tk) specific - CRITICAL for accessibility
        root.option_add("*Tk.Background", cls.COLORS["bg"], "startupFile")
        root.option_add("*Tk.Foreground", cls.COLORS["fg"], "startupFile")

        # Specific widget types with high priority
        widget_types = [
            "Button",
            "Label",
            "Entry",
            "Text",
            "Frame",
            "Toplevel",
            "Canvas",
            "Listbox",
            "Scale",
            "Checkbutton",
            "Radiobutton",
            "Menu",
            "Menubutton",
            "Message",
            "Spinbox",
            "PanedWindow",
            "LabelFrame",
            "Scrollbar",
        ]

        for widget_type in widget_types:
            root.option_add(
                f"*{widget_type}.Background", cls.COLORS["bg"], "startupFile"
            )
            root.option_add(
                f"*{widget_type}.Foreground", cls.COLORS["fg"], "startupFile"
            )
            root.option_add(
                f"*{widget_type}.selectBackground",
                cls.COLORS["select_bg"],
                "startupFile",
            )
            root.option_add(
                f"*{widget_type}.selectForeground",
                cls.COLORS["select_fg"],
                "startupFile",
            )
            root.option_add(
                f"*{widget_type}.activeBackground",
                cls.COLORS["active_bg"],
                "startupFile",
            )
            root.option_add(
                f"*{widget_type}.activeForeground",
                cls.COLORS["active_fg"],
                "startupFile",
            )

        # Special cases
        root.option_add("*Entry.fieldBackground", cls.COLORS["bg"], "startupFile")
        root.option_add(
            "*Entry.insertBackground", cls.COLORS["insert_bg"], "startupFile"
        )
        root.option_add(
            "*Text.insertBackground", cls.COLORS["insert_bg"], "startupFile"
        )
        root.option_add("*Scale.troughColor", cls.COLORS["active_bg"], "startupFile")
        root.option_add(
            "*Scrollbar.troughColor", cls.COLORS["active_bg"], "startupFile"
        )
        root.option_add(
            "*Checkbutton.selectColor", cls.COLORS["select_bg"], "startupFile"
        )
        root.option_add(
            "*Radiobutton.selectColor", cls.COLORS["select_bg"], "startupFile"
        )

    @classmethod
    def _setup_auto_theming(cls, root: tk.Tk) -> None:
        """Set up automatic theming for widgets created after apply() is called"""

        # Override widget creation to auto-theme new widgets
        def auto_theme_new_widgets() -> None:
            """Periodically check for and theme new widgets"""
            if root in cls._themed_roots:
                try:
                    cls._apply_to_children(root)
                    # Schedule next check
                    root.after(100, auto_theme_new_widgets)  # Check every 100ms
                except tk.TclError:
                    # Root was destroyed
                    pass

        # Start the auto-theming loop
        root.after(100, auto_theme_new_widgets)

    @classmethod
    def _apply_to_widget(cls, widget: tk.Misc) -> None:
        """Apply theme to a single widget with comprehensive coverage"""
        try:
            widget_class = widget.winfo_class()

            # Get all configurable options for this widget
            try:
                config_options = widget.configure()
            except tk.TclError:
                return

            # Apply colors in groups
            cls._apply_basic_colors(widget, config_options)
            cls._apply_selection_colors(widget, config_options)
            cls._apply_active_colors(widget, config_options)
            cls._apply_special_colors(widget, config_options)
            cls._apply_widget_specific_colors(widget, widget_class, config_options)

            # Force widget to update its appearance
            try:
                widget.update_idletasks()
            except tk.TclError:
                pass

        except (tk.TclError, AttributeError):
            # Widget doesn't support these operations
            pass

    @classmethod
    def _apply_basic_colors(cls, widget: tk.Misc, config_options: dict) -> None:
        """Apply basic background and foreground colors"""
        if "background" in config_options or "bg" in config_options:
            try:
                widget.configure(bg=cls.COLORS["bg"])  # type: ignore[call-arg]
            except tk.TclError:
                pass

        if "foreground" in config_options or "fg" in config_options:
            try:
                widget.configure(fg=cls.COLORS["fg"])  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _apply_selection_colors(cls, widget: tk.Misc, config_options: dict) -> None:
        """Apply selection colors"""
        if "selectbackground" in config_options:
            try:
                widget.configure(
                    selectbackground=cls.COLORS["select_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

        if "selectforeground" in config_options:
            try:
                widget.configure(
                    selectforeground=cls.COLORS["select_fg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _apply_active_colors(cls, widget: tk.Misc, config_options: dict) -> None:
        """Apply active colors"""
        if "activebackground" in config_options:
            try:
                widget.configure(
                    activebackground=cls.COLORS["active_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

        if "activeforeground" in config_options:
            try:
                widget.configure(
                    activeforeground=cls.COLORS["active_fg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _apply_special_colors(cls, widget: tk.Misc, config_options: dict) -> None:
        """Apply special colors like insert and disabled"""
        if "insertbackground" in config_options:
            try:
                widget.configure(
                    insertbackground=cls.COLORS["insert_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

        if "disabledforeground" in config_options:
            try:
                widget.configure(
                    disabledforeground=cls.COLORS["disabled_fg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

        if "disabledbackground" in config_options:
            try:
                widget.configure(
                    disabledbackground=cls.COLORS["disabled_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _apply_widget_specific_colors(
        cls, widget: tk.Misc, widget_class: str, config_options: dict
    ) -> None:
        """Apply widget-specific colors"""
        if widget_class == "Entry":
            cls._apply_entry_colors(widget, config_options)
        elif widget_class == "Scale":
            cls._apply_scale_colors(widget, config_options)
        elif widget_class in ["Checkbutton", "Radiobutton"]:
            cls._apply_button_colors(widget, config_options)
        elif widget_class == "Scrollbar":
            cls._apply_scrollbar_colors(widget, config_options)
        elif widget_class == "Menu":
            cls._apply_menu_colors(widget, config_options)

    @classmethod
    def _apply_entry_colors(cls, widget: tk.Misc, config_options: dict) -> None:
        """Apply Entry-specific colors"""
        if "fieldbackground" in config_options:
            try:
                widget.configure(
                    fieldbackground=cls.COLORS["bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _apply_scale_colors(cls, widget: tk.Misc, config_options: dict) -> None:
        """Apply Scale-specific colors"""
        if "troughcolor" in config_options:
            try:
                widget.configure(
                    troughcolor=cls.COLORS["active_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _apply_button_colors(cls, widget: tk.Misc, config_options: dict) -> None:
        """Apply Checkbutton/Radiobutton-specific colors"""
        if "selectcolor" in config_options:
            try:
                widget.configure(
                    selectcolor=cls.COLORS["select_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _apply_scrollbar_colors(cls, widget: tk.Misc, config_options: dict) -> None:
        """Apply Scrollbar-specific colors"""
        if "troughcolor" in config_options:
            try:
                widget.configure(
                    troughcolor=cls.COLORS["active_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _apply_menu_colors(cls, widget: tk.Misc, config_options: dict) -> None:
        """Apply Menu-specific colors"""
        if "activebackground" in config_options:
            try:
                widget.configure(
                    activebackground=cls.COLORS["select_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass
        if "activeforeground" in config_options:
            try:
                widget.configure(
                    activeforeground=cls.COLORS["select_fg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _apply_to_children(cls, parent: tk.Misc) -> None:
        """Recursively apply theme to all children"""
        try:
            for child in parent.winfo_children():
                cls._apply_to_widget(child)
                cls._apply_to_children(child)
        except tk.TclError:
            # Parent was destroyed
            pass

    @classmethod
    def remove(cls, root: tk.Tk) -> None:
        """Remove high contrast theme and restore defaults"""
        if root not in cls._themed_roots:
            return  # Not themed

        # Remove from themed roots
        cls._themed_roots.discard(root)

        # Clear the option database completely
        try:
            root.option_clear()
        except tk.TclError:
            # Option database may not be available or root may be destroyed
            pass

        # Restore original option database values
        cls._restore_option_database(root)

        # Reset the root window
        cls._restore_root_window(root)

        # Apply standard colors to all existing widgets
        cls._restore_all_widgets(root)

        # Clean up stored options
        if root in cls._original_options:
            del cls._original_options[root]

    @classmethod
    def _restore_option_database(cls, root: tk.Tk) -> None:
        """Restore original option database values"""
        # Set standard system colors
        standard_colors = cls.STANDARD_COLORS

        # General widget defaults
        root.option_add("*Background", standard_colors["bg"], "startupFile")
        root.option_add("*Foreground", standard_colors["fg"], "startupFile")
        root.option_add(
            "*selectBackground", standard_colors["select_bg"], "startupFile"
        )
        root.option_add(
            "*selectForeground", standard_colors["select_fg"], "startupFile"
        )
        root.option_add(
            "*activeBackground", standard_colors["active_bg"], "startupFile"
        )
        root.option_add(
            "*activeForeground", standard_colors["active_fg"], "startupFile"
        )
        root.option_add(
            "*insertBackground", standard_colors["insert_bg"], "startupFile"
        )
        root.option_add(
            "*disabledForeground", standard_colors["disabled_fg"], "startupFile"
        )
        root.option_add(
            "*disabledBackground", standard_colors["disabled_bg"], "startupFile"
        )

        # Main window
        root.option_add("*Tk.Background", standard_colors["bg"], "startupFile")
        root.option_add("*Tk.Foreground", standard_colors["fg"], "startupFile")

        # Specific widget types
        widget_types = [
            "Button",
            "Label",
            "Entry",
            "Text",
            "Frame",
            "Toplevel",
            "Canvas",
            "Listbox",
            "Scale",
            "Checkbutton",
            "Radiobutton",
            "Menu",
            "Menubutton",
            "Message",
            "Spinbox",
            "PanedWindow",
            "LabelFrame",
            "Scrollbar",
        ]

        for widget_type in widget_types:
            root.option_add(
                f"*{widget_type}.Background", standard_colors["bg"], "startupFile"
            )
            root.option_add(
                f"*{widget_type}.Foreground", standard_colors["fg"], "startupFile"
            )
            root.option_add(
                f"*{widget_type}.selectBackground",
                standard_colors["select_bg"],
                "startupFile",
            )
            root.option_add(
                f"*{widget_type}.selectForeground",
                standard_colors["select_fg"],
                "startupFile",
            )
            root.option_add(
                f"*{widget_type}.activeBackground",
                standard_colors["active_bg"],
                "startupFile",
            )
            root.option_add(
                f"*{widget_type}.activeForeground",
                standard_colors["active_fg"],
                "startupFile",
            )

    @classmethod
    def _restore_root_window(cls, root: tk.Tk) -> None:
        """Restore root window to standard appearance"""
        try:
            root.configure(bg=cls.STANDARD_COLORS["bg"])
            # Reset palette
            try:
                root.tk.call("tk_setPalette", cls.STANDARD_COLORS["bg"])
            except tk.TclError:
                pass
        except tk.TclError:
            pass

    @classmethod
    def _restore_all_widgets(cls, root: tk.Tk) -> None:
        """Restore all widgets to standard appearance"""
        # Restore root first
        cls._restore_widget(root)

        # Then restore all children recursively
        cls._restore_children(root)

        # Force update
        root.update_idletasks()

    @classmethod
    def _restore_widget(cls, widget: tk.Misc) -> None:
        """Restore a single widget to standard appearance"""
        try:
            widget_class = widget.winfo_class()
            standard_colors = cls.STANDARD_COLORS

            # Get all configurable options for this widget
            try:
                config_options = widget.configure()
            except tk.TclError:
                return

            # Restore colors in groups
            cls._restore_basic_colors(widget, config_options, standard_colors)
            cls._restore_selection_colors(widget, config_options, standard_colors)
            cls._restore_active_colors(widget, config_options, standard_colors)
            cls._restore_special_colors(widget, config_options, standard_colors)
            cls._restore_widget_specific_colors(
                widget, widget_class, config_options, standard_colors
            )

            # Force widget to update its appearance
            try:
                widget.update_idletasks()
            except tk.TclError:
                pass

        except (tk.TclError, AttributeError):
            # Widget doesn't support these operations
            pass

    @classmethod
    def _restore_basic_colors(
        cls, widget: tk.Misc, config_options: dict, standard_colors: dict
    ) -> None:
        """Restore basic background and foreground colors"""
        if "background" in config_options or "bg" in config_options:
            try:
                widget.configure(bg=standard_colors["bg"])  # type: ignore[call-arg]
            except tk.TclError:
                pass

        if "foreground" in config_options or "fg" in config_options:
            try:
                widget.configure(fg=standard_colors["fg"])  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _restore_selection_colors(
        cls, widget: tk.Misc, config_options: dict, standard_colors: dict
    ) -> None:
        """Restore selection colors"""
        if "selectbackground" in config_options:
            try:
                widget.configure(
                    selectbackground=standard_colors["select_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

        if "selectforeground" in config_options:
            try:
                widget.configure(
                    selectforeground=standard_colors["select_fg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _restore_active_colors(
        cls, widget: tk.Misc, config_options: dict, standard_colors: dict
    ) -> None:
        """Restore active colors"""
        if "activebackground" in config_options:
            try:
                widget.configure(
                    activebackground=standard_colors["active_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

        if "activeforeground" in config_options:
            try:
                widget.configure(
                    activeforeground=standard_colors["active_fg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _restore_special_colors(
        cls, widget: tk.Misc, config_options: dict, standard_colors: dict
    ) -> None:
        """Restore special colors like insert and disabled"""
        if "insertbackground" in config_options:
            try:
                widget.configure(
                    insertbackground=standard_colors["insert_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

        if "disabledforeground" in config_options:
            try:
                widget.configure(
                    disabledforeground=standard_colors["disabled_fg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

        if "disabledbackground" in config_options:
            try:
                widget.configure(
                    disabledbackground=standard_colors["disabled_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _restore_widget_specific_colors(
        cls,
        widget: tk.Misc,
        widget_class: str,
        config_options: dict,
        standard_colors: dict,
    ) -> None:
        """Restore widget-specific colors"""
        if widget_class == "Entry":
            cls._restore_entry_colors(widget, config_options, standard_colors)
        elif widget_class == "Scale":
            cls._restore_scale_colors(widget, config_options, standard_colors)
        elif widget_class in ["Checkbutton", "Radiobutton"]:
            cls._restore_button_colors(widget, config_options, standard_colors)
        elif widget_class == "Scrollbar":
            cls._restore_scrollbar_colors(widget, config_options, standard_colors)

    @classmethod
    def _restore_entry_colors(
        cls, widget: tk.Misc, config_options: dict, standard_colors: dict
    ) -> None:
        """Restore Entry-specific colors"""
        if "fieldbackground" in config_options:
            try:
                widget.configure(
                    fieldbackground=standard_colors["bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _restore_scale_colors(
        cls, widget: tk.Misc, config_options: dict, standard_colors: dict
    ) -> None:
        """Restore Scale-specific colors"""
        if "troughcolor" in config_options:
            try:
                widget.configure(
                    troughcolor=standard_colors["active_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _restore_button_colors(
        cls, widget: tk.Misc, config_options: dict, standard_colors: dict
    ) -> None:
        """Restore Checkbutton/Radiobutton-specific colors"""
        if "selectcolor" in config_options:
            try:
                widget.configure(
                    selectcolor=standard_colors["select_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _restore_scrollbar_colors(
        cls, widget: tk.Misc, config_options: dict, standard_colors: dict
    ) -> None:
        """Restore Scrollbar-specific colors"""
        if "troughcolor" in config_options:
            try:
                widget.configure(
                    troughcolor=standard_colors["active_bg"]
                )  # type: ignore[call-arg]
            except tk.TclError:
                pass

    @classmethod
    def _restore_children(cls, parent: tk.Misc) -> None:
        """Recursively restore all children to standard appearance"""
        try:
            for child in parent.winfo_children():
                cls._restore_widget(child)
                cls._restore_children(child)
        except tk.TclError:
            # Parent was destroyed
            pass

    @classmethod
    def is_applied(cls, root: tk.Tk) -> bool:
        """Check if high contrast theme is applied to a root window"""
        return root in cls._themed_roots


class AccessibilityFontManager:
    """Manages accessibility-friendly fonts and font settings"""

    # Dyslexic-friendly fonts in order of preference
    DYSLEXIC_FONTS = [
        "OpenDyslexic",
        "OpenDyslexic-Regular",
        "Dyslexie",
        "Lexie Readable",
        "Comic Sans MS",  # Often helpful for dyslexic users
        "Verdana",  # Good fallback
        "Arial",  # Common fallback
        "Helvetica",  # Mac fallback
        "sans-serif",  # Generic fallback
    ]

    # High-readability fonts
    READABLE_FONTS = [
        "Atkinson Hyperlegible",
        "Inter",
        "Source Sans Pro",
        "Roboto",
        "Lato",
        "Open Sans",
        "Verdana",
        "Arial",
        "Helvetica",
        "sans-serif",
    ]

    # Minimum font sizes for accessibility (in points)
    MIN_FONT_SIZES = {"normal": 12, "large": 14, "extra_large": 16}

    def __init__(self, root: tk.Tk):
        self.root = root
        self._applied_fonts: Dict[tk.Widget, tuple] = {}
        self._original_fonts: Dict[tk.Widget, tuple] = {}
        self._font_scale = 1.0

    def get_available_fonts(self) -> List[str]:
        """Get list of available system fonts"""
        try:
            return list(self.root.tk.call("font", "families"))
        except tk.TclError:
            return []

    def find_best_font(self, preferred_fonts: List[str]) -> str:
        """Find the best available font from a preference list"""
        available_fonts = self.get_available_fonts()

        for font in preferred_fonts:
            if font in available_fonts:
                return font

        # Return first available font as ultimate fallback
        return available_fonts[0] if available_fonts else "TkDefaultFont"

    def apply_dyslexic_font(self, size: int = 12, weight: str = "normal") -> None:
        """Apply dyslexic-friendly font to all widgets"""
        font_family = self.find_best_font(self.DYSLEXIC_FONTS)

        # Ensure minimum size for accessibility
        size = max(size, self.MIN_FONT_SIZES["normal"])

        font_config = (font_family, int(size * self._font_scale), weight)
        self._apply_font_to_all_widgets(font_config)

    def apply_readable_font(self, size: int = 12, weight: str = "normal") -> None:
        """Apply high-readability font to all widgets"""
        font_family = self.find_best_font(self.READABLE_FONTS)

        # Ensure minimum size for accessibility
        size = max(size, self.MIN_FONT_SIZES["normal"])

        font_config = (font_family, int(size * self._font_scale), weight)
        self._apply_font_to_all_widgets(font_config)

    def set_font_scale(self, scale: float) -> None:
        """Set global font scale factor"""
        self._font_scale = max(0.5, min(scale, 3.0))  # Limit scale between 0.5x and 3x

        # Reapply current fonts with new scale
        for widget, (family, size, weight) in self._applied_fonts.items():
            try:
                new_size = int(size * self._font_scale)
                new_config = (family, new_size, weight)
                widget.configure(font=new_config)
                self._applied_fonts[widget] = new_config
            except tk.TclError:
                # Widget may have been destroyed
                pass

    def increase_font_size(self, increment: int = 2) -> None:
        """Increase font size for all widgets"""
        for widget, (family, size, weight) in self._applied_fonts.items():
            try:
                new_size = size + increment
                new_config = (family, new_size, weight)
                widget.configure(font=new_config)
                self._applied_fonts[widget] = new_config
            except tk.TclError:
                pass

    def decrease_font_size(self, decrement: int = 2) -> None:
        """Decrease font size for all widgets (with minimum limit)"""
        for widget, (family, size, weight) in self._applied_fonts.items():
            try:
                new_size = max(size - decrement, self.MIN_FONT_SIZES["normal"])
                new_config = (family, new_size, weight)
                widget.configure(font=new_config)
                self._applied_fonts[widget] = new_config
            except tk.TclError:
                pass

    def apply_large_text(self) -> None:
        """Apply large text sizes for low vision users"""
        for widget, (family, _, weight) in self._applied_fonts.items():
            try:
                new_size = self.MIN_FONT_SIZES["large"]
                new_config = (family, int(new_size * self._font_scale), weight)
                widget.configure(font=new_config)
                self._applied_fonts[widget] = new_config
            except tk.TclError:
                pass

    def apply_extra_large_text(self) -> None:
        """Apply extra large text sizes for severe low vision"""
        for widget, (family, _, weight) in self._applied_fonts.items():
            try:
                new_size = self.MIN_FONT_SIZES["extra_large"]
                new_config = (family, int(new_size * self._font_scale), weight)
                widget.configure(font=new_config)
                self._applied_fonts[widget] = new_config
            except tk.TclError:
                pass

    def restore_original_fonts(self) -> None:
        """Restore original fonts for all widgets"""
        for widget, original_font in self._original_fonts.items():
            try:
                widget.configure(font=original_font)
            except tk.TclError:
                pass

        self._applied_fonts.clear()

    def _apply_font_to_all_widgets(self, font_config: tuple) -> None:
        """Apply font configuration to all widgets"""
        self._apply_font_to_widget(self.root, font_config)
        self._apply_font_to_children(self.root, font_config)

    def _apply_font_to_widget(self, widget: tk.Widget, font_config: tuple) -> None:
        """Apply font to a single widget"""
        try:
            # Store original font if not already stored
            if widget not in self._original_fonts:
                try:
                    current_font = widget.cget("font")
                    self._original_fonts[widget] = current_font
                except tk.TclError:
                    self._original_fonts[widget] = "TkDefaultFont"

            # Apply new font
            widget.configure(font=font_config)
            self._applied_fonts[widget] = font_config

        except tk.TclError:
            # Widget doesn't support font configuration
            pass

    def _apply_font_to_children(self, parent: tk.Widget, font_config: tuple) -> None:
        """Recursively apply font to all children"""
        try:
            for child in parent.winfo_children():
                self._apply_font_to_widget(child, font_config)
                self._apply_font_to_children(child, font_config)
        except tk.TclError:
            # Parent was destroyed
            pass

    def get_font_info(self, widget: tk.Widget) -> Dict[str, Any]:
        """Get font information for a widget"""
        try:
            current_font = widget.cget("font")
            if isinstance(current_font, tuple):
                family, size, *style = current_font
                return {
                    "family": family,
                    "size": size,
                    "style": style,
                    "is_accessible_size": size >= self.MIN_FONT_SIZES["normal"],
                }
            else:
                return {
                    "family": str(current_font),
                    "size": "unknown",
                    "style": [],
                    "is_accessible_size": True,  # Assume system fonts are accessible
                }
        except tk.TclError:
            return {
                "family": "unknown",
                "size": "unknown",
                "style": [],
                "is_accessible_size": False,
            }


class ColorBlindnessSupport:
    """Support for color blindness accessibility"""

    # Color palettes safe for different types of color blindness
    COLORBLIND_SAFE_PALETTES = {
        "protanopia": {  # Red-blind
            "primary": "#0173B2",  # Blue
            "secondary": "#DE8F05",  # Orange
            "success": "#029E73",  # Green
            "warning": "#CC78BC",  # Pink
            "danger": "#D55E00",  # Red-orange
            "info": "#56B4E9",  # Light blue
        },
        "deuteranopia": {  # Green-blind
            "primary": "#0173B2",  # Blue
            "secondary": "#DE8F05",  # Orange
            "success": "#029E73",  # Teal
            "warning": "#CC78BC",  # Pink
            "danger": "#D55E00",  # Red-orange
            "info": "#56B4E9",  # Light blue
        },
        "tritanopia": {  # Blue-blind
            "primary": "#D55E00",  # Red-orange
            "secondary": "#009E73",  # Green
            "success": "#F0E442",  # Yellow
            "warning": "#CC79A7",  # Pink
            "danger": "#E69F00",  # Orange
            "info": "#999999",  # Gray
        },
        "universal": {  # Safe for all types
            "primary": "#0173B2",  # Blue
            "secondary": "#DE8F05",  # Orange
            "success": "#029E73",  # Green
            "warning": "#F0E442",  # Yellow
            "danger": "#D55E00",  # Red-orange
            "info": "#56B4E9",  # Light blue
        },
    }

    @classmethod
    def get_safe_palette(cls, colorblind_type: str = "universal") -> Dict[str, str]:
        """Get color palette safe for specified type of color blindness"""
        return cls.COLORBLIND_SAFE_PALETTES.get(
            colorblind_type, cls.COLORBLIND_SAFE_PALETTES["universal"]
        )

    @classmethod
    def apply_colorblind_safe_theme(
        cls, root: tk.Tk, colorblind_type: str = "universal"
    ) -> None:
        """Apply colorblind-safe theme to application"""
        palette = cls.get_safe_palette(colorblind_type)

        # Apply colors using option database
        root.option_add("*selectBackground", palette["primary"], "startupFile")
        root.option_add("*activeBackground", palette["secondary"], "startupFile")
        root.option_add("*Button.activeBackground", palette["primary"], "startupFile")


# Global font manager instance
_font_manager: Optional[AccessibilityFontManager] = None


def get_font_manager(root: tk.Tk) -> AccessibilityFontManager:
    """Get or create global font manager"""
    global _font_manager
    if _font_manager is None:
        _font_manager = AccessibilityFontManager(root)
    return _font_manager


def set_dyslexic_font(
    root: tk.Tk, family: str = "", size: int = 12, weight: str = "normal"
) -> None:
    """
    Apply dyslexic-friendly font to root and all children.
    If family is not specified, automatically selects the best available dyslexic font.
    """
    font_manager = get_font_manager(root)

    if family:
        # Use specified font with fallback
        available_fonts = font_manager.get_available_fonts()
        if family not in available_fonts:
            family = font_manager.find_best_font(
                AccessibilityFontManager.DYSLEXIC_FONTS
            )

        # Ensure minimum size
        size = max(size, AccessibilityFontManager.MIN_FONT_SIZES["normal"])
        font_config = (family, size, weight)
        font_manager._apply_font_to_all_widgets(font_config)
    else:
        # Use automatic dyslexic font selection
        font_manager.apply_dyslexic_font(size, weight)


def set_readable_font(root: tk.Tk, size: int = 12, weight: str = "normal") -> None:
    """Apply high-readability font optimized for accessibility"""
    font_manager = get_font_manager(root)
    font_manager.apply_readable_font(size, weight)


def set_large_text(root: tk.Tk) -> None:
    """Apply large text sizes for low vision users"""
    font_manager = get_font_manager(root)
    font_manager.apply_large_text()


def set_extra_large_text(root: tk.Tk) -> None:
    """Apply extra large text sizes for severe low vision"""
    font_manager = get_font_manager(root)
    font_manager.apply_extra_large_text()


def increase_font_size(root: tk.Tk, increment: int = 2) -> None:
    """Increase font size for all widgets"""
    font_manager = get_font_manager(root)
    font_manager.increase_font_size(increment)


def decrease_font_size(root: tk.Tk, decrement: int = 2) -> None:
    """Decrease font size for all widgets"""
    font_manager = get_font_manager(root)
    font_manager.decrease_font_size(decrement)


def set_font_scale(root: tk.Tk, scale: float) -> None:
    """Set global font scale factor"""
    font_manager = get_font_manager(root)
    font_manager.set_font_scale(scale)


def apply_colorblind_safe_theme(
    root: tk.Tk, colorblind_type: str = "universal"
) -> None:
    """Apply colorblind-safe color theme"""
    ColorBlindnessSupport.apply_colorblind_safe_theme(root, colorblind_type)


def validate_font_accessibility(root: tk.Tk) -> List[str]:
    """Validate font accessibility across all widgets"""
    font_manager = get_font_manager(root)
    issues = []

    def check_widget_font(widget: tk.Widget) -> None:
        font_info = font_manager.get_font_info(widget)

        if not font_info["is_accessible_size"]:
            issues.append(f"Widget {widget} has font size below accessibility minimum")

        # Check for problematic fonts
        family = font_info["family"].lower()
        if any(problematic in family for problematic in ["times", "serif", "script"]):
            issues.append(
                f"Widget {widget} uses potentially problematic font: {family}"
            )

    def check_children(parent: tk.Widget) -> None:
        try:
            check_widget_font(parent)
            for child in parent.winfo_children():
                check_children(child)
        except tk.TclError:
            pass

    check_children(root)
    return issues


# Legacy function for backward compatibility
def _apply_font_to_widget(widget: tk.Misc, font_config: tuple) -> None:
    """Apply font to a single widget (legacy function)"""
    try:
        widget.configure(font=font_config)  # type: ignore[call-arg]
    except tk.TclError:
        pass


def _apply_font_to_children(parent: tk.Misc, font_config: tuple) -> None:
    """Recursively apply font to all children (legacy function)"""
    try:
        for child in parent.winfo_children():
            _apply_font_to_widget(child, font_config)
            _apply_font_to_children(child, font_config)
    except tk.TclError:
        pass
