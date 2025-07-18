#!/usr/bin/env python3

"""
Auto-generate tkaria11y/stubs/widgets.pyi
based on tkaria11y/widgets.py _WIDGET_MAP

This script ensures your stubs/widgets.pyi always matches _WIDGET_MAP,
saves manual updates when you add/remove widgets, and keeps MyPy/IDE
autocomplete in sync.
"""

import subprocess
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing tkaria11y
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from tkaria11y import widgets
except ImportError:
    # Fallback for when running as a script
    import importlib.util

    widgets_path = Path(__file__).parent.parent / "widgets.py"
    spec = importlib.util.spec_from_file_location("widgets", widgets_path)
    widgets = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(widgets)


def main() -> None:
    """Main entry point for the stub generator"""
    # Determine the correct path for stubs directory
    script_path = Path(__file__).resolve()
    if script_path.parent.parent.name == "tkaria11y":
        # Running as module: tkaria11y/scripts/generate_stubs.py -> tkaria11y/stubs/
        stub_dir = script_path.parent.parent / "stubs"
    else:
        # Running as script from root: scripts/generate_stubs.py -> stubs/
        stub_dir = script_path.parent.parent / "stubs"

    stub_dir.mkdir(parents=True, exist_ok=True)
    stub_path = stub_dir / "widgets.pyi"

    lines = ["import tkinter as tk\n", "\n", "__all__ = [\n"]
    widget_map = getattr(widgets, "_WIDGET_MAP", {})
    for name in widget_map:
        lines.append(f'    "Accessible{name}",\n')
    lines.append("]\n\n")

    for i, (name, (role, base)) in enumerate(widget_map.items()):
        lines.append(f"class Accessible{name}(tk.{base.__name__}):\n")
        lines.append(
            "    def __init__(self, master=None, *, "
            'accessible_name: str = "", **kw) -> None: ...\n'
        )
        lines.append("\n")
        lines.append("    accessible_name: str\n")
        lines.append("    accessible_role: str\n")
        lines.append("    accessible_description: str\n")
        # Add blank line between classes, but not after the last one
        if i < len(widget_map) - 1:
            lines.append("\n")

    content = "".join(lines)

    old = stub_path.read_text() if stub_path.exists() else ""
    if content != old:
        stub_path.write_text(content)

        # Format with black
        try:
            subprocess.run(
                [sys.executable, "-m", "black", str(stub_path)],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not format with black: {e}")
        except FileNotFoundError:
            print("Warning: black not found, skipping formatting")

        print(f"Updated stubs: {stub_path}")
    else:
        print("Stubs up-to-date.")


if __name__ == "__main__":
    main()
