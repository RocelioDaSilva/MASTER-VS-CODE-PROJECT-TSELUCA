#!/usr/bin/env python
import subprocess
import sys

# Run pytest tests
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=no"],
    capture_output=True,
    text=True,
    timeout=120
)

print(result.stdout)
print(result.stderr)
sys.exit(result.returncode)
