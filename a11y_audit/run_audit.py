#!/usr/bin/env python3
# a11y_audit/run_audit.py

"""
Main accessibility compliance audit runner.

This script provides a command-line interface to run comprehensive
accessibility audits on the tkaria11y codebase using various linting
tools and custom accessibility checkers.
"""

import sys
import argparse
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from a11y_audit.linters import AccessibilityLinter
from a11y_audit.config import get_report_path, SOURCE_DIRS


class AccessibilityAuditRunner:
    """Main accessibility audit runner."""

    def __init__(self):
        self.results: Dict[str, Any] = {}
        self.start_time = time.time()
        self.settings = {
            "run_flake8": True,
            "run_pylint": True,
            "run_mypy": True,
            "run_custom_checks": True,
            "run_documentation_audit": True,
            "generate_reports": True,
            "fail_on_error": False,
            "fail_on_warning": False,
        }

    def run_full_audit(self, audit_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run full accessibility audit."""
        if audit_types is None:
            audit_types = ["all"]

        print("=" * 70)
        print("TKARIA11Y ACCESSIBILITY COMPLIANCE AUDIT")
        print("=" * 70)
        print(f"Audit types: {', '.join(audit_types)}")
        print(f"Source directories: {[str(d) for d in SOURCE_DIRS if d.exists()]}")
        print()

        # Initialize linter
        linter = AccessibilityLinter()

        # Run audits based on selection
        if "all" in audit_types or "linting" in audit_types:
            if self.settings["run_flake8"]:
                print("Running flake8 accessibility audit...")
                self.results["flake8"] = linter.run_flake8_audit()
                print()

            if self.settings["run_pylint"]:
                print("Running pylint code quality audit...")
                self.results["pylint"] = linter.run_pylint_audit()
                print()

            if self.settings["run_mypy"]:
                print("Running mypy type checking audit...")
                self.results["mypy"] = linter.run_mypy_audit()
                print()

        if "all" in audit_types or "custom" in audit_types:
            if self.settings["run_custom_checks"]:
                print("Running custom accessibility checks...")
                self.results["custom_checks"] = linter.run_custom_accessibility_checks()
                print()

        if "all" in audit_types or "documentation" in audit_types:
            if self.settings["run_documentation_audit"]:
                print("Running documentation accessibility audit...")
                self.results["documentation"] = linter.run_documentation_audit()
                print()

        return self.results

    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive audit report."""
        end_time = time.time()
        duration = end_time - self.start_time

        report = []
        report.append("TKARIA11Y ACCESSIBILITY COMPLIANCE AUDIT REPORT")
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
        for source_dir in SOURCE_DIRS:
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
        tools_run = 0
        tools_skipped = 0

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
            elif status == "SKIPPED":
                tools_skipped += 1

        report.append("")
        report.append("STATISTICS:")
        report.append(f"  Tools run successfully: {tools_run}")
        report.append(f"  Tools skipped: {tools_skipped}")
        report.append(f"  Total issues found: {total_issues}")
        report.append("")

        if total_issues > 0:
            report.append("ISSUES BY SEVERITY:")
            if error_issues > 0:
                report.append(f"  ✗ Errors: {error_issues}")
            if warning_issues > 0:
                report.append(f"  ⚠ Warnings: {warning_issues}")
            report.append("")

        # Recommendations
        if tools_skipped > 0:
            report.append("RECOMMENDATIONS:")
            report.append("  SETUP:")
            report.append("    • Install missing linting tools")

        if total_issues == 0 and tools_run > 0:
            report.append("RECOMMENDATIONS:")
            report.append("  ✓ EXCELLENT:")
            report.append("    • No accessibility issues found!")

        return "\n".join(report)

    def save_results(self, format="json") -> Path:
        """Save audit results to file."""
        if format == "json":
            report_file = get_report_path("accessibility_audit", "json")
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "timestamp": time.time(),
                        "audit_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "settings": self.settings,
                        "results": self.results,
                        "summary": self.generate_comprehensive_report(),
                    },
                    f,
                    indent=2,
                )
        else:
            report_file = get_report_path("accessibility_audit", "txt")
            with open(report_file, "w", encoding="utf-8") as f:
                f.write(self.generate_comprehensive_report())

        return report_file

    def check_exit_conditions(self) -> int:
        """Check if audit should exit with error code."""
        if not self.results:
            return 0

        error_count = 0
        warning_count = 0

        for result in self.results.values():
            if "issues" in result:
                for issue in result["issues"]:
                    severity = issue.get("severity", "warning")
                    if severity == "error":
                        error_count += 1
                    elif severity == "warning":
                        warning_count += 1

        if self.settings["fail_on_error"] and error_count > 0:
            return 1

        if self.settings["fail_on_warning"] and warning_count > 0:
            return 1

        return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run tkaria11y accessibility compliance audit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Audit Types:
  all           Run all audit types (default)
  linting       Run code linting tools (flake8, pylint, mypy)
  custom        Run custom accessibility checks
  documentation Run documentation accessibility audit

Examples:
  python a11y_audit/run_audit.py                    # Run all audits
  python a11y_audit/run_audit.py --type linting     # Run only linting tools
  python a11y_audit/run_audit.py --type custom      # Run only custom checks
  python a11y_audit/run_audit.py --fail-on-error    # Exit with error if issues found
        """,
    )

    # Audit type selection
    parser.add_argument(
        "--type",
        choices=["all", "linting", "custom", "documentation"],
        default="all",
        help="Type of audit to run",
    )

    # Tool selection
    parser.add_argument("--no-flake8", action="store_true", help="Skip flake8 linting")
    parser.add_argument("--no-pylint", action="store_true", help="Skip pylint linting")
    parser.add_argument(
        "--no-mypy", action="store_true", help="Skip mypy type checking"
    )
    parser.add_argument(
        "--no-custom", action="store_true", help="Skip custom accessibility checks"
    )
    parser.add_argument(
        "--no-docs", action="store_true", help="Skip documentation audit"
    )

    # Options
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Exit with error code if error-level issues found",
    )
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Exit with error code if warning-level issues found",
    )
    parser.add_argument(
        "--no-reports", action="store_true", help="Do not generate report files"
    )
    parser.add_argument(
        "--format",
        choices=["txt", "json"],
        default="json",
        help="Report format (default: json)",
    )
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")

    # Information
    parser.add_argument(
        "--list-tools", action="store_true", help="List available audit tools"
    )
    parser.add_argument("--version", action="version", version="tkaria11y audit v1.0")

    args = parser.parse_args()

    # Handle list tools
    if args.list_tools:
        print("Available audit tools:")
        print("  flake8        - Code style and accessibility linting")
        print("  pylint        - Code quality and accessibility analysis")
        print("  mypy          - Static type checking")
        print("  custom        - Custom accessibility pattern checking")
        print("  documentation - Documentation accessibility audit")
        return

    try:
        # Create and configure runner
        runner = AccessibilityAuditRunner()

        # Configure tool selection
        if args.no_flake8:
            runner.settings["run_flake8"] = False
        if args.no_pylint:
            runner.settings["run_pylint"] = False
        if args.no_mypy:
            runner.settings["run_mypy"] = False
        if args.no_custom:
            runner.settings["run_custom_checks"] = False
        if args.no_docs:
            runner.settings["run_documentation_audit"] = False

        # Configure exit conditions
        if args.fail_on_error:
            runner.settings["fail_on_error"] = True
        if args.fail_on_warning:
            runner.settings["fail_on_warning"] = True

        # Configure reporting
        if args.no_reports:
            runner.settings["generate_reports"] = False

        # Run audit
        audit_types = [args.type] if args.type != "all" else ["all"]
        results = runner.run_full_audit(audit_types)

        # Generate and display report
        if not args.quiet:
            report = runner.generate_comprehensive_report()
            print(report)

        # Save results if requested
        if runner.settings["generate_reports"]:
            report_file = runner.save_results(args.format)
            if not args.quiet:
                print(f"\nDetailed report saved to: {report_file}")

        # Exit with appropriate code
        exit_code = runner.check_exit_conditions()
        sys.exit(exit_code)

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
