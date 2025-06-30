@echo off
echo Running Xempla AI Prototype Tests...

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

REM Run tests with coverage
echo Running tests with coverage...
python -m pytest tests/ -v --cov=src --cov=simulation --cov=utils --cov-report=html --cov-report=term-missing

REM Check if tests passed
if errorlevel 1 (
    echo.
    echo ========================================
    echo Some tests failed! Check the output above.
    echo ========================================
) else (
    echo.
    echo ========================================
    echo All tests passed successfully!
    echo ========================================
)

echo.
echo Coverage report generated in htmlcov/index.html
echo.
pause 