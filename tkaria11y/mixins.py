# tkaria11y/mixins.py

"""
Enhanced AccessibleMixin providing comprehensive accessibility features:
- ARIA compliance with full property support
- Platform-specific screen reader integration
- Advanced focus management
- Keyboard navigation
- State management and announcements
- Braille display support
- WCAG 2.1 compliance validation
"""

import tkinter as tk
import threading
import time
from typing import Any, Dict, List, Callable
from .a11y_engine import speak
from .platform_adapter import (
    set_accessible_name,
    set_accessible_description,
    set_accessible_role,
    set_accessible_value,
    set_accessible_state,
    announce,
    is_screen_reader_active,
)
from .aria_compliance import (
    ARIARole,
    ARIAProperty,
    get_default_role,
    validate_aria_compliance,
    calculate_contrast_ratio,
    validate_contrast_ratio,
)


class AccessibleMixin:
    """
    Enhanced accessibility mixin providing full WCAG 2.1 compliance.

    Features:
    - ARIA roles, properties, and states
    - Platform-specific screen reader integration
    - Debounced TTS announcements
    - Keyboard navigation support
    - Focus management
    - State change announcements
    - Braille display integration
    - Contrast validation
    """

    def __init__(
        self,
        *args: Any,
        accessible_name: str = "",
        accessible_role: str = "",
        accessible_description: str = "",
        accessible_value: str = "",
        live_region: str = "off",
        **kwargs: Any,
    ) -> None:
        # Core accessibility properties
        self.accessible_name = accessible_name
        self.accessible_role = accessible_role or self._get_default_role()
        self.accessible_description = accessible_description
        self.accessible_value = accessible_value
        self.live_region = live_region

        # ARIA properties and states
        self._aria_properties: Dict[ARIAProperty, Any] = {}
        self._aria_states: Dict[str, bool] = {}

        # TTS and announcement management
        self._last_announcement_time = 0
        self._announcement_debounce_delay = 0.5  # 500ms debounce
        self._announcement_queue: List[str] = []
        self._announcement_lock = threading.Lock()

        # Focus and interaction tracking
        self._has_focus = False
        self._is_hovered = False
        self._focus_callbacks: List[Callable] = []
        self._state_change_callbacks: List[Callable] = []

        # Keyboard navigation
        self._keyboard_shortcuts: Dict[str, Callable] = {}
        self._supports_arrow_keys = False

        # Validation and compliance
        self._validation_errors: List[str] = []
        self._compliance_level = "AA"  # WCAG compliance level

        super().__init__(*args, **kwargs)

        # Initialize accessibility features
        self._setup_accessibility()

    def _get_default_role(self) -> str:
        """Get default ARIA role for this widget type"""
        try:
            widget_class = self.winfo_class()  # type: ignore
            role = get_default_role(self)  # type: ignore
            return role.value
        except (AttributeError, tk.TclError):
            return "none"

    def _setup_accessibility(self) -> None:
        """Initialize all accessibility features"""
        # Set platform-specific properties
        self._set_platform_properties()

        # Bind accessibility events
        self._bind_accessibility_events()

        # Set up keyboard navigation
        self._setup_keyboard_navigation()

        # Initialize ARIA properties
        self._initialize_aria_properties()

        # Validate accessibility compliance
        self._validate_accessibility()

        # Register with focus manager
        self._register_with_focus_manager()

    def _set_platform_properties(self) -> None:
        """Set platform-specific accessibility properties"""
        if self.accessible_name:
            set_accessible_name(self, self.accessible_name)  # type: ignore

        if self.accessible_description:
            set_accessible_description(self, self.accessible_description)  # type: ignore

        if self.accessible_role:
            set_accessible_role(self, self.accessible_role)  # type: ignore

        if self.accessible_value:
            set_accessible_value(self, self.accessible_value)  # type: ignore

    def _bind_accessibility_events(self) -> None:
        """Bind accessibility-related events"""
        # Try to bind focus events first - these are critical for accessibility
        focus_events_bound = False
        try:
            self.bind("<FocusIn>", self._on_focus_in, add="+")  # type: ignore
            self.bind("<FocusOut>", self._on_focus_out, add="+")  # type: ignore
            focus_events_bound = True
        except (NotImplementedError, AttributeError):
            pass

        # Try to bind other events
        try:
            # Mouse events
            self.bind("<Enter>", self._on_mouse_enter, add="+")  # type: ignore
            self.bind("<Leave>", self._on_mouse_leave, add="+")  # type: ignore

            # State change events
            self.bind("<Configure>", self._on_configure, add="+")  # type: ignore

            # Widget-specific events
            self._bind_widget_specific_events()
        except (NotImplementedError, AttributeError):
            # CustomTkinter widgets don't support traditional event binding
            pass

        # If focus events couldn't be bound, log it for debugging
        if not focus_events_bound:
            print(f"Warning: Could not bind focus events for {self.__class__.__name__}")

    def _bind_widget_specific_events(self) -> None:
        """Bind widget-specific accessibility events"""
        try:
            widget_class = getattr(self, "winfo_class", lambda: "")()

            if widget_class == "Button":
                self.bind("<Button-1>", self._on_button_click, add="+")  # type: ignore
                self.bind("<Return>", self._on_button_activate, add="+")  # type: ignore
                self.bind("<space>", self._on_button_activate, add="+")  # type: ignore

            elif widget_class in ["Checkbutton", "Radiobutton"]:
                self.bind("<Button-1>", self._on_toggle_click, add="+")  # type: ignore
                self.bind("<Return>", self._on_toggle_activate, add="+")  # type: ignore
                self.bind("<space>", self._on_toggle_activate, add="+")  # type: ignore

            elif widget_class in ["Entry", "Text"]:
                self.bind("<KeyPress>", self._on_text_input, add="+")  # type: ignore
                self.bind("<KeyRelease>", self._on_text_change, add="+")  # type: ignore

            elif widget_class == "Scale":
                self.bind("<ButtonRelease-1>", self._on_scale_change, add="+")  # type: ignore
                self.bind("<KeyRelease>", self._on_scale_change, add="+")  # type: ignore

            elif widget_class == "Listbox":
                self.bind("<<ListboxSelect>>", self._on_listbox_select, add="+")  # type: ignore
        except (NotImplementedError, AttributeError):
            # CustomTkinter widgets don't support traditional event binding
            pass

    def _setup_keyboard_navigation(self) -> None:
        """Setup keyboard navigation and shortcuts"""
        # Standard keyboard shortcuts
        self._keyboard_shortcuts.update(
            {
                "<F1>": self._show_help,
                "<Control-h>": self._show_help,
                "<Alt-F4>": self._close_dialog,
            }
        )

        # Bind keyboard shortcuts
        try:
            for key, callback in self._keyboard_shortcuts.items():
                self.bind(key, callback, add="+")  # type: ignore
        except (NotImplementedError, AttributeError):
            # CustomTkinter widgets don't support traditional event binding
            pass

        # Set up arrow key navigation if supported
        widget_class = getattr(self, "winfo_class", lambda: "")()
        if widget_class in ["Scale", "Scrollbar", "Listbox"]:
            self._supports_arrow_keys = True

    def _initialize_aria_properties(self) -> None:
        """Initialize ARIA properties based on widget type and state"""
        # Set basic ARIA properties
        if self.accessible_name:
            self._aria_properties[ARIAProperty.LABEL] = self.accessible_name

        if self.accessible_description:
            self._aria_properties[ARIAProperty.DESCRIBEDBY] = (
                self.accessible_description
            )

        # Set widget-specific ARIA properties
        widget_class = getattr(self, "winfo_class", lambda: "")()

        if widget_class in ["Checkbutton", "Radiobutton"]:
            self._aria_properties[ARIAProperty.CHECKED] = "false"

        elif widget_class == "Scale":
            try:
                from_val = self.cget("from")  # type: ignore
                to_val = self.cget("to")  # type: ignore
                current_val = self.get()  # type: ignore

                self._aria_properties[ARIAProperty.VALUEMIN] = str(from_val)
                self._aria_properties[ARIAProperty.VALUEMAX] = str(to_val)
                self._aria_properties[ARIAProperty.VALUENOW] = str(current_val)
            except (AttributeError, tk.TclError):
                pass

        elif widget_class in ["Entry", "Text"]:
            try:
                state = self.cget("state")  # type: ignore
                self._aria_properties[ARIAProperty.READONLY] = (
                    "true" if state == "readonly" else "false"
                )
            except (AttributeError, tk.TclError):
                pass

    def _validate_accessibility(self) -> None:
        """Validate accessibility compliance"""
        try:
            role = ARIARole(self.accessible_role)
            errors = validate_aria_compliance(self, role, self._aria_properties)  # type: ignore
            self._validation_errors = errors

            # Log validation errors in debug mode
            if errors and hasattr(self, "_debug_accessibility"):
                print(f"Accessibility validation errors for {self}: {errors}")

        except (ValueError, AttributeError):
            # Invalid role or widget doesn't support validation
            pass

    def _register_with_focus_manager(self) -> None:
        """Register widget with global focus manager"""
        try:
            from .focus_manager import get_focus_manager

            root = self.winfo_toplevel()  # type: ignore
            focus_manager = get_focus_manager(root)

            # Only register if this is a focusable widget
            if focus_manager._is_focusable_widget(self):  # type: ignore
                focus_manager.register_widget(self)  # type: ignore
        except (AttributeError, ImportError, tk.TclError):
            # Focus manager not available or widget not ready
            pass

    # Event handlers
    def _on_focus_in(self, event: tk.Event) -> None:
        """Handle focus in event"""
        self._has_focus = True

        # Announce widget with debouncing
        self._announce_widget_focus()

        # Call focus callbacks
        for callback in self._focus_callbacks:
            try:
                callback(self, True)
            except Exception:
                # Ignore callback errors
                pass

        # Update platform accessibility
        set_accessible_state(self, "focused", True)  # type: ignore

    def _on_focus_out(self, event: tk.Event) -> None:
        """Handle focus out event"""
        self._has_focus = False

        # Call focus callbacks
        for callback in self._focus_callbacks:
            try:
                callback(self, False)
            except Exception:
                pass

        # Update platform accessibility
        set_accessible_state(self, "focused", False)  # type: ignore

    def _on_mouse_enter(self, event: tk.Event) -> None:
        """Handle mouse enter event"""
        self._is_hovered = True

        # Announce on hover if no screen reader is active
        if not is_screen_reader_active() and self.accessible_name:
            self._debounced_announce(self.accessible_name, priority="low")

    def _on_mouse_leave(self, event: tk.Event) -> None:
        """Handle mouse leave event"""
        self._is_hovered = False

    def _on_configure(self, event: tk.Event) -> None:
        """Handle widget configuration changes"""
        # Re-validate accessibility when widget changes
        self._validate_accessibility()

    def _on_button_click(self, event: tk.Event) -> None:
        """Handle button click"""
        self._announce_action("activated")

    def _on_button_activate(self, event: tk.Event) -> None:
        """Handle button keyboard activation"""
        self._announce_action("activated")
        return "break"

    def _on_toggle_click(self, event: tk.Event) -> None:
        """Handle toggle button click"""
        # Announce state change after click
        self.after(10, self._announce_toggle_state)  # type: ignore

    def _on_toggle_activate(self, event: tk.Event) -> None:
        """Handle toggle button keyboard activation"""
        # Announce state change after activation
        self.after(10, self._announce_toggle_state)  # type: ignore
        return "break"

    def _on_text_input(self, event: tk.Event) -> None:
        """Handle text input"""
        # Announce character input for screen readers
        if event.char and event.char.isprintable():
            self._debounced_announce(event.char, priority="low")

    def _on_text_change(self, event: tk.Event) -> None:
        """Handle text change"""
        # Update accessible value
        try:
            current_value = self.get()  # type: ignore
            self.set_accessible_value(str(current_value))
        except (AttributeError, tk.TclError):
            pass

    def _on_scale_change(self, event: tk.Event) -> None:
        """Handle scale value change"""
        try:
            current_value = self.get()  # type: ignore
            self._aria_properties[ARIAProperty.VALUENOW] = str(current_value)
            self._announce_value_change(current_value)
        except (AttributeError, tk.TclError):
            pass

    def _on_listbox_select(self, event: tk.Event) -> None:
        """Handle listbox selection"""
        try:
            selection = self.curselection()  # type: ignore
            if selection:
                selected_text = self.get(selection[0])  # type: ignore
                self._debounced_announce(f"Selected: {selected_text}")
        except (AttributeError, tk.TclError):
            pass

    # Announcement methods
    def _announce_widget_focus(self) -> None:
        """Announce widget when it receives focus"""
        announcement_parts = []

        # Add role
        if self.accessible_role and self.accessible_role != "none":
            announcement_parts.append(self.accessible_role)

        # Add name
        if self.accessible_name:
            announcement_parts.append(self.accessible_name)

        # Add value if applicable
        if self.accessible_value:
            announcement_parts.append(self.accessible_value)

        # Add state information
        state_info = self._get_state_announcement()
        if state_info:
            announcement_parts.append(state_info)

        # Add description
        if self.accessible_description:
            announcement_parts.append(self.accessible_description)

        if announcement_parts:
            announcement = ", ".join(announcement_parts)
            self._debounced_announce(announcement)

    def _announce_toggle_state(self) -> None:
        """Announce toggle button state"""
        try:
            # Get current state
            var = self.cget("variable")  # type: ignore
            if var:
                value = var.get()
                state = "checked" if value else "unchecked"
            else:
                # Fallback to widget state
                state = "checked" if self.cget("state") == "active" else "unchecked"  # type: ignore

            self._aria_properties[ARIAProperty.CHECKED] = (
                "true" if state == "checked" else "false"
            )
            self._debounced_announce(state)

        except (AttributeError, tk.TclError):
            pass

    def _announce_value_change(self, value: Any) -> None:
        """Announce value change"""
        self._debounced_announce(str(value))

    def _announce_action(self, action: str) -> None:
        """Announce widget action"""
        announcement = (
            f"{self.accessible_name} {action}" if self.accessible_name else action
        )
        self._debounced_announce(announcement)

    def _get_state_announcement(self) -> str:
        """Get current state for announcement"""
        states = []

        try:
            # Check disabled state
            try:
                if self.cget("state") == "disabled":  # type: ignore
                    states.append("disabled")
            except (tk.TclError, ValueError):
                # Widget doesn't support state attribute (e.g., CTkFrame and some other widgets)
                pass

            # Check widget-specific states
            widget_class = getattr(self, "winfo_class", lambda: "")()

            if widget_class in ["Checkbutton", "Radiobutton"]:
                var = self.cget("variable")  # type: ignore
                if var and var.get():
                    states.append("checked")

            elif widget_class == "Entry":
                if self.cget("show"):  # type: ignore
                    states.append("password field")

        except (AttributeError, tk.TclError):
            pass

        return ", ".join(states)

    def _debounced_announce(self, message: str, priority: str = "medium") -> None:
        """Announce message with debouncing to prevent chattiness"""
        current_time = time.time()

        with self._announcement_lock:
            # Check if we should debounce
            if (
                current_time - self._last_announcement_time
                < self._announcement_debounce_delay
            ):
                # Add to queue instead of announcing immediately
                self._announcement_queue.append(message)
                return

            self._last_announcement_time = current_time

        # Announce immediately
        self._do_announce(message, priority)

        # Process queued announcements after delay
        if self._announcement_queue:
            self.after(int(self._announcement_debounce_delay * 1000), self._process_announcement_queue)  # type: ignore

    def _process_announcement_queue(self) -> None:
        """Process queued announcements"""
        with self._announcement_lock:
            if self._announcement_queue:
                # Announce the last queued message
                message = self._announcement_queue[-1]
                self._announcement_queue.clear()
                self._do_announce(message)

    def _do_announce(self, message: str, priority: str = "medium") -> None:
        """Perform the actual announcement"""
        # Use platform-specific announcement if screen reader is active
        if is_screen_reader_active():
            announce(message, priority)
        else:
            # Fall back to TTS
            speak(message)

    # Keyboard shortcut handlers
    def _show_help(self, event: tk.Event) -> str:
        """Show help for the widget"""
        help_text = (
            self.accessible_description
            or f"Help for {self.accessible_name or 'widget'}"
        )
        self._debounced_announce(help_text)
        return "break"

    def _close_dialog(self, event: tk.Event) -> str:
        """Close dialog if this is a dialog widget"""
        try:
            if self.winfo_class() == "Toplevel":  # type: ignore
                self.destroy()  # type: ignore
                return "break"
        except (AttributeError, tk.TclError):
            pass
        return ""

    # Public API methods
    def set_accessible_name(self, name: str) -> None:
        """Set accessible name"""
        self.accessible_name = name
        self._aria_properties[ARIAProperty.LABEL] = name
        set_accessible_name(self, name)  # type: ignore

    def set_accessible_description(self, description: str) -> None:
        """Set accessible description"""
        self.accessible_description = description
        self._aria_properties[ARIAProperty.DESCRIBEDBY] = description
        set_accessible_description(self, description)  # type: ignore

    def set_accessible_role(self, role: str) -> None:
        """Set accessible role"""
        self.accessible_role = role
        set_accessible_role(self, role)  # type: ignore

    def set_accessible_value(self, value: str) -> None:
        """Set accessible value"""
        self.accessible_value = value
        set_accessible_value(self, value)  # type: ignore

    def set_aria_property(self, property: ARIAProperty, value: Any) -> None:
        """Set ARIA property"""
        self._aria_properties[property] = value

        # Update platform-specific properties
        if property == ARIAProperty.CHECKED:
            set_accessible_state(self, "checked", value == "true")  # type: ignore
        elif property == ARIAProperty.EXPANDED:
            set_accessible_state(self, "expanded", value == "true")  # type: ignore
        elif property == ARIAProperty.SELECTED:
            set_accessible_state(self, "selected", value == "true")  # type: ignore

    def get_aria_property(self, property: ARIAProperty) -> Any:
        """Get ARIA property value"""
        return self._aria_properties.get(property)

    def add_focus_callback(self, callback: Callable) -> None:
        """Add focus change callback"""
        self._focus_callbacks.append(callback)

    def remove_focus_callback(self, callback: Callable) -> None:
        """Remove focus change callback"""
        try:
            self._focus_callbacks.remove(callback)
        except ValueError:
            pass

    def add_state_change_callback(self, callback: Callable) -> None:
        """Add state change callback"""
        self._state_change_callbacks.append(callback)

    def remove_state_change_callback(self, callback: Callable) -> None:
        """Remove state change callback"""
        try:
            self._state_change_callbacks.remove(callback)
        except ValueError:
            pass

    def set_keyboard_shortcut(self, key: str, callback: Callable) -> None:
        """Set custom keyboard shortcut"""
        self._keyboard_shortcuts[key] = callback
        self.bind(key, callback, add="+")  # type: ignore

    def remove_keyboard_shortcut(self, key: str) -> None:
        """Remove keyboard shortcut"""
        if key in self._keyboard_shortcuts:
            del self._keyboard_shortcuts[key]
            self.unbind(key)  # type: ignore

    def validate_accessibility_compliance(self) -> List[str]:
        """Validate accessibility compliance and return errors"""
        self._validate_accessibility()
        return self._validation_errors.copy()

    def set_compliance_level(self, level: str) -> None:
        """Set WCAG compliance level (A, AA, AAA)"""
        if level in ["A", "AA", "AAA"]:
            self._compliance_level = level
            self._validate_accessibility()

    def is_accessible(self) -> bool:
        """Check if widget meets accessibility requirements"""
        return len(self._validation_errors) == 0

    def get_accessibility_info(self) -> Dict[str, Any]:
        """Get comprehensive accessibility information"""
        return {
            "accessible_name": self.accessible_name,
            "accessible_role": self.accessible_role,
            "accessible_description": self.accessible_description,
            "accessible_value": self.accessible_value,
            "aria_properties": self._aria_properties.copy(),
            "aria_states": self._aria_states.copy(),
            "validation_errors": self._validation_errors.copy(),
            "compliance_level": self._compliance_level,
            "has_focus": self._has_focus,
            "is_hovered": self._is_hovered,
            "supports_keyboard": bool(self._keyboard_shortcuts),
        }

    def announce(self, message: str, priority: str = "medium") -> None:
        """Manually announce a message"""
        self._debounced_announce(message, priority)

    def set_live_region(self, live_type: str) -> None:
        """Set live region type (off, polite, assertive)"""
        if live_type in ["off", "polite", "assertive"]:
            self.live_region = live_type
            self._aria_properties[ARIAProperty.LIVE] = live_type


class BrailleMixin:
    """
    Mixin for braille display support.
    Provides integration with braille displays for tactile feedback.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._braille_enabled = False
        self._braille_text = ""
        self._init_braille_support()

    def _init_braille_support(self) -> None:
        """Initialize braille display support"""
        try:
            # Try to detect braille display
            self._braille_enabled = self._detect_braille_display()
        except Exception:
            self._braille_enabled = False

    def _detect_braille_display(self) -> bool:
        """Detect if braille display is available"""
        # This would integrate with braille display APIs
        # For now, return False as placeholder
        return False

    def set_braille_text(self, text: str) -> None:
        """Set text for braille display"""
        self._braille_text = text
        if self._braille_enabled:
            self._send_to_braille_display(text)

    def _send_to_braille_display(self, text: str) -> None:
        """Send text to braille display"""
        # Placeholder for braille display integration
        pass

    def get_braille_text(self) -> str:
        """Get current braille text"""
        return self._braille_text


class HighContrastMixin:
    """
    Mixin for high contrast support and color validation.
    Ensures WCAG contrast compliance.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._contrast_validated = False
        self._init_contrast_validation()

    def _init_contrast_validation(self) -> None:
        """Initialize contrast validation"""
        self.bind("<Configure>", self._validate_contrast, add="+")  # type: ignore

    def _validate_contrast(self, event: tk.Event = None) -> None:
        """Validate color contrast"""
        try:
            fg_color = self.cget("fg") or self.cget("foreground")  # type: ignore
            bg_color = self.cget("bg") or self.cget("background")  # type: ignore

            if fg_color and bg_color:
                contrast_ratio = calculate_contrast_ratio(fg_color, bg_color)
                self._contrast_validated = validate_contrast_ratio(
                    fg_color, bg_color, level="AA", size="normal"
                )

                if not self._contrast_validated:
                    print(
                        f"Warning: Insufficient contrast ratio {contrast_ratio:.2f} for widget {self}"
                    )

        except (AttributeError, tk.TclError):
            # Widget doesn't support color configuration
            pass

    def is_contrast_compliant(self) -> bool:
        """Check if widget meets contrast requirements"""
        return self._contrast_validated

    def get_contrast_ratio(self) -> float:
        """Get current contrast ratio"""
        try:
            fg_color = self.cget("fg") or self.cget("foreground")  # type: ignore
            bg_color = self.cget("bg") or self.cget("background")  # type: ignore

            if fg_color and bg_color:
                return calculate_contrast_ratio(fg_color, bg_color)
        except (AttributeError, tk.TclError):
            pass

        return 1.0  # Minimum ratio


# Combined accessibility mixin with all features
class ComprehensiveAccessibilityMixin(AccessibleMixin, BrailleMixin, HighContrastMixin):
    """
    Comprehensive accessibility mixin combining all accessibility features:
    - Full ARIA compliance
    - Platform integration
    - Braille support
    - High contrast validation
    - Advanced focus management
    - Keyboard navigation
    - TTS integration
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_comprehensive_accessibility_report(self) -> Dict[str, Any]:
        """Get comprehensive accessibility report"""
        base_info = self.get_accessibility_info()
        base_info.update(
            {
                "braille_enabled": getattr(self, "_braille_enabled", False),
                "braille_text": getattr(self, "_braille_text", ""),
                "contrast_validated": getattr(self, "_contrast_validated", False),
                "contrast_ratio": self.get_contrast_ratio(),
            }
        )
        return base_info
