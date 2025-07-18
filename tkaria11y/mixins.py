# tkaria11y/mixins.py

"""
AccessibleMixin:
Adds accessible_name, accessible_role, accessible_description,
binds TTS on FocusIn and logical tab traversal.
"""

import tkinter as tk
from typing import Any
from .a11y_engine import speak


class AccessibleMixin:
    def __init__(
        self,
        *args: Any,
        accessible_name: str = "",
        accessible_role: str = "",
        accessible_description: str = "",
        **kwargs: Any,
    ) -> None:
        self.accessible_name = accessible_name
        self.accessible_role = accessible_role
        self.accessible_description = accessible_description

        super().__init__(*args, **kwargs)

        # Bind focus event for TTS
        if accessible_name:
            self.bind("<FocusIn>", self._on_focus_in, add="+")  # type: ignore[attr-defined]
        # Optional: mouse hover
        self.bind("<Enter>", self._on_mouse_enter, add="+")  # type: ignore[attr-defined]

    def _on_focus_in(self, event: tk.Event) -> None:
        label = self.accessible_name
        if self.accessible_description:
            label += f", {self.accessible_description}"
        speak(label)

    def _on_mouse_enter(self, event: tk.Event) -> None:
        # Speak shorter name on hover
        speak(self.accessible_name)
