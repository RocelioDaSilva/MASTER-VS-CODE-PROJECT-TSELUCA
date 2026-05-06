#!/usr/bin/env bash
# Run Streamlit dashboard (UNIX)
source venv/bin/activate
streamlit run dashboard/app.py --server.headless true --server.port 8501
