#!/usr/bin/env python3
"""Pre-Deployment Auditor for Hugo blog posts"""
import yaml
import re
import os
import sys
from pathlib import Path

BLOG_DIR = Path("/home/kweeb/.hermes/workspace/exampleSite/content/english/blog")
ERRORS = []
FIXED = []

def add_error(file, msg):
    ERRORS.append(f"{file}: {msg}")

def add_fixed(file, msg):
    FIXED.append(f"{file}: {msg}")

def check_front_matter(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check delimiters
    if not content.startswith('---\n'):
        add_error(file_path.name, "Missing opening --- delimiter")
        return False
    
    # Find closing ---
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        add_error(file_path.name, "Missing closing --- delimiter")
        return False
    
    front_matter = parts[1]
    
    # Parse YAML
    try:
        data = yaml.safe_load(front_matter)
        if not data:
            add_error(file_path.name, "Empty front matter")
            return False
    except yaml.YAMLError as e:
        add_error(file_path.name, f"YAML parse error: {e}")
        return False
    
    # Check required fields
    if 'title' not in data:
        add_error(file_path.name, "Missing title field")
    elif not isinstance(data['title'], str) or not data['title'].strip():
        add_error(file_path.name, "Title is empty or not a string")
    
    # Check date (accept date, datepublished, publishDate)
    date_fields = ['date', 'datepublished', 'publishDate', 'pubDate']
    if not any(f in data for f in date_fields):
        add_error(file_path.name, f"Missing date field (need {date_fields})")
        # Debug: print keys
        print(f"  DEBUG {file_path.name}: Parsed keys = {list(data.keys())}")
    
    # Check draft
    if 'draft' in data:
        if data['draft'] is True:
            add_error(file_path.name, "draft: true (must be false or absent)")
    
    return True

def check_markdown_syntax(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check broken links: [text](url) with empty url
    broken_links = re.findall(r'\[([^\]]*)\]\((\s*)\)', content)
    for text, url in broken_links:
        add_error(file_path.name, f"Empty link URL for: {text[:20]}...")
    
    # Check unclosed shortcodes: {{< ... >}} or {{% ... %}}
    shortcodes = re.findall(r'{{[<%](.*?)[>%]}', content, re.DOTALL)
    for sc in shortcodes:
        if not sc.strip():
            add_error(file_path.name, f"Empty shortcode: {sc[:20]}...")
    
    # Check extra quotes at end of lines (common issue)
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if line.strip().endswith('""'):
            add_error(file_path.name, f"Line {i}: Extra quote at end of line")
            # Auto-fix
            fixed_line = line.rstrip('"')  # Remove extra quote
            lines[i-1] = fixed_line
            with open(file_path, 'w') as f:
                f.write('\n'.join(lines))
            add_fixed(file_path.name, f"Fixed extra quote on line {i}")

def check_build_readiness(file_path):
    # Check file is in correct subdirectory
    if str(BLOG_DIR) not in str(file_path):
        add_error(file_path.name, f"Not in correct blog directory: {BLOG_DIR}")
        return False
    return True

def main():
    print("🔍 Running Pre-Deployment Audit...")
    
    md_files = [f for f in BLOG_DIR.glob("*.md") if f.name != "_index.md"]  # Exclude _index.md
    if not md_files:
        print("No markdown files found!")
        sys.exit(1)
    
    for md_file in md_files:
        print(f"\nChecking: {md_file.name}")
        check_build_readiness(md_file)
        check_front_matter(md_file)
        check_markdown_syntax(md_file)
    
    # Report results
    if FIXED:
        print("\n✅ Auto-fixed issues:")
        for fix in FIXED:
            print(f"  - {fix}")
    
    if ERRORS:
        print(f"\n❌ Errors found (not fixed): {len(ERRORS)}")
        for err in ERRORS[:10]:  # Show first 10
            print(f"  - {err}")
        if len(ERRORS) > 10:
            print(f"  ... and {len(ERRORS)-10} more")
        print("\n🛑 Fix errors before pushing!")
        sys.exit(1)
    else:
        print("\n✅ All checks passed! Safe to push.")
        sys.exit(0)

if __name__ == "__main__":
    main()
