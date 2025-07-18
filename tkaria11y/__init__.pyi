from .a11y_engine import tts as tts, speak as speak
from .app import AccessibleApp as AccessibleApp
from .utils import configure_focus_traversal as configure_focus_traversal
from .themes import (
    HighContrastTheme as HighContrastTheme,
    set_dyslexic_font as set_dyslexic_font,
)
from .widgets import (
    AccessibleButton as AccessibleButton,
    AccessibleEntry as AccessibleEntry,
    AccessibleLabel as AccessibleLabel,
    AccessibleCheckbutton as AccessibleCheckbutton,
    AccessibleRadiobutton as AccessibleRadiobutton,
    AccessibleScale as AccessibleScale,
    AccessibleListbox as AccessibleListbox,
    AccessibleFrame as AccessibleFrame,
)

__version__: str
