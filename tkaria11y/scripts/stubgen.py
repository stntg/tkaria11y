#!/usr/bin/env python3
"""
tkaria11y-stubgen - Type stub generator for tkaria11y

Generates comprehensive type stubs for the tkaria11y accessibility framework
to provide full IDE support with type checking and autocomplete.
"""

import os
import sys
import ast
import inspect
import argparse
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Union
import importlib
import pkgutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import tkaria11y
    from tkaria11y import widgets, mixins, accessibility_validator
    from tkaria11y import braille_support, audio_accessibility
except ImportError as e:
    print(f"Error importing tkaria11y: {e}")
    print("Make sure tkaria11y is installed or run from the project directory")
    sys.exit(1)


class TypeStubGenerator:
    """Generates type stubs for tkaria11y modules"""

    def __init__(self, output_dir: str = "stubs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # If output_dir is "package", generate stubs directly in the main package
        if output_dir == "package":
            import tkaria11y

            self.output_dir = Path(tkaria11y.__file__).parent

        # Type mappings for common Python types
        self.type_mappings = {
            "str": "str",
            "int": "int",
            "float": "float",
            "bool": "bool",
            "list": "List[Any]",
            "dict": "Dict[str, Any]",
            "tuple": "Tuple[Any, ...]",
            "set": "Set[Any]",
            "NoneType": "None",
            "function": "Callable[..., Any]",
            "method": "Callable[..., Any]",
            "builtin_function_or_method": "Callable[..., Any]",
        }

        # Tkinter type mappings
        self.tkinter_mappings = {
            "Widget": "tk.Widget",
            "Tk": "tk.Tk",
            "Toplevel": "tk.Toplevel",
            "Frame": "tk.Frame",
            "Button": "tk.Button",
            "Entry": "tk.Entry",
            "Label": "tk.Label",
            "Checkbutton": "tk.Checkbutton",
            "Radiobutton": "tk.Radiobutton",
            "Scale": "tk.Scale",
            "Listbox": "tk.Listbox",
            "Text": "tk.Text",
            "Canvas": "tk.Canvas",
            "Menu": "tk.Menu",
            "Menubutton": "tk.Menubutton",
            "OptionMenu": "tk.OptionMenu",
            "Spinbox": "tk.Spinbox",
            "PanedWindow": "tk.PanedWindow",
            "Scrollbar": "tk.Scrollbar",
            "LabelFrame": "tk.LabelFrame",
            "Variable": "tk.Variable",
            "StringVar": "tk.StringVar",
            "IntVar": "tk.IntVar",
            "DoubleVar": "tk.DoubleVar",
            "BooleanVar": "tk.BooleanVar",
            "Event": "tk.Event",
        }

        # TTK type mappings
        self.ttk_mappings = {
            "Button": "ttk.Button",
            "Entry": "ttk.Entry",
            "Label": "ttk.Label",
            "Checkbutton": "ttk.Checkbutton",
            "Radiobutton": "ttk.Radiobutton",
            "Scale": "ttk.Scale",
            "Frame": "ttk.Frame",
            "LabelFrame": "ttk.LabelFrame",
            "Notebook": "ttk.Notebook",
            "Combobox": "ttk.Combobox",
            "Treeview": "ttk.Treeview",
            "Progressbar": "ttk.Progressbar",
            "Separator": "ttk.Separator",
            "Sizegrip": "ttk.Sizegrip",
            "Spinbox": "ttk.Spinbox",
            "PanedWindow": "ttk.PanedWindow",
        }

    def get_type_annotation(self, obj: Any, name: str = "") -> str:
        """Get type annotation for an object"""
        if obj is None:
            return "None"

        obj_type = type(obj).__name__

        # Check direct mappings first
        if obj_type in self.type_mappings:
            return self.type_mappings[obj_type]

        # Check for tkinter widgets
        if hasattr(obj, "__module__") and obj.__module__:
            if "tkinter" in obj.__module__ and obj_type in self.tkinter_mappings:
                return self.tkinter_mappings[obj_type]
            elif "ttk" in obj.__module__ and obj_type in self.ttk_mappings:
                return self.ttk_mappings[obj_type]

        # Handle special cases
        if inspect.isclass(obj):
            return f"Type[{obj.__name__}]"
        elif inspect.isfunction(obj) or inspect.ismethod(obj):
            return "Callable[..., Any]"
        elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes)):
            return "List[Any]"
        elif isinstance(obj, dict):
            return "Dict[str, Any]"

        # Default to Any for unknown types
        return "Any"

    def extract_function_signature(self, func: Any) -> str:
        """Extract function signature with type annotations"""
        try:
            sig = inspect.signature(func)
            params = []

            for param_name, param in sig.parameters.items():
                param_str = param_name

                # Add type annotation if available
                if param.annotation != inspect.Parameter.empty:
                    if hasattr(param.annotation, "__name__"):
                        param_str += f": {param.annotation.__name__}"
                    else:
                        param_str += f": {param.annotation}"
                else:
                    param_str += ": Any"

                # Add default value
                if param.default != inspect.Parameter.empty:
                    param_str += " = ..."

                params.append(param_str)

            # Handle return type
            return_type = "Any"
            if sig.return_annotation != inspect.Signature.empty:
                if hasattr(sig.return_annotation, "__name__"):
                    return_type = sig.return_annotation.__name__
                else:
                    return_type = str(sig.return_annotation)

            params_str = ", ".join(params)
            return f"({params_str}) -> {return_type}"

        except (ValueError, TypeError):
            return "(...) -> Any"

    def generate_class_stub(self, cls: type, indent: str = "") -> List[str]:
        """Generate stub for a class"""
        lines = []

        # Class definition
        bases = []
        if hasattr(cls, "__bases__"):
            for base in cls.__bases__:
                if base.__name__ != "object":
                    if hasattr(base, "__module__") and base.__module__:
                        if "tkinter" in base.__module__:
                            if base.__name__ in self.tkinter_mappings:
                                bases.append(self.tkinter_mappings[base.__name__])
                            else:
                                bases.append(f"tk.{base.__name__}")
                        elif "ttk" in base.__module__:
                            if base.__name__ in self.ttk_mappings:
                                bases.append(self.ttk_mappings[base.__name__])
                            else:
                                bases.append(f"ttk.{base.__name__}")
                        else:
                            bases.append(base.__name__)
                    else:
                        bases.append(base.__name__)

        if bases:
            class_def = f"{indent}class {cls.__name__}({', '.join(bases)}):"
        else:
            class_def = f"{indent}class {cls.__name__}:"

        lines.append(class_def)

        # Class docstring
        if hasattr(cls, "__doc__") and cls.__doc__:
            lines.append(f'{indent}    """' + cls.__doc__.split("\n")[0] + '"""')

        # Class attributes
        class_attrs = []
        for attr_name in dir(cls):
            if not attr_name.startswith("_") or attr_name in ["__init__"]:
                try:
                    attr = getattr(cls, attr_name)
                    if not callable(attr) and not inspect.ismethod(attr):
                        attr_type = self.get_type_annotation(attr, attr_name)
                        class_attrs.append(f"{indent}    {attr_name}: {attr_type}")
                except (AttributeError, TypeError):
                    continue

        if class_attrs:
            lines.extend(class_attrs)
            lines.append("")

        # Methods
        methods = []
        for method_name in dir(cls):
            if not method_name.startswith("_") or method_name == "__init__":
                try:
                    method = getattr(cls, method_name)
                    if callable(method) or inspect.ismethod(method):
                        sig = self.extract_function_signature(method)
                        methods.append(f"{indent}    def {method_name}{sig}: ...")
                except (AttributeError, TypeError):
                    continue

        if methods:
            lines.extend(methods)
        else:
            lines.append(f"{indent}    ...")

        return lines

    def generate_function_stub(self, func: Any, indent: str = "") -> str:
        """Generate stub for a function"""
        sig = self.extract_function_signature(func)
        return f"{indent}def {func.__name__}{sig}: ..."

    def generate_enum_stub(self, enum_cls: type, indent: str = "") -> List[str]:
        """Generate stub for an Enum class"""
        lines = []
        lines.append(f"{indent}class {enum_cls.__name__}(Enum):")

        # Enum members
        if hasattr(enum_cls, "__members__") and enum_cls.__members__:
            for member_name, member_value in enum_cls.__members__.items():
                lines.append(f'{indent}    {member_name} = "{member_value.value}"')
        else:
            lines.append(f"{indent}    pass")

        return lines

    def generate_module_stub(self, module: Any, module_name: str) -> str:
        """Generate complete stub for a module"""
        lines = []

        # Header
        lines.append(f"# {module_name}.pyi")
        lines.append(f"# Type stubs for {module_name}")
        lines.append("")

        # Imports
        imports = [
            "from typing import Any, Dict, List, Optional, Union, Callable, Tuple, Type, Set",
            "import tkinter as tk",
            "from tkinter import ttk",
            "from enum import Enum",
            "from abc import ABC, abstractmethod",
        ]

        # Add specific imports based on module
        if "threading" in str(module):
            imports.append("import threading")
        if "queue" in str(module):
            imports.append("import queue")
        if "time" in str(module):
            imports.append("import time")

        lines.extend(imports)
        lines.append("")

        # Module contents
        module_items = []

        # Get all public items from module
        if hasattr(module, "__all__"):
            items_to_process = module.__all__
        else:
            items_to_process = [
                name for name in dir(module) if not name.startswith("_")
            ]

        for item_name in items_to_process:
            try:
                item = getattr(module, item_name)

                if inspect.isclass(item):
                    # Check if it's an Enum
                    if hasattr(item, "__bases__") and any(
                        "Enum" in str(base) for base in item.__bases__
                    ):
                        module_items.extend(self.generate_enum_stub(item))
                    else:
                        module_items.extend(self.generate_class_stub(item))
                    module_items.append("")

                elif inspect.isfunction(item):
                    module_items.append(self.generate_function_stub(item))
                    module_items.append("")

                elif not callable(item):
                    # Module-level variable
                    item_type = self.get_type_annotation(item, item_name)
                    module_items.append(f"{item_name}: {item_type}")

            except (AttributeError, TypeError, ImportError):
                continue

        lines.extend(module_items)

        # __all__ export
        if hasattr(module, "__all__"):
            lines.append(f"__all__: List[str]")

        return "\n".join(lines)

    def generate_all_stubs(self) -> None:
        """Generate stubs for all tkaria11y modules"""
        print("Generating type stubs for tkaria11y...")

        # Main module
        print("  Generating __init__.pyi...")
        main_stub = self.generate_module_stub(tkaria11y, "tkaria11y")
        with open(self.output_dir / "__init__.pyi", "w", encoding="utf-8") as f:
            f.write(main_stub)

        # Widgets module
        if hasattr(tkaria11y, "widgets"):
            print("  Generating widgets.pyi...")
            widgets_stub = self.generate_module_stub(widgets, "tkaria11y.widgets")
            with open(self.output_dir / "widgets.pyi", "w", encoding="utf-8") as f:
                f.write(widgets_stub)

        # Mixins module
        if hasattr(tkaria11y, "mixins"):
            print("  Generating mixins.pyi...")
            mixins_stub = self.generate_module_stub(mixins, "tkaria11y.mixins")
            with open(self.output_dir / "mixins.pyi", "w", encoding="utf-8") as f:
                f.write(mixins_stub)

        # Accessibility validator module
        if hasattr(tkaria11y, "accessibility_validator"):
            print("  Generating accessibility_validator.pyi...")
            validator_stub = self.generate_module_stub(
                accessibility_validator, "tkaria11y.accessibility_validator"
            )
            with open(
                self.output_dir / "accessibility_validator.pyi", "w", encoding="utf-8"
            ) as f:
                f.write(validator_stub)

        # Braille support module
        if hasattr(tkaria11y, "braille_support"):
            print("  Generating braille_support.pyi...")
            braille_stub = self.generate_module_stub(
                braille_support, "tkaria11y.braille_support"
            )
            with open(
                self.output_dir / "braille_support.pyi", "w", encoding="utf-8"
            ) as f:
                f.write(braille_stub)

        # Audio accessibility module
        if hasattr(tkaria11y, "audio_accessibility"):
            print("  Generating audio_accessibility.pyi...")
            audio_stub = self.generate_module_stub(
                audio_accessibility, "tkaria11y.audio_accessibility"
            )
            with open(
                self.output_dir / "audio_accessibility.pyi", "w", encoding="utf-8"
            ) as f:
                f.write(audio_stub)

        # Generate stubs for other modules
        for module_name in [
            "app",
            "themes",
            "utils",
            "a11y_engine",
            "focus_manager",
            "platform_integration",
            "aria_compliance",
        ]:
            try:
                module = getattr(tkaria11y, module_name, None)
                if module:
                    print(f"  Generating {module_name}.pyi...")
                    stub = self.generate_module_stub(module, f"tkaria11y.{module_name}")
                    with open(
                        self.output_dir / f"{module_name}.pyi", "w", encoding="utf-8"
                    ) as f:
                        f.write(stub)
            except (AttributeError, ImportError):
                continue

        print(f"Type stubs generated in {self.output_dir}/")

    def validate_stubs(self, validate_package_stubs: bool = False) -> None:
        """Validate generated stubs using mypy"""
        if validate_package_stubs:
            # Validate stubs in the main package directory
            import tkaria11y

            package_dir = Path(tkaria11y.__file__).parent
            stub_files = list(package_dir.glob("*.pyi"))
            if not stub_files:
                print("No stub files found in package directory")
                return
            print(f"Validating {len(stub_files)} stub files in package directory...")
            validation_target = str(package_dir)
        else:
            print("Validating generated stubs...")
            validation_target = str(self.output_dir)

        try:
            import subprocess

            result = subprocess.run(
                ["mypy", "--ignore-missing-imports", validation_target],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print("✓ All stubs are valid!")
            else:
                print("⚠ Some stubs have issues:")
                print(result.stdout)
                print(result.stderr)

        except FileNotFoundError:
            print("mypy not found. Install mypy to validate stubs.")
        except Exception as e:
            print(f"Error validating stubs: {e}")

    def create_py_typed_marker(self) -> None:
        """Create py.typed marker file"""
        py_typed_path = Path(tkaria11y.__file__).parent / "py.typed"
        with open(py_typed_path, "w") as f:
            f.write("# Marker file for PEP 561\n")
        print(f"Created py.typed marker at {py_typed_path}")


def main() -> None:
    """Main entry point for stub generator"""
    parser = argparse.ArgumentParser(
        description="Generate type stubs for tkaria11y",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tkaria11y-stubgen                    # Generate stubs in ./stubs/
  tkaria11y-stubgen -o package         # Generate stubs directly in tkaria11y package
  tkaria11y-stubgen -o typings         # Generate stubs in ./typings/
  tkaria11y-stubgen --validate         # Generate and validate stubs
  tkaria11y-stubgen --py-typed         # Create py.typed marker
        """,
    )

    parser.add_argument(
        "-o",
        "--output",
        default="stubs",
        help="Output directory for stubs (default: stubs). Use 'package' to generate directly in tkaria11y package directory.",
    )

    parser.add_argument(
        "--validate", action="store_true", help="Validate generated stubs with mypy"
    )

    parser.add_argument(
        "--validate-package",
        action="store_true",
        help="Validate existing stubs in the package directory with mypy",
    )

    parser.add_argument(
        "--py-typed", action="store_true", help="Create py.typed marker file"
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Create stub generator
    generator = TypeStubGenerator(args.output)

    try:
        # Handle validation-only mode
        if args.validate_package:
            generator.validate_stubs(validate_package_stubs=True)
            return

        # Generate stubs
        generator.generate_all_stubs()

        # Validate if requested
        if args.validate:
            generator.validate_stubs()

        # Create py.typed marker if requested
        if args.py_typed:
            generator.create_py_typed_marker()

        print("\n✓ Stub generation completed successfully!")
        print(f"Stubs are available in: {generator.output_dir}")
        print("\nTo use the stubs in your IDE:")
        print("1. Add the stubs directory to your Python path")
        print("2. Or copy the .pyi files to your site-packages/tkaria11y/ directory")
        print("3. Restart your IDE for full type checking support")

    except Exception as e:
        print(f"Error generating stubs: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
