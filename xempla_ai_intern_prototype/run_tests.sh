#!/bin/bash

echo "Running Xempla AI Prototype Tests..."

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup_environment.sh first"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run tests with coverage
echo "Running tests with coverage..."
python -m pytest tests/ -v --cov=src --cov=simulation --cov=utils --cov-report=html --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "All tests passed successfully!"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "Some tests failed! Check the output above."
    echo "========================================"
fi

echo ""
echo "Coverage report generated in htmlcov/index.html"
echo "" 