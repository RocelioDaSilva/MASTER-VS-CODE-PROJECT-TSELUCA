@echo off
echo Starting Auto-Sync Watcher...
echo Press Ctrl+C in the PowerShell window to stop syncing.
echo.

set "SCRIPT_DIR=%~dp0"
powershell -NoExit -ExecutionPolicy Bypass -Command "& { Set-Location '%SCRIPT_DIR%'; & '.\scripts\auto_sync_watcher.ps1' -DebounceSeconds 30 -Remote origin -Branch main }"
