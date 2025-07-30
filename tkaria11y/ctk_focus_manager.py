#!/usr/bin/env python3
"""
CustomTkinter-specific focus management system.

This module provides focus management for CustomTkinter widgets that works
around CTK's limitations with traditional event binding.
"""

import tkinter as tk
from typing import List, Optional, Dict, Callable
import threading
import time
import weakref

try:
    import customtkinter as ctk

    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False


class CTKFocusIndicator:
    """Visual focus indicator specifically for CustomTkinter widgets"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self._current_widget: Optional[tk.Misc] = None
        self._indicator_color = "#FFD700"  # Gold color for high visibility
        self._indicator_width = 3

        # Use widget highlighting instead of overlay canvas
        self._original_properties: Dict[tk.Misc, Dict[str, any]] = {}

    def show_focus(self, widget: tk.Misc) -> None:
        """Show focus indicator for CustomTkinter widget"""
        self._current_widget = widget

        try:
            # Store original properties if not already stored
            if widget not in self._original_properties:
                self._original_properties[widget] = {}

                # Try to get original border properties
                try:
                    if hasattr(widget, "cget"):
                        self._original_properties[widget]["border_width"] = widget.cget(
                            "border_width"
                        )
                        self._original_properties[widget]["border_color"] = widget.cget(
                            "border_color"
                        )
                except:
                    pass

            # Apply focus highlighting using CTK's border system
            try:
                if hasattr(widget, "configure"):
                    widget.configure(
                        border_width=self._indicator_width,
                        border_color=self._indicator_color,
                    )
            except:
                # Fallback: try to use standard Tkinter highlighting
                try:
                    widget.configure(
                        highlightthickness=self._indicator_width,
                        highlightcolor=self._indicator_color,
                        highlightbackground=self._indicator_color,
                    )
                except:
                    pass
        except:
            pass

    def hide_focus(self) -> None:
        """Hide focus indicator"""
        if self._current_widget and self._current_widget in self._original_properties:
            try:
                # Restore original properties
                original = self._original_properties[self._current_widget]

                if hasattr(self._current_widget, "configure"):
                    # Restore CTK border properties
                    if "border_width" in original:
                        self._current_widget.configure(
                            border_width=original["border_width"]
                        )
                    if "border_color" in original:
                        self._current_widget.configure(
                            border_color=original["border_color"]
                        )

                    # Also try to reset standard highlighting
                    try:
                        self._current_widget.configure(
                            highlightthickness=0, highlightcolor="SystemWindowFrame"
                        )
                    except:
                        pass
            except:
                pass

        self._current_widget = None

    def update_focus(self) -> None:
        """Update focus indicator position"""
        if self._current_widget:
            self.show_focus(self._current_widget)

    def set_color(self, color: str) -> None:
        """Set focus indicator color"""
        self._indicator_color = color
        if self._current_widget:
            self.show_focus(self._current_widget)


class CTKFocusManager:
    """Focus management system specifically for CustomTkinter widgets"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self._focus_order: List[tk.Misc] = []
        self._current_focus_index = 0
        self._focus_indicator = CTKFocusIndicator(root)
        self._focus_callbacks: Dict[tk.Misc, List[Callable]] = {}
        self._monitoring = True

        # Track widgets using weak references
        self._widget_refs: weakref.WeakSet = weakref.WeakSet()

        # Start focus monitoring thread
        self._monitor_thread = threading.Thread(target=self._monitor_focus, daemon=True)
        self._monitor_thread.start()

        # Set up keyboard navigation
        self._setup_keyboard_navigation()

    def _setup_keyboard_navigation(self) -> None:
        """Set up keyboard navigation for CTK widgets"""
        # Bind to root window since CTK widgets don't support individual binding
        try:
            self.root.bind_all("<Tab>", self._handle_tab, add="+")
            self.root.bind_all("<Shift-Tab>", self._handle_shift_tab, add="+")
            self.root.bind_all("<Up>", self._handle_up_arrow, add="+")
            self.root.bind_all("<Down>", self._handle_down_arrow, add="+")
            self.root.bind_all("<Left>", self._handle_left_arrow, add="+")
            self.root.bind_all("<Right>", self._handle_right_arrow, add="+")
        except:
            pass

    def _monitor_focus(self) -> None:
        """Monitor focus changes across all registered widgets"""
        last_focused_widget = None

        while self._monitoring:
            try:
                # Get currently focused widget
                current_focus = self.root.focus_get()

                if current_focus != last_focused_widget:
                    # Focus changed
                    if last_focused_widget:
                        self._on_widget_focus_lost(last_focused_widget)

                    if current_focus and current_focus in self._focus_order:
                        self._on_widget_focus_gained(current_focus)
                        self._update_focus_index(current_focus)

                    last_focused_widget = current_focus

                time.sleep(0.1)  # Check every 100ms
            except:
                break

    def _on_widget_focus_gained(self, widget: tk.Misc) -> None:
        """Handle when a widget gains focus"""
        # Show focus indicator
        self._focus_indicator.show_focus(widget)

        # Call focus callbacks
        if widget in self._focus_callbacks:
            for callback in self._focus_callbacks[widget]:
                try:
                    callback()
                except:
                    pass

    def _on_widget_focus_lost(self, widget: tk.Misc) -> None:
        """Handle when a widget loses focus"""
        # Hide focus indicator
        self._focus_indicator.hide_focus()

    def register_widget(
        self, widget: tk.Misc, focus_group: Optional[str] = None
    ) -> None:
        """Register a CustomTkinter widget for focus management"""
        if widget not in self._focus_order:
            self._focus_order.append(widget)
            self._widget_refs.add(widget)

    def unregister_widget(self, widget: tk.Misc) -> None:
        """Unregister a widget from focus management"""
        if widget in self._focus_order:
            self._focus_order.remove(widget)

        if widget in self._focus_callbacks:
            del self._focus_callbacks[widget]

    def add_focus_callback(self, widget: tk.Misc, callback: Callable) -> None:
        """Add a callback to be called when widget receives focus"""
        if widget not in self._focus_callbacks:
            self._focus_callbacks[widget] = []
        self._focus_callbacks[widget].append(callback)

    def focus_next(self) -> bool:
        """Move focus to next widget"""
        if not self._focus_order:
            return False

        self._current_focus_index = (self._current_focus_index + 1) % len(
            self._focus_order
        )
        return self._focus_widget_at_index(self._current_focus_index)

    def focus_previous(self) -> bool:
        """Move focus to previous widget"""
        if not self._focus_order:
            return False

        self._current_focus_index = (self._current_focus_index - 1) % len(
            self._focus_order
        )
        return self._focus_widget_at_index(self._current_focus_index)

    def focus_first(self) -> bool:
        """Move focus to first widget"""
        if not self._focus_order:
            return False

        self._current_focus_index = 0
        return self._focus_widget_at_index(0)

    def focus_last(self) -> bool:
        """Move focus to last widget"""
        if not self._focus_order:
            return False

        self._current_focus_index = len(self._focus_order) - 1
        return self._focus_widget_at_index(self._current_focus_index)

    def _focus_widget_at_index(self, index: int) -> bool:
        """Focus widget at specific index"""
        if 0 <= index < len(self._focus_order):
            widget = self._focus_order[index]
            try:
                widget.focus_set()
                return True
            except:
                return False
        return False

    def _update_focus_index(self, widget: tk.Misc) -> None:
        """Update current focus index based on focused widget"""
        try:
            self._current_focus_index = self._focus_order.index(widget)
        except ValueError:
            pass

    def get_current_focus(self) -> Optional[tk.Misc]:
        """Get currently focused widget"""
        try:
            return self.root.focus_get()
        except:
            return None

    # Event handlers for keyboard navigation
    def _handle_tab(self, event: tk.Event) -> str:
        """Handle Tab key press"""
        # Only handle if focus is on a registered CTK widget
        current_focus = self.get_current_focus()
        if current_focus in self._focus_order:
            if self.focus_next():
                return "break"
        return ""

    def _handle_shift_tab(self, event: tk.Event) -> str:
        """Handle Shift+Tab key press"""
        current_focus = self.get_current_focus()
        if current_focus in self._focus_order:
            if self.focus_previous():
                return "break"
        return ""

    def _handle_up_arrow(self, event: tk.Event) -> str:
        """Handle Up arrow key press"""
        current_focus = self.get_current_focus()
        if current_focus in self._focus_order:
            # For CTK widgets, up arrow can also navigate
            if self.focus_previous():
                return "break"
        return ""

    def _handle_down_arrow(self, event: tk.Event) -> str:
        """Handle Down arrow key press"""
        current_focus = self.get_current_focus()
        if current_focus in self._focus_order:
            # For CTK widgets, down arrow can also navigate
            if self.focus_next():
                return "break"
        return ""

    def _handle_left_arrow(self, event: tk.Event) -> str:
        """Handle Left arrow key press"""
        # Let the widget handle this normally
        return ""

    def _handle_right_arrow(self, event: tk.Event) -> str:
        """Handle Right arrow key press"""
        # Let the widget handle this normally
        return ""

    def destroy(self) -> None:
        """Clean up the focus manager"""
        self._monitoring = False
        self._focus_indicator.hide_focus()


# Global CTK focus manager instance
_ctk_focus_managers: Dict[tk.Tk, CTKFocusManager] = {}


def get_ctk_focus_manager(root: tk.Tk) -> CTKFocusManager:
    """Get or create CTK focus manager for root window"""
    if root not in _ctk_focus_managers:
        _ctk_focus_managers[root] = CTKFocusManager(root)
    return _ctk_focus_managers[root]


def cleanup_ctk_focus_manager(root: tk.Tk) -> None:
    """Clean up CTK focus manager for root window"""
    if root in _ctk_focus_managers:
        _ctk_focus_managers[root].destroy()
        del _ctk_focus_managers[root]
