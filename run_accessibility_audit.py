#!/usr/bin/env python3
"""
Standalone Accessibility Compliance Audit for tkaria11y

This script runs a comprehensive accessibility audit on the tkaria11y codebase
to identify potential accessibility issues and compliance problems.
"""

import sys
import argparse
import json
import time
import ast
import re
import subprocess
from pathlib import Path
from typing import Dict, Any, List


class AccessibilityAuditor:
    """Main accessibility auditor."""

    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        self.project_root = Path(__file__).parent

        # Source directories to audit
        self.source_dirs = [
            self.project_root / "tkaria11y",
            self.project_root / "examples",
            self.project_root / "tests",
        ]

        # Patterns to exclude
        self.exclude_patterns = [
            "__pycache__",
            "*.pyc",
            ".git",
            ".pytest_cache",
            "build",
            "dist",
            "*.egg-info",
            "a11y_test_suite",
        ]

    def run_flake8_audit(self) -> Dict[str, Any]:
        """Run flake8 with accessibility focus."""
        print("Running flake8 accessibility audit...")

        try:
            # Check if flake8 is available
            result = subprocess.run(
                ["flake8", "--version"], capture_output=True, text=True
            )
            if result.returncode != 0:
                return {
                    "status": "SKIPPED",
                    "message": "flake8 not available - install with: pip install flake8",
                }

            # Build flake8 command
            cmd = ["flake8", "--max-line-length=88", "--ignore=E203,W503"]

            # Add source directories
            for source_dir in self.source_dirs:
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

    def run_custom_accessibility_checks(self) -> Dict[str, Any]:
        """Run custom accessibility-specific checks."""
        print("Running custom accessibility checks...")

        try:
            checker = CustomAccessibilityChecker(self.exclude_patterns)
            issues = []

            for source_dir in self.source_dirs:
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
        """Audit documentation for accessibility."""
        print("Running documentation accessibility audit...")

        try:
            doc_checker = DocumentationAccessibilityChecker()
            issues = []

            # Check markdown files in source directories
            for source_dir in self.source_dirs:
                if source_dir.exists():
                    for md_file in source_dir.rglob("*.md"):
                        issues.extend(doc_checker.check_markdown_file(md_file))

            # Check README files
            readme_files = [
                self.project_root / "README.md",
                self.project_root / "docs" / "README.md",
                self.project_root / "examples" / "README.md",
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
                    issues.append(
                        {
                            "filename": parts[0],
                            "line": int(parts[1]) if parts[1].isdigit() else 0,
                            "column": int(parts[2]) if parts[2].isdigit() else 0,
                            "message": parts[3].strip(),
                            "code": "",
                            "severity": "warning",
                            "category": "style",
                        }
                    )
        return issues

    def run_all_audits(self) -> Dict[str, Any]:
        """Run all accessibility audits."""
        print("=" * 70)
        print("TKARIA11Y ACCESSIBILITY COMPLIANCE AUDIT")
        print("=" * 70)
        print()

        # Run audits
        self.results["flake8"] = self.run_flake8_audit()
        print()

        self.results["custom_checks"] = self.run_custom_accessibility_checks()
        print()

        self.results["documentation"] = self.run_documentation_audit()
        print()

        return self.results

    def generate_summary_report(self) -> str:
        """Generate summary report of all audit results."""
        end_time = time.time()
        duration = end_time - self.start_time

        report = []
        report.append("ACCESSIBILITY COMPLIANCE AUDIT REPORT")
        report.append("=" * 70)
        report.append(f"Audit Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Duration: {duration:.2f} seconds")
        report.append("")

        # Environment information
        import platform

        report.append("ENVIRONMENT:")
        report.append(f"  Platform: {platform.platform()}")
        report.append(f"  Python: {sys.version.split()[0]}")
        report.append(f"  Working Directory: {Path.cwd()}")
        report.append("")

        # Audit scope
        report.append("AUDIT SCOPE:")
        for source_dir in self.source_dirs:
            if source_dir.exists():
                py_files = list(source_dir.rglob("*.py"))
                md_files = list(source_dir.rglob("*.md"))
                report.append(
                    f"  {source_dir.name}: {len(py_files)} Python files, {len(md_files)} Markdown files"
                )
        report.append("")

        # Results summary
        report.append("AUDIT RESULTS SUMMARY:")

        total_issues = 0
        error_issues = 0
        warning_issues = 0
        info_issues = 0
        tools_run = 0
        tools_skipped = 0
        tools_error = 0

        for tool_name, result in self.results.items():
            status = result.get("status", "UNKNOWN")
            issues_count = result.get("issues_found", 0)
            message = result.get("message", "No message")

            status_symbol = {"COMPLETED": "✓", "SKIPPED": "○", "ERROR": "✗"}.get(
                status, "?"
            )

            report.append(f"{status_symbol} {tool_name.upper()}: {status}")
            report.append(f"  {message}")

            if status == "COMPLETED":
                tools_run += 1
                total_issues += issues_count

                # Count issues by severity
                if "issues" in result:
                    for issue in result["issues"]:
                        severity = issue.get("severity", "warning")
                        if severity == "error":
                            error_issues += 1
                        elif severity == "warning":
                            warning_issues += 1
                        elif severity == "info":
                            info_issues += 1
            elif status == "SKIPPED":
                tools_skipped += 1
            elif status == "ERROR":
                tools_error += 1

        report.append("")
        report.append("STATISTICS:")
        report.append(f"  Tools run successfully: {tools_run}")
        report.append(f"  Tools skipped: {tools_skipped}")
        report.append(f"  Tools with errors: {tools_error}")
        report.append(f"  Total issues found: {total_issues}")
        report.append("")

        if total_issues > 0:
            report.append("ISSUES BY SEVERITY:")
            if error_issues > 0:
                report.append(f"  ✗ Errors: {error_issues}")
            if warning_issues > 0:
                report.append(f"  ⚠ Warnings: {warning_issues}")
            if info_issues > 0:
                report.append(f"  ℹ Info: {info_issues}")
            report.append("")

        # Issue breakdown by category
        category_counts = {}
        for tool_result in self.results.values():
            if "issues" in tool_result:
                for issue in tool_result["issues"]:
                    category = issue.get("category", "general")
                    category_counts[category] = category_counts.get(category, 0) + 1

        if category_counts:
            report.append("ISSUES BY CATEGORY:")
            for category, count in sorted(category_counts.items()):
                report.append(f"  {category.title()}: {count}")
            report.append("")

        # Top issues
        all_issues = []
        for tool_result in self.results.values():
            if "issues" in tool_result:
                all_issues.extend(tool_result["issues"])

        if all_issues:
            # Group by message for top issues
            message_counts = {}
            for issue in all_issues:
                msg = issue.get("message", "Unknown issue")
                message_counts[msg] = message_counts.get(msg, 0) + 1

            top_issues = sorted(
                message_counts.items(), key=lambda x: x[1], reverse=True
            )[:5]

            if top_issues:
                report.append("TOP ISSUES:")
                for i, (message, count) in enumerate(top_issues, 1):
                    report.append(f"  {i}. {message} ({count} occurrences)")
                report.append("")

        # Recommendations
        report.append("RECOMMENDATIONS:")

        if tools_skipped > 0:
            report.append("  SETUP:")
            report.append("    • Install missing linting tools:")
            report.append("      pip install flake8 pylint mypy")

        if error_issues > 0:
            report.append("  CRITICAL:")
            report.append(
                f"    • Fix {error_issues} error-level accessibility issues immediately"
            )
            report.append(
                "    • These issues may prevent proper accessibility functionality"
            )

        if warning_issues > 0:
            report.append("  IMPORTANT:")
            report.append(
                f"    • Review and address {warning_issues} warning-level issues"
            )
            report.append("    • These issues may impact accessibility experience")

        if "aria" in category_counts:
            report.append("  ACCESSIBILITY:")
            report.append(f"    • Fix {category_counts['aria']} ARIA-related issues")
            report.append(
                "    • Ensure all interactive elements have proper accessible names"
            )

        if "keyboard" in category_counts:
            report.append(
                f"    • Address {category_counts['keyboard']} keyboard accessibility issues"
            )
            report.append("    • Ensure all functionality is keyboard accessible")

        if "color" in category_counts:
            report.append(
                f"    • Fix {category_counts['color']} color-related accessibility issues"
            )
            report.append("    • Ensure information is not conveyed by color alone")

        if total_issues == 0 and tools_run > 0:
            report.append("  ✓ EXCELLENT:")
            report.append("    • No accessibility issues found!")
            report.append("    • Your codebase follows accessibility best practices")
            report.append("    • Consider running periodic audits to maintain quality")

        # Next steps
        report.append("")
        report.append("NEXT STEPS:")
        report.append("  1. Review detailed issue reports below")
        report.append("  2. Fix high-priority issues first (errors, then warnings)")
        report.append("  3. Run audit again to verify fixes")
        report.append("  4. Consider integrating audit into development workflow")

        return "\n".join(report)


class CustomAccessibilityChecker:
    """Custom accessibility checker for Python code."""

    def __init__(self, exclude_patterns):
        self.exclude_patterns = exclude_patterns

    def check_directory(self, directory: Path) -> List[Dict[str, Any]]:
        """Check all Python files in directory."""
        issues = []

        for py_file in directory.rglob("*.py"):
            # Skip excluded patterns
            if any(pattern in str(py_file) for pattern in self.exclude_patterns):
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

            # Run various checks
            issues.extend(self._check_aria_attributes(tree, file_path, content))
            issues.extend(self._check_keyboard_handlers(tree, file_path, content))
            issues.extend(self._check_color_only_info(tree, file_path, content))
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
        """Check for proper ARIA attribute usage."""
        issues = []

        class ARIAVisitor(ast.NodeVisitor):
            def visit_Call(self, node):
                # Check for widget creation without accessible_name
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
        """Check for keyboard event handlers."""
        issues = []

        # Look for mouse-only event handlers
        mouse_only_patterns = [
            r'\.bind\(["\']<Button-1>["\']',  # Mouse click only
            r'\.bind\(["\']<Double-Button-1>["\']',  # Double click only
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
                    ]

                    # Look in surrounding lines for keyboard handler
                    has_keyboard_handler = False
                    for check_line in lines[
                        max(0, line_num - 5) : min(len(lines), line_num + 5)
                    ]:
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

    def _check_color_only_info(
        self, tree: ast.AST, file_path: Path, content: str
    ) -> List[Dict[str, Any]]:
        """Check for information conveyed by color only."""
        issues = []

        # Look for color-only information patterns
        color_only_patterns = [
            r"(red|green|blue|yellow)\s+(text|color|background)",
            r'color\s*=\s*["\']red["\'].*error',
            r'color\s*=\s*["\']green["\'].*success',
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
                    ]
                    has_text_indicator = any(
                        indicator in line for indicator in text_indicators
                    )

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
        """Check for text alternatives for non-text content."""
        issues = []

        # Look for image or icon usage without alt text
        image_patterns = [
            r"PhotoImage\(",
            r"BitmapImage\(",
            r"image\s*=",
            r"icon\s*=",
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
                    ]

                    # Look in surrounding lines for alt text
                    has_alt_text = False
                    for check_line in lines[
                        max(0, line_num - 3) : min(len(lines), line_num + 3)
                    ]:
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
    """Checker for documentation accessibility."""

    def check_markdown_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check markdown file for accessibility issues."""
        issues = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.split("\n")

            # Check various accessibility aspects
            issues.extend(self._check_heading_structure(lines, file_path))
            issues.extend(self._check_link_text(lines, file_path))
            issues.extend(self._check_alt_text(lines, file_path))
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
        """Check heading structure for accessibility."""
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
        """Check link text for accessibility."""
        issues = []

        # Pattern for markdown links
        link_pattern = r"\[([^\]]*)\]\([^)]+\)"

        for line_num, line in enumerate(lines, 1):
            matches = re.finditer(link_pattern, line)
            for match in matches:
                link_text = match.group(1).strip()

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

        return issues

    def _check_alt_text(
        self, lines: List[str], file_path: Path
    ) -> List[Dict[str, Any]]:
        """Check alt text for images."""
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

                # Check for poor alt text
                poor_alt_texts = ["image", "picture", "photo", "screenshot", "img"]

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
        """Check for color-only references."""
        issues = []

        color_only_patterns = [
            r"(red|green|blue|yellow|orange|purple|pink)\s+(button|text|link|area)",
            r"click\s+the\s+(red|green|blue|yellow)\s+",
            r"see\s+the\s+(red|green|blue|yellow)\s+",
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


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run tkaria11y accessibility compliance audit"
    )

    parser.add_argument(
        "--format",
        choices=["txt", "json"],
        default="txt",
        help="Report format (default: txt)",
    )
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Exit with error code if error-level issues found",
    )
    parser.add_argument(
        "--save-report", action="store_true", help="Save detailed report to file"
    )

    args = parser.parse_args()

    try:
        # Create and run auditor
        auditor = AccessibilityAuditor()
        results = auditor.run_all_audits()

        # Generate and display report
        report = auditor.generate_summary_report()
        print(report)

        # Show detailed issues if any found
        total_issues = sum(result.get("issues_found", 0) for result in results.values())
        if total_issues > 0:
            print("\n" + "=" * 70)
            print("DETAILED ISSUE REPORT")
            print("=" * 70)

            for tool_name, result in results.items():
                if result.get("issues"):
                    print(f"\n{tool_name.upper()} ISSUES:")
                    print("-" * 40)

                    for issue in result["issues"]:
                        filename = Path(issue["filename"]).name
                        line = issue.get("line", 0)
                        code = issue.get("code", "")
                        severity = issue.get("severity", "warning").upper()
                        message = issue.get("message", "")

                        print(f"  {severity} [{code}] {filename}:{line}")
                        print(f"    {message}")
                        print()

        # Save report if requested
        if args.save_report:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            report_file = f"accessibility_audit_{timestamp}.{args.format}"

            if args.format == "json":
                with open(report_file, "w") as f:
                    json.dump(
                        {
                            "timestamp": time.time(),
                            "audit_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "results": results,
                            "summary": report,
                        },
                        f,
                        indent=2,
                    )
            else:
                with open(report_file, "w", encoding="utf-8") as f:
                    f.write(report)
                    if total_issues > 0:
                        f.write("\n\nDETAILED ISSUES:\n")
                        for tool_name, result in results.items():
                            if result.get("issues"):
                                f.write(f"\n{tool_name.upper()} ISSUES:\n")
                                for issue in result["issues"]:
                                    f.write(
                                        f"  {issue.get('severity', 'warning').upper()} [{issue.get('code', '')}] "
                                    )
                                    f.write(
                                        f"{Path(issue['filename']).name}:{issue.get('line', 0)}\n"
                                    )
                                    f.write(f"    {issue.get('message', '')}\n")

            print(f"\nDetailed report saved to: {report_file}")

        # Exit with appropriate code
        if args.fail_on_error:
            error_count = sum(
                len(
                    [
                        issue
                        for issue in result.get("issues", [])
                        if issue.get("severity") == "error"
                    ]
                )
                for result in results.values()
                if isinstance(result, dict) and "issues" in result
            )
            sys.exit(1 if error_count > 0 else 0)

    except KeyboardInterrupt:
        print("\nAccessibility audit interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Error running accessibility audit: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
