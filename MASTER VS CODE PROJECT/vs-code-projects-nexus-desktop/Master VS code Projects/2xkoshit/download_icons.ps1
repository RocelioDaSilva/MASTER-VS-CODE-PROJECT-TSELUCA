# Download 2XKO Button Notation SVG Icons from Official CDN

$output = "images\notation"
if (!(Test-Path $output)) { New-Item -ItemType Directory $output | Out-Null }

$base = "https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest"
$icons = "L","M","H","S1","S2","down","forward","back","up","plus"

Write-Host "Downloading button icons..." -ForegroundColor Cyan

foreach ($icon in $icons) {
    $url = "$base/$icon.svg"
    $file = "$output\$icon.svg"
    try {
        Invoke-WebRequest -Uri $url -OutFile $file -ErrorAction Stop
        Write-Host "  $icon.svg OK" -ForegroundColor Green
    } catch {
        Write-Host "  $icon.svg FAILED: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Download complete!" -ForegroundColor Green
Write-Host "SVG icons saved to: $(Resolve-Path $output)" -ForegroundColor Gray
