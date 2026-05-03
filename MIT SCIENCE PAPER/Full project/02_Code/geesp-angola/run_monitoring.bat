@echo off
REM Run Streamlit monitoring dashboard using project's venv
call venv\Scripts\activate
streamlit run monitoring\monitoring_app.py --server.headless true --server.port 8502
pause
