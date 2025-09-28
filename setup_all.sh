#!/bin/bash

# NVIDIA AI Workbench Tutorial App - Master Setup Script (Linux/Mac)
# This script provides a menu to choose different setup configurations

set -e

echo ""
echo "==============================================="
echo " NVIDIA AI Workbench Tutorial App Setup"
echo "==============================================="
echo ""
echo "This script helps you set up the tutorial application"
echo "with different configurations and environments."
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo ""
    echo "Expected files not found. Please ensure you're in the project root."
    read -p "Press Enter to exit..."
    exit 1
fi

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8+ and try again."
    read -p "Press Enter to exit..."
    exit 1
fi
echo "✅ Python found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip not found. Please install pip and try again."
    read -p "Press Enter to exit..."
    exit 1
fi
echo "✅ pip found"

# Check git
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git and try again."
    read -p "Press Enter to exit..."
    exit 1
fi
echo "✅ Git found"

# Check Docker (optional)
if command -v docker &> /dev/null; then
    echo "✅ Docker found"
    DOCKER_AVAILABLE=true
else
    echo "⚠️  Docker not found (optional for local development)"
    DOCKER_AVAILABLE=false
fi

echo ""
echo "==============================================="
echo " Setup Options"
echo "==============================================="
echo ""
echo "1) Quick Setup (Basic dependencies only)"
echo "   - Install Python dependencies"
echo "   - Basic configuration"
echo ""
echo "2) Local Development Setup"
echo "   - Full local development environment"
echo "   - NVIDIA AI Workbench local integration"
echo "   - Helper scripts and documentation"
echo ""
echo "3) NVIDIA Integration Setup (Production)"
echo "   - Complete NVIDIA AI Workbench integration"
echo "   - Production-ready configuration"
echo "   - Environment-specific settings"
echo ""
echo "4) Docker Environment Setup"
echo "   - Docker Compose environment"
echo "   - Local Gitea server"
echo "   - Monitoring stack (Prometheus/Grafana)"
echo ""
echo "5) Run Tests"
echo "   - Execute all test suites"
echo "   - Performance and integration tests"
echo ""
echo "6) Environment Validation"
echo "   - Check all services and configurations"
echo "   - Health checks and diagnostics"
echo ""
echo "0) Exit"
echo ""
echo "==============================================="

while true; do
    read -p "Enter your choice (0-6): " choice

    case $choice in
        0)
            break
            ;;
        1)
            echo ""
            echo "==============================================="
            echo " Quick Setup"
            echo "==============================================="
            echo ""
            if [ -f "setup.bat" ]; then
                echo "Note: setup.bat is for Windows. For Linux, running pip install..."
                pip3 install -r requirements.txt
            else
                pip3 install -r requirements.txt
            fi
            if [ $? -eq 0 ]; then
                echo "✅ Quick setup completed successfully"
            else
                echo "❌ Quick setup failed"
                continue
            fi
            ;;
        2)
            echo ""
            echo "==============================================="
            echo " Local Development Setup"
            echo "==============================================="
            echo ""
            if [ -f "setup_local_nvidia_workbench_simple.bat" ]; then
                echo "Note: setup_local_nvidia_workbench_simple.bat is for Windows."
                echo "Running equivalent Linux setup..."
                # Run pip install and create .env.local if needed
                pip3 install -r requirements.txt
                if [ ! -f ".env.local" ]; then
                    echo "Creating .env.local for local development..."
                    cat > .env.local << 'EOF'
# Local NVIDIA AI Workbench Development Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# Application Settings
STREAMLIT_SERVER_HEADLESS=false
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_THEME_BASE=dark

# Local NVIDIA AI Workbench Integration
LOCAL_INTEGRATION=true
WORKBENCH_SOCKET_PATH=/tmp/nvidia-workbench.sock
WORKBENCH_API_URL=http://localhost:8080

# Database/Cache (Local)
REDIS_URL=redis://localhost:6379
REDIS_MAX_CONNECTIONS=10

# Security (Relaxed for Local Development)
SECRET_KEY=dev-secret-key-change-in-production
SESSION_TIMEOUT=3600
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=60
ALLOWED_DOMAINS=localhost,127.0.0.1

# Development Features
ENABLE_DEBUG_LOGGING=true
ENABLE_PERFORMANCE_MONITORING=true
ENABLE_SECURITY_HEADERS=false
AUTO_RELOAD=true
DEVELOPMENT_MODE=true
MAINTENANCE_MODE=false

# NVIDIA Environment Flags
NVIDIA_ENVIRONMENT=true
INTERNAL_DEPLOYMENT=false
ALLOW_LOCAL_CONNECTIONS=true
SKIP_SSL_VERIFICATION=true
EOF
                fi
            fi
            if [ $? -eq 0 ]; then
                echo "✅ Local development setup completed successfully"
            else
                echo "❌ Local development setup failed"
                continue
            fi
            ;;
        3)
            echo ""
            echo "==============================================="
            echo " NVIDIA Integration Setup"
            echo "==============================================="
            echo ""
            if [ -f "setup_nvidia_integration.sh" ]; then
                bash setup_nvidia_integration.sh
            else
                echo "setup_nvidia_integration.sh not found. Skipping."
            fi
            if [ $? -eq 0 ]; then
                echo "✅ NVIDIA integration setup completed successfully"
            else
                echo "❌ NVIDIA integration setup failed"
                continue
            fi
            ;;
        4)
            echo ""
            echo "==============================================="
            echo " Docker Environment Setup"
            echo "==============================================="
            echo ""
            if [ "$DOCKER_AVAILABLE" = false ]; then
                echo "❌ Docker is required for this setup but was not found."
                echo "Please install Docker and try again."
                continue
            fi

            echo "Starting Docker environment..."
            docker-compose up -d
            if [ $? -eq 0 ]; then
                echo "Waiting for services to be ready..."
                sleep 10
                echo "✅ Docker environment setup completed successfully"
                echo ""
                echo "🌐 Access URLs:"
                echo "   Tutorial App: http://localhost"
                echo "   Gitea (Git):   http://localhost:3001 (admin/admin)"
                echo "   Grafana:       http://localhost:3000 (admin/admin)"
                echo "   Prometheus:    http://localhost:9090"
            else
                echo "❌ Docker environment setup failed"
                continue
            fi
            ;;
        5)
            echo ""
            echo "==============================================="
            echo " Running Tests"
            echo "==============================================="
            echo ""
            python3 run_all_tests.py
            if [ $? -eq 0 ]; then
                echo "✅ All tests passed"
            else
                echo "❌ Some tests failed"
                continue
            fi
            ;;
        6)
            echo ""
            echo "==============================================="
            echo " Environment Validation"
            echo "==============================================="
            echo ""
            echo "🔍 Validating environment..."

            # Check if services are running
            if docker-compose ps &> /dev/null; then
                echo "✅ Docker services are running"
            else
                echo "⚠️  Docker services not running (run option 4 first)"
            fi

            # Check application health
            if curl -s http://localhost/healthz &> /dev/null; then
                echo "✅ Application is responding"
            else
                echo "⚠️  Application not responding"
            fi

            # Check Gitea
            if curl -s -u admin:admin http://localhost:3001/api/v1/version &> /dev/null; then
                echo "✅ Gitea is responding"
            else
                echo "⚠️  Gitea not responding"
            fi

            echo ""
            echo "📋 Validation complete. Check the output above for any issues."
            ;;
        *)
            echo ""
            echo "❌ Invalid choice. Please select 0-6."
            continue
            ;;
    esac

    echo ""
    echo "==============================================="
    echo " Setup Complete!"
    echo "==============================================="
    echo ""
    echo "What would you like to do next?"
    echo ""
    echo "1) Return to main menu"
    echo "2) Start the application"
    echo "3) Open documentation"
    echo "4) Exit"
    echo ""
    read -p "Enter your choice (1-4): " next_choice

    case $next_choice in
        1)
            continue
            ;;
        2)
            echo ""
            echo "🚀 Starting the application..."
            if [ -f "start-local.bat" ]; then
                echo "Note: start-local.bat is for Windows. Running streamlit directly..."
            fi
            streamlit run src/tutorial_app/streamlit_app.py --server.headless false --server.address localhost --server.port 8501
            exit 0
            ;;
        3)
            echo ""
            echo "📖 Opening documentation..."
            if command -v xdg-open &> /dev/null; then
                xdg-open README.md
                xdg-open docs/DEVELOPER_GUIDE.md
            elif command -v open &> /dev/null; then
                open README.md
                open docs/DEVELOPER_GUIDE.md
            else
                echo "Please open README.md and docs/DEVELOPER_GUIDE.md manually."
            fi
            exit 0
            ;;
        4)
            break
            ;;
        *)
            echo "Invalid choice. Returning to main menu."
            continue
            ;;
    esac
done

echo ""
echo "Thank you for using the NVIDIA AI Workbench Tutorial App setup!"
read -p "Press Enter to exit..."
