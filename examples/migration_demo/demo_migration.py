#!/usr/bin/env python3
"""
Demonstration of the tkaria11y migration tool.
This script shows what the migrate command does by creating before/after examples.
"""

import sys
from pathlib import Path

from tkaria11y.scripts.migrate import TkinterToA11yTransformer

# Add the parent directory to the path so we can import tkaria11y
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def demonstrate_migration():
    """Demonstrate the migration process with examples"""

    print("🔄 tkaria11y Migration Tool Demonstration")
    print("=" * 50)

    # Get the current directory
    current_demo_dir = Path(__file__).parent

    # Files to migrate
    files_to_migrate = [
        current_demo_dir / "before_migration.py",
        current_demo_dir / "simple_form.py",
    ]

    # Create transformer
    transformer = TkinterToA11yTransformer(interactive=False)

    for file_path in files_to_migrate:
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            continue

        print(f"\n📁 Processing: {file_path.name}")
        print("-" * 30)

        # Read original content
        original_content = file_path.read_text(encoding="utf-8")

        # Transform content
        transformed_content = transformer.transform_file(original_content)

        # Create output file
        output_file = file_path.parent / f"after_{file_path.name}"
        output_file.write_text(transformed_content, encoding="utf-8")

        # Show changes
        if original_content != transformed_content:
            print("✅ Changes made:")

            original_lines = original_content.split("\n")
            transformed_lines = transformed_content.split("\n")

            changes_count = 0
            for i, (old_line, new_line) in enumerate(
                zip(original_lines, transformed_lines)
            ):
                if old_line != new_line:
                    changes_count += 1
                    if changes_count <= 5:  # Show first 5 changes
                        print(f"  Line {i+1}:")
                        print(f"    - {old_line.strip()}")
                        print(f"    + {new_line.strip()}")

            if changes_count > 5:
                print(f"    ... and {changes_count - 5} more changes")

            print(f"📊 Total changes: {changes_count} lines modified")
            print(f"💾 Output saved to: {output_file.name}")
        else:
            print("ℹ️  No changes needed - file already uses accessible widgets")

    print("\n🎉 Migration demonstration complete!")
    print("📂 Check the 'after_*.py' files to see the results")

    # Show summary of what the migration does
    print("\n📋 What the migration tool does:")
    print("   • Converts tk.Button → AccessibleButton")
    print("   • Converts tk.Entry → AccessibleEntry")
    print("   • Converts tk.Label → AccessibleLabel")
    print("   • Converts tk.Frame → AccessibleFrame")
    print("   • Adds accessible_name parameters based on text= values")
    print("   • Adds necessary imports from tkaria11y.widgets")
    print("   • Preserves all existing functionality")


def show_file_comparison(file1_path: Path, file2_path: Path):
    """Show a side-by-side comparison of two files"""
    if not file1_path.exists() or not file2_path.exists():
        print("❌ Cannot compare - one or both files don't exist")
        return

    print(f"\n📊 Comparison: {file1_path.name} vs {file2_path.name}")
    print("=" * 60)

    content1 = file1_path.read_text().split("\n")
    content2 = file2_path.read_text().split("\n")

    max_lines = max(len(content1), len(content2))

    for i in range(min(20, max_lines)):  # Show first 20 lines
        line1 = content1[i] if i < len(content1) else ""
        line2 = content2[i] if i < len(content2) else ""

        if line1 != line2:
            print(f"Line {i+1}:")
            print(f"  BEFORE: {line1}")
            print(f"  AFTER:  {line2}")
            print()


if __name__ == "__main__":
    demonstrate_migration()

    # Optionally show detailed comparison
    demo_dir = Path(__file__).parent
    if input("\n🔍 Show detailed file comparison? (y/n): ").lower() == "y":
        show_file_comparison(
            demo_dir / "before_migration.py", demo_dir / "after_before_migration.py"
        )
