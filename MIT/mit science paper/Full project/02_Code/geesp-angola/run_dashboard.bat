@echo off
REM Run Streamlit dashboard using project's venv
call venv\Scripts\activate
streamlit run dashboard\app.py --server.headless true --server.port 8501
pause
