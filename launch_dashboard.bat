@echo off
echo Starting Xempla AI Intern Prototype Dashboard...
echo.
echo Please wait while the dashboard loads...
echo.
echo Once loaded, open your browser to: http://localhost:8502
echo.
echo Press Ctrl+C to stop the dashboard
echo.
cd /d "C:\Users\Shekhar Bhardwaj\OneDrive\Desktop\Projects\xempla_ai_intern_prototype"
python -m streamlit run enhanced_dashboard.py --server.port 8502 --server.address localhost
pause 