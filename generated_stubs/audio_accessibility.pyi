# tkaria11y.audio_accessibility.pyi
# Type stubs for tkaria11y.audio_accessibility

from typing import Any, Dict, List, Optional, Union, Callable, Tuple, Type, Set
import tkinter as tk
from tkinter import ttk
from enum import Enum
from abc import ABC, abstractmethod

class Any:
    """Special type indicating an unconstrained type."""

    def __init__(self: Any, args: Any, kwargs: Any) -> Any: ...

class AudioAccessibilityManager:
    """Manages audio accessibility features for widgets"""

    def __init__(self: Any, root: Tk) -> Any: ...
    def add_audio_callback(self: Any, event_type: str, callback: Callable) -> None: ...
    def get_audio_info(self: Any) -> Dict: ...
    def is_audio_available(self: Any) -> bool: ...
    def play_cue_for_widget(
        self: Any, widget: Widget, cue_type: AudioCueType
    ) -> None: ...
    def play_error_sound(self: Any) -> None: ...
    def play_notification_sound(self: Any) -> None: ...
    def play_success_sound(self: Any) -> None: ...
    def play_warning_sound(self: Any) -> None: ...
    def remove_audio_callback(
        self: Any, event_type: str, callback: Callable
    ) -> None: ...
    def set_audio_enabled(self: Any, enabled: bool) -> None: ...
    def set_cue_volume(self: Any, volume: float) -> None: ...
    def set_master_volume(self: Any, volume: float) -> None: ...
    def set_spatial_audio_enabled(self: Any, enabled: bool) -> None: ...
    def shutdown(self: Any) -> None: ...

class AudioCue:
    """Represents an audio cue"""

    pattern: str
    spatial_position: None

    def __init__(
        self: Any,
        cue_type: AudioCueType,
        frequency: float,
        duration: float,
        volume: float,
        pattern: str = ...,
        spatial_position: Optional = ...,
    ) -> None: ...

class AudioCueType(Enum):
    FOCUS_CHANGE: str
    BUTTON_PRESS: str
    CHECKBOX_CHECK: str
    CHECKBOX_UNCHECK: str
    MENU_OPEN: str
    MENU_CLOSE: str
    ERROR: str
    WARNING: str
    SUCCESS: str
    NOTIFICATION: str
    PROGRESS_UPDATE: str
    TEXT_INPUT: str
    SELECTION_CHANGE: str
    WINDOW_OPEN: str
    WINDOW_CLOSE: str
    TAB_CHANGE: str
    SCROLL: str
    DRAG_START: str
    DRAG_END: str
    DROP: str

class AudioEngine:
    """Audio engine for accessibility sounds"""

    def __init__(self: Any) -> Any: ...
    def configure_spatial_audio(
        self: Any,
        head_width: float = ...,
        sound_speed: float = ...,
        max_delay: float = ...,
    ) -> None: ...
    def get_cue_definition(self: Any, cue_type: AudioCueType) -> Optional: ...
    def get_cue_volume(self: Any) -> float: ...
    def get_master_volume(self: Any) -> float: ...
    def is_audio_available(self: Any) -> bool: ...
    def is_audio_enabled(self: Any) -> bool: ...
    def is_spatial_audio_enabled(self: Any) -> bool: ...
    def play_cue(
        self: Any, cue_type: AudioCueType, spatial_position: Optional = ...
    ) -> None: ...
    def set_audio_enabled(self: Any, enabled: bool) -> None: ...
    def set_cue_definition(
        self: Any, cue_type: AudioCueType, cue: AudioCue
    ) -> None: ...
    def set_cue_volume(self: Any, volume: float) -> None: ...
    def set_master_volume(self: Any, volume: float) -> None: ...
    def set_spatial_audio_enabled(self: Any, enabled: bool) -> None: ...
    def shutdown(self: Any) -> None: ...

class Enum:
    """"""

    ...

class SpatialAudioConfig:
    """Configuration for spatial audio"""

    enabled: bool
    head_width: float
    max_delay: float
    sound_speed: float

    def __init__(
        self: Any,
        enabled: bool = ...,
        head_width: float = ...,
        sound_speed: float = ...,
        max_delay: float = ...,
    ) -> None: ...

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
def get_audio_info() -> Dict: ...
def get_audio_manager(root: Tk) -> AudioAccessibilityManager: ...
def is_audio_available() -> bool: ...

math: Any
os: Any

def play_audio_cue(cue_type: AudioCueType, widget: Optional = ...) -> None: ...
def play_error_sound() -> None: ...
def play_notification_sound() -> None: ...
def play_success_sound() -> None: ...
def play_warning_sound() -> None: ...

queue: Any

def set_audio_enabled(enabled: bool) -> None: ...
def set_audio_volume(master_volume: float, cue_volume: float) -> None: ...
def set_spatial_audio_enabled(enabled: bool) -> None: ...
def setup_audio_accessibility(
    root: Tk,
    enable_spatial: bool = ...,
    master_volume: float = ...,
    cue_volume: float = ...,
) -> None: ...
def shutdown_audio_accessibility() -> None: ...

sys: Any
threading: Any
time: Any
tk: Any
