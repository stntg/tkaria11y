# Migration Script Fix - Black Formatting Issues

## The Problem

Yes, there **was** an issue with the migration script that caused the black formatting failures. The script was generating syntactically invalid Python code.

### Root Cause

The migration script in `tkaria11y/scripts/migrate.py` was inserting the `accessible_name` parameter at the **wrong position** in the function call.

#### What the script was doing (WRONG)

```python
# Original tkinter code:
label = tk.Label(root, text="Hello World")

# Migration script output (INVALID SYNTAX):
label = AccessibleLabel(accessible_name="Hello World", root, text="Hello World")
#                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ^^^^
#                      keyword argument                 positional argument
```

This violates Python's syntax rule: **positional arguments cannot follow keyword arguments**.

#### What it should do (CORRECT)

```python
# Original tkinter code:
label = tk.Label(root, text="Hello World")

# Fixed migration script output (VALID SYNTAX):
label = AccessibleLabel(root, accessible_name="Hello World", text="Hello World")
#                      ^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                      positional arg    keyword arguments
```

## The Fix

### 1. **Parameter Insertion Logic**

**Before (lines 72-87 in original script):**

```python
# Insert accessible_name parameter
insert_pos = transformed_line.find("(") + 1  # RIGHT after opening parenthesis
if transformed_line[insert_pos:].strip().startswith(")"):
    # Empty parameters
    transformed_line = (
        transformed_line[:insert_pos]
        + f'accessible_name="{text_value}"'  # WRONG: First parameter
        + transformed_line[insert_pos:]
    )
else:
    # Has other parameters
    transformed_line = (
        transformed_line[:insert_pos]
        + f'accessible_name="{text_value}", '  # WRONG: Before parent widget
        + transformed_line[insert_pos:]
    )
```

**After (fixed logic):**

```python
# Insert accessible_name parameter after the first positional argument (parent)
paren_pos = transformed_line.find("(")
after_paren = transformed_line[paren_pos + 1:].strip()

if after_paren.startswith(")"):
    # Empty parameters - just add accessible_name
    insert_pos = paren_pos + 1
    transformed_line = (
        transformed_line[:insert_pos]
        + f'accessible_name="{text_value}"'
        + transformed_line[insert_pos:]
    )
else:
    # Has parameters - need to find where to insert accessible_name
    # Look for the first comma that's not inside parentheses/brackets
    comma_pos = self._find_first_param_comma(transformed_line, paren_pos + 1)
    if comma_pos != -1:
        # Insert after first parameter (parent widget)
        insert_pos = comma_pos + 1
        transformed_line = (
            transformed_line[:insert_pos]
            + f' accessible_name="{text_value}",'  # CORRECT: After parent
            + transformed_line[insert_pos:]
        )
    else:
        # Only one parameter, add accessible_name as second parameter
        close_paren = transformed_line.rfind(")")
        transformed_line = (
            transformed_line[:close_paren]
            + f', accessible_name="{text_value}"'  # CORRECT: After parent
            + transformed_line[close_paren:]
        )
```

### 2. **Smart Comma Detection**

Added a helper method `_find_first_param_comma()` that properly handles:

- **String literals**: Ignores commas inside quotes
- **Nested structures**: Ignores commas inside parentheses, brackets, braces
- **Escape sequences**: Handles escaped quotes correctly

```python
def _find_first_param_comma(self, line: str, start_pos: int) -> int:
    """Find the position of the first comma that separates parameters (not inside nested structures)"""
    paren_depth = 0
    bracket_depth = 0
    brace_depth = 0
    in_string = False
    string_char = None
    
    for i in range(start_pos, len(line)):
        char = line[i]
        
        # Handle string literals
        if char in ('"', "'") and (i == 0 or line[i-1] != "\\"):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None
            continue
        
        if in_string:
            continue
            
        # Track nesting depth
        if char == "(":
            paren_depth += 1
        elif char == ")":
            paren_depth -= 1
        elif char == "[":
            bracket_depth += 1
        elif char == "]":
            bracket_depth -= 1
        elif char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth -= 1
        elif char == "," and paren_depth == 0 and bracket_depth == 0 and brace_depth == 0:
            return i
            
    return -1
```

## Test Results

### Before Fix

```bash
$ python -m black --check examples
error: cannot format ... failed to parse source file AST: positional argument follows keyword argument
Oh no! 💥 💔 💥
3 files would fail to reformat.
```

### After Fix

```bash
$ python -m black --check .
All done! ✨ 🍰 ✨
42 files would be left unchanged.
```

## Migration Examples

### Simple Widget

```python
# Before migration:
label = tk.Label(root, text="Hello")

# After migration (now correct):
label = AccessibleLabel(root, accessible_name="Hello", text="Hello")
```

### Complex Widget

```python
# Before migration:
button = tk.Button(root, text="Click Me", command=callback, bg="blue", fg="white")

# After migration (now correct):
button = AccessibleButton(root, accessible_name="Click Me", text="Click Me", command=callback, bg="blue", fg="white")
```

### Widget with No Text

```python
# Before migration:
entry = tk.Entry(root, width=30)

# After migration (no accessible_name added, which is correct):
entry = AccessibleEntry(root, width=30)
```

## Impact

This fix ensures that:

1. **✅ Migration script generates syntactically valid Python code**
2. **✅ Generated code passes black formatting checks**
3. **✅ Generated code follows Python parameter ordering rules**
4. **✅ Complex parameter lists are handled correctly**
5. **✅ Nested structures (lists, dicts, function calls) are preserved**

## Files Fixed

1. **`tkaria11y/scripts/migrate.py`** - Fixed parameter insertion logic
2. **`examples/migration_demo/after_*.py`** - Fixed syntax errors from old migration
3. **`tests/test_themes.py`** - Fixed test that was accessing invalid property

The migration script now generates clean, properly formatted, syntactically correct code that passes all linting and formatting checks! 🎉
