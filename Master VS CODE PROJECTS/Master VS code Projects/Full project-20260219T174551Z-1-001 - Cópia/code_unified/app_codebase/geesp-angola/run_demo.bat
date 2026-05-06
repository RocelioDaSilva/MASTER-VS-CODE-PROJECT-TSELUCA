@echo off
setlocal EnableDelayedExpansion

echo ============================================================
echo  GEESP-Angola  ^|  Investor Demo Launcher
echo ============================================================
echo.

:: --- Locate venv Python -------------------------------------------------
set "VENV_PYTHON=%~dp0..\..\..\..\.venv\Scripts\python.exe"
if not exist "%VENV_PYTHON%" (
    :: fallback: look for python on PATH
    where python >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python not found. Activate your virtual environment first.
        pause
        exit /b 1
    )
    set "VENV_PYTHON=python"
)

:: --- Check / install streamlit ------------------------------------------
"%VENV_PYTHON%" -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing streamlit...
    "%VENV_PYTHON%" -m pip install streamlit --quiet
)

:: --- Create logs directory ----------------------------------------------
if not exist "%~dp0logs" mkdir "%~dp0logs"

:: --- Open browser after 3 second delay ----------------------------------
start "" /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8501"

echo Starting GEESP-Angola dashboard at http://localhost:8501
echo Press Ctrl+C to stop.
echo.

:: --- Launch app ---------------------------------------------------------
cd /d "%~dp0"
"%VENV_PYTHON%" -m streamlit run backend\dashboard\app.py ^
    --server.port=8501 ^
    --server.headless=false ^
    --browser.gatherUsageStats=false ^
    2>&1 | tee logs\demo_%DATE:~-4,4%%DATE:~-10,2%%DATE:~-7,2%.log

pause
