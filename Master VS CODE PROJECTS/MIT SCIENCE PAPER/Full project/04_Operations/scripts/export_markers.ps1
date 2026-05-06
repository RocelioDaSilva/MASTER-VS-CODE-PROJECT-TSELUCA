<#
Run from workspace root to export all TODO/TBD/DRAFT/FIXME/INCOMPLETE matches to CSV.
Usage: Open PowerShell in the repo root and run:
  .\scripts\export_markers.ps1 -OutPath .\docs\technical_debt_matches_full.csv
#>

param(
    [string]$OutPath = "docs/technical_debt_matches_full.csv",
    [string]$Root = "."
)

$pattern = 'TODO|TBD|DRAFT|FIXME|INCOMPLETE'

Write-Host "Searching for markers under '$Root'..."

$results = Select-String -Path "$Root\**\*.*" -Pattern $pattern | ForEach-Object {
    [PSCustomObject]@{
        Path = $_.Path
        LineNumber = $_.LineNumber
        Match = $_.Line.Trim()
    }
}

if (-not (Test-Path (Split-Path $OutPath))) {
    New-Item -ItemType Directory -Path (Split-Path $OutPath) -Force | Out-Null
}

$results | Export-Csv -Path $OutPath -NoTypeInformation -Encoding UTF8
Write-Host "Exported" ($results.Count) "matches to" $OutPath
