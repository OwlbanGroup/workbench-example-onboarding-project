@echo off
REM NVIDIA AI Workbench Tutorial App - Environment Setup Script (Windows)
REM This script configures the application for NVIDIA integration with error handling

setlocal enabledelayedexpansion

echo 🚀 Setting up NVIDIA AI Workbench Tutorial App Environment
echo ==========================================================

REM Check if we're in the right directory
if not exist "pyproject.toml" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check if deploy directory exists
if not exist "deploy\environments" (
    echo ❌ Error: deploy\environments directory not found
    echo Please ensure the project structure is complete.
    pause
    exit /b 1
)

echo 📋 Gathering configuration information...

REM NVIDIA Environment Configuration
set NVWB_API=https://api.nvidia-workbench.internal
set PROXY_PREFIX=/tutorial

REM Generate secret key with error handling
set SECRET_KEY=
echo Generating secure secret key...
powershell -command "$bytes = New-Object Byte[] 32; (New-Object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes); [System.Convert]::ToHexString($bytes).ToLower()" > temp_secret.txt 2>nul
if exist temp_secret.txt (
    set /p SECRET_KEY=<temp_secret.txt
    del temp_secret.txt
) else (
    echo ❌ Failed to generate secret key. Using fallback.
    set SECRET_KEY=fallback-secret-key-please-change-in-production
)

if "%SECRET_KEY%"=="" (
    echo ❌ Secret key generation failed completely.
    pause
    exit /b 1
)

set ALLOWED_DOMAINS=nvidia.com,developer.nvidia.com,forums.developer.nvidia.com

REM Environment selection with validation
set env_choice=3
if "%env_choice%"=="1" (
    set ENV_FILE=deploy\environments\development.env
    set ENVIRONMENT=development
) else if "%env_choice%"=="2" (
    set ENV_FILE=deploy\environments\staging.env
    set ENVIRONMENT=staging
    REM Create staging env if it doesn't exist
    if not exist "%ENV_FILE%" (
        if exist "deploy\environments\production.env" (
            copy "deploy\environments\production.env" "%ENV_FILE%" >nul
            echo Staging environment created from production template.
        ) else (
            echo ❌ Production environment template not found.
            pause
            exit /b 1
        )
    )
) else if "%env_choice%"=="3" (
    set ENV_FILE=deploy\environments\production.env
    set ENVIRONMENT=production
) else (
    echo ⚠️  Invalid choice. Using development.
    set ENV_FILE=deploy\environments\development.env
    set ENVIRONMENT=development
)

REM Ensure deploy/environments directory exists
if not exist "deploy\environments" mkdir "deploy\environments"

echo.
echo ⚙️  Configuring environment file: %ENV_FILE%

REM Create environment file with error handling
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

if %errorlevel% neq 0 (
    echo ❌ Failed to create environment file.
    pause
    exit /b 1
)

echo ✅ Environment configuration saved to %ENV_FILE%

REM Create .env for local development with backup
echo.
echo 🏠 Setting up local development environment...

if exist .env (
    copy .env .env.backup >nul 2>&1
    echo Existing .env backed up to .env.backup
)

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

if %errorlevel% neq 0 (
    echo ❌ Failed to create .env file.
    pause
    exit /b 1
)

echo ✅ Local development configuration saved to .env

REM Update variables.env for AI Workbench with backup
echo.
echo 🔧 Updating AI Workbench variables.env...

if exist variables.env (
    copy variables.env variables.env.backup >nul 2>&1
    echo Existing variables.env backed up to variables.env.backup
)

(
echo.
echo # NVIDIA Integration Settings ^(added by setup script^)
echo NVWB_API=%NVWB_API%
echo PROXY_PREFIX=%PROXY_PREFIX%
echo SECRET_KEY=%SECRET_KEY%
echo ALLOWED_DOMAINS=%ALLOWED_DOMAINS%
echo NVIDIA_ENVIRONMENT=true
) >> variables.env

if %errorlevel% neq 0 (
    echo ❌ Failed to update variables.env.
    pause
    exit /b 1
)

echo ✅ AI Workbench variables updated

REM Validate configuration
echo.
echo 🔍 Validating configuration files...

if exist "%ENV_FILE%" (
    echo ✅ %ENV_FILE% created successfully
) else (
    echo ❌ %ENV_FILE% not found after creation
    pause
    exit /b 1
)

if exist .env (
    echo ✅ .env created successfully
) else (
    echo ❌ .env not found after creation
    pause
    exit /b 1
)

echo.
echo 🎉 Environment setup complete!
echo.
echo 📋 Next steps:
echo 1. Review and customize the environment files if needed
echo 2. For production deployment, run: docker-compose up -d
echo 3. For Kubernetes deployment, run: kubectl apply -f deploy/kubernetes/
echo 4. Test the application: streamlit run src/tutorial_app/streamlit_app.py
echo.
echo 🔗 Configuration Summary:
echo    - Environment: %ENVIRONMENT%
echo    - API Endpoint: %NVWB_API%
echo    - Proxy Prefix: %PROXY_PREFIX%
echo    - Secret Key: [HIDDEN]
echo    - Allowed Domains: %ALLOWED_DOMAINS%
echo.

pause
endlocal
