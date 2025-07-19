# tka11y/__init__.py
__version__ = "0.0.1"

"""4. Registering in __init__.py"""

from .a11y_engine import tts, speak
from .app import AccessibleApp
from .widgets import (
    AccessibleButton,
    AccessibleEntry,
    AccessibleLabel,
    AccessibleCheckbutton,
    AccessibleRadiobutton,
    AccessibleScale,
    AccessibleListbox,
    AccessibleFrame,
)
from .utils import configure_focus_traversal
from .themes import HighContrastTheme, set_dyslexic_font

# Import widgets module to get __all__
from . import widgets

__all__ = [
    "tts",
    "speak",
    "AccessibleApp",
    "configure_focus_traversal",
    "HighContrastTheme",
    "set_dyslexic_font",
] + widgets.__all__
# Ensure widgets are registered for type stubs
"""This gives users a single import point:

from tkaria11y import AccessibleApp, AccessibleButton, AccessibleEntry """
