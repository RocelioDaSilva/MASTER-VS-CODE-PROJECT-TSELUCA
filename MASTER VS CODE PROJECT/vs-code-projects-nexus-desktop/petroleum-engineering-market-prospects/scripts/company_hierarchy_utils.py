#!/usr/bin/env python3
"""
company_hierarchy_utils.py
==========================

Shared utilities for company hierarchy processing scripts.
Consolidates common functions used by add_backlinks.py, rename_files_with_company_names.py,
and deduplicate_hierarchy.py.

Includes:
  - File path parsing (extract company name, NIF, service, niche, tipo from paths)
  - CSV operations (load status map)
  - Directory walking with proper encoding handling
  - Windows extended-path support
  - Filename sanitization
"""

import csv
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote

# ──────────────────────────────────────────────────────────────────────────────
# Regular expressions for parsing
# ──────────────────────────────────────────────────────────────────────────────

# Match filename: Company Name_NIF.md (or similar variants)
FNAME_RE = re.compile(r"^(.+?)_([^_]+)\.md$", re.UNICODE)

# Match filename for extraction: anything_NIF.md
NIF_RE = re.compile(r"_([^_]+)\.md$", re.IGNORECASE)

# Match title in markdown: # Company Name
TITLE_RE = re.compile(r"^# (.+)$", re.MULTILINE)

# Match NIF in markdown: - **NIF:** 5000000000
NIF_CONTENT_RE = re.compile(r"- \*\*NIF:\*\* (.+)$", re.MULTILINE)

# ──────────────────────────────────────────────────────────────────────────────
# Path utilities
# ──────────────────────────────────────────────────────────────────────────────

def get_windows_extended_path(path_str):
    """Return Windows extended-length path prefix if needed, else regular path."""
    if sys.platform == "win32" and len(os.path.abspath(path_str)) > 260:
        return "\\\\?\\" + os.path.abspath(path_str)
    return path_str

def normalize_path(path_str):
    """Normalize path by removing extended-length prefix."""
    return path_str.replace("\\\\?\\", "").replace("/", os.sep)

def parse_filepath(fpath, hier_root):
    """
    Extract (nome, nif, servico, nicho, tipo) from absolute file path.
    
    Example:
      …/company_hierarchy/1. Consultoria/Admin/SCA/Empresa X_5000222879.md
      → ('Empresa X', '5000222879', '1. Consultoria', 'Admin', 'SCA')
    
    Returns:
      tuple (nome, nif, servico, nicho, tipo) or None if parse fails
    """
    norm = normalize_path(fpath)
    root = normalize_path(hier_root)
    
    try:
        rel = os.path.relpath(norm, root)
    except ValueError:
        return None
    
    parts = rel.split(os.sep)
    if len(parts) < 4:
        return None
    
    servico = parts[0]
    nicho = parts[1]
    tipo = parts[2]
    filename = parts[-1]
    
    m = FNAME_RE.match(filename)
    if not m:
        return None
    
    nome = m.group(1)
    nif = m.group(2)
    return nome, nif, servico, nicho, tipo

# ──────────────────────────────────────────────────────────────────────────────
# File operations
# ──────────────────────────────────────────────────────────────────────────────

def read_file_safe(path_str, encodings=None):
    """
    Safely read file with fallback encodings.
    
    Args:
      path_str: file path
      encodings: list of encodings to try (default: utf-8, latin-1, cp1252)
    
    Returns:
      tuple (content, encoding_used) or (None, None) if all fail
    """
    if encodings is None:
        encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for enc in encodings:
        try:
            with open(path_str, 'r', encoding=enc) as f:
                content = f.read()
            return content, enc
        except Exception:
            continue
    
    return None, None

def write_file_safe(path_str, content, encoding='utf-8'):
    """
    Safely write file with proper encoding and error handling.
    
    Args:
      path_str: file path
      content: content to write
      encoding: encoding to use (default: utf-8)
    
    Returns:
      bool: True if successful, False otherwise
    """
    try:
        # Ensure parent directory exists
        Path(path_str).parent.mkdir(parents=True, exist_ok=True)
        with open(path_str, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing {path_str}: {e}")
        return False

# ──────────────────────────────────────────────────────────────────────────────
# CSV operations
# ──────────────────────────────────────────────────────────────────────────────

def load_status_map(csv_path):
    """
    Load NIF → Status mapping from CSV.
    
    Args:
      csv_path: path to company_hierarchy.csv
    
    Returns:
      dict: {NIF (str) → Status (str)}
    """
    status_map = {}
    try:
        with open(csv_path, encoding='utf-8', newline='') as f:
            for row in csv.DictReader(f):
                nif = str(row.get("NIF", "")).strip()
                status = row.get("Status", "").strip()
                if nif and status and nif not in status_map:
                    status_map[nif] = status
    except Exception as e:
        print(f"Warning: Could not load CSV ({e})")
    
    return status_map

# ──────────────────────────────────────────────────────────────────────────────
# Directory operations
# ──────────────────────────────────────────────────────────────────────────────

def build_dir_index(root):
    """
    Index all markdown files in directory tree.
    
    Returns:
      dict: {dirpath → list of entries}
        where each entry is {fname, name, nif, fpath}
    """
    index = {}
    root_win = get_windows_extended_path(root)
    
    for dirpath, _dirs, files in os.walk(root_win):
        md_files = [f for f in files if f.lower().endswith('.md')]
        if not md_files:
            continue
        
        entries = []
        for fname in md_files:
            m = FNAME_RE.match(fname)
            if m:
                name = m.group(1)
                nif = m.group(2)
            else:
                name = fname[:-3]
                nif = ''
            
            entries.append({
                'fname': fname,
                'name': name,
                'nif': nif,
                'fpath': os.path.join(dirpath, fname)
            })
        
        entries.sort(key=lambda x: x['name'].lower())
        index[dirpath] = entries
    
    return index

def walk_md_files(root):
    """
    Generator: yield all markdown files in tree.
    
    Yields:
      tuple (dirpath, filename, full_path)
    """
    root_win = get_windows_extended_path(root)
    for dirpath, _dirs, files in os.walk(root_win):
        for fname in files:
            if fname.lower().endswith('.md'):
                fpath = os.path.join(dirpath, fname)
                yield dirpath, fname, fpath

# ──────────────────────────────────────────────────────────────────────────────
# Text utilities
# ──────────────────────────────────────────────────────────────────────────────

def sanitize_filename(name, max_length=200):
    """
    Sanitize string for safe use as filename.
    
    Removes/replaces invalid characters and limits length.
    """
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*\r\n\t]', '', name)
    name = re.sub(r'\s+', ' ', name)
    if len(name) > max_length:
        name = name[:max_length].rstrip()
    return name

def make_rel_link(from_path, to_path):
    """
    Create relative markdown link path with proper URL quoting.
    
    Args:
      from_path: absolute path of source file
      to_path: absolute path of target file
    
    Returns:
      str: relative path with URL-quoted segments (e.g., "foo%20bar/file.md")
    """
    rel = os.path.relpath(to_path, os.path.dirname(from_path)).replace('\\', '/')
    parts = rel.split('/')
    parts_q = [quote(p, safe='') for p in parts]
    return '/'.join(parts_q)

# ──────────────────────────────────────────────────────────────────────────────
# Logging utilities
# ──────────────────────────────────────────────────────────────────────────────

class ProgressTracker:
    """Simple progress tracker for processing files."""
    
    def __init__(self, checkpoint_interval=5000):
        self.total = 0
        self.updated = 0
        self.skipped = 0
        self.errors = 0
        self.checkpoint_interval = checkpoint_interval
    
    def increment(self, count=1, updated=0, skipped=0, errors=0):
        """Increment counters and optionally print progress."""
        self.total += count
        self.updated += updated
        self.skipped += skipped
        self.errors += errors
        
        if self.total % self.checkpoint_interval == 0:
            self.print_progress()
    
    def print_progress(self):
        """Print current progress."""
        print(f"  ... {self.total:,} total | {self.updated:,} updated | {self.skipped:,} skipped")
    
    def print_summary(self):
        """Print final summary."""
        print(f"\nProcessing complete.")
        print(f"  Total            : {self.total:,}")
        print(f"  Updated          : {self.updated:,}")
        print(f"  Skipped          : {self.skipped:,}")
        if self.errors:
            print(f"  Errors           : {self.errors:,}")

# ──────────────────────────────────────────────────────────────────────────────
# Auto-detect hierarchy root
# ──────────────────────────────────────────────────────────────────────────────

def get_hierarchy_root(script_location=None):
    """
    Auto-detect company_hierarchy root directory.
    
    Searches:
      1. data/processed/company_hierarchy relative to script
      2. data/processed/company_hierarchy relative to repo root
      3. ./company_hierarchy in current directory
    """
    if script_location is None:
        script_location = Path(__file__).resolve().parent
    else:
        script_location = Path(script_location).resolve()
    
    search_paths = [
        script_location / 'data' / 'processed' / 'company_hierarchy',  # if in root
        script_location.parent / 'data' / 'processed' / 'company_hierarchy',  # if in scripts/
        script_location.parent.parent / 'data' / 'processed' / 'company_hierarchy',  # if in data/processed/
        Path.cwd() / 'company_hierarchy',  # current dir
    ]
    
    for path in search_paths:
        if path.exists():
            return str(path)
    
    return None
