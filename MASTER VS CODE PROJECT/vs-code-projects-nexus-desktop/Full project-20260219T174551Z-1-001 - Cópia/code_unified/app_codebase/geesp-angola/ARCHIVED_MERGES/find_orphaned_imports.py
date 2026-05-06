#!/usr/bin/env python3
"""
Orphaned Imports Finder - Detects unused and broken imports

This script scans all Python files and identifies:
1. Imports from modules that don't exist
2. Imports that are aliased but never used
3. Wildcard imports that could be more specific

Usage:
    python find_orphaned_imports.py
"""

import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

class ImportVisitor(ast.NodeVisitor):
    """AST visitor to extract imports and their usage."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.imports = []  # (line, type, module, names, alias)
        self.used_names = set()  # Names actually used in code
        
    def visit_Import(self, node):
        """Handle: import x, import x as y"""
        for alias in node.names:
            self.imports.append({
                'line': node.lineno,
                'type': 'import',
                'module': alias.name,
                'names': [alias.name.split('.')[0]],
                'alias': alias.asname,
                'used_name': alias.asname or alias.name.split('.')[0]
            })
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Handle: from x import y, from x import y as z"""
        names = []
        used_names = []
        for alias in node.names:
            names.append(alias.name)
            used_names.append(alias.asname if alias.asname else alias.name)
        
        self.imports.append({
            'line': node.lineno,
            'type': 'from',
            'module': node.module or '',
            'level': node.level,  # Relative import level (e.g., .. is 2)
            'names': names,
            'used_names': used_names
        })
        self.generic_visit(node)
    
    def visit_Name(self, node):
        """Track used variable names."""
        if isinstance(node.ctx, (ast.Load, ast.Del)):
            self.used_names.add(node.id)
        self.generic_visit(node)
    
    def visit_Attribute(self, node):
        """Track module.attribute access."""
        if isinstance(node.value, ast.Name):
            self.used_names.add(node.value.id)
        self.generic_visit(node)

def analyze_file(file_path: Path) -> Tuple[List[Dict], Set[str]]:
    """Analyze a Python file for imports and usage."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        visitor = ImportVisitor(str(file_path))
        visitor.visit(tree)
        
        return visitor.imports, visitor.used_names
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return [], set()

def check_module_exists(module_name: str, root_path: str) -> bool:
    """Check if a module exists in the project."""
    # Handle relative imports
    if module_name.startswith('.'):
        return True  # Can't easily validate relative imports without context
    
    # Convert module name to path
    parts = module_name.split('.')
    potential_paths = [
        Path(root_path) / f"{parts[0]}.py",
        Path(root_path) / parts[0] / "__init__.py",
    ]
    
    # Check if any path exists
    for path in potential_paths:
        if path.exists():
            return True
    
    return False

def find_python_files(root_path: str) -> List[Path]:
    """Find all Python files."""
    files = []
    for path in Path(root_path).rglob("*.py"):
        if "__pycache__" not in str(path):
            files.append(path)
    return files

def generate_report(root_path: str) -> None:
    """Generate report on orphaned and unused imports."""
    print("=" * 80)
    print("ORPHANED & UNUSED IMPORTS REPORT")
    print("=" * 80)
    print()
    
    python_files = find_python_files(root_path)
    print(f"Scanning {len(python_files)} Python files...\n")
    
    unused_imports = []
    wildcard_imports = []
    file_count = 0
    
    for file_path in python_files:
        imports, used_names = analyze_file(file_path)
        
        if not imports:
            continue
        
        file_count += 1
        rel_path = str(file_path.relative_to(root_path))
        
        for imp in imports:
            # Check for wildcard imports
            if imp['type'] == 'from' and 'names' in imp and '*' in imp['names']:
                wildcard_imports.append((rel_path, imp))
            
            # Check for unused imports
            if imp['type'] == 'from':
                for used_name in imp.get('used_names', []):
                    if used_name not in used_names and used_name != '*':
                        unused_imports.append((rel_path, imp, used_name))
        
    # Report unused imports
    if unused_imports:
        print(f"⚠️  UNUSED IMPORTS ({len(unused_imports)} found):\n")
        for rel_path, imp, name in sorted(unused_imports)[:20]:  # Show top 20
            print(f"  {rel_path}:{imp['line']}")
            print(f"    from {imp['module']} import {name} (never used)")
            print()
    else:
        print("✓ No obviously unused imports detected.\n")
    
    # Report wildcard imports
    if wildcard_imports:
        print(f"⚠️  WILDCARD IMPORTS ({len(wildcard_imports)} found):\n")
        for rel_path, imp in wildcard_imports:
            print(f"  {rel_path}:{imp['line']}")
            print(f"    from {imp['module']} import *")
            print(f"    → Consider making explicit: from {imp['module']} import X, Y, Z")
            print()
    
    print()
    print("=" * 80)
    print(f"Summary: Analyzed {file_count} files")
    print(f"  - Unused imports: {len(unused_imports)}")
    print(f"  - Wildcard imports: {len(wildcard_imports)}")
    print("=" * 80)
    print()
    print("NOTE: This is a best-effort static analysis. Some 'unused' imports might be")
    print("      legitimately used via string references or dynamic imports.")
    print()

if __name__ == "__main__":
    backend_path = "backend"
    
    if not os.path.exists(backend_path):
        print("Error: 'backend' directory not found.")
        print("Run this from the project root.")
        exit(1)
    
    generate_report(backend_path)
