#!/usr/bin/env python3
"""
Rename all company markdown files to include company name before NIF.
Changes: NIF.md -> Company Name_NIF.md
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def sanitize_filename(name, max_length=200):
    """Sanitize filename to remove/replace invalid characters and limit length."""
    # Remove leading/trailing whitespace
    name = name.strip()
    # Replace invalid filename characters more aggressively
    name = re.sub(r'[<>:"/\\|?*\r\n\t]', '', name)
    # Replace multiple spaces with single space
    name = re.sub(r'\s+', ' ', name)
    # Truncate to max length for filename safety
    if len(name) > max_length:
        name = name[:max_length].rstrip()
    return name

def rename_company_files(root_dir):
    """Rename all company markdown files to include company name."""
    root_path = Path(root_dir)
    renamed_count = 0
    error_count = 0
    skipped_count = 0
    # Track duplicate names per directory
    name_counts = defaultdict(lambda: defaultdict(int))
    
    # First pass: collect all files and detect duplicates
    files_to_process = []
    for md_file in sorted(root_path.rglob('*.md')):
        files_to_process.append(md_file)
    
    print(f"Processing {len(files_to_process)} files...")
    
    # Process files
    for idx, md_file in enumerate(files_to_process):
        if (idx + 1) % 10000 == 0:
            print(f"Progress: {idx + 1}/{len(files_to_process)} files...")
        
        try:
            # Read the file to get company name
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract company name from the title (first line after #)
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if not title_match:
                error_count += 1
                continue
            
            company_name = title_match.group(1).strip()
            
            # Extract NIF from the file
            nif_match = re.search(r'- \*\*NIF:\*\* (.+)$', content, re.MULTILINE)
            if not nif_match:
                error_count += 1
                continue
            
            nif = nif_match.group(1).strip()
            # Also sanitize NIF (remove invalid chars like asterisks)
            nif = re.sub(r'[<>:"/\\|?*\r\n\t]', '', nif)
            
            # Sanitize the company name for use in filename
            safe_name = sanitize_filename(company_name)
            
            # Track duplicates in this directory
            parent_dir = str(md_file.parent)
            name_counts[parent_dir][safe_name] += 1
            
            # Create new filename with counter if duplicate
            if name_counts[parent_dir][safe_name] > 1:
                counter = name_counts[parent_dir][safe_name]
                new_filename = f"{safe_name}_{nif}_{counter}.md"
            else:
                new_filename = f"{safe_name}_{nif}.md"
            
            new_file_path = md_file.parent / new_filename
            
            # Skip if already renamed
            if md_file.name == new_filename:
                skipped_count += 1
                continue
            
            # Check if target already exists to avoid conflicts
            if new_file_path.exists():
                # Find alternative name
                counter = 1
                while True:
                    alt_filename = f"{safe_name}_{nif}_{counter}.md"
                    alt_file_path = md_file.parent / alt_filename
                    if not alt_file_path.exists():
                        new_filename = alt_filename
                        new_file_path = alt_file_path
                        break
                    counter += 1
            
            # Perform the rename
            try:
                md_file.rename(new_file_path)
                renamed_count += 1
            except Exception as rename_error:
                print(f"✗ Rename failed for {md_file.name}: {rename_error}")
                error_count += 1
        
        except Exception as e:
            error_count += 1
    
    print(f"\n✓ Complete!")
    print(f"  Renamed: {renamed_count} files")
    print(f"  Skipped (already renamed): {skipped_count} files")
    print(f"  Errors: {error_count} files")

if __name__ == '__main__':
    import argparse
    _dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "data", "processed"))
    parser = argparse.ArgumentParser(description="Rename company files to CompanyName_NIF.md")
    parser.add_argument("--root", default=os.path.join(_dir, "company_hierarchy"),
                        help="Root directory of company hierarchy (default: data/processed/company_hierarchy/)")
    args = parser.parse_args()
    
    print(f"Starting file renaming in: {args.root}\n")
    rename_company_files(args.root)
