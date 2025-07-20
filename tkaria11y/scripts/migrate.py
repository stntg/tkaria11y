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
    """Simple text-based transformer to convert tkinter widgets to accessible
    versions. This class is designed as a single-purpose transformer with
    one main public method."""

    def __init__(self, interactive: bool = False, config: Optional[str] = None):
        self.interactive = interactive
        self.config = config

        # Mapping of tkinter widgets to accessible versions
        self.widget_mapping = {
            "tk.Button": "AccessibleButton",
            "tk.Entry": "AccessibleEntry",
            "tk.Label": "AccessibleLabel",
            "tk.Checkbutton": "AccessibleCheckbutton",
            "tk.Radiobutton": "AccessibleRadiobutton",
            "tk.Scale": "AccessibleScale",
            "tk.Listbox": "AccessibleListbox",
            "tk.Frame": "AccessibleFrame",
            "Button": "AccessibleButton",
            "Entry": "AccessibleEntry",
            "Label": "AccessibleLabel",
            "Checkbutton": "AccessibleCheckbutton",
            "Radiobutton": "AccessibleRadiobutton",
            "Scale": "AccessibleScale",
            "Listbox": "AccessibleListbox",
            "Frame": "AccessibleFrame",
        }

    def _check_existing_imports(self, lines: List[str]) -> bool:
        """Check if tkaria11y is already imported"""
        for line in lines:
            if "from tkaria11y.widgets import" in line or "import tkaria11y" in line:
                return True
        return False

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

    def _transform_widget_line(self, line: str) -> Tuple[str, bool]:
        """Transform a single line containing widget instantiation"""
        transformed_line = line
        needs_import = False

        for old_widget, new_widget in self.widget_mapping.items():
            # Pattern to match widget instantiation
            pattern = rf"\b{re.escape(old_widget)}\s*\("
            if re.search(pattern, line):
                needs_import = True
                # Replace the widget name
                transformed_line = re.sub(pattern, f"{new_widget}(", transformed_line)

                # Try to add accessible_name if text= is present
                text_match = re.search(
                    r'text\s*=\s*["\']([^"\']*)["\']', transformed_line
                )
                if text_match and "accessible_name=" not in transformed_line:
                    text_value = text_match.group(1)
                    transformed_line = self._add_accessible_name_parameter(
                        transformed_line, text_value
                    )

        return transformed_line, needs_import

    def _create_import_statement(self, transformed_lines: List[str]) -> str:
        """Create the import statement for used widgets"""
        used_widgets = set(
            widget
            for widget in self.widget_mapping.values()
            if any(widget in line for line in transformed_lines)
        )
        return "from tkaria11y.widgets import " + ", ".join(used_widgets)

    def _find_import_insertion_point(self, lines: List[str]) -> int:
        """Find the best place to insert the import statement"""
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.strip().startswith(("import ", "from ")) and "tkinter" in line:
                insert_idx = i + 1
            elif line.strip().startswith(("import ", "from ")):
                insert_idx = max(insert_idx, i + 1)
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

        # Transform each line
        for line in lines:
            transformed_line, line_needs_import = self._transform_widget_line(line)
            if line_needs_import:
                needs_import = True
            transformed_lines.append(transformed_line)

        # Add import if needed and not already present
        if needs_import and not has_tkaria11y_import:
            import_line = self._create_import_statement(transformed_lines)
            insert_idx = self._find_import_insertion_point(transformed_lines)
            transformed_lines.insert(insert_idx, import_line)

        return "\n".join(transformed_lines)


def _collect_python_files(paths: Tuple[str, ...]) -> List[pathlib.Path]:
    """Collect all .py files from the given paths"""
    files: List[pathlib.Path] = []
    for path_str in paths:
        path = pathlib.Path(path_str)
        if path.is_dir():
            files.extend(path.rglob("*.py"))
        else:
            files.append(path)
    return files


def _show_diff(src_text: str, transformed_text: str) -> None:
    """Show a simple diff-like output"""
    original_lines = src_text.split("\n")
    new_lines = transformed_text.split("\n")
    for i, (old, new) in enumerate(zip(original_lines, new_lines)):
        if old != new:
            click.echo(f"Line {i+1}:")
            click.echo(f"  - {old}")
            click.echo(f"  + {new}")


def _process_file_interactive(
    src: pathlib.Path, src_text: str, transformed_text: str
) -> bool:
    """Process a file in interactive mode, return True if updated"""
    click.echo(f"\nProposed changes for {src}:")
    click.echo("=" * 50)
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
    help="Prompt for accessible_name vs. infer from text= vs. skip",
)
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    help="YAML/JSON file with name overrides",
)
def main(paths: Tuple[str, ...], interactive: bool, config: Optional[str]) -> None:
    """
    Migrate one or more .py files or directories under PATHS:

      tkaria11y-migrate ./myapp --interactive
    """
    # Collect all .py files under each path
    files = _collect_python_files(paths)

    # Apply transformer to each file
    transformer = TkinterToA11yTransformer(interactive=interactive, config=config)
    updated_files = []

    for src in files:
        src_text = src.read_text(encoding="utf-8")
        transformed_text = transformer.transform_file(src_text)

        if transformed_text != src_text:
            if interactive:
                if _process_file_interactive(src, src_text, transformed_text):
                    updated_files.append(src)
            else:
                if _process_file_batch(src, transformed_text):
                    updated_files.append(src)

    # Show final results
    if updated_files:
        click.echo(f"\nMigration complete! Updated {len(updated_files)} files.")
        click.echo("Review changes, test your application, then commit.")
    else:
        click.echo("No files needed migration.")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
