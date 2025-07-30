#!/usr/bin/env python3
"""
CustomTkinter-specific accessible widgets with proper event handling.

This module provides CustomTkinter widgets with accessibility features
that work around CTK's limitations with traditional event binding.
"""

import tkinter as tk
from typing import Optional, Callable, Any, Dict
import threading
import time

try:
    import customtkinter as ctk

    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False

    # Create dummy classes for type hints
    class ctk:
        class CTkFrame:
            pass

        class CTkButton:
            pass

        class CTkEntry:
            pass

        class CTkLabel:
            pass

        class CTkCheckBox:
            pass

        class CTkRadioButton:
            pass

        class CTkSlider:
            pass

        class CTkTabview:
            pass

        class CTkScrollableFrame:
            pass


from .a11y_engine import speak
from .platform_adapter import set_accessible_name, set_accessible_description


class CTKAccessibilityMixin:
    """Accessibility mixin specifically designed for CustomTkinter widgets"""

    def __init__(self, *args, **kwargs):
        # Extract accessibility parameters
        self.accessible_name = kwargs.pop("accessible_name", None)
        self.accessible_description = kwargs.pop("accessible_description", None)
        self.accessible_role = kwargs.pop("accessible_role", None)

        # Initialize the CTK widget
        super().__init__(*args, **kwargs)

        # Set up accessibility features
        self._setup_ctk_accessibility()

        # Focus tracking
        self._has_focus = False
        self._focus_callbacks: list[Callable] = []

        # Manual event simulation since CTK doesn't support binding
        self._setup_manual_events()

        # Register with focus manager
        self._register_with_focus_manager()

    def _setup_ctk_accessibility(self) -> None:
        """Set up accessibility features for CustomTkinter widgets"""
        if self.accessible_name:
            try:
                set_accessible_name(self, self.accessible_name)
            except:
                pass

        if self.accessible_description:
            try:
                set_accessible_description(self, self.accessible_description)
            except:
                pass

    def _setup_manual_events(self) -> None:
        """Set up manual event handling since CTK doesn't support traditional binding"""
        # Start a background thread to monitor focus changes
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_focus, daemon=True)
        self._monitor_thread.start()

    def _monitor_focus(self) -> None:
        """Monitor focus changes manually"""
        last_focus_state = False

        while self._monitoring:
            try:
                # Check if this widget has focus
                current_focus = self._check_focus()

                if current_focus != last_focus_state:
                    if current_focus:
                        self._on_focus_gained()
                    else:
                        self._on_focus_lost()
                    last_focus_state = current_focus

                time.sleep(0.1)  # Check every 100ms
            except:
                break

    def _check_focus(self) -> bool:
        """Check if this widget currently has focus"""
        try:
            # For CTK widgets, we need to check focus differently
            root = self.winfo_toplevel()
            focused_widget = root.focus_get()
            return focused_widget == self
        except:
            return False

    def _on_focus_gained(self) -> None:
        """Handle focus gained event"""
        self._has_focus = True

        # Announce the widget
        announcement = self._get_focus_announcement()
        if announcement:
            speak(announcement)

        # Call focus callbacks
        for callback in self._focus_callbacks:
            try:
                callback()
            except:
                pass

    def _on_focus_lost(self) -> None:
        """Handle focus lost event"""
        self._has_focus = False

    def _get_focus_announcement(self) -> str:
        """Get announcement text when widget receives focus"""
        parts = []

        # Widget name
        if self.accessible_name:
            parts.append(self.accessible_name)
        elif hasattr(self, "cget"):
            try:
                text = self.cget("text")
                if text:
                    parts.append(text)
            except:
                pass

        # Widget type
        widget_type = self._get_widget_type_announcement()
        if widget_type:
            parts.append(widget_type)

        # Widget state
        state = self._get_state_announcement()
        if state:
            parts.append(state)

        # Description
        if self.accessible_description:
            parts.append(self.accessible_description)

        return ", ".join(parts)

    def _get_widget_type_announcement(self) -> str:
        """Get widget type for announcement"""
        class_name = self.__class__.__name__

        if "Button" in class_name:
            return "button"
        elif "Entry" in class_name:
            return "text field"
        elif "Label" in class_name:
            return "label"
        elif "CheckBox" in class_name:
            return "checkbox"
        elif "RadioButton" in class_name:
            return "radio button"
        elif "Slider" in class_name:
            return "slider"
        elif "Frame" in class_name:
            return "group"
        else:
            return "control"

    def _get_state_announcement(self) -> str:
        """Get current state for announcement"""
        states = []

        try:
            # Check disabled state
            if hasattr(self, "cget"):
                try:
                    if self.cget("state") == "disabled":
                        states.append("disabled")
                except:
                    pass

            # Check checkbox/radio button state
            if hasattr(self, "get"):
                try:
                    value = self.get()
                    if isinstance(value, (bool, int)):
                        if value:
                            states.append("checked")
                        else:
                            states.append("unchecked")
                except:
                    pass
        except:
            pass

        return ", ".join(states)

    def add_focus_callback(self, callback: Callable) -> None:
        """Add a callback to be called when widget receives focus"""
        self._focus_callbacks.append(callback)

    def remove_focus_callback(self, callback: Callable) -> None:
        """Remove a focus callback"""
        try:
            self._focus_callbacks.remove(callback)
        except ValueError:
            pass

    def _register_with_focus_manager(self) -> None:
        """Register this widget with the main focus manager"""
        try:
            from .focus_manager import get_focus_manager

            root = self.winfo_toplevel()
            focus_manager = get_focus_manager(root)

            # Only register if this is a focusable widget
            if focus_manager._is_focusable_widget(self):
                focus_manager.register_widget(self)
        except (AttributeError, ImportError, tk.TclError):
            # Focus manager not available or widget not ready
            pass

    def destroy(self) -> None:
        """Clean up when widget is destroyed"""
        self._monitoring = False
        super().destroy()


class AccessibleCTKFrame(CTKAccessibilityMixin, ctk.CTkFrame):
    """Accessible CustomTkinter Frame"""

    pass


class AccessibleCTKButton(CTKAccessibilityMixin, ctk.CTkButton):
    """Accessible CustomTkinter Button"""

    def __init__(self, *args, **kwargs):
        # Store original command
        self._original_command = kwargs.get("command")

        # Wrap command to add accessibility
        if self._original_command:
            kwargs["command"] = self._accessible_command

        super().__init__(*args, **kwargs)

    def _accessible_command(self) -> None:
        """Wrapped command that adds accessibility feedback"""
        # Announce button activation
        announcement = f"{self.accessible_name or 'Button'} activated"
        speak(announcement)

        # Call original command
        if self._original_command:
            self._original_command()


class AccessibleCTKEntry(CTKAccessibilityMixin, ctk.CTkEntry):
    """Accessible CustomTkinter Entry"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Monitor text changes
        self._last_text = ""
        self._setup_text_monitoring()

    def _setup_text_monitoring(self) -> None:
        """Monitor text changes since CTK doesn't support text change events"""

        def monitor_text():
            while self._monitoring:
                try:
                    current_text = self.get()
                    if current_text != self._last_text:
                        self._on_text_changed(current_text)
                        self._last_text = current_text
                    time.sleep(0.2)  # Check every 200ms
                except:
                    break

        threading.Thread(target=monitor_text, daemon=True).start()

    def _on_text_changed(self, new_text: str) -> None:
        """Handle text change"""
        if self._has_focus:
            # Announce text changes for screen readers
            if len(new_text) > len(self._last_text):
                # Text was added
                added_text = new_text[len(self._last_text) :]
                if len(added_text) == 1:
                    speak(added_text)
            elif len(new_text) < len(self._last_text):
                # Text was removed
                speak("deleted")


class AccessibleCTKLabel(CTKAccessibilityMixin, ctk.CTkLabel):
    """Accessible CustomTkinter Label"""

    pass


class AccessibleCTKCheckBox(CTKAccessibilityMixin, ctk.CTkCheckBox):
    """Accessible CustomTkinter CheckBox"""

    def __init__(self, *args, **kwargs):
        # Store original command
        self._original_command = kwargs.get("command")

        # Wrap command to add accessibility
        if self._original_command:
            kwargs["command"] = self._accessible_command

        super().__init__(*args, **kwargs)

    def _accessible_command(self) -> None:
        """Wrapped command that adds accessibility feedback"""
        # Announce checkbox state change
        try:
            checked = self.get()
            state = "checked" if checked else "unchecked"
            announcement = f"{self.accessible_name or 'Checkbox'} {state}"
            speak(announcement)
        except:
            pass

        # Call original command
        if self._original_command:
            self._original_command()


class AccessibleCTKRadioButton(CTKAccessibilityMixin, ctk.CTkRadioButton):
    """Accessible CustomTkinter RadioButton"""

    def __init__(self, *args, **kwargs):
        # Store original command
        self._original_command = kwargs.get("command")

        # Wrap command to add accessibility
        if self._original_command:
            kwargs["command"] = self._accessible_command

        super().__init__(*args, **kwargs)

    def _accessible_command(self) -> None:
        """Wrapped command that adds accessibility feedback"""
        # Announce radio button selection
        announcement = f"{self.accessible_name or 'Radio button'} selected"
        speak(announcement)

        # Call original command
        if self._original_command:
            self._original_command()


class AccessibleCTKSlider(CTKAccessibilityMixin, ctk.CTkSlider):
    """Accessible CustomTkinter Slider"""

    def __init__(self, *args, **kwargs):
        # Store original command
        self._original_command = kwargs.get("command")

        # Wrap command to add accessibility
        if self._original_command:
            kwargs["command"] = self._accessible_command

        super().__init__(*args, **kwargs)

        # Track last announced value to avoid spam
        self._last_announced_value = None
        self._announce_timer = None

    def _accessible_command(self, value: float) -> None:
        """Wrapped command that adds accessibility feedback"""
        # Debounce announcements
        if self._announce_timer:
            self._announce_timer.cancel()

        def announce_value():
            try:
                int_value = int(value)
                if self._last_announced_value != int_value:
                    announcement = f"{self.accessible_name or 'Slider'} {int_value}"
                    speak(announcement)
                    self._last_announced_value = int_value
            except:
                pass

        # Delay announcement to avoid spam during dragging
        self._announce_timer = threading.Timer(0.5, announce_value)
        self._announce_timer.start()

        # Call original command
        if self._original_command:
            self._original_command(value)


class AccessibleCTKTabview(CTKAccessibilityMixin, ctk.CTkTabview):
    """Accessible CustomTkinter Tabview"""

    def add(self, name: str, **kwargs) -> ctk.CTkFrame:
        """Add a tab with accessibility support"""
        tab_frame = super().add(name, **kwargs)

        # Announce tab creation
        speak(f"Tab {name} added")

        return tab_frame

    def set(self, name: str) -> None:
        """Set active tab with accessibility feedback"""
        super().set(name)

        # Announce tab change
        speak(f"Tab {name} selected")


class AccessibleCTKScrollableFrame(CTKAccessibilityMixin, ctk.CTkScrollableFrame):
    """Accessible CustomTkinter ScrollableFrame"""

    pass


# Export all accessible CTK widgets
__all__ = [
    "CTKAccessibilityMixin",
    "AccessibleCTKFrame",
    "AccessibleCTKButton",
    "AccessibleCTKEntry",
    "AccessibleCTKLabel",
    "AccessibleCTKCheckBox",
    "AccessibleCTKRadioButton",
    "AccessibleCTKSlider",
    "AccessibleCTKTabview",
    "AccessibleCTKScrollableFrame",
    "CTK_AVAILABLE",
]
