@echo off
REM 2XKO Vi Guide Compilation Script
REM Compiles LaTeX guide with 2XKO notation images

setlocal enabledelayedexpansion

cls
echo.
echo ============================================
echo 2XKO Vi Guide Compilation Tool
echo ============================================
echo.

REM Check if pdflatex is available
where pdflatex >nul 2>nul
if errorlevel 1 (
    echo ERROR: pdflatex not found in PATH
    echo Please install MiKTeX or TeX Live
    echo.
    pause
    exit /b 1
)

echo Checking for required files...
if not exist "Vishit.tex" (
    echo ERROR: Vishit.tex not found
    pause
    exit /b 1
)

if not exist "images\notation" (
    echo ERROR: images\notation directory not found
    pause
    exit /b 1
)

echo.
echo Images found in notation folder:
for %%f in (images\notation\*.svg) do echo   - %%~nxf

echo.
echo ============================================
echo Starting compilation...
echo ============================================
echo.

REM Run pdflatex (twice for proper TOC and references)
echo [1/2] First pass...
pdflatex -quiet Vishit.tex

if errorlevel 1 (
    echo ERROR: First compilation failed
    pause
    exit /b 1
)

echo [2/2] Second pass...
pdflatex -quiet Vishit.tex

if errorlevel 1 (
    echo ERROR: Second compilation failed
    pause
    exit /b 1
)

echo.
echo ============================================
echo Compilation SUCCESSFUL!
echo ============================================
echo.

if exist "Vishit.pdf" (
    echo Generated: Vishit.pdf
    echo Size: 
    for /f %%A in ('wmic datafile where name="!cd:\=\\!\Vishit.pdf" get filesize^| findstr [0-9]') do (
        set /a size=%%A/1024
        echo   !size! KB
    )
    echo.
    echo Opening PDF...
    start Vishit.pdf
) else (
    echo ERROR: Vishit.pdf not created
    pause
    exit /b 1
)

echo.
echo Press any key to exit...
pause >nul
