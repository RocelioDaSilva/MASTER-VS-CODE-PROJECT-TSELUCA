param(
    [string]$WatchPath = (Split-Path -Parent $PSScriptRoot),
    [int]$DebounceSeconds = 30,
    [string]$Remote = "origin",
    [string]$Branch = "main",
    [switch]$PullOnly,
    [switch]$Verbose
)

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# AUTO SYNC WATCHER
# Watches for file changes and auto-commits + pushes.
# Runs git pull before each push to stay in sync.
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts][$Level] $Message"
    Write-Host $line
    Add-Content -LiteralPath (Join-Path $WatchPath ".sync_watcher.log") -Value $line
}

function Get-GitStatus {
    $result = & git -C $WatchPath status --porcelain 2>&1
    return @($result | Where-Object { $_ -ne "" })
}

function Invoke-GitPull {
    Write-Log "Pulling from $Remote/$Branch..."
    $output = & git -C $WatchPath pull --rebase $Remote $Branch 2>&1
    $exitCode = $LASTEXITCODE
    if ($exitCode -eq 0) {
        Write-Log "Pull OK: $($output | Select-Object -Last 1)"
    } else {
        Write-Log "Pull failed (exit $exitCode): $($output | Select-Object -Last 3 | Out-String)" "WARN"
    }
    return $exitCode
}

function Invoke-GitCommitPush {
    $changes = Get-GitStatus
    if ($changes.Count -eq 0) {
        Write-Log "Nothing to commit."
        return
    }

    # Exclude files too large for GitHub (>100MB) and temp sync artifacts
    $toAdd = @()
    foreach ($statusLine in $changes) {
        $filePath = $statusLine.Substring(3).Trim().Trim('"')
        $fullPath = Join-Path $WatchPath $filePath
        if (Test-Path -LiteralPath $fullPath) {
            $size = (Get-Item -LiteralPath $fullPath -Force).Length
            if ($size -ge 100MB) {
                Write-Log "Skipping large file ($([math]::Round($size/1MB,1)) MB): $filePath" "WARN"
                continue
            }
        }
        $toAdd += $filePath
    }

    if ($toAdd.Count -eq 0) {
        Write-Log "All changed files are too large to commit."
        return
    }

    # Pull first to avoid push rejection
    Invoke-GitPull | Out-Null

    # Stage changed (non-large) files
    & git -C $WatchPath add --all 2>&1 | Out-Null
    # Unstage oversized files
    $bigFiles = & git -C $WatchPath ls-files --others --exclude-standard 2>&1
    foreach ($statusLine in $changes) {
        $filePath = $statusLine.Substring(3).Trim().Trim('"')
        $fullPath = Join-Path $WatchPath $filePath
        if (Test-Path -LiteralPath $fullPath) {
            $size = (Get-Item -LiteralPath $fullPath -Force).Length
            if ($size -ge 100MB) {
                & git -C $WatchPath reset HEAD -- "$filePath" 2>&1 | Out-Null
            }
        }
    }

    $msg = "auto-sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm') [$($toAdd.Count) change(s)]"
    $commitOut = & git -C $WatchPath commit -m $msg 2>&1
    $commitExit = $LASTEXITCODE

    if ($commitExit -ne 0) {
        Write-Log "Commit failed: $($commitOut | Out-String)" "ERROR"
        return
    }
    Write-Log "Committed: $msg"

    $pushOut = & git -C $WatchPath push $Remote $Branch 2>&1
    $pushExit = $LASTEXITCODE
    if ($pushExit -eq 0) {
        Write-Log "Pushed to $Remote/$Branch OK"
    } else {
        Write-Log "Push failed: $($pushOut | Out-String)" "ERROR"
    }
}

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Setup FileSystemWatcher
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

Write-Log "Starting auto-sync watcher on: $WatchPath"
Write-Log "Debounce: ${DebounceSeconds}s | Remote: $Remote/$Branch | PullOnly: $PullOnly"
Write-Log "Press Ctrl+C to stop."

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $WatchPath
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true
$watcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite `
    -bor [System.IO.NotifyFilters]::FileName `
    -bor [System.IO.NotifyFilters]::DirectoryName

# Paths to ignore in the watcher (git internals, venv, logs)
$ignorePaths = @(".git", ".venv", ".sync_watcher.log", "*.log", "*.tmp")

$lastTrigger = [datetime]::MinValue
$script:lastPull = [datetime]::MinValue
$pending = $false

$action = {
    $path = $Event.SourceEventArgs.FullPath
    $name = $Event.SourceEventArgs.Name

    # Skip git internals and venv
    foreach ($ig in $ignorePaths) {
        if ($name -like $ig -or $path -like "*\.git\*" -or $path -like "*\.venv\*") {
            return
        }
    }

    $script:lastTrigger = Get-Date
    $script:pending = $true
}

$jobs = @(
    Register-ObjectEvent $watcher "Changed" -Action $action
    Register-ObjectEvent $watcher "Created" -Action $action
    Register-ObjectEvent $watcher "Deleted" -Action $action
    Register-ObjectEvent $watcher "Renamed" -Action $action
)

# Pull once immediately on startup to make sure we're up to date
Invoke-GitPull | Out-Null

try {
    while ($true) {
        Start-Sleep -Seconds 5

        # Periodic pull every 5 minutes regardless of local changes
        if ((Get-Date) -gt $script:lastPull.AddMinutes(5)) {
            Invoke-GitPull | Out-Null
            $script:lastPull = Get-Date
        }

        if ($PullOnly) { continue }

        if ($script:pending) {
            $elapsed = ((Get-Date) - $script:lastTrigger).TotalSeconds
            if ($elapsed -ge $DebounceSeconds) {
                $script:pending = $false
                Write-Log "Change detected - debounce passed, syncing..."
                Invoke-GitCommitPush
            }
        }
    }
}
finally {
    $jobs | ForEach-Object { Unregister-Event -SourceIdentifier $_.Name; Remove-Job $_ -Force }
    $watcher.EnableRaisingEvents = $false
    $watcher.Dispose()
    Write-Log "Watcher stopped."
}

