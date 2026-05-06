# Syncthing Multi-Device Sync Setup
**Status:** ✅ Desktop (NEXUS) - Installed & Running  
**Date:** May 1, 2026

---

## Desktop Device (NEXUS)
**Installation Status:** ✅ Complete  
**Web UI:** http://127.0.0.1:8384  
**Device ID:** `XVMNNZF-KDKG77E-AANW7M7-NXGJLW6-BGJN7BU-2SRELTE-3TEERVU-MDLZJAG`  
**Location:** `C:\Users\PCGAME\AppData\Roaming\Syncthing\syncthing.exe`  
**Status:** Running in background (PID: 18208, 20656)

---

## Setup Steps for Remaining Devices

### Laptop Device #1 & #2
Follow the same process for each laptop:

1. **Install Syncthing**
   - Use the installer scripts from `repo_admin/sync_setup/`
   - Windows: `install_syncthing_windows.ps1`
   - Linux: `install_syncthing_linux.sh`
   - Or download directly: https://syncthing.net/downloads/

2. **Start Syncthing**
   - Windows: Run `syncthing.exe` (will start web UI on http://127.0.0.1:8384)
   - Linux: `syncthing &`

3. **Note Your Device ID**
   - Open http://127.0.0.1:8384 in browser
   - Go to Devices → This Device → click "Identification" → copy full Device ID

4. **Add NEXUS (Desktop) as Remote Device**
   - In web UI: Devices → Add Remote Device
   - Paste Device ID: `XVMNNZF-KDKG77E-AANW7M7-NXGJLW6-BGJN7BU-2SRELTE-3TEERVU-MDLZJAG`
   - Device Name: `NEXUS-DESKTOP` (or similar)
   - Click Add Device
   - On NEXUS, accept the connection

5. **Add Folder Share**
   - In web UI: Folders → Add Folder
   - Folder Path: Path to your project folder (same on all devices or choose local equivalent)
   - Label: `MIT-SCIENCE-PAPER` or similar
   - Devices: Check all connected devices
   - Ignore Patterns: Copy from `repo_admin/sync_setup/.stignore.example`
   - Click Save

6. **Wait for Initial Sync**
   - First sync may take time depending on folder size
   - Monitor progress in web UI: Devices section

---

## Device IDs (To be filled in as devices are added)

```
NEXUS (Desktop):
  ID: XVMNNZF-KDKG77E-AANW7M7-NXGJLW6-BGJN7BU-2SRELTE-3TEERVU-MDLZJAG
  Status: ✅ Running
  Host: 127.0.0.1:8384

Laptop #1:
  ID: [TO BE CONFIGURED]
  Status: ⏳ Pending
  Host: [IP address]

Laptop #2:
  ID: [TO BE CONFIGURED]
  Status: ⏳ Pending
  Host: [IP address]
```

---

## Ignore Patterns
The following patterns are automatically excluded from sync (copy to folder Ignore Patterns):
```
.git/
.venv/
venv/
node_modules/
repo_admin/reorg_archives/
.vscode/
__pycache__/
*.pyc
*.log
*.aux
*.fls
*.fdb_latexmk
*.toc
*.syncthing/
.DS_Store
Thumbs.db
```

---

## Configuration Notes

### Recommended Settings
1. **Auto-enable on device startup**
   - Syncthing should auto-start on all devices
   - Task Scheduler (Windows) / Systemd (Linux) / LaunchAgent (macOS)

2. **Keep git history separate**
   - `.git/` folders are excluded to avoid merge conflicts
   - All devices pull from `origin/main` as canonical backup
   - Use `git pull` before making changes to stay in sync

3. **Conflict Resolution**
   - If file conflicts occur during sync, Syncthing creates `.sync-conflict-*` files
   - Review and manually merge conflicts (typically rare with .stignore patterns)

4. **Storage Requirements**
   - Each device needs full copy of workspace (estimate: [SIZE_TO_BE_MEASURED])
   - Syncthing uses `.syncthing/` temporary directory during transfer (excluded)

---

## Testing Real-Time Sync

1. **Test on one device:**
   - Create a new file `test-sync-$(date).txt` in the workspace root
   - Check if it appears on other devices within 30-60 seconds

2. **Test file updates:**
   - Edit a file on one device
   - Verify changes appear on other devices

3. **Verify ignore patterns:**
   - Create a file matching ignore patterns (e.g., `test.pyc`)
   - Confirm it does NOT sync to other devices

---

## Emergency Access
If Syncthing UI is inaccessible:

**Windows:**
```powershell
# Restart Syncthing
Get-Process syncthing | Stop-Process
Start-Process 'C:\Users\PCGAME\AppData\Roaming\Syncthing\syncthing.exe' -WindowStyle Hidden
```

**Linux:**
```bash
pkill syncthing
syncthing &
```

---

## Next Steps
1. ✅ Install & configure Syncthing on NEXUS (Desktop) — **DONE**
2. ⏳ Install & configure Syncthing on Laptop #1
3. ⏳ Install & configure Syncthing on Laptop #2
4. ⏳ Add all devices to each other (bidirectional trust)
5. ⏳ Create folder share on all devices
6. ⏳ Test sync with sample file
7. ⏳ Update this guide with Device IDs and test results

---

## Backup Strategy
- **Real-time sync:** Syncthing keeps devices synchronized
- **Canonical backup:** `origin/main` on GitHub remains authoritative
- **Automated backup:** Run `git add .; git commit -m "auto-backup"; git push origin main` periodically
- **Manual versioning:** Syncthing's Simple File Versioning available in folder settings

---

## Troubleshooting

### Syncthing won't start
- Check if another instance is already running: `tasklist | find syncthing`
- Verify binary exists at installation path
- Check Windows Event Viewer for errors

### Folder not syncing
- Verify both devices are "Connected" (green dot in web UI)
- Check that both devices have folder added with same label
- Review .stignore patterns (may be excluding important files)
- Check folder path is correct and accessible on both devices

### Files showing as "Out of Sync"
- Check "Failed Items" in web UI Folders section
- Common causes: insufficient disk space, file permissions, antivirus interference
- Solution: Pause sync, fix issue, resume

---

**Last Updated:** 2026-05-01  
**Config Files:** See `repo_admin/sync_setup/`
