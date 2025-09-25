#!/bin/bash

# NVIDIA AI Workbench Tutorial App - Production Deployment Script (Linux)
# This script handles production deployment on Linux systems

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENVIRONMENT=${ENVIRONMENT:-production}
NAMESPACE=${NAMESPACE:-tutorial-prod}
DEPLOY_KUBERNETES=${DEPLOY_KUBERNETES:-false}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    # Check if docker-compose is available
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    elif docker compose version &> /dev/null; then
        COMPOSE_CMD="docker compose"
    else
        log_error "docker-compose is not available. Please install docker-compose."
        exit 1
    fi

    # Check if kubectl is available (optional for Kubernetes deployment)
    if command -v kubectl &> /dev/null; then
        log_info "kubectl is available"
    else
        if [ "$DEPLOY_KUBERNETES" = "true" ]; then
            log_error "kubectl is required for Kubernetes deployment but not found."
            exit 1
        else
            log_warning "kubectl is not available. Kubernetes deployment features will be limited."
        fi
    fi

    log_success "Prerequisites check passed"
}

# Build Docker image
build_image() {
    log_info "Building Docker image..."

    cd "$PROJECT_ROOT"

    # Generate version tag
    TAG="$ENVIRONMENT-$(date +%Y%m%d-%H%M%S)"

    # Build image
    docker build -t tutorial-app:$TAG .

    # Tag for registry if needed
    if [ -n "$REGISTRY" ]; then
        docker tag tutorial-app:$TAG $REGISTRY/tutorial-app:$TAG
        log_info "Tagged image for registry: $REGISTRY/tutorial-app:$TAG"
    fi

    log_success "Docker image built: tutorial-app:$TAG"
    echo "TAG=$TAG" >> $GITHUB_ENV 2>/dev/null || true
}

# Deploy with Docker Compose
deploy_docker_compose() {
    log_info "Deploying with Docker Compose..."

    cd "$PROJECT_ROOT"

    # Set production environment
    export ENVIRONMENT=production

    # Start services
    $COMPOSE_CMD up -d

    # Wait for services to be ready
    log_info "Waiting for services to start..."
    sleep 30

    log_success "Docker Compose deployment completed"
}

# Deploy to Kubernetes
deploy_kubernetes() {
    if [ "$DEPLOY_KUBERNETES" != "true" ]; then
        return 0
    fi

    log_info "Deploying to Kubernetes..."

    # Create namespace if it doesn't exist
    kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

    # Apply Redis deployment first
    kubectl apply -f deploy/kubernetes/redis.yml -n $NAMESPACE

    # Wait for Redis to be ready
    log_info "Waiting for Redis to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/redis -n $NAMESPACE

    # Apply application deployment
    kubectl apply -f deploy/kubernetes/deployment.yml -n $NAMESPACE

    # Wait for application to be ready
    log_info "Waiting for application to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/tutorial-app -n $NAMESPACE

    log_success "Kubernetes deployment completed"
}

# Setup monitoring stack
setup_monitoring() {
    log_info "Setting up monitoring stack..."

    # For Docker Compose, monitoring services are included
    log_info "Monitoring services available at:"
    log_info "  - Grafana: http://localhost:3000 (admin/admin)"
    log_info "  - Prometheus: http://localhost:9090"

    # For Kubernetes, apply monitoring configurations
    if [ "$DEPLOY_KUBERNETES" = "true" ]; then
        kubectl apply -f deploy/kubernetes/monitoring.yml -n $NAMESPACE 2>/dev/null || true
        log_info "Kubernetes monitoring configurations applied"
    fi

    log_success "Monitoring setup completed"
}

# Run health checks
run_health_checks() {
    log_info "Running health checks..."

    # For Docker Compose deployment
    if $COMPOSE_CMD exec -T tutorial-app curl -f http://localhost:8501/healthz &>/dev/null; then
        log_success "Docker Compose health check passed"
    else
        log_error "Docker Compose health check failed"
        return 1
    fi

    # For Kubernetes deployment
    if [ "$DEPLOY_KUBERNETES" = "true" ]; then
        SERVICE_URL=$(kubectl get svc tutorial-app-service -n $NAMESPACE -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}' 2>/dev/null)
        if [ -n "$SERVICE_URL" ]; then
            if curl -f http://$SERVICE_URL/healthz &>/dev/null; then
                log_success "Kubernetes health check passed"
            else
                log_warning "Kubernetes health check failed - service may not be fully ready"
            fi
        fi
    fi
}

# Run smoke tests
run_smoke_tests() {
    log_info "Running smoke tests..."

    # Test Streamlit import
    if $COMPOSE_CMD exec -T tutorial-app python -c "import streamlit; print('Streamlit import successful')" &>/dev/null; then
        log_success "Streamlit smoke test passed"
    else
        log_error "Streamlit smoke test failed"
        return 1
    fi

    # Test security module
    if $COMPOSE_CMD exec -T tutorial-app python -c "from src.tutorial_app.common.security import InputSanitizer; print('Security module loaded')" &>/dev/null; then
        log_success "Security module smoke test passed"
    else
        log_error "Security module smoke test failed"
        return 1
    fi

    # Test NVIDIA integration
    if $COMPOSE_CMD exec -T tutorial-app python -c "from src.tutorial_app.common.wb_svc_client import list_projects; print('NVIDIA integration loaded')" &>/dev/null; then
        log_success "NVIDIA integration smoke test passed"
    else
        log_warning "NVIDIA integration smoke test failed - may not be configured"
    fi
}

# Backup configuration
backup_config() {
    log_info "Creating configuration backup..."

    BACKUP_DIR="$PROJECT_ROOT/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"

    # Backup environment files
    cp deploy/environments/production.env "$BACKUP_DIR/" 2>/dev/null || true
    cp .env "$BACKUP_DIR/" 2>/dev/null || true
    cp variables.env "$BACKUP_DIR/" 2>/dev/null || true

    log_success "Configuration backed up to $BACKUP_DIR"
}

# Generate deployment report
generate_report() {
    log_info "Generating deployment report..."

    REPORT_FILE="$PROJECT_ROOT/deployment_report_$(date +%Y%m%d_%H%M%S).txt"

    cat > "$REPORT_FILE" << EOF
NVIDIA AI Workbench Tutorial App - Deployment Report
==================================================

Deployment Time: $(date)
Environment: $ENVIRONMENT
Namespace: $NAMESPACE
Kubernetes Deployment: $DEPLOY_KUBERNETES

Application URLs:
- Main Application: http://localhost (Docker) / http://$(kubectl get svc tutorial-app-service -n $NAMESPACE -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}' 2>/dev/null || echo 'N/A') (Kubernetes)
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

Environment Configuration:
$(cat deploy/environments/production.env 2>/dev/null || echo "No production.env found")

Deployment Status: SUCCESS ✅

Next Steps:
1. Verify application functionality
2. Configure domain and SSL certificates
3. Set up automated backups
4. Configure alerting and monitoring
5. Test user workflows

For support, see docs/DEVELOPER_GUIDE.md or create an issue on GitHub.
EOF

    log_success "Deployment report generated: $REPORT_FILE"
}

# Rollback function
rollback() {
    log_warning "Rolling back deployment..."

    # Stop Docker Compose services
    cd "$PROJECT_ROOT"
    $COMPOSE_CMD down 2>/dev/null || true

    # Rollback Kubernetes deployment
    if [ "$DEPLOY_KUBERNETES" = "true" ]; then
        kubectl rollout undo deployment/tutorial-app -n $NAMESPACE 2>/dev/null || true
        kubectl wait --for=condition=available --timeout=300s deployment/tutorial-app -n $NAMESPACE 2>/dev/null || true
    fi

    log_success "Rollback completed"
}

# Cleanup function
cleanup() {
    log_info "Cleaning up temporary files..."

    # Remove dangling Docker images
    docker image prune -f >/dev/null 2>&1 || true

    log_success "Cleanup completed"
}

# Main deployment function
main() {
    log_info "Starting production deployment to $ENVIRONMENT environment"

    # Trap for cleanup on error
    trap 'log_error "Deployment failed!"; cleanup; rollback' ERR

    # Backup current configuration
    backup_config

    # Check prerequisites
    check_prerequisites

    # Build image
    build_image

    # Deploy with Docker Compose (primary method)
    deploy_docker_compose

    # Deploy to Kubernetes if requested
    deploy_kubernetes

    # Setup monitoring
    setup_monitoring

    # Run health checks
    if ! run_health_checks; then
        log_error "Health checks failed"
        rollback
        exit 1
    fi

    # Run smoke tests
    if ! run_smoke_tests; then
        log_error "Smoke tests failed"
        rollback
        exit 1
    fi

    # Generate deployment report
    generate_report

    # Cleanup
    cleanup

    log_success "Production deployment to $ENVIRONMENT completed successfully! 🎉"
    echo ""
    echo "Application URLs:"
    echo "  - Main App: http://localhost"
    if [ "$DEPLOY_KUBERNETES" = "true" ]; then
        SERVICE_IP=$(kubectl get svc tutorial-app-service -n $NAMESPACE -o jsonpath='{.spec.clusterIP}' 2>/dev/null)
        SERVICE_PORT=$(kubectl get svc tutorial-app-service -n $NAMESPACE -o jsonpath='{.spec.ports[0].port}' 2>/dev/null)
        echo "  - Kubernetes: http://$SERVICE_IP:$SERVICE_PORT"
    fi
    echo "  - Grafana: http://localhost:3000 (admin/admin)"
    echo "  - Prometheus: http://localhost:9090"
    echo ""
    echo "See deployment_report_*.txt for detailed information."
}

# Help function
show_help() {
    cat << EOF
NVIDIA AI Workbench Tutorial App - Production Deployment Script (Linux)

USAGE:
    $0 [OPTIONS]

OPTIONS:
    -k, --kubernetes    Deploy to Kubernetes cluster
    -r, --registry REG  Docker registry URL
    -n, --namespace NS  Kubernetes namespace [default: tutorial-prod]
    -e, --environment ENV Deployment environment [default: production]
    -h, --help          Show this help message

ENVIRONMENT VARIABLES:
    REGISTRY           Docker registry URL
    DEPLOY_KUBERNETES  Deploy to Kubernetes (true/false) [default: false]
    ENVIRONMENT        Deployment environment [default: production]
    NAMESPACE          Kubernetes namespace [default: tutorial-prod]

EXAMPLES:
    $0
    DEPLOY_KUBERNETES=true $0
    $0 --registry ghcr.io/myorg --namespace tutorial-prod
    $0 --environment staging --kubernetes

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -k|--kubernetes)
            DEPLOY_KUBERNETES=true
            shift
            ;;
        -r|--registry)
            REGISTRY="$2"
            shift 2
            ;;
        -n|--namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Run main deployment
main "$@"
