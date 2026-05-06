# Build Windows App: Quick Start

## ⚡ ONE-COMMAND BUILD (Recommended)

```powershell
cd "c:\Users\rocel\OneDrive\Desktop\Full project-20260219T174551Z-1-001 - Cópia\MIT-SCIENCE-PAPER\Full project\02_Code\geesp-angola"

python build_windows_app.py
```

**That's it!** Script handles everything:
- ✓ Installs PyInstaller if needed
- ✓ Cleans previous builds
- ✓ Generates synthetic maps
- ✓ Builds executable

---

## 📊 Result

```
✅ GEESP-Angola.exe created in: dist/GEESP-Angola/

Size: ~800 MB
Ready to: 
  - Double-click to run
  - Distribute to others
  - Create installer
```

---

## 🎯 What You Get

**Single Folder:** `dist/GEESP-Angola/`
- `GEESP-Angola.exe` - Main app (double-click to launch)
- Python runtime (bundled inside)
- All dependencies (numpy, pandas, streamlit, etc)
- Data files (synthetic maps)

**Double-click exe → Browser opens → Dashboard ready**

---

## 📦 Distribute

Zip the folder:
```
GEESP-Angola-v1.0.zip
  └── dist/GEESP-Angola/  (all files inside)
```

Send to others. They just:
1. Download + unzip
2. Double-click `GEESP-Angola.exe`
3. Dashboard opens

No Python, pip, or dependencies needed. It's **self-contained**.

---

## 🔧 Manual Build (if script doesn't work)

```powershell
# 1. Install PyInstaller
pip install pyinstaller

# 2. Build
cd geesp-angola
pyinstaller GEESP-Angola.spec --clean

# 3. Test
.\dist\GEESP-Angola\GEESP-Angola.exe
```

---

## 💡 Pro Tips

**Smaller Size (~400 MB):** Edit `GEESP-Angola.spec`
```python
# Change:
console=False  # Hides console window, smaller footprint
```

**Faster Startup:** Keep console visible
```python
console=True  # 2 second startup instead of 5
```

**Custom Icon:** Add icon file
```python
icon='app_icon.ico'  # Place .ico file in this directory
```

---

## ✅ Success Checklist

```
☐ Python 3.10+ installed
☐ All dependencies: pip install -r requirements.txt
☐ Synthetic maps exist: data/processed/*.npy
☐ launcher.py created
☐ GEESP-Angola.spec created
☐ PyInstaller installed: pip install pyinstaller
☐ Run: python build_windows_app.py
☐ Check: dist/GEESP-Angola/GEESP-Angola.exe exists
☐ Test: Double-click exe
✓ Dashboard appears in browser
```

---

## 🆘 Troubleshooting

**"ModuleNotFoundError" when running exe:**
- Solution: Edit `GEESP-Angola.spec`
- Add missing module to `hiddenimports=[]`
- Rebuild: `python build_windows_app.py`

**"Port already in use":**
- Solution: Close other Streamlit instances
- Or change port in `launcher.py`

**"Data files not found":**
- Solution: Verify `data/processed/` has 6 .npy files
- Generate: `python generate_synthetic_maps_quick.py`
- Rebuild: `python build_windows_app.py`

---

## 📈 Size Comparison

| Component | Size |
|-----------|------|
| Python runtime | 100 MB |
| Streamlit | 200 MB |
| NumPy/Pandas | 350 MB |
| Other libs | 50 MB |
| Your app | < 1 MB |
| Data (maps) | 6 MB |
| **Total** | **~800 MB** |

---

## 🚀 Next: Create Professional Installer

If you want users to install via `Setup.exe`:

```bash
# Download NSIS: https://nsis.sourceforge.io/

# Create: installer.nsi
# Run: makensis installer.nsi
# Output: Setup-GEESP-Angola.exe
```

For now, just share `dist/GEESP-Angola/` folder.

---

## ✨ You now have a Windows application!

**Distribution ready** - Zip and send to stakeholders without requiring Python installation.

