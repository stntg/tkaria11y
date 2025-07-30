# tkaria11y/braille_support.py

"""
Braille display support for tkaria11y.
Provides integration with braille displays for tactile feedback and navigation.
"""

import tkinter as tk
import threading
import time
import queue
from typing import Dict, List, Optional, Callable, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class BrailleDisplayType(Enum):
    """Types of braille displays"""

    GENERIC = "generic"
    FREEDOM_SCIENTIFIC = "freedom_scientific"
    HUMANWARE = "humanware"
    PAPENMEIER = "papenmeier"
    ALVA = "alva"
    BAUM = "baum"
    HANDY_TECH = "handy_tech"
    HIMS = "hims"
    NIPPON_TELESOFT = "nippon_telesoft"
    OPTELEC = "optelec"
    SEIKA = "seika"
    EUROBRAILLE = "eurobraille"


@dataclass
class BrailleCell:
    """Represents a single braille cell"""

    dots: int  # 8-bit value representing dot pattern
    cursor: bool = False

    def __post_init__(self) -> None:
        # Ensure dots is within valid range (0-255)
        self.dots = max(0, min(255, self.dots))

    def to_unicode(self) -> str:
        """Convert braille cell to Unicode braille character"""
        # Unicode braille patterns start at U+2800
        return chr(0x2800 + self.dots)

    @classmethod
    def from_char(cls, char: str) -> "BrailleCell":
        """Create braille cell from character"""
        if not char:
            return cls(0)

        # Convert character to braille using basic ASCII mapping
        char = char.upper()

        # Basic braille mapping for common characters
        braille_map = {
            "A": 0x01,
            "B": 0x03,
            "C": 0x09,
            "D": 0x19,
            "E": 0x11,
            "F": 0x0B,
            "G": 0x1B,
            "H": 0x13,
            "I": 0x0A,
            "J": 0x1A,
            "K": 0x05,
            "L": 0x07,
            "M": 0x0D,
            "N": 0x1D,
            "O": 0x15,
            "P": 0x0F,
            "Q": 0x1F,
            "R": 0x17,
            "S": 0x0E,
            "T": 0x1E,
            "U": 0x25,
            "V": 0x27,
            "W": 0x3A,
            "X": 0x2D,
            "Y": 0x3D,
            "Z": 0x35,
            " ": 0x00,
            ".": 0x2E,
            ",": 0x02,
            "?": 0x26,
            "!": 0x16,
            "'": 0x04,
            "-": 0x24,
            "(": 0x2F,
            ")": 0x2F,
            "0": 0x2A,
            "1": 0x01,
            "2": 0x03,
            "3": 0x09,
            "4": 0x19,
            "5": 0x11,
            "6": 0x0B,
            "7": 0x1B,
            "8": 0x13,
            "9": 0x0A,
        }

        dots = braille_map.get(char.upper(), 0x3F)  # Default to full cell
        return cls(dots)


class BrailleDisplay(ABC):
    """Abstract base class for braille display drivers"""

    def __init__(self, display_type: BrailleDisplayType, cell_count: int):
        self.display_type = display_type
        self.cell_count = cell_count
        self.connected = False
        self._cells: List[BrailleCell] = [BrailleCell(0) for _ in range(cell_count)]
        self._cursor_position = 0
        self._callbacks: Dict[str, List[Callable]] = {
            "key_press": [],
            "routing_key": [],
            "cursor_routing": [],
        }

    @abstractmethod
    def connect(self) -> bool:
        """Connect to braille display"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from braille display"""
        pass

    @abstractmethod
    def write_cells(self, cells: List[BrailleCell], start_pos: int = 0) -> bool:
        """Write braille cells to display"""
        pass

    @abstractmethod
    def read_keys(self) -> List[str]:
        """Read pressed keys from display"""
        pass

    def set_text(self, text: str, start_pos: int = 0) -> None:
        """Set text on braille display"""
        cells = []
        for i, char in enumerate(text):
            if start_pos + i >= self.cell_count:
                break
            cells.append(BrailleCell.from_char(char))

        self.write_cells(cells, start_pos)

    def set_cursor_position(self, position: int) -> None:
        """Set cursor position on display"""
        if 0 <= position < self.cell_count:
            # Clear old cursor
            if 0 <= self._cursor_position < len(self._cells):
                self._cells[self._cursor_position].cursor = False

            # Set new cursor
            self._cursor_position = position
            if position < len(self._cells):
                self._cells[position].cursor = True

            # Update display
            self.write_cells(self._cells)

    def add_callback(self, event_type: str, callback: Callable) -> None:
        """Add event callback"""
        if event_type in self._callbacks:
            self._callbacks[event_type].append(callback)

    def remove_callback(self, event_type: str, callback: Callable) -> None:
        """Remove event callback"""
        if event_type in self._callbacks and callback in self._callbacks[event_type]:
            self._callbacks[event_type].remove(callback)

    def _trigger_callback(self, event_type: str, *args: Any) -> None:
        """Trigger callbacks for event"""
        for callback in self._callbacks.get(event_type, []):
            try:
                callback(*args)
            except Exception:
                # Ignore callback errors
                pass


class GenericBrailleDisplay(BrailleDisplay):
    """Generic braille display implementation"""

    def __init__(self, cell_count: int = 40):
        super().__init__(BrailleDisplayType.GENERIC, cell_count)
        self._simulation_mode = True
        self._simulated_text = ""

    def connect(self) -> bool:
        """Connect to generic braille display"""
        # In simulation mode, always succeed
        if self._simulation_mode:
            self.connected = True
            return True

        # Real implementation would attempt hardware connection
        return False

    def disconnect(self) -> None:
        """Disconnect from braille display"""
        self.connected = False
        self._simulated_text = ""

    def write_cells(self, cells: List[BrailleCell], start_pos: int = 0) -> bool:
        """Write cells to display"""
        if not self.connected:
            return False

        # Update internal cell buffer
        for i, cell in enumerate(cells):
            pos = start_pos + i
            if pos < len(self._cells):
                self._cells[pos] = cell

        # In simulation mode, convert to text
        if self._simulation_mode:
            text_chars = []
            for cell in self._cells:
                if cell.dots == 0:
                    text_chars.append(" ")
                else:
                    # Convert back to approximate character
                    text_chars.append(self._dots_to_char(cell.dots))

            self._simulated_text = "".join(text_chars)

        return True

    def read_keys(self) -> List[str]:
        """Read keys from display"""
        # Simulation mode returns empty list
        return []

    def get_simulated_text(self) -> str:
        """Get simulated braille text (for testing)"""
        return self._simulated_text

    def _dots_to_char(self, dots: int) -> str:
        """Convert dot pattern back to character (approximate)"""
        # Reverse mapping for common patterns (letters take precedence)
        reverse_map = {
            0x01: "A",
            0x03: "B",
            0x09: "C",
            0x19: "D",
            0x11: "E",
            0x0B: "F",
            0x1B: "G",
            0x13: "H",
            0x0A: "I",
            0x1A: "J",
            0x05: "K",
            0x07: "L",
            0x0D: "M",
            0x1D: "N",
            0x15: "O",
            0x0F: "P",
            0x1F: "Q",
            0x17: "R",
            0x0E: "S",
            0x1E: "T",
            0x25: "U",
            0x27: "V",
            0x3A: "W",
            0x2D: "X",
            0x3D: "Y",
            0x35: "Z",
            0x00: " ",
            0x2E: ".",
            0x02: ",",
            0x26: "?",
            0x16: "!",
            0x04: "'",
            0x24: "-",
            0x2F: "(",
            0x2A: "0",
        }

        return reverse_map.get(dots, "?")


class BrailleManager:
    """Manages braille display integration"""

    def __init__(self) -> None:
        self._displays: List[BrailleDisplay] = []
        self._active_display: Optional[BrailleDisplay] = None
        self._text_queue: queue.Queue = queue.Queue()
        self._worker_thread: Optional[threading.Thread] = None
        self._running = False
        self._focus_tracking = True
        self._current_widget: Optional[tk.Misc] = None

        # Braille translation settings
        self._grade = 1  # Grade 1 (uncontracted) braille
        self._show_cursor = True
        self._cursor_blink = True
        self._cursor_blink_rate = 0.5  # seconds

        # Auto-detection
        self._auto_detect_displays()

    def _auto_detect_displays(self) -> None:
        """Auto-detect available braille displays"""
        # For now, add a generic display for simulation
        generic_display = GenericBrailleDisplay(40)
        self.add_display(generic_display)

        # Real implementation would scan for hardware displays
        # self._scan_usb_displays()
        # self._scan_bluetooth_displays()
        # self._scan_serial_displays()

    def add_display(self, display: BrailleDisplay) -> None:
        """Add braille display"""
        if display not in self._displays:
            self._displays.append(display)

            # Set as active if it's the first one
            if not self._active_display:
                self.set_active_display(display)

    def remove_display(self, display: BrailleDisplay) -> None:
        """Remove braille display"""
        if display in self._displays:
            if display == self._active_display:
                display.disconnect()
                self._active_display = None

            self._displays.remove(display)

    def set_active_display(self, display: BrailleDisplay) -> bool:
        """Set active braille display"""
        if display in self._displays:
            # Disconnect current display
            if self._active_display:
                self._active_display.disconnect()

            # Connect new display
            if display.connect():
                self._active_display = display
                self._start_worker_thread()
                return True

        return False

    def get_active_display(self) -> Optional[BrailleDisplay]:
        """Get active braille display"""
        return self._active_display

    def get_available_displays(self) -> List[BrailleDisplay]:
        """Get list of available displays"""
        return self._displays.copy()

    def _start_worker_thread(self) -> None:
        """Start worker thread for braille processing"""
        if self._worker_thread and self._worker_thread.is_alive():
            return

        self._running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

    def _stop_worker_thread(self) -> None:
        """Stop worker thread"""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=1.0)

    def _worker_loop(self) -> None:
        """Worker thread main loop"""
        cursor_blink_time = time.time()
        cursor_visible = True

        while self._running and self._active_display:
            try:
                # Process text queue
                try:
                    text, position = self._text_queue.get_nowait()
                    self._active_display.set_text(text, position)
                except queue.Empty:
                    pass

                # Handle cursor blinking
                if self._cursor_blink and self._show_cursor:
                    current_time = time.time()
                    if current_time - cursor_blink_time >= self._cursor_blink_rate:
                        cursor_visible = not cursor_visible
                        cursor_blink_time = current_time

                        # Update cursor visibility
                        if hasattr(self._active_display, "_cursor_position"):
                            pos = self._active_display._cursor_position
                            if 0 <= pos < len(self._active_display._cells):
                                self._active_display._cells[pos].cursor = cursor_visible
                                self._active_display.write_cells(
                                    self._active_display._cells
                                )

                # Read input from display
                keys = self._active_display.read_keys()
                for key in keys:
                    self._handle_braille_key(key)

                time.sleep(0.1)  # 100ms update rate

            except Exception:
                # Continue on errors
                time.sleep(0.1)

    def _handle_braille_key(self, key: str) -> None:
        """Handle key press from braille display"""
        # Handle common braille display keys
        if key.startswith("routing_"):
            # Cursor routing key pressed
            try:
                position = int(key.split("_")[1])
                self._handle_cursor_routing(position)
            except (ValueError, IndexError):
                pass

        elif key in ["left", "pan_left"]:
            self._pan_left()

        elif key in ["right", "pan_right"]:
            self._pan_right()

        elif key in ["up", "cursor_up"]:
            self._move_cursor_up()

        elif key in ["down", "cursor_down"]:
            self._move_cursor_down()

        # Trigger callbacks
        if self._active_display:
            self._active_display._trigger_callback("key_press", key)

    def _handle_cursor_routing(self, position: int) -> None:
        """Handle cursor routing key press"""
        if self._current_widget and hasattr(self._current_widget, "icursor"):
            try:
                # Move text cursor to braille position
                self._current_widget.icursor(position)
                self._current_widget.focus_set()
            except tk.TclError:
                pass

    def _pan_left(self) -> None:
        """Pan braille display left"""
        # Implementation would depend on current context
        pass

    def _pan_right(self) -> None:
        """Pan braille display right"""
        # Implementation would depend on current context
        pass

    def _move_cursor_up(self) -> None:
        """Move cursor up in current context"""
        if self._current_widget:
            # Generate Up arrow key event
            self._current_widget.event_generate("<Up>")

    def _move_cursor_down(self) -> None:
        """Move cursor down in current context"""
        if self._current_widget:
            # Generate Down arrow key event
            self._current_widget.event_generate("<Down>")

    def display_text(self, text: str, position: int = 0) -> None:
        """Display text on braille display"""
        if self._active_display:
            try:
                self._text_queue.put_nowait((text, position))
            except queue.Full:
                # Queue is full, skip this update
                pass

    def display_widget_info(self, widget: tk.Misc) -> None:
        """Display widget information on braille display"""
        if not self._active_display:
            return

        self._current_widget = widget

        # Build braille text from widget info
        text_parts = []

        # Add accessible name
        if hasattr(widget, "accessible_name") and widget.accessible_name:
            text_parts.append(widget.accessible_name)
        else:
            # Fallback to widget text or class
            try:
                widget_text = widget.cget("text")
                if widget_text:
                    text_parts.append(widget_text)
                else:
                    text_parts.append(widget.winfo_class())
            except tk.TclError:
                text_parts.append(widget.winfo_class())

        # Add role information
        if hasattr(widget, "accessible_role") and widget.accessible_role:
            text_parts.append(f"({widget.accessible_role})")

        # Add state information
        state_info = self._get_widget_state_for_braille(widget)
        if state_info:
            text_parts.append(state_info)

        # Add value for input widgets
        if hasattr(widget, "get"):
            try:
                value = widget.get()
                if value:
                    text_parts.append(f": {value}")
            except (tk.TclError, TypeError):
                pass

        braille_text = " ".join(text_parts)
        self.display_text(braille_text)

    def _get_widget_state_for_braille(self, widget: tk.Misc) -> str:
        """Get widget state information for braille display"""
        states = []

        try:
            widget_class = widget.winfo_class()

            # Check common states
            state = widget.cget("state")
            if state == "disabled":
                states.append("disabled")

            # Widget-specific states
            if widget_class in ["Checkbutton", "TCheckbutton"]:
                var = widget.cget("variable")
                if var and var.get():
                    states.append("checked")
                else:
                    states.append("unchecked")

            elif widget_class in ["Radiobutton", "TRadiobutton"]:
                var = widget.cget("variable")
                value = widget.cget("value")
                if var and var.get() == value:
                    states.append("selected")

            elif widget_class in ["Entry", "TEntry"]:
                if widget.cget("show"):
                    states.append("password")

        except tk.TclError:
            pass

        return " ".join(states)

    def set_focus_tracking(self, enabled: bool) -> None:
        """Enable/disable automatic focus tracking"""
        self._focus_tracking = enabled

    def is_focus_tracking_enabled(self) -> bool:
        """Check if focus tracking is enabled"""
        return self._focus_tracking

    def set_grade(self, grade: int) -> None:
        """Set braille grade (1 or 2)"""
        if grade in [1, 2]:
            self._grade = grade

    def get_grade(self) -> int:
        """Get current braille grade"""
        return self._grade

    def set_cursor_settings(
        self, show: bool = True, blink: bool = True, rate: float = 0.5
    ) -> None:
        """Set cursor display settings"""
        self._show_cursor = show
        self._cursor_blink = blink
        self._cursor_blink_rate = max(0.1, rate)

    def shutdown(self) -> None:
        """Shutdown braille manager"""
        self._stop_worker_thread()

        for display in self._displays:
            display.disconnect()

        self._displays.clear()
        self._active_display = None


# Global braille manager instance
_braille_manager: Optional[BrailleManager] = None


def get_braille_manager() -> BrailleManager:
    """Get global braille manager instance"""
    global _braille_manager
    if _braille_manager is None:
        _braille_manager = BrailleManager()
    return _braille_manager


def setup_braille_support(root: tk.Tk) -> None:
    """Set up braille support for application"""
    braille_manager = get_braille_manager()

    # Set up focus tracking
    def on_focus_change(event: tk.Event) -> None:
        if braille_manager.is_focus_tracking_enabled():
            widget = event.widget
            braille_manager.display_widget_info(widget)

    root.bind_all("<FocusIn>", on_focus_change, add="+")

    # Set up text change tracking for input widgets
    def on_text_change(event: tk.Event) -> None:
        widget = event.widget
        if hasattr(widget, "get") and braille_manager.is_focus_tracking_enabled():
            try:
                text = widget.get()
                braille_manager.display_text(text)
            except (tk.TclError, TypeError):
                pass

    root.bind_all("<KeyRelease>", on_text_change, add="+")


def display_braille_text(text: str, position: int = 0) -> None:
    """Display text on braille display"""
    braille_manager = get_braille_manager()
    braille_manager.display_text(text, position)


def display_widget_on_braille(widget: tk.Widget) -> None:
    """Display widget information on braille display"""
    braille_manager = get_braille_manager()
    braille_manager.display_widget_info(widget)


def is_braille_display_available() -> bool:
    """Check if braille display is available"""
    braille_manager = get_braille_manager()
    return braille_manager.get_active_display() is not None


def get_braille_display_info() -> Dict[str, Any]:
    """Get information about active braille display"""
    braille_manager = get_braille_manager()
    active_display = braille_manager.get_active_display()

    if active_display:
        return {
            "type": active_display.display_type.value,
            "cell_count": active_display.cell_count,
            "connected": active_display.connected,
            "cursor_position": getattr(active_display, "_cursor_position", 0),
        }

    return {"type": None, "cell_count": 0, "connected": False, "cursor_position": 0}


def shutdown_braille_support() -> None:
    """Shutdown braille support"""
    global _braille_manager
    if _braille_manager:
        _braille_manager.shutdown()
        _braille_manager = None
