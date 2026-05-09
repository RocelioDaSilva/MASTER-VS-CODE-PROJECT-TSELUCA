@echo off
echo Starting Auto-Sync Watcher...
echo Press Ctrl+C in the PowerShell window to stop syncing.
echo.

powershell -NoExit -ExecutionPolicy Bypass -Command "& { Set-Location 'c:\Users\PCGAME\Desktop\MASTER VS CODE PROJECT TSELUCA'; & '.\scripts\auto_sync_watcher.ps1' -DebounceSeconds 30 -Remote origin -Branch main }"
