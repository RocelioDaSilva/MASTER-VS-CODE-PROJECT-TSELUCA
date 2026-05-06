<#
Run the Automatic1111 batch img2img using the mapping.csv provided.
Usage (PowerShell):
  ./run_batch.ps1

Optional params:
  -WebUIUrl http://127.0.0.1:7860
  -InputDir finished-manuscript/cwbook_minimal_package
  -Mapping tools/image_pipeline/mapping.csv
  -OutputDir outputs/headers
  -Width 2400 -Height 400
#>
param(
  [string]$WebUIUrl = "http://127.0.0.1:7860",
  [string]$InputDir = "finished-manuscript/cwbook_minimal_package",
  [string]$Mapping = "tools/image_pipeline/mapping.csv",
  [string]$OutputDir = "outputs/headers",
  [int]$Width = 2400,
  [int]$Height = 400,
  [int]$Sleep = 1
)

# Activate virtual environment if present
$venvActivate = Join-Path -Path "." -ChildPath ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
  Write-Host "Activating virtual environment..."
  & $venvActivate
} else {
  Write-Host "No virtualenv activate script found at $venvActivate. Ensure Python and required packages are available." -ForegroundColor Yellow
}

# Check Automatic1111 API availability
try {
  $check = Invoke-RestMethod -Uri ("$WebUIUrl/sdapi/v1/sd-models") -Method Get -ErrorAction Stop
  Write-Host "Automatic1111 API reachable at $WebUIUrl." -ForegroundColor Green
} catch {
  Write-Warning "Could not reach Automatic1111 API at $WebUIUrl. Start the WebUI and try again.";
}

# Ensure output folder exists
if (-not (Test-Path $OutputDir)) { New-Item -ItemType Directory -Path $OutputDir | Out-Null }

Write-Host "Starting batch img2img..."
python tools/image_pipeline/batch_img2img.py --api-url $WebUIUrl --input-dir $InputDir --mapping $Mapping --output-dir $OutputDir --width $Width --height $Height --sleep $Sleep

if ($LASTEXITCODE -eq 0) {
  Write-Host "Batch completed. Outputs saved to: $OutputDir" -ForegroundColor Green
} else {
  Write-Host "Batch script exited with code $LASTEXITCODE" -ForegroundColor Red
}

# Optional: call a local upscaler here (Real-ESRGAN, Topaz) if installed
# Example (Real-ESRGAN CLI invocation placeholder):
# Get-ChildItem -Path $OutputDir -Filter "*.png" | ForEach-Object {
#   & python path\to\realesrgan\inference_realesrgan.py -n RealESRGAN_x4plus -i $_.FullName -o "${($_.DirectoryName)}\upscaled_${($_.Name)}" -s 2
# }
