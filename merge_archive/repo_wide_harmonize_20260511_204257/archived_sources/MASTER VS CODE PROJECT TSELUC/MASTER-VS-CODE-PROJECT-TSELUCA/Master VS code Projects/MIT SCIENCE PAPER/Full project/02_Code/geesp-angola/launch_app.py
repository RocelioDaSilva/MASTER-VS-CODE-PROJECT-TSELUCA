#!/usr/bin/env python3
"""
GEESP-Angola Cross-Platform Launcher
One-click launcher that works on Windows, macOS, and Linux
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python():
    """Check if Python 3.11+ is available"""
    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10+ is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import numpy
        import pandas
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    requirements_file = Path(__file__).parent / "requirements-app.txt"
    if not requirements_file.exists():
        print(f"ERROR: {requirements_file} not found")
        return False
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        return True
    except subprocess.CalledProcessError:
        print("ERROR: Failed to install dependencies")
        return False

def create_directories():
    """Create necessary directories"""
    base_dir = Path(__file__).parent
    dirs = ["data/processed", "logs", "output"]
    for dir_path in dirs:
        (base_dir / dir_path).mkdir(parents=True, exist_ok=True)

def launch_app():
    """Launch the Streamlit application"""
    app_file = Path(__file__).parent / "geesp_unified_app.py"
    if not app_file.exists():
        print(f"ERROR: {app_file} not found")
        return False
    
    print("\n" + "=" * 70)
    print("  GEESP-Angola Application")
    print("  Geospatial Energy for Equity & Solar Planning")
    print("=" * 70)
    print("\nStarting application...")
    print("The app will open in your default browser at http://localhost:8501")
    print("\nPress Ctrl+C to stop the application\n")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(app_file),
            "--server.headless=false",
            "--server.port=8501"
        ])
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user.")
        return True
    except Exception as e:
        print(f"\nERROR: Failed to launch application: {e}")
        return False

def main():
    """Main launcher function"""
    print("=" * 70)
    print("  GEESP-Angola Launcher")
    print("=" * 70)
    print()
    
    # Check Python version
    if not check_python():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("Dependencies not found. Installing...")
        if not install_dependencies():
            sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Launch app
    if not launch_app():
        sys.exit(1)

if __name__ == "__main__":
    main()
