#!/usr/bin/env python
"""
PHASE 2: FIX WINDOWS UNICODE LOGGING
Configure UTF-8 encoding for Windows console output
"""

import os
import re
from pathlib import Path

print("=" * 70)
print("PHASE 2: WINDOWS UNICODE LOGGING FIX")
print("=" * 70)

# Read the logging setup file
logging_file = Path("utils/logging_setup.py")

if not logging_file.exists():
    print(f"\n✗ ERROR: {logging_file} not found!")
else:
    print(f"\n[STEP 1] Analyzing {logging_file}")
    print("-" * 70)
    
    with open(logging_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for UTF-8 encoding specification
    has_utf8 = 'encoding' in content and 'utf-8' in content.lower()
    
    if has_utf8:
        print("✓ UTF-8 encoding already configured")
    else:
        print("✗ UTF-8 encoding not found - needs fixing")
        print("\nRecommended fix:")
        print("""
  Add encoding='utf-8' to all logging handlers:
  
  # For FileHandler:
  file_handler = logging.FileHandler(
      log_file,
      encoding='utf-8'
  )
  
  # For StreamHandler (console):
  stream_handler = logging.StreamHandler()
  # Or on Windows:
  if sys.platform == 'win32':
      import io
      stream_handler.stream = io.TextIOWrapper(
          sys.stdout.buffer,
          encoding='utf-8'
      )
""")

print("\n[STEP 2] Environment Configuration")
print("-" * 70)

print("\nFor Windows, additionally set:")
print("  SET PYTHONIOENCODING=utf-8")
print("\nOr in Python code at startup:")
print("  os.environ['PYTHONIOENCODING'] = 'utf-8'")

print("\n[STEP 3] Test Configuration")
print("-" * 70)

print("\nTest Portuguese/Unicode characters:")
test_strings = [
    ("Check mark", "✓"),
    ("Portuguese ã", "ão"),
    ("Portuguese ç", "ç"),
    ("Portuguese é", "é"),
    ("Cross mark", "✗"),
]

print("\nTesting console output:")
try:
    for label, char in test_strings:
        print(f"  {label}: {char}")
    print("\n  If above characters display correctly, encoding is working!")
except UnicodeEncodeError as e:
    print(f"\n  ✗ UnicodeEncodeError: {e}")
    print("  Solution: Set PYTHONIOENCODING=utf-8")

print("\n" + "=" * 70)
print("PHASE 2: UNICODE LOGGING IMPLEMENTATION GUIDE")
print("=" * 70)

print("""
WINDOWS CONSOLE ENCODING ISSUES:

Problem:
  • Python on Windows uses 'cp1252' encoding by default
  • Portuguese characters (ã, ç, é) fail to display
  • Unicode symbols (✓, ✗, ⚠) cause errors

Solution:
  1. Set environment variable:
     SET PYTHONIOENCODING=utf-8
  
  2. Update logging_setup.py handlers:
     - Add encoding='utf-8' to FileHandler
     - Wrap stdout for console output
  
  3. Add to main entry points:
     os.environ['PYTHONIOENCODING'] = 'utf-8'

Impact:
  • Minimal - only affects console display
  • Functionality unaffected
  • All output readable with proper encoding

Status: Requires code update in utils/logging_setup.py
Complexity: Low
Estimated time: 30 minutes
""")

print("For implementation, see: PHASE2_UNICODE_LOGGING_FIX.md")
