# tkaria11y/themes.py

"""
Theme utilities for accessibility:
- HighContrastTheme: Apply high-contrast colors
- set_dyslexic_font: Apply dyslexic-friendly fonts
"""

import tkinter as tk
from typing import Dict
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
                    # This is tricky - Tkinter doesn't provide easy access to
                    # current option values
                    # We'll store the standard system colors as defaults
                    if "Background" in option:
                        cls._original_options[root][option] = cls.STANDARD_COLORS["bg"]
                    elif "Foreground" in option:
                        cls._original_options[root][option] = cls.STANDARD_COLORS["fg"]
                    elif "select" in option.lower():
                        if "Background" in option:
                            cls._original_options[root][option] = cls.STANDARD_COLORS[
                                "select_bg"
                            ]
                        else:
                            cls._original_options[root][option] = cls.STANDARD_COLORS[
                                "select_fg"
                            ]
                    elif "active" in option.lower():
                        if "Background" in option:
                            cls._original_options[root][option] = cls.STANDARD_COLORS[
                                "active_bg"
                            ]
                        else:
                            cls._original_options[root][option] = cls.STANDARD_COLORS[
                                "active_fg"
                            ]
                    elif "insert" in option.lower():
                        cls._original_options[root][option] = cls.STANDARD_COLORS[
                            "insert_bg"
                        ]
                    elif "disabled" in option.lower():
                        if "Background" in option:
                            cls._original_options[root][option] = cls.STANDARD_COLORS[
                                "disabled_bg"
                            ]
                        else:
                            cls._original_options[root][option] = cls.STANDARD_COLORS[
                                "disabled_fg"
                            ]
                except (KeyError, AttributeError, tk.TclError):
                    # Skip if option doesn't exist or can't be accessed
                    pass

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
        # Store original bind_class method
        if not hasattr(root, "_original_bind_class"):
            root._original_bind_class = root.bind_class  # type: ignore[attr-defined]

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

            # Apply basic colors if the widget supports them
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

            # Selection colors
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

            # Active colors
            if "activebackground" in config_options:
                try:
                    widget.configure(activebackground=cls.COLORS["active_bg"])  # type: ignore[call-arg]
                except tk.TclError:
                    pass

            if "activeforeground" in config_options:
                try:
                    widget.configure(activeforeground=cls.COLORS["active_fg"])  # type: ignore[call-arg]
                except tk.TclError:
                    pass

            # Insert/cursor color
            if "insertbackground" in config_options:
                try:
                    widget.configure(insertbackground=cls.COLORS["insert_bg"])  # type: ignore[call-arg]
                except tk.TclError:
                    pass

            # Disabled colors
            if "disabledforeground" in config_options:
                try:
                    widget.configure(disabledforeground=cls.COLORS["disabled_fg"])  # type: ignore[call-arg]
                except tk.TclError:
                    pass

            if "disabledbackground" in config_options:
                try:
                    widget.configure(disabledbackground=cls.COLORS["disabled_bg"])  # type: ignore[call-arg]
                except tk.TclError:
                    pass

            # Widget-specific special handling
            if widget_class == "Entry":
                if "fieldbackground" in config_options:
                    try:
                        widget.configure(fieldbackground=cls.COLORS["bg"])  # type: ignore[call-arg]
                    except tk.TclError:
                        pass

            elif widget_class == "Scale":
                if "troughcolor" in config_options:
                    try:
                        widget.configure(troughcolor=cls.COLORS["active_bg"])  # type: ignore[call-arg]
                    except tk.TclError:
                        pass

            elif widget_class in ["Checkbutton", "Radiobutton"]:
                if "selectcolor" in config_options:
                    try:
                        widget.configure(selectcolor=cls.COLORS["select_bg"])  # type: ignore[call-arg]
                    except tk.TclError:
                        pass

            elif widget_class == "Scrollbar":
                if "troughcolor" in config_options:
                    try:
                        widget.configure(troughcolor=cls.COLORS["active_bg"])  # type: ignore[call-arg]
                    except tk.TclError:
                        pass

            elif widget_class == "Menu":
                # Menus need special handling
                if "activebackground" in config_options:
                    try:
                        widget.configure(activebackground=cls.COLORS["select_bg"])  # type: ignore[call-arg]
                    except tk.TclError:
                        pass
                if "activeforeground" in config_options:
                    try:
                        widget.configure(activeforeground=cls.COLORS["select_fg"])  # type: ignore[call-arg]
                    except tk.TclError:
                        pass

            # Force widget to update its appearance
            try:
                widget.update_idletasks()
            except tk.TclError:
                pass

        except (tk.TclError, AttributeError):
            # Widget doesn't support these operations
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

            # Restore basic colors if the widget supports them
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

            # Restore selection colors
            if "selectbackground" in config_options:
                try:
                    widget.configure(selectbackground=standard_colors["select_bg"])  # type: ignore[call-arg]
                except tk.TclError:
                    pass

            if "selectforeground" in config_options:
                try:
                    widget.configure(selectforeground=standard_colors["select_fg"])  # type: ignore[call-arg]
                except tk.TclError:
                    pass

            # Restore active colors
            if "activebackground" in config_options:
                try:
                    widget.configure(activebackground=standard_colors["active_bg"])  # type: ignore[call-arg]
                except tk.TclError:
                    pass

            if "activeforeground" in config_options:
                try:
                    widget.configure(activeforeground=standard_colors["active_fg"])  # type: ignore[call-arg]
                except tk.TclError:
                    pass

            # Restore insert/cursor color
            if "insertbackground" in config_options:
                try:
                    widget.configure(insertbackground=standard_colors["insert_bg"])  # type: ignore[call-arg]
                except tk.TclError:
                    pass

            # Restore disabled colors
            if "disabledforeground" in config_options:
                try:
                    widget.configure(disabledforeground=standard_colors["disabled_fg"])  # type: ignore[call-arg]
                except tk.TclError:
                    pass

            if "disabledbackground" in config_options:
                try:
                    widget.configure(disabledbackground=standard_colors["disabled_bg"])  # type: ignore[call-arg]
                except tk.TclError:
                    pass

            # Widget-specific restoration
            if widget_class == "Entry":
                if "fieldbackground" in config_options:
                    try:
                        widget.configure(fieldbackground=standard_colors["bg"])  # type: ignore[call-arg]
                    except tk.TclError:
                        pass

            elif widget_class == "Scale":
                if "troughcolor" in config_options:
                    try:
                        widget.configure(troughcolor=standard_colors["active_bg"])  # type: ignore[call-arg]
                    except tk.TclError:
                        pass

            elif widget_class in ["Checkbutton", "Radiobutton"]:
                if "selectcolor" in config_options:
                    try:
                        widget.configure(selectcolor=standard_colors["select_bg"])  # type: ignore[call-arg]
                    except tk.TclError:
                        pass

            elif widget_class == "Scrollbar":
                if "troughcolor" in config_options:
                    try:
                        widget.configure(troughcolor=standard_colors["active_bg"])  # type: ignore[call-arg]
                    except tk.TclError:
                        pass

            # Force widget to update its appearance
            try:
                widget.update_idletasks()
            except tk.TclError:
                pass

        except (tk.TclError, AttributeError):
            # Widget doesn't support these operations
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


def set_dyslexic_font(
    root: tk.Tk, family: str = "OpenDyslexic", size: int = 12
) -> None:
    """
    Apply dyslexic-friendly font to root and all children.
    Falls back to common fonts if OpenDyslexic is not available.
    """
    # Fallback fonts if OpenDyslexic is not available
    fallback_fonts = ["Arial", "Helvetica", "sans-serif"]

    # Try to use the requested font, fall back if not available
    available_fonts = root.tk.call("font", "families")
    if family not in available_fonts:
        for fallback in fallback_fonts:
            if fallback in available_fonts:
                family = fallback
                break

    font_config = (family, size)
    _apply_font_to_widget(root, font_config)
    _apply_font_to_children(root, font_config)


def _apply_font_to_widget(widget: tk.Misc, font_config: tuple) -> None:
    """Apply font to a single widget"""
    try:
        widget.configure(font=font_config)  # type: ignore[call-arg]
    except tk.TclError:
        pass


def _apply_font_to_children(parent: tk.Misc, font_config: tuple) -> None:
    """Recursively apply font to all children"""
    for child in parent.winfo_children():
        _apply_font_to_widget(child, font_config)
        _apply_font_to_children(child, font_config)
