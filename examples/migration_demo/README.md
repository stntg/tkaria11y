# tkaria11y Migration Tool Demo

This directory demonstrates how the `tkaria11y-migrate` tool works to convert existing tkinter applications to use accessible widgets.

## Files in this demo:

- **`before_migration.py`** - A typical tkinter calculator app before migration
- **`simple_form.py`** - A form with various tkinter widgets before migration  
- **`demo_migration.py`** - Script that demonstrates the migration process
- **`README.md`** - This file

## What the Migration Tool Does

The migration tool automatically transforms your existing tkinter code to use tkaria11y's accessible widgets:

### Widget Transformations

| Before (tkinter) | After (tkaria11y) |
|------------------|-------------------|
| `tk.Button` | `AccessibleButton` |
| `tk.Entry` | `AccessibleEntry` |
| `tk.Label` | `AccessibleLabel` |
| `tk.Frame` | `AccessibleFrame` |
| `tk.Checkbutton` | `AccessibleCheckbutton` |
| `tk.Radiobutton` | `AccessibleRadiobutton` |
| `tk.Scale` | `AccessibleScale` |
| `tk.Listbox` | `AccessibleListbox` |

### Automatic Enhancements

1. **Import Management**: Adds necessary imports from `tkaria11y.widgets`
2. **Accessible Names**: Automatically adds `accessible_name` parameters based on existing `text=` values
3. **Preserves Functionality**: All existing behavior is maintained
4. **Screen Reader Support**: Widgets become compatible with screen readers
5. **TTS Integration**: Widgets can announce themselves when focused

## Running the Demo

### Option 1: Run the demonstration script
```bash
cd examples/migration_demo
python demo_migration.py
```

This will:
- Process the example files
- Show you what changes were made
- Create `after_*.py` files with the migrated code
- Display a summary of transformations

### Option 2: Use the actual migration tool
```bash
# From the project root
python -m tkaria11y.scripts.migrate examples/migration_demo/before_migration.py

# Or migrate an entire directory
python -m tkaria11y.scripts.migrate examples/migration_demo/ --interactive
```

## Example Transformation

### Before Migration:
```python
import tkinter as tk

root = tk.Tk()
button = tk.Button(root, text="Click Me", command=some_function)
entry = tk.Entry(root)
label = tk.Label(root, text="Enter your name:")
```

### After Migration:
```python
import tkinter as tk
from tkaria11y.widgets import AccessibleButton, AccessibleEntry, AccessibleLabel

root = tk.Tk()
button = AccessibleButton(root, accessible_name="Click Me", text="Click Me", command=some_function)
entry = AccessibleEntry(root, accessible_name="Name input field")
label = AccessibleLabel(root, accessible_name="Enter your name:", text="Enter your name:")
```

## Benefits After Migration

1. **Screen Reader Compatibility**: All widgets work with NVDA, JAWS, and other screen readers
2. **Text-to-Speech**: Widgets announce themselves when focused
3. **Better Navigation**: Improved keyboard navigation and focus management
4. **Accessibility Standards**: Follows WCAG guidelines
5. **No Functionality Loss**: Your app works exactly the same, just more accessible

## Interactive Mode

Use `--interactive` flag to review each change before applying:

```bash
python -m tkaria11y.scripts.migrate myapp.py --interactive
```

This will:
- Show you each proposed change
- Ask for confirmation before applying
- Let you skip changes you don't want

## Testing After Migration

After migration, test your application to ensure:

1. All functionality still works as expected
2. Screen readers can access all controls
3. Keyboard navigation works properly
4. TTS announcements are helpful (not too verbose)

## Customization

You can customize the migration process by:

1. **Config Files**: Use `--config` to specify custom accessible names
2. **Manual Review**: Always review the changes before committing
3. **Incremental Migration**: Migrate one file at a time for large projects

## Next Steps

After migration:

1. Test your application thoroughly
2. Consider enabling additional accessibility features:
   - High contrast themes
   - Dyslexic-friendly fonts
   - Inspector tool for debugging
3. Add more descriptive `accessible_name` values where needed
4. Consider using `AccessibleApp` instead of `tk.Tk()` for additional features