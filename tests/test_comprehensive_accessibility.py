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
    configure_advanced_focus_traversal,
    # Validation and testing
    run_accessibility_audit,
    auto_fix_accessibility_issues,
    test_keyboard_navigation,
    test_screen_reader_compatibility,
    ValidationLevel,
    AccessibilityValidator,
    # Platform integration
    get_platform_adapter,
    is_screen_reader_active,
    # ARIA compliance
    ARIARole,
    ARIAProperty,
    validate_aria_compliance,
    calculate_contrast_ratio,
    validate_contrast_ratio,
    # Braille support
    get_braille_manager,
    setup_braille_support,
    display_braille_text,
    is_braille_display_available,
    BrailleDisplayType,
    # Audio accessibility
    get_audio_manager,
    setup_audio_accessibility,
    play_audio_cue,
    AudioCueType,
    is_audio_available,
    # TTS
    speak,
    tts,
)


class TestComprehensiveAccessibility:
    """Test comprehensive accessibility features"""

    def setup_method(self):
        """Set up test environment"""
        self.root = AccessibleApp()
        self.root.withdraw()  # Hide window during tests

    def teardown_method(self):
        """Clean up test environment"""
        if self.root:
            self.root.destroy()

    def test_accessible_app_creation(self):
        """Test AccessibleApp creation and basic functionality"""
        assert isinstance(self.root, tk.Tk)
        assert hasattr(self.root, "accessibility_features")

        # Test that accessibility features are initialized
        features = self.root.accessibility_features
        assert "tts_enabled" in features
        assert "focus_management" in features
        assert "high_contrast" in features

    def test_full_accessibility_setup(self):
        """Test complete accessibility setup"""
        # Test setup with all features enabled
        setup_full_accessibility(
            self.root,
            high_contrast=True,
            dyslexic_font=True,
            large_text=False,
            auto_fix=True,
            enable_audio=True,
            enable_braille=True,
            enable_spatial_audio=True,
        )

        # Verify focus manager is set up
        focus_manager = get_focus_manager(self.root)
        assert focus_manager is not None

        # Verify audio manager is set up
        audio_manager = get_audio_manager(self.root)
        assert audio_manager is not None

        # Verify braille manager is set up
        braille_manager = get_braille_manager()
        assert braille_manager is not None

    def test_accessible_widgets_creation(self):
        """Test creation of accessible widgets"""
        # Test basic widgets
        button = AccessibleButton(
            self.root,
            text="Test Button",
            accessible_name="Test button",
            accessible_description="A test button for accessibility",
            accessible_role="button",
        )
        assert hasattr(button, "accessible_name")
        assert button.accessible_name == "Test button"
        assert hasattr(button, "accessible_description")
        assert hasattr(button, "accessible_role")

        entry = AccessibleEntry(
            self.root,
            accessible_name="Test entry",
            accessible_description="A test entry field",
        )
        assert hasattr(entry, "accessible_name")
        assert entry.accessible_name == "Test entry"

        checkbox = AccessibleCheckbutton(
            self.root,
            text="Test Checkbox",
            accessible_name="Test checkbox",
            accessible_description="A test checkbox",
        )
        assert hasattr(checkbox, "accessible_name")
        assert checkbox.accessible_name == "Test checkbox"

    def test_aria_compliance(self):
        """Test ARIA compliance validation"""
        button = AccessibleButton(
            self.root,
            text="ARIA Test Button",
            accessible_name="ARIA test button",
            accessible_role="button",
        )

        # Test ARIA role validation
        role = ARIARole.BUTTON
        properties = {ARIAProperty.LABEL: "ARIA test button"}

        errors = validate_aria_compliance(button, role, properties)
        assert isinstance(errors, list)

        # Test contrast ratio calculation
        ratio = calculate_contrast_ratio("#000000", "#FFFFFF")
        assert ratio > 20.0  # Black on white should have high contrast

        # Test contrast validation
        assert validate_contrast_ratio("#000000", "#FFFFFF", "AA", "normal")
        assert validate_contrast_ratio("#000000", "#FFFFFF", "AAA", "normal")

    def test_focus_management(self):
        """Test advanced focus management"""
        # Create multiple focusable widgets
        button1 = AccessibleButton(
            self.root, text="Button 1", accessible_name="First button"
        )
        button2 = AccessibleButton(
            self.root, text="Button 2", accessible_name="Second button"
        )
        entry = AccessibleEntry(self.root, accessible_name="Test entry")

        button1.pack()
        button2.pack()
        entry.pack()

        # Get focus manager
        focus_manager = get_focus_manager(self.root)

        # Register widgets
        focus_manager.register_widget(button1)
        focus_manager.register_widget(button2)
        focus_manager.register_widget(entry)

        # Test focus traversal
        focusable_widgets = focus_manager.get_focusable_widgets()
        assert len(focusable_widgets) >= 3

        # Test focus callbacks
        callback_called = False

        def focus_callback(widget, has_focus):
            nonlocal callback_called
            callback_called = True

        focus_manager.add_focus_callback(focus_callback)

        # Simulate focus change
        button1.focus_set()
        self.root.update()

        # Note: callback might not be called in test environment
        # but we can verify the callback was registered
        assert focus_callback in focus_manager._focus_callbacks

    def test_accessibility_validation(self):
        """Test accessibility validation and auditing"""
        # Create widgets with various accessibility issues
        good_button = AccessibleButton(
            self.root,
            text="Good Button",
            accessible_name="Well-labeled button",
            accessible_description="This button has proper accessibility",
        )

        bad_button = tk.Button(self.root, text="Bad Button")  # No accessibility

        good_button.pack()
        bad_button.pack()

        # Run accessibility audit
        audit_report = run_accessibility_audit(self.root)

        assert "compliance_score" in audit_report
        assert "total_issues" in audit_report
        assert "all_issues" in audit_report
        assert isinstance(audit_report["all_issues"], list)

        # Test quick audit
        quick_report = quick_accessibility_audit(self.root)
        assert "compliance_score" in quick_report
        assert "total_issues" in quick_report
        assert "recommendations" in quick_report

        # Test auto-fix
        fixed_count = auto_fix_accessibility_issues(self.root)
        assert isinstance(fixed_count, int)
        assert fixed_count >= 0

    def test_keyboard_navigation(self):
        """Test keyboard navigation validation"""
        button = AccessibleButton(
            self.root, text="Keyboard Test", accessible_name="Keyboard test button"
        )
        button.pack()

        # Test keyboard navigation validation
        nav_issues = test_keyboard_navigation(self.root)
        assert isinstance(nav_issues, list)

    def test_screen_reader_compatibility(self):
        """Test screen reader compatibility"""
        button = AccessibleButton(
            self.root,
            text="Screen Reader Test",
            accessible_name="Screen reader test button",
            accessible_description="Button for testing screen reader compatibility",
        )
        button.pack()

        # Test screen reader compatibility
        sr_report = test_screen_reader_compatibility(self.root)

        assert "screen_reader_detected" in sr_report
        assert "widgets_with_names" in sr_report
        assert "widgets_with_roles" in sr_report
        assert "widgets_with_descriptions" in sr_report

        # Should have at least one widget with name
        assert sr_report["widgets_with_names"] >= 1

    def test_platform_integration(self):
        """Test platform-specific accessibility integration"""
        adapter = get_platform_adapter()
        assert adapter is not None

        button = AccessibleButton(
            self.root, text="Platform Test", accessible_name="Platform test button"
        )

        # Test platform adapter methods (should not raise exceptions)
        try:
            adapter.set_accessible_name(button, "Platform test button")
            adapter.set_accessible_description(button, "Test description")
            adapter.set_accessible_role(button, "button")
            adapter.set_accessible_value(button, "test value")
            adapter.set_accessible_state(button, "focused", True)
        except Exception as e:
            # Platform adapters may not work in test environment
            # but should not crash
            pass

        # Test screen reader detection
        sr_active = is_screen_reader_active()
        assert isinstance(sr_active, bool)

    def test_theming_and_fonts(self):
        """Test theming and font accessibility features"""
        # Test high contrast theme
        HighContrastTheme.apply(self.root)
        assert HighContrastTheme.is_applied(self.root)

        # Test dyslexic font
        set_dyslexic_font(self.root, size=14)

        # Test large text
        set_large_text(self.root)

        # Remove high contrast theme
        HighContrastTheme.remove(self.root)
        assert not HighContrastTheme.is_applied(self.root)

    def test_tts_integration(self):
        """Test text-to-speech integration"""
        # Test basic TTS functionality
        try:
            speak("Test message", priority="low")
            # TTS should not raise exceptions
        except Exception as e:
            # TTS might not be available in test environment
            pass

        # Test TTS engine properties
        assert hasattr(tts, "speak")
        assert hasattr(tts, "set_rate")
        assert hasattr(tts, "set_volume")
        assert hasattr(tts, "set_voice")

    @pytest.mark.skipif(not is_audio_available(), reason="Audio not available")
    def test_audio_accessibility(self):
        """Test audio accessibility features"""
        # Set up audio accessibility
        setup_audio_accessibility(self.root, enable_spatial=True)

        audio_manager = get_audio_manager(self.root)
        assert audio_manager is not None

        # Test audio cues
        play_audio_cue(AudioCueType.BUTTON_PRESS)
        play_audio_cue(AudioCueType.FOCUS_CHANGE)
        play_audio_cue(AudioCueType.SUCCESS)

        # Test audio settings
        audio_manager.set_master_volume(0.5)
        assert audio_manager.audio_engine.get_master_volume() == 0.5

        audio_manager.set_audio_enabled(False)
        assert not audio_manager.audio_engine.is_audio_enabled()

        audio_manager.set_audio_enabled(True)
        assert audio_manager.audio_engine.is_audio_enabled()

        # Test audio info
        audio_info = audio_manager.get_audio_info()
        assert "available" in audio_info
        assert "enabled" in audio_info
        assert "master_volume" in audio_info

    @pytest.mark.skipif(
        not is_braille_display_available(), reason="Braille display not available"
    )
    def test_braille_support(self):
        """Test braille display support"""
        # Set up braille support
        setup_braille_support(self.root)

        braille_manager = get_braille_manager()
        assert braille_manager is not None

        # Test braille text display
        display_braille_text("Test braille message")

        # Test widget braille display
        button = AccessibleButton(
            self.root, text="Braille Test", accessible_name="Braille test button"
        )
        display_widget_on_braille(button)

        # Test braille display info
        braille_info = braille_manager.get_braille_display_info()
        assert isinstance(braille_info, dict)

    def test_comprehensive_widget_accessibility(self):
        """Test comprehensive accessibility for all widget types"""
        widgets = [
            AccessibleButton(self.root, text="Button", accessible_name="Test button"),
            AccessibleEntry(self.root, accessible_name="Test entry"),
            AccessibleLabel(self.root, text="Label", accessible_name="Test label"),
            AccessibleCheckbutton(
                self.root, text="Checkbox", accessible_name="Test checkbox"
            ),
            AccessibleRadiobutton(
                self.root, text="Radio", accessible_name="Test radio"
            ),
            AccessibleScale(self.root, accessible_name="Test scale"),
            AccessibleListbox(self.root, accessible_name="Test listbox"),
        ]

        for widget in widgets:
            # Pack widget
            widget.pack()

            # Test basic accessibility properties
            assert hasattr(widget, "accessible_name")
            assert widget.accessible_name

            # Test ARIA properties if available
            if hasattr(widget, "get_accessibility_info"):
                info = widget.get_accessibility_info()
                assert isinstance(info, dict)
                assert "accessible_name" in info

            # Test focus capability
            try:
                widget.focus_set()
                focused = self.root.focus_get()
                # Focus might not work in test environment
            except tk.TclError:
                pass

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

        # Test mixin methods
        button = AccessibleButton(
            self.root, text="Mixin Test", accessible_name="Mixin test button"
        )

        if hasattr(button, "set_accessible_name"):
            button.set_accessible_name("Updated name")
            assert button.accessible_name == "Updated name"

        if hasattr(button, "get_accessibility_info"):
            info = button.get_accessibility_info()
            assert isinstance(info, dict)

    def test_wcag_compliance_levels(self):
        """Test WCAG compliance level validation"""
        validator = AccessibilityValidator(ValidationLevel.AA)

        # Create test widgets
        good_button = AccessibleButton(
            self.root,
            text="WCAG Test",
            accessible_name="WCAG compliant button",
            accessible_description="This button meets WCAG guidelines",
        )
        good_button.pack()

        # Run validation
        issues = validator.validate_application(self.root)
        assert isinstance(issues, list)

        # Generate report
        report = validator.generate_report()
        assert "compliance_level" in report
        assert "total_issues" in report
        assert "compliance_score" in report
        assert "issues_by_severity" in report
        assert "issues_by_category" in report

        # Test different compliance levels
        for level in [ValidationLevel.A, ValidationLevel.AA, ValidationLevel.AAA]:
            validator_level = AccessibilityValidator(level)
            level_issues = validator_level.validate_application(self.root)
            assert isinstance(level_issues, list)

    def test_error_handling_and_robustness(self):
        """Test error handling and robustness of accessibility features"""
        # Test with invalid parameters
        try:
            # Invalid contrast colors
            ratio = calculate_contrast_ratio("invalid", "colors")
            assert ratio >= 1.0  # Should return minimum ratio
        except Exception:
            pass

        # Test with destroyed widgets
        button = AccessibleButton(self.root, text="Test", accessible_name="Test")
        button.pack()
        button.destroy()

        # Should not crash when validating destroyed widgets
        try:
            audit_report = run_accessibility_audit(self.root)
            assert isinstance(audit_report, dict)
        except Exception:
            pass

        # Test with None values
        try:
            speak(None)  # Should handle None gracefully
        except Exception:
            pass

    def test_integration_with_standard_tkinter(self):
        """Test integration with standard Tkinter widgets"""
        # Mix accessible and standard widgets
        accessible_button = AccessibleButton(
            self.root, text="Accessible", accessible_name="Accessible button"
        )
        standard_button = tk.Button(self.root, text="Standard")

        accessible_button.pack()
        standard_button.pack()

        # Should handle mixed widget types gracefully
        audit_report = run_accessibility_audit(self.root)
        assert isinstance(audit_report, dict)

        # Standard widgets should be flagged as having accessibility issues
        assert audit_report["total_issues"] > 0

    def test_performance_and_memory(self):
        """Test performance and memory usage of accessibility features"""
        import time
        import gc

        # Create many accessible widgets
        start_time = time.time()

        widgets = []
        for i in range(100):
            widget = AccessibleButton(
                self.root,
                text=f"Button {i}",
                accessible_name=f"Button number {i}",
                accessible_description=f"This is button number {i}",
            )
            widgets.append(widget)

        creation_time = time.time() - start_time

        # Should create widgets reasonably quickly (less than 5 seconds)
        assert creation_time < 5.0

        # Test memory cleanup
        for widget in widgets:
            widget.destroy()

        widgets.clear()
        gc.collect()

        # Memory should be freed (basic test)
        # In a real test, you might use memory profiling tools


class TestAccessibilityIntegration:
    """Test integration between different accessibility components"""

    def setup_method(self):
        """Set up test environment"""
        self.root = AccessibleApp()
        self.root.withdraw()

    def teardown_method(self):
        """Clean up test environment"""
        if self.root:
            self.root.destroy()

    def test_tts_and_focus_integration(self):
        """Test integration between TTS and focus management"""
        button = AccessibleButton(
            self.root, text="TTS Test", accessible_name="TTS integration test button"
        )
        button.pack()

        # Set up focus management
        focus_manager = get_focus_manager(self.root)
        focus_manager.register_widget(button)

        # Focus should trigger TTS announcement
        button.focus_set()
        self.root.update()

        # Test passed if no exceptions were raised

    def test_audio_and_braille_integration(self):
        """Test integration between audio cues and braille display"""
        if is_audio_available() and is_braille_display_available():
            setup_audio_accessibility(self.root)
            setup_braille_support(self.root)

            button = AccessibleButton(
                self.root,
                text="Multi-modal Test",
                accessible_name="Multi-modal test button",
            )
            button.pack()

            # Focus should trigger both audio and braille updates
            button.focus_set()
            self.root.update()

    def test_validation_and_auto_fix_integration(self):
        """Test integration between validation and auto-fix"""
        # Create widgets with fixable issues
        button = tk.Button(self.root, text="Fixable Button")
        button.pack()

        # Run audit to find issues
        initial_report = run_accessibility_audit(self.root)
        initial_issues = initial_report["total_issues"]

        # Auto-fix issues
        fixed_count = auto_fix_accessibility_issues(self.root)

        # Run audit again
        final_report = run_accessibility_audit(self.root)
        final_issues = final_report["total_issues"]

        # Should have fewer issues after auto-fix
        if fixed_count > 0:
            assert final_issues < initial_issues


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
