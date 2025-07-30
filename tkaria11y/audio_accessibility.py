# tkaria11y/audio_accessibility.py

"""
Comprehensive audio accessibility support for tkaria11y.
Provides audio cues, sound feedback, spatial audio, and hearing accessibility features.
"""

import tkinter as tk
import threading
import time
import queue
import math
from typing import Dict, List, Optional, Callable, Any, Tuple, TYPE_CHECKING
from enum import Enum
from dataclasses import dataclass

if TYPE_CHECKING:
    try:
        import numpy
    except ImportError:
        numpy = None  # type: ignore
import sys


class AudioCueType(Enum):
    """Types of audio cues"""

    FOCUS_CHANGE = "focus_change"
    BUTTON_PRESS = "button_press"
    CHECKBOX_CHECK = "checkbox_check"
    CHECKBOX_UNCHECK = "checkbox_uncheck"
    MENU_OPEN = "menu_open"
    MENU_CLOSE = "menu_close"
    ERROR = "error"
    WARNING = "warning"
    SUCCESS = "success"
    NOTIFICATION = "notification"
    PROGRESS_UPDATE = "progress_update"
    TEXT_INPUT = "text_input"
    SELECTION_CHANGE = "selection_change"
    WINDOW_OPEN = "window_open"
    WINDOW_CLOSE = "window_close"
    TAB_CHANGE = "tab_change"
    SCROLL = "scroll"
    DRAG_START = "drag_start"
    DRAG_END = "drag_end"
    DROP = "drop"


@dataclass
class AudioCue:
    """Represents an audio cue"""

    cue_type: AudioCueType
    frequency: float  # Hz
    duration: float  # seconds
    volume: float  # 0.0 to 1.0
    pattern: str = "tone"  # tone, beep, click, etc.
    spatial_position: Optional[Tuple[float, float]] = None  # (x, y) for spatial audio


@dataclass
class SpatialAudioConfig:
    """Configuration for spatial audio"""

    enabled: bool = False
    head_width: float = 0.18  # meters, average human head width
    sound_speed: float = 343.0  # m/s, speed of sound in air
    max_delay: float = 0.0006  # maximum interaural time difference


class AudioEngine:
    """Audio engine for accessibility sounds"""

    def __init__(self) -> None:
        self._audio_available = False
        self._audio_module: Optional[str] = None
        self._init_audio()

        # Audio settings
        self._master_volume = 0.7
        self._cue_volume = 0.5
        self._spatial_audio = SpatialAudioConfig()
        self._audio_enabled = True

        # Audio cue definitions
        self._audio_cues = self._create_default_cues()

        # Audio queue and processing
        self._audio_queue: queue.Queue = queue.Queue()
        self._worker_thread: Optional[threading.Thread] = None
        self._running = False

        # Frequency and tone generation
        self._sample_rate = 44100
        self._bit_depth = 16

        self._start_audio_worker()

    def _init_audio(self) -> None:
        """Initialize audio system"""
        # Try different audio libraries in order of preference
        audio_libs = [
            ("pygame", self._init_pygame),
            ("pyaudio", self._init_pyaudio),
            ("winsound", self._init_winsound),
            ("ossaudiodev", self._init_oss),
        ]

        for lib_name, init_func in audio_libs:
            try:
                if init_func():
                    print(f"Audio initialized with {lib_name}")
                    self._audio_available = True
                    break
            except Exception:
                continue

        if not self._audio_available:
            print("Warning: No audio system available for accessibility sounds")

    def _init_pygame(self) -> bool:
        """Initialize pygame audio"""
        try:
            import pygame

            pygame.mixer.pre_init(
                frequency=self._sample_rate, size=-self._bit_depth, channels=2
            )
            pygame.mixer.init()
            self._audio_module = pygame
            return True
        except ImportError:
            return False

    def _init_pyaudio(self) -> bool:
        """Initialize PyAudio"""
        try:
            import pyaudio
            import numpy as np

            self._pyaudio = pyaudio.PyAudio()
            self._audio_module = "pyaudio"
            self._numpy = np
            return True
        except ImportError:
            return False

    def _init_winsound(self) -> bool:
        """Initialize Windows sound (Windows only)"""
        if sys.platform.startswith("win"):
            try:
                import winsound

                self._audio_module = "winsound"
                return True
            except ImportError:
                return False
        return False  # type: ignore[unreachable]

    def _init_oss(self) -> bool:
        """Initialize OSS audio (Linux only)"""
        if sys.platform.startswith("linux"):
            try:
                import ossaudiodev

                self._audio_module = ossaudiodev
                return True
            except ImportError:
                return False
        return False

    def _create_default_cues(self) -> Dict[AudioCueType, AudioCue]:
        """Create default audio cues"""
        return {
            AudioCueType.FOCUS_CHANGE: AudioCue(
                AudioCueType.FOCUS_CHANGE, 800, 0.1, 0.3, "tone"
            ),
            AudioCueType.BUTTON_PRESS: AudioCue(
                AudioCueType.BUTTON_PRESS, 1000, 0.05, 0.4, "click"
            ),
            AudioCueType.CHECKBOX_CHECK: AudioCue(
                AudioCueType.CHECKBOX_CHECK, 1200, 0.08, 0.4, "beep"
            ),
            AudioCueType.CHECKBOX_UNCHECK: AudioCue(
                AudioCueType.CHECKBOX_UNCHECK, 800, 0.08, 0.4, "beep"
            ),
            AudioCueType.MENU_OPEN: AudioCue(
                AudioCueType.MENU_OPEN, 600, 0.15, 0.3, "tone"
            ),
            AudioCueType.MENU_CLOSE: AudioCue(
                AudioCueType.MENU_CLOSE, 400, 0.15, 0.3, "tone"
            ),
            AudioCueType.ERROR: AudioCue(AudioCueType.ERROR, 300, 0.5, 0.6, "buzz"),
            AudioCueType.WARNING: AudioCue(AudioCueType.WARNING, 500, 0.3, 0.5, "beep"),
            AudioCueType.SUCCESS: AudioCue(
                AudioCueType.SUCCESS, 1500, 0.2, 0.4, "chime"
            ),
            AudioCueType.NOTIFICATION: AudioCue(
                AudioCueType.NOTIFICATION, 900, 0.12, 0.4, "tone"
            ),
            AudioCueType.PROGRESS_UPDATE: AudioCue(
                AudioCueType.PROGRESS_UPDATE, 1100, 0.06, 0.2, "tick"
            ),
            AudioCueType.TEXT_INPUT: AudioCue(
                AudioCueType.TEXT_INPUT, 1300, 0.03, 0.2, "click"
            ),
            AudioCueType.SELECTION_CHANGE: AudioCue(
                AudioCueType.SELECTION_CHANGE, 950, 0.08, 0.3, "tone"
            ),
            AudioCueType.WINDOW_OPEN: AudioCue(
                AudioCueType.WINDOW_OPEN, 700, 0.2, 0.4, "chime"
            ),
            AudioCueType.WINDOW_CLOSE: AudioCue(
                AudioCueType.WINDOW_CLOSE, 500, 0.2, 0.4, "chime"
            ),
            AudioCueType.TAB_CHANGE: AudioCue(
                AudioCueType.TAB_CHANGE, 850, 0.1, 0.3, "tone"
            ),
            AudioCueType.SCROLL: AudioCue(AudioCueType.SCROLL, 1000, 0.04, 0.2, "tick"),
            AudioCueType.DRAG_START: AudioCue(
                AudioCueType.DRAG_START, 1200, 0.1, 0.4, "tone"
            ),
            AudioCueType.DRAG_END: AudioCue(
                AudioCueType.DRAG_END, 800, 0.1, 0.4, "tone"
            ),
            AudioCueType.DROP: AudioCue(AudioCueType.DROP, 600, 0.15, 0.5, "thud"),
        }

    def _start_audio_worker(self) -> None:
        """Start audio processing worker thread"""
        if self._worker_thread and self._worker_thread.is_alive():
            return

        self._running = True
        self._worker_thread = threading.Thread(
            target=self._audio_worker_loop, daemon=True
        )
        self._worker_thread.start()

    def _stop_audio_worker(self) -> None:
        """Stop audio processing worker thread"""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=1.0)

    def _audio_worker_loop(self) -> None:
        """Audio worker thread main loop"""
        while self._running:
            try:
                # Get audio cue from queue
                cue, spatial_pos = self._audio_queue.get(timeout=0.1)

                if cue and self._audio_enabled:
                    self._play_audio_cue(cue, spatial_pos)

            except queue.Empty:
                continue
            except Exception:
                # Continue on errors
                time.sleep(0.01)

    def _play_audio_cue(
        self, cue: AudioCue, spatial_pos: Optional[Tuple[float, float]] = None
    ) -> None:
        """Play an audio cue"""
        if not self._audio_available:
            return

        try:
            if self._audio_module == "pygame":
                self._play_pygame_cue(cue, spatial_pos)
            elif self._audio_module == "pyaudio":
                self._play_pyaudio_cue(cue, spatial_pos)
            elif hasattr(self._audio_module, "Beep"):  # winsound
                self._play_winsound_cue(cue)
            elif hasattr(self._audio_module, "open"):  # ossaudiodev
                self._play_oss_cue(cue)

        except Exception:
            # Ignore audio playback errors
            pass

    def _play_pygame_cue(
        self, cue: AudioCue, spatial_pos: Optional[Tuple[float, float]]
    ) -> None:
        """Play audio cue using pygame"""
        import pygame
        import numpy as np

        # Generate audio data
        samples = int(cue.duration * self._sample_rate)
        audio_data = self._generate_audio_data(cue, samples)

        # Apply spatial audio if enabled and position provided
        if self._spatial_audio.enabled and spatial_pos:
            audio_data = self._apply_spatial_audio(audio_data, spatial_pos)

        # Convert to pygame format
        audio_data = (audio_data * 32767).astype(np.int16)

        # Create and play sound
        sound = pygame.sndarray.make_sound(audio_data)
        sound.set_volume(cue.volume * self._master_volume * self._cue_volume)
        sound.play()

    def _play_pyaudio_cue(
        self, cue: AudioCue, spatial_pos: Optional[Tuple[float, float]]
    ) -> None:
        """Play audio cue using PyAudio"""
        import pyaudio

        # Generate audio data
        samples = int(cue.duration * self._sample_rate)
        audio_data = self._generate_audio_data(cue, samples)

        # Apply spatial audio if enabled
        if self._spatial_audio.enabled and spatial_pos:
            audio_data = self._apply_spatial_audio(audio_data, spatial_pos)

        # Convert to bytes
        audio_bytes = (audio_data * 32767).astype(self._numpy.int16).tobytes()

        # Play audio
        stream = self._pyaudio.open(
            format=pyaudio.paInt16,
            channels=2 if self._spatial_audio.enabled else 1,
            rate=self._sample_rate,
            output=True,
        )

        stream.write(audio_bytes)
        stream.stop_stream()
        stream.close()

    def _play_winsound_cue(self, cue: AudioCue) -> None:
        """Play audio cue using Windows sound"""
        import winsound

        # Use system beep with frequency
        frequency = int(cue.frequency)
        duration = int(cue.duration * 1000)  # Convert to milliseconds

        winsound.Beep(frequency, duration)

    def _play_oss_cue(self, cue: AudioCue) -> None:
        """Play audio cue using OSS (Linux)"""
        # Simplified OSS implementation
        # Real implementation would generate and write audio data
        pass

    def _generate_audio_data(self, cue: AudioCue, samples: int) -> Any:
        """Generate audio data for a cue"""
        try:
            import numpy as np
        except ImportError:
            # Return empty array if numpy not available
            return []

        t = np.linspace(0, cue.duration, samples, False)

        if cue.pattern == "tone":
            # Simple sine wave
            audio = np.sin(2 * np.pi * cue.frequency * t)

        elif cue.pattern == "beep":
            # Sine wave with envelope
            envelope = np.exp(-t * 5)  # Exponential decay
            audio = np.sin(2 * np.pi * cue.frequency * t) * envelope

        elif cue.pattern == "click":
            # Short impulse with decay
            envelope = np.exp(-t * 50)
            audio = np.sin(2 * np.pi * cue.frequency * t) * envelope

        elif cue.pattern == "buzz":
            # Square wave for harsh sound
            audio = np.sign(np.sin(2 * np.pi * cue.frequency * t))

        elif cue.pattern == "chime":
            # Multiple harmonics
            audio = (
                np.sin(2 * np.pi * cue.frequency * t)
                + 0.5 * np.sin(2 * np.pi * cue.frequency * 2 * t)
                + 0.25 * np.sin(2 * np.pi * cue.frequency * 3 * t)
            )
            envelope = np.exp(-t * 3)
            audio *= envelope

        elif cue.pattern == "tick":
            # Very short click
            envelope = np.exp(-t * 100)
            audio = np.sin(2 * np.pi * cue.frequency * t) * envelope

        elif cue.pattern == "thud":
            # Low frequency with quick decay
            envelope = np.exp(-t * 20)
            audio = np.sin(2 * np.pi * (cue.frequency * 0.5) * t) * envelope

        else:
            # Default to tone
            audio = np.sin(2 * np.pi * cue.frequency * t)

        # Apply volume
        audio *= cue.volume * self._master_volume * self._cue_volume

        # Ensure audio is in valid range
        audio = np.clip(audio, -1.0, 1.0)

        return audio

    def _apply_spatial_audio(
        self, audio_data: Any, position: Tuple[float, float]
    ) -> Any:
        """Apply spatial audio effects"""
        import numpy as np

        x, y = position

        # Calculate distance from center
        distance = math.sqrt(x * x + y * y)

        # Calculate interaural time difference (ITD)
        # Simplified model: delay based on horizontal position
        max_delay_samples = int(self._spatial_audio.max_delay * self._sample_rate)
        delay_samples = int(x * max_delay_samples)

        # Calculate interaural level difference (ILD)
        # Simplified model: volume difference based on position
        left_gain = 1.0 - max(0, x) * 0.5
        right_gain = 1.0 + min(0, x) * 0.5

        # Apply distance attenuation
        distance_attenuation = 1.0 / (1.0 + distance * 2.0)
        left_gain *= distance_attenuation
        right_gain *= distance_attenuation

        # Create stereo audio
        stereo_audio = np.zeros((len(audio_data), 2))

        # Left channel
        if delay_samples > 0:
            # Delay left channel
            stereo_audio[delay_samples:, 0] = audio_data[:-delay_samples] * left_gain
        else:
            stereo_audio[:, 0] = audio_data * left_gain

        # Right channel
        if delay_samples < 0:
            # Delay right channel
            stereo_audio[-delay_samples:, 1] = audio_data[:delay_samples] * right_gain
        else:
            stereo_audio[:, 1] = audio_data * right_gain

        return stereo_audio

    def play_cue(
        self,
        cue_type: AudioCueType,
        spatial_position: Optional[Tuple[float, float]] = None,
    ) -> None:
        """Play an audio cue"""
        if not self._audio_enabled or cue_type not in self._audio_cues:
            return

        cue = self._audio_cues[cue_type]

        # Override spatial position if provided
        if spatial_position:
            cue.spatial_position = spatial_position

        try:
            self._audio_queue.put_nowait((cue, spatial_position))
        except queue.Full:
            # Queue is full, skip this cue
            pass

    def set_cue_definition(self, cue_type: AudioCueType, cue: AudioCue) -> None:
        """Set custom audio cue definition"""
        self._audio_cues[cue_type] = cue

    def get_cue_definition(self, cue_type: AudioCueType) -> Optional[AudioCue]:
        """Get audio cue definition"""
        return self._audio_cues.get(cue_type)

    def set_master_volume(self, volume: float) -> None:
        """Set master volume (0.0 to 1.0)"""
        self._master_volume = max(0.0, min(1.0, volume))

    def get_master_volume(self) -> float:
        """Get master volume"""
        return self._master_volume

    def set_cue_volume(self, volume: float) -> None:
        """Set audio cue volume (0.0 to 1.0)"""
        self._cue_volume = max(0.0, min(1.0, volume))

    def get_cue_volume(self) -> float:
        """Get audio cue volume"""
        return self._cue_volume

    def set_audio_enabled(self, enabled: bool) -> None:
        """Enable/disable audio cues"""
        self._audio_enabled = enabled

    def is_audio_enabled(self) -> bool:
        """Check if audio cues are enabled"""
        return self._audio_enabled

    def set_spatial_audio_enabled(self, enabled: bool) -> None:
        """Enable/disable spatial audio"""
        self._spatial_audio.enabled = enabled

    def is_spatial_audio_enabled(self) -> bool:
        """Check if spatial audio is enabled"""
        return self._spatial_audio.enabled

    def configure_spatial_audio(
        self,
        head_width: float = 0.18,
        sound_speed: float = 343.0,
        max_delay: float = 0.0006,
    ) -> None:
        """Configure spatial audio parameters"""
        self._spatial_audio.head_width = head_width
        self._spatial_audio.sound_speed = sound_speed
        self._spatial_audio.max_delay = max_delay

    def is_audio_available(self) -> bool:
        """Check if audio system is available"""
        return self._audio_available

    def shutdown(self) -> None:
        """Shutdown audio engine"""
        self._stop_audio_worker()

        if hasattr(self, "_pyaudio"):
            self._pyaudio.terminate()


class AudioAccessibilityManager:
    """Manages audio accessibility features for widgets"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.audio_engine = AudioEngine()
        self._widget_positions: Dict[tk.Widget, Tuple[float, float]] = {}
        self._audio_callbacks: Dict[str, List[Callable]] = {}
        self._setup_widget_tracking()

    def _setup_widget_tracking(self) -> None:
        """Set up automatic widget tracking for audio cues"""
        # Focus events
        self.root.bind_all("<FocusIn>", self._on_focus_in, add="+")

        # Button events
        self.root.bind_all("<Button-1>", self._on_button_press, add="+")

        # Key events
        self.root.bind_all("<KeyPress>", self._on_key_press, add="+")

        # Window events
        self.root.bind("<Map>", self._on_window_open, add="+")
        self.root.bind("<Unmap>", self._on_window_close, add="+")

    def _on_focus_in(self, event: tk.Event) -> None:
        """Handle focus in event"""
        widget = event.widget
        spatial_pos = self._get_widget_spatial_position(widget)
        self.audio_engine.play_cue(AudioCueType.FOCUS_CHANGE, spatial_pos)

        # Call custom callbacks
        self._trigger_callbacks("focus_in", widget)

    def _on_button_press(self, event: tk.Event) -> None:
        """Handle button press event"""
        widget = event.widget
        widget_class = widget.winfo_class()

        spatial_pos = self._get_widget_spatial_position(widget)

        if widget_class in ["Button", "TButton"]:
            self.audio_engine.play_cue(AudioCueType.BUTTON_PRESS, spatial_pos)

        elif widget_class in ["Checkbutton", "TCheckbutton"]:
            # Determine if checking or unchecking
            try:
                var = widget.cget("variable")
                if var:
                    # Check state after the click
                    widget.after(
                        10, lambda: self._check_checkbox_state(widget, spatial_pos)
                    )
            except tk.TclError:
                pass

        # Call custom callbacks
        self._trigger_callbacks("button_press", widget)

    def _check_checkbox_state(
        self, widget: tk.Misc, spatial_pos: Optional[Tuple[float, float]]
    ) -> None:
        """Check checkbox state and play appropriate cue"""
        try:
            var = widget.cget("variable")
            if var and var.get():
                self.audio_engine.play_cue(AudioCueType.CHECKBOX_CHECK, spatial_pos)
            else:
                self.audio_engine.play_cue(AudioCueType.CHECKBOX_UNCHECK, spatial_pos)
        except tk.TclError:
            pass

    def _on_key_press(self, event: tk.Event) -> None:
        """Handle key press event"""
        widget = event.widget

        # Play text input cue for text widgets
        if widget.winfo_class() in ["Entry", "TEntry", "Text"]:
            if event.char and event.char.isprintable():
                spatial_pos = self._get_widget_spatial_position(widget)
                self.audio_engine.play_cue(AudioCueType.TEXT_INPUT, spatial_pos)

        # Call custom callbacks
        self._trigger_callbacks("key_press", widget, event.keysym)

    def _on_window_open(self, event: tk.Event) -> None:
        """Handle window open event"""
        self.audio_engine.play_cue(AudioCueType.WINDOW_OPEN)
        self._trigger_callbacks("window_open", event.widget)

    def _on_window_close(self, event: tk.Event) -> None:
        """Handle window close event"""
        self.audio_engine.play_cue(AudioCueType.WINDOW_CLOSE)
        self._trigger_callbacks("window_close", event.widget)

    def _get_widget_spatial_position(
        self, widget: tk.Misc
    ) -> Optional[Tuple[float, float]]:
        """Get spatial position of widget for 3D audio"""
        if not self.audio_engine.is_spatial_audio_enabled():
            return None

        try:
            # Get widget position relative to root window
            x = widget.winfo_rootx() - self.root.winfo_rootx()
            y = widget.winfo_rooty() - self.root.winfo_rooty()

            # Get root window dimensions
            root_width = self.root.winfo_width()
            root_height = self.root.winfo_height()

            # Normalize to -1.0 to 1.0 range
            norm_x = (x / root_width) * 2.0 - 1.0 if root_width > 0 else 0.0
            norm_y = (y / root_height) * 2.0 - 1.0 if root_height > 0 else 0.0

            return (norm_x, norm_y)

        except tk.TclError:
            return None

    def _trigger_callbacks(self, event_type: str, *args: Any) -> None:
        """Trigger custom callbacks"""
        for callback in self._audio_callbacks.get(event_type, []):
            try:
                callback(*args)
            except Exception:
                # Ignore callback errors
                pass

    def add_audio_callback(self, event_type: str, callback: Callable) -> None:
        """Add custom audio callback"""
        if event_type not in self._audio_callbacks:
            self._audio_callbacks[event_type] = []
        self._audio_callbacks[event_type].append(callback)

    def remove_audio_callback(self, event_type: str, callback: Callable) -> None:
        """Remove custom audio callback"""
        if (
            event_type in self._audio_callbacks
            and callback in self._audio_callbacks[event_type]
        ):
            self._audio_callbacks[event_type].remove(callback)

    def play_cue_for_widget(self, widget: tk.Misc, cue_type: AudioCueType) -> None:
        """Play audio cue for specific widget"""
        spatial_pos = self._get_widget_spatial_position(widget)
        self.audio_engine.play_cue(cue_type, spatial_pos)

    def play_success_sound(self) -> None:
        """Play success sound"""
        self.audio_engine.play_cue(AudioCueType.SUCCESS)

    def play_error_sound(self) -> None:
        """Play error sound"""
        self.audio_engine.play_cue(AudioCueType.ERROR)

    def play_warning_sound(self) -> None:
        """Play warning sound"""
        self.audio_engine.play_cue(AudioCueType.WARNING)

    def play_notification_sound(self) -> None:
        """Play notification sound"""
        self.audio_engine.play_cue(AudioCueType.NOTIFICATION)

    def set_master_volume(self, volume: float) -> None:
        """Set master audio volume"""
        self.audio_engine.set_master_volume(volume)

    def set_cue_volume(self, volume: float) -> None:
        """Set audio cue volume"""
        self.audio_engine.set_cue_volume(volume)

    def set_audio_enabled(self, enabled: bool) -> None:
        """Enable/disable audio cues"""
        self.audio_engine.set_audio_enabled(enabled)

    def set_spatial_audio_enabled(self, enabled: bool) -> None:
        """Enable/disable spatial audio"""
        self.audio_engine.set_spatial_audio_enabled(enabled)

    def is_audio_available(self) -> bool:
        """Check if audio is available"""
        return self.audio_engine.is_audio_available()

    def get_audio_info(self) -> Dict[str, Any]:
        """Get audio system information"""
        return {
            "available": self.audio_engine.is_audio_available(),
            "enabled": self.audio_engine.is_audio_enabled(),
            "master_volume": self.audio_engine.get_master_volume(),
            "cue_volume": self.audio_engine.get_cue_volume(),
            "spatial_audio": self.audio_engine.is_spatial_audio_enabled(),
            "audio_module": getattr(self.audio_engine, "_audio_module", None),
        }

    def shutdown(self) -> None:
        """Shutdown audio accessibility"""
        self.audio_engine.shutdown()


# Global audio manager instance
_audio_manager: Optional[AudioAccessibilityManager] = None


def get_audio_manager(root: tk.Tk) -> AudioAccessibilityManager:
    """Get global audio accessibility manager"""
    global _audio_manager
    if _audio_manager is None:
        _audio_manager = AudioAccessibilityManager(root)
    return _audio_manager


def setup_audio_accessibility(
    root: tk.Tk,
    enable_spatial: bool = False,
    master_volume: float = 0.7,
    cue_volume: float = 0.5,
) -> None:
    """Set up audio accessibility for application"""
    audio_manager = get_audio_manager(root)
    audio_manager.set_master_volume(master_volume)
    audio_manager.set_cue_volume(cue_volume)
    audio_manager.set_spatial_audio_enabled(enable_spatial)


def play_audio_cue(cue_type: AudioCueType, widget: Optional[tk.Misc] = None) -> None:
    """Play audio cue"""
    if _audio_manager:
        if widget:
            _audio_manager.play_cue_for_widget(widget, cue_type)
        else:
            _audio_manager.audio_engine.play_cue(cue_type)


def play_success_sound() -> None:
    """Play success sound"""
    if _audio_manager:
        _audio_manager.play_success_sound()


def play_error_sound() -> None:
    """Play error sound"""
    if _audio_manager:
        _audio_manager.play_error_sound()


def play_warning_sound() -> None:
    """Play warning sound"""
    if _audio_manager:
        _audio_manager.play_warning_sound()


def play_notification_sound() -> None:
    """Play notification sound"""
    if _audio_manager:
        _audio_manager.play_notification_sound()


def set_audio_volume(master_volume: float, cue_volume: float) -> None:
    """Set audio volumes"""
    if _audio_manager:
        _audio_manager.set_master_volume(master_volume)
        _audio_manager.set_cue_volume(cue_volume)


def set_audio_enabled(enabled: bool) -> None:
    """Enable/disable audio accessibility"""
    if _audio_manager:
        _audio_manager.set_audio_enabled(enabled)


def set_spatial_audio_enabled(enabled: bool) -> None:
    """Enable/disable spatial audio"""
    if _audio_manager:
        _audio_manager.set_spatial_audio_enabled(enabled)


def is_audio_available() -> bool:
    """Check if audio is available"""
    return _audio_manager.is_audio_available() if _audio_manager else False


def get_audio_info() -> Dict[str, Any]:
    """Get audio system information"""
    return _audio_manager.get_audio_info() if _audio_manager else {}


def shutdown_audio_accessibility() -> None:
    """Shutdown audio accessibility"""
    global _audio_manager
    if _audio_manager:
        _audio_manager.shutdown()
        _audio_manager = None
