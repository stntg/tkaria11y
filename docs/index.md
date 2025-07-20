# tkaria11y Documentation

## Overview

tkaria11y is a comprehensive Python accessibility framework that transforms standard Tkinter applications into fully accessible, inclusive software. Built with ARIA principles and WCAG guidelines in mind, it provides automatic text-to-speech feedback, enhanced keyboard navigation, high-contrast theming, and dyslexic-friendly fonts.

### Key Benefits

- **Zero Boilerplate**: Drop-in replacements for standard Tkinter widgets
- **Screen Reader Ready**: Full compatibility with NVDA, JAWS, and VoiceOver
- **Developer Friendly**: Type hints, IDE support, and comprehensive testing
- **Production Ready**: Robust error handling and performance optimization

## Documentation Sections

- **[Getting Started](getting-started.md)**: Installation, quick start, and basic usage
- **[API Reference](#api-reference)**: Complete API documentation (below)
- **[Examples](../examples/)**: Working code examples and demos
- **[Migration Guide](getting-started.md#migration-from-standard-tkinter)**: Convert existing Tkinter apps
- **[Best Practices](getting-started.md#best-practices)**: Accessibility guidelines and tips
- **[Testing](getting-started.md#testing-accessibility)**: How to test accessibility features
- **[Roadmap](../ROADMAP.md)**: Future development plans

## Quick Start

```python
from tkaria11y import AccessibleApp
from tkaria11y.widgets import AccessibleButton, AccessibleEntry

# Create accessible app
app = AccessibleApp(
    title="My Accessible App",
    high_contrast=True,
    dyslexic_font=True,
    enable_inspector=True
)

# Create accessible widgets
entry = AccessibleEntry(app, accessible_name="Name field")
entry.pack(padx=10, pady=5)

button = AccessibleButton(app, text="Submit", accessible_name="Submit button")
button.pack(padx=10, pady=5)

app.mainloop()
```

## Features

- **Accessible Widgets**: Drop-in replacements for standard Tkinter widgets
- **Text-to-Speech**: Automatic announcements on focus and hover
- **ARIA Metadata**: `accessible_name`, `accessible_role`, `accessible_description`
- **Keyboard Navigation**: Enhanced Tab/Shift-Tab traversal
- **High Contrast**: Built-in high-contrast themes
- **Dyslexic Fonts**: OpenDyslexic font support with fallbacks
- **Runtime Inspector**: F2 to toggle accessibility inspector

## Available Widgets

All widgets are drop-in replacements for their standard Tkinter counterparts:

| Accessible Widget | Standard Widget | ARIA Role | TTS Support |
|-------------------|-----------------|-----------|-------------|
| `AccessibleButton` | `tk.Button` | `button` | ✅ |
| `AccessibleEntry` | `tk.Entry` | `textbox` | ✅ |
| `AccessibleLabel` | `tk.Label` | `label` | ✅ |
| `AccessibleCheckbutton` | `tk.Checkbutton` | `checkbox` | ✅ |
| `AccessibleRadiobutton` | `tk.Radiobutton` | `radio` | ✅ |
| `AccessibleScale` | `tk.Scale` | `slider` | ✅ |
| `AccessibleListbox` | `tk.Listbox` | `listbox` | ✅ |
| `AccessibleFrame` | `tk.Frame` | `group` | ✅ |

### Widget Features

- **Automatic ARIA Roles**: Each widget has appropriate semantic roles
- **Focus Management**: Enhanced focus indicators and logical tab order
- **TTS Integration**: Speaks accessible names and state changes
- **Keyboard Support**: Full keyboard navigation and activation

## API Reference

### AccessibleApp

Main application class that extends `tk.Tk` with comprehensive accessibility features.

```python
app = AccessibleApp(
    title="My App",
    high_contrast=True,
    dyslexic_font=True,
    scaling=1.2,
    enable_inspector=True
)
```

**Parameters:**
- `title` (str): Window title
- `high_contrast` (bool): Enable high-contrast theme (default: False)
- `dyslexic_font` (bool): Enable OpenDyslexic font (default: False)  
- `scaling` (float): UI scaling factor for better visibility (default: 1.0)
- `enable_inspector` (bool): Enable F2 accessibility inspector (default: True)

**Methods:**
- `apply_theme()`: Apply current theme settings
- `toggle_inspector()`: Show/hide accessibility inspector
- `get_focused_widget()`: Get currently focused accessible widget

### Accessible Widgets

All accessible widgets inherit from their standard Tkinter counterparts and add accessibility features:

```python
widget = AccessibleButton(
    parent,
    text="Click me",
    accessible_name="Submit button",
    accessible_description="Submits the form data",
    command=my_function
)
```

**Common Parameters:**
- `accessible_name` (str): Primary text announced by screen readers
- `accessible_role` (str): ARIA role (automatically set based on widget type)
- `accessible_description` (str): Additional descriptive text
- `enable_tts` (bool): Enable text-to-speech for this widget (default: True)

**Accessibility Events:**
- `<FocusIn>`: Announces accessible_name via TTS
- `<Enter>`: Announces description on hover (if available)
- `<KeyPress>`: Enhanced keyboard interaction

## Advanced Features

### Text-to-Speech Engine

```python
from tkaria11y import speak, tts

# Direct speech
speak("Hello, world!")

# Configure TTS engine
tts.set_property('rate', 150)  # Words per minute
tts.set_property('volume', 0.8)  # Volume level
```

### High-Contrast Themes

```python
from tkaria11y.themes import HighContrastTheme

# Apply to specific widget
theme = HighContrastTheme()
theme.apply(widget)

# Available theme colors
theme.bg_color      # Background color
theme.fg_color      # Foreground/text color  
theme.select_color  # Selection highlight
theme.focus_color   # Focus indicator
```

### Runtime Inspector

The accessibility inspector provides real-time debugging:

- **F2**: Toggle inspector window
- **Widget Tree**: Hierarchical view of all accessible widgets
- **Metadata Panel**: Shows accessible_name, role, description
- **Focus Tracking**: Highlights currently focused widget
- **Navigation Testing**: Verify tab order and keyboard navigation

### Migration Tool

Convert existing Tkinter applications:

```bash
# Interactive mode with prompts
tkaria11y-migrate myapp.py --interactive

# Batch conversion
tkaria11y-migrate ./src --batch

# Custom configuration
tkaria11y-migrate ./app --config config.yaml
```

**Migration Features:**
- Automatic import handling
- Widget replacement (Button → AccessibleButton)
- accessible_name inference from text= parameters
- Preservation of existing functionality
- Backup creation

## Development Tools

### Generate Type Stubs
```bash
tkaria11y-stubgen
```
Creates comprehensive type stubs for IDE support and type checking.

### Run Tests
```bash
# All tests
pytest

# Specific test suites
pytest tests/test_widgets.py
pytest a11y_test_suite/

# With coverage
pytest --cov=tkaria11y --cov-report=html
```

### Accessibility Testing

Use the comprehensive test suite:

```bash
# Run accessibility compliance tests
python a11y_test_suite/run_tests.py

# Interactive widget testing
python a11y_test_suite/interactive/widget_test_app.py

# TTS performance testing  
python a11y_test_suite/performance/tts_performance.py
```