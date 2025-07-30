# tkaria11y/accessibility_validator.py

"""
Comprehensive accessibility validation and testing module.
Provides automated testing for WCAG 2.1 compliance, ARIA validation,
keyboard navigation, and screen reader compatibility.
"""

import tkinter as tk
from typing import List, Dict, Any, Optional, Set
import time
from dataclasses import dataclass
from enum import Enum
from .aria_compliance import (
    ARIARole,
    calculate_contrast_ratio,
    validate_keyboard_navigation,
)
from .platform_adapter import is_screen_reader_active


class ValidationLevel(Enum):
    """WCAG compliance levels"""

    A = "A"
    AA = "AA"
    AAA = "AAA"


class ValidationCategory(Enum):
    """Categories of accessibility validation"""

    PERCEIVABLE = "perceivable"
    OPERABLE = "operable"
    UNDERSTANDABLE = "understandable"
    ROBUST = "robust"


class IssueSeverity(Enum):
    """Severity levels for accessibility issues"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class AccessibilityIssue:
    """Represents an accessibility issue"""

    severity: IssueSeverity
    category: ValidationCategory
    title: str
    description: str
    widget: Optional[tk.Misc] = None
    widget_class: str = ""
    widget_path: str = ""
    recommendation: str = ""
    wcag_criterion: str = ""
    auto_fixable: bool = False


class AccessibilityValidator:
    """Comprehensive accessibility validator"""

    def __init__(self, compliance_level: ValidationLevel = ValidationLevel.AA):
        self.compliance_level = compliance_level
        self.issues: List[AccessibilityIssue] = []
        self.validated_widgets: Set[tk.Misc] = set()

    def validate_application(self, root: tk.Tk) -> List[AccessibilityIssue]:
        """Validate entire application for accessibility compliance"""
        self.issues.clear()
        self.validated_widgets.clear()

        # Validate all four WCAG principles
        self._validate_perceivable(root)
        self._validate_operable(root)
        self._validate_understandable(root)
        self._validate_robust(root)

        # Additional comprehensive validations
        self._validate_widget_hierarchy(root)
        self._validate_error_handling(root)
        self._validate_responsive_design(root)
        self._validate_internationalization(root)

        return self.issues.copy()

    def _validate_perceivable(self, root: tk.Tk) -> None:
        """Validate Perceivable principle (WCAG 1.x)"""
        self._validate_text_alternatives(root)
        self._validate_color_contrast(root)
        self._validate_text_sizing(root)
        self._validate_audio_content(root)
        self._validate_color_usage(root)

    def _validate_operable(self, root: tk.Tk) -> None:
        """Validate Operable principle (WCAG 2.x)"""
        self._validate_keyboard_accessibility(root)
        self._validate_focus_management(root)
        self._validate_timing_requirements(root)
        self._validate_seizure_safety(root)
        self._validate_form_structure(root)

    def _validate_understandable(self, root: tk.Tk) -> None:
        """Validate Understandable principle (WCAG 3.x)"""
        self._validate_readable_content(root)
        self._validate_predictable_functionality(root)
        self._validate_input_assistance(root)

    def _validate_robust(self, root: tk.Tk) -> None:
        """Validate Robust principle (WCAG 4.x)"""
        self._validate_markup_compatibility(root)
        self._validate_assistive_technology_support(root)
        self._validate_future_compatibility(root)

    # Perceivable validations
    def _validate_text_alternatives(self, root: tk.Tk) -> None:
        """Validate text alternatives for non-text content (WCAG 1.1.1)"""

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            if widget in self.validated_widgets:
                return
            self.validated_widgets.add(widget)

            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check for widgets that need text alternatives
            needs_alt_text = widget_class in [
                "Button",
                "Canvas",
                "Label",
                "Checkbutton",
                "Radiobutton",
            ]

            if needs_alt_text:
                has_accessible_name = (
                    hasattr(widget, "accessible_name") and widget.accessible_name
                )
                has_text = False

                try:
                    text = widget.cget("text")
                    has_text = bool(text and text.strip())
                except tk.TclError:
                    pass

                if not has_accessible_name and not has_text:
                    if widget_class == "Button":
                        severity = IssueSeverity.CRITICAL
                    elif widget_class in ["Checkbutton", "Radiobutton"]:
                        severity = IssueSeverity.HIGH
                    else:
                        severity = IssueSeverity.MEDIUM

                    self.issues.append(
                        AccessibilityIssue(
                            severity=severity,
                            category=ValidationCategory.PERCEIVABLE,
                            title="Missing text alternative",
                            description=f"{widget_class} widget lacks accessible name "
                            f"or text",
                            widget=widget,
                            widget_class=widget_class,
                            widget_path=current_path,
                            recommendation="Add accessible_name parameter or text "
                            "attribute",
                            wcag_criterion="1.1.1 Non-text Content",
                            auto_fixable=False,
                        )
                    )

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_color_contrast(self, root: tk.Tk) -> None:
        """Validate color contrast ratios (WCAG 1.4.3, 1.4.6)"""

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            if widget in self.validated_widgets:
                return

            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            try:
                fg_color = widget.cget("fg") or widget.cget("foreground")
                bg_color = widget.cget("bg") or widget.cget("background")

                if fg_color and bg_color:
                    contrast_ratio = calculate_contrast_ratio(fg_color, bg_color)

                    # Determine required ratio based on compliance level
                    if self.compliance_level == ValidationLevel.AAA:
                        required_ratio = 7.0
                        criterion = "1.4.6 Contrast (Enhanced)"
                    else:
                        required_ratio = 4.5
                        criterion = "1.4.3 Contrast (Minimum)"

                    if contrast_ratio < required_ratio:
                        severity = (
                            IssueSeverity.HIGH
                            if contrast_ratio < 3.0
                            else IssueSeverity.MEDIUM
                        )

                        self.issues.append(
                            AccessibilityIssue(
                                severity=severity,
                                category=ValidationCategory.PERCEIVABLE,
                                title="Insufficient color contrast",
                                description=f"Contrast ratio {contrast_ratio:.2f} is "
                                f"below required {required_ratio}",
                                widget=widget,
                                widget_class=widget_class,
                                widget_path=current_path,
                                recommendation=f"Adjust colors to achieve "
                                f"{required_ratio}:1 contrast ratio",
                                wcag_criterion=criterion,
                                auto_fixable=True,
                            )
                        )

            except (tk.TclError, AttributeError):
                pass

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_text_sizing(self, root: tk.Tk) -> None:
        """Validate text can be resized (WCAG 1.4.4)"""

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            try:
                font = widget.cget("font")
                if font:
                    if isinstance(font, tuple) and len(font) >= 2:
                        size = font[1]
                        if isinstance(size, int) and size < 12:
                            self.issues.append(
                                AccessibilityIssue(
                                    severity=IssueSeverity.MEDIUM,
                                    category=ValidationCategory.PERCEIVABLE,
                                    title="Font size too small",
                                    description=f"Font size {size}pt is below "
                                    f"recommended minimum of 12pt",
                                    widget=widget,
                                    widget_class=widget_class,
                                    widget_path=current_path,
                                    recommendation="Use font size of at least 12pt",
                                    wcag_criterion="1.4.4 Resize text",
                                    auto_fixable=True,
                                )
                            )
            except (tk.TclError, AttributeError):
                pass

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_audio_content(self, root: tk.Tk) -> None:
        """Validate audio content accessibility (WCAG 1.2.x)"""

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check for audio-related widgets or attributes
            if hasattr(widget, "audio_manager") or hasattr(widget, "tts_enabled"):
                # Check if audio has text alternatives
                if not (
                    hasattr(widget, "accessible_description")
                    and widget.accessible_description
                ):
                    self.issues.append(
                        AccessibilityIssue(
                            severity=IssueSeverity.HIGH,
                            category=ValidationCategory.PERCEIVABLE,
                            title="Audio content lacks text alternative",
                            description=f"{widget_class} with audio lacks description",
                            widget=widget,
                            widget_class=widget_class,
                            widget_path=current_path,
                            recommendation="Provide text description for audio "
                            "content",
                            wcag_criterion="1.2.1 Audio-only and Video-only",
                            auto_fixable=False,
                        )
                    )

            # Check for Canvas widgets that might contain multimedia
            if widget_class == "Canvas":
                self.issues.append(
                    AccessibilityIssue(
                        severity=IssueSeverity.INFO,
                        category=ValidationCategory.PERCEIVABLE,
                        title="Canvas may contain multimedia content",
                        description="Canvas widgets should be checked for audio/video",
                        widget=widget,
                        widget_class=widget_class,
                        widget_path=current_path,
                        recommendation="Ensure any multimedia has text alternatives",
                        wcag_criterion="1.2.1 Audio-only and Video-only",
                        auto_fixable=False,
                    )
                )

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_color_usage(self, root: tk.Tk) -> None:
        """Validate that color is not the only means of conveying information"""

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check for widgets that might rely solely on color
            if widget_class in ["Button", "Label"]:
                try:
                    bg_color = widget.cget("bg") or widget.cget("background")
                    text = widget.cget("text")

                    # Check for color-coded buttons without text
                    if bg_color and bg_color.lower() in [
                        "red",
                        "#ff0000",
                        "#f00",
                        "green",
                        "#00ff00",
                        "#0f0",
                        "yellow",
                        "#ffff00",
                        "#ff0",
                        "blue",
                        "#0000ff",
                        "#00f",
                    ]:
                        if not text or len(text.strip()) < 2:
                            self.issues.append(
                                AccessibilityIssue(
                                    severity=IssueSeverity.HIGH,
                                    category=ValidationCategory.PERCEIVABLE,
                                    title="Color used as only means of information",
                                    description=f"{widget_class} relies on color "
                                    f"without text alternative",
                                    widget=widget,
                                    widget_class=widget_class,
                                    widget_path=current_path,
                                    recommendation="Add text labels or icons to "
                                    "supplement color coding",
                                    wcag_criterion="1.4.1 Use of Color",
                                    auto_fixable=False,
                                )
                            )
                except tk.TclError:
                    pass

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    # Operable validations
    def _validate_keyboard_accessibility(self, root: tk.Tk) -> None:
        """Validate keyboard accessibility (WCAG 2.1.1, 2.1.2)"""

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check if interactive widget can receive focus
            interactive_widgets = [
                "Button",
                "Entry",
                "Text",
                "Checkbutton",
                "Radiobutton",
                "Scale",
                "Listbox",
                "Scrollbar",
                "Spinbox",
            ]

            if widget_class in interactive_widgets:
                try:
                    takefocus = widget.cget("takefocus")
                    if takefocus == 0:
                        self.issues.append(
                            AccessibilityIssue(
                                severity=IssueSeverity.HIGH,
                                category=ValidationCategory.OPERABLE,
                                title="Interactive widget not keyboard accessible",
                                description=f"{widget_class} cannot receive "
                                f"keyboard focus",
                                widget=widget,
                                widget_class=widget_class,
                                widget_path=current_path,
                                recommendation="Set takefocus=True or remove "
                                "takefocus=0",
                                wcag_criterion="2.1.1 Keyboard",
                                auto_fixable=True,
                            )
                        )
                except tk.TclError:
                    pass

                # Validate keyboard navigation
                nav_errors = validate_keyboard_navigation(widget)
                for error in nav_errors:
                    self.issues.append(
                        AccessibilityIssue(
                            severity=IssueSeverity.MEDIUM,
                            category=ValidationCategory.OPERABLE,
                            title="Keyboard navigation issue",
                            description=error,
                            widget=widget,
                            widget_class=widget_class,
                            widget_path=current_path,
                            recommendation="Add appropriate keyboard event bindings",
                            wcag_criterion="2.1.1 Keyboard",
                            auto_fixable=False,
                        )
                    )

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_focus_management(self, root: tk.Tk) -> None:
        """Validate focus management (WCAG 2.4.3, 2.4.7)"""
        # Check for focus traps and logical focus order
        focusable_widgets = []

        def collect_focusable(widget: tk.Misc) -> None:
            try:
                takefocus = widget.cget("takefocus")
                if takefocus != 0:
                    focusable_widgets.append(widget)
            except tk.TclError:
                pass

            try:
                for child in widget.winfo_children():
                    collect_focusable(child)
            except tk.TclError:
                pass

        collect_focusable(root)

        # Check if focus order is logical (simplified check)
        if len(focusable_widgets) > 1:
            # Check if widgets have logical tab order
            for i, widget in enumerate(focusable_widgets[:-1]):
                next_widget = focusable_widgets[i + 1]

                try:
                    widget_y = widget.winfo_y()
                    next_y = next_widget.winfo_y()

                    # If next widget is significantly above current widget,
                    # focus order might be illogical
                    if next_y < widget_y - 50:  # 50 pixel threshold
                        self.issues.append(
                            AccessibilityIssue(
                                severity=IssueSeverity.LOW,
                                category=ValidationCategory.OPERABLE,
                                title="Potentially illogical focus order",
                                description="Focus order may not follow visual layout",
                                widget=widget,
                                widget_class=widget.winfo_class(),
                                widget_path="",
                                recommendation="Review and adjust tab order",
                                wcag_criterion="2.4.3 Focus Order",
                                auto_fixable=False,
                            )
                        )
                        break

                except tk.TclError:
                    pass

    def _validate_timing_requirements(self, root: tk.Tk) -> None:
        """Validate timing requirements (WCAG 2.2.1, 2.2.2)"""

        # Check for widgets with after() calls that might create time limits
        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check if widget has timing-related attributes or methods
            if hasattr(widget, "_after_ids") or hasattr(widget, "after_idle"):
                # This is a basic check - in practice, you'd need to analyze
                # the actual timing behavior
                self.issues.append(
                    AccessibilityIssue(
                        severity=IssueSeverity.INFO,
                        category=ValidationCategory.OPERABLE,
                        title="Widget may have timing constraints",
                        description=f"{widget_class} may implement timing behavior",
                        widget=widget,
                        widget_class=widget_class,
                        widget_path=current_path,
                        recommendation="Ensure timing can be extended or disabled",
                        wcag_criterion="2.2.1 Timing Adjustable",
                        auto_fixable=False,
                    )
                )

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_seizure_safety(self, root: tk.Tk) -> None:
        """Validate seizure and vestibular disorder safety (WCAG 2.3.1)"""

        # Check for potentially problematic visual effects
        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check for Canvas widgets that might contain animations
            if widget_class == "Canvas":
                self.issues.append(
                    AccessibilityIssue(
                        severity=IssueSeverity.INFO,
                        category=ValidationCategory.OPERABLE,
                        title="Canvas may contain flashing content",
                        description="Canvas widgets should be checked for flashing "
                        "or rapidly changing content",
                        widget=widget,
                        widget_class=widget_class,
                        widget_path=current_path,
                        recommendation="Ensure no content flashes more than 3 times "
                        "per second",
                        wcag_criterion="2.3.1 Three Flashes or Below Threshold",
                        auto_fixable=False,
                    )
                )

            # Check for widgets with background color changes
            try:
                bg_color = widget.cget("bg") or widget.cget("background")
                if bg_color and bg_color.lower() in ["red", "#ff0000", "#f00"]:
                    self.issues.append(
                        AccessibilityIssue(
                            severity=IssueSeverity.LOW,
                            category=ValidationCategory.OPERABLE,
                            title="Bright red background may be problematic",
                            description="Bright red backgrounds can be problematic "
                            "for some users",
                            widget=widget,
                            widget_class=widget_class,
                            widget_path=current_path,
                            recommendation="Consider using less intense colors",
                            wcag_criterion="2.3.1 Three Flashes or Below Threshold",
                            auto_fixable=True,
                        )
                    )
            except tk.TclError:
                pass

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_form_structure(self, root: tk.Tk) -> None:
        """Validate form structure and grouping (WCAG 2.4.6, 3.3.2)"""
        form_widgets = []

        def collect_form_widgets(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            if widget_class in [
                "Entry",
                "Text",
                "Spinbox",
                "Checkbutton",
                "Radiobutton",
                "Scale",
                "Listbox",
            ]:
                form_widgets.append((widget, widget_class, current_path))

            # Check children
            try:
                for child in widget.winfo_children():
                    collect_form_widgets(child, current_path)
            except tk.TclError:
                pass

        collect_form_widgets(root)

        # Validate each form widget
        for widget, widget_class, path in form_widgets:
            # Check for proper labeling
            has_label = hasattr(widget, "accessible_name") and widget.accessible_name

            if not has_label:
                # Look for nearby Label widgets
                nearby_label = self._find_nearby_label(widget)
                if not nearby_label:
                    self.issues.append(
                        AccessibilityIssue(
                            severity=IssueSeverity.HIGH,
                            category=ValidationCategory.OPERABLE,
                            title="Form control lacks proper label",
                            description=f"{widget_class} has no associated label",
                            widget=widget,
                            widget_class=widget_class,
                            widget_path=path,
                            recommendation="Add accessible_name or associate "
                            "with Label widget",
                            wcag_criterion="2.4.6 Headings and Labels",
                            auto_fixable=False,
                        )
                    )

            # Check for required field indicators
            if widget_class in ["Entry", "Text", "Spinbox"]:
                # This is a basic check - in practice, you'd check for
                # visual indicators or validation rules
                if not hasattr(widget, "required") or not widget.required:
                    self.issues.append(
                        AccessibilityIssue(
                            severity=IssueSeverity.INFO,
                            category=ValidationCategory.OPERABLE,
                            title="Form field may need required indicator",
                            description=f"{widget_class} should indicate if required",
                            widget=widget,
                            widget_class=widget_class,
                            widget_path=path,
                            recommendation="Add visual and programmatic "
                            "required indicators",
                            wcag_criterion="3.3.2 Labels or Instructions",
                            auto_fixable=False,
                        )
                    )

    def _find_nearby_label(self, widget: tk.Misc) -> bool:
        """Find if there's a Label widget near the given widget"""
        try:
            parent = widget.winfo_parent()
            if parent:
                parent_widget = widget.nametowidget(parent)
                for sibling in parent_widget.winfo_children():
                    if sibling.winfo_class() == "Label":
                        return True
        except tk.TclError:
            pass
        return False

    # Understandable validations
    def _validate_readable_content(self, root: tk.Tk) -> None:
        """Validate readable and understandable content (WCAG 3.1.x)"""

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check for problematic fonts
            try:
                font = widget.cget("font")
                if font and isinstance(font, tuple) and len(font) > 0:
                    font_family = font[0].lower()
                    problematic_fonts = ["times", "serif", "script", "cursive"]

                    if any(prob in font_family for prob in problematic_fonts):
                        self.issues.append(
                            AccessibilityIssue(
                                severity=IssueSeverity.LOW,
                                category=ValidationCategory.UNDERSTANDABLE,
                                title="Potentially difficult to read font",
                                description=f"Font family '{font[0]}' may be "
                                f"difficult to read",
                                widget=widget,
                                widget_class=widget_class,
                                widget_path=current_path,
                                recommendation="Use sans-serif fonts for better "
                                "readability",
                                wcag_criterion="3.1.5 Reading Level",
                                auto_fixable=True,
                            )
                        )
            except (tk.TclError, AttributeError):
                pass

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_predictable_functionality(self, root: tk.Tk) -> None:
        """Validate predictable functionality (WCAG 3.2.x)"""
        # Check for consistent navigation and identification
        button_texts = []
        button_positions = []

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Collect button information for consistency checking
            if widget_class == "Button":
                try:
                    text = widget.cget("text")
                    if text:
                        button_texts.append(text.lower())
                        try:
                            x, y = widget.winfo_x(), widget.winfo_y()
                            button_positions.append((x, y, text))
                        except tk.TclError:
                            pass
                except tk.TclError:
                    pass

            # Check for widgets that change context unexpectedly
            if widget_class in ["Button", "Checkbutton", "Radiobutton"]:
                # Check if widget has focus event bindings that might change context
                try:
                    bindings = widget.bind()
                    if "<FocusIn>" in str(bindings) or "<FocusOut>" in str(bindings):
                        self.issues.append(
                            AccessibilityIssue(
                                severity=IssueSeverity.INFO,
                                category=ValidationCategory.UNDERSTANDABLE,
                                title="Widget has focus event bindings",
                                description=f"{widget_class} has focus bindings that "
                                f"might change context",
                                widget=widget,
                                widget_class=widget_class,
                                widget_path=current_path,
                                recommendation="Ensure focus events don't "
                                "unexpectedly change context",
                                wcag_criterion="3.2.1 On Focus",
                                auto_fixable=False,
                            )
                        )
                except tk.TclError:
                    pass

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

        # Check for duplicate button texts (potential confusion)
        seen_texts = set()
        for text in button_texts:
            if text in seen_texts and text.strip():
                self.issues.append(
                    AccessibilityIssue(
                        severity=IssueSeverity.LOW,
                        category=ValidationCategory.UNDERSTANDABLE,
                        title="Duplicate button text found",
                        description=f"Multiple buttons with text '{text}' found",
                        widget=None,
                        widget_class="Button",
                        widget_path="",
                        recommendation="Use unique, descriptive button text",
                        wcag_criterion="3.2.4 Consistent Identification",
                        auto_fixable=False,
                    )
                )
                break
            seen_texts.add(text)

    def _validate_input_assistance(self, root: tk.Tk) -> None:
        """Validate input assistance (WCAG 3.3.x)"""

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check form inputs for labels and error handling
            if widget_class in ["Entry", "Text", "Spinbox"]:
                has_label = (
                    hasattr(widget, "accessible_name") and widget.accessible_name
                )

                if not has_label:
                    self.issues.append(
                        AccessibilityIssue(
                            severity=IssueSeverity.HIGH,
                            category=ValidationCategory.UNDERSTANDABLE,
                            title="Input field missing label",
                            description=f"{widget_class} lacks accessible label",
                            widget=widget,
                            widget_class=widget_class,
                            widget_path=current_path,
                            recommendation="Add accessible_name or associate "
                            "with label",
                            wcag_criterion="3.3.2 Labels or Instructions",
                            auto_fixable=False,
                        )
                    )

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    # Robust validations
    def _validate_markup_compatibility(self, root: tk.Tk) -> None:
        """Validate markup compatibility (WCAG 4.1.1)"""

        # Check for proper widget hierarchy and structure
        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()

            # Check for proper ARIA roles if widget has accessibility features
            if hasattr(widget, "accessible_role"):
                try:
                    from .aria_compliance import get_default_role

                    expected_role = get_default_role(widget)
                    actual_role = widget.accessible_role

                    if actual_role and actual_role != expected_role.value:
                        # Validate the custom role is appropriate
                        valid_roles = [role.value for role in ARIARole]
                        if actual_role not in valid_roles:
                            self.issues.append(
                                AccessibilityIssue(
                                    severity=IssueSeverity.MEDIUM,
                                    category=ValidationCategory.ROBUST,
                                    title="Invalid ARIA role",
                                    description=f"Role '{actual_role}' is not a "
                                    f"valid ARIA role",
                                    widget=widget,
                                    widget_class=widget_class,
                                    widget_path=path,
                                    recommendation="Use valid ARIA role or remove "
                                    "custom role",
                                    wcag_criterion="4.1.1 Parsing",
                                    auto_fixable=True,
                                )
                            )

                except (AttributeError, ImportError):
                    pass

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(
                        child, f"{path}/{widget_class}" if path else widget_class
                    )
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_assistive_technology_support(self, root: tk.Tk) -> None:
        """Validate assistive technology support (WCAG 4.1.2)"""

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check if widget has proper accessibility properties
            if not hasattr(widget, "accessible_name"):
                interactive_widgets = [
                    "Button",
                    "Entry",
                    "Text",
                    "Checkbutton",
                    "Radiobutton",
                    "Scale",
                    "Listbox",
                    "Scrollbar",
                    "Spinbox",
                ]

                if widget_class in interactive_widgets:
                    self.issues.append(
                        AccessibilityIssue(
                            severity=IssueSeverity.HIGH,
                            category=ValidationCategory.ROBUST,
                            title="Widget lacks accessibility support",
                            description=f"{widget_class} missing AccessibleMixin",
                            widget=widget,
                            widget_class=widget_class,
                            widget_path=current_path,
                            recommendation="Use accessible widget classes or add "
                            "AccessibleMixin",
                            wcag_criterion="4.1.2 Name, Role, Value",
                            auto_fixable=False,
                        )
                    )

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_future_compatibility(self, root: tk.Tk) -> None:
        """Validate future compatibility"""

        # Check for deprecated patterns or potential compatibility issues
        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check for deprecated Tkinter patterns
            deprecated_options = ["bd", "highlightcolor", "selectcolor"]
            for option in deprecated_options:
                try:
                    value = widget.cget(option)
                    if value:
                        self.issues.append(
                            AccessibilityIssue(
                                severity=IssueSeverity.INFO,
                                category=ValidationCategory.ROBUST,
                                title=f"Deprecated option '{option}' used",
                                description=f"Widget uses deprecated option '{option}'",
                                widget=widget,
                                widget_class=widget_class,
                                widget_path=current_path,
                                recommendation=f"Consider using modern alternatives "
                                f"to '{option}'",
                                wcag_criterion="4.1.1 Parsing",
                                auto_fixable=False,
                            )
                        )
                except tk.TclError:
                    pass

            # Check for missing modern accessibility features
            if not hasattr(widget, "accessible_name") and widget_class in [
                "Button",
                "Entry",
                "Text",
                "Checkbutton",
                "Radiobutton",
                "Scale",
                "Listbox",
                "Scrollbar",
                "Spinbox",
            ]:
                self.issues.append(
                    AccessibilityIssue(
                        severity=IssueSeverity.MEDIUM,
                        category=ValidationCategory.ROBUST,
                        title="Widget lacks modern accessibility features",
                        description=f"{widget_class} doesn't use accessibility mixins",
                        widget=widget,
                        widget_class=widget_class,
                        widget_path=current_path,
                        recommendation="Upgrade to accessible widget classes",
                        wcag_criterion="4.1.2 Name, Role, Value",
                        auto_fixable=False,
                    )
                )

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_widget_hierarchy(self, root: tk.Tk) -> None:
        """Validate proper widget hierarchy and structure"""

        def check_widget(widget: tk.Misc, depth: int = 0, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check for excessive nesting depth
            if depth > 10:
                self.issues.append(
                    AccessibilityIssue(
                        severity=IssueSeverity.LOW,
                        category=ValidationCategory.ROBUST,
                        title="Excessive widget nesting",
                        description=f"Widget hierarchy is {depth} levels deep",
                        widget=widget,
                        widget_class=widget_class,
                        widget_path=current_path,
                        recommendation="Consider flattening widget hierarchy",
                        wcag_criterion="4.1.1 Parsing",
                        auto_fixable=False,
                    )
                )

            # Check for proper container usage
            if widget_class == "Frame" and not widget.winfo_children():
                self.issues.append(
                    AccessibilityIssue(
                        severity=IssueSeverity.INFO,
                        category=ValidationCategory.ROBUST,
                        title="Empty container found",
                        description="Frame widget contains no children",
                        widget=widget,
                        widget_class=widget_class,
                        widget_path=current_path,
                        recommendation="Remove empty containers or add content",
                        wcag_criterion="4.1.1 Parsing",
                        auto_fixable=True,
                    )
                )

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, depth + 1, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_error_handling(self, root: tk.Tk) -> None:
        """Validate error handling and user feedback"""

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check Entry widgets for validation
            if widget_class in ["Entry", "Spinbox"]:
                # Check if widget has validation
                try:
                    validate_cmd = widget.cget("validate")
                    if not validate_cmd or validate_cmd == "none":
                        self.issues.append(
                            AccessibilityIssue(
                                severity=IssueSeverity.LOW,
                                category=ValidationCategory.UNDERSTANDABLE,
                                title="Input field lacks validation",
                                description=f"{widget_class} has no input validation",
                                widget=widget,
                                widget_class=widget_class,
                                widget_path=current_path,
                                recommendation="Add input validation and error "
                                "messages",
                                wcag_criterion="3.3.1 Error Identification",
                                auto_fixable=False,
                            )
                        )
                except tk.TclError:
                    pass

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_responsive_design(self, root: tk.Tk) -> None:
        """Validate responsive design aspects"""

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check for fixed sizes that might not scale
            try:
                width = widget.cget("width")
                height = widget.cget("height")

                if isinstance(width, int) and width > 0:
                    if width < 44:  # Minimum touch target size
                        self.issues.append(
                            AccessibilityIssue(
                                severity=IssueSeverity.MEDIUM,
                                category=ValidationCategory.OPERABLE,
                                title="Widget too small for touch interaction",
                                description=f"{widget_class} width {width} is below "
                                f"minimum 44px",
                                widget=widget,
                                widget_class=widget_class,
                                widget_path=current_path,
                                recommendation="Increase widget size to at least "
                                "44x44 pixels",
                                wcag_criterion="2.5.5 Target Size",
                                auto_fixable=True,
                            )
                        )

                if isinstance(height, int) and height > 0:
                    if height < 44:  # Minimum touch target size
                        self.issues.append(
                            AccessibilityIssue(
                                severity=IssueSeverity.MEDIUM,
                                category=ValidationCategory.OPERABLE,
                                title="Widget too small for touch interaction",
                                description=f"{widget_class} height {height} is below "
                                f"minimum 44px",
                                widget=widget,
                                widget_class=widget_class,
                                widget_path=current_path,
                                recommendation="Increase widget size to at least "
                                "44x44 pixels",
                                wcag_criterion="2.5.5 Target Size",
                                auto_fixable=True,
                            )
                        )
            except tk.TclError:
                pass

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def _validate_internationalization(self, root: tk.Tk) -> None:
        """Validate internationalization and localization support"""

        def check_widget(widget: tk.Misc, path: str = "") -> None:
            widget_class = widget.winfo_class()
            current_path = f"{path}/{widget_class}" if path else widget_class

            # Check for hardcoded text that should be localized
            try:
                text = widget.cget("text")
                if text and isinstance(text, str):
                    # Check for English-specific patterns
                    english_patterns = [
                        "OK",
                        "Cancel",
                        "Yes",
                        "No",
                        "Submit",
                        "Close",
                        "Save",
                        "Open",
                        "Delete",
                    ]
                    if text in english_patterns:
                        self.issues.append(
                            AccessibilityIssue(
                                severity=IssueSeverity.INFO,
                                category=ValidationCategory.UNDERSTANDABLE,
                                title="Hardcoded text found",
                                description=f"Widget contains hardcoded text: '{text}'",
                                widget=widget,
                                widget_class=widget_class,
                                widget_path=current_path,
                                recommendation="Use localization system for text",
                                wcag_criterion="3.1.2 Language of Parts",
                                auto_fixable=False,
                            )
                        )
            except tk.TclError:
                pass

            # Check children
            try:
                for child in widget.winfo_children():
                    check_widget(child, current_path)
            except tk.TclError:
                pass

        check_widget(root)

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive accessibility report"""
        issues_by_severity: Dict[str, List[AccessibilityIssue]] = {}
        issues_by_category: Dict[str, List[AccessibilityIssue]] = {}

        for issue in self.issues:
            # Group by severity
            severity_key = issue.severity.value
            if severity_key not in issues_by_severity:
                issues_by_severity[severity_key] = []
            issues_by_severity[severity_key].append(issue)

            # Group by category
            category_key = issue.category.value
            if category_key not in issues_by_category:
                issues_by_category[category_key] = []
            issues_by_category[category_key].append(issue)

        # Calculate compliance score
        total_issues = len(self.issues)
        critical_issues = len(issues_by_severity.get("critical", []))
        high_issues = len(issues_by_severity.get("high", []))

        # Simple scoring algorithm
        if critical_issues > 0:
            compliance_score = 0
        elif high_issues > 5:
            compliance_score = max(0, 50 - (high_issues * 5))
        else:
            compliance_score = max(0, 100 - (total_issues * 2))

        return {
            "compliance_level": self.compliance_level.value,
            "total_issues": total_issues,
            "compliance_score": compliance_score,
            "issues_by_severity": issues_by_severity,
            "issues_by_category": issues_by_category,
            "all_issues": [
                {
                    "severity": issue.severity.value,
                    "category": issue.category.value,
                    "title": issue.title,
                    "description": issue.description,
                    "widget_class": issue.widget_class,
                    "widget_path": issue.widget_path,
                    "recommendation": issue.recommendation,
                    "wcag_criterion": issue.wcag_criterion,
                    "auto_fixable": issue.auto_fixable,
                }
                for issue in self.issues
            ],
            "summary": {
                "perceivable_issues": len(issues_by_category.get("perceivable", [])),
                "operable_issues": len(issues_by_category.get("operable", [])),
                "understandable_issues": len(
                    issues_by_category.get("understandable", [])
                ),
                "robust_issues": len(issues_by_category.get("robust", [])),
            },
        }

    def auto_fix_issues(self, root: tk.Tk) -> int:
        """Automatically fix issues that can be auto-fixed"""
        fixed_count = 0

        for issue in self.issues:
            if not issue.auto_fixable or not issue.widget:
                continue

            try:
                if "contrast" in issue.title.lower():
                    # Apply high contrast theme
                    from .themes import HighContrastTheme

                    HighContrastTheme.apply(root)
                    fixed_count += 1

                elif "font size" in issue.title.lower():
                    # Increase font size
                    try:
                        current_font = issue.widget.cget("font")
                        if isinstance(current_font, tuple) and len(current_font) >= 2:
                            new_font = (
                                current_font[0],
                                max(12, current_font[1]),
                                *current_font[2:],
                            )
                            issue.widget.configure(font=new_font)
                            fixed_count += 1
                    except (tk.TclError, AttributeError):
                        pass

                elif (
                    "keyboard" in issue.title.lower()
                    and "takefocus" in issue.description
                ):
                    # Enable keyboard focus
                    try:
                        issue.widget.configure(takefocus=True)
                        fixed_count += 1
                    except (tk.TclError, AttributeError):
                        pass

                elif (
                    "font" in issue.title.lower()
                    and "difficult to read" in issue.description
                ):
                    # Change to readable font
                    try:
                        current_font = issue.widget.cget("font")
                        if isinstance(current_font, tuple):
                            new_font = (
                                "Arial",
                                current_font[1] if len(current_font) > 1 else 12,
                                *current_font[2:],
                            )
                            issue.widget.configure(font=new_font)
                            fixed_count += 1
                    except (tk.TclError, AttributeError):
                        pass

                elif "empty container" in issue.title.lower():
                    # Remove empty containers
                    try:
                        if issue.widget and not issue.widget.winfo_children():
                            issue.widget.destroy()
                            fixed_count += 1
                    except (tk.TclError, AttributeError):
                        pass

                elif (
                    "too small" in issue.title.lower() and "touch" in issue.description
                ):
                    # Increase widget size for touch targets
                    try:
                        current_width = issue.widget.cget("width")
                        current_height = issue.widget.cget("height")

                        new_width = (
                            max(44, current_width)
                            if isinstance(current_width, int)
                            else current_width
                        )
                        new_height = (
                            max(44, current_height)
                            if isinstance(current_height, int)
                            else current_height
                        )

                        if new_width != current_width:
                            issue.widget.configure(width=new_width)
                            fixed_count += 1
                        if new_height != current_height:
                            issue.widget.configure(height=new_height)
                            fixed_count += 1
                    except (tk.TclError, AttributeError):
                        pass

                elif "bright red background" in issue.title.lower():
                    # Change problematic red background
                    try:
                        issue.widget.configure(bg="#cc0000")  # Darker red
                        fixed_count += 1
                    except (tk.TclError, AttributeError):
                        pass

                elif "invalid aria role" in issue.title.lower():
                    # Remove invalid ARIA role
                    try:
                        if hasattr(issue.widget, "accessible_role"):
                            issue.widget.accessible_role = None
                            fixed_count += 1
                    except (tk.TclError, AttributeError):
                        pass

            except (tk.TclError, AttributeError):
                # Widget may not support the fix
                continue

        return fixed_count


class AccessibilityTester:
    """Interactive accessibility testing tools"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.validator = AccessibilityValidator()

    def run_full_audit(self) -> Dict[str, Any]:
        """Run complete accessibility audit"""
        print("Running accessibility audit...")

        start_time = time.time()
        self.validator.validate_application(self.root)
        end_time = time.time()

        report = self.validator.generate_report()
        report["audit_duration"] = end_time - start_time
        report["screen_reader_active"] = is_screen_reader_active()

        return report

    def test_keyboard_navigation(self) -> List[str]:
        """Test keyboard navigation interactively"""
        issues = []

        # This would implement interactive keyboard navigation testing
        # For now, return basic validation
        def check_widget(widget: tk.Misc) -> None:
            # Basic keyboard navigation validation without recursion
            widget_class = widget.winfo_class()

            # Check if widget can receive focus
            try:
                takefocus = widget.cget("takefocus")
                if takefocus == 0:
                    issues.append(
                        f"Widget {widget_class} cannot receive keyboard focus"
                    )
            except tk.TclError:
                pass

            # Check for keyboard bindings on interactive widgets
            interactive_widgets = [
                "Button",
                "Entry",
                "Text",
                "Listbox",
                "Scale",
                "Checkbutton",
                "Radiobutton",
                "Menu",
            ]
            if widget_class in interactive_widgets:
                bindings = widget.bind()
                key_bindings = [
                    b
                    for b in bindings
                    if any(key in b for key in ["<Key", "<Return", "<Tab", "<Space"])
                ]
                if not key_bindings:
                    issues.append(
                        f"Interactive widget {widget_class} lacks keyboard bindings"
                    )

            try:
                for child in widget.winfo_children():
                    check_widget(child)
            except tk.TclError:
                pass

        check_widget(self.root)
        return issues

    def test_screen_reader_compatibility(self) -> Dict[str, Any]:
        """Test screen reader compatibility"""
        return {
            "screen_reader_detected": is_screen_reader_active(),
            "widgets_with_names": self._count_widgets_with_names(),
            "widgets_with_roles": self._count_widgets_with_roles(),
            "widgets_with_descriptions": self._count_widgets_with_descriptions(),
        }

    def _count_widgets_with_names(self) -> int:
        """Count widgets with accessible names"""
        count = 0

        def check_widget(widget: tk.Misc) -> None:
            nonlocal count
            if hasattr(widget, "accessible_name") and widget.accessible_name:
                count += 1

            try:
                for child in widget.winfo_children():
                    check_widget(child)
            except tk.TclError:
                pass

        check_widget(self.root)
        return count

    def _count_widgets_with_roles(self) -> int:
        """Count widgets with accessible roles"""
        count = 0

        def check_widget(widget: tk.Misc) -> None:
            nonlocal count
            if hasattr(widget, "accessible_role") and widget.accessible_role:
                count += 1

            try:
                for child in widget.winfo_children():
                    check_widget(child)
            except tk.TclError:
                pass

        check_widget(self.root)
        return count

    def _count_widgets_with_descriptions(self) -> int:
        """Count widgets with accessible descriptions"""
        count = 0

        def check_widget(widget: tk.Misc) -> None:
            nonlocal count
            if (
                hasattr(widget, "accessible_description")
                and widget.accessible_description
            ):
                count += 1

            try:
                for child in widget.winfo_children():
                    check_widget(child)
            except tk.TclError:
                pass

        check_widget(self.root)
        return count


# Convenience functions
def validate_accessibility(
    root: tk.Tk, compliance_level: ValidationLevel = ValidationLevel.AA
) -> Dict[str, Any]:
    """Validate accessibility of an application"""
    validator = AccessibilityValidator(compliance_level)
    validator.validate_application(root)
    return validator.generate_report()


def auto_fix_accessibility_issues(root: tk.Tk) -> int:
    """Automatically fix accessibility issues that can be auto-fixed"""
    validator = AccessibilityValidator()
    validator.validate_application(root)
    return validator.auto_fix_issues(root)


def run_accessibility_audit(root: tk.Tk) -> Dict[str, Any]:
    """Run comprehensive accessibility audit"""
    tester = AccessibilityTester(root)
    return tester.run_full_audit()


def validate_keyboard_navigation_local(root: tk.Tk) -> List[str]:
    """Test keyboard navigation without recursion"""
    issues = []

    def check_widget_navigation(widget: tk.Misc) -> None:
        widget_class = widget.winfo_class()

        # Check if widget can receive focus
        try:
            takefocus = widget.cget("takefocus")
            if takefocus == 0 and widget_class in [
                "Button",
                "Entry",
                "Text",
                "Listbox",
            ]:
                issues.append(f"Interactive widget {widget_class} cannot receive focus")
        except tk.TclError:
            pass

        # Check for basic keyboard accessibility
        if widget_class in ["Button", "Entry", "Text", "Listbox", "Scale"]:
            try:
                bindings = widget.bind()
                if not any("<Key" in b or "<Return>" in b for b in bindings):
                    issues.append(
                        f"Widget {widget_class} may lack keyboard accessibility"
                    )
            except tk.TclError:
                pass

        # Recursively check children
        try:
            for child in widget.winfo_children():
                check_widget_navigation(child)
        except tk.TclError:
            pass

    check_widget_navigation(root)
    return issues


def validate_screen_reader_compatibility(root: tk.Tk) -> Dict[str, Any]:
    """Test screen reader compatibility"""
    tester = AccessibilityTester(root)
    return tester.test_screen_reader_compatibility()
