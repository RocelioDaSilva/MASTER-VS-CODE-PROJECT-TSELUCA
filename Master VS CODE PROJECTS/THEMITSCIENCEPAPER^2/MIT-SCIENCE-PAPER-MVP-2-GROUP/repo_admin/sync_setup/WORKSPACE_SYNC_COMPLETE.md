# Syncthing Master VS CODE Projects Sync Setup Complete

**Date:** May 1, 2026  
**Status:** ✅ Desktop (NEXUS) Configured & Scanning

---

## Desktop Configuration Summary

### Syncthing Status
- **Device Name:** NEXUS (Desktop)
- **Device ID:** `XVMNNZF-KDKG77E-AANW7M7-NXGJLW6-BGJN7BU-2SRELTE-3TEERVU-MDLZJAG`
- **Web UI:** http://127.0.0.1:8384
- **Version:** v2.1.0-rc.1 (Windows 64-bit)
- **Status:** ✅ Running & Syncing

### Shared Folders

#### 1. Master VS CODE Projects (Main Workspace)
- **Folder ID:** jxcu3-2upzt
- **Path:** `C:\Users\PCGAME\Desktop\Master VS CODE PROJECTS`
- **Status:** Scanning (768 files, ~48.9 MiB)
- **Share Type:** Send & Receive
- **Ignore Patterns:** Configured (see below)

#### 2. MIT-SCIENCE-PAPER (Subfolder - currently unshared)
- **Folder ID:** vz3f9-qvauy
- **Path:** `C:\Users\PCGAME\Desktop\Master VS CODE PROJECTS\THEMITSCIENCEPAPER^2\MIT-SCIENCE-PAPER-MVP-2-GROUP`
- **Status:** Unshared
- **Note:** This is a subfolder of Master VS CODE Projects

### Configured Ignore Patterns
```
.git/                      # Git repository (backup to GitHub instead)
.venv/                     # Python virtual environment
venv/                      # Alternative venv
node_modules/              # Node dependencies
repo_admin/reorg_archives/ # Archive duplicates (manual backup)
.vscode/                   # VS Code user settings (sync separately if needed)
__pycache__/               # Python cache
*.pyc                      # Python compiled files
*.log                      # Log files
*.aux                      # LaTeX auxiliaries
*.fls                      # LaTeX file lists
*.fdb_latexmk              # LaTeX make database
*.toc                      # LaTeX table of contents
*.syncthing/               # Syncthing temp files
.DS_Store                  # macOS
Thumbs.db                  # Windows thumbnails
```

---

## Next Steps to Complete Sync Setup

### Step 1: Install Syncthing on Your Other PC
On each PC/Laptop, follow the same process:

**Option A: Use installer script (if Windows)**
```powershell
# Download and run the installer
powershell -ExecutionPolicy Bypass -File install_syncthing_windows.ps1
```

**Option B: Manual download**
- Visit: https://syncthing.net/downloads/
- Download Windows/Linux/macOS version
- Extract and run `syncthing.exe`

**Option C: Package manager (Linux)**
```bash
# Debian/Ubuntu
sudo apt install syncthing

# Arch
sudo pacman -S syncthing

# Then start:
syncthing &
```

### Step 2: Get Device ID from Other PC
1. Start Syncthing on the other PC
2. Open: http://127.0.0.1:8384
3. Go to: **Devices** → **This Device** → **Identification**
4. Copy the full Device ID (e.g., `ABCD1234-...`)

### Step 3: Add Other PC to NEXUS
1. On NEXUS: Open http://127.0.0.1:8384
2. Go to: **Devices** → **Add Remote Device**
3. Paste the other PC's Device ID
4. Click **Add Device**
5. Set a device name (e.g., "Laptop-1")

### Step 4: Accept Connection on Other PC
1. On the other PC's Syncthing web UI
2. A notification will appear: "Device NEXUS wants to connect"
3. Click **Accept**

### Step 5: Add Folder Share on Other PC
1. On other PC: Go to **Folders** → **Add Folder**
2. Set **Folder Label:** `Master VS CODE Projects` (or same as NEXUS)
3. Set **Folder ID:** `jxcu3-2upzt` (MUST match NEXUS)
4. Set **Folder Path:** Same local path (or equivalent)
5. Go to **Ignore Patterns** tab
6. Copy ignore patterns from DEVICE_IDS.txt or .stignore.example
7. Go to **Sharing** tab
8. Check **NEXUS** to share with it
9. Click **Save**

### Step 6: Wait for Sync
- First sync may take several minutes depending on folder size (~49 MiB)
- Monitor progress in Syncthing web UI
- Watch download rate on NEXUS and upload rate on other PC

### Step 7: Test Sync
1. Create a new file on one device: `test-sync-$(date).txt`
2. Check if it appears on other devices within 1-2 minutes
3. Verify that files matching ignore patterns are NOT synced

### Step 8: Repeat for Second PC (if applicable)
- Follow Steps 1-7 for your second laptop
- When both are connected, files will sync to all three devices

---

## Canonical Backup Strategy

**Important:** Syncthing syncs files in real-time, but for canonical backup:

1. **Use GitHub as authoritative backup:**
   ```bash
   git add .
   git commit -m "backup: $(date)"
   git push origin main
   ```

2. **Automate periodic backups:**
   - Run the above command on a schedule (cron job / Task Scheduler)
   - Or use `auto_git_push.sh` script (with caution)

3. **Never rely on Syncthing alone:**
   - Syncthing is for real-time sync, not backup
   - Deleted files sync too (will be deleted on all devices!)
   - Use Git history as your backup

---

## Troubleshooting

### Folder not syncing?
- ✅ Check Folder ID matches on all devices (must be identical)
- ✅ Check devices are "Connected" (green dot in web UI)
- ✅ Verify Ignore Patterns didn't exclude important files
- ✅ Check file permissions on both devices
- ✅ Restart Syncthing if needed

### Conflicts?
- Syncthing creates `.sync-conflict-TIMESTAMP-HOSTNAME` files
- Manually review and merge conflicts
- Delete `.sync-conflict-*` files after merging

### Performance issues?
- Pause folder scanning if too slow: **Folder** → **Pause**
- Increase rescan interval: **Folder Edit** → **General** → **Rescans**
- Disable "Block Indexing" for faster scanning

### Connection issues?
- Check firewall (Syncthing uses ports 22000-22999)
- Ensure both devices are on same network or have Internet access
- Verify discovery servers are working: **Settings** → **Connections**

---

## Device Registration

```
NEXUS (Desktop)
✅ CONFIGURED & RUNNING
ID: XVMNNZF-KDKG77E-AANW7M7-NXGJLW6-BGJN7BU-2SRELTE-3TEERVU-MDLZJAG
Uptime: 31+ minutes
Folders: Master VS CODE Projects (scanning)

Laptop #1
⏳ TO BE CONFIGURED
ID: [pending installation]
Status: Waiting for installation

Laptop #2
⏳ TO BE CONFIGURED
ID: [pending installation]
Status: Waiting for installation
```

---

## Key Files Location

All configuration scripts and guides are in:
```
MIT-SCIENCE-PAPER-MVP-2-GROUP/repo_admin/sync_setup/
├── README_SYNC.md                    # Original sync setup guide
├── SYNCTHING_SETUP_GUIDE.md          # Detailed guide
├── DEVICE_IDS.txt                    # Quick reference with Device IDs
├── .stignore.example                 # Ignore patterns template
├── install_syncthing_windows.ps1     # Windows installer
├── install_syncthing_linux.sh        # Linux installer
└── auto_git_push.sh                  # Optional auto-commit helper
```

---

## Resources

- **Syncthing Documentation:** https://docs.syncthing.net/
- **Syncthing Forum:** https://forum.syncthing.net/
- **GitHub Backup:** https://github.com/RocelioDaSilva/MIT-SCIENCE-PAPER-MVP-2-GROUP

---

**Last Updated:** 2026-05-01  
**Configuration Time:** ~30 minutes  
**Next Update:** After laptops are configured
