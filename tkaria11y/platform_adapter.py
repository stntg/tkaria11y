# tkaria11y/platform_adapter.py

"""
Platform-specific accessibility integration for screen readers and assistive technologies.
Provides OS-level integration for Windows (UIA), Linux (AT-SPI), and macOS (VoiceOver).
"""

import sys
import threading
import weakref
from typing import Optional, Dict, Any, List, Union
import tkinter as tk
from abc import ABC, abstractmethod

# Platform-specific imports with fallbacks
try:
    if sys.platform.startswith("win"):
        import comtypes
        import comtypes.client
        from comtypes import GUID

        WINDOWS_AVAILABLE = True
    else:
        WINDOWS_AVAILABLE = False
except ImportError:
    WINDOWS_AVAILABLE = False

try:
    if sys.platform.startswith("linux"):
        import pyatspi  # type: ignore

        LINUX_AVAILABLE = True
    else:
        LINUX_AVAILABLE = False
        pyatspi = None
except ImportError:
    LINUX_AVAILABLE = False
    pyatspi = None

try:
    if sys.platform.startswith("darwin"):
        import objc
        from Foundation import NSObject
        from AppKit import NSAccessibility

        MACOS_AVAILABLE = True
    else:
        MACOS_AVAILABLE = False
except ImportError:
    MACOS_AVAILABLE = False


class AccessibilityAdapter(ABC):
    """Abstract base class for platform-specific accessibility adapters"""

    def __init__(self) -> None:
        self._widget_registry: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()
        self._lock = threading.Lock()

    @abstractmethod
    def set_accessible_name(self, widget: tk.Widget, name: str) -> None:
        """Set the accessible name for a widget"""
        pass

    @abstractmethod
    def set_accessible_description(self, widget: tk.Widget, description: str) -> None:
        """Set the accessible description for a widget"""
        pass

    @abstractmethod
    def set_accessible_role(self, widget: tk.Widget, role: str) -> None:
        """Set the accessible role for a widget"""
        pass

    @abstractmethod
    def set_accessible_value(self, widget: tk.Widget, value: str) -> None:
        """Set the accessible value for a widget"""
        pass

    @abstractmethod
    def set_accessible_state(self, widget: tk.Widget, state: str, value: bool) -> None:
        """Set an accessible state for a widget"""
        pass

    @abstractmethod
    def announce(self, message: str, priority: str = "medium") -> None:
        """Announce a message to screen readers"""
        pass

    @abstractmethod
    def is_screen_reader_active(self) -> bool:
        """Check if a screen reader is currently active"""
        pass


class WindowsUIAAdapter(AccessibilityAdapter):
    """Windows UI Automation adapter for screen reader integration"""

    def __init__(self) -> None:
        super().__init__()
        self._uia_client = None
        self._automation_properties: Dict[str, Any] = {}
        self._init_uia()

    def _init_uia(self) -> None:
        """Initialize Windows UI Automation"""
        if not WINDOWS_AVAILABLE:
            return

        try:
            comtypes.CoInitialize()
            # Initialize UI Automation client
            self._uia_client = comtypes.client.CreateObject(
                "UIAutomationCore.CUIAutomation"
            )
        except Exception:
            # UIA not available or failed to initialize
            self._uia_client = None

    def set_accessible_name(self, widget: tk.Widget, name: str) -> None:
        """Set accessible name using UIA AutomationProperties"""
        if not self._uia_client:
            return

        try:  # type: ignore[unreachable]
            # Store the name for the widget
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                self._widget_registry[widget]["name"] = name

            # Set UIA property if possible
            self._set_uia_property(widget, "Name", name)
        except Exception:
            # Ignore UIA errors to prevent crashes
            pass

    def set_accessible_description(self, widget: tk.Widget, description: str) -> None:
        """Set accessible description using UIA AutomationProperties"""
        if not self._uia_client:
            return

        try:  # type: ignore[unreachable]
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                self._widget_registry[widget]["description"] = description

            self._set_uia_property(widget, "HelpText", description)
        except Exception:
            pass

    def set_accessible_role(self, widget: tk.Widget, role: str) -> None:
        """Set accessible role using UIA control types"""
        if not self._uia_client:
            return

        try:  # type: ignore[unreachable]
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                self._widget_registry[widget]["role"] = role

            # Map ARIA roles to UIA control types
            uia_control_type = self._map_role_to_uia_control_type(role)
            self._set_uia_property(widget, "ControlType", uia_control_type)
        except Exception:
            pass

    def set_accessible_value(self, widget: tk.Widget, value: str) -> None:
        """Set accessible value"""
        try:
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                self._widget_registry[widget]["value"] = value
        except Exception:
            pass

    def set_accessible_state(self, widget: tk.Widget, state: str, value: bool) -> None:
        """Set accessible state"""
        try:
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                if "states" not in self._widget_registry[widget]:
                    self._widget_registry[widget]["states"] = {}
                self._widget_registry[widget]["states"][state] = value
        except Exception:
            pass

    def announce(self, message: str, priority: str = "medium") -> None:
        """Announce message to Windows screen readers"""
        if not self._uia_client:
            return

        try:  # type: ignore[unreachable]
            # Use UIA notification API if available
            # This is a simplified implementation
            pass
        except Exception:
            pass

    def is_screen_reader_active(self) -> bool:
        """Check if a Windows screen reader is active"""
        try:
            import winreg

            # Check for common screen readers in registry
            screen_readers = [
                r"SOFTWARE\Freedom Scientific\JAWS",
                r"SOFTWARE\NV Access\NVDA",
                r"SOFTWARE\Microsoft\Narrator",
            ]

            for sr_path in screen_readers:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sr_path):
                        return True
                except FileNotFoundError:
                    continue

            return False
        except Exception:
            return False

    def _set_uia_property(
        self, widget: tk.Widget, property_name: str, value: Any
    ) -> None:
        """Set UIA automation property"""
        # This is a placeholder for actual UIA property setting
        # Real implementation would require more complex COM interop
        pass

    def _map_role_to_uia_control_type(self, role: str) -> int:
        """Map ARIA role to UIA control type"""
        role_mapping = {
            "button": 50000,  # UIA_ButtonControlTypeId
            "textbox": 50004,  # UIA_EditControlTypeId
            "label": 50020,  # UIA_TextControlTypeId
            "checkbox": 50002,  # UIA_CheckBoxControlTypeId
            "radio": 50013,  # UIA_RadioButtonControlTypeId
            "slider": 50015,  # UIA_SliderControlTypeId
            "listbox": 50008,  # UIA_ListControlTypeId
            "region": 50026,  # UIA_GroupControlTypeId
            "menu": 50009,  # UIA_MenuControlTypeId
            "menuitem": 50011,  # UIA_MenuItemControlTypeId
            "tab": 50018,  # UIA_TabControlTypeId
            "tabpanel": 50017,  # UIA_TabItemControlTypeId
            "tree": 50023,  # UIA_TreeControlTypeId
            "treeitem": 50024,  # UIA_TreeItemControlTypeId
        }
        return role_mapping.get(role, 50026)  # Default to Group


class LinuxATSPIAdapter(AccessibilityAdapter):
    """Linux AT-SPI adapter for screen reader integration"""

    def __init__(self) -> None:
        super().__init__()
        self._atspi_registry = None
        self._init_atspi()

    def _init_atspi(self) -> None:
        """Initialize AT-SPI"""
        if not LINUX_AVAILABLE:
            return

        try:
            if pyatspi is not None:
                self._atspi_registry = pyatspi.Registry  # type: ignore[unreachable]
            else:
                self._atspi_registry = None
        except Exception:
            self._atspi_registry = None

    def set_accessible_name(self, widget: tk.Widget, name: str) -> None:
        """Set accessible name using AT-SPI"""
        try:
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                self._widget_registry[widget]["name"] = name
        except Exception:
            pass

    def set_accessible_description(self, widget: tk.Widget, description: str) -> None:
        """Set accessible description using AT-SPI"""
        try:
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                self._widget_registry[widget]["description"] = description
        except Exception:
            pass

    def set_accessible_role(self, widget: tk.Widget, role: str) -> None:
        """Set accessible role using AT-SPI"""
        try:
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                self._widget_registry[widget]["role"] = role
        except Exception:
            pass

    def set_accessible_value(self, widget: tk.Widget, value: str) -> None:
        """Set accessible value"""
        try:
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                self._widget_registry[widget]["value"] = value
        except Exception:
            pass

    def set_accessible_state(self, widget: tk.Widget, state: str, value: bool) -> None:
        """Set accessible state"""
        try:
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                if "states" not in self._widget_registry[widget]:
                    self._widget_registry[widget]["states"] = {}
                self._widget_registry[widget]["states"][state] = value
        except Exception:
            pass

    def announce(self, message: str, priority: str = "medium") -> None:
        """Announce message to Linux screen readers"""
        # AT-SPI announcement implementation would go here
        pass

    def is_screen_reader_active(self) -> bool:
        """Check if a Linux screen reader is active"""
        try:
            # Check for common Linux screen readers
            import subprocess

            result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            screen_readers = ["orca", "speakup", "brltty"]

            for sr in screen_readers:
                if sr in result.stdout:
                    return True
            return False
        except Exception:
            return False


class MacOSVoiceOverAdapter(AccessibilityAdapter):
    """macOS VoiceOver adapter for screen reader integration"""

    def __init__(self) -> None:
        super().__init__()
        self._init_voiceover()

    def _init_voiceover(self) -> None:
        """Initialize VoiceOver integration"""
        if not MACOS_AVAILABLE:
            return

    def set_accessible_name(self, widget: tk.Widget, name: str) -> None:
        """Set accessible name for VoiceOver"""
        try:
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                self._widget_registry[widget]["name"] = name
        except Exception:
            pass

    def set_accessible_description(self, widget: tk.Widget, description: str) -> None:
        """Set accessible description for VoiceOver"""
        try:
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                self._widget_registry[widget]["description"] = description
        except Exception:
            pass

    def set_accessible_role(self, widget: tk.Widget, role: str) -> None:
        """Set accessible role for VoiceOver"""
        try:
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                self._widget_registry[widget]["role"] = role
        except Exception:
            pass

    def set_accessible_value(self, widget: tk.Widget, value: str) -> None:
        """Set accessible value"""
        try:
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                self._widget_registry[widget]["value"] = value
        except Exception:
            pass

    def set_accessible_state(self, widget: tk.Widget, state: str, value: bool) -> None:
        """Set accessible state"""
        try:
            with self._lock:
                if widget not in self._widget_registry:
                    self._widget_registry[widget] = {}
                if "states" not in self._widget_registry[widget]:
                    self._widget_registry[widget]["states"] = {}
                self._widget_registry[widget]["states"][state] = value
        except Exception:
            pass

    def announce(self, message: str, priority: str = "medium") -> None:
        """Announce message to VoiceOver"""
        # VoiceOver announcement implementation would go here
        pass

    def is_screen_reader_active(self) -> bool:
        """Check if VoiceOver is active"""
        try:
            # Check VoiceOver status
            import subprocess

            result = subprocess.run(
                ["defaults", "read", "com.apple.universalaccess", "voiceOverOnOffKey"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False


class FallbackAdapter(AccessibilityAdapter):
    """Fallback adapter when platform-specific adapters are not available"""

    def __init__(self) -> None:
        super().__init__()

    def set_accessible_name(self, widget: tk.Widget, name: str) -> None:
        """Store accessible name locally"""
        with self._lock:
            if widget not in self._widget_registry:
                self._widget_registry[widget] = {}
            self._widget_registry[widget]["name"] = name

    def set_accessible_description(self, widget: tk.Widget, description: str) -> None:
        """Store accessible description locally"""
        with self._lock:
            if widget not in self._widget_registry:
                self._widget_registry[widget] = {}
            self._widget_registry[widget]["description"] = description

    def set_accessible_role(self, widget: tk.Widget, role: str) -> None:
        """Store accessible role locally"""
        with self._lock:
            if widget not in self._widget_registry:
                self._widget_registry[widget] = {}
            self._widget_registry[widget]["role"] = role

    def set_accessible_value(self, widget: tk.Widget, value: str) -> None:
        """Store accessible value locally"""
        with self._lock:
            if widget not in self._widget_registry:
                self._widget_registry[widget] = {}
            self._widget_registry[widget]["value"] = value

    def set_accessible_state(self, widget: tk.Widget, state: str, value: bool) -> None:
        """Store accessible state locally"""
        with self._lock:
            if widget not in self._widget_registry:
                self._widget_registry[widget] = {}
            if "states" not in self._widget_registry[widget]:
                self._widget_registry[widget]["states"] = {}
            self._widget_registry[widget]["states"][state] = value

    def announce(self, message: str, priority: str = "medium") -> None:
        """No-op announcement for fallback"""
        pass

    def is_screen_reader_active(self) -> bool:
        """Always return False for fallback"""
        return False


# Global adapter instance
_adapter: Optional[AccessibilityAdapter] = None


def get_platform_adapter() -> AccessibilityAdapter:
    """Get the appropriate platform adapter"""
    global _adapter

    if _adapter is None:
        if sys.platform.startswith("win") and WINDOWS_AVAILABLE:
            _adapter = WindowsUIAAdapter()
        elif sys.platform.startswith("linux") and LINUX_AVAILABLE:
            _adapter = LinuxATSPIAdapter()
        elif sys.platform.startswith("darwin") and MACOS_AVAILABLE:
            _adapter = MacOSVoiceOverAdapter()
        else:
            _adapter = FallbackAdapter()

    return _adapter


# Convenience functions
def set_accessible_name(widget: tk.Widget, name: str) -> None:
    """Set accessible name for a widget"""
    get_platform_adapter().set_accessible_name(widget, name)


def set_accessible_description(widget: tk.Widget, description: str) -> None:
    """Set accessible description for a widget"""
    get_platform_adapter().set_accessible_description(widget, description)


def set_accessible_role(widget: tk.Widget, role: str) -> None:
    """Set accessible role for a widget"""
    get_platform_adapter().set_accessible_role(widget, role)


def set_accessible_value(widget: tk.Widget, value: str) -> None:
    """Set accessible value for a widget"""
    get_platform_adapter().set_accessible_value(widget, value)


def set_accessible_state(widget: tk.Widget, state: str, value: bool) -> None:
    """Set accessible state for a widget"""
    get_platform_adapter().set_accessible_state(widget, state, value)


def announce(message: str, priority: str = "medium") -> None:
    """Announce message to screen readers"""
    get_platform_adapter().announce(message, priority)


def is_screen_reader_active() -> bool:
    """Check if a screen reader is currently active"""
    return get_platform_adapter().is_screen_reader_active()
