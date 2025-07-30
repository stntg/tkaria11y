# a11y_audit/config.py

"""
Configuration for accessibility audit tools.
"""

from pathlib import Path

# Audit configuration
AUDIT_ROOT = Path(__file__).parent
PROJECT_ROOT = AUDIT_ROOT.parent
REPORTS_DIR = AUDIT_ROOT / "reports"
CONFIGS_DIR = AUDIT_ROOT / "configs"

# Ensure directories exist
REPORTS_DIR.mkdir(exist_ok=True)
CONFIGS_DIR.mkdir(exist_ok=True)

# Source directories to audit
SOURCE_DIRS = [
    PROJECT_ROOT / "tkaria11y",
    PROJECT_ROOT / "examples",
    PROJECT_ROOT / "tests",
]

# File patterns to exclude
EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    ".git",
    ".pytest_cache",
    "build",
    "dist",
    "*.egg-info",
    "a11y_test_suite",  # Exclude test suite from audit
    "a11y_audit/reports",  # Exclude audit reports
]

# Audit configuration
AUDIT_CONFIG = {
    "linting": {
        "flake8": {
            "enabled": True,
            "max_line_length": 88,
            "ignore": ["E203", "W503", "E501"],
            "plugins": ["flake8-docstrings", "flake8-import-order", "flake8-naming"],
        },
        "pylint": {
            "enabled": True,
            "disable": ["C0114", "C0115", "C0116", "R0903", "R0913"],
            "max_line_length": 88,
        },
        "mypy": {"enabled": True, "strict": True, "ignore_missing_imports": True},
    },
    "code_patterns": {
        "check_aria_attributes": True,
        "check_keyboard_handlers": True,
        "check_focus_management": True,
        "check_color_only_info": True,
        "check_text_alternatives": True,
    },
    "documentation": {
        "check_heading_structure": True,
        "check_link_text": True,
        "check_alt_text": True,
        "check_color_references": True,
    },
    "wcag": {"level": "AA", "version": "2.1"},  # A, AA, or AAA
    "reporting": {
        "formats": ["json", "txt"],
        "include_context": True,
        "max_issues_per_category": 50,
    },
}

# CI/CD configuration
CI_CONFIG = {
    "github_actions": {
        "enabled": True,
        "python_versions": ["3.9", "3.10", "3.11"],
        "fail_on_error": True,
        "upload_artifacts": True,
    },
    "pre_commit": {
        "enabled": True,
        "hooks": ["flake8", "mypy", "custom-a11y"],
        "fail_fast": False,
    },
}


def get_report_path(tool_name, format="json"):
    """Get path for audit report."""
    timestamp = __import__("time").strftime("%Y%m%d_%H%M%S")
    filename = f"{tool_name}_audit_{timestamp}.{format}"
    return REPORTS_DIR / filename


def get_config_path(tool_name):
    """Get path for tool configuration file."""
    config_files = {"flake8": ".flake8", "pylint": ".pylintrc", "mypy": "mypy.ini"}
    return CONFIGS_DIR / config_files.get(tool_name, f"{tool_name}.conf")
