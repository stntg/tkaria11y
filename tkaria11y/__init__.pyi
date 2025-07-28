# tkaria11y/__init__.pyi
# Type stubs for tkaria11y main module

from typing import Any, Optional
import tkinter as tk

# Version info
__version__: str

# Main accessibility functions
def init_tts() -> None: ...
def shutdown_tts() -> None: ...

class AccessibleApp(tk.Tk):
    """Main accessible application class"""

    def __init__(
        self,
        title: str = ...,
        high_contrast: bool = ...,
        dyslexic_font: bool = ...,
        scaling: float = ...,
        enable_inspector: bool = ...,
    ) -> None: ...
    def announce(self, message: str, priority: str = ...) -> None: ...
    def set_theme(self, theme_name: str) -> None: ...
    def enable_high_contrast(self) -> None: ...
    def disable_high_contrast(self) -> None: ...
    def set_scaling(self, factor: float) -> None: ...

# Re-exports from submodules
from .widgets import *
from .mixins import *
from .themes import *
from .utils import *
