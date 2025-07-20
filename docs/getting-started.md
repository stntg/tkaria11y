# Getting Started with tkaria11y

## Installation

### From PyPI (Recommended)

```bash
# Install the latest stable release
pip install tkaria11y

# Install with development tools
pip install "tkaria11y[dev]"
```

### From Source

```bash
# Clone the repository
git clone https://github.com/stntg/tkaria11y.git
cd tkaria11y

# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### Basic Application

```python
from tkaria11y import AccessibleApp
from tkaria11y.widgets import AccessibleButton, AccessibleEntry, AccessibleLabel

# Create accessible app
app = AccessibleApp(
    title="My Accessible App",
    high_contrast=True,
    dyslexic_font=True,
    enable_inspector=True
)

# Add accessible widgets
label = AccessibleLabel(
    app,
    text="Enter your name:",
    accessible_name="Name input label"
)
label.pack(pady=5)

entry = AccessibleEntry(
    app,
    accessible_name="Name input field",
    accessible_description="Enter your full name here"
)
entry.pack(pady=5)

def submit():
    name = entry.get()
    print(f"Hello, {name}!")

button = AccessibleButton(
    app,
    text="Submit",
    accessible_name="Submit button",
    command=submit
)
button.pack(pady=10)

app.mainloop()
```

### Key Features Demonstrated

- **AccessibleApp**: Main application class with built-in accessibility features
- **Accessible Widgets**: Drop-in replacements for standard Tkinter widgets
- **ARIA Metadata**: `accessible_name` and `accessible_description` for screen readers
- **High Contrast**: Automatic high-contrast theme application
- **Dyslexic Font**: OpenDyslexic font with fallbacks
- **Inspector**: F2 to toggle accessibility debugging

## Widget Reference

### Available Widgets

| Widget | Standard Equivalent | Purpose |
|--------|-------------------|---------|
| `AccessibleButton` | `tk.Button` | Clickable buttons with TTS feedback |
| `AccessibleEntry` | `tk.Entry` | Text input fields with accessibility metadata |
| `AccessibleLabel` | `tk.Label` | Text labels with proper ARIA roles |
| `AccessibleCheckbutton` | `tk.Checkbutton` | Checkboxes with state announcements |
| `AccessibleRadiobutton` | `tk.Radiobutton` | Radio buttons with group navigation |
| `AccessibleScale` | `tk.Scale` | Sliders with value announcements |
| `AccessibleListbox` | `tk.Listbox` | Lists with keyboard navigation |
| `AccessibleFrame` | `tk.Frame` | Container widgets with grouping |

### Widget Parameters

All accessible widgets support these additional parameters:

```python
widget = AccessibleWidget(
    parent,
    # Standard Tkinter parameters...
    text="Button Text",
    
    # Accessibility parameters
    accessible_name="Screen reader announcement",
    accessible_description="Additional context",
    accessible_role="button",  # Usually auto-set
    enable_tts=True  # Enable/disable TTS for this widget
)
```

## Accessibility Features

### Text-to-Speech (TTS)

```python
from tkaria11y import speak, tts

# Direct speech
speak("Hello, world!")

# Configure TTS settings
tts.set_property('rate', 150)    # Words per minute
tts.set_property('volume', 0.8)  # Volume (0.0 to 1.0)
tts.set_property('voice', voice_id)  # Specific voice
```

### High-Contrast Themes

```python
from tkaria11y.themes import HighContrastTheme

# Apply theme to specific widget
theme = HighContrastTheme()
theme.apply(widget)

# Theme colors
print(theme.bg_color)      # Background
print(theme.fg_color)      # Foreground/text
print(theme.select_color)  # Selection highlight
print(theme.focus_color)   # Focus indicator
```

### Dyslexic-Friendly Fonts

```python
from tkaria11y.themes import set_dyslexic_font

# Apply to specific widget
set_dyslexic_font(widget)

# Apply to entire app (done automatically in AccessibleApp)
app = AccessibleApp(dyslexic_font=True)
```

### Runtime Inspector

Press **F2** in any tkaria11y application to open the accessibility inspector:

- **Widget Tree**: Hierarchical view of all accessible widgets
- **Metadata Panel**: Shows accessible names, roles, and descriptions
- **Focus Tracking**: Highlights currently focused widget
- **Navigation Testing**: Verify tab order and keyboard shortcuts

## Best Practices

### Accessible Names

```python
# Good: Descriptive and specific
AccessibleButton(
    app,
    text="Save",
    accessible_name="Save document button"
)

# Better: Include context
AccessibleButton(
    app,
    text="Save",
    accessible_name="Save current document to file"
)

# Best: Include state when relevant
AccessibleButton(
    app,
    text="Save",
    accessible_name="Save document (unsaved changes)"
)
```

### Descriptions

```python
# Use descriptions for additional context
AccessibleEntry(
    app,
    accessible_name="Password field",
    accessible_description="Must be at least 8 characters with numbers and symbols"
)
```

### Keyboard Navigation

```python
# Ensure logical tab order
entry1.pack()
entry2.pack()
button.pack()

# Set initial focus
entry1.focus_set()

# Custom tab order if needed
from tkaria11y.utils import configure_focus_traversal
configure_focus_traversal([entry1, entry2, button])
```

### Form Layouts

```python
# Group related controls
form_frame = AccessibleFrame(
    app,
    accessible_name="User information form"
)

# Label-input pairs
name_label = AccessibleLabel(
    form_frame,
    text="Name:",
    accessible_name="Name field label"
)
name_entry = AccessibleEntry(
    form_frame,
    accessible_name="Name input field"
)

# Use grid for better layout
name_label.grid(row=0, column=0, sticky="w")
name_entry.grid(row=0, column=1, padx=5)
```

## Migration from Standard Tkinter

### Using the Migration Tool

```bash
# Interactive migration
tkaria11y-migrate myapp.py --interactive

# Batch migration
tkaria11y-migrate ./src --batch

# With custom configuration
tkaria11y-migrate ./app --config migration.yaml
```

### Manual Migration

1. **Replace imports**:
   ```python
   # Before
   import tkinter as tk
   from tkinter import ttk
   
   # After
   from tkaria11y import AccessibleApp
   from tkaria11y.widgets import AccessibleButton, AccessibleEntry
   ```

2. **Update app creation**:
   ```python
   # Before
   root = tk.Tk()
   
   # After
   app = AccessibleApp(
       title="My App",
       high_contrast=True,
       dyslexic_font=True
   )
   ```

3. **Replace widgets**:
   ```python
   # Before
   button = tk.Button(root, text="Click me")
   
   # After
   button = AccessibleButton(
       app,
       text="Click me",
       accessible_name="Click me button"
   )
   ```

4. **Add accessibility metadata**:
   ```python
   # Add accessible names and descriptions
   entry = AccessibleEntry(
       app,
       accessible_name="Email address field",
       accessible_description="Enter your email address"
   )
   ```

## Testing Accessibility

### Built-in Testing

```bash
# Run accessibility test suite
python a11y_test_suite/run_tests.py

# Interactive widget testing
python a11y_test_suite/interactive/widget_test_app.py

# TTS performance testing
python a11y_test_suite/performance/tts_performance.py
```

### Manual Testing

1. **Keyboard Navigation**: Test Tab/Shift-Tab traversal
2. **Screen Reader**: Test with NVDA, JAWS, or VoiceOver
3. **High Contrast**: Verify visibility in high-contrast mode
4. **TTS**: Ensure announcements are clear and helpful
5. **Inspector**: Use F2 to verify metadata and structure

### Automated Testing

```python
import pytest
from tkaria11y import AccessibleApp
from tkaria11y.widgets import AccessibleButton

def test_button_accessibility():
    app = AccessibleApp()
    button = AccessibleButton(
        app,
        text="Test",
        accessible_name="Test button"
    )
    
    # Test accessibility attributes
    assert button.accessible_name == "Test button"
    assert button.accessible_role == "button"
    assert hasattr(button, 'speak_on_focus')
```

## Troubleshooting

### Common Issues

1. **TTS Not Working**:
   ```python
   # Check TTS engine
   from tkaria11y import tts
   print(tts.get_property('voices'))
   ```

2. **Fonts Not Loading**:
   ```python
   # Check font availability
   import tkinter.font as tkfont
   print(tkfont.families())
   ```

3. **Inspector Not Opening**:
   ```python
   # Ensure inspector is enabled
   app = AccessibleApp(enable_inspector=True)
   ```

### Getting Help

- **Documentation**: Check `docs/` directory
- **Examples**: See `examples/` for working code
- **Issues**: Report bugs on GitHub
- **Community**: Join discussions and ask questions

## Next Steps

- Explore the `examples/` directory for more complex applications
- Read the full API documentation in `docs/index.md`
- Check out the roadmap in `ROADMAP.md`
- Contribute to the project - see `CONTRIBUTING.md`