#!/bin/bash
# GEESP-Angola One-Click Launcher for Linux/macOS
# Launches the unified Streamlit application

echo "========================================"
echo "  GEESP-Angola Application Launcher"
echo "  Geospatial Energy for Equity & Solar Planning"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.11+ from https://www.python.org/"
    exit 1
fi

# Navigate to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "No virtual environment found. Using system Python."
fi

# Check if dependencies are installed
python3 -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements-app.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Create necessary directories
mkdir -p data/processed
mkdir -p logs

echo ""
echo "Starting GEESP-Angola application..."
echo "The app will open in your default browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Launch Streamlit app (using canonical unified app)
streamlit run geesp_unified_app.py --server.headless=false --server.port=8501
