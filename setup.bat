@echo off
REM NVIDIA AI Workbench Tutorial App - Basic Setup Script (Windows)
REM This script installs basic dependencies with error handling

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo  NVIDIA AI Workbench Tutorial App - Quick Setup
echo ===============================================
echo.

REM Check if we're in the right directory
if not exist "pyproject.toml" (
    echo ❌ Error: Please run this script from the project root directory
    echo.
    echo Expected files not found. Please ensure you're in the project root.
    pause
    exit /b 1
)

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ❌ Error: requirements.txt not found
    echo Please ensure the file exists in the project root.
    pause
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)
echo ✅ Python found

REM Check pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found. Please install pip and try again.
    pause
    exit /b 1
)
echo ✅ pip found

echo.
echo Installing dependencies for Owlban Group integration...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies. Please check the error above.
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully.
echo.
echo 📋 Next steps:
echo - Run the app with: streamlit run src/tutorial_app/streamlit_app.py
echo - For full setup, use: setup_all.bat
echo.
pause
endlocal
