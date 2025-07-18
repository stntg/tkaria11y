# tkaria11y/app.py

"""
AccessibleApp:
Tk root wrapper—sets title, scaling, high-contrast theme, and inspector.
"""

import tkinter as tk
from .utils import configure_focus_traversal
from .themes import HighContrastTheme, set_dyslexic_font
from .utils_inspector import launch_inspector
from .a11y_engine import shutdown_tts


class AccessibleApp(tk.Tk):
    def __init__(
        self,
        *,
        title: str = "",
        high_contrast: bool = False,
        dyslexic_font: bool = False,
        scaling: float = 1.0,
        enable_inspector: bool = False
    ):
        super().__init__()
        if title:
            self.title(title)
        self.tk.call("tk", "scaling", scaling)

        # Store theme preferences
        self._high_contrast_enabled = False
        self._dyslexic_font_enabled = False

        if high_contrast:
            self.enable_high_contrast()
        if dyslexic_font:
            self.enable_dyslexic_font()

        configure_focus_traversal(self)

        if enable_inspector:
            launch_inspector(self)

        # Register cleanup handler for TTS
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def enable_high_contrast(self) -> None:
        """Enable high contrast theme"""
        if not self._high_contrast_enabled:
            HighContrastTheme.apply(self)
            self._high_contrast_enabled = True

    def disable_high_contrast(self) -> None:
        """Disable high contrast theme"""
        if self._high_contrast_enabled:
            HighContrastTheme.remove(self)
            self._high_contrast_enabled = False

    def toggle_high_contrast(self) -> bool:
        """Toggle high contrast theme on/off. Returns new state."""
        if self._high_contrast_enabled:
            self.disable_high_contrast()
        else:
            self.enable_high_contrast()
        return self._high_contrast_enabled

    def is_high_contrast_enabled(self) -> bool:
        """Check if high contrast theme is enabled"""
        return self._high_contrast_enabled

    def enable_dyslexic_font(self) -> None:
        """Enable dyslexic-friendly font"""
        if not self._dyslexic_font_enabled:
            set_dyslexic_font(self)
            self._dyslexic_font_enabled = True

    def disable_dyslexic_font(self) -> None:
        """Disable dyslexic-friendly font (reset to system default)"""
        if self._dyslexic_font_enabled:
            # Reset to system default font
            set_dyslexic_font(self, family="TkDefaultFont", size=9)
            self._dyslexic_font_enabled = False

    def toggle_dyslexic_font(self) -> bool:
        """Toggle dyslexic-friendly font on/off. Returns new state."""
        if self._dyslexic_font_enabled:
            self.disable_dyslexic_font()
        else:
            self.enable_dyslexic_font()
        return self._dyslexic_font_enabled

    def is_dyslexic_font_enabled(self) -> bool:
        """Check if dyslexic-friendly font is enabled"""
        return self._dyslexic_font_enabled

    def _on_closing(self) -> None:
        """Handle application closing to ensure proper TTS cleanup"""
        try:
            shutdown_tts()
        except (RuntimeError, AttributeError):
            # TTS engine may already be shut down or not initialized
            pass
        self.destroy()
