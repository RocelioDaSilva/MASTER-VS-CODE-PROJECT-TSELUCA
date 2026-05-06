@echo off
REM Daily news fetch - run via Windows Task Scheduler
REM Working directory should be the repository root

cd /d "%~dp0\.."
python automation\fetch_alerts.py
