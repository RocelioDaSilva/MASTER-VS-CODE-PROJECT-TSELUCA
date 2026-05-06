<#
Create a GitHub Gist containing the prompts files in tools/image_pipeline.
Requirements:
 - Set environment variable GITHUB_TOKEN to a personal access token with "gist" scope.
Usage:
  $env:GITHUB_TOKEN = "ghp_..."  # or set permanently in Windows
  ./gist_upload.ps1
#>
param(
  [string]$GITHUB_TOKEN = $env:GITHUB_TOKEN,
  [string]$Description = "Chain Weapon Story - header prompts and Claude prompt",
  [bool]$Public = $false
)

if (-not $GITHUB_TOKEN) {
  Write-Error "GITHUB_TOKEN environment variable is not set. Create a personal access token with 'gist' scope and set $env:GITHUB_TOKEN before running."; exit 1
}

$promptsPath = "tools/image_pipeline/prompts_48.txt"
$claudePath = "tools/image_pipeline/claude_opus_prompt.txt"

if (-not (Test-Path $promptsPath)) { Write-Error "Missing $promptsPath"; exit 1 }
if (-not (Test-Path $claudePath)) { Write-Error "Missing $claudePath"; exit 1 }

$prompts = Get-Content -Raw -Path $promptsPath
$claude = Get-Content -Raw -Path $claudePath

$payload = @{ description = $Description; public = $Public; files = @{ "prompts_48.txt" = @{ content = $prompts }; "claude_opus_prompt.txt" = @{ content = $claude } } } | ConvertTo-Json -Depth 10

$headers = @{ Authorization = "token $GITHUB_TOKEN"; Accept = "application/vnd.github+json" }

try {
  $resp = Invoke-RestMethod -Uri "https://api.github.com/gists" -Method Post -Headers $headers -Body $payload -ContentType "application/json"
  Write-Host "Gist created: $($resp.html_url)" -ForegroundColor Green
} catch {
  Write-Error "Failed to create gist: $_"
  exit 1
}
