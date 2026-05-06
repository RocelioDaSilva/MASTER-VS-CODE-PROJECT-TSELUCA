param(
    [string]$DesktopDeviceID = "XVMNNZF-KDKG77E-AANW7M7-NXGJLW6-BGJN7BU-2SRELTE-3TEERVU-MDLZJAG",
    [string]$FolderID = "vz3f9-qvauy",
    [string]$FolderPath = "",
    [string]$FolderLabel = "MIT-SCIENCE-PAPER"
)

Write-Host "=== Syncthing Laptop Setup & Pairing Script ===" -ForegroundColor Cyan
Write-Host ""

# Get workspace folder if not provided
if (-not $FolderPath -or $FolderPath -eq "") {
    $FolderPath = Read-Host "Enter the full path to your workspace folder (Master VS CODE PROJECTS folder)"
}

if (-not (Test-Path $FolderPath)) {
    Write-Host "ERROR: Path does not exist: $FolderPath" -ForegroundColor Red
    exit 1
}

Write-Host "Workspace: $FolderPath" -ForegroundColor Green

# Syncthing config path
$SyncthingAppDataPath = "$env:APPDATA\Syncthing"
$SyncthingConfigPath = "$SyncthingAppDataPath\config.xml"
$SyncthingExePath = "$SyncthingAppDataPath\syncthing.exe"

Write-Host ""
Write-Host "Step 1: Install Syncthing" -ForegroundColor Yellow

if (-not (Test-Path $SyncthingExePath)) {
    Write-Host "Installing Syncthing..."
    $apiUrl = 'https://api.github.com/repos/syncthing/syncthing/releases?per_page=1'
    try {
        $releases = Invoke-RestMethod -Uri $apiUrl
        $latest = $releases[0]
        $asset = $latest.assets | Where-Object { $_.name -match 'windows-amd64' -and $_.name -match '\.zip$' } | Select-Object -First 1
        
        if ($asset) {
            $url = $asset.browser_download_url
            $filename = $asset.name
            $tempZip = "$env:TEMP\$filename"
            
            Write-Host "Downloading: $filename"
            Invoke-WebRequest -Uri $url -OutFile $tempZip -UseBasicParsing
            
            if (Test-Path $tempZip) {
                if (!(Test-Path $SyncthingAppDataPath)) {
                    New-Item -ItemType Directory -Path $SyncthingAppDataPath -Force | Out-Null
                }
                Write-Host "Extracting..."
                Expand-Archive -Path $tempZip -DestinationPath $SyncthingAppDataPath -Force
                
                # Move syncthing.exe to root
                $extractedDir = Get-ChildItem $SyncthingAppDataPath -Directory | Where-Object { $_.Name -match "syncthing-windows" } | Select-Object -First 1
                if ($extractedDir) {
                    $exePath = Join-Path $extractedDir.FullName "syncthing.exe"
                    if (Test-Path $exePath) {
                        Move-Item -Path $exePath -Destination "$SyncthingAppDataPath\syncthing.exe" -Force
                        Remove-Item $extractedDir.FullName -Recurse -Force
                    }
                }
                
                Remove-Item $tempZip
                Write-Host "✓ Syncthing installed" -ForegroundColor Green
            }
        }
    } catch {
        Write-Host "ERROR downloading Syncthing: $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✓ Syncthing already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Start Syncthing" -ForegroundColor Yellow

# Kill any existing Syncthing process
Get-Process syncthing -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1

# Start Syncthing
Start-Process $SyncthingExePath -WindowStyle Hidden
Write-Host "Starting Syncthing daemon..."
Start-Sleep -Seconds 5

Write-Host "✓ Syncthing started" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Wait for config creation" -ForegroundColor Yellow

$maxWait = 30
$waited = 0
while ($waited -lt $maxWait -and -not (Test-Path $SyncthingConfigPath)) {
    Write-Host "Waiting... ($waited seconds)"
    Start-Sleep -Seconds 2
    $waited += 2
}

if (-not (Test-Path $SyncthingConfigPath)) {
    Write-Host "ERROR: Syncthing config not created" -ForegroundColor Red
    Write-Host "Please open http://127.0.0.1:8384 manually to complete setup"
    exit 1
}

Write-Host "✓ Config file ready" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Extract laptop Device ID" -ForegroundColor Yellow

try {
    $xml = [xml](Get-Content $SyncthingConfigPath)
    $laptopDeviceID = $xml.SelectSingleNode('//device').GetAttribute('id')
    Write-Host "Laptop Device ID: $laptopDeviceID" -ForegroundColor Green
} catch {
    Write-Host "ERROR reading config: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 5: Configure folder (via API)" -ForegroundColor Yellow

# Get API key from config
$apiKeyNode = $xml.SelectSingleNode('//gui/apikey')
if ($apiKeyNode) {
    $apiKey = $apiKeyNode.InnerText
    Write-Host "API Key found" -ForegroundColor Green
    
    # Get current folders
    $foldersResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8384/rest/config/folders" `
        -Headers @{"X-API-Key" = $apiKey} -ErrorAction SilentlyContinue
    
    $folderExists = $foldersResponse | Where-Object { $_.id -eq $FolderID }
    
    if ($folderExists) {
        Write-Host "✓ Folder already configured on laptop" -ForegroundColor Green
    } else {
        Write-Host "Adding folder via API..."
        $folderConfig = @{
            id = $FolderID
            label = $FolderLabel
            path = $FolderPath
            type = "sendreceive"
            ignorePerms = $false
            autoNormalize = $true
            rescanIntervalS = 3600
            devices = @(
                @{
                    deviceID = $laptopDeviceID
                    introducedBy = ""
                }
            )
            minDiskFree = @{
                value = 1
                unit = "%"
            }
        }
        
        try {
            $response = Invoke-RestMethod -Uri "http://127.0.0.1:8384/rest/config/folders" `
                -Headers @{"X-API-Key" = $apiKey} `
                -Method POST `
                -ContentType "application/json" `
                -Body ($folderConfig | ConvertTo-Json -Depth 10)
            Write-Host "✓ Folder added" -ForegroundColor Green
        } catch {
            Write-Host "WARNING: Could not add folder via API: $_" -ForegroundColor Yellow
            Write-Host "You may need to add it manually via web UI" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "WARNING: Could not find API key. Configure folder manually via web UI" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Laptop Device ID: $laptopDeviceID" -ForegroundColor Green
Write-Host "Web UI: http://127.0.0.1:8384" -ForegroundColor Cyan
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. On DESKTOP (NEXUS): Go to Devices → Add Remote Device"
Write-Host "2. Enter Laptop Device ID: $laptopDeviceID"
Write-Host "3. On LAPTOP: Accept the connection from DESKTOP"
Write-Host "4. On DESKTOP: Edit MIT-SCIENCE-PAPER folder → Sharing → Select LAPTOP device"
Write-Host "5. Files will start syncing automatically"
Write-Host ""
Write-Host "Save this Device ID to share with other devices!"
