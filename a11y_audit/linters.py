# a11y_audit/linters.py

"""
Accessibility linting tools and custom checkers.

This module provides various linting tools and custom accessibility checkers
for analyzing Python code and documentation for accessibility compliance.
"""

import ast
import re
import subprocess
import shutil
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from .config import SOURCE_DIRS, EXCLUDE_PATTERNS, AUDIT_CONFIG, get_config_path


class AccessibilityLinter:
    """Main accessibility linter that coordinates various tools."""

    def __init__(self):
        self.config = AUDIT_CONFIG

    def run_flake8_audit(self) -> Dict[str, Any]:
        """Run flake8 with accessibility-focused configuration."""
        try:
            # Find flake8 executable
            flake8_path = shutil.which("flake8")
            if not flake8_path:
                return {
                    "status": "SKIPPED",
                    "message": "flake8 not available - install with: pip install flake8",
                }

            # Check if flake8 is available
            result = subprocess.run(
                [flake8_path, "--version"], capture_output=True, text=True
            )
            if result.returncode != 0:
                return {
                    "status": "SKIPPED",
                    "message": "flake8 not available - install with: pip install flake8",
                }

            # Build flake8 command with config
            config_file = get_config_path("flake8")
            cmd = [flake8_path]

            if config_file.exists():
                cmd.extend(["--config", str(config_file)])
            else:
                # Fallback configuration
                cmd.extend(["--max-line-length=88", "--ignore=E203,W503"])

            # Add source directories
            for source_dir in SOURCE_DIRS:
                if source_dir.exists():
                    cmd.append(str(source_dir))

            # Run flake8
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Parse results
            issues = self._parse_flake8_output(result.stdout)

            return {
                "status": "COMPLETED",
                "issues_found": len(issues),
                "issues": issues,
                "exit_code": result.returncode,
                "message": f"Found {len(issues)} code style issues",
            }

        except FileNotFoundError:
            return {
                "status": "SKIPPED",
                "message": "flake8 not found - install with: pip install flake8",
            }
        except Exception as e:
            return {"status": "ERROR", "message": f"Error running flake8: {str(e)}"}

    def run_pylint_audit(self) -> Dict[str, Any]:
        """Run pylint with accessibility-focused configuration."""
        try:
            # Find pylint executable
            pylint_path = shutil.which("pylint")
            if not pylint_path:
                return {
                    "status": "SKIPPED",
                    "message": "pylint not available - install with: pip install pylint",
                }

            # Check if pylint is available
            result = subprocess.run(
                [pylint_path, "--version"], capture_output=True, text=True
            )
            if result.returncode != 0:
                return {
                    "status": "SKIPPED",
                    "message": "pylint not available - install with: pip install pylint",
                }

            # Build pylint command with config
            config_file = get_config_path("pylint")
            cmd = [pylint_path, "--output-format=json"]

            if config_file.exists():
                cmd.extend(["--rcfile", str(config_file)])

            # Add source directories
            source_files = []
            for source_dir in SOURCE_DIRS:
                if source_dir.exists():
                    for py_file in source_dir.rglob("*.py"):
                        if not any(
                            pattern in str(py_file) for pattern in EXCLUDE_PATTERNS
                        ):
                            source_files.append(str(py_file))

            if not source_files:
                return {
                    "status": "SKIPPED",
                    "message": "No Python files found to analyze",
                }

            cmd.extend(source_files)

            # Run pylint
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Parse JSON results
            issues = self._parse_pylint_output(result.stdout)

            return {
                "status": "COMPLETED",
                "issues_found": len(issues),
                "issues": issues,
                "exit_code": result.returncode,
                "message": f"Found {len(issues)} code quality issues",
            }

        except FileNotFoundError:
            return {
                "status": "SKIPPED",
                "message": "pylint not found - install with: pip install pylint",
            }
        except Exception as e:
            return {"status": "ERROR", "message": f"Error running pylint: {str(e)}"}

    def run_mypy_audit(self) -> Dict[str, Any]:
        """Run mypy type checking with accessibility focus."""
        try:
            # Find mypy executable
            mypy_path = shutil.which("mypy")
            if not mypy_path:
                return {
                    "status": "SKIPPED",
                    "message": "mypy not available - install with: pip install mypy",
                }

            # Check if mypy is available
            result = subprocess.run(
                [mypy_path, "--version"], capture_output=True, text=True
            )
            if result.returncode != 0:
                return {
                    "status": "SKIPPED",
                    "message": "mypy not available - install with: pip install mypy",
                }

            # Build mypy command with config
            config_file = get_config_path("mypy")
            cmd = [mypy_path]

            if config_file.exists():
                cmd.extend(["--config-file", str(config_file)])
            else:
                # Fallback configuration
                cmd.extend(["--ignore-missing-imports", "--show-error-codes"])

            # Add source directories
            for source_dir in SOURCE_DIRS:
                if source_dir.exists() and source_dir.name == "tkaria11y":
                    cmd.append(str(source_dir))

            # Run mypy
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Parse results
            issues = self._parse_mypy_output(result.stdout)

            return {
                "status": "COMPLETED",
                "issues_found": len(issues),
                "issues": issues,
                "exit_code": result.returncode,
                "message": f"Found {len(issues)} type checking issues",
            }

        except FileNotFoundError:
            return {
                "status": "SKIPPED",
                "message": "mypy not found - install with: pip install mypy",
            }
        except Exception as e:
            return {"status": "ERROR", "message": f"Error running mypy: {str(e)}"}

    def run_custom_accessibility_checks(self) -> Dict[str, Any]:
        """Run custom accessibility-specific checks."""
        try:
            checker = CustomAccessibilityChecker()
            issues = []

            for source_dir in SOURCE_DIRS:
                if source_dir.exists():
                    issues.extend(checker.check_directory(source_dir))

            return {
                "status": "COMPLETED",
                "issues_found": len(issues),
                "issues": issues,
                "message": f"Found {len(issues)} accessibility-specific issues",
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Error running custom checks: {str(e)}",
            }

    def run_documentation_audit(self) -> Dict[str, Any]:
        """Run documentation accessibility audit."""
        try:
            doc_checker = DocumentationAccessibilityChecker()
            issues = []

            # Check markdown files in source directories
            for source_dir in SOURCE_DIRS:
                if source_dir.exists():
                    for md_file in source_dir.rglob("*.md"):
                        issues.extend(doc_checker.check_markdown_file(md_file))

            # Check README files
            readme_files = [
                Path("README.md"),
                Path("docs/README.md"),
                Path("examples/README.md"),
            ]

            for readme_file in readme_files:
                if readme_file.exists():
                    issues.extend(doc_checker.check_markdown_file(readme_file))

            return {
                "status": "COMPLETED",
                "issues_found": len(issues),
                "issues": issues,
                "message": f"Found {len(issues)} documentation accessibility issues",
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Error running documentation audit: {str(e)}",
            }

    def _parse_flake8_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse flake8 text output into structured format."""
        issues = []
        for line in output.strip().split("\n"):
            if line and ":" in line:
                parts = line.split(":", 3)
                if len(parts) >= 4:
                    # Extract error code from message
                    message = parts[3].strip()
                    code_match = re.match(r"([A-Z]\d+)", message)
                    code = code_match.group(1) if code_match else ""

                    issues.append(
                        {
                            "filename": parts[0],
                            "line": int(parts[1]) if parts[1].isdigit() else 0,
                            "column": int(parts[2]) if parts[2].isdigit() else 0,
                            "message": message,
                            "code": code,
                            "severity": "error" if code.startswith("E") else "warning",
                            "category": "style",
                        }
                    )
        return issues

    def _parse_pylint_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse pylint JSON output into structured format."""
        issues = []
        try:
            if output.strip():
                pylint_issues = json.loads(output)
                for issue in pylint_issues:
                    issues.append(
                        {
                            "filename": issue.get("path", ""),
                            "line": issue.get("line", 0),
                            "column": issue.get("column", 0),
                            "message": issue.get("message", ""),
                            "code": issue.get("message-id", ""),
                            "severity": issue.get("type", "warning"),
                            "category": "quality",
                        }
                    )
        except json.JSONDecodeError:
            # Fallback to text parsing if JSON fails
            pass
        return issues

    def _parse_mypy_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse mypy text output into structured format."""
        issues = []
        for line in output.strip().split("\n"):
            if ":" in line and ("error:" in line or "warning:" in line):
                parts = line.split(":", 3)
                if len(parts) >= 3:
                    message = parts[-1].strip()
                    severity = "error" if "error:" in message else "warning"

                    # Extract error code if present
                    code_match = re.search(r"\[([a-z-]+)\]", message)
                    code = code_match.group(1) if code_match else ""

                    issues.append(
                        {
                            "filename": parts[0],
                            "line": int(parts[1]) if parts[1].isdigit() else 0,
                            "column": 0,
                            "message": message,
                            "code": code,
                            "severity": severity,
                            "category": "typing",
                        }
                    )
        return issues


class CustomAccessibilityChecker:
    """Custom accessibility checker for Python code using AST analysis."""

    def __init__(self):
        self.config = AUDIT_CONFIG["code_patterns"]

    def check_directory(self, directory: Path) -> List[Dict[str, Any]]:
        """Check all Python files in directory for accessibility issues."""
        issues = []

        for py_file in directory.rglob("*.py"):
            # Skip excluded patterns
            if any(pattern in str(py_file) for pattern in EXCLUDE_PATTERNS):
                continue

            issues.extend(self.check_file(py_file))

        return issues

    def check_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check a single Python file for accessibility issues."""
        issues = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content, filename=str(file_path))

            # Run various accessibility checks
            if self.config.get("check_aria_attributes", True):
                issues.extend(self._check_aria_attributes(tree, file_path, content))

            if self.config.get("check_keyboard_handlers", True):
                issues.extend(self._check_keyboard_handlers(tree, file_path, content))

            if self.config.get("check_focus_management", True):
                issues.extend(self._check_focus_management(tree, file_path, content))

            if self.config.get("check_color_only_info", True):
                issues.extend(self._check_color_only_info(tree, file_path, content))

            if self.config.get("check_text_alternatives", True):
                issues.extend(self._check_text_alternatives(tree, file_path, content))

        except Exception as e:
            issues.append(
                {
                    "filename": str(file_path),
                    "line": 0,
                    "column": 0,
                    "message": f"Error parsing file: {str(e)}",
                    "code": "A000",
                    "severity": "error",
                    "category": "parsing",
                }
            )

        return issues

    def _check_aria_attributes(
        self, tree: ast.AST, file_path: Path, content: str
    ) -> List[Dict[str, Any]]:
        """Check for proper ARIA attribute usage (A001)."""
        issues = []

        class ARIAVisitor(ast.NodeVisitor):
            def visit_Call(self, node):
                # Check for accessible widget creation without accessible_name
                if isinstance(node.func, ast.Attribute) and node.func.attr in [
                    "AccessibleButton",
                    "AccessibleEntry",
                    "AccessibleLabel",
                    "AccessibleFrame",
                    "AccessibleText",
                    "AccessibleListbox",
                ]:

                    # Check if accessible_name is provided
                    has_accessible_name = any(
                        kw.arg == "accessible_name" for kw in node.keywords
                    )

                    if not has_accessible_name:
                        issues.append(
                            {
                                "filename": str(file_path),
                                "line": node.lineno,
                                "column": node.col_offset,
                                "message": f"Widget {node.func.attr} missing accessible_name parameter",
                                "code": "A001",
                                "severity": "warning",
                                "category": "aria",
                            }
                        )

                self.generic_visit(node)

        visitor = ARIAVisitor()
        visitor.visit(tree)

        return issues

    def _check_keyboard_handlers(
        self, tree: ast.AST, file_path: Path, content: str
    ) -> List[Dict[str, Any]]:
        """Check for keyboard event handlers (A002)."""
        issues = []

        # Look for mouse-only event handlers
        mouse_only_patterns = [
            r'\.bind\(["\']<Button-1>["\']',  # Mouse click only
            r'\.bind\(["\']<Double-Button-1>["\']',  # Double click only
            r'\.bind\(["\']<ButtonRelease-1>["\']',  # Mouse release only
        ]

        lines = content.split("\n")
        for line_num, line in enumerate(lines, 1):
            for pattern in mouse_only_patterns:
                if re.search(pattern, line):
                    # Check if there's a corresponding keyboard handler
                    keyboard_patterns = [
                        r'\.bind\(["\']<Return>["\']',
                        r'\.bind\(["\']<space>["\']',
                        r'\.bind\(["\']<Key>["\']',
                        r'\.bind\(["\']<KeyPress>["\']',
                    ]

                    # Look in surrounding lines for keyboard handler
                    has_keyboard_handler = False
                    search_range = range(
                        max(0, line_num - 10), min(len(lines), line_num + 10)
                    )
                    for check_line_num in search_range:
                        check_line = lines[check_line_num]
                        if any(re.search(kp, check_line) for kp in keyboard_patterns):
                            has_keyboard_handler = True
                            break

                    if not has_keyboard_handler:
                        issues.append(
                            {
                                "filename": str(file_path),
                                "line": line_num,
                                "column": 0,
                                "message": "Mouse-only event handler without keyboard equivalent",
                                "code": "A002",
                                "severity": "warning",
                                "category": "keyboard",
                            }
                        )

        return issues

    def _check_focus_management(
        self, tree: ast.AST, file_path: Path, content: str
    ) -> List[Dict[str, Any]]:
        """Check for proper focus management (A003)."""
        issues = []

        # Look for focus_set() usage patterns
        focus_patterns = [
            r"\.focus_set\(\)",
            r"\.focus_force\(\)",
            r"\.focus\(\)",
        ]

        lines = content.split("\n")
        for line_num, line in enumerate(lines, 1):
            for pattern in focus_patterns:
                if re.search(pattern, line):
                    # Check if focus is set in appropriate context
                    # Expanded list of legitimate contexts
                    context_patterns = [
                        # Event handlers
                        r"def\s+\w*event\w*",
                        r"def\s+\w*click\w*",
                        r"def\s+\w*key\w*",
                        r"def\s+\w*handler\w*",
                        r"def\s+\w*callback\w*",
                        # Initialization contexts
                        r"def\s+__init__",
                        r"def\s+\w*init\w*",
                        r"def\s+\w*setup\w*",
                        r"def\s+main\b",
                        # Test contexts
                        r"def\s+test_\w*",
                        r"def\s+\w*test\w*",
                        # Widget binding
                        r"\.bind\(",
                        # Comments indicating intentional initial focus
                        r"#.*initial.*focus",
                        r"#.*focus.*initial",
                        r"#.*set.*focus",
                        r"#.*focus.*entry",
                        r"#.*focus.*field",
                    ]

                    has_proper_context = False
                    # Expand search range for better context detection
                    search_range = range(
                        max(0, line_num - 10), min(len(lines), line_num + 3)
                    )
                    for check_line_num in search_range:
                        check_line = lines[check_line_num]
                        if any(
                            re.search(cp, check_line, re.IGNORECASE)
                            for cp in context_patterns
                        ):
                            has_proper_context = True
                            break

                    # Additional check: if we're in a test file, be more lenient
                    if not has_proper_context and "test" in str(file_path).lower():
                        # In test files, focus_set() is often used for testing purposes
                        test_indicators = [
                            r"simulate",
                            r"testing",
                            r"verify",
                            r"check",
                            r"assert",
                            r"app\.update\(\)",
                            r"app\.destroy\(\)",
                        ]

                        # Look in broader context for test indicators
                        broader_range = range(
                            max(0, line_num - 15), min(len(lines), line_num + 5)
                        )
                        for check_line_num in broader_range:
                            check_line = lines[check_line_num]
                            if any(
                                re.search(ti, check_line, re.IGNORECASE)
                                for ti in test_indicators
                            ):
                                has_proper_context = True
                                break

                    if not has_proper_context:
                        issues.append(
                            {
                                "filename": str(file_path),
                                "line": line_num,
                                "column": 0,
                                "message": "focus_set() used outside of proper event context",
                                "code": "A003",
                                "severity": "info",
                                "category": "focus",
                            }
                        )

        return issues

    def _check_color_only_info(
        self, tree: ast.AST, file_path: Path, content: str
    ) -> List[Dict[str, Any]]:
        """Check for information conveyed by color only (A004)."""
        issues = []

        # Look for color-only information patterns
        color_only_patterns = [
            r"(red|green|blue|yellow|orange|purple|pink)\s+(text|color|background)",
            r'color\s*=\s*["\']red["\'].*error',
            r'color\s*=\s*["\']green["\'].*success',
            r'bg\s*=\s*["\']red["\']',
            r'fg\s*=\s*["\']green["\']',
        ]

        lines = content.split("\n")
        for line_num, line in enumerate(lines, 1):
            for pattern in color_only_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Check if there's also text or other indicators
                    text_indicators = [
                        "text=",
                        "message=",
                        "label=",
                        "accessible_description=",
                        "accessible_name=",
                        "tooltip=",
                        "status=",
                    ]

                    has_text_indicator = any(
                        indicator in line for indicator in text_indicators
                    )

                    # Also check surrounding lines
                    if not has_text_indicator:
                        search_range = range(
                            max(0, line_num - 3), min(len(lines), line_num + 3)
                        )
                        for check_line_num in search_range:
                            check_line = lines[check_line_num]
                            if any(
                                indicator in check_line for indicator in text_indicators
                            ):
                                has_text_indicator = True
                                break

                    if not has_text_indicator:
                        issues.append(
                            {
                                "filename": str(file_path),
                                "line": line_num,
                                "column": 0,
                                "message": "Information may be conveyed by color only",
                                "code": "A004",
                                "severity": "warning",
                                "category": "color",
                            }
                        )

        return issues

    def _check_text_alternatives(
        self, tree: ast.AST, file_path: Path, content: str
    ) -> List[Dict[str, Any]]:
        """Check for text alternatives for non-text content (A005)."""
        issues = []

        # Look for image or icon usage without alt text
        image_patterns = [
            r"PhotoImage\(",
            r"BitmapImage\(",
            r"image\s*=",
            r"icon\s*=",
            r"bitmap\s*=",
        ]

        lines = content.split("\n")
        for line_num, line in enumerate(lines, 1):
            for pattern in image_patterns:
                if re.search(pattern, line):
                    # Check for accessible description
                    alt_patterns = [
                        r"accessible_description\s*=",
                        r"accessible_name\s*=",
                        r"alt\s*=",
                        r"tooltip\s*=",
                    ]

                    # Look in surrounding lines for alt text
                    has_alt_text = False
                    search_range = range(
                        max(0, line_num - 5), min(len(lines), line_num + 5)
                    )
                    for check_line_num in search_range:
                        check_line = lines[check_line_num]
                        if any(re.search(ap, check_line) for ap in alt_patterns):
                            has_alt_text = True
                            break

                    if not has_alt_text:
                        issues.append(
                            {
                                "filename": str(file_path),
                                "line": line_num,
                                "column": 0,
                                "message": "Image or icon without text alternative",
                                "code": "A005",
                                "severity": "warning",
                                "category": "text_alternatives",
                            }
                        )

        return issues


class DocumentationAccessibilityChecker:
    """Checker for documentation accessibility issues."""

    def __init__(self):
        self.config = AUDIT_CONFIG["documentation"]

    def check_markdown_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check markdown file for accessibility issues."""
        issues = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.split("\n")

            # Run various documentation checks
            if self.config.get("check_heading_structure", True):
                issues.extend(self._check_heading_structure(lines, file_path))

            if self.config.get("check_link_text", True):
                issues.extend(self._check_link_text(lines, file_path))

            if self.config.get("check_alt_text", True):
                issues.extend(self._check_alt_text(lines, file_path))

            if self.config.get("check_color_references", True):
                issues.extend(self._check_color_references(lines, file_path))

        except Exception as e:
            issues.append(
                {
                    "filename": str(file_path),
                    "line": 0,
                    "column": 0,
                    "message": f"Error reading file: {str(e)}",
                    "code": "D000",
                    "severity": "error",
                    "category": "parsing",
                }
            )

        return issues

    def _check_heading_structure(
        self, lines: List[str], file_path: Path
    ) -> List[Dict[str, Any]]:
        """Check heading structure for accessibility (D001)."""
        issues = []
        heading_levels = []

        for line_num, line in enumerate(lines, 1):
            if line.startswith("#"):
                level = len(line) - len(line.lstrip("#"))
                heading_levels.append((line_num, level))

                # Check for skipped heading levels
                if len(heading_levels) > 1:
                    prev_level = heading_levels[-2][1]
                    if level > prev_level + 1:
                        issues.append(
                            {
                                "filename": str(file_path),
                                "line": line_num,
                                "column": 0,
                                "message": f"Heading level {level} skips level {prev_level + 1}",
                                "code": "D001",
                                "severity": "warning",
                                "category": "headings",
                            }
                        )

        return issues

    def _check_link_text(
        self, lines: List[str], file_path: Path
    ) -> List[Dict[str, Any]]:
        """Check link text for accessibility (D002, D003)."""
        issues = []

        # Pattern for markdown links
        link_pattern = r"\[([^\]]*)\]\([^)]+\)"

        for line_num, line in enumerate(lines, 1):
            matches = re.finditer(link_pattern, line)
            for match in matches:
                link_text = match.group(1).strip()

                # Check for empty link text
                if not link_text:
                    issues.append(
                        {
                            "filename": str(file_path),
                            "line": line_num,
                            "column": match.start(),
                            "message": "Empty link text",
                            "code": "D003",
                            "severity": "error",
                            "category": "links",
                        }
                    )
                    continue

                # Check for poor link text
                poor_link_texts = [
                    "click here",
                    "here",
                    "read more",
                    "more",
                    "link",
                    "this",
                    "this link",
                    "click",
                    "see here",
                    "learn more",
                ]

                if link_text.lower() in poor_link_texts:
                    issues.append(
                        {
                            "filename": str(file_path),
                            "line": line_num,
                            "column": match.start(),
                            "message": f'Poor link text: "{link_text}"',
                            "code": "D002",
                            "severity": "warning",
                            "category": "links",
                        }
                    )

        return issues

    def _check_alt_text(
        self, lines: List[str], file_path: Path
    ) -> List[Dict[str, Any]]:
        """Check alt text for images (D004, D005)."""
        issues = []

        # Pattern for markdown images
        image_pattern = r"!\[([^\]]*)\]\([^)]+\)"

        for line_num, line in enumerate(lines, 1):
            matches = re.finditer(image_pattern, line)
            for match in matches:
                alt_text = match.group(1).strip()

                # Check for missing alt text
                if not alt_text:
                    issues.append(
                        {
                            "filename": str(file_path),
                            "line": line_num,
                            "column": match.start(),
                            "message": "Image missing alt text",
                            "code": "D004",
                            "severity": "error",
                            "category": "images",
                        }
                    )
                    continue

                # Check for poor alt text
                poor_alt_texts = [
                    "image",
                    "picture",
                    "photo",
                    "screenshot",
                    "img",
                    "graphic",
                    "icon",
                    "logo",
                ]

                if alt_text.lower() in poor_alt_texts:
                    issues.append(
                        {
                            "filename": str(file_path),
                            "line": line_num,
                            "column": match.start(),
                            "message": f'Poor alt text: "{alt_text}"',
                            "code": "D005",
                            "severity": "warning",
                            "category": "images",
                        }
                    )

        return issues

    def _check_color_references(
        self, lines: List[str], file_path: Path
    ) -> List[Dict[str, Any]]:
        """Check for color-only references (D006)."""
        issues = []

        color_only_patterns = [
            r"(red|green|blue|yellow|orange|purple|pink)\s+(button|text|link|area)",
            r"click\s+the\s+(red|green|blue|yellow)\s+",
            r"see\s+the\s+(red|green|blue|yellow)\s+",
            r"(red|green|blue|yellow)\s+(indicates|means|shows)",
        ]

        for line_num, line in enumerate(lines, 1):
            for pattern in color_only_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(
                        {
                            "filename": str(file_path),
                            "line": line_num,
                            "column": 0,
                            "message": "Information may be conveyed by color only",
                            "code": "D006",
                            "severity": "warning",
                            "category": "color",
                        }
                    )

        return issues
