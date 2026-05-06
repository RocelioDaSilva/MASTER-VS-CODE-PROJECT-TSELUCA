Syncthing + GitHub: Real-time workspace sync

Overview
- Goal: Keep your working files in `Master VS CODE PROJECTS` (or a chosen workspace folder) synchronized between your desktop and laptops in near real-time, while keeping a canonical backup on GitHub.
- Approach: Use Syncthing (peer-to-peer, encrypted, instantaneous sync) for live file sync and GitHub as the authoritative backup/history.

What I added
- `.stignore.example`: recommended Syncthing ignore patterns (in this folder). Copy into your share root or paste into Syncthing "Ignore Patterns".
- `install_syncthing_windows.ps1`: PowerShell helper to install Syncthing (via winget/choco) and launch it.
- `install_syncthing_linux.sh`: Linux install helper (apt/pacman fallback).
- `auto_git_push.sh`: optional auto-commit+push helper (use with caution — may create noisy commits).

Quick decision checklist
1. Pick the folder to sync (recommended):
   - `C:\Users\<you>\Desktop\Master VS CODE PROJECTS` (example). Use the same absolute path on each device if possible.
2. Install Syncthing on every device that will participate.
3. Add the folder as a Syncthing share on one device and share it with the other devices (by Device ID).
4. Add recommended ignores (.stignore) so you do not sync virtualenvs, build artifacts or `.git`.
5. Keep using Git for commits + pushes to GitHub (the repository remains the canonical backup).

Important: ignore rules
- Do NOT sync `.git` directories. Do NOT sync virtual environments or large dependency folders (e.g., `.venv`, `node_modules`).
- Use the provided `.stignore.example` as the basis for your Syncthing ignore list.

Syncthing install (one-liners)
- Windows (winget):
  winget install -e --id Syncthing.Syncthing
  (or with Chocolatey: `choco install syncthing`)

- macOS (Homebrew):
  brew install syncthing

- Debian/Ubuntu:
  sudo apt update && sudo apt install syncthing

- Arch/Manjaro:
  sudo pacman -S syncthing

First-time Syncthing setup (GUI)
1. Start Syncthing on each machine; open the web UI at `http://127.0.0.1:8384`.
2. On device A: Actions → Show ID → copy the Device ID.
3. On device B: Actions → Add Remote Device → paste device A's ID, give a name, and save.
4. On device A: You will be prompted to share folders with device B — accept the share.
5. Create a folder share pointing to your workspace folder path. In the folder settings paste the contents of `.stignore.example` into "Ignore Patterns" and enable simple file versioning (File Versioning → Simple File Versioning) to keep conflict backups.

Notes on ignores
- Put `.stignore` at the root of the shared folder (Syncthing will respect it) or paste the patterns into the web UI Ignore Patterns for the folder.
- Example ignore patterns are in `.stignore.example` in this `repo_admin/sync_setup` folder.

Auto-backup (GitHub)
- Continue using normal Git workflows (`git add`, `git commit`, `git push`). Syncthing will sync working tree files but the Git history is maintained by commits.
- Optional: `auto_git_push.sh` (provided) will auto-commit and push any repo changes — use only if you accept noisy commits and potential merge conflicts.

VS Code settings and extensions
- Use VS Code Settings Sync to keep your editor configuration & extensions in sync between machines (Settings Sync uses Microsoft/GitHub account sign-in).

Conflict handling
- Syncthing will create conflict files when the same file is edited on two machines simultaneously. Resolve manually and commit resolved state to Git.

Security and performance tips
- Enable versioning (Simple File Versioning) for important shares.
- Exclude large datasets or binary caches that don't need real-time sync.
- If you have intermittent connectivity, Syncthing will reconcile when devices reconnect.

If you want, I can:
- Generate a device-config template (requires the device IDs of the other machines), or
- Help you install Syncthing on a specific machine now (I can provide and run install commands on the current machine), or
- Set up a safe auto-commit workflow tuned to your repo.

Files added in `repo_admin/sync_setup`
- `.stignore.example`
- `install_syncthing_windows.ps1`
- `install_syncthing_linux.sh`
- `auto_git_push.sh`

