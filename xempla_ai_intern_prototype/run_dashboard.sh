#!/bin/bash

echo "Starting Xempla AI Dashboard..."

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup_environment.sh first"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dashboard file exists
if [ ! -f "xempla_final_dashboard.py" ]; then
    echo "ERROR: Dashboard file not found!"
    echo "Please ensure xempla_final_dashboard.py exists in the current directory"
    exit 1
fi

# Start the dashboard
echo "Starting Xempla Dashboard..."
echo "Dashboard will be available at: http://localhost:8501"
echo "Press Ctrl+C to stop the dashboard"
echo ""
streamlit run xempla_final_dashboard.py --server.port 8501 