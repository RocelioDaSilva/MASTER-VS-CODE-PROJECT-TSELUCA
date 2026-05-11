import subprocess
import sys


def test_manuscript_front_matter_ok():
    # Run the front-matter checker on the manuscript folder
    result = subprocess.run([sys.executable, 'scripts/check_front_matter.py', '--path', 'manuscript'], capture_output=True, text=True)
    print(result.stdout)
    assert result.returncode == 0
