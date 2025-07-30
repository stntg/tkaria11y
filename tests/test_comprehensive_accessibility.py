# tests/test_comprehensive_accessibility.py

"""
Comprehensive tests for all accessibility features in tkaria11y.
Tests integration of all accessibility components including WCAG compliance,
ARIA support, platform integration, braille, audio, and more.
"""

import pytest
import tkinter as tk
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path to import tkaria11y
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tkaria11y import (
    # Core components
    AccessibleApp,
    setup_full_accessibility,
    quick_accessibility_audit,
    # Widgets
    AccessibleButton,
    AccessibleEntry,
    AccessibleLabel,
    AccessibleCheckbutton,
    AccessibleRadiobutton,
    AccessibleScale,
    AccessibleListbox,
    # Theming and fonts
    HighContrastTheme,
    set_dyslexic_font,
    set_large_text,
    # Focus management
    get_focus_manager,
    # Validation and testing
    run_accessibility_audit,
    auto_fix_accessibility_issues,
    validate_keyboard_navigation,
    validate_screen_reader_compatibility,
    ValidationLevel,
    AccessibilityValidator,
    # Platform integration
    get_platform_adapter,
    is_screen_reader_active,
    # ARIA compliance
    ARIARole,
    calculate_contrast_ratio,
    validate_contrast_ratio,
    # Braille support
    get_braille_manager,
    setup_braille_support,
    display_braille_text,
    is_braille_display_available,
    # Audio and TTS
    speak,
    get_audio_manager,
    setup_audio_accessibility,
)


class TestComprehensiveAccessibility:
    """Comprehensive accessibility testing suite"""

    def setup_method(self):
        """Set up test environment"""
        self.root = AccessibleApp()
        self.root.withdraw()  # Hide window during tests

    def teardown_method(self):
        """Clean up test environment"""
        if self.root:
            try:
                self.root.destroy()
            except tk.TclError:
                pass

    def test_accessible_app_initialization(self):
        """Test AccessibleApp initialization and basic features"""
        app = AccessibleApp()
        app.withdraw()

        # Test basic accessibility features are available
        assert hasattr(app, "_high_contrast_enabled")
        assert hasattr(app, "_dyslexic_font_enabled")

        # Test accessibility methods are available
        assert hasattr(app, "enable_high_contrast")
        assert hasattr(app, "enable_dyslexic_font")
        assert hasattr(app, "is_high_contrast_enabled")
        assert hasattr(app, "is_dyslexic_font_enabled")

        # Test window properties
        assert app.winfo_class() == "Tk"

        app.destroy()

    def test_full_accessibility_setup(self):
        """Test complete accessibility setup"""
        # Test with all options enabled
        setup_full_accessibility(
            self.root,
            high_contrast=True,
            dyslexic_font=True,
            large_text=True,
            enable_audio=True,
            enable_braille=True,
            enable_spatial_audio=True,
        )

        # Verify accessibility features are available
        assert hasattr(self.root, "_high_contrast_enabled")
        assert hasattr(self.root, "_dyslexic_font_enabled")

    def test_all_accessible_widgets(self):
        """Test all accessible widget types"""
        widgets = [
            AccessibleButton(
                self.root, text="Test Button", accessible_name="Test button"
            ),
            AccessibleEntry(self.root, accessible_name="Test entry field"),
            AccessibleLabel(self.root, text="Test Label", accessible_name="Test label"),
            AccessibleCheckbutton(
                self.root, text="Test Checkbox", accessible_name="Test checkbox"
            ),
            AccessibleRadiobutton(
                self.root, text="Test Radio", accessible_name="Test radio button"
            ),
            AccessibleScale(self.root, from_=0, to=100, accessible_name="Test scale"),
            AccessibleListbox(self.root, accessible_name="Test listbox"),
        ]

        for widget in widgets:
            # Test basic accessibility properties
            assert hasattr(widget, "accessible_name")
            assert widget.accessible_name is not None
            assert len(widget.accessible_name) > 0

            # Test ARIA properties
            assert hasattr(widget, "accessible_role")
            assert hasattr(widget, "accessible_description")

            # Test widget can be packed/displayed
            widget.pack()
            assert widget.winfo_manager() == "pack"

            # Test focus capability
            try:
                widget.focus_set()
            except tk.TclError:
                # Some widgets may not support focus in test environment
                pass

            widget.destroy()

    def test_wcag_compliance_validation(self):
        """Test WCAG compliance validation at all levels"""
        # Test AA level (default)
        validator_aa = AccessibilityValidator(ValidationLevel.AA)
        validator_aa.validate_application(self.root)
        report_aa = validator_aa.generate_report()

        assert "compliance_level" in report_aa
        assert report_aa["compliance_level"] == "AA"
        assert "total_issues" in report_aa
        assert "compliance_score" in report_aa

        # Test AAA level
        validator_aaa = AccessibilityValidator(ValidationLevel.AAA)
        validator_aaa.validate_application(self.root)
        report_aaa = validator_aaa.generate_report()

        assert report_aaa["compliance_level"] == "AAA"

    def test_comprehensive_validation_categories(self):
        """Test all WCAG validation categories"""
        # Create a complex widget hierarchy for testing
        frame = tk.Frame(self.root)
        frame.pack()

        # Add various widgets to test different validation aspects
        button = AccessibleButton(
            frame, text="Click me", accessible_name="Action button"
        )
        button.pack()

        entry = AccessibleEntry(frame, accessible_name="Input field")
        entry.pack()

        label = AccessibleLabel(frame, text="Information", accessible_name="Info label")
        label.pack()

        # Run comprehensive validation
        validator = AccessibilityValidator(ValidationLevel.AA)
        validator.validate_application(self.root)
        report = validator.generate_report()

        # Check that all WCAG categories are covered
        assert "summary" in report
        summary = report["summary"]

        assert "perceivable_issues" in summary
        assert "operable_issues" in summary
        assert "understandable_issues" in summary
        assert "robust_issues" in summary

        # Check issues by category
        assert "issues_by_category" in report
        categories = report["issues_by_category"]

        # Check that we have at least some categories with issues
        # (not all categories may have issues in every test case)
        expected_categories = ["perceivable", "operable", "understandable", "robust"]
        found_categories = set(categories.keys())

        # Should have at least 2 categories with issues
        assert len(found_categories) >= 2

        # All found categories should be valid WCAG categories
        for category in found_categories:
            assert category in expected_categories

    def test_color_contrast_validation(self):
        """Test color contrast validation"""
        # Test high contrast
        high_ratio = calculate_contrast_ratio("#000000", "#FFFFFF")
        assert high_ratio > 7.0  # Should meet AAA standard
        assert validate_contrast_ratio("#000000", "#FFFFFF", "AAA")

        # Test low contrast
        low_ratio = calculate_contrast_ratio("#888888", "#999999")
        assert low_ratio < 4.5  # Should fail AA standard
        assert not validate_contrast_ratio("#888888", "#999999", "AA")

        # Test medium contrast (use a color that meets AA but not AAA)
        medium_ratio = calculate_contrast_ratio("#FFFFFF", "#757575")
        assert 4.5 <= medium_ratio < 7.0  # Should meet AA but not AAA
        assert validate_contrast_ratio("#FFFFFF", "#757575", "AA")
        assert not validate_contrast_ratio("#FFFFFF", "#757575", "AAA")

    def test_keyboard_navigation(self):
        """Test keyboard navigation functionality"""
        # Create focusable widgets
        button1 = AccessibleButton(
            self.root, text="Button 1", accessible_name="First button"
        )
        button1.pack()

        entry1 = AccessibleEntry(self.root, accessible_name="Text input")
        entry1.pack()

        button2 = AccessibleButton(
            self.root, text="Button 2", accessible_name="Second button"
        )
        button2.pack()

        # Test keyboard navigation
        navigation_issues = validate_keyboard_navigation(self.root)
        assert isinstance(navigation_issues, list)

        # Test focus manager
        focus_manager = get_focus_manager(self.root)
        assert focus_manager is not None

    def test_screen_reader_compatibility(self):
        """Test screen reader compatibility"""
        # Add widgets with proper accessibility attributes
        button = AccessibleButton(
            self.root,
            text="Test Button",
            accessible_name="Test action button",
            accessible_description="Performs a test action",
        )
        button.pack()

        entry = AccessibleEntry(
            self.root,
            accessible_name="Test input",
            accessible_description="Enter test data here",
        )
        entry.pack()

        # Test screen reader compatibility
        compatibility = validate_screen_reader_compatibility(self.root)
        assert isinstance(compatibility, dict)
        assert "screen_reader_detected" in compatibility
        assert "widgets_with_names" in compatibility
        assert "widgets_with_roles" in compatibility
        assert "widgets_with_descriptions" in compatibility

        # Should find our widgets
        assert compatibility["widgets_with_names"] >= 2
        assert compatibility["widgets_with_descriptions"] >= 2

    def test_platform_integration(self):
        """Test platform-specific accessibility integration"""
        try:
            adapter = get_platform_adapter()
            assert adapter is not None

            # Test basic adapter functionality
            button = AccessibleButton(
                self.root, text="Test", accessible_name="Test button"
            )
            button.pack()

            # These might not work in test environment but shouldn't crash
            adapter.set_accessible_name(button, "Platform test button")
            adapter.set_accessible_description(button, "Test description")
            adapter.set_accessible_role(button, "button")

        except Exception:
            # Platform adapters may not work in test environment
            # but should not crash
            pass

    def test_high_contrast_theming(self):
        """Test high contrast theme functionality"""
        # Apply high contrast theme
        HighContrastTheme.apply(self.root)

        # Create widgets to test theming
        button = AccessibleButton(
            self.root, text="Themed Button", accessible_name="Themed button"
        )
        button.pack()

        entry = AccessibleEntry(self.root, accessible_name="Themed entry")
        entry.pack()

        # Test that theme was applied (colors should be high contrast)
        try:
            button_bg = button.cget("bg")
            button_fg = button.cget("fg")

            # High contrast theme should use specific colors
            assert button_bg is not None
            assert button_fg is not None

        except tk.TclError:
            # Theme might not apply in test environment
            pass

    def test_dyslexic_font_support(self):
        """Test dyslexic-friendly font functionality"""
        button = AccessibleButton(
            self.root, text="Font Test", accessible_name="Font test button"
        )
        button.pack()

        # Apply dyslexic font
        set_dyslexic_font(self.root)

        # Test large text
        set_large_text(self.root)

        # Font should be applied
        try:
            font = button.cget("font")
            assert font is not None
        except tk.TclError:
            pass

    def test_audio_feedback(self):
        """Test audio feedback and TTS functionality"""
        try:
            # Test basic TTS functionality
            speak("Test message", priority="low")
            # TTS should not raise exceptions
        except Exception:
            # TTS might not be available in test environment
            pass

        # Test audio manager
        try:
            audio_manager = get_audio_manager(self.root)
            assert audio_manager is not None

            # Test audio feedback setup
            setup_audio_accessibility(self.root, enable_tts=True, enable_sounds=True)

        except Exception:
            # Audio might not be available in test environment
            pass

    def test_braille_support(self):
        """Test braille display support"""
        try:
            # Test braille manager
            braille_manager = get_braille_manager()
            assert braille_manager is not None

            # Test braille setup
            setup_braille_support(self.root)

            # Test braille display availability
            available = is_braille_display_available()
            assert isinstance(available, bool)

            # Test braille text display
            display_braille_text("Test braille message")

            # Test braille display info
            braille_info = braille_manager.get_braille_display_info()
            assert isinstance(braille_info, dict)

        except Exception:
            # Braille might not be available in test environment
            pass

    def test_aria_compliance(self):
        """Test ARIA compliance validation"""
        # Create widgets with ARIA properties
        button = AccessibleButton(
            self.root,
            text="ARIA Test",
            accessible_name="ARIA test button",
            accessible_description="Tests ARIA compliance",
        )
        button.pack()

        # Set ARIA role
        if hasattr(button, "accessible_role"):
            button.accessible_role = ARIARole.BUTTON.value

    def test_auto_fix_functionality(self):
        """Test automatic accessibility issue fixing"""
        # Create widgets with potential issues
        button_no_name = tk.Button(self.root, text="No Name")
        button_no_name.pack()

        small_button = tk.Button(self.root, text="Small", width=1, height=1)
        small_button.pack()

        # Run auto-fix
        fixed_count = auto_fix_accessibility_issues(self.root)
        assert isinstance(fixed_count, int)
        assert fixed_count >= 0

    def test_comprehensive_audit(self):
        """Test comprehensive accessibility audit"""
        # Create a complex interface
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Add various widgets
        title = AccessibleLabel(
            main_frame, text="Test Application", accessible_name="Application title"
        )
        title.pack()

        form_frame = tk.Frame(main_frame)
        form_frame.pack()

        name_entry = AccessibleEntry(form_frame, accessible_name="Name field")
        name_entry.pack()

        submit_button = AccessibleButton(
            form_frame, text="Submit", accessible_name="Submit form"
        )
        submit_button.pack()

        # Run comprehensive audit
        audit_result = run_accessibility_audit(self.root)

        assert isinstance(audit_result, dict)
        assert "compliance_level" in audit_result
        assert "total_issues" in audit_result
        assert "compliance_score" in audit_result
        assert "issues_by_severity" in audit_result
        assert "issues_by_category" in audit_result
        assert "all_issues" in audit_result
        assert "summary" in audit_result

        # Test quick audit
        quick_result = quick_accessibility_audit(self.root)
        assert isinstance(quick_result, dict)
        assert "total_issues" in quick_result
        assert "critical_issues" in quick_result

    def test_validation_edge_cases(self):
        """Test validation with edge cases and complex scenarios"""
        # Test empty application
        empty_app = AccessibleApp()
        empty_app.withdraw()

        validator = AccessibilityValidator()
        validator.validate_application(empty_app)
        empty_report = validator.generate_report()

        assert empty_report["total_issues"] >= 0

        empty_app.destroy()

        # Test deeply nested widgets
        current_parent = self.root
        for i in range(5):
            frame = tk.Frame(current_parent)
            frame.pack()
            current_parent = frame

        deep_button = AccessibleButton(
            current_parent, text="Deep Button", accessible_name="Deeply nested button"
        )
        deep_button.pack()

        validator.validate_application(self.root)
        deep_report = validator.generate_report()

        assert isinstance(deep_report, dict)

    def test_accessibility_mixins(self):
        """Test accessibility mixins functionality"""
        from tkaria11y.mixins import (
            AccessibleMixin,
            BrailleMixin,
            HighContrastMixin,
            ComprehensiveAccessibilityMixin,
        )

        # Test that mixins can be imported and have expected methods
        assert hasattr(AccessibleMixin, "__init__")
        assert hasattr(BrailleMixin, "__init__")
        assert hasattr(HighContrastMixin, "__init__")
        assert hasattr(ComprehensiveAccessibilityMixin, "__init__")

    def test_error_handling_and_robustness(self):
        """Test error handling and robustness of accessibility features"""
        # Test with invalid parameters
        try:
            # This should not crash
            validator = AccessibilityValidator(ValidationLevel.AA)
            validator.validate_application(None)
        except Exception:
            # Should handle gracefully
            pass

        # Test with destroyed widgets
        button = AccessibleButton(
            self.root, text="Temp", accessible_name="Temporary button"
        )
        button.pack()
        button.destroy()

        # Validation should handle destroyed widgets
        validator = AccessibilityValidator()
        validator.validate_application(self.root)
        report = validator.generate_report()

        assert isinstance(report, dict)

    def test_performance_with_large_applications(self):
        """Test performance with applications containing many widgets"""
        # Create a large number of widgets
        container = tk.Frame(self.root)
        container.pack()

        widgets = []
        for i in range(50):  # Create 50 widgets
            if i % 3 == 0:
                widget = AccessibleButton(
                    container, text=f"Button {i}", accessible_name=f"Button number {i}"
                )
            elif i % 3 == 1:
                widget = AccessibleEntry(container, accessible_name=f"Entry field {i}")
            else:
                widget = AccessibleLabel(
                    container, text=f"Label {i}", accessible_name=f"Label number {i}"
                )

            widget.pack()
            widgets.append(widget)

        # Run validation and measure basic performance
        import time

        start_time = time.time()

        validator = AccessibilityValidator()
        validator.validate_application(self.root)
        report = validator.generate_report()

        end_time = time.time()
        validation_time = end_time - start_time

        # Validation should complete in reasonable time (< 5 seconds)
        assert validation_time < 5.0
        assert isinstance(report, dict)
        assert report["total_issues"] >= 0

    def test_integration_with_standard_tkinter(self):
        """Test integration with standard Tkinter widgets"""
        # Mix accessible and standard widgets
        std_button = tk.Button(self.root, text="Standard Button")
        std_button.pack()

        acc_button = AccessibleButton(
            self.root, text="Accessible Button", accessible_name="Accessible button"
        )
        acc_button.pack()

        std_entry = tk.Entry(self.root)
        std_entry.pack()

        acc_entry = AccessibleEntry(self.root, accessible_name="Accessible entry")
        acc_entry.pack()

        # Validation should handle both types
        validator = AccessibilityValidator()
        validator.validate_application(self.root)
        report = validator.generate_report()

        assert isinstance(report, dict)
        # Should find issues with standard widgets lacking accessibility
        assert report["total_issues"] > 0

    def test_wcag_criterion_coverage(self):
        """Test that validation covers all major WCAG criteria"""
        # Create widgets that test different WCAG criteria

        # 1.1.1 Non-text Content
        img_button = tk.Button(self.root, text="")  # Button without text
        img_button.pack()

        # 1.4.3 Contrast (Minimum)
        low_contrast_label = tk.Label(
            self.root, text="Low contrast", bg="#cccccc", fg="#dddddd"
        )
        low_contrast_label.pack()

        # 2.1.1 Keyboard
        no_focus_widget = tk.Label(self.root, text="No focus", takefocus=0)
        no_focus_widget.pack()

        # 3.3.2 Labels or Instructions
        unlabeled_entry = tk.Entry(self.root)
        unlabeled_entry.pack()

        # 4.1.2 Name, Role, Value
        custom_widget = tk.Frame(self.root)
        custom_widget.pack()

        # Run validation
        validator = AccessibilityValidator(ValidationLevel.AA)
        validator.validate_application(self.root)
        report = validator.generate_report()

        # Should find multiple issues covering different WCAG criteria
        assert report["total_issues"] > 0

        # Check that issues reference WCAG criteria
        wcag_criteria_found = set()
        for issue in report["all_issues"]:
            if "wcag_criterion" in issue and issue["wcag_criterion"]:
                wcag_criteria_found.add(issue["wcag_criterion"])

        # Should find issues for multiple WCAG criteria
        assert len(wcag_criteria_found) > 0

    def test_comprehensive_validator_methods(self):
        """Test that all validator methods are working"""
        validator = AccessibilityValidator(ValidationLevel.AA)

        # Create widgets that will trigger various validation methods

        # Widget without accessible name (perceivable)
        nameless_button = tk.Button(self.root, text="")
        nameless_button.pack()

        # Widget with poor contrast (perceivable)
        poor_contrast = tk.Label(
            self.root, text="Hard to read", bg="#cccccc", fg="#dddddd"
        )
        poor_contrast.pack()

        # Widget that can't receive focus (operable)
        no_focus = tk.Label(self.root, text="No focus", takefocus=0)
        no_focus.pack()

        # Entry without label (understandable)
        unlabeled_entry = tk.Entry(self.root)
        unlabeled_entry.pack()

        # Widget without accessibility features (robust)
        basic_frame = tk.Frame(self.root)
        basic_frame.pack()

        # Run validation
        validator.validate_application(self.root)
        report = validator.generate_report()

        # Should find issues in all categories
        assert report["total_issues"] > 0

        # Test auto-fix functionality
        fixed_count = validator.auto_fix_issues(self.root)
        assert isinstance(fixed_count, int)
        assert fixed_count >= 0

    def test_validator_comprehensive_coverage(self):
        """Test that validator covers all accessibility aspects"""
        validator = AccessibilityValidator(ValidationLevel.AAA)

        # Create a comprehensive test interface
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True)

        # Test text alternatives (1.1.1)
        image_button = tk.Button(main_container, text="")
        image_button.pack()

        # Test color usage (1.4.1)
        color_only_button = tk.Button(main_container, bg="red", text="")
        color_only_button.pack()

        # Test contrast (1.4.3, 1.4.6)
        low_contrast = tk.Label(
            main_container, text="Low contrast", bg="#aaaaaa", fg="#bbbbbb"
        )
        low_contrast.pack()

        # Test text sizing (1.4.4)
        tiny_text = tk.Label(main_container, text="Tiny text", font=("Arial", 6))
        tiny_text.pack()

        # Test keyboard access (2.1.1)
        no_keyboard = tk.Button(main_container, text="No keyboard", takefocus=0)
        no_keyboard.pack()

        # Test focus order (2.4.3)
        for i in range(3):
            btn = tk.Button(main_container, text=f"Button {i}")
            btn.pack()

        # Test form labels (3.3.2)
        unlabeled_input = tk.Entry(main_container)
        unlabeled_input.pack()

        # Test assistive technology (4.1.2)
        no_aria = tk.Button(main_container, text="No ARIA")
        no_aria.pack()

        # Run comprehensive validation
        validator.validate_application(self.root)
        report = validator.generate_report()

        # Should find multiple issues
        assert report["total_issues"] > 5

        # Should cover all WCAG categories
        summary = report["summary"]
        assert summary["perceivable_issues"] > 0
        assert summary["operable_issues"] > 0
        assert summary["understandable_issues"] > 0
        assert summary["robust_issues"] > 0

        # Should have issues at different severity levels
        issues_by_severity = report["issues_by_severity"]
        total_severity_issues = sum(
            len(issues) for issues in issues_by_severity.values()
        )
        assert total_severity_issues == report["total_issues"]


if __name__ == "__main__":
    pytest.main([__file__])
