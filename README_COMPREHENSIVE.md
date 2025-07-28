# tkaria11y - Comprehensive Accessibility Framework for Tkinter

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![WCAG Compliance](https://img.shields.io/badge/WCAG-2.1%20AAA-brightgreen.svg)](https://www.w3.org/WAI/WCAG21/quickref/)

A comprehensive accessibility framework for Tkinter applications that provides **full WCAG 2.1 compliance** with complete ARIA support, platform-specific screen reader integration, braille display support, audio accessibility, and much more.

## 🌟 Key Features

### **Complete WCAG 2.1 Compliance**
- ✅ **Level A, AA, and AAA** compliance validation
- ✅ **Automated accessibility testing** and reporting
- ✅ **Auto-fix** common accessibility issues
- ✅ **Real-time compliance monitoring**

### **Full ARIA Implementation**
- 🎯 **Complete ARIA roles, properties, and states**
- 🎯 **Automatic role detection** for all widgets
- 🎯 **ARIA validation** and error reporting
- 🎯 **Custom ARIA property support**

### **Platform-Specific Screen Reader Integration**
- 🖥️ **Windows**: UI Automation (UIA) for NVDA, JAWS, Narrator
- 🐧 **Linux**: AT-SPI for Orca and other screen readers
- 🍎 **macOS**: VoiceOver integration via Cocoa accessibility
- 🔄 **Automatic platform detection** and adaptation

### **Advanced Audio Accessibility**
- 🔊 **Spatial audio positioning** for UI elements
- 🔊 **Customizable audio cues** for all interactions
- 🔊 **Multiple audio backends** (pygame, PyAudio, platform-specific)
- 🔊 **Audio feedback** for focus, clicks, state changes

### **Braille Display Support**
- ⠃ **Multi-vendor braille display** compatibility
- ⠃ **Real-time braille updates** with focus tracking
- ⠃ **Cursor routing** and navigation support
- ⠃ **Grade 1 and Grade 2** braille translation

### **Visual Accessibility**
- 🎨 **High contrast themes** with WCAG-compliant ratios
- 🎨 **Dyslexic-friendly fonts** (OpenDyslexic, Atkinson Hyperlegible)
- 🎨 **Color blindness support** with safe color palettes
- 🎨 **Scalable text** and UI elements
- 🎨 **Focus indicators** with customizable styling

### **Advanced Focus Management**
- ⌨️ **Logical tab order** with automatic detection
- ⌨️ **Arrow key navigation** for appropriate contexts
- ⌨️ **Focus trapping** for modal dialogs
- ⌨️ **Focus history** and restoration
- ⌨️ **Keyboard shortcuts** and accelerators

### **Text-to-Speech Integration**
- 🗣️ **Multi-platform TTS** with voice selection
- 🗣️ **Priority-based announcements** with debouncing
- 🗣️ **Context-aware speech** with widget information
- 🗣️ **Customizable speech rates** and volumes

### **Comprehensive Widget Support**
- 🧩 **All Tkinter widgets** with accessibility enhancements
- 🧩 **TTK widget support** with native theming
- 🧩 **CustomTkinter compatibility** for modern UIs
- 🧩 **Drop-in replacements** for existing widgets

## 🚀 Quick Start

### Basic Usage

```python
import tkinter as tk
from tkaria11y import AccessibleApp, AccessibleButton, AccessibleEntry, setup_full_accessibility

# Create accessible application
root = AccessibleApp()
root.title("My Accessible App")

# Set up full accessibility features
setup_full_accessibility(
    root,
    high_contrast=True,      # Enable high contrast theme
    dyslexic_font=True,      # Use dyslexic-friendly font
    enable_audio=True,       # Enable audio cues
    enable_braille=True,     # Enable braille support
    enable_spatial_audio=True # Enable 3D audio positioning
)

# Create accessible widgets
button = AccessibleButton(
    root,
    text="Click Me",
    accessible_name="Main action button",
    accessible_description="Performs the primary action when clicked",
    accessible_role="button"
)
button.pack(pady=10)

entry = AccessibleEntry(
    root,
    accessible_name="Name input field",
    accessible_description="Enter your full name here",
    accessible_role="textbox"
)
entry.pack(pady=10)

# Run accessibility audit
from tkaria11y import quick_accessibility_audit
audit_results = quick_accessibility_audit(root)
print(f"Accessibility Score: {audit_results['compliance_score']}/100")

root.mainloop()
```

## 📦 Installation

### Basic Installation
```bash
pip install tkaria11y
```

### Platform-Specific Features
```bash
# Windows (UI Automation support)
pip install tkaria11y[windows]

# Linux (AT-SPI support)  
pip install tkaria11y[linux]

# macOS (VoiceOver support)
pip install tkaria11y[macos]

# Enhanced features (CustomTkinter, image processing)
pip install tkaria11y[enhanced]

# Everything (all platforms and features)
pip install tkaria11y[full]
```

### Development Installation
```bash
git clone https://github.com/your-repo/tkaria11y.git
cd tkaria11y
pip install -e .[dev]
```

## 🧪 Testing Your Application

### Quick Accessibility Audit
```python
from tkaria11y import quick_accessibility_audit

# Get quick overview
results = quick_accessibility_audit(root)
print(f"Compliance Score: {results['compliance_score']}/100")
print(f"Issues Found: {results['total_issues']}")
```

### Comprehensive Testing
```python
from tkaria11y import (
    run_accessibility_audit,
    test_keyboard_navigation,
    test_screen_reader_compatibility,
    auto_fix_accessibility_issues
)

# Full accessibility audit
report = run_accessibility_audit(root)

# Test keyboard navigation
nav_issues = test_keyboard_navigation(root)

# Test screen reader compatibility
sr_report = test_screen_reader_compatibility(root)

# Auto-fix common issues
fixed_count = auto_fix_accessibility_issues(root)
```

## 🎯 WCAG 2.1 Compliance

tkaria11y helps you achieve full WCAG 2.1 compliance across all levels:

### Level A (Minimum)
- ✅ Keyboard accessibility
- ✅ Text alternatives
- ✅ Color independence
- ✅ Focus management

### Level AA (Standard)
- ✅ 4.5:1 contrast ratios
- ✅ Resizable text (200%)
- ✅ Keyboard shortcuts
- ✅ Focus indicators

### Level AAA (Enhanced)
- ✅ 7:1 contrast ratios
- ✅ Context help
- ✅ Error prevention
- ✅ Advanced navigation

## 🔧 Configuration

### Audio Settings
```python
from tkaria11y import setup_audio_accessibility, set_audio_volume

# Configure audio
setup_audio_accessibility(
    root,
    enable_spatial=True,
    master_volume=0.8,
    cue_volume=0.6
)

# Adjust volumes
set_audio_volume(master_volume=0.7, cue_volume=0.5)
```

### Visual Settings
```python
from tkaria11y import (
    HighContrastTheme,
    set_dyslexic_font,
    apply_colorblind_safe_theme
)

# Apply high contrast
HighContrastTheme.apply(root)

# Use dyslexic-friendly font
set_dyslexic_font(root, size=14)

# Apply colorblind-safe colors
apply_colorblind_safe_theme(root, "deuteranopia")
```

### Braille Settings
```python
from tkaria11y import setup_braille_support, get_braille_manager

# Set up braille
setup_braille_support(root)

# Configure braille manager
braille_manager = get_braille_manager()
braille_manager.set_grade(2)  # Grade 2 braille
braille_manager.set_cursor_settings(show=True, blink=True)
```

## 📚 Widget Reference

### Accessible Widgets
All widgets support these accessibility properties:

```python
widget = AccessibleButton(
    parent,
    text="Button Text",
    accessible_name="Descriptive name for screen readers",
    accessible_description="Detailed description of purpose",
    accessible_role="button",  # ARIA role
    accessible_value="current value",  # For inputs
    live_region="polite"  # For dynamic content
)
```

### Available Widgets
- `AccessibleButton`, `AccessibleTTKButton`
- `AccessibleEntry`, `AccessibleTTKEntry`
- `AccessibleLabel`, `AccessibleTTKLabel`
- `AccessibleCheckbutton`, `AccessibleTTKCheckbutton`
- `AccessibleRadiobutton`, `AccessibleTTKRadiobutton`
- `AccessibleScale`, `AccessibleTTKScale`
- `AccessibleListbox`, `AccessibleTreeview`
- `AccessibleFrame`, `AccessibleTTKFrame`
- `AccessibleNotebook`, `AccessibleTTKNotebook`
- `AccessibleCombobox`, `AccessibleTTKCombobox`
- And many more...

## 🔍 Debugging and Validation

### Real-time Validation
```python
from tkaria11y import AccessibilityValidator, ValidationLevel

# Create validator
validator = AccessibilityValidator(ValidationLevel.AA)

# Validate application
issues = validator.validate_application(root)

# Generate detailed report
report = validator.generate_report()
print(f"Compliance Score: {report['compliance_score']}/100")
```

### Debug Mode
```python
# Enable debug mode for detailed logging
import tkaria11y
tkaria11y.set_debug_mode(True)

# This will log all accessibility events and validations
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
git clone https://github.com/your-repo/tkaria11y.git
cd tkaria11y
pip install -e .[dev]
pytest  # Run tests
```

## 📖 Documentation

- [API Reference](docs/api.md)
- [WCAG Compliance Guide](docs/wcag.md)
- [Platform Integration](docs/platforms.md)
- [Widget Gallery](docs/widgets.md)
- [Testing Guide](docs/testing.md)
- [Migration Guide](docs/migration.md)

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/tkaria11y/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/tkaria11y/discussions)
- **Documentation**: [Full Documentation](https://tkaria11y.readthedocs.io)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Web Content Accessibility Guidelines (WCAG) 2.1
- WAI-ARIA Authoring Practices Guide
- Screen reader communities (NVDA, JAWS, Orca, VoiceOver users)
- Accessibility testing tools and validators
- The Python and Tkinter communities

---

**Made with ❤️ for accessibility and inclusion**