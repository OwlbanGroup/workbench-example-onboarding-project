@echo off
REM NVIDIA AI Workbench Tutorial App - Production Deployment Script (Windows)
REM This script handles production deployment on Windows systems

setlocal enabledelayedexpansion

echo 🚀 NVIDIA AI Workbench Tutorial App - Production Deployment
echo ==========================================================

REM Configuration
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "ENVIRONMENT=production"
set "NAMESPACE=tutorial-prod"

REM Colors (using PowerShell for colored output)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

:log_info
powershell -command "Write-Host '%BLUE%[INFO]%NC% %~1' -ForegroundColor Blue"
goto :eof

:log_success
powershell -command "Write-Host '%GREEN%[SUCCESS]%NC% %~1' -ForegroundColor Green"
goto :eof

:log_warning
powershell -command "Write-Host '%YELLOW%[WARNING]%NC% %~1' -ForegroundColor Yellow"
goto :eof

:log_error
powershell -command "Write-Host '%RED%[ERROR]%NC% %~1' -ForegroundColor Red"
goto :eof

REM Check prerequisites
:check_prerequisites
call :log_info "Checking prerequisites..."

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker is not installed. Please install Docker Desktop first."
    goto :error
)

REM Check if kubectl is available (optional for Docker deployment)
kubectl version --client >nul 2>&1
if errorlevel 1 (
    call :log_warning "kubectl is not installed. Kubernetes deployment features will be limited."
) else (
    call :log_info "kubectl is available"
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    call :log_warning "docker-compose is not available. Using 'docker compose' instead."
    set "COMPOSE_CMD=docker compose"
) else (
    set "COMPOSE_CMD=docker-compose"
)

call :log_success "Prerequisites check passed"
goto :eof

REM Build Docker image
:build_image
call :log_info "Building Docker image..."

cd /d "%PROJECT_ROOT%"

REM Generate version tag
for /f "tokens=2 delims==" %%i in ('wmic os get localdatetime /value') do set datetime=%%i
set "TAG=%ENVIRONMENT%-%datetime:~0,8%-%datetime:~8,6%"

REM Build image
docker build -t tutorial-app:%TAG% .

REM Tag for registry if needed
if defined REGISTRY (
    docker tag tutorial-app:%TAG% %REGISTRY%/tutorial-app:%TAG%
)

call :log_success "Docker image built: tutorial-app:%TAG%"
goto :eof

REM Deploy with Docker Compose
:deploy_docker_compose
call :log_info "Deploying with Docker Compose..."

cd /d "%PROJECT_ROOT%"

REM Set production environment
set "ENVIRONMENT=production"

REM Start services
%COMPOSE_CMD% up -d

REM Wait for services to be ready
timeout /t 30 /nobreak >nul

call :log_success "Docker Compose deployment completed"
goto :eof

REM Deploy to Kubernetes (if available)
:deploy_kubernetes
call :log_info "Deploying to Kubernetes..."

REM Check if kubectl is available
kubectl version --client >nul 2>&1
if errorlevel 1 (
    call :log_warning "kubectl not available, skipping Kubernetes deployment"
    goto :eof
)

REM Create namespace if it doesn't exist
kubectl create namespace %NAMESPACE% --dry-run=client -o yaml | kubectl apply -f -

REM Apply Redis deployment first
kubectl apply -f deploy/kubernetes/redis.yml -n %NAMESPACE%

REM Wait for Redis to be ready
call :log_info "Waiting for Redis to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/redis -n %NAMESPACE%

REM Apply application deployment
kubectl apply -f deploy/kubernetes/deployment.yml -n %NAMESPACE%

REM Wait for application to be ready
call :log_info "Waiting for application to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/tutorial-app -n %NAMESPACE%

call :log_success "Kubernetes deployment completed"
goto :eof

REM Run health checks
:run_health_checks
call :log_info "Running health checks..."

REM For Docker Compose deployment
%COMPOSE_CMD% exec -T tutorial-app curl -f http://localhost:8501/healthz >nul 2>&1
if errorlevel 1 (
    call :log_error "Health check failed for Docker Compose deployment"
    goto :error
)

REM For Kubernetes deployment (if applicable)
kubectl get svc tutorial-app-service -n %NAMESPACE% >nul 2>&1
if not errorlevel 1 (
    REM Get service URL and check health
    for /f "tokens=*" %%i in ('kubectl get svc tutorial-app-service -n %NAMESPACE% -o jsonpath="{.spec.clusterIP}:{.spec.ports[0].port}"') do set SERVICE_URL=%%i
    powershell -command "try { Invoke-WebRequest -Uri 'http://%SERVICE_URL%/healthz' -TimeoutSec 10 | Out-Null; Write-Host 'Kubernetes health check passed' } catch { Write-Host 'Kubernetes health check failed' }"
)

call :log_success "Health checks passed"
goto :eof

REM Run smoke tests
:run_smoke_tests
call :log_info "Running smoke tests..."

REM Basic smoke tests for Docker Compose
%COMPOSE_CMD% exec -T tutorial-app python -c "import streamlit; print('Streamlit import successful')" >nul 2>&1
if errorlevel 1 (
    call :log_error "Smoke test failed: Streamlit import"
    goto :error
)

%COMPOSE_CMD% exec -T tutorial-app python -c "from src.tutorial_app.common.security import InputSanitizer; print('Security module loaded')" >nul 2>&1
if errorlevel 1 (
    call :log_error "Smoke test failed: Security module"
    goto :error
)

call :log_success "Smoke tests passed"
goto :eof

REM Setup monitoring
:setup_monitoring
call :log_info "Setting up monitoring..."

REM For Docker Compose, monitoring is included in docker-compose.yml
call :log_info "Monitoring services should be available at:"
call :log_info "  - Grafana: http://localhost:3000 (admin/admin)"
call :log_info "  - Prometheus: http://localhost:9090"

call :log_success "Monitoring setup completed"
goto :eof

REM Backup configuration
:backup_config
call :log_info "Creating configuration backup..."

set "BACKUP_DIR=%PROJECT_ROOT%\backups\%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%"
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Backup environment files
copy "deploy\environments\production.env" "%BACKUP_DIR%\" >nul
copy ".env" "%BACKUP_DIR%\" >nul 2>&1
copy "variables.env" "%BACKUP_DIR%\" >nul

call :log_success "Configuration backed up to %BACKUP_DIR%"
goto :eof

REM Main deployment function
:main
call :log_info "Starting production deployment to %ENVIRONMENT% environment"

REM Check prerequisites
call :check_prerequisites
if errorlevel 1 goto :error

REM Backup current configuration
call :backup_config

REM Build image
call :build_image
if errorlevel 1 goto :error

REM Deploy with Docker Compose (primary method for Windows)
call :deploy_docker_compose
if errorlevel 1 goto :error

REM Try Kubernetes deployment if requested
if "%DEPLOY_KUBERNETES%"=="true" (
    call :deploy_kubernetes
)

REM Setup monitoring
call :setup_monitoring

REM Run health checks
call :run_health_checks
if errorlevel 1 goto :error

REM Run smoke tests
call :run_smoke_tests
if errorlevel 1 goto :error

call :log_success "Production deployment to %ENVIRONMENT% completed successfully! 🎉"
call :log_info "Application is available at: http://localhost"
call :log_info "Grafana dashboard: http://localhost:3000 (admin/admin)"
goto :eof

:error
call :log_error "Deployment failed!"
exit /b 1

REM Help function
:help
echo NVIDIA AI Workbench Tutorial App - Production Deployment Script ^(Windows^)
echo.
echo USAGE:
echo     %0 [OPTIONS]
echo.
echo OPTIONS:
echo     -k, --kubernetes    Also deploy to Kubernetes cluster
echo     -r, --registry REG  Docker registry URL
echo     -n, --namespace NS  Kubernetes namespace [default: tutorial-prod]
echo     -h, --help          Show this help message
echo.
echo ENVIRONMENT VARIABLES:
echo     REGISTRY           Docker registry URL
echo     DEPLOY_KUBERNETES  Deploy to Kubernetes ^(true/false^) [default: false]
echo.
echo EXAMPLES:
echo     %0
echo     set DEPLOY_KUBERNETES=true ^& %0
echo     %0 --registry ghcr.io/myorg --namespace tutorial-prod
echo.
goto :eof

REM Parse arguments
set "DEPLOY_KUBERNETES=false"
set "REGISTRY="

if "%1"=="-h" goto help
if "%1"=="--help" goto help
if "%1"=="-k" set "DEPLOY_KUBERNETES=true" && shift
if "%1"=="--kubernetes" set "DEPLOY_KUBERNETES=true" && shift
if "%1"=="-r" set "REGISTRY=%2" && shift && shift
if "%1"=="--registry" set "REGISTRY=%2" && shift && shift
if "%1"=="-n" set "NAMESPACE=%2" && shift && shift
if "%1"=="--namespace" set "NAMESPACE=%2" && shift && shift

REM Run main deployment
call :main
goto :eof
