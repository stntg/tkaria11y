`markdown

Contributing to tk-a11y

Thank you for your interest in contributing to tk-a11y! We welcome all kinds of contributions—from bug reports and documentation fixes to new features and plugins. This guide walks you through the process and explains our expectations for code style, testing, and collaboration.

---

Table of Contents

- Filing Issues  
- Getting the Code  
- Setting Up Your Environment  
- Branching Strategy  
- Coding Guidelines  
  - Code Style  
  - Type Checking  
  - Testing  
  - Stub Generation  
  - Documentation Updates  
- Submitting a Pull Request  
- Code of Conduct  
- Release Process  
- Additional Resources

---

Filing Issues

1. Search existing issues to avoid duplicates.  
2. Open a new issue with a clear title and description.  
3. Include steps to reproduce, expected vs. actual behavior, and environment details (OS, Python version).  
4. Tag the issue with appropriate labels (e.g., bug, feature-request, question).

---

Getting the Code

`bash
git clone git@github.com:stntg/tk-a11y.git
cd tk-a11y
`

---

Setting Up Your Environment

1. Create a virtual environment:
   `bash
   python3 -m venv .venv
   source .venv/bin/activate
   `
2. Install the package and dev dependencies:
   `bash
   pip install --upgrade pip
   pip install ".[dev]"
   `
3. Generate initial type stubs:
   `bash
   python scripts/generate_stubs.py
   `

---

Branching Strategy

- Always branch off main for new work.  
- Name branches descriptively:  
  - feature/<short-description>  
  - bugfix/<short-description>  
  - docs/<short-description>  
- Keep branches focused on a single change or feature.

---

Coding Guidelines

Code Style

- Follow PEP 8 for Python code.  
- Use black for formatting:
  `bash
  black .
  `
- Lint with flake8 and fix any errors:
  `bash
  flake8 tka11y tests
  `

Type Checking

- Keep type hints up to date in code and stubs.  
- Run mypy in strict mode:
  `bash
  mypy tka11y
  `

Testing

- Write tests for all new functionality under the tests/ folder.  
- Use pytest for test discovery:
  `bash
  pytest --maxfail=1 --disable-warnings -q
  `
- Aim for high coverage, especially on accessibility behaviors and edge cases.

Stub Generation

- Whenever WIDGETMAP changes, regenerate stubs:
  `bash
  python scripts/generate_stubs.py
  `
- Ensure tka11y/stubs/widgets.pyi matches the mapped widgets.

Documentation Updates

- Update README.md, docs/, and inline docstrings for new features.  
- Follow the style of existing documentation in docs/index.md.  
- When adding public APIs, include examples and usage snippets.

---

Submitting a Pull Request

1. Push your branch to GitHub:
   `bash
   git push origin feature/your-feature
   `
2. Open a Pull Request against main.  
3. In your PR description:
   - Reference related issues (e.g., Closes #123).  
   - Summarize your changes and rationale.  
   - List any breaking changes or migration steps.  
4. Ensure CI passes all checks (lint, type, tests, stub generation).  
5. Address review feedback; keep discussions focused and respectful.

---

Code of Conduct

This project follows the Contributor Covenant Code of Conduct. By participating, you agree to abide by its terms.

---

Release Process

1. Bump version in tka11y/init.py and pyproject.toml.  
2. Tag the commit:  
   `bash
   git tag vX.Y.Z
   git push --tags
   `
3. CI will automatically publish to PyPI when a v tag is pushed.  
4. Update CHANGELOG.md with notable changes for the release.

---

Additional Resources

- Project roadmap: ROADMAP.md  
- Issue tracker on GitHub  
- Official ARIA Authoring Practices: https://www.w3.org/TR/wai-aria-practices/  
- WCAG guidelines: https://www.w3.org/WAI/standards-guidelines/wcag/

Thank you for helping make tk-a11y better and more accessible!  
`