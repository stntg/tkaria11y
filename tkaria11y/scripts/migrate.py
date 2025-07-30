#!/usr/bin/env python3
"""
tkaria11y-migrate
CLI tool to codemod an existing Tk codebase into tkaria11y widgets.
"""

# import sys
import pathlib
import re
from typing import Tuple, Optional, List

import click


class TkinterToA11yTransformer:  # pylint: disable=too-few-public-methods
    """Comprehensive text-based transformer to convert tkinter, ttk, and customtkinter
    widgets to accessible versions. This class is designed as a single-purpose transformer
    with one main public method."""

    def __init__(
        self,
        interactive: bool = False,
        config: Optional[str] = None,
        include_todos: bool = True,
    ):
        self.interactive = interactive
        self.config = config
        self.include_todos = include_todos

        # Comprehensive mapping of all supported widgets to accessible versions
        self.widget_mapping = {
            # Standard Tkinter widgets - with tk. prefix
            "tk.Button": "AccessibleButton",
            "tk.Entry": "AccessibleEntry",
            "tk.Label": "AccessibleLabel",
            "tk.Text": "AccessibleText",
            "tk.Checkbutton": "AccessibleCheckbutton",
            "tk.Radiobutton": "AccessibleRadiobutton",
            "tk.Scale": "AccessibleScale",
            "tk.Scrollbar": "AccessibleScrollbar",
            "tk.Listbox": "AccessibleListbox",
            "tk.Menu": "AccessibleMenu",
            "tk.Menubutton": "AccessibleMenubutton",
            "tk.Frame": "AccessibleFrame",
            "tk.LabelFrame": "AccessibleLabelFrame",
            "tk.Toplevel": "AccessibleToplevel",
            "tk.Canvas": "AccessibleCanvas",
            "tk.Message": "AccessibleMessage",
            "tk.Spinbox": "AccessibleSpinbox",
            "tk.PanedWindow": "AccessiblePanedWindow",
            # Standard Tkinter widgets - without prefix (direct import)
            "Button": "AccessibleButton",
            "Entry": "AccessibleEntry",
            "Label": "AccessibleLabel",
            "Text": "AccessibleText",
            "Checkbutton": "AccessibleCheckbutton",
            "Radiobutton": "AccessibleRadiobutton",
            "Scale": "AccessibleScale",
            "Scrollbar": "AccessibleScrollbar",
            "Listbox": "AccessibleListbox",
            "Menu": "AccessibleMenu",
            "Menubutton": "AccessibleMenubutton",
            "Frame": "AccessibleFrame",
            "LabelFrame": "AccessibleLabelFrame",
            "Toplevel": "AccessibleToplevel",
            "Canvas": "AccessibleCanvas",
            "Message": "AccessibleMessage",
            "Spinbox": "AccessibleSpinbox",
            "PanedWindow": "AccessiblePanedWindow",
            # TTK widgets - with ttk. prefix
            "ttk.Button": "AccessibleTTKButton",
            "ttk.Entry": "AccessibleTTKEntry",
            "ttk.Label": "AccessibleTTKLabel",
            "ttk.Checkbutton": "AccessibleTTKCheckbutton",
            "ttk.Radiobutton": "AccessibleTTKRadiobutton",
            "ttk.Scale": "AccessibleTTKScale",
            "ttk.Scrollbar": "AccessibleTTKScrollbar",
            "ttk.Frame": "AccessibleTTKFrame",
            "ttk.LabelFrame": "AccessibleTTKLabelFrame",
            "ttk.Notebook": "AccessibleNotebook",  # Specialized widget
            "ttk.Progressbar": "AccessibleTTKProgressbar",
            "ttk.Separator": "AccessibleTTKSeparator",
            "ttk.Sizegrip": "AccessibleTTKSizegrip",
            "ttk.Treeview": "AccessibleTreeview",  # Specialized widget
            "ttk.Combobox": "AccessibleCombobox",  # Specialized widget
            "ttk.Spinbox": "AccessibleTTKSpinbox",
            "ttk.PanedWindow": "AccessibleTTKPanedWindow",
            # CustomTkinter widgets - with ctk. prefix
            "ctk.CTkButton": "AccessibleCTKButton",
            "ctk.CTkEntry": "AccessibleCTKEntry",
            "ctk.CTkLabel": "AccessibleCTKLabel",
            "ctk.CTkCheckBox": "AccessibleCTKCheckBox",
            "ctk.CTkRadioButton": "AccessibleCTKRadioButton",
            "ctk.CTkSlider": "AccessibleCTKSlider",
            "ctk.CTkScrollbar": "AccessibleCTKScrollbar",
            "ctk.CTkFrame": "AccessibleCTKFrame",
            "ctk.CTkTabview": "AccessibleCTKTabview",
            "ctk.CTkProgressBar": "AccessibleCTKProgressBar",
            "ctk.CTkSwitch": "AccessibleCTKSwitch",
            "ctk.CTkComboBox": "AccessibleCTKComboBox",
            "ctk.CTkTextbox": "AccessibleCTKTextbox",
            "ctk.CTkScrollableFrame": "AccessibleCTKScrollableFrame",
            "ctk.CTkToplevel": "AccessibleCTKToplevel",
            # CustomTkinter widgets - without prefix (direct import)
            "CTkButton": "AccessibleCTKButton",
            "CTkEntry": "AccessibleCTKEntry",
            "CTkLabel": "AccessibleCTKLabel",
            "CTkCheckBox": "AccessibleCTKCheckBox",
            "CTkRadioButton": "AccessibleCTKRadioButton",
            "CTkSlider": "AccessibleCTKSlider",
            "CTkScrollbar": "AccessibleCTKScrollbar",
            "CTkFrame": "AccessibleCTKFrame",
            "CTkTabview": "AccessibleCTKTabview",
            "CTkProgressBar": "AccessibleCTKProgressBar",
            "CTkSwitch": "AccessibleCTKSwitch",
            "CTkComboBox": "AccessibleCTKComboBox",
            "CTkTextbox": "AccessibleCTKTextbox",
            "CTkScrollableFrame": "AccessibleCTKScrollableFrame",
            "CTkToplevel": "AccessibleCTKToplevel",
        }

    def _check_existing_imports(self, lines: List[str]) -> bool:
        """Check if tkaria11y is already imported"""
        for line in lines:
            if "from tkaria11y.widgets import" in line or "import tkaria11y" in line:
                return True
        return False

    def _detect_import_patterns(self, lines: List[str]) -> dict:
        """Detect what import patterns are used in the file"""
        patterns = {
            "has_tk_import": False,
            "has_ttk_import": False,
            "has_ctk_import": False,
            "tk_import_style": None,  # 'import tkinter as tk' or 'from tkinter import *'
            "ttk_import_style": None,  # 'import tkinter.ttk as ttk' or 'from tkinter import ttk'
            "ctk_import_style": None,  # 'import customtkinter as ctk' or 'from customtkinter import *'
        }

        for line in lines:
            line_stripped = line.strip()

            # Detect tkinter import patterns
            if "import tkinter as tk" in line_stripped:
                patterns["has_tk_import"] = True
                patterns["tk_import_style"] = "as_tk"
            elif "from tkinter import" in line_stripped:
                patterns["has_tk_import"] = True
                patterns["tk_import_style"] = "from_import"
            elif "import tkinter" in line_stripped and "as tk" not in line_stripped:
                patterns["has_tk_import"] = True
                patterns["tk_import_style"] = "direct"

            # Detect TTK import patterns
            if "import tkinter.ttk as ttk" in line_stripped:
                patterns["has_ttk_import"] = True
                patterns["ttk_import_style"] = "as_ttk"
            elif "from tkinter import ttk" in line_stripped:
                patterns["has_ttk_import"] = True
                patterns["ttk_import_style"] = "from_tkinter"
            elif "from tkinter.ttk import" in line_stripped:
                patterns["has_ttk_import"] = True
                patterns["ttk_import_style"] = "from_ttk"

            # Detect CustomTkinter import patterns
            if "import customtkinter as ctk" in line_stripped:
                patterns["has_ctk_import"] = True
                patterns["ctk_import_style"] = "as_ctk"
            elif "from customtkinter import" in line_stripped:
                patterns["has_ctk_import"] = True
                patterns["ctk_import_style"] = "from_import"
            elif (
                "import customtkinter" in line_stripped
                and "as ctk" not in line_stripped
            ):
                patterns["has_ctk_import"] = True
                patterns["ctk_import_style"] = "direct"

        return patterns

    def _add_accessible_name_empty_params(
        self, line: str, text_value: str, paren_pos: int
    ) -> str:
        """Add accessible_name to widget with empty parameters"""
        insert_pos = paren_pos + 1
        return line[:insert_pos] + f'accessible_name="{text_value}"' + line[insert_pos:]

    def _add_accessible_name_with_params(
        self, line: str, text_value: str, paren_pos: int
    ) -> str:
        """Add accessible_name to widget with existing parameters"""
        comma_pos = self._find_first_param_comma(line, paren_pos + 1)
        if comma_pos != -1:
            # Insert after first parameter (parent widget)
            insert_pos = comma_pos + 1
            return (
                line[:insert_pos]
                + f' accessible_name="{text_value}",'
                + line[insert_pos:]
            )

        # Only one param, add accessible_name as second
        close_paren = line.rfind(")")
        return (
            line[:close_paren]
            + f', accessible_name="{text_value}"'
            + line[close_paren:]
        )

    def _add_accessible_name_parameter(self, line: str, text_value: str) -> str:
        """Add accessible_name parameter to widget instantiation"""
        paren_pos = line.find("(")
        after_paren = line[paren_pos + 1 :].strip()

        if after_paren.startswith(")"):
            return self._add_accessible_name_empty_params(line, text_value, paren_pos)

        return self._add_accessible_name_with_params(line, text_value, paren_pos)

    def _extract_text_value(self, line: str) -> Optional[str]:
        """Extract text value from various widget parameters"""
        # Try different text parameter patterns
        patterns = [
            r'text\s*=\s*["\']([^"\']*)["\']',  # text="value"
            r'label\s*=\s*["\']([^"\']*)["\']',  # label="value" (for CTk widgets)
            r'title\s*=\s*["\']([^"\']*)["\']',  # title="value" (for windows)
        ]

        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(1)

        return None

    def _should_add_accessible_name(self, widget_name: str, line: str) -> bool:
        """Determine if accessible_name should be added based on widget type"""
        # Widgets that require accessible_name
        required_widgets = [
            "Button",
            "Checkbutton",
            "Radiobutton",
            "Scale",
            "Entry",
            "Listbox",
            "Menu",
            "Menubutton",
            "CTkButton",
            "CTkCheckBox",
            "CTkRadioButton",
            "CTkSlider",
            "CTkEntry",
            "CTkComboBox",
        ]

        # Check if this widget type requires accessible_name
        for required in required_widgets:
            if required in widget_name:
                return "accessible_name=" not in line

        return False

    def _transform_widget_line(self, line: str) -> Tuple[str, bool]:
        """Transform a single line containing widget instantiation"""
        transformed_line = line
        needs_import = False

        # Sort by length (longest first) to avoid partial matches
        sorted_mappings = sorted(
            self.widget_mapping.items(), key=lambda x: len(x[0]), reverse=True
        )

        for old_widget, new_widget in sorted_mappings:
            # Pattern to match widget instantiation - more flexible matching
            pattern = rf"\b{re.escape(old_widget)}\s*\("
            if re.search(pattern, transformed_line):
                needs_import = True
                # Replace the widget name
                transformed_line = re.sub(pattern, f"{new_widget}(", transformed_line)

                # Try to add accessible_name if appropriate
                if self._should_add_accessible_name(new_widget, transformed_line):
                    text_value = self._extract_text_value(transformed_line)
                    if text_value:
                        transformed_line = self._add_accessible_name_parameter(
                            transformed_line, text_value
                        )
                    elif (
                        self.include_todos
                        and "# TODO: Add accessible_name parameter"
                        not in transformed_line
                    ):
                        # Add a TODO comment for missing accessible_name
                        transformed_line = (
                            transformed_line.rstrip()
                            + "  # TODO: Add accessible_name parameter"
                        )

                # Only process the first match to avoid double transformation
                break

        return transformed_line, needs_import

    def _create_import_statement(self, transformed_lines: List[str]) -> str:
        """Create the import statement for used widgets"""
        used_widgets = set()

        # Find all accessible widgets used in the transformed code
        for widget in self.widget_mapping.values():
            if any(widget in line for line in transformed_lines):
                used_widgets.add(widget)

        if not used_widgets:
            return ""

        # Sort widgets for consistent output
        sorted_widgets = sorted(used_widgets)

        # Create import statement - split into multiple lines if too long
        import_line = "from tkaria11y.widgets import " + ", ".join(sorted_widgets)

        # If the line is too long, split it properly
        if len(import_line) > 88:  # PEP 8 line length minus some margin
            widgets_per_line = []
            current_line = "from tkaria11y.widgets import ("
            indent = "    "

            for i, widget in enumerate(sorted_widgets):
                if i == 0:
                    current_line += widget
                else:
                    test_line = current_line + ", " + widget
                    if len(test_line) > 85:  # Leave room for closing paren
                        widgets_per_line.append(current_line + ",")
                        current_line = indent + widget
                    else:
                        current_line += ", " + widget

            if current_line.strip():
                widgets_per_line.append(current_line)

            # Add closing parenthesis
            if widgets_per_line:
                widgets_per_line.append(")")
                return "\n".join(widgets_per_line)

        return import_line

    def _find_import_insertion_point(self, lines: List[str]) -> int:
        """Find the best place to insert the import statement"""
        insert_idx = 0
        last_import_idx = -1

        # Find the last import statement that's not inside a try block
        in_try_block = False
        try_block_depth = 0

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Track try blocks
            if stripped.startswith("try:"):
                in_try_block = True
                try_block_depth = len(line) - len(line.lstrip())
            elif in_try_block:
                current_indent = len(line) - len(line.lstrip())
                # If we're back to the same or less indentation as the try, we're out of the try block
                if stripped and current_indent <= try_block_depth:
                    in_try_block = False

            # Only consider imports that are not inside try blocks
            if stripped.startswith(("import ", "from ")) and not in_try_block:
                last_import_idx = i
                # Prefer to insert after GUI-related imports
                if any(gui_lib in stripped for gui_lib in ["tkinter", "ttk"]):
                    insert_idx = i + 1
                elif insert_idx == 0:  # If no GUI imports found yet, use any import
                    insert_idx = i + 1

        # If we found imports, insert after the last one
        if last_import_idx >= 0:
            insert_idx = max(insert_idx, last_import_idx + 1)

        # Skip any blank lines after imports
        while insert_idx < len(lines) and lines[insert_idx].strip() == "":
            insert_idx += 1

        return insert_idx

    def _find_first_param_comma(self, line: str, start_pos: int) -> int:
        """Find the position of the first comma that separates parameters
        (not inside nested structures)"""
        paren_depth = 0
        bracket_depth = 0
        brace_depth = 0
        in_string = False
        string_char = None

        for i in range(start_pos, len(line)):
            char = line[i]

            # Handle string literals
            if char in ('"', "'") and (i == 0 or line[i - 1] != "\\"):
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
            elif (
                char == ","
                and paren_depth == 0
                and bracket_depth == 0
                and brace_depth == 0
            ):
                return i

        return -1

    def transform_file(self, content: str) -> str:
        """Transform the content of a Python file"""
        lines = content.split("\n")
        transformed_lines = []
        needs_import = False

        # Check if tkaria11y is already imported
        has_tkaria11y_import = self._check_existing_imports(lines)

        # Detect import patterns for better transformation
        import_patterns = self._detect_import_patterns(lines)

        # Transform each line
        for line in lines:
            transformed_line, line_needs_import = self._transform_widget_line(line)
            if line_needs_import:
                needs_import = True
            transformed_lines.append(transformed_line)

        # Add import if needed and not already present
        if needs_import and not has_tkaria11y_import:
            import_line = self._create_import_statement(transformed_lines)
            if import_line:  # Only add if we have widgets to import
                insert_idx = self._find_import_insertion_point(transformed_lines)

                # Handle multi-line imports
                if "\n" in import_line and import_line.startswith(
                    "from tkaria11y.widgets import ("
                ):
                    import_lines = import_line.split("\n")
                    for i, imp_line in enumerate(reversed(import_lines)):
                        transformed_lines.insert(insert_idx, imp_line)
                else:
                    transformed_lines.insert(insert_idx, import_line)

        return "\n".join(transformed_lines)

    def _prompt_for_accessible_name(self, widget_type: str, line: str) -> Optional[str]:
        """Prompt user for accessible_name in interactive mode"""
        if not self.interactive:
            return None

        print(f"\nFound {widget_type} widget without accessible_name:")
        print(f"Line: {line.strip()}")

        # Try to suggest a name based on context
        text_value = self._extract_text_value(line)
        if text_value:
            suggestion = text_value
        else:
            suggestion = f"{widget_type.lower()}_widget"

        accessible_name = input(
            f"Enter accessible_name (suggested: '{suggestion}'): "
        ).strip()

        if not accessible_name:
            accessible_name = suggestion

        return accessible_name

    def _add_app_migration_comment(self, lines: List[str]) -> List[str]:
        """Add helpful comments about migrating to AccessibleApp"""
        # Look for tk.Tk() instantiation
        for i, line in enumerate(lines):
            if re.search(r"\btk\.Tk\s*\(", line) or re.search(r"\bTk\s*\(", line):
                comment = "# TODO: Consider migrating to AccessibleApp for better accessibility support"
                lines.insert(i + 1, comment)
                break
        return lines

    def get_migration_summary(
        self, original_content: str, transformed_content: str
    ) -> dict:
        """Generate a summary of the migration changes"""
        original_lines = original_content.split("\n")
        transformed_lines = transformed_content.split("\n")

        # Count widget transformations
        widget_counts = {}
        for old_widget, new_widget in self.widget_mapping.items():
            old_count = sum(1 for line in original_lines if old_widget in line)
            new_count = sum(1 for line in transformed_lines if new_widget in line)
            if old_count > 0:
                widget_counts[old_widget] = {"old": old_count, "new": new_count}

        return {
            "widgets_transformed": widget_counts,
            "total_widgets": sum(counts["old"] for counts in widget_counts.values()),
            "lines_changed": sum(
                1 for old, new in zip(original_lines, transformed_lines) if old != new
            ),
            "import_added": "from tkaria11y.widgets import" in transformed_content
            and "from tkaria11y.widgets import" not in original_content,
        }


def _collect_python_files(
    paths: Tuple[str, ...], exclude_pattern: Optional[str] = None
) -> List[pathlib.Path]:
    """Collect all .py files from the given paths"""
    import fnmatch

    files: List[pathlib.Path] = []
    for path_str in paths:
        path = pathlib.Path(path_str)
        if path.is_dir():
            for py_file in path.rglob("*.py"):
                # Skip excluded files
                if exclude_pattern and fnmatch.fnmatch(py_file.name, exclude_pattern):
                    continue
                files.append(py_file)
        else:
            # Skip excluded files even if explicitly specified
            if not (exclude_pattern and fnmatch.fnmatch(path.name, exclude_pattern)):
                files.append(path)
    return files


def _show_diff(src_text: str, transformed_text: str) -> None:
    """Show a simple diff-like output"""
    original_lines = src_text.split("\n")
    new_lines = transformed_text.split("\n")
    for i, (old, new) in enumerate(zip(original_lines, new_lines)):
        if old != new:
            click.echo(f"Line {i + 1}:")
            click.echo(f"  - {old}")
            click.echo(f"  + {new}")


def _process_file_interactive(
    src: pathlib.Path,
    src_text: str,
    transformed_text: str,
    transformer: TkinterToA11yTransformer,
) -> bool:
    """Process a file in interactive mode, return True if updated"""
    click.echo(f"\nProposed changes for {src}:")
    click.echo("=" * 50)

    # Show migration summary
    summary = transformer.get_migration_summary(src_text, transformed_text)
    if summary["total_widgets"] > 0:
        click.echo(f"Widgets to transform: {summary['total_widgets']}")
        for widget, counts in summary["widgets_transformed"].items():
            click.echo(f"  {widget}: {counts['old']} instances")
        click.echo()

    _show_diff(src_text, transformed_text)

    if click.confirm("Apply these changes?"):
        src.write_text(transformed_text, encoding="utf-8")
        click.echo(f"✓ Updated {src}")
        return True

    click.echo(f"✗ Skipped {src}")
    return False


def _process_file_batch(src: pathlib.Path, transformed_text: str) -> bool:
    """Process a file in batch mode, return True if updated"""
    src.write_text(transformed_text, encoding="utf-8")
    click.echo(f"✓ Updated {src}")
    return True


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument(
    "paths",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    nargs=-1,
)
@click.option(
    "--interactive/--batch",
    default=False,
    help="Interactive mode: prompt for each file vs. batch process all files",
)
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    help="YAML/JSON file with custom widget mappings and name overrides",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be changed without modifying files",
)
@click.option(
    "--include-todos",
    is_flag=True,
    default=True,
    help="Add TODO comments for widgets that need manual accessible_name",
)
@click.option(
    "--exclude-pattern",
    help="Exclude files matching this glob pattern (e.g., '*test*.py')",
)
def main(
    paths: Tuple[str, ...],
    interactive: bool,
    config: Optional[str],
    dry_run: bool,
    include_todos: bool,
    exclude_pattern: Optional[str],
) -> None:
    """
    Migrate one or more .py files or directories under PATHS:

      tkaria11y-migrate ./myapp --interactive
      tkaria11y-migrate ./myapp --dry-run
      tkaria11y-migrate ./myapp --exclude-pattern "*test*"
    """
    if not paths:
        click.echo("Error: No paths specified. Use --help for usage information.")
        return

    # Collect all .py files under each path
    files = _collect_python_files(paths, exclude_pattern)

    if not files:
        click.echo("No Python files found to process.")
        return

    click.echo(f"Found {len(files)} Python files to process.")
    if exclude_pattern:
        click.echo(f"Excluding files matching pattern: {exclude_pattern}")

    if dry_run:
        click.echo("DRY RUN MODE - No files will be modified")

    # Apply transformer to each file
    transformer = TkinterToA11yTransformer(
        interactive=interactive, config=config, include_todos=include_todos
    )
    updated_files = []
    skipped_files = []

    for src in files:
        try:
            src_text = src.read_text(encoding="utf-8")
            transformed_text = transformer.transform_file(src_text)

            if transformed_text != src_text:
                if dry_run:
                    click.echo(f"\nWould modify: {src}")
                    summary = transformer.get_migration_summary(
                        src_text, transformed_text
                    )
                    if summary["total_widgets"] > 0:
                        click.echo(
                            f"  Widgets to transform: {summary['total_widgets']}"
                        )
                        for widget, counts in summary["widgets_transformed"].items():
                            click.echo(f"    {widget}: {counts['old']} instances")
                    updated_files.append(src)
                elif interactive:
                    if _process_file_interactive(
                        src, src_text, transformed_text, transformer
                    ):
                        updated_files.append(src)
                    else:
                        skipped_files.append(src)
                else:
                    if _process_file_batch(src, transformed_text):
                        updated_files.append(src)
            else:
                # File doesn't need changes
                pass
        except Exception as e:
            click.echo(f"Error processing {src}: {e}", err=True)
            continue

    # Show final results
    if dry_run:
        if updated_files:
            click.echo(f"\nDRY RUN SUMMARY: Would update {len(updated_files)} files:")
            for file in updated_files:
                click.echo(f"  → {file}")
            click.echo("\nRun without --dry-run to apply these changes.")
        else:
            click.echo("\nDRY RUN SUMMARY: No files need migration.")
    else:
        if updated_files:
            click.echo(f"\nMigration complete! Updated {len(updated_files)} files:")
            for file in updated_files:
                click.echo(f"  ✓ {file}")

            if skipped_files:
                click.echo(f"\nSkipped {len(skipped_files)} files:")
                for file in skipped_files:
                    click.echo(f"  ✗ {file}")

            click.echo("\nNext steps:")
            click.echo("1. Review the changes carefully")
            click.echo("2. Test your application with the new accessible widgets")
            click.echo(
                "3. Consider migrating tk.Tk() to AccessibleApp for full accessibility"
            )
            click.echo(
                "4. Add any missing accessible_name parameters marked with TODO comments"
            )
            click.echo("5. Run your tests to ensure everything works correctly")
            click.echo("6. Commit your changes")
        else:
            click.echo("No files needed migration.")

    # Show overall statistics
    total_files_processed = len(files)
    files_with_changes = len(updated_files)
    click.echo(f"\nProcessed {total_files_processed} files total.")
    if files_with_changes > 0:
        percentage = (files_with_changes / total_files_processed) * 100
        click.echo(f"Files with GUI widgets: {files_with_changes} ({percentage:.1f}%)")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
