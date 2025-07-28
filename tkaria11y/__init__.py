# tkaria11y/__init__.py
from typing import TYPE_CHECKING

__version__ = "0.1.1"

"""
tkaria11y - Comprehensive Accessibility Framework for Tkinter
Provides full WCAG 2.1 compliance with ARIA support, platform integration,
and comprehensive accessibility features for all GUI elements.
"""

# Core accessibility engine
from .a11y_engine import tts, speak, shutdown_tts

# Application framework
from .app import AccessibleApp

# Focus management
from .utils import configure_focus_traversal
from .focus_manager import (
    get_focus_manager,
    configure_advanced_focus_traversal,
    FocusManager,
)

# Theming and visual accessibility
from .themes import (
    HighContrastTheme,
    set_dyslexic_font,
    set_readable_font,
    set_large_text,
    set_extra_large_text,
    increase_font_size,
    decrease_font_size,
    set_font_scale,
    apply_colorblind_safe_theme,
    get_font_manager,
    AccessibilityFontManager,
    ColorBlindnessSupport,
)

# Platform integration
from .platform_adapter import (
    get_platform_adapter,
    set_accessible_name,
    set_accessible_description,
    set_accessible_role,
    set_accessible_value,
    set_accessible_state,
    announce,
    is_screen_reader_active,
)

# ARIA compliance
from .aria_compliance import (
    ARIARole,
    ARIAProperty,
    get_default_role,
    validate_aria_compliance,
    calculate_contrast_ratio,
    validate_contrast_ratio,
    validate_keyboard_navigation,
)

# Enhanced mixins
from .mixins import (
    AccessibleMixin,
    BrailleMixin,
    HighContrastMixin,
    ComprehensiveAccessibilityMixin,
)

# Accessibility validation and testing
from .accessibility_validator import (
    AccessibilityValidator,
    AccessibilityTester,
    ValidationLevel,
    ValidationCategory,
    IssueSeverity,
    validate_accessibility,
    auto_fix_accessibility_issues,
    run_accessibility_audit,
    test_keyboard_navigation,
    test_screen_reader_compatibility,
)

# Braille display support
from .braille_support import (
    get_braille_manager,
    setup_braille_support,
    display_braille_text,
    display_widget_on_braille,
    is_braille_display_available,
    get_braille_display_info,
    shutdown_braille_support,
    BrailleDisplayType,
    BrailleCell,
    BrailleManager,
)

# Audio accessibility
from .audio_accessibility import (
    get_audio_manager,
    setup_audio_accessibility,
    play_audio_cue,
    play_success_sound,
    play_error_sound,
    play_warning_sound,
    play_notification_sound,
    set_audio_volume,
    set_audio_enabled,
    set_spatial_audio_enabled,
    is_audio_available,
    get_audio_info,
    shutdown_audio_accessibility,
    AudioCueType,
    AudioCue,
    AudioAccessibilityManager,
)

# Widget enhancements
from .widgets import (
    validate_widget_accessibility,
    enhance_widget_accessibility,
    create_accessible_widget,
    discover_widgets,
    enhance_existing_widgets,
)

# Import widgets module to get __all__
from . import widgets

if TYPE_CHECKING:
    # For type checking, import from stubs
    from .stubs.widgets import (
        AccessibleButton,
        AccessibleEntry,
        AccessibleLabel,
        AccessibleCheckbutton,
        AccessibleRadiobutton,
        AccessibleScale,
        AccessibleListbox,
        AccessibleFrame,
        AccessibleTTKButton,
        AccessibleTTKEntry,
        AccessibleTTKLabel,
        AccessibleTTKCheckbutton,
        AccessibleTTKRadiobutton,
        AccessibleTTKScale,
        AccessibleTTKScrollbar,
        AccessibleTTKFrame,
        AccessibleTTKLabelFrame,
        AccessibleTTKNotebook,
        AccessibleTTKProgressbar,
        AccessibleTTKSeparator,
        AccessibleTTKTreeview,
        AccessibleTTKCombobox,
        AccessibleTTKSpinbox,
        AccessibleNotebook,
        AccessibleTreeview,
        AccessibleCombobox,
    )
else:
    # For runtime, use star import to get dynamically created classes
    from .widgets import *

# Complete public API
__all__ = [
    # Core functionality
    "tts",
    "speak",
    "shutdown_tts",
    "AccessibleApp",
    # Focus management
    "configure_focus_traversal",
    "get_focus_manager",
    "configure_advanced_focus_traversal",
    "FocusManager",
    # Theming and fonts
    "HighContrastTheme",
    "set_dyslexic_font",
    "set_readable_font",
    "set_large_text",
    "set_extra_large_text",
    "increase_font_size",
    "decrease_font_size",
    "set_font_scale",
    "apply_colorblind_safe_theme",
    "get_font_manager",
    "AccessibilityFontManager",
    "ColorBlindnessSupport",
    # Platform integration
    "get_platform_adapter",
    "set_accessible_name",
    "set_accessible_description",
    "set_accessible_role",
    "set_accessible_value",
    "set_accessible_state",
    "announce",
    "is_screen_reader_active",
    # ARIA compliance
    "ARIARole",
    "ARIAProperty",
    "get_default_role",
    "validate_aria_compliance",
    "calculate_contrast_ratio",
    "validate_contrast_ratio",
    "validate_keyboard_navigation",
    # Mixins
    "AccessibleMixin",
    "BrailleMixin",
    "HighContrastMixin",
    "ComprehensiveAccessibilityMixin",
    # Validation and testing
    "AccessibilityValidator",
    "AccessibilityTester",
    "ValidationLevel",
    "ValidationCategory",
    "IssueSeverity",
    "validate_accessibility",
    "auto_fix_accessibility_issues",
    "run_accessibility_audit",
    "test_keyboard_navigation",
    "test_screen_reader_compatibility",
    # Braille display support
    "get_braille_manager",
    "setup_braille_support",
    "display_braille_text",
    "display_widget_on_braille",
    "is_braille_display_available",
    "get_braille_display_info",
    "shutdown_braille_support",
    "BrailleDisplayType",
    "BrailleCell",
    "BrailleManager",
    # Audio accessibility
    "get_audio_manager",
    "setup_audio_accessibility",
    "play_audio_cue",
    "play_success_sound",
    "play_error_sound",
    "play_warning_sound",
    "play_notification_sound",
    "set_audio_volume",
    "set_audio_enabled",
    "set_spatial_audio_enabled",
    "is_audio_available",
    "get_audio_info",
    "shutdown_audio_accessibility",
    "AudioCueType",
    "AudioCue",
    "AudioAccessibilityManager",
    # Widget utilities
    "validate_widget_accessibility",
    "enhance_widget_accessibility",
    "create_accessible_widget",
    "discover_widgets",
    "enhance_existing_widgets",
] + widgets.__all__


# Convenience functions for quick setup
def setup_full_accessibility(
    root,
    high_contrast=False,
    dyslexic_font=False,
    large_text=False,
    auto_fix=True,
    enable_audio=True,
    enable_braille=True,
    enable_spatial_audio=False,
):
    """
    Quick setup for full accessibility features.

    Args:
        root: Tkinter root window
        high_contrast: Apply high contrast theme
        dyslexic_font: Apply dyslexic-friendly font
        large_text: Apply large text sizes
        auto_fix: Automatically fix common accessibility issues
        enable_audio: Enable audio accessibility cues
        enable_braille: Enable braille display support
        enable_spatial_audio: Enable spatial audio positioning
    """
    # Set up advanced focus management
    configure_advanced_focus_traversal(root)

    # Apply visual accessibility features
    if high_contrast:
        HighContrastTheme.apply(root)

    if dyslexic_font:
        set_dyslexic_font(root)
    elif large_text:
        set_large_text(root)

    # Set up audio accessibility
    if enable_audio:
        setup_audio_accessibility(root, enable_spatial=enable_spatial_audio)

    # Set up braille support
    if enable_braille:
        setup_braille_support(root)

    # Auto-fix accessibility issues
    if auto_fix:
        auto_fix_accessibility_issues(root)

    # Enhance existing widgets
    enhance_existing_widgets(root)


def quick_accessibility_audit(root):
    """
    Run a quick accessibility audit and return summary.

    Args:
        root: Tkinter root window

    Returns:
        Dict with audit results and recommendations
    """
    report = run_accessibility_audit(root)

    # Create simplified summary
    summary = {
        "compliance_score": report["compliance_score"],
        "total_issues": report["total_issues"],
        "critical_issues": len(report["issues_by_severity"].get("critical", [])),
        "high_issues": len(report["issues_by_severity"].get("high", [])),
        "recommendations": [],
        "auto_fixable_count": sum(
            1 for issue in report["all_issues"] if issue["auto_fixable"]
        ),
    }

    # Add top recommendations
    if summary["critical_issues"] > 0:
        summary["recommendations"].append(
            "Fix critical accessibility issues immediately"
        )
    if summary["high_issues"] > 0:
        summary["recommendations"].append("Address high priority accessibility issues")
    if summary["auto_fixable_count"] > 0:
        summary["recommendations"].append(
            f"Run auto_fix_accessibility_issues() to fix {summary['auto_fixable_count']} issues automatically"
        )

    return summary


# Add convenience functions to __all__
__all__.extend(["setup_full_accessibility", "quick_accessibility_audit"])

# Module-level documentation
"""
tkaria11y provides comprehensive accessibility support for Tkinter applications.

Key Features:
- Full WCAG 2.1 compliance (A, AA, AAA levels)
- Complete ARIA role and property support
- Platform-specific screen reader integration (Windows UIA, Linux AT-SPI, macOS VoiceOver)
- Advanced focus management and keyboard navigation
- High contrast themes and dyslexic-friendly fonts
- Automated accessibility testing and validation
- Support for all Tkinter, TTK, and CustomTkinter widgets
- Braille display integration
- Color blindness support
- Text-to-speech with priority and debouncing
- Comprehensive accessibility auditing tools

Quick Start:
    import tkinter as tk
    from tkaria11y import AccessibleApp, AccessibleButton, setup_full_accessibility
    
    root = AccessibleApp()
    setup_full_accessibility(root, high_contrast=True, dyslexic_font=True)
    
    button = AccessibleButton(root, 
                             text="Click me",
                             accessible_name="Main action button",
                             accessible_description="Performs the primary action")
    button.pack()
    
    root.mainloop()

For comprehensive documentation, see: https://github.com/your-repo/tkaria11y
"""
