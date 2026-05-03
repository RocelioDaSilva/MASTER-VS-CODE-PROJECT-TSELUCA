#!/usr/bin/env bash
# Run Streamlit monitoring dashboard (UNIX)
source venv/bin/activate
streamlit run monitoring/monitoring_app.py --server.headless true --server.port 8502
