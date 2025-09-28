@echo off
REM NVIDIA AI Workbench Tutorial App - Health Check Script (Windows)
REM This script performs comprehensive health checks including NVIDIA GPU

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo  NVIDIA AI Workbench Tutorial App - Health Check
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

echo 🔍 Performing comprehensive health checks...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found
    goto :health_failed
)
echo ✅ Python found

REM Check pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found
    goto :health_failed
)
echo ✅ pip found

REM Check NVIDIA GPU
nvidia-smi >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  NVIDIA GPU not detected or nvidia-smi not available
    set NVIDIA_AVAILABLE=false
) else (
    echo ✅ NVIDIA GPU detected
    set NVIDIA_AVAILABLE=true
)

REM Check if requirements.txt exists and is valid
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found
    goto :health_failed
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

    docker-compose ps --services --filter "status=running" 2>nul | findstr /c:"prometheus" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Prometheus container running
    ) else (
        echo ⚠️  Prometheus container not running
    )

    docker-compose ps --services --filter "status=running" 2>nul | findstr /c:"grafana" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Grafana container running
    ) else (
        echo ⚠️  Grafana container not running
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

REM Check backend API
curl -s -f http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend API responding (http://localhost:8000/health)
) else (
    echo ⚠️  Backend API not responding
)

REM Check Gitea
curl -s -f -u admin:admin http://localhost:3001/api/v1/version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Gitea responding (http://localhost:3001)
) else (
    echo ⚠️  Gitea not responding
)

REM Check Grafana
curl -s -f http://localhost:3000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Grafana responding (http://localhost:3000)
) else (
    echo ⚠️  Grafana not responding
)

REM Check Prometheus
curl -s -f http://localhost:9090/-/healthy >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Prometheus responding (http://localhost:9090)
) else (
    echo ⚠️  Prometheus not responding
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

if exist ".streamlit\secrets.toml" (
    echo ✅ Streamlit secrets file exists
) else (
    echo ⚠️  Streamlit secrets file not found
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

REM Check security module
python -c "import sys; sys.path.append('src'); from tutorial_app.common.security import initialize_security; print('✅ Security module importable')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Security module not importable
)

echo.
echo ===============================================
echo  Health Check Summary
echo ===============================================
echo.

echo 📋 Comprehensive health check complete.
echo.
echo 🌐 Service URLs (if running):
echo    Tutorial App: http://localhost
echo    Backend API:  http://localhost:8000
echo    Gitea (Git):   http://localhost:3001 (admin/admin)
echo    Grafana:       http://localhost:3000 (admin/admin)
echo    Prometheus:    http://localhost:9090
echo.
echo 📖 For troubleshooting, see:
echo    docs/TROUBLESHOOTING.md
echo    docs/QUICK_START.md
echo.
echo 💡 Quick fixes:
echo    - Run setup_all.bat for full setup
echo    - Run docker-compose up -d to start services
echo    - Check logs with docker-compose logs
echo    - Run environment_validation.bat for basic checks
echo.

goto :end

:health_failed
echo.
echo ❌ Health check failed. Please address the critical errors above.
echo.
pause
exit /b 1

:end
echo All health checks completed successfully.
pause
endlocal
