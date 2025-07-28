# tkaria11y Type Stub Generation System

This document describes the comprehensive type stub generation system for the tkaria11y accessibility framework.

## Overview

The tkaria11y package includes a sophisticated type stub generation system that provides full IDE support with type checking, autocomplete, and comprehensive documentation. The system consists of:

1. **Pre-written comprehensive stubs** in the `stubs/` directory
2. **Automated stub generator** (`tkaria11y-stubgen`) for dynamic generation
3. **Widget-specific generator** (`tkaria11y-generate-widget-stubs`) for quick updates
4. **PEP 561 compliance** with `py.typed` marker

## Available Stub Files

### Core Module Stubs
- `__init__.pyi` - Main module exports and global functions
- `app.pyi` - AccessibleApp class and application utilities
- `widgets.pyi` - All accessible widget classes with full inheritance
- `themes.pyi` - Theme management and accessibility themes
- `utils.pyi` - Utility functions for accessibility operations

### Advanced Feature Stubs
- `accessibility_validator.pyi` - WCAG compliance validation system
- `aria_compliance.pyi` - Complete ARIA roles, properties, and validation
- `braille_support.pyi` - Braille display integration and management
- `audio_accessibility.pyi` - Audio cues, spatial audio, and sound management
- `mixins.pyi` - Comprehensive accessibility mixins for custom widgets

## Stub Generation Tools

### 1. Comprehensive Stub Generator (`tkaria11y-stubgen`)

The main stub generator creates complete type stubs for all modules:

```bash
# Generate all stubs to default location
tkaria11y-stubgen

# Generate to custom directory
tkaria11y-stubgen -o my_stubs

# Generate and validate with mypy
tkaria11y-stubgen --validate

# Create py.typed marker file
tkaria11y-stubgen --py-typed

# Verbose output for debugging
tkaria11y-stubgen --verbose
```

**Features:**
- ✅ Analyzes actual implementation using introspection
- ✅ Generates accurate type annotations for all public APIs
- ✅ Handles complex inheritance hierarchies
- ✅ Includes comprehensive docstrings
- ✅ Validates generated stubs with mypy
- ✅ Creates PEP 561 compliant package structure

### 2. Widget-Specific Generator (`tkaria11y-generate-widget-stubs`)

Quick generator for widget stubs based on `_WIDGET_MAP`:

```bash
# Generate only widget stubs
tkaria11y-generate-widget-stubs
```

**Use Cases:**
- During active widget development
- Quick updates when adding new widgets
- Lightweight stub generation for CI/CD

### 3. Manual Stub Creation

For specialized cases, stubs can be manually created or edited:

```python
# Example manual stub
class CustomAccessibleWidget(tk.Widget):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        accessible_name: str,
        custom_property: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...
    
    def custom_method(self, param: str) -> bool: ...
```

## Stub Quality and Coverage

### Type Annotation Coverage
- **100% Public API Coverage**: All public classes, functions, and constants
- **Accurate Parameter Types**: Proper typing for all parameters and returns
- **Generic Type Support**: Full support for generic types and type variables
- **Union Types**: Proper handling of optional and union parameters
- **Callable Types**: Accurate callback and function parameter typing

### Accessibility-Specific Features
- **ARIA Compliance**: Complete ARIA role and property definitions
- **Widget Inheritance**: Correct inheritance from Tkinter/TTK widgets
- **Platform Integration**: Windows, macOS, and Linux accessibility APIs
- **Assistive Technology**: TTS, braille, screen reader integration
- **Validation Framework**: WCAG compliance checking and auto-fixing

### IDE Integration
- **VS Code**: Full IntelliSense with Pylance
- **PyCharm**: Complete type checking and autocomplete
- **mypy**: Static type analysis and error detection
- **Other IDEs**: Any IDE supporting PEP 484 type hints

## Installation and Usage

### Package Installation
When installing tkaria11y, stubs are automatically included:

```bash
pip install tkaria11y
```

The package includes:
- `py.typed` marker for PEP 561 compliance
- Pre-generated stub files in the package
- Console scripts for stub generation

### Development Setup
For development with full type checking:

```bash
# Install in development mode
pip install -e .

# Generate fresh stubs
tkaria11y-stubgen --py-typed

# Validate stubs
tkaria11y-stubgen --validate
```

### IDE Configuration

#### VS Code
Add to `settings.json`:
```json
{
    "python.analysis.typeCheckingMode": "strict",
    "python.analysis.autoImportCompletions": true,
    "python.analysis.stubPath": "./stubs"
}
```

#### PyCharm
1. Settings → Project → Python Interpreter
2. Add stubs directory to interpreter paths
3. Enable type checking in inspections

#### mypy Configuration
Add to `pyproject.toml`:
```toml
[tool.mypy]
mypy_path = "stubs"
strict = true
warn_return_any = true
warn_unused_configs = true
```

## Example Usage with Type Support

### Basic Widget Creation
```python
from tkaria11y import AccessibleApp, AccessibleButton
from tkaria11y.widgets import AccessibleEntry

# Full type checking and autocomplete
app: AccessibleApp = AccessibleApp(
    title="My Accessible App",
    high_contrast=True,
    dyslexic_font=True
)

button: AccessibleButton = AccessibleButton(
    app,
    text="Click Me",
    accessible_name="Main action button",
    accessible_description="Performs the primary action"
)

entry: AccessibleEntry = AccessibleEntry(
    app,
    accessible_name="User input",
    accessible_role="textbox"
)
```

### Advanced Accessibility Features
```python
from tkaria11y.accessibility_validator import (
    AccessibilityValidator, 
    ValidationLevel,
    IssueSeverity
)
from tkaria11y.braille_support import BrailleManager
from tkaria11y.audio_accessibility import AudioAccessibilityManager

# Type-safe accessibility validation
validator: AccessibilityValidator = AccessibilityValidator(
    level=ValidationLevel.AA
)
issues = validator.validate_application(app)

# Filter issues by severity
critical_issues = [
    issue for issue in issues 
    if issue.severity == IssueSeverity.CRITICAL
]

# Braille and audio support with full typing
braille: BrailleManager = BrailleManager()
audio: AudioAccessibilityManager = AudioAccessibilityManager(app)
```

### Theme Management
```python
from tkaria11y.themes import (
    HighContrastTheme,
    ThemeManager,
    FontManager
)

# Type-safe theme operations
theme_manager: ThemeManager = ThemeManager(app)
theme_manager.apply_theme("high_contrast", variant="dark")

font_manager: FontManager = FontManager(app)
font_manager.set_font_family("OpenDyslexic")
font_manager.increase_font_size(2)
```

## Validation and Testing

### Automated Validation
The stub generator includes built-in validation:

```bash
# Validate all generated stubs
tkaria11y-stubgen --validate

# Manual validation with mypy
mypy --strict stubs/
```

### Runtime Testing
Stubs are validated against the actual implementation:

```python
# Test stub accuracy
import tkaria11y
from tkaria11y.widgets import AccessibleButton

# This should work without type errors
app = tkaria11y.AccessibleApp()
button = AccessibleButton(app, text="Test")
```

### Continuous Integration
Include stub validation in CI/CD:

```yaml
# GitHub Actions example
- name: Validate Type Stubs
  run: |
    pip install mypy
    tkaria11y-stubgen --validate
    mypy --strict stubs/
```

## Troubleshooting

### Common Issues

#### Stubs Not Recognized
```bash
# Ensure py.typed marker exists
ls tkaria11y/py.typed

# Regenerate stubs
tkaria11y-stubgen --py-typed

# Check IDE settings
```

#### Type Errors
```bash
# Update stubs to match implementation
tkaria11y-stubgen

# Validate syntax
mypy stubs/

# Check for import issues
python -c "import tkaria11y; print('OK')"
```

#### Missing Autocomplete
```bash
# Restart IDE after generating stubs
# Check Python interpreter settings
# Verify stub files are in correct location
```

### Debug Mode
Enable verbose output for troubleshooting:

```bash
tkaria11y-stubgen --verbose
```

This provides detailed information about:
- Module discovery and analysis
- Type annotation generation
- Validation results
- File creation and updates

## Contributing to Stubs

### Adding New Features
When adding new functionality to tkaria11y:

1. **Implement the feature** in the main codebase
2. **Regenerate stubs**: `tkaria11y-stubgen`
3. **Validate types**: `tkaria11y-stubgen --validate`
4. **Test IDE support**: Verify autocomplete works
5. **Update documentation**: Include type examples

### Manual Stub Updates
For complex cases requiring manual intervention:

1. Edit the appropriate `.pyi` file
2. Follow PEP 484 standards
3. Use `...` for function bodies
4. Include comprehensive docstrings
5. Validate with mypy: `mypy stubs/filename.pyi`

### Best Practices
- **Keep stubs in sync** with implementation
- **Use specific types** instead of `Any` when possible
- **Document complex types** with comments
- **Test with multiple IDEs** to ensure compatibility
- **Validate regularly** during development

## Future Enhancements

### Planned Features
- **Incremental stub generation** for faster updates
- **IDE plugin integration** for real-time stub updates
- **Advanced type inference** using static analysis
- **Stub versioning** for backward compatibility
- **Performance optimization** for large codebases

### Community Contributions
- Submit stub improvements via pull requests
- Report type annotation issues
- Suggest new validation rules
- Share IDE configuration examples

## Support and Resources

### Documentation
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [PEP 561 - Distributing Type Information](https://www.python.org/dev/peps/pep-0561/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Pylance Documentation](https://github.com/microsoft/pylance-release)

### Getting Help
1. Check this documentation
2. Regenerate stubs: `tkaria11y-stubgen`
3. Validate with mypy: `mypy stubs/`
4. Report issues on GitHub with:
   - Python version
   - IDE and version
   - Error messages
   - Minimal reproduction example

The tkaria11y stub generation system provides comprehensive type support for building accessible Tkinter applications with full IDE integration and static type checking.