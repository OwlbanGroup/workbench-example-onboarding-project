#!/bin/bash

# NVIDIA AI Workbench Tutorial App - Environment Setup Script
# This script configures the application for NVIDIA integration

set -e

echo "🚀 Setting up NVIDIA AI Workbench Tutorial App Environment"
echo "========================================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to prompt for input with default
prompt_with_default() {
    local prompt="$1"
    local default="$2"
    local response

    read -p "$prompt [$default]: " response
    echo "${response:-$default}"
}

echo "📋 Gathering configuration information..."

# NVIDIA Environment Configuration
NVWB_API=$(prompt_with_default "NVIDIA AI Workbench API URL" "https://api.nvidia-workbench.internal")
PROXY_PREFIX=$(prompt_with_default "Reverse proxy prefix (e.g., /tutorial)" "/tutorial")
SECRET_KEY=$(prompt_with_default "Application secret key" "$(openssl rand -hex 32)")
ALLOWED_DOMAINS=$(prompt_with_default "Allowed domains (comma-separated)" "nvidia.com,developer.nvidia.com,forums.developer.nvidia.com")

# Environment selection
echo ""
echo "🌍 Select deployment environment:"
echo "1) Development"
echo "2) Staging"
echo "3) Production"
read -p "Enter choice (1-3): " env_choice

case $env_choice in
    1)
        ENV_FILE="deploy/environments/development.env"
        ENVIRONMENT="development"
        ;;
    2)
        ENV_FILE="deploy/environments/staging.env"
        ENVIRONMENT="staging"
        # Create staging env if it doesn't exist
        if [ ! -f "$ENV_FILE" ]; then
            cp deploy/environments/production.env "$ENV_FILE"
        fi
        ;;
    3)
        ENV_FILE="deploy/environments/production.env"
        ENVIRONMENT="production"
        ;;
    *)
        echo "❌ Invalid choice. Using development."
        ENV_FILE="deploy/environments/development.env"
        ENVIRONMENT="development"
        ;;
esac

echo ""
echo "⚙️  Configuring environment file: $ENV_FILE"

# Update environment file
cat > "$ENV_FILE" << EOF
# $ENVIRONMENT Environment Configuration for NVIDIA Integration
ENVIRONMENT=$ENVIRONMENT
DEBUG=false
LOG_LEVEL=INFO

# Application Settings
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_THEME_BASE=dark

# NVIDIA AI Workbench Integration
NVWB_API=$NVWB_API
PROXY_PREFIX=$PROXY_PREFIX

# Database/Cache
REDIS_URL=redis://redis-service:6379
REDIS_MAX_CONNECTIONS=50

# Security
SECRET_KEY=$SECRET_KEY
SESSION_TIMEOUT=1800
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
ALLOWED_DOMAINS=$ALLOWED_DOMAINS

# External Services
PROMETHEUS_URL=http://prometheus:9090
GRAFANA_URL=http://grafana:3000

# Feature Flags
ENABLE_DEBUG_LOGGING=false
ENABLE_PERFORMANCE_MONITORING=true
ENABLE_SECURITY_HEADERS=true

# SSL/TLS Settings
SSL_CERT_PATH=/etc/ssl/certs/tutorial-app.crt
SSL_KEY_PATH=/etc/ssl/private/tutorial-app.key
FORCE_SSL=true

# Monitoring
METRICS_ENABLED=true
HEALTH_CHECK_INTERVAL=30
LOG_TO_STDOUT=true

# Performance
MAX_WORKERS=4
WORKER_TIMEOUT=30
MAX_REQUESTS_PER_WORKER=1000

# NVIDIA-specific configuration
NVIDIA_ENVIRONMENT=true
INTERNAL_DEPLOYMENT=true
EOF

echo "✅ Environment configuration saved to $ENV_FILE"

# Create .env for local development
echo ""
echo "🏠 Setting up local development environment..."
cp .env .env.backup 2>/dev/null || true

cat > .env << EOF
# Local Development Environment Configuration
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# Application Settings
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_THEME_BASE=dark

# NVIDIA AI Workbench Integration
NVWB_API=$NVWB_API
PROXY_PREFIX=$PROXY_PREFIX

# Database/Cache
REDIS_URL=redis://localhost:6379
REDIS_MAX_CONNECTIONS=10

# Security
SECRET_KEY=$SECRET_KEY
SESSION_TIMEOUT=3600
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=60
ALLOWED_DOMAINS=$ALLOWED_DOMAINS

# Feature Flags
ENABLE_DEBUG_LOGGING=true
ENABLE_PERFORMANCE_MONITORING=true
ENABLE_SECURITY_HEADERS=true

# Development Settings
AUTO_RELOAD=true
DEVELOPMENT_MODE=true
MAINTENANCE_MODE=false

# NVIDIA Environment Flags
NVIDIA_ENVIRONMENT=true
INTERNAL_DEPLOYMENT=false
EOF

echo "✅ Local development configuration saved to .env"

# Update variables.env for AI Workbench
echo ""
echo "🔧 Updating AI Workbench variables.env..."
cat >> variables.env << EOF

# NVIDIA Integration Settings (added by setup script)
NVWB_API=$NVWB_API
PROXY_PREFIX=$PROXY_PREFIX
SECRET_KEY=$SECRET_KEY
ALLOWED_DOMAINS=$ALLOWED_DOMAINS
NVIDIA_ENVIRONMENT=true
EOF

echo "✅ AI Workbench variables updated"

echo ""
echo "🎉 Environment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Review and customize the environment files if needed"
echo "2. For production deployment, run: docker-compose up -d"
echo "3. For Kubernetes deployment, run: kubectl apply -f deploy/kubernetes/"
echo "4. Test the application: python -m streamlit run app/tutorial_app/streamlit_app.py"
echo ""
echo "🔗 Configuration Summary:"
echo "   - Environment: $ENVIRONMENT"
echo "   - API Endpoint: $NVWB_API"
echo "   - Proxy Prefix: $PROXY_PREFIX"
echo "   - Secret Key: [HIDDEN]"
echo "   - Allowed Domains: $ALLOWED_DOMAINS"
