#!/bin/bash

# NVIDIA AI Workbench Tutorial App Deployment Script
# This script handles deployment to different environments

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENVIRONMENT=${1:-development}
NAMESPACE=${2:-default}

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

    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed. Please install it first."
        exit 1
    fi

    # Check if docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "docker is not installed. Please install it first."
        exit 1
    fi

    # Check if helm is installed (optional)
    if command -v helm &> /dev/null; then
        log_info "Helm is available"
    else
        log_warning "Helm is not installed. Some features may not be available."
    fi

    log_success "Prerequisites check passed"
}

# Build Docker image
build_image() {
    log_info "Building Docker image..."

    cd "$PROJECT_ROOT"

    # Generate version tag
    if [ "$ENVIRONMENT" = "production" ]; then
        TAG="latest"
    else
        TAG="$ENVIRONMENT-$(date +%Y%m%d-%H%M%S)"
    fi

    # Build image
    docker build -t tutorial-app:$TAG .

    # Tag for registry if needed
    if [ -n "$REGISTRY" ]; then
        docker tag tutorial-app:$TAG $REGISTRY/tutorial-app:$TAG
    fi

    log_success "Docker image built: tutorial-app:$TAG"
    echo "TAG=$TAG" >> $GITHUB_ENV
}

# Deploy to Kubernetes
deploy_kubernetes() {
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

# Deploy monitoring stack
deploy_monitoring() {
    log_info "Deploying monitoring stack..."

    # Apply Prometheus and Grafana configurations
    kubectl apply -f deploy/kubernetes/monitoring.yml -n $NAMESPACE

    log_success "Monitoring stack deployed"
}

# Run health checks
run_health_checks() {
    log_info "Running health checks..."

    # Get service URL
    SERVICE_URL=$(kubectl get svc tutorial-app-service -n $NAMESPACE -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}')

    # Wait for service to be ready
    max_attempts=30
    attempt=1

    while [ $attempt -le $max_attempts ]; do
        if curl -f http://$SERVICE_URL/healthz &>/dev/null; then
            log_success "Health check passed"
            return 0
        fi

        log_info "Health check attempt $attempt/$max_attempts failed, retrying..."
        sleep 10
        ((attempt++))
    done

    log_error "Health check failed after $max_attempts attempts"
    return 1
}

# Run smoke tests
run_smoke_tests() {
    log_info "Running smoke tests..."

    # Get service URL
    SERVICE_URL=$(kubectl get svc tutorial-app-service -n $NAMESPACE -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}')

    # Basic smoke tests
    if curl -f http://$SERVICE_URL/healthz &>/dev/null; then
        log_success "Smoke tests passed"
    else
        log_error "Smoke tests failed"
        return 1
    fi
}

# Rollback function
rollback() {
    log_warning "Rolling back deployment..."

    # Rollback to previous version
    kubectl rollout undo deployment/tutorial-app -n $NAMESPACE

    # Wait for rollback to complete
    kubectl wait --for=condition=available --timeout=300s deployment/tutorial-app -n $NAMESPACE

    log_success "Rollback completed"
}

# Main deployment function
main() {
    log_info "Starting deployment to $ENVIRONMENT environment in namespace $NAMESPACE"

    # Check prerequisites
    check_prerequisites

    # Build image
    build_image

    # Deploy to Kubernetes
    if deploy_kubernetes; then
        log_success "Kubernetes deployment successful"
    else
        log_error "Kubernetes deployment failed"
        exit 1
    fi

    # Deploy monitoring (optional)
    if [ "$DEPLOY_MONITORING" = "true" ]; then
        deploy_monitoring
    fi

    # Run health checks
    if run_health_checks; then
        log_success "Health checks passed"
    else
        log_error "Health checks failed"
        rollback
        exit 1
    fi

    # Run smoke tests
    if run_smoke_tests; then
        log_success "Smoke tests passed"
    else
        log_error "Smoke tests failed"
        rollback
        exit 1
    fi

    log_success "Deployment to $ENVIRONMENT completed successfully! 🎉"
    log_info "Application is available at: http://$(kubectl get svc tutorial-app-service -n $NAMESPACE -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}')"
}

# Help function
show_help() {
    cat << EOF
NVIDIA AI Workbench Tutorial App Deployment Script

USAGE:
    $0 [ENVIRONMENT] [NAMESPACE]

ARGUMENTS:
    ENVIRONMENT    Target environment (development, staging, production) [default: development]
    NAMESPACE      Kubernetes namespace [default: default]

ENVIRONMENT VARIABLES:
    REGISTRY           Docker registry URL
    DEPLOY_MONITORING  Deploy monitoring stack (true/false) [default: false]

EXAMPLES:
    $0 development
    $0 staging tutorial-staging
    REGISTRY=ghcr.io/myorg DEPLOY_MONITORING=true $0 production tutorial-prod

EOF
}

# Parse arguments
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
