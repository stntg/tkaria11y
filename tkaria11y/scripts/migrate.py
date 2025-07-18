#!/usr/bin/env python3
"""
tkaria11y-migrate
CLI tool to codemod an existing Tk codebase into tkaria11y widgets.
"""

import pathlib
import click
import re
from typing import Tuple, Optional, List


class TkinterToA11yTransformer:
    """Simple text-based transformer to convert tkinter widgets to accessible
    versions"""

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
        has_tkaria11y_import = False

        for line in lines:
            # Check if tkaria11y is already imported
            if "from tkaria11y.widgets import" in line or "import tkaria11y" in line:
                has_tkaria11y_import = True

            # Transform widget instantiations
            transformed_line = line
            for old_widget, new_widget in self.widget_mapping.items():
                # Pattern to match widget instantiation
                pattern = rf"\b{re.escape(old_widget)}\s*\("
                if re.search(pattern, line):
                    needs_import = True
                    # Replace the widget name
                    transformed_line = re.sub(
                        pattern, f"{new_widget}(", transformed_line
                    )

                    # Try to add accessible_name if text= is present
                    text_match = re.search(
                        r'text\s*=\s*["\']([^"\']*)["\']', transformed_line
                    )
                    if text_match and "accessible_name=" not in transformed_line:
                        text_value = text_match.group(1)
                        # Insert accessible_name parameter after the first positional argument (parent)
                        paren_pos = transformed_line.find("(")
                        after_paren = transformed_line[paren_pos + 1 :].strip()

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
                            comma_pos = self._find_first_param_comma(
                                transformed_line, paren_pos + 1
                            )
                            if comma_pos != -1:
                                # Insert after first parameter (parent widget)
                                insert_pos = comma_pos + 1
                                transformed_line = (
                                    transformed_line[:insert_pos]
                                    + f' accessible_name="{text_value}",'
                                    + transformed_line[insert_pos:]
                                )
                            else:
                                # Only one parameter, add accessible_name as second parameter
                                close_paren = transformed_line.rfind(")")
                                transformed_line = (
                                    transformed_line[:close_paren]
                                    + f', accessible_name="{text_value}"'
                                    + transformed_line[close_paren:]
                                )

            transformed_lines.append(transformed_line)

        # Add import if needed and not already present
        if needs_import and not has_tkaria11y_import:
            # Find the best place to insert the import
            import_line = "from tkaria11y.widgets import " + ", ".join(
                set(
                    widget
                    for widget in self.widget_mapping.values()
                    if any(widget in line for line in transformed_lines)
                )
            )

            # Insert after existing imports
            insert_idx = 0
            for i, line in enumerate(transformed_lines):
                if line.strip().startswith(("import ", "from ")) and "tkinter" in line:
                    insert_idx = i + 1
                elif line.strip().startswith(("import ", "from ")):
                    insert_idx = max(insert_idx, i + 1)

            transformed_lines.insert(insert_idx, import_line)

        return "\n".join(transformed_lines)


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
    # from .generate_stubs import main as generate_stubs  # if you want to
    # stub afterwards

    # 1. collect all .py files under each path
    files: List[pathlib.Path] = []
    for path_str in paths:
        p = pathlib.Path(path_str)
        if p.is_dir():
            files.extend(p.rglob("*.py"))
        else:
            files.append(p)

    # 2. apply transformer to each file
    transformer = TkinterToA11yTransformer(interactive=interactive, config=config)
    updated_files = []

    for src in files:
        src_text = src.read_text(encoding="utf-8")
        transformed_text = transformer.transform_file(src_text)

        if transformed_text != src_text:
            if interactive:
                click.echo(f"\nProposed changes for {src}:")
                click.echo("=" * 50)
                # Show a simple diff-like output
                original_lines = src_text.split("\n")
                new_lines = transformed_text.split("\n")
                for i, (old, new) in enumerate(zip(original_lines, new_lines)):
                    if old != new:
                        click.echo(f"Line {i+1}:")
                        click.echo(f"  - {old}")
                        click.echo(f"  + {new}")

                if click.confirm("Apply these changes?"):
                    src.write_text(transformed_text, encoding="utf-8")
                    updated_files.append(src)
                    click.echo(f"✓ Updated {src}")
                else:
                    click.echo(f"✗ Skipped {src}")
            else:
                src.write_text(transformed_text, encoding="utf-8")
                updated_files.append(src)
                click.echo(f"✓ Updated {src}")

    if updated_files:
        click.echo(f"\nMigration complete! Updated {len(updated_files)} files.")
        click.echo("Review changes, test your application, then commit.")
    else:
        click.echo("No files needed migration.")


if __name__ == "__main__":
    main()
