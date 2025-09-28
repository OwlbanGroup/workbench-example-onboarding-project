@echo off
REM NVIDIA AI Workbench Tutorial App - Master Setup Script (Windows)
REM This script provides a menu to choose different setup configurations

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo  NVIDIA AI Workbench Tutorial App Setup
echo ===============================================
echo.
echo This script helps you set up the tutorial application
echo with different configurations and environments.
echo.

REM Check if we're in the right directory
if not exist "pyproject.toml" (
    echo ❌ Error: Please run this script from the project root directory
    echo.
    echo Expected files not found. Please ensure you're in the project root.
    pause
    exit /b 1
)

REM Check prerequisites
echo 🔍 Checking prerequisites...

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

REM Check git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git not found. Please install Git and try again.
    pause
    exit /b 1
)
echo ✅ Git found

REM Check Docker (optional)
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker found
    set DOCKER_AVAILABLE=true
) else (
    echo ⚠️  Docker not found (optional for local development)
    set DOCKER_AVAILABLE=false
)

echo.
echo ===============================================
echo  Setup Options
echo ===============================================
echo.
echo 1) Quick Setup (Basic dependencies only)
echo    - Install Python dependencies
echo    - Basic configuration
echo.
echo 2) Local Development Setup
echo    - Full local development environment
echo    - NVIDIA AI Workbench local integration
echo    - Helper scripts and documentation
echo.
echo 3) NVIDIA Integration Setup (Production)
echo    - Complete NVIDIA AI Workbench integration
echo    - Production-ready configuration
echo    - Environment-specific settings
echo.
echo 4) Docker Environment Setup
echo    - Docker Compose environment
echo    - Local Gitea server
echo    - Monitoring stack (Prometheus/Grafana)
echo.
echo 5) Run Tests
echo    - Execute all test suites
echo    - Performance and integration tests
echo.
echo 6) Environment Validation
echo    - Check all services and configurations
echo    - Health checks and diagnostics
echo.
echo 0) Exit
echo.
echo ===============================================

:menu
set /p choice="Enter your choice (0-6): "

if "%choice%"=="0" goto :exit
if "%choice%"=="1" goto :quick_setup
if "%choice%"=="2" goto :local_dev_setup
if "%choice%"=="3" goto :nvidia_setup
if "%choice%"=="4" goto :docker_setup
if "%choice%"=="5" goto :run_tests
if "%choice%"=="6" goto :validate_env
goto :invalid_choice

:quick_setup
echo.
echo ===============================================
echo  Quick Setup
echo ===============================================
echo.
call setup.bat
if %errorlevel% neq 0 (
    echo ❌ Quick setup failed
    goto :error_exit
)
echo ✅ Quick setup completed successfully
goto :setup_complete

:local_dev_setup
echo.
echo ===============================================
echo  Local Development Setup
echo ===============================================
echo.
call setup_local_nvidia_workbench_simple.bat
if %errorlevel% neq 0 (
    echo ❌ Local development setup failed
    goto :error_exit
)
echo ✅ Local development setup completed successfully
goto :setup_complete

:nvidia_setup
echo.
echo ===============================================
echo  NVIDIA Integration Setup
echo ===============================================
echo.
call setup_nvidia_integration.bat
if %errorlevel% neq 0 (
    echo ❌ NVIDIA integration setup failed
    goto :error_exit
)
echo ✅ NVIDIA integration setup completed successfully
goto :setup_complete

:docker_setup
echo.
echo ===============================================
echo  Docker Environment Setup
echo ===============================================
echo.
if "%DOCKER_AVAILABLE%"=="false" (
    echo ❌ Docker is required for this setup but was not found.
    echo Please install Docker and try again.
    goto :error_exit
)

echo Starting Docker environment...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ❌ Docker environment setup failed
    goto :error_exit
)

echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo ✅ Docker environment setup completed successfully
echo.
echo 🌐 Access URLs:
echo    Tutorial App: http://localhost
echo    Gitea (Git):   http://localhost:3001 (admin/admin)
echo    Grafana:       http://localhost:3000 (admin/admin)
echo    Prometheus:    http://localhost:9090
goto :setup_complete

:run_tests
echo.
echo ===============================================
echo  Running Tests
echo ===============================================
echo.
call run_all_tests.py
if %errorlevel% neq 0 (
    echo ❌ Some tests failed
    goto :error_exit
)
echo ✅ All tests passed
goto :setup_complete

:validate_env
echo.
echo ===============================================
echo  Environment Validation
echo ===============================================
echo.
echo 🔍 Validating environment...

REM Check if services are running
docker-compose ps >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker services are running
) else (
    echo ⚠️  Docker services not running (run option 4 first)
)

REM Check application health
curl -s http://localhost/healthz >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Application is responding
) else (
    echo ⚠️  Application not responding
)

REM Check Gitea
curl -s -u admin:admin http://localhost:3001/api/v1/version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Gitea is responding
) else (
    echo ⚠️  Gitea not responding
)

echo.
echo 📋 Validation complete. Check the output above for any issues.
goto :setup_complete

:invalid_choice
echo.
echo ❌ Invalid choice. Please select 0-6.
goto :menu

:setup_complete
echo.
echo ===============================================
echo  Setup Complete!
echo ===============================================
echo.
echo What would you like to do next?
echo.
echo 1) Return to main menu
echo 2) Start the application
echo 3) Open documentation
echo 4) Exit
echo.
set /p next_choice="Enter your choice (1-4): "

if "%next_choice%"=="1" goto :menu
if "%next_choice%"=="2" goto :start_app
if "%next_choice%"=="3" goto :open_docs
if "%next_choice%"=="4" goto :exit
goto :setup_complete

:start_app
echo.
echo 🚀 Starting the application...
if exist "start-local.bat" (
    call start-local.bat
) else (
    streamlit run src/tutorial_app/streamlit_app.py
)
goto :exit

:open_docs
echo.
echo 📖 Opening documentation...
start README.md
start docs/DEVELOPER_GUIDE.md
goto :exit

:error_exit
echo.
echo ❌ Setup failed. Please check the error messages above.
pause
goto :exit

:exit
echo.
echo Thank you for using the NVIDIA AI Workbench Tutorial App setup!
echo.
pause
endlocal
exit /b 0
