@echo off
REM NVIDIA AI Workbench Tutorial App - Environment Validation Script (Windows)
REM This script validates the environment setup and services

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo  NVIDIA AI Workbench Tutorial App - Environment Validation
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

echo 🔍 Validating environment setup...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found
    goto :validation_failed
)
echo ✅ Python found

REM Check pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found
    goto :validation_failed
)
echo ✅ pip found

REM Check if requirements.txt exists and is valid
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found
    goto :validation_failed
)
echo ✅ requirements.txt found

REM Check if dependencies are installed
pip list | findstr "streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Streamlit not installed (run setup.bat first)
) else (
    echo ✅ Streamlit installed
)

echo.
echo 🔍 Checking Docker services...
echo.

REM Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Docker not available (optional for local development)
    set DOCKER_AVAILABLE=false
) else (
    echo ✅ Docker available
    set DOCKER_AVAILABLE=true
)

if "%DOCKER_AVAILABLE%"=="true" (
    REM Check if docker-compose services are running
    docker-compose ps --services --filter "status=running" 2>nul | findstr /c:"tutorial-app" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Tutorial app container running
    ) else (
        echo ⚠️  Tutorial app container not running
    )

    docker-compose ps --services --filter "status=running" 2>nul | findstr /c:"gitea" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Gitea container running
    ) else (
        echo ⚠️  Gitea container not running
    )

    docker-compose ps --services --filter "status=running" 2>nul | findstr /c:"redis" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Redis container running
    ) else (
        echo ⚠️  Redis container not running
    )
)

echo.
echo 🔍 Checking service endpoints...
echo.

REM Check tutorial app health
curl -s -f http://localhost/healthz >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Tutorial app responding (http://localhost/healthz)
) else (
    echo ⚠️  Tutorial app not responding
)

REM Check Gitea
curl -s -f -u admin:admin http://localhost:3001/api/v1/version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Gitea responding (http://localhost:3001)
) else (
    echo ⚠️  Gitea not responding
)

REM Check Redis if Docker is available
if "%DOCKER_AVAILABLE%"=="true" (
    docker-compose exec -T redis redis-cli ping 2>nul | findstr "PONG" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Redis responding
    ) else (
        echo ⚠️  Redis not responding
    )
)

echo.
echo 🔍 Checking configuration files...
echo.

REM Check environment files
if exist ".env" (
    echo ✅ .env file exists
) else (
    echo ⚠️  .env file not found
)

if exist "variables.env" (
    echo ✅ variables.env file exists
) else (
    echo ⚠️  variables.env file not found
)

if exist "deploy\environments\production.env" (
    echo ✅ Production environment file exists
) else (
    echo ⚠️  Production environment file not found
)

echo.
echo 🔍 Checking application modules...
echo.

REM Check if main application can be imported
python -c "import sys; sys.path.append('src'); from tutorial_app.streamlit_app import main; print('✅ Main application module importable')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Main application module not importable
)

REM Check NVIDIA workbench client
python -c "import sys; sys.path.append('src'); from tutorial_app.common.wb_svc_client import list_projects; print('✅ NVIDIA workbench client importable')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  NVIDIA workbench client not importable
)

echo.
echo ===============================================
echo  Validation Summary
echo ===============================================
echo.

REM Count warnings and errors
set WARNINGS=0
set ERRORS=0

REM This is a simplified summary - in a real script you'd track these properly
echo 📋 Environment validation complete.
echo.
echo 🌐 Service URLs (if running):
echo    Tutorial App: http://localhost
echo    Gitea (Git):   http://localhost:3001 (admin/admin)
echo    Grafana:       http://localhost:3000 (admin/admin)
echo    Prometheus:    http://localhost:9090
echo.
echo 📖 For detailed setup instructions, see:
echo    README.md
echo    docs/DEVELOPER_GUIDE.md
echo.
echo 💡 Quick fixes:
echo    - Run setup_all.bat for full setup
echo    - Run docker-compose up -d to start services
echo    - Check logs with docker-compose logs
echo.

goto :end

:validation_failed
echo.
echo ❌ Validation failed. Please address the errors above.
echo.
pause
exit /b 1

:end
echo Validation completed.
pause
endlocal
