#!/usr/bin/env python3
# a11y_audit/ci_integration.py

"""
CI/CD Integration for Accessibility Audits

This module provides tools to integrate accessibility audits into
continuous integration and deployment pipelines.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List

from .config import PROJECT_ROOT, CI_CONFIG


class GitHubActionsIntegration:
    """GitHub Actions workflow integration."""

    def generate_workflow(self) -> Dict[str, Any]:
        """Generate GitHub Actions workflow for accessibility audits."""
        workflow = {
            "name": "Accessibility Audit",
            "on": {
                "push": {"branches": ["main", "develop"]},
                "pull_request": {"branches": ["main", "develop"]},
                "schedule": [{"cron": "0 2 * * 1"}],  # Weekly on Monday at 2 AM
            },
            "jobs": {
                "accessibility-audit": {
                    "runs-on": "ubuntu-latest",
                    "strategy": {
                        "matrix": {
                            "python-version": CI_CONFIG["github_actions"][
                                "python_versions"
                            ]
                        }
                    },
                    "steps": [
                        {"name": "Checkout code", "uses": "actions/checkout@v4"},
                        {
                            "name": "Set up Python ${{ matrix.python-version }}",
                            "uses": "actions/setup-python@v4",
                            "with": {"python-version": "${{ matrix.python-version }}"},
                        },
                        {
                            "name": "Install dependencies",
                            "run": """
                                python -m pip install --upgrade pip
                                pip install flake8 pylint mypy
                                pip install flake8-docstrings flake8-import-order \\
                                    flake8-naming
                                pip install -e .
                            """,
                        },
                        {
                            "name": "Run accessibility audit",
                            "run": (
                                "python a11y_audit/run_audit.py "
                                "--fail-on-error --format json"
                            ),
                        },
                        {
                            "name": "Upload audit results",
                            "uses": "actions/upload-artifact@v3",
                            "if": "always()",
                            "with": {
                                "name": "accessibility-audit-results-${{ matrix.python-version }}",
                                "path": "a11y_audit/reports/",
                            },
                        },
                        {
                            "name": "Comment PR with results",
                            "uses": "actions/github-script@v6",
                            "if": "github.event_name == 'pull_request' && always()",
                            "with": {
                                "script": """
                                    const fs = require('fs');
                                    const path = require('path');
                                    
                                    // Find the latest audit report
                                    const reportsDir = 'a11y_audit/reports';
                                    if (fs.existsSync(reportsDir)) {
                                        const files = fs.readdirSync(reportsDir)
                                            .filter(f => f.includes('accessibility_audit') && f.endsWith('.json'))
                                            .sort()
                                            .reverse();
                                        
                                        if (files.length > 0) {
                                            const reportPath = path.join(reportsDir, files[0]);
                                            const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
                                            
                                            let comment = '## 🔍 Accessibility Audit Results\\n\\n';
                                            
                                            // Add summary
                                            let totalIssues = 0;
                                            let errorCount = 0;
                                            let warningCount = 0;
                                            
                                            for (const [tool, result] of Object.entries(report.results)) {
                                                if (result.issues) {
                                                    totalIssues += result.issues.length;
                                                    result.issues.forEach(issue => {
                                                        if (issue.severity === 'error') errorCount++;
                                                        else if (issue.severity === 'warning') warningCount++;
                                                    });
                                                }
                                            }
                                            
                                            if (totalIssues === 0) {
                                                comment += '✅ **No accessibility issues found!**\\n\\n';
                                            } else {
                                                comment += `⚠️ **Found ${totalIssues} accessibility issues:**\\n`;
                                                comment += `- 🚨 Errors: ${errorCount}\\n`;
                                                comment += `- ⚠️ Warnings: ${warningCount}\\n\\n`;
                                            }
                                            
                                            // Add tool results
                                            comment += '### Tool Results\\n\\n';
                                            for (const [tool, result] of Object.entries(report.results)) {
                                                const status = result.status === 'COMPLETED' ? '✅' : 
                                                             result.status === 'SKIPPED' ? '⏭️' : '❌';
                                                comment += `${status} **${tool}**: ${result.message}\\n`;
                                            }
                                            
                                            // Post comment
                                            github.rest.issues.createComment({
                                                issue_number: context.issue.number,
                                                owner: context.repo.owner,
                                                repo: context.repo.repo,
                                                body: comment
                                            });
                                        }
                                    }
                                """
                            },
                        },
                    ],
                }
            },
        }

        return workflow

    def create_workflow_file(self) -> Path:
        """Create GitHub Actions workflow file."""
        workflow_dir = PROJECT_ROOT / ".github" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)

        workflow_file = workflow_dir / "accessibility-audit.yml"
        workflow = self.generate_workflow()

        with open(workflow_file, "w") as f:
            yaml.dump(workflow, f, default_flow_style=False, sort_keys=False)

        return workflow_file


class PreCommitIntegration:
    """Pre-commit hooks integration."""

    def generate_config(self) -> Dict[str, Any]:
        """Generate pre-commit configuration."""
        config = {
            "repos": [
                {
                    "repo": "https://github.com/pre-commit/pre-commit-hooks",
                    "rev": "v4.4.0",
                    "hooks": [
                        {"id": "trailing-whitespace"},
                        {"id": "end-of-file-fixer"},
                        {"id": "check-yaml"},
                        {"id": "check-json"},
                        {"id": "check-merge-conflict"},
                        {"id": "check-added-large-files"},
                    ],
                },
                {
                    "repo": "https://github.com/psf/black",
                    "rev": "23.3.0",
                    "hooks": [{"id": "black", "language_version": "python3"}],
                },
                {
                    "repo": "https://github.com/pycqa/isort",
                    "rev": "5.12.0",
                    "hooks": [{"id": "isort", "args": ["--profile", "black"]}],
                },
                {
                    "repo": "https://github.com/pycqa/flake8",
                    "rev": "6.0.0",
                    "hooks": [
                        {
                            "id": "flake8",
                            "additional_dependencies": [
                                "flake8-docstrings",
                                "flake8-import-order",
                                "flake8-naming",
                            ],
                            "args": ["--config=a11y_audit/configs/.flake8"],
                        }
                    ],
                },
                {
                    "repo": "https://github.com/pre-commit/mirrors-mypy",
                    "rev": "v1.3.0",
                    "hooks": [
                        {
                            "id": "mypy",
                            "args": ["--config-file=a11y_audit/configs/mypy.ini"],
                            "additional_dependencies": ["types-all"],
                        }
                    ],
                },
                {
                    "repo": "local",
                    "hooks": [
                        {
                            "id": "accessibility-audit",
                            "name": "Accessibility Audit",
                            "entry": "python a11y_audit/run_audit.py --type custom --fail-on-error",
                            "language": "system",
                            "files": r"\.py$",
                            "pass_filenames": False,
                        }
                    ],
                },
            ]
        }

        return config

    def create_config_file(self) -> Path:
        """Create pre-commit configuration file."""
        config_file = PROJECT_ROOT / ".pre-commit-config.yaml"
        config = self.generate_config()

        with open(config_file, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        return config_file


class VSCodeIntegration:
    """VS Code integration for accessibility audits."""

    def generate_settings(self) -> Dict[str, Any]:
        """Generate VS Code settings for accessibility development."""
        settings = {
            "python.linting.enabled": True,
            "python.linting.flake8Enabled": True,
            "python.linting.flake8Args": ["--config=a11y_audit/configs/.flake8"],
            "python.linting.pylintEnabled": True,
            "python.linting.pylintArgs": ["--rcfile=a11y_audit/configs/.pylintrc"],
            "python.linting.mypyEnabled": True,
            "python.linting.mypyArgs": ["--config-file=a11y_audit/configs/mypy.ini"],
            "python.formatting.provider": "black",
            "python.formatting.blackArgs": ["--line-length=88"],
            "python.sortImports.args": ["--profile=black"],
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {"source.organizeImports": True},
            "files.associations": {"*.py": "python"},
            "python.analysis.typeCheckingMode": "basic",
            "python.analysis.autoImportCompletions": True,
            "accessibility.signals.sounds.volume": 0.5,
            "accessibility.signals.sounds.enabled": True,
            "workbench.colorCustomizations": {
                "editorError.foreground": "#ff0000",
                "editorWarning.foreground": "#ff8800",
                "editorInfo.foreground": "#0088ff",
            },
        }

        return settings

    def generate_tasks(self) -> Dict[str, Any]:
        """Generate VS Code tasks for accessibility audits."""
        tasks = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Run Accessibility Audit",
                    "type": "shell",
                    "command": "python",
                    "args": ["a11y_audit/run_audit.py"],
                    "group": {"kind": "test", "isDefault": True},
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                    },
                    "problemMatcher": [],
                },
                {
                    "label": "Run Quick Accessibility Check",
                    "type": "shell",
                    "command": "python",
                    "args": [
                        "a11y_audit/run_audit.py",
                        "--type",
                        "custom",
                        "--no-reports",
                    ],
                    "group": "test",
                    "presentation": {
                        "echo": True,
                        "reveal": "silent",
                        "focus": False,
                        "panel": "shared",
                    },
                },
                {
                    "label": "Run Flake8 Accessibility Lint",
                    "type": "shell",
                    "command": "flake8",
                    "args": ["--config=a11y_audit/configs/.flake8", "tkaria11y/"],
                    "group": "test",
                    "presentation": {
                        "echo": True,
                        "reveal": "silent",
                        "focus": False,
                        "panel": "shared",
                    },
                },
            ],
        }

        return tasks

    def create_vscode_config(self) -> List[Path]:
        """Create VS Code configuration files."""
        vscode_dir = PROJECT_ROOT / ".vscode"
        vscode_dir.mkdir(exist_ok=True)

        created_files = []

        # Settings
        settings_file = vscode_dir / "settings.json"
        with open(settings_file, "w") as f:
            import json

            json.dump(self.generate_settings(), f, indent=2)
        created_files.append(settings_file)

        # Tasks
        tasks_file = vscode_dir / "tasks.json"
        with open(tasks_file, "w") as f:
            import json

            json.dump(self.generate_tasks(), f, indent=2)
        created_files.append(tasks_file)

        return created_files


def setup_ci_integration():
    """Set up CI/CD integration files."""
    print("Setting up CI/CD integration for accessibility audits...")

    created_files = []

    # GitHub Actions
    gh_actions = GitHubActionsIntegration()
    workflow_file = gh_actions.create_workflow_file()
    created_files.append(workflow_file)
    print(f"Created GitHub Actions workflow: {workflow_file}")

    # Pre-commit hooks
    pre_commit = PreCommitIntegration()
    config_file = pre_commit.create_config_file()
    created_files.append(config_file)
    print(f"Created pre-commit config: {config_file}")

    # VS Code integration
    vscode = VSCodeIntegration()
    vscode_files = vscode.create_vscode_config()
    created_files.extend(vscode_files)
    print(f"Created VS Code config files: {[str(f) for f in vscode_files]}")

    print("\nCI/CD Integration Setup Complete!")
    print("\nNext steps:")
    print("1. Install pre-commit: pip install pre-commit")
    print("2. Install hooks: pre-commit install")
    print("3. Test hooks: pre-commit run --all-files")
    print("4. Commit and push to trigger GitHub Actions")

    return created_files


if __name__ == "__main__":
    setup_ci_integration()
