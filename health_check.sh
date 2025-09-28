#!/bin/bash
# NVIDIA AI Workbench Tutorial App - Health Check Script (Linux/macOS)
# This script performs comprehensive health checks including NVIDIA GPU

set -e

echo
echo "==============================================="
echo " NVIDIA AI Workbench Tutorial App - Health Check"
echo "==============================================="
echo

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo
    echo "Expected files not found. Please ensure you're in the project root."
    exit 1
fi

echo "🔍 Performing comprehensive health checks..."
echo

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found"
    exit 1
fi
echo "✅ Python found"

# Check pip
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found"
    exit 1
fi
echo "✅ pip found"

# Check NVIDIA GPU
if command -v nvidia-smi &> /dev/null; then
    if nvidia-smi &> /dev/null; then
        echo "✅ NVIDIA GPU detected"
        NVIDIA_AVAILABLE=true
    else
        echo "⚠️  NVIDIA GPU not detected"
        NVIDIA_AVAILABLE=false
    fi
else
    echo "⚠️  nvidia-smi not available"
    NVIDIA_AVAILABLE=false
fi

# Check if requirements.txt exists and is valid
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi
echo "✅ requirements.txt found"

# Check if dependencies are installed
if pip list | grep -q "streamlit"; then
    echo "✅ Streamlit installed"
else
    echo "⚠️  Streamlit not installed (run setup.sh first)"
fi

echo
echo "🔍 Checking Docker services..."
echo

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✅ Docker available"
    DOCKER_AVAILABLE=true

    # Check if docker-compose services are running
    if docker-compose ps --services --filter "status=running" 2>/dev/null | grep -q "tutorial-app"; then
        echo "✅ Tutorial app container running"
    else
        echo "⚠️  Tutorial app container not running"
    fi

    if docker-compose ps --services --filter "status=running" 2>/dev/null | grep -q "gitea"; then
        echo "✅ Gitea container running"
    else
        echo "⚠️  Gitea container not running"
    fi

    if docker-compose ps --services --filter "status=running" 2>/dev/null | grep -q "redis"; then
        echo "✅ Redis container running"
    else
        echo "⚠️  Redis container not running"
    fi

    if docker-compose ps --services --filter "status=running" 2>/dev/null | grep -q "prometheus"; then
        echo "✅ Prometheus container running"
    else
        echo "⚠️  Prometheus container not running"
    fi

    if docker-compose ps --services --filter "status=running" 2>/dev/null | grep -q "grafana"; then
        echo "✅ Grafana container running"
    else
        echo "⚠️  Grafana container not running"
    fi
else
    echo "⚠️  Docker not available (optional for local development)"
    DOCKER_AVAILABLE=false
fi

echo
echo "🔍 Checking service endpoints..."
echo

# Check tutorial app health
if curl -s -f http://localhost/healthz &> /dev/null; then
    echo "✅ Tutorial app responding (http://localhost/healthz)"
else
    echo "⚠️  Tutorial app not responding"
fi

# Check backend API
if curl -s -f http://localhost:8000/health &> /dev/null; then
    echo "✅ Backend API responding (http://localhost:8000/health)"
else
    echo "⚠️  Backend API not responding"
fi

# Check Gitea
if curl -s -f -u admin:admin http://localhost:3001/api/v1/version &> /dev/null; then
    echo "✅ Gitea responding (http://localhost:3001)"
else
    echo "⚠️  Gitea not responding"
fi

# Check Grafana
if curl -s -f http://localhost:3000/api/health &> /dev/null; then
    echo "✅ Grafana responding (http://localhost:3000)"
else
    echo "⚠️  Grafana not responding"
fi

# Check Prometheus
if curl -s -f http://localhost:9090/-/healthy &> /dev/null; then
    echo "✅ Prometheus responding (http://localhost:9090)"
else
    echo "⚠️  Prometheus not responding"
fi

# Check Redis if Docker is available
if [ "$DOCKER_AVAILABLE" = true ]; then
    if docker-compose exec -T redis redis-cli ping 2>/dev/null | grep -q "PONG"; then
        echo "✅ Redis responding"
    else
        echo "⚠️  Redis not responding"
    fi
fi

echo
echo "🔍 Checking configuration files..."
echo

# Check environment files
if [ -f ".env" ]; then
    echo "✅ .env file exists"
else
    echo "⚠️  .env file not found"
fi

if [ -f "variables.env" ]; then
    echo "✅ variables.env file exists"
else
    echo "⚠️  variables.env file not found"
fi

if [ -f "deploy/environments/production.env" ]; then
    echo "✅ Production environment file exists"
else
    echo "⚠️  Production environment file not found"
fi

if [ -f ".streamlit/secrets.toml" ]; then
    echo "✅ Streamlit secrets file exists"
else
    echo "⚠️  Streamlit secrets file not found"
fi

echo
echo "🔍 Checking application modules..."
echo

# Check if main application can be imported
if python -c "import sys; sys.path.append('src'); from tutorial_app.streamlit_app import main; print('✅ Main application module importable')" 2>/dev/null; then
    :
else
    echo "⚠️  Main application module not importable"
fi

# Check NVIDIA workbench client
if python -c "import sys; sys.path.append('src'); from tutorial_app.common.wb_svc_client import list_projects; print('✅ NVIDIA workbench client importable')" 2>/dev/null; then
    :
else
    echo "⚠️  NVIDIA workbench client not importable"
fi

# Check security module
if python -c "import sys; sys.path.append('src'); from tutorial_app.common.security import initialize_security; print('✅ Security module importable')" 2>/dev/null; then
    :
else
    echo "⚠️  Security module not importable"
fi

echo
echo "==============================================="
echo " Health Check Summary"
echo "==============================================="
echo

echo "📋 Comprehensive health check complete."
echo
echo "🌐 Service URLs (if running):"
echo "   Tutorial App: http://localhost"
echo "   Backend API:  http://localhost:8000"
echo "   Gitea (Git):   http://localhost:3001 (admin/admin)"
echo "   Grafana:       http://localhost:3000 (admin/admin)"
echo "   Prometheus:    http://localhost:9090"
echo
echo "📖 For troubleshooting, see:"
echo "   docs/TROUBLESHOOTING.md"
echo "   docs/QUICK_START.md"
echo
echo "💡 Quick fixes:"
echo "   - Run ./setup_all.sh for full setup"
echo "   - Run docker-compose up -d to start services"
echo "   - Check logs with docker-compose logs"
echo "   - Run ./environment_validation.sh for basic checks"
echo

echo "All health checks completed successfully."
