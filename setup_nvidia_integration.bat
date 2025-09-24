@echo off
REM NVIDIA AI Workbench Tutorial App - Environment Setup Script (Windows)
REM This script configures the application for NVIDIA integration

echo 🚀 Setting up NVIDIA AI Workbench Tutorial App Environment
echo ==========================================================

REM Check if we're in the right directory
if not exist "pyproject.toml" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

echo 📋 Gathering configuration information...

REM NVIDIA Environment Configuration
set /p NVWB_API="NVIDIA AI Workbench API URL [https://api.nvidia-workbench.internal]: "
if "%NVWB_API%"=="" set NVWB_API=https://api.nvidia-workbench.internal

set /p PROXY_PREFIX="Reverse proxy prefix (e.g., /tutorial) [/tutorial]: "
if "%PROXY_PREFIX%"=="" set PROXY_PREFIX=/tutorial

set /p SECRET_KEY="Application secret key [auto-generate]: "
if "%SECRET_KEY%"=="" (
    REM Generate a random secret key using PowerShell
    for /f %%i in ('powershell -command "$bytes = New-Object Byte[] 32; (New-Object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes); [System.Convert]::ToHexString($bytes).ToLower()"') do set SECRET_KEY=%%i
)

set /p ALLOWED_DOMAINS="Allowed domains (comma-separated) [nvidia.com,developer.nvidia.com,forums.developer.nvidia.com]: "
if "%ALLOWED_DOMAINS%"=="" set ALLOWED_DOMAINS=nvidia.com,developer.nvidia.com,forums.developer.nvidia.com

REM Environment selection
echo.
echo 🌍 Select deployment environment:
echo 1^) Development
echo 2^) Staging
echo 3^) Production
set /p env_choice="Enter choice (1-3): "

if "%env_choice%"=="1" (
    set ENV_FILE=deploy\environments\development.env
    set ENVIRONMENT=development
) else if "%env_choice%"=="2" (
    set ENV_FILE=deploy\environments\staging.env
    set ENVIRONMENT=staging
    REM Create staging env if it doesn't exist
    if not exist "%ENV_FILE%" copy deploy\environments\production.env "%ENV_FILE%" >nul
) else if "%env_choice%"=="3" (
    set ENV_FILE=deploy\environments\production.env
    set ENVIRONMENT=production
) else (
    echo ❌ Invalid choice. Using development.
    set ENV_FILE=deploy\environments\development.env
    set ENVIRONMENT=development
)

echo.
echo ⚙️  Configuring environment file: %ENV_FILE%

REM Create environment file
(
echo # %ENVIRONMENT% Environment Configuration for NVIDIA Integration
echo ENVIRONMENT=%ENVIRONMENT%
echo DEBUG=false
echo LOG_LEVEL=INFO
echo.
echo # Application Settings
echo STREAMLIT_SERVER_HEADLESS=true
echo STREAMLIT_SERVER_PORT=8501
echo STREAMLIT_SERVER_ADDRESS=0.0.0.0
echo STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
echo STREAMLIT_THEME_BASE=dark
echo.
echo # NVIDIA AI Workbench Integration
echo NVWB_API=%NVWB_API%
echo PROXY_PREFIX=%PROXY_PREFIX%
echo.
echo # Database/Cache
echo REDIS_URL=redis://redis-service:6379
echo REDIS_MAX_CONNECTIONS=50
echo.
echo # Security
echo SECRET_KEY=%SECRET_KEY%
echo SESSION_TIMEOUT=1800
echo RATE_LIMIT_REQUESTS=100
echo RATE_LIMIT_WINDOW=60
echo ALLOWED_DOMAINS=%ALLOWED_DOMAINS%
echo.
echo # External Services
echo PROMETHEUS_URL=http://prometheus:9090
echo GRAFANA_URL=http://grafana:3000
echo.
echo # Feature Flags
echo ENABLE_DEBUG_LOGGING=false
echo ENABLE_PERFORMANCE_MONITORING=true
echo ENABLE_SECURITY_HEADERS=true
echo.
echo # SSL/TLS Settings
echo SSL_CERT_PATH=/etc/ssl/certs/tutorial-app.crt
echo SSL_KEY_PATH=/etc/ssl/private/tutorial-app.key
echo FORCE_SSL=true
echo.
echo # Monitoring
echo METRICS_ENABLED=true
echo HEALTH_CHECK_INTERVAL=30
echo LOG_TO_STDOUT=true
echo.
echo # Performance
echo MAX_WORKERS=4
echo WORKER_TIMEOUT=30
echo MAX_REQUESTS_PER_WORKER=1000
echo.
echo # NVIDIA-specific configuration
echo NVIDIA_ENVIRONMENT=true
echo INTERNAL_DEPLOYMENT=true
) > "%ENV_FILE%"

echo ✅ Environment configuration saved to %ENV_FILE%

REM Create .env for local development
echo.
echo 🏠 Setting up local development environment...

if exist .env copy .env .env.backup >nul 2>&1

(
echo # Local Development Environment Configuration
echo ENVIRONMENT=development
echo DEBUG=true
echo LOG_LEVEL=DEBUG
echo.
echo # Application Settings
echo STREAMLIT_SERVER_HEADLESS=true
echo STREAMLIT_SERVER_PORT=8501
echo STREAMLIT_SERVER_ADDRESS=0.0.0.0
echo STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
echo STREAMLIT_THEME_BASE=dark
echo.
echo # NVIDIA AI Workbench Integration
echo NVWB_API=%NVWB_API%
echo PROXY_PREFIX=%PROXY_PREFIX%
echo.
echo # Database/Cache
echo REDIS_URL=redis://localhost:6379
echo REDIS_MAX_CONNECTIONS=10
echo.
echo # Security
echo SECRET_KEY=%SECRET_KEY%
echo SESSION_TIMEOUT=3600
echo RATE_LIMIT_REQUESTS=1000
echo RATE_LIMIT_WINDOW=60
echo ALLOWED_DOMAINS=%ALLOWED_DOMAINS%
echo.
echo # Feature Flags
echo ENABLE_DEBUG_LOGGING=true
echo ENABLE_PERFORMANCE_MONITORING=true
echo ENABLE_SECURITY_HEADERS=true
echo.
echo # Development Settings
echo AUTO_RELOAD=true
echo DEVELOPMENT_MODE=true
echo MAINTENANCE_MODE=false
echo.
echo # NVIDIA Environment Flags
echo NVIDIA_ENVIRONMENT=true
echo INTERNAL_DEPLOYMENT=false
) > .env

echo ✅ Local development configuration saved to .env

REM Update variables.env for AI Workbench
echo.
echo 🔧 Updating AI Workbench variables.env...

(
echo.
echo # NVIDIA Integration Settings ^(added by setup script^)
echo NVWB_API=%NVWB_API%
echo PROXY_PREFIX=%PROXY_PREFIX%
echo SECRET_KEY=%SECRET_KEY%
echo ALLOWED_DOMAINS=%ALLOWED_DOMAINS%
echo NVIDIA_ENVIRONMENT=true
) >> variables.env

echo ✅ AI Workbench variables updated

echo.
echo 🎉 Environment setup complete!
echo.
echo 📋 Next steps:
echo 1. Review and customize the environment files if needed
echo 2. For production deployment, run: docker-compose up -d
echo 3. For Kubernetes deployment, run: kubectl apply -f deploy/kubernetes/
echo 4. Test the application: python -m streamlit run app/tutorial_app/streamlit_app.py
echo.
echo 🔗 Configuration Summary:
echo    - Environment: %ENVIRONMENT%
echo    - API Endpoint: %NVWB_API%
echo    - Proxy Prefix: %PROXY_PREFIX%
echo    - Secret Key: [HIDDEN]
echo    - Allowed Domains: %ALLOWED_DOMAINS%

pause
