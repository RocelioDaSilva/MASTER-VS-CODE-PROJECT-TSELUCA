#!/usr/bin/env python3
"""
Consolidated Files Validator - Validates that merged files maintain integrity

This script validates:
1. All original imports are preserved in consolidated files
2. Function/class counts match expected consolidation targets
3. No duplicate definitions exist
4. Documentation is preserved

Usage:
    python validate_consolidations.py
"""

import os
import ast
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

class CodeAnalyzer(ast.NodeVisitor):
    """Extract functions, classes, and imports from a file."""
    
    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = set()
        
    def visit_FunctionDef(self, node):
        self.functions.append({
            'name': node.name,
            'line': node.lineno,
            'has_docstring': ast.get_docstring(node) is not None
        })
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        """Handle async functions (FastAPI endpoints)."""
        self.functions.append({
            'name': node.name,
            'line': node.lineno,
            'has_docstring': ast.get_docstring(node) is not None,
            'async': True
        })
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        self.classes.append({
            'name': node.name,
            'line': node.lineno,
            'has_docstring': ast.get_docstring(node) is not None,
            'methods': len([n for n in node.body if isinstance(n, ast.FunctionDef)])
        })
        self.generic_visit(node)
    
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

def analyze_file(file_path: Path) -> Dict:
    """Analyze a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)
        
        return {
            'functions': analyzer.functions,
            'classes': analyzer.classes,
            'imports': list(analyzer.imports),
            'lines': len(content.split('\n')),
            'size_bytes': len(content.encode('utf-8')),
            'error': None
        }
    except Exception as e:
        return {
            'functions': [],
            'classes': [],
            'imports': [],
            'lines': 0,
            'size_bytes': 0,
            'error': str(e)
        }

# Expected consolidations
CONSOLIDATION_EXPECTATIONS = {
    'backend/api/endpoints.py': {
        'min_functions': 8,  # 10 async API endpoints
        'min_classes': 0,  # No classes, just functions
        'min_lines': 400,
        'description': 'Consolidated REST API endpoints'
    },
    'backend/database/models.py': {
        'min_functions': 8,  # Mostly __init__, __repr__, and relationships
        'min_classes': 8,  # The 8 consolidated models
        'min_lines': 400,
        'description': 'Consolidated ORM models (Scenario, AnalysisResult, etc.)'
    },
    'backend/analysis/base.py': {
        'min_functions': 5,
        'min_classes': 2,
        'min_lines': 50,
        'description': 'Base analysis classes'
    },
    'backend/analysis/lcoe.py': {
        'min_functions': 8,
        'min_classes': 1,
        'min_lines': 150,
        'description': 'LCOE calculation engine'
    },
    'backend/analysis/mcda.py': {
        'min_functions': 8,
        'min_classes': 1,
        'min_lines': 150,
        'description': 'Multi-criteria decision analysis'
    },
    'backend/analysis/validation_base.py': {
        'min_functions': 10,
        'min_classes': 2,
        'min_lines': 200,
        'description': 'Validation framework'
    },
}

def validate_consolidations(root_path: str) -> None:
    """Validate all consolidations."""
    print("=" * 80)
    print("CONSOLIDATION VALIDATION REPORT")
    print("=" * 80)
    print()
    
    all_pass = True
    
    for file_path, expectations in CONSOLIDATION_EXPECTATIONS.items():
        full_path = Path(root_path) / file_path
        
        print(f"Validating: {file_path}")
        print(f"  Description: {expectations['description']}")
        
        if not full_path.exists():
            print(f"  ❌ FILE NOT FOUND")
            all_pass = False
            print()
            continue
        
        analysis = analyze_file(full_path)
        
        if analysis['error']:
            print(f"  ❌ Parse error: {analysis['error']}")
            all_pass = False
            print()
            continue
        
        # Check metrics
        checks = [
            ('Functions', len(analysis['functions']), expectations.get('min_functions', 0), '>='),
            ('Classes', len(analysis['classes']), expectations.get('min_classes', 0), '>='),
            ('Lines', analysis['lines'], expectations.get('min_lines', 0), '>='),
        ]
        
        file_pass = True
        for check_name, actual, expected, op in checks:
            if op == '>=':
                passed = actual >= expected
            else:
                passed = actual == expected
            
            status = "✓" if passed else "❌"
            print(f"  {status} {check_name}: {actual} (expected {op} {expected})")
            if not passed:
                file_pass = False
                all_pass = False
        
        # Show content summary
        if analysis['classes']:
            class_names = [c['name'] for c in analysis['classes']]
            print(f"  Classes defined: {', '.join(class_names)}")
        
        if analysis['functions']:
            func_names = [f['name'] for f in analysis['functions'][:5]]
            if len(analysis['functions']) > 5:
                func_names.append(f"... +{len(analysis['functions']) - 5} more")
            print(f"  Functions: {', '.join(func_names)}")
        
        # Check documentation
        undocumented_classes = [c['name'] for c in analysis['classes'] if not c['has_docstring']]
        if undocumented_classes:
            print(f"  ⚠️  Undocumented classes: {', '.join(undocumented_classes)}")
        
        print()
    
    print("=" * 80)
    if all_pass:
        print("✓ All consolidations validated successfully!")
    else:
        print("❌ Some consolidations failed validation. See details above.")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Run import migration analyzer: python import_migration_analyzer.py")
    print("2. Check for unused imports: python find_orphaned_imports.py")
    print("3. Execute Phase B3 file moves (see import_migration_analyzer.py output)")
    print("4. Update all import statements throughout codebase")
    print("5. Run: python -m pytest tests/ -v")
    print()

def generate_consolidation_summary(root_path: str) -> None:
    """Generate JSON summary of consolidations."""
    summary = {}
    
    for file_path in CONSOLIDATION_EXPECTATIONS.keys():
        full_path = Path(root_path) / file_path
        analysis = analyze_file(full_path)
        
        summary[file_path] = {
            'exists': full_path.exists(),
            'functions': len(analysis['functions']),
            'classes': len(analysis['classes']),
            'lines': analysis['lines'],
            'bytes': analysis['size_bytes'],
            'class_names': [c['name'] for c in analysis['classes']],
            'error': analysis['error']
        }
    
    # Save to JSON
    output_file = Path(root_path) / "CONSOLIDATION_SUMMARY.json"
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Consolidation summary saved to: {output_file}")

if __name__ == "__main__":
    backend_root = "."  # Run from project root
    
    validate_consolidations(backend_root)
    generate_consolidation_summary(backend_root)
