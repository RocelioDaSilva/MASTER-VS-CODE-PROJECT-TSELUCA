"""
Automated PyInstaller Build Script for GEESP-Angola
Builds Windows .exe with single command
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("=" * 70)
    print("GEESP-Angola Windows App Builder")
    print("=" * 70)
    print()
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller not found.")
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✓ PyInstaller installed\n")
    
    # Get project directory
    project_dir = Path(__file__).parent
    spec_file = project_dir / "GEESP-Angola.spec"
    
    print(f"Project directory: {project_dir}")
    print(f"Spec file: {spec_file}")
    print()
    
    # Verify spec file exists
    if not spec_file.exists():
        print("❌ GEESP-Angola.spec not found!")
        print(f"Expected at: {spec_file}")
        return 1
    
    # Verify data directory
    data_dir = project_dir / "data" / "processed"
    if not data_dir.exists():
        print(f"⚠️  Data directory not found: {data_dir}")
        print("Generating synthetic maps...")
        gen_script = project_dir / "generate_synthetic_maps_quick.py"
        if gen_script.exists():
            subprocess.run([sys.executable, str(gen_script)], check=False)
        else:
            print("⚠️  Could not generate maps automatically")
    
    # Verify launcher exists
    launcher = project_dir / "launcher.py"
    if not launcher.exists():
        print(f"❌ launcher.py not found at {launcher}")
        return 1
    
    # Verify main app exists
    app_file = project_dir / "geesp_unified_app.py"
    if not app_file.exists():
        print(f"❌ geesp_unified_app.py not found at {app_file}")
        return 1
    
    print("✓ All prerequisites verified\n")
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for folder in ["build", "dist", "__pycache__"]:
        folder_path = project_dir / folder
        if folder_path.exists():
            shutil.rmtree(folder_path)
            print(f"  ✓ Removed {folder}")
    
    print()
    print("=" * 70)
    print("Building executable from spec file...")
    print("=" * 70)
    print()
    
    # Run PyInstaller
    try:
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            str(spec_file),
            "--distpath", str(project_dir / "dist"),
            "--buildpath", str(project_dir / "build"),
            "--clean"
        ], check=False)
        
        if result.returncode != 0:
            print("\n❌ PyInstaller build failed!")
            return 1
        
    except Exception as e:
        print(f"\n❌ Error running PyInstaller: {e}")
        return 1
    
    # Verify output
    exe_path = project_dir / "dist" / "GEESP-Angola" / "GEESP-Angola.exe"
    
    print()
    print("=" * 70)
    if exe_path.exists():
        exe_size = exe_path.stat().st_size / (1024*1024)
        print(f"✅ SUCCESS! Windows app created!")
        print("=" * 70)
        print()
        print(f"Location: {exe_path}")
        print(f"Size: {exe_size:.1f} MB")
        print()
        print("To run the app, double-click:")
        print(f"  {project_dir / 'dist' / 'GEESP-Angola' / 'GEESP-Angola.exe'}")
        print()
        print("To distribute, zip the folder:")
        print(f"  {project_dir / 'dist' / 'GEESP-Angola'}")
        print()
        print("What happens when you run it:")
        print("  1. Launcher starts (brief console window)")
        print("  2. Streamlit service initializes")
        print("  3. Browser opens at http://localhost:8501")
        print("  4. Dashboard appears with 6 MCDA criteria")
        print()
        
        # Ask if user wants to test
        response = input("Do you want to test the app now? (y/n): ").strip().lower()
        if response == 'y':
            print("\nLaunching GEESP-Angola...\n")
            os.startfile(str(exe_path))
            print("App launched! Check your browser.")
        
        return 0
    else:
        print(f"❌ Build failed - executable not found at {exe_path}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
