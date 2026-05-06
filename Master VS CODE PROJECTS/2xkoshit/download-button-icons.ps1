# Download Official 2XKO Button Notation SVG Icons from Riot Games CDN

$outputPath = "images\notation"

if (!(Test-Path $outputPath)) {
    New-Item -ItemType Directory -Path $outputPath | Out-Null
}

$baseUrl = "https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest"

$icons = @(
    "L.svg", "M.svg", "H.svg",
    "S1.svg", "S2.svg",
    "down.svg", "forward.svg", "back.svg",
    "down_forward.svg", "down_back.svg",
    "forward_forward.svg", "back_back.svg",
    "up.svg", "plus.svg"
)

$downloaded = 0
$failed = 0

Write-Host "Downloading 2XKO Button Notation SVG Icons..." -ForegroundColor Green

foreach ($icon in $icons) {
    $url = "$baseUrl/$icon"
    $outputFile = Join-Path $outputPath $icon
    
    try {
        # Using Invoke-WebRequest to download
        Write-Host "Downloading: $icon" -NoNewline
        Invoke-WebRequest -Uri $url -OutFile $outputFile -ErrorAction Stop
        Write-Host " OK" -ForegroundColor Green
        $downloaded++
    }
    catch {
        Write-Host " FAILED" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
}


Write-Host "Downloaded: $downloaded | Failed: $failed" -ForegroundColor Green

# Verify files
$fileCount = (Get-ChildItem -Path $outputPath -Filter "*.svg" -ErrorAction SilentlyContinue | Measure-Object).Count
Write-Host "Total SVG files in notation folder: $fileCount files" -ForegroundColor Cyan
Write-Host ""

if ($fileCount -gt 0) {
    Write-Host "Files downloaded successfully! You can now use these in your LaTeX guide." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Download move demonstration screenshots from 2XKO game" -ForegroundColor Gray
    Write-Host "2. Save screenshots to images/moves/ directory" -ForegroundColor Gray
    Write-Host "3. Compile LaTeX guide with: pdflatex Vishit.tex" -ForegroundColor Gray
}
else {
    Write-Host "Warning: No SVG files were downloaded. Check your internet connection." -ForegroundColor Yellow
}
