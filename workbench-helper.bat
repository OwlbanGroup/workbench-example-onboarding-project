@echo off
REM NVIDIA AI Workbench Integration Helper Script
REM This script helps with local NVIDIA AI Workbench operations

setlocal enabledelayedexpansion

REM Check if workbench is available
where workbench >nul 2>1
if %errorlevel% neq 0 (
   echo NVIDIA AI Workbench CLI not found in PATH
   echo Please ensure NVIDIA AI Workbench is installed and CLI is in PATH
   pause
   exit /b 1
)

echo NVIDIA AI Workbench CLI found

REM Display available projects
echo Available projects:
workbench projects list

REM Check current project status
echo Current project status:
workbench status

echo.
echo Integration Commands:
echo   workbench run          - Start the application
echo   workbench stop          - Stop the application
echo   workbench logs          - View application logs
echo   workbench shell         - Open shell in container
echo   workbench test          - Run tests
echo.
pause
