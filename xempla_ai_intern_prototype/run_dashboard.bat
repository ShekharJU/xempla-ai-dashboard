@echo off
echo Starting Xempla AI Dashboard...

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_environment.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dashboard file exists
if not exist "xempla_final_dashboard.py" (
    echo ERROR: Dashboard file not found!
    echo Please ensure xempla_final_dashboard.py exists in the current directory
    pause
    exit /b 1
)

REM Start the dashboard
echo Starting Xempla Dashboard...
echo Dashboard will be available at: http://localhost:8501
echo Press Ctrl+C to stop the dashboard
echo.
python -m streamlit run xempla_final_dashboard.py --server.port 8501

pause 