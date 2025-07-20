# tkaria11y

[![CI](https://github.com/stntg/tkaria11y/workflows/CI/badge.svg)](https://github.com/stntg/tkaria11y/actions/workflows/CI.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/stntg/tkaria11y/badge)](https://www.codefactor.io/repository/github/stntg/tkaria11y)
[![PyPI version](https://badge.fury.io/py/tkaria11y.svg)](https://badge.fury.io/py/tkaria11y)
[![Python versions](https://img.shields.io/pypi/pyversions/tkaria11y.svg)](https://pypi.org/project/tkaria11y/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/tkaria11y)](https://pepy.tech/project/tkaria11y)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Accessibility](https://img.shields.io/badge/accessibility-WCAG%202.1-blue.svg)](https://www.w3.org/WAI/WCAG21/quickref/)
[![Type checked](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy.readthedocs.io/)

tkaria11y is a Python framework for building fully accessible Tkinter applications—offering ARIA-style metadata, automatic text-to-speech feedback, keyboard navigation, high-contrast theming, and dyslexic-friendly fonts.

Whether you're crafting GUIs for the visually impaired, dyslexic users, screen-reader users, or simply building inclusive software, tkaria11y gives you a robust set of tools with minimal boilerplate.

---

## Features

- ✅ **Accessible Widget Classes**: Drop-in replacements for standard Tkinter widgets
  - `AccessibleButton`, `AccessibleEntry`, `AccessibleLabel`
  - `AccessibleCheckbutton`, `AccessibleRadiobutton`, `AccessibleScale`
  - `AccessibleListbox`, `AccessibleFrame`
- 🎙️ **Text-to-Speech Feedback**: Automatic announcements on focus and hover using pyttsx3
- 🔍 **ARIA-style Metadata**: `accessible_name`, `accessible_role`, `accessible_description`
- ⌨️ **Keyboard Navigation**: Enhanced Tab/Shift-Tab traversal with logical focus order
- 🎨 **High-Contrast Themes**: Built-in high-contrast themes for better visibility
- 🔤 **Dyslexic-Friendly Fonts**: OpenDyslexic font support with automatic fallbacks
- 🧪 **Runtime Inspector**: Press F2 to toggle accessibility inspector with widget tree
- 🛠️ **Type Stub Generator**: Full IDE support with `tkaria11y-stubgen` command
- 📦 **Migration Tool**: Convert existing Tkinter apps with `tkaria11y-migrate`
- 🧱 **Dynamic Widget Factory**: Extensible architecture for custom accessible widgets

---

## Installation

Install the stable release from PyPI:

```bash
pip install tkaria11y
```

Install optional dev tools (testing, type checking, stub generation):

```bash
pip install "tkaria11y[dev]"
```

---

## Quickstart

Here's a simple example to get you started:

```python
from tkaria11y import AccessibleApp
from tkaria11y.widgets import AccessibleButton, AccessibleEntry, AccessibleLabel

# Create accessible app with accessibility features enabled
app = AccessibleApp(
    title="My Accessible App",
    high_contrast=True,
    dyslexic_font=True,
    enable_inspector=True
)

# Add accessible widgets with proper ARIA metadata
title = AccessibleLabel(
    app,
    text="Welcome to tkaria11y",
    accessible_name="Application title",
    font=("Arial", 16, "bold")
)
title.pack(pady=10)

entry = AccessibleEntry(
    app,
    accessible_name="Name input field",
    accessible_description="Enter your name here",
    width=30
)
entry.pack(padx=10, pady=5)

def greet():
    name = entry.get().strip()
    if name:
        print(f"Hello, {name}!")

button = AccessibleButton(
    app,
    text="Greet",
    accessible_name="Greet button",
    accessible_description="Click to display greeting",
    command=greet
)
button.pack(padx=10, pady=10)

# Start the app
app.mainloop()
```

### Try it out

- **Tab/Shift-Tab** to navigate between controls
- **Focus events** trigger TTS announcements  
- **Press F2** to toggle the accessibility inspector
- **High contrast theme** and **dyslexic font** are automatically applied

## Runtime Inspector

Press **F2** to open the built-in accessibility inspector:

- 🔍 **Widget Hierarchy**: Visual tree of all accessible widgets
- 🎯 **Focus Tracking**: Highlights currently focused widget in real-time
- 📋 **Metadata Display**: Shows accessible names, roles, and descriptions
- 🔧 **Navigation Audit**: Helps verify proper Tab order and focus flow
- 📊 **Accessibility Stats**: Overview of widget accessibility coverage

Perfect for debugging accessibility issues and ensuring proper ARIA implementation.

---

## Developer Tools

### Generate Type Stubs

```bash
tkaria11y-stubgen
```

Automatically generates `stubs/widgets.pyi` for full IDE support with type checking and autocomplete.

### Migrate Existing Code

```bash
# Interactive migration with prompts
tkaria11y-migrate path/to/your/app.py --interactive

# Batch migration for multiple files
tkaria11y-migrate ./src --batch

# Use custom configuration
tkaria11y-migrate ./app --config migration.yaml
```

Converts standard Tkinter widgets to accessible versions with automatic import handling and `accessible_name` inference.

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tkaria11y

# Run specific test categories
pytest tests/test_widgets.py -v
```

### Lint & Format

```bash
# Format code
black .

# Check style
flake8 .

# Type checking
mypy tkaria11y
```

---

## Examples

Explore the `examples/` directory for comprehensive demos:

- **`minimal_app.py`**: Basic usage with essential features
- **`comprehensive_demo.py`**: All widgets and features showcase  
- **`theme_demo.py`**: High-contrast themes and font options
- **`inspector_demo.py`**: Runtime inspector demonstration
- **`migration_demo/`**: Before/after migration examples

Run any example:

```bash
python examples/minimal_app.py
```

---

## Documentation

- **API Reference**: See `docs/index.md` for detailed API documentation
- **Examples**: Comprehensive examples in the `examples/` directory
- **Type Stubs**: Generated stubs provide IDE support and type hints
- **Migration Guide**: See `examples/migration_demo/` for migration examples
- **Accessibility Testing**: Use the built-in inspector and test suite in `a11y_test_suite/`

Full documentation site coming soon at tkaria11y.readthedocs.io.

---

## Contributing

We welcome accessibility advocates, Tkinter hackers, and curious contributors of all skill levels.

- See CONTRIBUTING.md
- Run tests and generate stubs before submitting PRs
- Open issues for bugs, ideas, or widget requests
- Adhere to our Code of Conduct

---

## License

MIT © [Your Name]  
See LICENSE for details.

---

## Acknowledgements

Inspired by ARIA specs, WCAG principles, open-source accessibility tooling, and the Python community’s commitment to inclusion.

---

## Roadmap

Want to see where we're headed? Check out ROADMAP.md.
