# tkaria11y/focus_manager.py

"""
Advanced focus management system for full keyboard accessibility.
Provides logical focus traversal, focus indicators, and keyboard navigation.
"""

import tkinter as tk
from typing import List, Optional, Dict, Callable, Set
import weakref
from enum import Enum


class FocusDirection(Enum):
    """Focus traversal directions"""

    NEXT = "next"
    PREVIOUS = "previous"
    FIRST = "first"
    LAST = "last"
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class FocusIndicator:
    """Visual focus indicator for accessibility"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self._indicator_canvas: Optional[tk.Canvas] = None
        self._current_widget: Optional[tk.Misc] = None
        self._indicator_color = "#FFD700"  # Gold color for high visibility
        self._indicator_width = 3
        self._create_indicator()

    def _create_indicator(self) -> None:
        """Create the focus indicator canvas"""
        self._indicator_canvas = tk.Canvas(
            self.root, highlightthickness=0, bd=0, height=0, width=0
        )
        self._indicator_canvas.place(x=0, y=0)
        # Ensure indicator is always on top
        try:
            self._indicator_canvas.tkraise()  # type: ignore[call-arg]
        except tk.TclError:
            pass

    def show_focus(self, widget: tk.Misc) -> None:
        """Show focus indicator around widget"""
        self._current_widget = widget
        
        try:
            # Get widget position and size
            x = widget.winfo_x()
            y = widget.winfo_y()
            width = widget.winfo_width()
            height = widget.winfo_height()
            
            # Convert to root coordinates
            root_x = widget.winfo_rootx() - self.root.winfo_rootx()
            root_y = widget.winfo_rooty() - self.root.winfo_rooty()
            
            # Clear previous indicator
            if self._indicator_canvas:
                self._indicator_canvas.delete("focus_indicator")
            
            # Create canvas overlay for focus indicator
            if not self._indicator_canvas:
                self._create_indicator()
            
            # Position and size the canvas
            self._indicator_canvas.place(
                x=root_x - self._indicator_width,
                y=root_y - self._indicator_width,
                width=width + 2 * self._indicator_width,
                height=height + 2 * self._indicator_width
            )
            
            # Draw focus rectangle
            self._indicator_canvas.create_rectangle(
                0, 0,
                width + 2 * self._indicator_width,
                height + 2 * self._indicator_width,
                outline=self._indicator_color,
                width=self._indicator_width,
                fill="",
                tags="focus_indicator"
            )
            
            # Ensure indicator is on top but doesn't block events
            self._indicator_canvas.tkraise()
            
        except tk.TclError:
            # Widget may have been destroyed or not ready
            pass

    def hide_focus(self) -> None:
        """Hide focus indicator"""
        if self._indicator_canvas:
            self._indicator_canvas.delete("focus_indicator")
            self._indicator_canvas.place_forget()
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

    def set_width(self, width: int) -> None:
        """Set focus indicator width"""
        self._indicator_width = width
        if self._current_widget:
            self.show_focus(self._current_widget)


class FocusManager:
    """Advanced focus management system"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self._focus_order: List[tk.Misc] = []
        self._focus_groups: Dict[str, List[tk.Misc]] = {}
        self._current_focus_index = 0
        self._focus_indicator = FocusIndicator(root)
        self._focus_callbacks: Dict[tk.Misc, List[Callable]] = {}
        self._skip_widgets: Set[tk.Misc] = set()
        self._focus_history: List[tk.Misc] = []
        self._max_history = 10

        # Bind global focus events
        self._setup_global_bindings()

        # Track widget destruction
        self._widget_refs: weakref.WeakSet = weakref.WeakSet()
        
        # Initialize CTK focus manager if available
        self._ctk_focus_manager = None
        try:
            from .ctk_focus_manager import get_ctk_focus_manager
            self._ctk_focus_manager = get_ctk_focus_manager(root)
        except ImportError:
            pass

    def _setup_global_bindings(self) -> None:
        """Setup global keyboard bindings for focus management"""
        # Tab navigation
        self.root.bind_all("<Tab>", self._handle_tab, add="+")
        self.root.bind_all("<Shift-Tab>", self._handle_shift_tab, add="+")

        # Arrow key navigation
        self.root.bind_all("<Up>", self._handle_up_arrow, add="+")
        self.root.bind_all("<Down>", self._handle_down_arrow, add="+")
        self.root.bind_all("<Left>", self._handle_left_arrow, add="+")
        self.root.bind_all("<Right>", self._handle_right_arrow, add="+")

        # Home/End navigation
        self.root.bind_all("<Home>", self._handle_home, add="+")
        self.root.bind_all("<End>", self._handle_end, add="+")

        # Focus events
        self.root.bind_all("<FocusIn>", self._handle_focus_in, add="+")
        self.root.bind_all("<FocusOut>", self._handle_focus_out, add="+")

        # Escape key for focus restoration
        self.root.bind_all("<Escape>", self._handle_escape, add="+")

    def register_widget(
        self,
        widget: tk.Misc,
        focus_group: Optional[str] = None,
        skip_focus: bool = False,
    ) -> None:
        """Register a widget for focus management"""
        if skip_focus:
            self._skip_widgets.add(widget)
            return

        # Only register focusable widgets
        if not self._is_focusable_widget(widget):
            return

        # Check if this is a CustomTkinter widget
        is_ctk_widget = self._is_ctk_widget(widget)
        
        if widget not in self._focus_order:
            self._focus_order.append(widget)
            self._widget_refs.add(widget)

        if focus_group:
            if focus_group not in self._focus_groups:
                self._focus_groups[focus_group] = []
            if widget not in self._focus_groups[focus_group]:
                self._focus_groups[focus_group].append(widget)

        # Set up widget-specific bindings
        if is_ctk_widget and self._ctk_focus_manager:
            # Register with CTK focus manager
            self._ctk_focus_manager.register_widget(widget, focus_group)
        else:
            # Regular widget binding
            self._setup_widget_bindings(widget)

    def unregister_widget(self, widget: tk.Misc) -> None:
        """Unregister a widget from focus management"""
        if widget in self._focus_order:
            self._focus_order.remove(widget)

        if widget in self._skip_widgets:
            self._skip_widgets.remove(widget)

        # Remove from focus groups
        for group_widgets in self._focus_groups.values():
            if widget in group_widgets:
                group_widgets.remove(widget)

        # Remove callbacks
        if widget in self._focus_callbacks:
            del self._focus_callbacks[widget]

        # Remove from history
        while widget in self._focus_history:
            self._focus_history.remove(widget)
    
    def _is_ctk_widget(self, widget: tk.Misc) -> bool:
        """Check if widget is a CustomTkinter widget"""
        widget_module = getattr(widget.__class__, '__module__', '')
        widget_class = widget.__class__.__name__
        return 'customtkinter' in widget_module or widget_class.startswith('CTk') or 'AccessibleCTK' in widget_class
    
    def _is_focusable_widget(self, widget: tk.Misc) -> bool:
        """Check if widget can receive focus (interactive widgets only)"""
        widget_class = widget.__class__.__name__
        
        # Interactive widget types that should receive focus
        focusable_types = {
            # Tkinter widgets
            'Button', 'Entry', 'Text', 'Listbox', 'Scale', 'Spinbox', 'Checkbutton', 'Radiobutton',
            # TTK widgets  
            'TtkButton', 'TtkEntry', 'TtkCombobox', 'TtkScale', 'TtkSpinbox', 'TtkCheckbutton', 'TtkRadiobutton',
            # Accessible widgets
            'AccessibleButton', 'AccessibleEntry', 'AccessibleText', 'AccessibleListbox', 'AccessibleScale',
            'AccessibleSpinbox', 'AccessibleCheckbutton', 'AccessibleRadiobutton',
            'AccessibleTTKButton', 'AccessibleTTKEntry', 'AccessibleTTKCombobox', 'AccessibleTTKScale',
            'AccessibleTTKSpinbox', 'AccessibleTTKCheckbutton', 'AccessibleTTKRadiobutton',
            # CustomTkinter widgets
            'CTkButton', 'CTkEntry', 'CTkCheckBox', 'CTkRadioButton', 'CTkSlider', 'CTkComboBox',
            'AccessibleCTKButton', 'AccessibleCTKEntry', 'AccessibleCTKCheckBox', 'AccessibleCTKRadioButton', 
            'AccessibleCTKSlider', 'AccessibleCTKComboBox'
        }
        
        # Check if widget type is focusable
        if widget_class in focusable_types:
            return True
            
        # Check if widget can actually take focus (skip for CTK widgets)
        if not self._is_ctk_widget(widget):
            try:
                # Try to check if widget has takefocus option
                takefocus = widget.cget('takefocus')
                if takefocus == 1 or takefocus == '1' or takefocus is True:
                    return True
                elif takefocus == 0 or takefocus == '0' or takefocus is False:
                    return False
            except (tk.TclError, AttributeError, ValueError):
                pass
        
        # For CustomTkinter widgets, check if they have focus methods
        if hasattr(widget, 'focus_set') and hasattr(widget, 'focus_get'):
            # Additional check for CTK widgets - they should be interactive
            if any(keyword in widget_class.lower() for keyword in ['button', 'entry', 'checkbox', 'radio', 'slider', 'combo']):
                return True
        
        return False

    def _setup_widget_bindings(self, widget: tk.Misc) -> None:
        """Setup widget-specific focus bindings"""
        try:
            # Bind focus events to show/hide indicator
            widget.bind("<FocusIn>", lambda e: self._show_focus_indicator(widget), add="+")
            widget.bind("<FocusOut>", lambda e: self._hide_focus_indicator(), add="+")

            # Bind configuration changes to update indicator
            widget.bind("<Configure>", lambda e: self._update_focus_indicator(), add="+")
        except (NotImplementedError, AttributeError, tk.TclError):
            # Widget doesn't support binding (e.g., CustomTkinter widgets)
            # For these widgets, we'll rely on manual focus tracking
            pass

    def add_focus_callback(self, widget: tk.Misc, callback: Callable) -> None:
        """Add a callback to be called when widget receives focus"""
        if widget not in self._focus_callbacks:
            self._focus_callbacks[widget] = []
        self._focus_callbacks[widget].append(callback)

    def remove_focus_callback(self, widget: tk.Misc, callback: Callable) -> None:
        """Remove a focus callback"""
        if widget in self._focus_callbacks:
            try:
                self._focus_callbacks[widget].remove(callback)
            except ValueError:
                pass

    def set_focus_order(self, widgets: List[tk.Misc]) -> None:
        """Set explicit focus order"""
        self._focus_order = [w for w in widgets if w not in self._skip_widgets]
        self._current_focus_index = 0

    def get_focus_order(self) -> List[tk.Misc]:
        """Get current focus order"""
        return self._focus_order.copy()

    def focus_next(self) -> bool:
        """Move focus to next widget"""
        return self._move_focus(FocusDirection.NEXT)

    def focus_previous(self) -> bool:
        """Move focus to previous widget"""
        return self._move_focus(FocusDirection.PREVIOUS)

    def focus_first(self) -> bool:
        """Move focus to first widget"""
        return self._move_focus(FocusDirection.FIRST)

    def focus_last(self) -> bool:
        """Move focus to last widget"""
        return self._move_focus(FocusDirection.LAST)

    def focus_widget(self, widget: tk.Misc) -> bool:
        """Set focus to specific widget"""
        if widget in self._skip_widgets:
            return False

        if not self._is_widget_focusable(widget):
            return False

        try:
            widget.focus_set()
            self._update_focus_index(widget)
            self._add_to_history(widget)
            return True
        except tk.TclError:
            return False

    def get_current_focus(self) -> Optional[tk.Misc]:
        """Get currently focused widget"""
        try:
            return self.root.focus_get()
        except tk.TclError:
            return None

    def restore_previous_focus(self) -> bool:
        """Restore focus to previous widget in history"""
        if len(self._focus_history) > 1:
            # Remove current focus from history
            self._focus_history.pop()
            # Get previous focus
            previous_widget = self._focus_history[-1]
            return self.focus_widget(previous_widget)
        return False

    def create_focus_group(self, name: str, widgets: List[tk.Misc]) -> None:
        """Create a focus group for related widgets"""
        self._focus_groups[name] = [w for w in widgets if w not in self._skip_widgets]

    def focus_group_next(self, group_name: str) -> bool:
        """Move focus to next widget in group"""
        if group_name not in self._focus_groups:
            return False

        group_widgets = self._focus_groups[group_name]
        if not group_widgets:
            return False

        current_widget = self.get_current_focus()
        if current_widget in group_widgets:
            current_index = group_widgets.index(current_widget)
            next_index = (current_index + 1) % len(group_widgets)
        else:
            next_index = 0

        return self.focus_widget(group_widgets[next_index])

    def focus_group_previous(self, group_name: str) -> bool:
        """Move focus to previous widget in group"""
        if group_name not in self._focus_groups:
            return False

        group_widgets = self._focus_groups[group_name]
        if not group_widgets:
            return False

        current_widget = self.get_current_focus()
        if current_widget in group_widgets:
            current_index = group_widgets.index(current_widget)
            prev_index = (current_index - 1) % len(group_widgets)
        else:
            prev_index = len(group_widgets) - 1

        return self.focus_widget(group_widgets[prev_index])

    def _move_focus(self, direction: FocusDirection) -> bool:
        """Move focus in specified direction"""
        if not self._focus_order:
            return False

        # Clean up destroyed widgets
        self._cleanup_destroyed_widgets()

        if direction == FocusDirection.NEXT:
            self._current_focus_index = (self._current_focus_index + 1) % len(
                self._focus_order
            )
        elif direction == FocusDirection.PREVIOUS:
            self._current_focus_index = (self._current_focus_index - 1) % len(
                self._focus_order
            )
        elif direction == FocusDirection.FIRST:
            self._current_focus_index = 0
        elif direction == FocusDirection.LAST:
            self._current_focus_index = len(self._focus_order) - 1

        # Find next focusable widget
        attempts = 0
        while attempts < len(self._focus_order):
            widget = self._focus_order[self._current_focus_index]
            if self._is_focusable_widget(widget):
                try:
                    # Special handling for CustomTkinter widgets
                    if self._is_ctk_widget(widget):
                        # For CTK widgets, we need to focus the underlying tkinter widget
                        self._focus_ctk_widget(widget)
                    else:
                        widget.focus_set()
                    
                    self._add_to_history(widget)
                    return True
                except tk.TclError:
                    # Widget was destroyed, remove it
                    self._focus_order.remove(widget)
                    if self._current_focus_index >= len(self._focus_order):
                        self._current_focus_index = 0
            else:
                # Move to next widget
                if (
                    direction == FocusDirection.NEXT
                    or direction == FocusDirection.FIRST
                ):
                    self._current_focus_index = (self._current_focus_index + 1) % len(
                        self._focus_order
                    )
                else:
                    self._current_focus_index = (self._current_focus_index - 1) % len(
                        self._focus_order
                    )

            attempts += 1

        return False
    
    def _focus_ctk_widget(self, widget: tk.Misc) -> None:
        """Focus a CustomTkinter widget properly"""
        try:
            # For CTK widgets, focus the appropriate internal widget
            widget_class = widget.__class__.__name__
            
            if 'Button' in widget_class:
                # For CTK buttons, focus the text label or canvas
                if hasattr(widget, '_text_label'):
                    widget._text_label.focus_set()
                elif hasattr(widget, '_canvas'):
                    widget._canvas.focus_set()
                else:
                    widget.focus_set()
            
            elif 'Entry' in widget_class:
                # For CTK entries, focus the internal entry widget
                if hasattr(widget, '_entry'):
                    widget._entry.focus_set()
                else:
                    widget.focus_set()
            
            else:
                # For other CTK widgets, try canvas first, then standard focus
                if hasattr(widget, '_canvas'):
                    widget._canvas.focus_set()
                else:
                    widget.focus_set()
            
        except (AttributeError, tk.TclError):
            # Fallback to standard focus
            try:
                widget.focus_set()
            except tk.TclError:
                pass
    
    def _find_parent_ctk_widget(self, widget: tk.Misc) -> Optional[tk.Misc]:
        """Find the parent CTK widget if this is an internal widget"""
        try:
            # Check if the widget's parent is a registered CTK widget
            parent = widget.master
            while parent:
                if parent in self._focus_order and self._is_ctk_widget(parent):
                    # Check if this widget is an internal component
                    if (hasattr(parent, '_canvas') and widget == parent._canvas) or \
                       (hasattr(parent, '_text_label') and widget == parent._text_label) or \
                       (hasattr(parent, '_entry') and widget == parent._entry):
                        return parent
                
                # Move up the widget hierarchy
                parent = parent.master
            
            return None
        except (AttributeError, tk.TclError):
            return None

    def _is_widget_focusable(self, widget: tk.Misc) -> bool:
        """Check if widget can receive focus (runtime check)"""
        try:
            # Check if widget exists
            if not widget.winfo_exists():
                return False

            # For CustomTkinter widgets, use the type-based check
            if self._is_ctk_widget(widget):
                return self._is_focusable_widget(widget)

            # Check if widget is visible (skip for now as widgets might not be mapped yet)
            # if not widget.winfo_viewable():
            #     return False

            # Check takefocus setting (only for non-CTK widgets)
            try:
                takefocus = widget.cget("takefocus")
                if takefocus == 0 or takefocus == '0' or takefocus is False:
                    return False
            except (tk.TclError, ValueError):
                pass

            # Check if widget is disabled
            try:
                state = widget.cget("state")
                if state == "disabled":
                    return False
            except (tk.TclError, ValueError):
                pass

            return True

        except tk.TclError:
            return False

    def _update_focus_index(self, widget: tk.Misc) -> None:
        """Update current focus index based on widget"""
        try:
            self._current_focus_index = self._focus_order.index(widget)
        except ValueError:
            # Widget not in focus order
            pass

    def _add_to_history(self, widget: tk.Misc) -> None:
        """Add widget to focus history"""
        if widget in self._focus_history:
            self._focus_history.remove(widget)

        self._focus_history.append(widget)

        # Limit history size
        if len(self._focus_history) > self._max_history:
            self._focus_history.pop(0)

    def _cleanup_destroyed_widgets(self) -> None:
        """Remove destroyed widgets from focus order"""
        self._focus_order = [w for w in self._focus_order if self._widget_exists(w)]

        # Clean up focus groups
        for group_name in self._focus_groups:
            self._focus_groups[group_name] = [
                w for w in self._focus_groups[group_name] if self._widget_exists(w)
            ]

        # Clean up history
        self._focus_history = [w for w in self._focus_history if self._widget_exists(w)]

    def _widget_exists(self, widget: tk.Misc) -> bool:
        """Check if widget still exists"""
        try:
            widget.winfo_exists()
            return True
        except tk.TclError:
            return False

    def _show_focus_indicator(self, widget: tk.Misc) -> None:
        """Show focus indicator for widget"""
        self._focus_indicator.show_focus(widget)

    def _hide_focus_indicator(self) -> None:
        """Hide focus indicator"""
        self._focus_indicator.hide_focus()

    def _update_focus_indicator(self) -> None:
        """Update focus indicator position"""
        self._focus_indicator.update_focus()

    # Event handlers
    def _handle_tab(self, event: tk.Event) -> str:
        """Handle Tab key press"""
        if self.focus_next():
            return "break"
        return ""

    def _handle_shift_tab(self, event: tk.Event) -> str:
        """Handle Shift+Tab key press"""
        if self.focus_previous():
            return "break"
        return ""

    def _handle_up_arrow(self, event: tk.Event) -> str:
        """Handle Up arrow key press"""
        # Only handle if current widget doesn't use arrow keys
        current_widget = self.get_current_focus()
        if current_widget and self._widget_uses_arrow_keys(current_widget):
            return ""

        if self.focus_previous():
            return "break"
        return ""

    def _handle_down_arrow(self, event: tk.Event) -> str:
        """Handle Down arrow key press"""
        current_widget = self.get_current_focus()
        if current_widget and self._widget_uses_arrow_keys(current_widget):
            return ""

        if self.focus_next():
            return "break"
        return ""

    def _handle_left_arrow(self, event: tk.Event) -> str:
        """Handle Left arrow key press"""
        current_widget = self.get_current_focus()
        if current_widget and self._widget_uses_arrow_keys(current_widget):
            return ""

        if self.focus_previous():
            return "break"
        return ""

    def _handle_right_arrow(self, event: tk.Event) -> str:
        """Handle Right arrow key press"""
        current_widget = self.get_current_focus()
        if current_widget and self._widget_uses_arrow_keys(current_widget):
            return ""

        if self.focus_next():
            return "break"
        return ""

    def _handle_home(self, event: tk.Event) -> str:
        """Handle Home key press"""
        if self.focus_first():
            return "break"
        return ""

    def _handle_end(self, event: tk.Event) -> str:
        """Handle End key press"""
        if self.focus_last():
            return "break"
        return ""

    def _handle_escape(self, event: tk.Event) -> str:
        """Handle Escape key press"""
        if self.restore_previous_focus():
            return "break"
        return ""

    def _handle_focus_in(self, event: tk.Event) -> None:
        """Handle FocusIn event"""
        widget = event.widget

        # Check if this is an internal widget of a registered CTK widget
        actual_widget = self._find_parent_ctk_widget(widget)
        if actual_widget:
            widget = actual_widget

        # Only handle registered widgets
        if widget not in self._focus_order:
            return

        # Show focus indicator
        self._focus_indicator.show_focus(widget)

        # Update focus index
        self._update_focus_index(widget)

        # Add to history
        self._add_to_history(widget)

        # Call focus callbacks
        if widget in self._focus_callbacks:
            for callback in self._focus_callbacks[widget]:
                try:
                    callback(widget)
                except Exception:
                    # Ignore callback errors
                    pass

    def _handle_focus_out(self, event: tk.Event) -> None:
        """Handle FocusOut event"""
        # Hide focus indicator when focus leaves
        # (Will be shown again by FocusIn if focus moves to another managed widget)
        pass

    def _widget_uses_arrow_keys(self, widget: tk.Misc) -> bool:
        """Check if widget uses arrow keys for its own navigation"""
        widget_class = widget.winfo_class()
        arrow_key_widgets = [
            "Entry",
            "Text",
            "Listbox",
            "Scale",
            "Scrollbar",
            "Spinbox",
            "ttk.Entry",
            "ttk.Spinbox",
            "ttk.Scale",
            "ttk.Treeview",
            "ttk.Combobox",
        ]
        return widget_class in arrow_key_widgets

    # Configuration methods
    def set_focus_indicator_color(self, color: str) -> None:
        """Set focus indicator color"""
        self._focus_indicator.set_color(color)

    def set_focus_indicator_width(self, width: int) -> None:
        """Set focus indicator width"""
        self._focus_indicator.set_width(width)

    def enable_focus_indicator(self, enabled: bool = True) -> None:
        """Enable or disable focus indicator"""
        if not enabled:
            self._focus_indicator.hide_focus()


# Global focus manager instance
_focus_manager: Optional[FocusManager] = None


def get_focus_manager(root: tk.Tk) -> FocusManager:
    """Get or create global focus manager"""
    global _focus_manager
    if _focus_manager is None:
        _focus_manager = FocusManager(root)
    return _focus_manager


def configure_advanced_focus_traversal(
    root: tk.Tk, widgets: Optional[List[tk.Widget]] = None
) -> FocusManager:
    """Configure advanced focus traversal for a window"""
    focus_manager = get_focus_manager(root)

    if widgets:
        for widget in widgets:
            focus_manager.register_widget(widget)
    else:
        # Auto-discover focusable widgets
        _auto_register_widgets(root, focus_manager)

    return focus_manager


def _auto_register_widgets(parent: tk.Misc, focus_manager: FocusManager) -> None:
    """Automatically register focusable widgets"""
    try:
        for child in parent.winfo_children():
            # Register child if it's focusable
            if _is_potentially_focusable(child):
                focus_manager.register_widget(child)

            # Recursively process children
            _auto_register_widgets(child, focus_manager)
    except tk.TclError:
        # Parent was destroyed
        pass


def _is_potentially_focusable(widget: tk.Misc) -> bool:
    """Check if widget is potentially focusable"""
    focusable_classes = [
        "Button",
        "Entry",
        "Text",
        "Checkbutton",
        "Radiobutton",
        "Scale",
        "Listbox",
        "Scrollbar",
        "Spinbox",
        "Canvas",
        "ttk.Button",
        "ttk.Entry",
        "ttk.Checkbutton",
        "ttk.Radiobutton",
        "ttk.Scale",
        "ttk.Scrollbar",
        "ttk.Spinbox",
        "ttk.Combobox",
        "ttk.Treeview",
        "ttk.Notebook",
    ]

    widget_class = widget.winfo_class()
    return widget_class in focusable_classes
