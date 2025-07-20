# tkaria11y Migration Tool - Complete Example

This document shows a complete example of what the `tkaria11y-migrate` tool does and how it transforms your tkinter applications to be accessible.

## What Just Happened?

We ran the migration tool on `test_file.py` and it automatically transformed the code:

### Before Migration

```python
#!/usr/bin/env python3
"""Test file for migration demonstration"""

import tkinter as tk

def create_simple_app():
    root = tk.Tk()
    root.title("Test App")
    
    # Simple widgets
    label = tk.Label(root, text="Hello World")
    entry = tk.Entry(root)
    button = tk.Button(root, text="Click Me")
    
    label.pack()
    entry.pack()
    button.pack()
    
    return root

if __name__ == "__main__":
    app = create_simple_app()
    app.mainloop()
```

### After Migration

```python
#!/usr/bin/env python3
"""Test file for migration demonstration"""

import tkinter as tk
from tkaria11y.widgets import AccessibleEntry, AccessibleButton, AccessibleLabel

def create_simple_app():
    root = tk.Tk()
    root.title("Test App")
    
    # Simple widgets
    label = AccessibleLabel(accessible_name="Hello World", root, text="Hello World")
    entry = AccessibleEntry(root)
    button = AccessibleButton(accessible_name="Click Me", root, text="Click Me")
    
    label.pack()
    entry.pack()
    button.pack()
    
    return root

if __name__ == "__main__":
    app = create_simple_app()
    app.mainloop()
```

## Key Changes Made

1. **Added Import**: `from tkaria11y.widgets import AccessibleEntry, AccessibleButton, AccessibleLabel`

2. **Widget Transformations**:
   - `tk.Label` → `AccessibleLabel` with `accessible_name="Hello World"`
   - `tk.Entry` → `AccessibleEntry`
   - `tk.Button` → `AccessibleButton` with `accessible_name="Click Me"`

3. **Automatic accessible_name Addition**: The tool detected `text="Hello World"` and `text="Click Me"` and automatically added corresponding `accessible_name` parameters.

## How to Use the Migration Tool

### Basic Usage

```bash
# Migrate a single file
python -m tkaria11y.scripts.migrate myapp.py

# Migrate all Python files in a directory
python -m tkaria11y.scripts.migrate ./my_project/

# Interactive mode (asks before each change)
python -m tkaria11y.scripts.migrate myapp.py --interactive
```

### Interactive Mode Example

```bash
$ python -m tkaria11y.scripts.migrate examples/migration_demo/test_file.py --interactive

Proposed changes for examples/migration_demo/test_file.py:
==================================================
Line 5:
  - 
  + from tkaria11y.widgets import AccessibleEntry, AccessibleButton, AccessibleLabel

Line 12:
  - label = tk.Label(root, text="Hello World")
  + label = AccessibleLabel(accessible_name="Hello World", root, text="Hello World")

Line 13:
  - entry = tk.Entry(root)
  + entry = AccessibleEntry(root)

Line 14:
  - button = tk.Button(root, text="Click Me")
  + button = AccessibleButton(accessible_name="Click Me", root, text="Click Me")

Apply these changes? [y/N]: y
✓ Updated examples/migration_demo/test_file.py
```

## What You Get After Migration

### 1. Screen Reader Compatibility

Your widgets now work with screen readers like NVDA, JAWS, and VoiceOver:

- Labels announce their text content
- Buttons announce their purpose
- Entry fields can be properly identified

### 2. Text-to-Speech Integration

When users focus on widgets, they hear audio announcements:

- Button focus: "Click Me, button"
- Label focus: "Hello World, label"
- Entry focus: "Text input field"

### 3. Better Keyboard Navigation

Enhanced keyboard support with proper focus management.

### 4. Preserved Functionality

All your existing code continues to work exactly the same - no breaking changes!

## Advanced Migration Examples

### Complex Form Migration

**Before:**

```python
import tkinter as tk

class UserForm:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_form()
    
    def setup_form(self):
        tk.Label(self.root, text="Name:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        
        tk.Label(self.root, text="Email:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()
        
        submit_btn = tk.Button(self.root, text="Submit", command=self.submit)
        submit_btn.pack()
```

**After Migration:**

```python
import tkinter as tk
from tkaria11y.widgets import AccessibleLabel, AccessibleEntry, AccessibleButton

class UserForm:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_form()
    
    def setup_form(self):
        AccessibleLabel(accessible_name="Name:", self.root, text="Name:").pack()
        self.name_entry = AccessibleEntry(self.root, accessible_name="Name input field")
        self.name_entry.pack()
        
        AccessibleLabel(accessible_name="Email:", self.root, text="Email:").pack()
        self.email_entry = AccessibleEntry(self.root, accessible_name="Email input field")
        self.email_entry.pack()
        
        submit_btn = AccessibleButton(accessible_name="Submit", self.root, text="Submit", command=self.submit)
        submit_btn.pack()
```

## Migration Tool Features

### Supported Widget Types

- ✅ `tk.Button` → `AccessibleButton`
- ✅ `tk.Label` → `AccessibleLabel`
- ✅ `tk.Entry` → `AccessibleEntry`
- ✅ `tk.Frame` → `AccessibleFrame`
- ✅ `tk.Checkbutton` → `AccessibleCheckbutton`
- ✅ `tk.Radiobutton` → `AccessibleRadiobutton`
- ✅ `tk.Scale` → `AccessibleScale`
- ✅ `tk.Listbox` → `AccessibleListbox`

### Smart Features

- **Automatic Import Management**: Adds only the imports you need
- **Text-Based accessible_name**: Extracts `accessible_name` from `text=` parameters
- **Preserves All Parameters**: Keeps all your existing widget configuration
- **Safe Transformation**: Only changes widget class names and adds accessibility

### What It Doesn't Change

- ❌ Your application logic
- ❌ Event handlers and callbacks
- ❌ Widget styling and appearance
- ❌ Layout management (pack, grid, place)
- ❌ Variable bindings and data flow

## Testing Your Migrated Application

After migration, test these aspects:

1. **Functionality**: Ensure all features work as before
2. **Screen Reader**: Test with NVDA or other screen readers
3. **Keyboard Navigation**: Tab through all controls
4. **TTS Announcements**: Listen to focus announcements

## Next Steps After Migration

1. **Review accessible_name Values**: Make them more descriptive if needed
2. **Add Missing accessible_name**: For Entry widgets without text labels
3. **Consider AccessibleApp**: Replace `tk.Tk()` with `AccessibleApp()` for additional features
4. **Enable Themes**: Add high-contrast or dyslexic-friendly options
5. **Use Inspector**: Enable the accessibility inspector for debugging

## Example: Full Application Migration

Here's how to migrate a complete application:

```bash
# 1. Backup your code
git commit -am "Before accessibility migration"

# 2. Run migration on your entire project
python -m tkaria11y.scripts.migrate ./src/ --interactive

# 3. Review changes
git diff

# 4. Test the application
python your_app.py

# 5. Commit the changes
git commit -am "Add accessibility with tkaria11y migration"
```

## Conclusion

The tkaria11y migration tool makes it easy to add accessibility to existing tkinter applications with minimal effort and zero breaking changes. Your users get a better experience, and you comply with accessibility standards - all with a single command!
