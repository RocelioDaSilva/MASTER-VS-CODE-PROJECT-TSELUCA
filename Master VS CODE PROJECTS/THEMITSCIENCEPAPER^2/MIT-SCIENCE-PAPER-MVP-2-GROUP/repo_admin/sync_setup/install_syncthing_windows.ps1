# Install Syncthing on Windows (winget preferred, fallback to Chocolatey)
# Run as Administrator if installing system-wide.

if (Get-Command winget -ErrorAction SilentlyContinue) {
  Write-Host "Installing Syncthing with winget..."
  winget install -e --id Syncthing.Syncthing
} elseif (Get-Command choco -ErrorAction SilentlyContinue) {
  Write-Host "Installing Syncthing with Chocolatey..."
  choco install syncthing -y
} else {
  Write-Host "Neither winget nor choco found. Please install Syncthing from https://syncthing.net/downloads/"
}

# Start Syncthing (current user)
try {
  Start-Process syncthing
  Write-Host "Syncthing started. Open http://127.0.0.1:8384 in your browser."
} catch {
  Write-Host "Failed to start syncthing automatically. Launch it from Start Menu or run 'syncthing' in PowerShell." 
}

Write-Host "When Syncthing is running: open the web UI (http://127.0.0.1:8384), add devices, and add a folder share pointing to your workspace root. Use the .stignore.example patterns."