@echo off
REM NVIDIA AI Workbench Tutorial App Deployment Script (Windows)
REM This script handles deployment to different environments

setlocal enabledelayedexpansion

REM Configuration
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."
set "ENVIRONMENT=%1"
set "NAMESPACE=%2"

if "%ENVIRONMENT%"=="" set "ENVIRONMENT=development"
if "%NAMESPACE%"=="" set "NAMESPACE=default"

REM Colors for output (Windows CMD)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM Logging functions
:log_info
echo [94m[INFO][0m %~1
goto :eof

:log_success
echo [92m[SUCCESS][0m %~1
goto :eof

:log_warning
echo [93m[WARNING][0m %~1
goto :eof
