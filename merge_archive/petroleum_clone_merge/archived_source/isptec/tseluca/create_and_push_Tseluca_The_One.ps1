param(
    [Parameter(Mandatory=$true)][string]$Token,
    [string]$RepoName = "Tseluca_The_One",
    [ValidateSet("public","private")][string]$Visibility = "private",
    [switch]$NoRenameOrigin
)

Set-StrictMode -Version Latest
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git not found in PATH"
    exit 1
}

$cwd = Get-Location

$body = @{
    name = $RepoName
    description = "Repository created from local Tseluca workspace"
    private = ($Visibility -eq "private")
} | ConvertTo-Json

$headers = @{
    Authorization = "token $Token"
    'User-Agent' = 'Tseluca-Script'
}

try {
    $resp = Invoke-RestMethod -Uri 'https://api.github.com/user/repos' -Method Post -Headers $headers -Body $body
} catch {
    Write-Error "Failed to create GitHub repo: $_"
    exit 1
}

$cloneUrl = $resp.clone_url
$fullName = $resp.full_name

Write-Host "Created repo $fullName"
Write-Host "Clone URL: $cloneUrl"

$existingRemotes = git remote
if ($existingRemotes -contains 'origin') {
    if (-not $NoRenameOrigin) {
        git remote rename origin upstream
        Write-Host "Renamed 'origin' -> 'upstream'"
    } else {
        Write-Host "'origin' exists and will not be renamed because -NoRenameOrigin was supplied."
    }
}

if ((git remote) -contains 'origin') {
    git remote remove origin
}

git remote add origin $cloneUrl
Write-Host "Added remote origin -> $cloneUrl"

Write-Host "Pushing branches..."
git -c http.extraheader="AUTHORIZATION: bearer $Token" push -u origin --all
Write-Host "Pushing tags..."
git -c http.extraheader="AUTHORIZATION: bearer $Token" push -u origin --tags

Write-Host "Repository pushed to https://github.com/$fullName"
