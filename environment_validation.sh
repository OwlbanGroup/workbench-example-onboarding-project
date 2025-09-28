#!/bin/bash

# NVIDIA AI Workbench Tutorial App - Environment Validation Script (Linux/Mac)
# This script validates the environment setup and services

echo ""
echo "==============================================="
echo " NVIDIA AI Workbench Tutorial App - Environment Validation"
echo "==============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo ""
    echo "Expected files not found. Please ensure you're in the project root."
    exit 1
fi

echo "🔍 Validating environment setup..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found"
    VALIDATION_FAILED=true
else
    echo "✅ Python found"
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip not found"
    VALIDATION_FAILED=true
else
    echo "✅ pip found"
fi

# Check if requirements.txt exists and is valid
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    VALIDATION_FAILED=true
else
    echo "✅ requirements.txt found"
fi

# Check if dependencies are installed
if python3 -c "import streamlit" &> /dev/null; then
    echo "✅ Streamlit installed"
else
    echo "⚠️  Streamlit not installed (run setup.sh first)"
fi

echo ""
echo "🔍 Checking Docker services..."
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker not available (optional for local development)"
    DOCKER_AVAILABLE=false
else
    echo "✅ Docker available"
    DOCKER_AVAILABLE=true
fi

if [ "$DOCKER_AVAILABLE" = true ]; then
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
fi

echo ""
echo "🔍 Checking service endpoints..."
echo ""

# Check tutorial app health
if curl -s -f http://localhost/healthz &> /dev/null; then
    echo "✅ Tutorial app responding (http://localhost/healthz)"
else
    echo "⚠️  Tutorial app not responding"
fi

# Check Gitea
if curl -s -f -u admin:admin http://localhost:3001/api/v1/version &> /dev/null; then
    echo "✅ Gitea responding (http://localhost:3001)"
else
    echo "⚠️  Gitea not responding"
fi

# Check Redis if Docker is available
if [ "$DOCKER_AVAILABLE" = true ]; then
    if docker-compose exec -T redis redis-cli ping 2>/dev/null | grep -q "PONG"; then
        echo "✅ Redis responding"
    else
        echo "⚠️  Redis not responding"
    fi
fi

echo ""
echo "🔍 Checking configuration files..."
echo ""

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

echo ""
echo "🔍 Checking application modules..."
echo ""

# Check if main application can be imported
if python3 -c "import sys; sys.path.append('src'); from tutorial_app.streamlit_app import main; print('✅ Main application module importable')" 2>/dev/null; then
    :
else
    echo "⚠️  Main application module not importable"
fi

# Check NVIDIA workbench client
if python3 -c "import sys; sys.path.append('src'); from tutorial_app.common.wb_svc_client import list_projects; print('✅ NVIDIA workbench client importable')" 2>/dev/null; then
    :
else
    echo "⚠️  NVIDIA workbench client not importable"
fi

echo ""
echo "==============================================="
echo " Validation Summary"
echo "==============================================="
echo ""

echo "📋 Environment validation complete."
echo ""
echo "🌐 Service URLs (if running):"
echo "   Tutorial App: http://localhost"
echo "   Gitea (Git):   http://localhost:3001 (admin/admin)"
echo "   Grafana:       http://localhost:3000 (admin/admin)"
echo "   Prometheus:    http://localhost:9090"
echo ""
echo "📖 For detailed setup instructions, see:"
echo "   README.md"
echo "   docs/DEVELOPER_GUIDE.md"
echo ""
echo "💡 Quick fixes:"
echo "   - Run ./setup_all.sh for full setup"
echo "   - Run docker-compose up -d to start services"
echo "   - Check logs with docker-compose logs"
echo ""

if [ "$VALIDATION_FAILED" = true ]; then
    echo "❌ Validation failed. Please address the errors above."
    exit 1
fi
