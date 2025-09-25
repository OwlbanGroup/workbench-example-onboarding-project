@echo off
REM NVIDIA AI Workbench Tutorial App - Local Computer Integration Script
REM This script integrates the tutorial app with local NVIDIA AI Workbench installation

setlocal enabledelayedexpansion

echo 🚀 Setting up NVIDIA AI Workbench Tutorial App - Local Integration
echo =================================================================

REM Check if we're in the right directory
if not exist "pyproject.toml" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Detect NVIDIA AI Workbench installation
:detect_workbench
echo 📍 Detecting NVIDIA AI Workbench installation...

set "WORKBENCH_PATH="
set "WORKBENCH_FOUND=false"

REM Common installation paths
set "POSSIBLE_PATHS=C:\Program Files\NVIDIA AI Workbench;C:\Program Files (x86)\NVIDIA AI Workbench;%USERPROFILE%\AppData\Local\NVIDIA AI Workbench;%PROGRAMFILES%\NVIDIA AI Workbench"

for %%p in (%POSSIBLE_PATHS%) do (
    if exist "%%p" (
        set "WORKBENCH_PATH=%%p"
        set "WORKBENCH_FOUND=true"
        goto :workbench_found
    )
)

REM Check if workbench command is available in PATH
where workbench >nul 2>&1
if %errorlevel%==0 (
    set "WORKBENCH_FOUND=true"
    echo ✅ NVIDIA AI Workbench found in PATH
    goto :configure_integration
)

:workbench_not_found
echo ⚠️  NVIDIA AI Workbench not found in standard locations
echo.
echo Please ensure NVIDIA AI Workbench is installed and running.
echo You can download it from: https://www.nvidia.com/en-us/deep-learning-ai/solutions/data-science/workbench/
echo.
set /p "CONTINUE=Do you want to continue with manual configuration? (y/n): "
if /i not "!CONTINUE!"=="y" (
    echo Setup cancelled.
    pause
    exit /b 1
)
goto :manual_config

:workbench_found
echo ✅ NVIDIA AI Workbench found at: !WORKBENCH_PATH!
goto :configure_integration

:configure_integration
echo.
echo 🔧 Configuring local NVIDIA AI Workbench integration...

REM Create local configuration
set "LOCAL_CONFIG=.nvidia-workbench-local"

if not exist "%LOCAL_CONFIG%" mkdir "%LOCAL_CONFIG%"

REM Generate local environment configuration
(
echo # Local NVIDIA AI Workbench Integration Configuration
echo # Generated on %DATE% %TIME%
echo.
echo # NVIDIA AI Workbench Paths
echo WORKBENCH_INSTALL_PATH=!WORKBENCH_PATH!
echo WORKBENCH_VERSION=detecting...
echo.
echo # Local Development Settings
echo LOCAL_INTEGRATION=true
echo WORKBENCH_SOCKET_PATH=/tmp/nvidia-workbench.sock
echo WORKBENCH_API_URL=http://localhost:8080
echo.
echo # Project Integration
echo PROJECT_NAME=workbench-example-onboarding-project
echo PROJECT_PATH=%CD%
echo.
echo # Security (Local Development)
echo ALLOW_LOCAL_CONNECTIONS=true
echo SKIP_SSL_VERIFICATION=true
echo DEVELOPMENT_MODE=true
) > "%LOCAL_CONFIG%\config.env"

echo ✅ Local configuration created at: %LOCAL_CONFIG%\config.env

REM Update variables.env for local integration
echo.
echo 🔄 Updating variables.env for local integration...

REM Backup existing variables.env
if exist "variables.env" copy "variables.env" "variables.env.backup" >nul

(
echo.
echo # Local NVIDIA AI Workbench Integration (added by setup script)
echo LOCAL_INTEGRATION=true
echo WORKBENCH_INSTALL_PATH=!WORKBENCH_PATH!
echo WORKBENCH_SOCKET_PATH=/tmp/nvidia-workbench.sock
echo WORKBENCH_API_URL=http://localhost:8080
echo ALLOW_LOCAL_CONNECTIONS=true
echo SKIP_SSL_VERIFICATION=true
echo NVIDIA_ENVIRONMENT=true
) >> "variables.env"

echo ✅ variables.env updated

REM Create local environment file
echo.
echo 🏠 Setting up local development environment...

if exist ".env.local" copy ".env.local" ".env.local.backup" >nul

(
echo # Local NVIDIA AI Workbench Development Environment
echo ENVIRONMENT=development
echo DEBUG=true
echo LOG_LEVEL=DEBUG
echo.
echo # Application Settings
echo STREAMLIT_SERVER_HEADLESS=false
echo STREAMLIT_SERVER_PORT=8501
echo STREAMLIT_SERVER_ADDRESS=localhost
echo STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
echo STREAMLIT_THEME_BASE=dark
echo.
echo # Local NVIDIA AI Workbench Integration
echo LOCAL_INTEGRATION=true
echo WORKBENCH_SOCKET_PATH=/tmp/nvidia-workbench.sock
echo WORKBENCH_API_URL=http://localhost:8080
echo.
echo # Database/Cache (Local)
echo REDIS_URL=redis://localhost:6379
echo REDIS_MAX_CONNECTIONS=10
echo.
echo # Security (Relaxed for Local Development)
echo SECRET_KEY=dev-secret-key-change-in-production
echo SESSION_TIMEOUT=3600
echo RATE_LIMIT_REQUESTS=1000
echo RATE_LIMIT_WINDOW=60
echo ALLOWED_DOMAINS=localhost,127.0.0.1
echo.
echo # Development Features
echo ENABLE_DEBUG_LOGGING=true
echo ENABLE_PERFORMANCE_MONITORING=true
echo ENABLE_SECURITY_HEADERS=false
echo AUTO_RELOAD=true
echo DEVELOPMENT_MODE=true
echo MAINTENANCE_MODE=false
echo.
echo # NVIDIA Environment Flags
echo NVIDIA_ENVIRONMENT=true
echo INTERNAL_DEPLOYMENT=false
echo ALLOW_LOCAL_CONNECTIONS=true
echo SKIP_SSL_VERIFICATION=true
) > ".env.local"

echo ✅ Local environment created at: .env.local

REM Create workbench integration script
:create_integration_script
echo.
echo 📜 Creating workbench integration helper script...

(
echo @echo off
echo REM NVIDIA AI Workbench Integration Helper Script
echo REM This script helps with local NVIDIA AI Workbench operations
echo.
echo setlocal enabledelayedexpansion
echo.
echo REM Check if workbench is available
echo where workbench ^>nul 2^>^1
echo if %%errorlevel%% neq 0 ^(
echo    echo ❌ NVIDIA AI Workbench CLI not found in PATH
echo    echo Please ensure NVIDIA AI Workbench is installed and CLI is in PATH
echo    pause
echo    exit /b 1
echo ^)
echo.
echo echo ✅ NVIDIA AI Workbench CLI found
echo.
echo REM Display available projects
echo echo 📋 Available projects:
echo workbench projects list
echo.
echo REM Check current project status
echo echo 🔍 Current project status:
echo workbench status
echo.
echo echo.
echo echo 💡 Integration Commands:
echo echo   workbench run          - Start the application
echo echo   workbench stop          - Stop the application
echo echo   workbench logs          - View application logs
echo echo   workbench shell         - Open shell in container
echo echo   workbench test          - Run tests
echo echo.
echo pause
) > "workbench-helper.bat"

echo ✅ Workbench helper script created: workbench-helper.bat

REM Test integration
:test_integration
echo.
echo 🧪 Testing local integration...

REM Test if we can import the workbench client
python -c "from src.tutorial_app.common.wb_svc_client import list_projects; print('✅ NVIDIA integration module loaded successfully')" 2>nul
if %errorlevel%==0 (
    echo ✅ NVIDIA integration module test passed
) else (
    echo ⚠️  NVIDIA integration module test failed - may need configuration
)

REM Check if socket path exists (for Unix socket communication)
if exist "%TEMP%\nvidia-workbench.sock" (
    echo ✅ Workbench socket found
) else (
    echo ℹ️  Workbench socket not found - will use HTTP fallback
)

echo ✅ Local integration testing completed

:manual_config
REM Manual configuration section
if "%WORKBENCH_FOUND%"=="false" (
    echo.
    echo 🔧 Manual NVIDIA AI Workbench Configuration
    echo ===========================================
    echo.
    echo Since NVIDIA AI Workbench was not auto-detected, please provide:
    echo.
    set /p "WB_PATH=Installation path (or press Enter to skip): "
    if defined WB_PATH (
        set "WORKBENCH_PATH=!WB_PATH!"
        echo Manual path set to: !WORKBENCH_PATH!
    )
)

:create_startup_script
echo.
echo 🚀 Creating startup script for easy launching...

(
echo @echo off
echo REM NVIDIA AI Workbench Tutorial App - Local Startup Script
echo REM This script starts the application with local NVIDIA integration
echo.
echo echo 🚀 Starting NVIDIA AI Workbench Tutorial App ^(Local Mode^)
echo echo ========================================================
echo.
echo REM Load local environment
echo if exist ".env.local" ^(
echo    for /f "tokens=*" %%i in ^(.env.local^) do set %%i
echo    echo ✅ Local environment loaded
echo ^) else ^(
echo    echo ⚠️  .env.local not found, using default configuration
echo ^)
echo.
echo REM Check Python environment
echo python --version ^>nul 2^>^1
echo if %%errorlevel%% neq 0 ^(
echo    echo ❌ Python not found
echo    pause
echo    exit /b 1
echo ^)
echo.
echo REM Install/update dependencies if needed
echo echo 📦 Checking dependencies...
echo pip install -q -e . ^>nul 2^>^1
echo if %%errorlevel%% equ 0 ^(
echo    echo ✅ Dependencies up to date
echo ^) else ^(
echo    echo ⚠️  Dependency installation failed
echo ^)
echo.
echo REM Start the application
echo echo 🎯 Starting Streamlit application...
echo echo.
echo streamlit run src/tutorial_app/streamlit_app.py --server.headless false --server.address localhost --server.port 8501
echo.
echo pause
) > "start-local.bat"

echo ✅ Local startup script created: start-local.bat

:create_readme
echo.
echo 📖 Creating local integration README...

(
echo # Local NVIDIA AI Workbench Integration
echo.
echo This document explains how to use the NVIDIA AI Workbench Tutorial App with your local NVIDIA AI Workbench installation.
echo.
echo ## Quick Start
echo.
echo 1. **Run the setup script:**
echo    ```batch
echo    setup_local_nvidia_workbench.bat
echo    ```
echo.
echo 2. **Start the application:**
echo    ```batch
echo    start-local.bat
echo    ```
echo    Or manually:
echo    ```batch
echo    streamlit run src/tutorial_app/streamlit_app.py
echo    ```
echo.
echo 3. **Use workbench helper:**
echo    ```batch
echo    workbench-helper.bat
echo    ```
echo.
echo ## Configuration Files
echo.
echo - **`.env.local`** - Local development environment variables
echo - **`.nvidia-workbench-local\config.env`** - NVIDIA Workbench integration settings
echo - **`variables.env`** - Updated with local integration settings
echo.
echo ## Features
echo.
echo - ✅ Local NVIDIA AI Workbench detection and integration
echo - ✅ Automatic environment configuration
echo - ✅ Helper scripts for common operations
echo - ✅ Development-friendly settings (relaxed security)
echo - ✅ Socket and HTTP communication support
echo.
echo ## Troubleshooting
echo.
echo ### Workbench Not Detected
echo If NVIDIA AI Workbench is not auto-detected:
echo 1. Ensure it's installed and running
echo 2. Check if the CLI is in your PATH
echo 3. Run setup again or configure manually
echo.
echo ### Connection Issues
echo - Check if NVIDIA AI Workbench is running
echo - Verify socket path: `/tmp/nvidia-workbench.sock`
echo - Check firewall settings for local connections
echo.
echo ### Import Errors
echo - Ensure all dependencies are installed: `pip install -e .`
echo - Check Python path includes the `src` directory
echo.
echo ## Security Note
echo.
echo This local integration uses relaxed security settings for development.
echo **Do not use these settings in production!**
echo.
echo For production deployment, use the production scripts:
echo - `deploy/scripts/deploy_production.bat` (Windows)
echo - `deploy/scripts/deploy_production.sh` (Linux)
) > "LOCAL_INTEGRATION_README.md"

echo ✅ Local integration README created: LOCAL_INTEGRATION_README.md

:final_summary
echo.
echo 🎉 Local NVIDIA AI Workbench integration setup complete!
echo.
echo 📋 Summary:
echo   - Local configuration: .env.local
echo   - Workbench config: .nvidia-workbench-local\config.env
echo   - Startup script: start-local.bat
echo   - Helper script: workbench-helper.bat
echo   - Documentation: LOCAL_INTEGRATION_README.md
echo.
echo 🚀 Next steps:
echo   1. Review the generated configuration files
echo   2. Run: start-local.bat to start the application
echo   3. Use: workbench-helper.bat for workbench operations
echo   4. Read: LOCAL_INTEGRATION_README.md for detailed information
echo.
echo 💡 Tips:
echo   - The app is configured for local development with relaxed security
echo   - Use production deployment scripts for production environments
echo   - Check logs in the terminal for any connection issues
echo.
pause
