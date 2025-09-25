# Deployment Guide

This guide provides comprehensive instructions for deploying the NVIDIA AI Workbench tutorial application across different environments and platforms.

## Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [CI/CD Pipeline](#ci-cd-pipeline)
- [Environment Configuration](#environment-configuration)
- [Monitoring & Observability](#monitoring--observability)
- [Backup & Recovery](#backup--recovery)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Local Development with Docker Compose

```bash
# Clone the repository
git clone <repository-url>
cd workbench-example-onboarding-project

# Start all services
docker-compose up -d

# Access the application
open http://localhost

# View monitoring
open http://localhost:3000  # Grafana (admin/admin)
open http://localhost:9090  # Prometheus
```

### Production Deployment

```bash
# Set environment variables
export ENVIRONMENT=production
export SECRET_KEY="your-secure-secret-key"

# Run deployment script
./deploy/scripts/deploy.sh production tutorial-prod
```

## Prerequisites

### System Requirements

- **Docker**: 20.10+ with Docker Compose
- **Kubernetes**: 1.24+ (for production deployment)
- **kubectl**: Configured for your cluster
- **Helm**: 3.0+ (optional, for advanced deployments)

### Network Requirements

- **Inbound**: TCP 80/443 (HTTP/HTTPS), TCP 8501 (Streamlit)
- **Outbound**: Access to external APIs, Redis, monitoring services

### Security Requirements

- **SSL/TLS certificates** for production
- **Secret management** system (Kubernetes secrets, AWS Secrets Manager, etc.)
- **Network policies** for pod-to-pod communication

## Local Development

### Docker Compose Setup

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd workbench-example-onboarding-project
   ```

2. **Create environment file:**
   ```bash
   cp deploy/environments/development.env .env
   # Edit .env with your local configuration
   ```

3. **Start services:**
   ```bash
   docker-compose up -d
   ```

4. **Verify deployment:**
   ```bash
   docker-compose ps
   curl http://localhost/healthz
   ```

### Development Workflow

```bash
# View logs
docker-compose logs -f tutorial-app

# Restart service
docker-compose restart tutorial-app

# Run tests
docker-compose exec tutorial-app python run_all_tests.py

# Stop services
docker-compose down
```

## Docker Deployment

### Building Custom Image

```bash
# Build image
docker build -t tutorial-app:latest .

# Run container
docker run -d \
  --name tutorial-app \
  -p 8501:8501 \
  -e ENVIRONMENT=production \
  tutorial-app:latest
```

### Multi-stage Build

The Dockerfile uses multi-stage builds for optimization:

```dockerfile
# Build stage
FROM python:3.11-slim as builder
# ... build dependencies

# Production stage
FROM python:3.11-slim as production
# ... copy built artifacts
```

### Image Optimization

- **Base image**: `python:3.11-slim` for minimal size
- **Multi-stage builds**: Separate build and runtime stages
- **Layer caching**: Dependencies installed before code copy
- **Security scanning**: Integrated with CI/CD pipeline

## Kubernetes Deployment

### Cluster Setup

1. **Create namespace:**
   ```bash
   kubectl create namespace tutorial-app
   ```

2. **Apply configurations:**
   ```bash
   kubectl apply -f deploy/kubernetes/ -n tutorial-app
   ```

3. **Verify deployment:**
   ```bash
   kubectl get pods -n tutorial-app
   kubectl get services -n tutorial-app
   ```

### Scaling

```bash
# Scale application
kubectl scale deployment tutorial-app --replicas=5 -n tutorial-app

# Auto-scaling (requires Metrics Server)
kubectl autoscale deployment tutorial-app \
  --cpu-percent=70 \
  --min=3 \
  --max=10 \
  -n tutorial-app
```

### Rolling Updates

```bash
# Update image
kubectl set image deployment/tutorial-app \
  tutorial-app=tutorial-app:v2.0.0 -n tutorial-app

# Check rollout status
kubectl rollout status deployment/tutorial-app -n tutorial-app

# Rollback if needed
kubectl rollout undo deployment/tutorial-app -n tutorial-app
```

## CI/CD Pipeline

### GitHub Actions Workflow

The CI/CD pipeline includes:

1. **Testing**: Unit tests, integration tests, security scanning
2. **Building**: Docker image build and push to registry
3. **Deployment**: Automated deployment to staging/production
4. **Monitoring**: Performance and E2E testing

### Pipeline Stages

```yaml
# .github/workflows/ci-cd.yml
- test: Run comprehensive test suite
- security-scan: Vulnerability scanning with Trivy
- build-and-push: Docker image build and registry push
- deploy-staging: Deploy to staging environment
- deploy-production: Deploy to production environment
- performance-test: Load testing against staging
- e2e-test: End-to-end testing
```

### Manual Deployment

#### Production Deployment Scripts

**Windows:**
```batch
# Basic production deployment
deploy\scripts\deploy_production.bat

# With Kubernetes deployment
set DEPLOY_KUBERNETES=true
deploy\scripts\deploy_production.bat

# With custom registry
set REGISTRY=ghcr.io/myorg
deploy\scripts\deploy_production.bat
```

**Linux:**
```bash
# Basic production deployment
./deploy/scripts/deploy_production.sh

# With Kubernetes deployment
./deploy/scripts/deploy_production.sh --kubernetes

# With custom registry and namespace
./deploy/scripts/deploy_production.sh --registry ghcr.io/myorg --namespace tutorial-prod
```

#### Legacy Deployment Script

```bash
# Deploy to specific environment
./deploy/scripts/deploy.sh production tutorial-prod

# With custom registry
REGISTRY=ghcr.io/myorg ./deploy/scripts/deploy.sh staging tutorial-staging
```

## Environment Configuration

### Configuration Files

- **`deploy/environments/development.env`**: Development settings
- **`deploy/environments/production.env`**: Production settings
- **`.env`**: Local environment overrides

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Deployment environment | `development` |
| `SECRET_KEY` | Application secret key | *Required in production* |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379` |
| `RATE_LIMIT_REQUESTS` | Rate limit per window | `100` |
| `SSL_CERT_PATH` | SSL certificate path | `/etc/ssl/certs/` |

### Secret Management

```bash
# Create Kubernetes secret
kubectl create secret generic tutorial-app-secrets \
  --from-literal=secret-key="your-secret-key" \
  --from-literal=database-url="postgresql://..." \
  -n tutorial-app
```

## Monitoring & Observability

### Prometheus Metrics

The application exposes metrics at `/metrics`:

- **HTTP request metrics**: Response times, status codes
- **Application metrics**: Active users, page views
- **System metrics**: CPU, memory, disk usage

### Grafana Dashboards

Pre-configured dashboards include:

- **Application Performance**: Response times, throughput
- **System Resources**: CPU, memory, network
- **Error Rates**: HTTP errors, application exceptions
- **User Activity**: Active sessions, page views

### Logging

```bash
# View application logs
kubectl logs -f deployment/tutorial-app -n tutorial-app

# View nginx logs
kubectl logs -f deployment/nginx -n tutorial-app

# Centralized logging with fluentd
kubectl apply -f deploy/kubernetes/logging.yml
```

### Alerting

Configure alerts for:

- **High error rates**: >5% error rate for 5 minutes
- **High response times**: >2s average response time
- **Resource exhaustion**: >90% CPU/memory usage
- **Service downtime**: Service unavailable for >1 minute

## Backup & Recovery

### Data Backup

```bash
# Backup Redis data
kubectl exec -it redis-pod -n tutorial-app -- redis-cli save

# Backup persistent volumes
kubectl cp tutorial-app/redis-data:/data/dump.rdb ./backups/redis-$(date +%Y%m%d).rdb
```

### Automated Backups

```bash
# Schedule daily backups
kubectl create cronjob backup-tutorial-app \
  --schedule="0 2 * * *" \
  --command="/bin/bash /scripts/backup.sh" \
  --image=tutorial-app:latest
```

### Disaster Recovery

1. **Scale down application:**
   ```bash
   kubectl scale deployment tutorial-app --replicas=0 -n tutorial-app
   ```

2. **Restore from backup:**
   ```bash
   kubectl cp ./backups/redis-20231201.rdb tutorial-app/redis-data:/data/dump.rdb
   ```

3. **Scale up application:**
   ```bash
   kubectl scale deployment tutorial-app --replicas=3 -n tutorial-app
   ```

## Troubleshooting

### Common Issues

#### Application Won't Start

```bash
# Check pod status
kubectl describe pod tutorial-app-pod -n tutorial-app

# Check logs
kubectl logs tutorial-app-pod -n tutorial-app

# Check resource usage
kubectl top pods -n tutorial-app
```

#### High Memory Usage

```bash
# Check memory limits
kubectl describe deployment tutorial-app -n tutorial-app

# Adjust resource limits
kubectl patch deployment tutorial-app \
  --type='json' \
  -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/resources/limits/memory", "value": "1Gi"}]' \
  -n tutorial-app
```

#### Database Connection Issues

```bash
# Check Redis connectivity
kubectl exec -it tutorial-app-pod -n tutorial-app -- redis-cli ping

# Check Redis logs
kubectl logs redis-pod -n tutorial-app
```

### Debug Mode

Enable debug logging:

```bash
# Set debug environment variable
kubectl set env deployment/tutorial-app LOG_LEVEL=DEBUG -n tutorial-app

# Restart deployment
kubectl rollout restart deployment/tutorial-app -n tutorial-app
```

### Health Checks

```bash
# Manual health check
curl http://tutorial-app-service:8501/healthz

# Check Kubernetes health
kubectl get endpoints tutorial-app-service -n tutorial-app
```

## Security Considerations

### Network Security

- **Network Policies**: Restrict pod-to-pod communication
- **Service Mesh**: Implement Istio or Linkerd
- **Firewall Rules**: Configure cloud firewall rules

### Access Control

- **RBAC**: Configure Kubernetes RBAC
- **API Gateway**: Implement authentication/authorization
- **Secret Rotation**: Regular secret rotation policies

### Compliance

- **Data Encryption**: Encrypt data at rest and in transit
- **Audit Logging**: Enable comprehensive audit logs
- **Vulnerability Scanning**: Regular security scans

## Performance Tuning

### Application Optimization

```python
# Enable caching
from common.caching import CacheManager
cache = CacheManager()

# Optimize database queries
from common.database import optimize_query
results = optimize_query("SELECT * FROM users WHERE active = ?", True)
```

### Infrastructure Scaling

```bash
# Horizontal Pod Autoscaler
kubectl autoscale deployment tutorial-app \
  --cpu-percent=70 \
  --min=3 \
  --max=10 \
  -n tutorial-app

# Cluster Autoscaler (for cloud providers)
# Automatically scales node pool based on demand
```

### CDN Integration

For global deployments, integrate with CDN:

```nginx
# nginx.conf
location /static/ {
    proxy_pass https://cdn.example.com;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Support

### Getting Help

1. **Check logs**: `kubectl logs deployment/tutorial-app -n tutorial-app`
2. **Review documentation**: `docs/` directory
3. **Check GitHub Issues**: Report bugs and request features
4. **Community Support**: NVIDIA Developer Forums

### Emergency Contacts

- **Production Issues**: On-call engineer rotation
- **Security Incidents**: security@nvidia.com
- **Infrastructure Issues**: DevOps team

---

## Deployment Checklist

- [ ] Environment configuration completed
- [ ] Secrets and certificates configured
- [ ] DNS records updated
- [ ] SSL/TLS certificates installed
- [ ] Monitoring and alerting configured
- [ ] Backup strategy implemented
- [ ] Security policies applied
- [ ] Performance baselines established
- [ ] Rollback plan documented
- [ ] Team notified of deployment

**Happy Deploying! 🚀**
