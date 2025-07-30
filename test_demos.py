#!/usr/bin/env python3
"""
Test script to verify that both demo applications can be imported and initialized.
"""

import sys
import traceback


def test_demo_imports():
    """Test that both demos can be imported without errors."""
    print("Testing demo imports...")

    try:
        print("  Importing simple_demo...")
        import simple_demo

        print("  ✓ simple_demo imported successfully")
    except Exception as e:
        print(f"  ✗ simple_demo import failed: {e}")
        traceback.print_exc()
        return False

    try:
        print("  Importing comprehensive_demo...")
        import comprehensive_demo

        print("  ✓ comprehensive_demo imported successfully")
    except Exception as e:
        print(f"  ✗ comprehensive_demo import failed: {e}")
        traceback.print_exc()
        return False

    return True


def test_demo_classes():
    """Test that demo classes can be instantiated."""
    print("\nTesting demo class instantiation...")

    try:
        print("  Creating SimpleDemoApp...")
        from simple_demo import SimpleDemoApp

        app = SimpleDemoApp()
        print("  ✓ SimpleDemoApp created successfully")
        app.destroy()  # Clean up
    except Exception as e:
        print(f"  ✗ SimpleDemoApp creation failed: {e}")
        traceback.print_exc()
        return False

    try:
        print("  Creating ComprehensiveDemoApp...")
        from comprehensive_demo import ComprehensiveDemoApp

        app = ComprehensiveDemoApp()
        print("  ✓ ComprehensiveDemoApp created successfully")
        app.destroy()  # Clean up
    except Exception as e:
        print(f"  ✗ ComprehensiveDemoApp creation failed: {e}")
        traceback.print_exc()
        return False

    return True


def test_widget_availability():
    """Test that all required widgets are available."""
    print("\nTesting widget availability...")

    try:
        from tkaria11y.widgets import (
            # Standard Tkinter widgets
            AccessibleButton,
            AccessibleEntry,
            AccessibleLabel,
            AccessibleText,
            AccessibleCheckbutton,
            AccessibleRadiobutton,
            AccessibleScale,
            AccessibleScrollbar,
            AccessibleListbox,
            AccessibleFrame,
            AccessibleLabelFrame,
            AccessibleCanvas,
            AccessibleMessage,
            AccessibleSpinbox,
            AccessiblePanedWindow,
            # TTK widgets
            AccessibleTTKButton,
            AccessibleTTKEntry,
            AccessibleTTKLabel,
            AccessibleTTKCheckbutton,
            AccessibleTTKRadiobutton,
            AccessibleTTKScale,
            AccessibleTTKScrollbar,
            AccessibleTTKFrame,
            AccessibleTTKLabelFrame,
            AccessibleNotebook,
            AccessibleTTKProgressbar,
            AccessibleTTKSeparator,
            AccessibleTreeview,
            AccessibleCombobox,
            AccessibleTTKSpinbox,
            AccessibleTTKPanedWindow,
        )

        print("  ✓ All required widgets imported successfully")

        # Test that TTKPanedWindow is properly available
        import tkinter.ttk as ttk

        root = ttk.Frame()
        paned = AccessibleTTKPanedWindow(root, orient="horizontal")
        print("  ✓ AccessibleTTKPanedWindow can be instantiated")

        return True
    except Exception as e:
        print(f"  ✗ Widget import failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("tkaria11y Demo Test Suite")
    print("=" * 40)

    success = True

    success &= test_demo_imports()
    success &= test_widget_availability()
    success &= test_demo_classes()

    print("\n" + "=" * 40)
    if success:
        print("✓ All tests passed! Both demos are working correctly.")
        return 0
    else:
        print("✗ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
