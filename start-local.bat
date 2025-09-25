@echo off
REM NVIDIA AI Workbench Tutorial App - Local Startup Script
REM This script starts the application with local NVIDIA integration

echo Starting NVIDIA AI Workbench Tutorial App (Local Mode)
echo ========================================================

REM Load local environment
if exist ".env.local" (
   for /f "tokens=*" %i in (.env.local) do set %i
   echo Local environment loaded
) else (
   echo .env.local not found, using default configuration
)

REM Check Python environment
python --version >nul 2>1
if %errorlevel% neq 0 (
   echo Python not found
   pause
   exit /b 1
)

REM Install/update dependencies if needed
echo Checking dependencies...
pip install -q -e . >nul 2>1
if %errorlevel% equ 0 (
   echo Dependencies up to date
) else (
   echo Dependency installation failed
)

REM Start the application
echo Starting Streamlit application...
echo.
streamlit run src/tutorial_app/streamlit_app.py --server.headless false --server.address localhost --server.port 8501

pause
