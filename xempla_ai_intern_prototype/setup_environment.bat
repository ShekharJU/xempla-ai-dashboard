@echo off
echo Setting up Python virtual environment for Xempla AI Prototype...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo WARNING: requirements.txt not found, installing basic dependencies...
    pip install streamlit pandas numpy plotly scikit-learn httpx python-dotenv
)

echo.
echo ========================================
echo Environment setup complete!
echo ========================================
echo.
echo To activate the environment:
echo   venv\Scripts\activate.bat
echo.
echo To run the dashboard:
echo   python -m streamlit run xempla_final_dashboard.py
echo.
echo To run tests:
echo   python -m pytest tests/ -v
echo.
echo To deactivate:
echo   deactivate
echo.
pause 