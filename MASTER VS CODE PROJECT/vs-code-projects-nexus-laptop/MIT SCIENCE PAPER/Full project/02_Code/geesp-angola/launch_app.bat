@echo off
REM GEESP-Angola One-Click Launcher for Windows
REM Launches the unified Streamlit application

echo ========================================
echo   GEESP-Angola Application Launcher
echo   Geospatial Energy for Equity ^& Solar Planning
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

REM Navigate to script directory
cd /d "%~dp0"

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Using system Python.
)

REM Check if dependencies are installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements-app.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create necessary directories
if not exist "data\processed" mkdir "data\processed"
if not exist "logs" mkdir "logs"

echo.
echo Starting GEESP-Angola application...
echo The app will open in your default browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

REM Launch Streamlit app (using canonical unified app)
streamlit run geesp_unified_app.py --server.headless=false --server.port=8501

pause
