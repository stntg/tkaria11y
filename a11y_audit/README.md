# Accessibility Compliance Audit System

A comprehensive automated accessibility compliance audit system for the tkaria11y codebase. This system uses multiple linting tools, custom accessibility checkers, and automated analysis to ensure code meets accessibility standards and best practices.

## Overview

The audit system provides:

1. **Automated Linting** - Using flake8, pylint, and mypy with accessibility-focused configurations
2. **Custom Accessibility Checks** - Python AST analysis for accessibility patterns
3. **Documentation Audits** - Markdown and documentation accessibility validation
4. **CI/CD Integration** - GitHub Actions, pre-commit hooks, and VS Code integration
5. **Comprehensive Reporting** - Detailed reports with actionable recommendations

## Quick Start

### Basic Usage

```bash
# Run complete accessibility audit
python a11y_audit/run_audit.py

# Run specific audit types
python a11y_audit/run_audit.py --type linting
python a11y_audit/run_audit.py --type custom
python a11y_audit/run_audit.py --type documentation

# Fail on errors (useful for CI)
python a11y_audit/run_audit.py --fail-on-error
```

### Installation

```bash
# Install required linting tools
pip install flake8 pylint mypy
pip install flake8-docstrings flake8-import-order flake8-naming

# Optional: Install pre-commit for automated checks
pip install pre-commit
```

## Audit Types

### 1. Automated Linting

Uses industry-standard tools with accessibility-focused configurations:

#### Flake8 (Code Style + Accessibility)

- **Configuration**: `configs/.flake8`
- **Plugins**: flake8-docstrings, flake8-import-order, flake8-naming
- **Focus**: Code style, documentation, accessibility patterns
- **Custom Rules**: ARIA attributes, keyboard handlers, color usage

#### Pylint (Code Quality)

- **Configuration**: `configs/.pylintrc`
- **Focus**: Code quality, accessibility best practices
- **Custom Checks**: Accessibility-specific patterns and conventions

#### MyPy (Type Checking)

- **Configuration**: `configs/mypy.ini`
- **Focus**: Type safety for accessibility APIs
- **Strict Mode**: Ensures proper typing for accessibility functions

### 2. Custom Accessibility Checks

Python AST-based analysis for accessibility-specific patterns:

#### ARIA Attributes (`A001`)

- Checks for missing `accessible_name` on interactive widgets
- Validates proper ARIA attribute usage
- Ensures semantic markup

#### Keyboard Accessibility (`A002`)

- Detects mouse-only event handlers without keyboard equivalents
- Validates keyboard navigation patterns
- Checks for proper focus management

#### Focus Management (`A003`)

- Analyzes `focus_set()` usage patterns
- Validates focus context and flow
- Ensures proper focus indicators

#### Color-Only Information (`A004`)

- Detects information conveyed by color alone
- Validates alternative text indicators
- Checks for proper contrast patterns

#### Text Alternatives (`A005`)

- Validates alt text for images and icons
- Checks for descriptive labels
- Ensures non-text content accessibility

### 3. Documentation Audits

Markdown and documentation accessibility validation:

#### Heading Structure (`D001`)

- Validates proper heading hierarchy
- Checks for skipped heading levels
- Ensures logical document structure

#### Link Text (`D002`, `D003`)

- Detects poor link text ("click here", "read more")
- Validates descriptive link text
- Checks for empty links

#### Image Alt Text (`D004`, `D005`)

- Validates alt text presence
- Checks for descriptive alt text
- Detects poor alt text patterns

#### Color References (`D006`)

- Detects color-only instructions
- Validates alternative descriptions
- Ensures inclusive documentation

## Configuration

### Tool Configurations

All linting tools use custom configurations optimized for accessibility:

- **`.flake8`** - Flake8 configuration with accessibility plugins
- **`.pylintrc`** - Pylint configuration with accessibility checks
- **`mypy.ini`** - MyPy configuration for type safety

### Audit Settings

Customize audit behavior in `config.py`:

```python
AUDIT_CONFIG = {
    'linting': {
        'flake8': {'enabled': True, 'max_line_length': 88},
        'pylint': {'enabled': True, 'disable': ['C0114']},
        'mypy': {'enabled': True, 'strict': True}
    },
    'code_patterns': {
        'check_aria_attributes': True,
        'check_keyboard_handlers': True,
        'check_focus_management': True,
        'check_color_only_info': True,
        'check_text_alternatives': True
    },
    'wcag': {
        'level': 'AA',  # A, AA, or AAA
        'version': '2.1'
    }
}
```

## Reports

### Report Formats

- **JSON** - Machine-readable detailed results
- **Text** - Human-readable summary reports
- **HTML** - Rich formatted reports (planned)

### Report Contents

- **Executive Summary** - High-level overview and statistics
- **Issue Breakdown** - By severity, category, and tool
- **Top Issues** - Most common problems
- **Recommendations** - Actionable next steps
- **Trend Analysis** - Issue tracking over time (planned)

### Sample Report Structure

```text
ACCESSIBILITY COMPLIANCE AUDIT REPORT
=====================================
Audit Date: 2024-01-15 14:30:00
Duration: 12.34 seconds

AUDIT RESULTS SUMMARY:
✓ FLAKE8: COMPLETED
  Found 3 accessibility issues
✓ CUSTOM_CHECKS: COMPLETED  
  Found 2 accessibility-specific issues
○ PYLINT: SKIPPED
  pylint not available

STATISTICS:
  Tools run successfully: 2
  Tools skipped: 1
  Total issues found: 5

ISSUES BY SEVERITY:
  ⚠ Warnings: 4
  ℹ Info: 1

RECOMMENDATIONS:
  SETUP:
    • Install missing linting tools
  IMPORTANT:
    • Review and address 4 warning-level issues
    • Fix 2 ARIA-related issues
```

## CI/CD Integration

### GitHub Actions

Automated workflow for pull requests and pushes:

```yaml
# .github/workflows/accessibility-audit.yml
name: Accessibility Audit
on: [push, pull_request]
jobs:
  accessibility-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run accessibility audit
        run: python a11y_audit/run_audit.py --fail-on-error
```

### Pre-commit Hooks

Automated checks before commits:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: accessibility-audit
        name: Accessibility Audit
        entry: python a11y_audit/run_audit.py --type custom --fail-on-error
        language: system
```

### VS Code Integration

IDE integration with tasks and settings:

- **Tasks** - Run audits from VS Code command palette
- **Settings** - Configured linters and formatters
- **Problem Matchers** - Display issues in Problems panel

## Command Line Options

```bash
# Audit type selection
--type {all,linting,custom,documentation}  # Type of audit to run

# Tool selection
--no-flake8        # Skip flake8 linting
--no-pylint        # Skip pylint linting  
--no-mypy          # Skip mypy type checking
--no-custom        # Skip custom accessibility checks
--no-docs          # Skip documentation audit

# Exit behavior
--fail-on-error    # Exit with error code if error-level issues found
--fail-on-warning  # Exit with error code if warning-level issues found

# Output control
--format {txt,json}  # Report format
--no-reports         # Don't generate report files
--quiet              # Reduce output verbosity

# Information
--list-tools       # List available audit tools
--version          # Show version information
```

## Development Workflow

### Local Development

```bash
# 1. Run quick check during development
python a11y_audit/run_audit.py --type custom --no-reports

# 2. Full audit before committing
python a11y_audit/run_audit.py --fail-on-error

# 3. Fix issues and re-run
python a11y_audit/run_audit.py --type linting
```

### Continuous Integration

```bash
# CI pipeline integration
python a11y_audit/run_audit.py --fail-on-error --format json

# Pre-commit hook
python a11y_audit/run_audit.py --type custom --fail-on-error --quiet
```

### Release Process

```bash
# 1. Full audit with strict settings
python a11y_audit/run_audit.py --fail-on-warning

# 2. Generate comprehensive report
python a11y_audit/run_audit.py --format txt

# 3. Review and address all issues
# 4. Re-run to verify fixes
```

## Troubleshooting

### Common Issues

1. **Tools not found**

   ```bash
   # Install missing tools
   pip install flake8 pylint mypy
   pip install flake8-docstrings flake8-import-order
   ```

2. **Configuration errors**

   ```bash
   # Check configuration files
   flake8 --config=a11y_audit/configs/.flake8 --version
   pylint --rcfile=a11y_audit/configs/.pylintrc --version
   ```

3. **Permission errors**

   ```bash
   # Ensure write permissions for reports directory
   chmod 755 a11y_audit/reports/
   ```

### Getting Help

1. **List available tools**: `python a11y_audit/run_audit.py --list-tools`
2. **Check configuration**: Review files in `configs/` directory
3. **View detailed reports**: Check `reports/` directory
4. **Debug mode**: Run with `--format json` for detailed output

## Extending the System

### Adding Custom Checks

1. **Create checker class** in `linters.py`
2. **Implement check methods** following existing patterns
3. **Add to audit pipeline** in `run_audit.py`
4. **Update configuration** in `config.py`

### Adding New Tools

1. **Add tool configuration** to `config.py`
2. **Implement runner method** in `linters.py`
3. **Add command line options** in `run_audit.py`
4. **Update documentation** and examples

### Custom Report Formats

1. **Implement formatter** in new module
2. **Add format option** to command line
3. **Update report generation** logic
4. **Add format-specific configuration**

## Best Practices

### For Developers

1. **Run audits frequently** during development
2. **Fix errors immediately** - don't let them accumulate
3. **Review warnings regularly** - they indicate potential issues
4. **Use pre-commit hooks** for automated checking
5. **Understand the rules** - learn accessibility best practices

### For Teams

1. **Integrate into CI/CD** pipeline
2. **Set quality gates** - fail builds on errors
3. **Regular audit reviews** - weekly or sprint-based
4. **Training and education** - ensure team understands accessibility
5. **Continuous improvement** - update rules and thresholds

### For Projects

1. **Establish baselines** - track improvement over time
2. **Set realistic goals** - gradual improvement is better than perfection
3. **Document exceptions** - when rules don't apply
4. **Regular tool updates** - keep linters and checkers current
5. **Community feedback** - involve accessibility experts

## Future Enhancements

### Planned Features

- **HTML Report Format** - Rich, interactive reports
- **Trend Analysis** - Track issues over time
- **Custom Rule Engine** - User-defined accessibility rules
- **Integration APIs** - Webhook and REST API support
- **Performance Metrics** - Audit performance tracking

### Tool Integrations

- **SonarQube** - Enterprise code quality platform
- **CodeClimate** - Automated code review
- **Snyk** - Security and quality scanning
- **Accessibility Insights** - Microsoft accessibility tools

## Contributing

This audit system is designed for local development and can be extended:

1. **Add new checkers** to `linters.py`
2. **Improve configurations** in `configs/` directory
3. **Enhance reporting** in report generation
4. **Add tool integrations** for new linters
5. **Update documentation** with new features

## Notes

- **Local Development Focus** - Designed for local use, CI integration optional
- **Extensible Architecture** - Easy to add new tools and checks
- **Accessibility First** - All tools and reports follow accessibility principles
- **Performance Conscious** - Optimized for fast feedback cycles
- **Standards Compliant** - Follows WCAG 2.1 and industry best practices
