Param(
    [Parameter(Mandatory=$false)]
    [string[]]$RootPaths,

    [string]$ReportPath = "$PSScriptRoot\harmonize_duplicates_report.csv",

    [switch]$DryRun,

    [ValidateSet("Report","Move","Delete","Link")]
    [string]$Action = "Report",

    [string]$DuplicatesFolder = "$PSScriptRoot\harmonize_duplicates",

    [switch]$KeepNewest
)

<#
Simple duplicate finder and dry-run reporter.
Usage examples:
  - Dry run report across the two project roots (default):
    powershell -NoProfile -ExecutionPolicy Bypass -File "./harmonize_find_dupes.ps1" -DryRun

  - Specify roots and output path:
    powershell -NoProfile -ExecutionPolicy Bypass -File "./harmonize_find_dupes.ps1" -RootPaths "C:\Path\A","C:\Path\B" -ReportPath "C:\temp\dupes.csv" -DryRun

Notes:
 - Default behavior: only reports duplicates; does not modify files.
 - To actually act on duplicates set `-Action Move|Delete|Link` and **do not** use `-DryRun`.
 - The script groups by file size first, then hashes only same-size groups for performance.
#>

function Resolve-DefaultRoots {
    param($ScriptRoot)
    $c1 = Join-Path -Path $ScriptRoot -ChildPath "MASTER VS CODE PROJECT"
    $c2 = Join-Path -Path $ScriptRoot -ChildPath "Master VS CODE PROJECTS"
    $r = @()
    if (Test-Path $c1) { $r += $c1 }
    if (Test-Path $c2) { $r += $c2 }
    return $r
}

if (-not $RootPaths -or $RootPaths.Count -eq 0) {
    $RootPaths = Resolve-DefaultRoots -ScriptRoot $PSScriptRoot
    if ($RootPaths.Count -eq 0) {
        Write-Error "No root paths supplied and default project folders not found under $PSScriptRoot"
        exit 2
    }
}

# If user passed a single comma-separated argument (common from CLI), split it into an array
if ($RootPaths.Count -eq 1 -and $RootPaths[0] -like '*,*') {
    $RootPaths = ($RootPaths -split ',') | ForEach-Object { $_.Trim() }
}

Write-Host "Starting duplicate scan..."
Write-Host "Roots:" -NoNewline; $RootPaths | ForEach-Object { Write-Host "`n - $_" -NoNewline }
Write-Host "`n"

# Enumerate files
$allFiles = @()
foreach ($root in $RootPaths) {
    Write-Host "Enumerating files under: $root"
    try {
        $items = Get-ChildItem -Path $root -File -Recurse -ErrorAction SilentlyContinue -Force
    } catch {
        Write-Warning ("Failed to enumerate {0}: {1}" -f $root, $_)
        continue
    }
    foreach ($it in $items) {
        if ($it.Length -eq 0) { continue }
        if ($it.Extension -ieq '.lnk') { continue }
        $allFiles += [PSCustomObject]@{
            Path = $it.FullName
            Length = $it.Length
            LastWriteTime = $it.LastWriteTime
            Root = $root
        }
    }
}

$total = $allFiles.Count
Write-Host "Files considered (non-zero, filtered): $total"
if ($total -eq 0) { Write-Host "No files to scan."; exit 0 }

# Group by size to reduce hashing
$sizeGroups = $allFiles | Group-Object -Property Length | Where-Object { $_.Count -gt 1 }
Write-Host "Size groups with more than one file: $($sizeGroups.Count)"

$hashTable = @{}
$progressCount = 0
$toHashCount = ($sizeGroups | ForEach-Object { $_.Group.Count }) | Measure-Object -Sum | Select-Object -ExpandProperty Sum
if (-not $toHashCount) { $toHashCount = 0 }
Write-Host "Files to hash (only in duplicate-size groups): $toHashCount"

foreach ($g in $sizeGroups) {
    foreach ($item in $g.Group) {
        $progressCount++
        if (($progressCount % 100) -eq 0) {
            Write-Progress -Activity "Hashing files" -Status "$progressCount / $toHashCount" -PercentComplete ([int](($progressCount/$toHashCount)*100))
        }
        try {
            $h = (Get-FileHash -Algorithm SHA256 -Path $item.Path -ErrorAction Stop).Hash
        } catch {
            Write-Warning "Hash failed for $($item.Path): $_"
            continue
        }
        if (-not $hashTable.ContainsKey($h)) { $hashTable[$h] = @() }
        $hashTable[$h] += [PSCustomObject]@{
            Path = $item.Path
            Length = $item.Length
            LastWriteTime = $item.LastWriteTime
            Root = $item.Root
        }
    }
}

# Identify duplicates (same hash, >1 file)
$duplicateGroups = $hashTable.GetEnumerator() | Where-Object { $_.Value.Count -gt 1 }
Write-Host "Duplicate content groups found: $($duplicateGroups.Count)"

$reportRows = @()

# Build a map for quick root priority lookup
$rootPriority = @{}
for ($i=0; $i -lt $RootPaths.Count; $i++) { $rootPriority[$RootPaths[$i].ToLower()] = $i }

foreach ($grp in $duplicateGroups) {
    $hash = $grp.Key
    $files = $grp.Value

    foreach ($f in $files) {
        $f | Add-Member -NotePropertyName RootIndex -NotePropertyValue (
            if ($rootPriority.ContainsKey($f.Root.ToLower())) { $rootPriority[$f.Root.ToLower()] } else { [int]::MaxValue }
        ) -Force
    }

    if ($KeepNewest) {
        $keep = $files | Sort-Object -Property LastWriteTime -Descending | Select-Object -First 1
    } else {
        $keep = $files | Sort-Object -Property RootIndex, @{Expression={$_.LastWriteTime};Descending=$true} | Select-Object -First 1
    }

    foreach ($f in $files) {
        $reportRows += [PSCustomObject]@{
            Hash = $hash
            Size = $f.Length
            Path = $f.Path
            LastWriteTime = $f.LastWriteTime
            IsKeep = ($f.Path -eq $keep.Path)
            SuggestedAction = if ($f.Path -eq $keep.Path) { 'Keep' } else { 'Duplicate' }
        }
    }
}

# Export CSV report
try {
    $reportRows | Sort-Object Hash, Path | Export-Csv -Path $ReportPath -NoTypeInformation -Encoding UTF8
    Write-Host "Report written to: $ReportPath"
} catch {
    Write-Warning ("Failed to write report to {0}: {1}" -f $ReportPath, $_)
}

# Summary
$totalDupFiles = ($reportRows | Where-Object { $_.SuggestedAction -eq 'Duplicate' }).Count
$totalGroups = $duplicateGroups.Count
Write-Host "Duplicate groups: $totalGroups -- Duplicate files: $totalDupFiles"

if (-not $DryRun -and $Action -ne 'Report') {
    Write-Host "Performing action: $Action"
    if ($Action -eq 'Move') {
        if (-not (Test-Path $DuplicatesFolder)) { New-Item -Path $DuplicatesFolder -ItemType Directory | Out-Null }
    }

    foreach ($row in $reportRows | Where-Object { $_.SuggestedAction -eq 'Duplicate' }) {
        $dupPath = $row.Path
        $groupHash = $row.Hash
        $keepPath = ($reportRows | Where-Object { $_.Hash -eq $groupHash -and $_.IsKeep })[0].Path

        try {
            switch ($Action) {
                'Delete' {
                    Remove-Item -LiteralPath $dupPath -Force -ErrorAction Stop
                    Write-Host "Deleted: $dupPath"
                }
                'Move' {
                    $relative = [IO.Path]::GetRelativePath((Split-Path -Path $dupPath -Parent), $dupPath) # may be same file
                    # Build simple unique name under duplicates folder
                    $dest = Join-Path -Path $DuplicatesFolder -ChildPath ([IO.Path]::GetFileName($dupPath))
                    $count = 0
                    while (Test-Path $dest) { $count++; $dest = Join-Path -Path $DuplicatesFolder -ChildPath ("$($count)_$([IO.Path]::GetFileName($dupPath))") }
                    Move-Item -LiteralPath $dupPath -Destination $dest -Force
                    Write-Host "Moved: $dupPath -> $dest"
                }
                'Link' {
                    # Replace duplicate with hardlink pointing to keepPath (must be same volume)
                    $drv1 = ([IO.Path]::GetPathRoot($dupPath)).ToLower()
                    $drv2 = ([IO.Path]::GetPathRoot($keepPath)).ToLower()
                    if ($drv1 -ne $drv2) { Write-Warning "Cannot create hardlink across volumes: $dupPath -> $keepPath"; continue }
                    # Remove duplicate then create hardlink
                    Remove-Item -LiteralPath $dupPath -Force -ErrorAction Stop
                    New-Item -ItemType HardLink -Path $dupPath -Target $keepPath -ErrorAction Stop | Out-Null
                    Write-Host "Replaced with hardlink: $dupPath -> $keepPath"
                }
            }
        } catch {
            Write-Warning ("Action failed for {0}: {1}" -f $dupPath, $_)
        }
    }
    Write-Host "Action complete."
} else {
    Write-Host "Dry-run mode: no files were modified. To act on duplicates, re-run without -DryRun and set -Action Move|Delete|Link."
}
