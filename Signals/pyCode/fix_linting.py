#!/usr/bin/env python3
"""
Quick script to fix common linting issues across DataDownloads files.
"""

import os
import re
from pathlib import Path


def fix_common_linting_issues(file_path):
    """Fix common linting issues in a Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix trailing whitespace
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]
    
    # Ensure file ends with newline
    if lines and lines[-1] != '':
        lines.append('')
    
    content = '\n'.join(lines)
    
    # Fix f-strings without placeholders
    content = re.sub(r'f"([^"]*)"(?![^{]*})', r'"\1"', content)
    content = re.sub(r"f'([^']*)'(?![^{]*})", r"'\1'", content)
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {file_path}")
        return True
    return False


def main():
    """Fix linting issues in all Python files in DataDownloads/."""
    downloads_dir = Path("DataDownloads")
    
    if not downloads_dir.exists():
        print("DataDownloads directory not found")
        return
    
    fixed_count = 0
    for py_file in downloads_dir.glob("*.py"):
        if fix_common_linting_issues(py_file):
            fixed_count += 1
    
    print(f"Fixed {fixed_count} files")


if __name__ == "__main__":
    main()