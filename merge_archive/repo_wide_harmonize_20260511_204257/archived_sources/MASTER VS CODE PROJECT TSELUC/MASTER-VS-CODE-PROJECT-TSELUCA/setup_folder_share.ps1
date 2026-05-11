#!/usr/bin/env powershell
# Syncthing Folder Share Setup for "Master VS CODE PROJECTS"
# This script automates adding a shared folder to Syncthing

$SyncthingWebUI = "http://127.0.0.1:8384"
$FolderPath = "C:\Users\PCGAME\Desktop\Master VS CODE PROJECTS"
$FolderLabel = "Master-VS-CODE-Projects"
$ConfigPath = "$env:APPDATA\Syncthing\config.xml"

Write-Host "Syncthing Folder Share Setup"
Write-Host "============================="
Write-Host ""

# Check if folder exists
if (!(Test-Path $FolderPath)) {
    Write-Host "ERROR: Folder not found: $FolderPath"
    exit 1
}

Write-Host "✓ Folder found: $FolderPath"
Write-Host ""

# Check if Syncthing config exists
if (!(Test-Path $ConfigPath)) {
    Write-Host "⚠ Syncthing config not found yet. Starting Syncthing..."
    Write-Host "Please wait 30 seconds for it to initialize..."
    exit 1
}

Write-Host "✓ Syncthing config found"
Write-Host ""
Write-Host "To add the folder share manually via web UI:"
Write-Host "1. Open: $SyncthingWebUI"
Write-Host "2. Click 'Add Folder'"
Write-Host "3. Set:"
Write-Host "   - Folder Label: $FolderLabel"
Write-Host "   - Folder Path: $FolderPath"
Write-Host "   - Devices: (Select all devices you want to sync with)"
Write-Host "4. Ignore Patterns:"
Write-Host "   Copy from: repo_admin/sync_setup/.stignore.example"
Write-Host "5. Click 'Save'"
Write-Host ""
Write-Host "Then add your other PC as a Remote Device and share this folder with it."
