# tkaria11y Documentation

## Overview

tkaria11y is a Python accessibility framework for building fully accessible Tkinter applications with ARIA-style metadata, automatic text-to-speech feedback, keyboard navigation, high-contrast theming, and dyslexic-friendly fonts.

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

- `AccessibleButton`
- `AccessibleEntry`
- `AccessibleLabel`
- `AccessibleCheckbutton`
- `AccessibleRadiobutton`
- `AccessibleScale`
- `AccessibleListbox`
- `AccessibleFrame`

## API Reference

### AccessibleApp

Main application class that extends `tk.Tk` with accessibility features.

**Parameters:**
- `title`: Window title
- `high_contrast`: Enable high-contrast theme
- `dyslexic_font`: Enable dyslexic-friendly fonts
- `scaling`: UI scaling factor
- `enable_inspector`: Enable F2 accessibility inspector

### Accessible Widgets

All accessible widgets support these parameters:
- `accessible_name`: Screen reader announcement text
- `accessible_role`: ARIA role (automatically set)
- `accessible_description`: Additional description

## Development Tools

### Generate Type Stubs
```bash
tkaria11y-stubgen
```

### Migrate Existing Code
```bash
tkaria11y-migrate path/to/your/app.py --interactive
```

### Run Tests
```bash
pytest
```