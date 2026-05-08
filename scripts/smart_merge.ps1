param(
    [string]$From = "origin/main",
    [string]$ConflictRoot = ".merge_conflicts",
    [switch]$FetchFirst
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true)][string[]]$Args,
        [switch]$AllowFailure
    )

    & git @Args
    $exitCode = $LASTEXITCODE

    if (-not $AllowFailure -and $exitCode -ne 0) {
        throw "git $($Args -join ' ') failed with exit code $exitCode"
    }

    return $exitCode
}

function Test-GitRepo {
    $null = Invoke-Git -Args @("rev-parse", "--is-inside-work-tree") -AllowFailure
    if ($LASTEXITCODE -ne 0) {
        throw "This folder is not a git repository."
    }
}

function Export-StageFile {
    param(
        [int]$Stage,
        [string]$Path,
        [string]$Destination
    )

    # checkout-index --temp writes a temporary file path we can copy without text encoding corruption.
    $line = (& git checkout-index "--stage=$Stage" --temp -- "$Path" 2>$null | Select-Object -First 1)
    if (-not $line) {
        return $false
    }

    $parts = $line -split "`t", 2
    if ($parts.Count -lt 1) {
        return $false
    }

    $tempPath = $parts[0].Trim()
    if (-not (Test-Path -LiteralPath $tempPath)) {
        return $false
    }

    Copy-Item -LiteralPath $tempPath -Destination $Destination -Force
    Remove-Item -LiteralPath $tempPath -Force
    return $true
}

function Get-SafeFolderName {
    param([string]$RelativePath)

    return ($RelativePath -replace '[\\/:*?""<>|]', "__")
}

Test-GitRepo

if ($FetchFirst) {
    Write-Host "Fetching remotes..."
    Invoke-Git -Args @("fetch", "--all", "--prune") | Out-Null
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$archiveDir = Join-Path -Path $ConflictRoot -ChildPath $timestamp

$divergenceRaw = (& git rev-list --left-right --count "HEAD...$From" 2>$null | Select-Object -First 1)
if (-not $divergenceRaw) {
    throw "Could not compare HEAD with '$From'. Make sure the ref exists (try -FetchFirst)."
}

$divergenceParts = $divergenceRaw.Trim() -split "\s+"
if ($divergenceParts.Count -lt 2) {
    throw "Unexpected rev-list output while comparing with '$From': $divergenceRaw"
}

$incomingOnlyCount = [int]$divergenceParts[1]
if ($incomingOnlyCount -eq 0) {
    Write-Host "Already up to date with '$From'."
    exit 0
}

Write-Host "Merging from '$From'..."
$mergeExit = Invoke-Git -Args @("merge", "--no-commit", "--no-ff", "$From") -AllowFailure

$conflictedPaths = @(
    (& git diff --name-only --diff-filter=U) |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -ne "" }
)

if ($conflictedPaths.Count -eq 0) {
    if ($mergeExit -ne 0) {
        throw "Merge failed without unresolved file conflicts. Check git output and run git merge --abort if needed."
    }

    Write-Host "Merge completed with no conflicts."
    exit 0
}

New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null

$manifest = New-Object System.Collections.Generic.List[object]

foreach ($path in $conflictedPaths) {
    $safeName = Get-SafeFolderName -RelativePath $path
    $targetDir = Join-Path -Path $archiveDir -ChildPath $safeName
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null

    $workingSnapshot = $false
    if (Test-Path -LiteralPath $path) {
        Copy-Item -LiteralPath $path -Destination (Join-Path -Path $targetDir -ChildPath "working") -Force
        $workingSnapshot = $true
    }

    $baseSnapshot = Export-StageFile -Stage 1 -Path $path -Destination (Join-Path -Path $targetDir -ChildPath "base")
    $oursSnapshot = Export-StageFile -Stage 2 -Path $path -Destination (Join-Path -Path $targetDir -ChildPath "ours")
    $theirsSnapshot = Export-StageFile -Stage 3 -Path $path -Destination (Join-Path -Path $targetDir -ChildPath "theirs")

    $manifest.Add([pscustomobject]@{
        path = $path
        folder = $targetDir
        snapshots = [pscustomobject]@{
            working = $workingSnapshot
            base = $baseSnapshot
            ours = $oursSnapshot
            theirs = $theirsSnapshot
        }
    })
}

$manifestPath = Join-Path -Path $archiveDir -ChildPath "manifest.json"
$manifest | ConvertTo-Json -Depth 6 | Set-Content -Path $manifestPath -Encoding UTF8

Write-Host ""
Write-Host "Conflict snapshots saved to: $archiveDir"
Write-Host "Files with conflicts: $($conflictedPaths.Count)"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Resolve conflicts in your working tree files."
Write-Host "2. Use snapshots in '$archiveDir' if you need base/ours/theirs references."
Write-Host "3. Run: git add <resolved files>"
Write-Host "4. Run: git commit"
Write-Host ""
Write-Host "To cancel this merge, run: git merge --abort"

exit 1
