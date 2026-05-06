@echo off
REM Root-level launcher for GEESP-Angola unified app
REM Delegates to 02_Code/geesp-angola/launch_app.bat

echo ========================================
echo   GEESP-Angola - Root Launcher
echo   (Unified Streamlit Application)
echo ========================================
echo.

REM Change to project root (this file's directory)
cd /d "%~dp0"

REM Navigate to the main code directory
cd "02_Code\geesp-angola"

REM Call the existing Windows launcher
call launch_app.bat

