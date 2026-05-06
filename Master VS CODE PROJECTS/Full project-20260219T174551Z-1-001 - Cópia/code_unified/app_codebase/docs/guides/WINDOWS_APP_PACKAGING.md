# GEESP-Angola: Windows App Packaging Guide

**Date:** March 3, 2026  
**Goal:** Convert Streamlit dashboard into Windows .exe application

---

## 📊 Three Options Comparison

| Option | Effort | Result | Size | UX |
|--------|--------|--------|------|-----|
| **1: PyInstaller (Recommended)** | ⭐ 15 min | Single .exe | ~800 MB | Streamlit in browser |
| **2: Installer (NSIS)** | ⭐⭐ 30 min | Setup.exe + app | ~900 MB | Professional installer |
| **3: Native Windows (WinForms)** | ⭐⭐⭐ 2 hours | Native app (.exe) | ~50 MB | True Windows integration |

---

## 🚀 OPTION 1: PyInstaller (FASTEST - 15 Minutes)

### Step 1: Install PyInstaller

```powershell
pip install pyinstaller
```

### Step 2: Generate Executable

Navigate to project folder and run:

```powershell
cd "c:\Users\rocel\OneDrive\Desktop\Full project-20260219T174551Z-1-001 - Cópia\MIT-SCIENCE-PAPER\Full project\02_Code\geesp-angola"

# Build from spec file
pyinstaller GEESP-Angola.spec --distpath ".\dist" --buildpath ".\build" --clean
```

**Expected output:**
```
✓ Building EXE from PYZ
✓ Successfully building 'GEESP-Angola.exe'
✓ Successfully building 'GEESP-Angola' folder in ./dist
```

### Step 3: Run the App

**Double-click:**
```
dist/GEESP-Angola/GEESP-Angola.exe
```

**What happens:**
1. Launcher opens (console window briefly)
2. Command: `streamlit run geesp_unified_app.py`
3. Browser opens automatically at `http://localhost:8501`
4. Dashboard appears

### Step 4: Create Shortcut (Optional)

```powershell
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$HOME\Desktop\GEESP-Angola.lnk")
$Shortcut.TargetPath = "$PWD\dist\GEESP-Angola\GEESP-Angola.exe"
$Shortcut.WorkingDirectory = "$PWD\dist\GEESP-Angola"
$Shortcut.IconLocation = "$PWD\dist\GEESP-Angola\GEESP-Angola.exe"
$Shortcut.Save()
```

**Result:** Desktop icon to launch app with double-click

---

## 📦 OPTION 2: Professional Installer (NSIS - 30 Minutes)

Creates `Setup-GEESP-Angola.exe` that users can install like normal Windows software

### Step 1: Install NSIS

Download: https://nsis.sourceforge.io/Download

### Step 2: Create Installer Script

Create file: `installer.nsi`

```nsis
; GEESP-Angola Installer Script
; Build with: makensis installer.nsi

!include "MUI2.nsh"

Name "GEESP-Angola"
OutFile "Setup-GEESP-Angola.exe"
InstallDir "$PROGRAMFILES\GEESP-Angola"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "dist\GEESP-Angola\*.*"
  
  ; Create Start Menu shortcut
  CreateDirectory "$SMPROGRAMS\GEESP-Angola"
  CreateShortcut "$SMPROGRAMS\GEESP-Angola\GEESP-Angola.lnk" "$INSTDIR\GEESP-Angola.exe"
  CreateShortcut "$DESKTOP\GEESP-Angola.lnk" "$INSTDIR\GEESP-Angola.exe"
  
  ; Uninstaller
  CreateShortcut "$SMPROGRAMS\GEESP-Angola\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
  RMDir /r "$INSTDIR"
  RMDir /r "$SMPROGRAMS\GEESP-Angola"
  Delete "$DESKTOP\GEESP-Angola.lnk"
SectionEnd
```

### Step 3: Build Installer

```powershell
# Install NSIS first, then:
& "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
```

**Output:** `Setup-GEESP-Angola.exe` in current directory

### Step 4: Distribute

Double-click `Setup-GEESP-Angola.exe` and it:
- Creates `C:\Program Files\GEESP-Angola\`
- Adds Start Menu shortcuts
- Registers uninstall in Control Panel → Programs

---

## 💻 OPTION 3: Native Windows App (WinForms - 2 Hours)

Convert to true native Windows application using IronPython or create C# wrapper

### Simplified Approach: Python GUI Wrapper

Create native Windows window that hosts Streamlit:

```python
# Create file: windows_app.py
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import webbrowser
import time

class GEESPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GEESP-Angola")
        self.root.geometry("400x300")
        self.process = None
        
        # GUI Elements
        tk.Label(root, text="GEESP-Angola", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root, text="Community Solar Site Analysis").pack()
        
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Start Dashboard", command=self.start_app).pack(pady=5)
        ttk.Button(btn_frame, text="Stop", command=self.stop_app).pack(pady=5)
        ttk.Button(btn_frame, text="Exit", command=root.quit).pack(pady=5)
        
        self.status = tk.Label(root, text="Ready", fg="blue")
        self.status.pack(pady=10)
    
    def start_app(self):
        if self.process is None:
            self.status.config(text="Starting...", fg="orange")
            thread = threading.Thread(target=self._run_streamlit)
            thread.daemon = True
            thread.start()
    
    def _run_streamlit(self):
        self.process = subprocess.Popen([
            'streamlit', 'run', 'geesp_unified_app.py',
            '--server.port=8501'
        ])
        time.sleep(3)
        webbrowser.open('http://localhost:8501')
        self.status.config(text="Running at localhost:8501", fg="green")
        self.process.wait()
        self.status.config(text="Stopped", fg="red")
        self.process = None
    
    def stop_app(self):
        if self.process:
            self.process.terminate()
            self.status.config(text="Stopping...", fg="orange")

root = tk.Tk()
app = GEESPApp(root)
root.mainloop()
```

Then package this with PyInstaller:

```bash
pyinstaller --onefile --windowed --name "GEESP-Angola" windows_app.py
```

---

## 🔧 Troubleshooting

### Issue: "Streamlit module not found in .exe"

**Solution:** Verify `GEESP-Angola.spec` includes all hidden imports:
```python
hiddenimports=[
    'streamlit',
    'numpy', 
    'pandas',
    'geopandas',
    'rasterio',
    'plotly',
    'folium',
    # ... add any missing modules
]
```

Then rebuild:
```bash
pyinstaller GEESP-Angola.spec --clean
```

---

### Issue: "Data files not included in .exe"

**Solution:** Verify spec file `datas=` section:
```python
datas=[
    ('data/processed', 'data/processed'),
    ('geesp_unified_app.py', '.'),
    ('scripts', 'scripts'),
]
```

---

### Issue: "Port 8501 already in use"

**Solution:** Modify launcher to use different port:
```python
port = 8502  # Change in launcher.py
```

---

### Issue: ".env file not found"

**Solution:** Create inside exe directory or bundle it:

```python
# In launcher.py, create if missing:
env_file = app_dir / '.env'
if not env_file.exists():
    with open(env_file, 'w') as f:
        f.write('ENV=production\n')
        f.write('LOG_LEVEL=INFO\n')
```

---

## 📊 Size Breakdown

**PyInstaller Output (Option 1):**
```
GEESP-Angola/
├── GEESP-Angola.exe        (25 MB - launcher)
├── python*.dll             (100 MB - Python runtime)
├── _internal/
│   ├── streamlit/          (200 MB - Streamlit + deps)
│   ├── numpy/              (150 MB)
│   ├── pandas/             (200 MB)
│   ├── geopandas/          (50 MB)
│   └── ... other libs
├── data/processed/         (6 MB - maps)
└── geesp_unified_app.py

Total: ~800-900 MB
```

**Optimizer Tips:**
1. Remove unused packages from spec file
2. Use `--onefile` option (creates single .exe, slower startup)
3. Strip debug symbols: `strip=True` in spec

---

## 🎯 Recommended Setup for Distribution

**For End Users (Easiest):**

Create folder structure:
```
GEESP-Angola-Installer/
├── Setup-GEESP-Angola.exe  (NSIS installer)
├── README.txt              (Quick start guide)
├── requirements.txt        (For reference)
└── LICENSE
```

Users download, run `Setup-GEESP-Angola.exe`, app installs to `C:\Program Files\GEESP-Angola\`

**For Developers (Development):**

Keep using:
```bash
streamlit run geesp_unified_app.py
```

---

## 📝 Quick Build Checklist

Before packaging:

```
☐ 1. All dependencies installed: pip install -r requirements.txt
☐ 2. Synthetic maps generated: python generate_synthetic_maps_quick.py
☐ 3. Streamlit app tested: streamlit run geesp_unified_app.py
☐ 4. .env file configured
☐ 5. Data directory in place: data/processed/*.npy
☐ 6. PyInstaller installed: pip install pyinstaller
☐ 7. GEESP-Angola.spec updated with correct file paths
☐ 8. launcher.py in place
```

---

## 🚀 Complete Build Sequence

```powershell
# Navigate to project
cd "c:\Users\rocel\OneDrive\Desktop\Full project-20260219T174551Z-1-001 - Cópia\MIT-SCIENCE-PAPER\Full project\02_Code\geesp-angola"

# 1. Install PyInstaller
pip install pyinstaller

# 2. Clean previous builds
Remove-Item -Path ".\build", ".\dist" -Recurse -ErrorAction SilentlyContinue

# 3. Build executable
pyinstaller GEESP-Angola.spec --clean

# 4. Test executable
.\dist\GEESP-Angola\GEESP-Angola.exe

# 5. Create desktop shortcut (optional)
# Then distribute dist/GEESP-Angola folder to end users
```

---

## 📦 Distribution Package

Send end-users this folder structure:

```
Download: GEESP-Angola-v1.0.zip

GEESP-Angola-v1.0/
├── GEESP-Angola.exe          (Main app - double-click to run)
├── README.md                 (Quick start guide)
├── REQUIREMENTS.txt          (System requirements)
├── LICENSE                   (MIT License)
└── data/processed/           (Synthetic maps included)
```

---

## ✅ Success Criteria

After packaging:

```
✓ Double-click .exe launches dashboard
✓ Browser opens automatically
✓ Data loads from bundled files
✓ All 6 MCDA sliders work
✓ LCOE calculator produces output
✓ No console errors
✓ App size < 1 GB
✓ Startup time < 5 seconds
```

---

## 🎓 Next Steps

1. **Test locally:** `pyinstaller GEESP-Angola.spec`
2. **Test standalone:** Run `dist/GEESP-Angola/GEESP-Angola.exe` from different folder
3. **Create installer:** Optional NSIS installer for professional distribution
4. **Deploy:** Share with stakeholders

**Recommendation:** Start with **Option 1 (PyInstaller)** - it takes 15 minutes and gives you a fully functional Windows app ready to distribute.

