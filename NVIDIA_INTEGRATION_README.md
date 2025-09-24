# NVIDIA AI Workbench Tutorial App - Integration Guide

This guide provides instructions for integrating the NVIDIA AI Workbench Tutorial Application into NVIDIA's infrastructure and deployment pipelines.

## 🚀 Quick Start

### Automated Setup (Recommended)

**Windows:**
```batch
setup_nvidia_integration.bat
```

**Linux/macOS:**
```bash
chmod +x setup_nvidia_integration.sh
./setup_nvidia_integration.sh
```

### Manual Setup

1. Copy environment template:
   ```bash
   cp deploy/environments/production.env .env
   ```

2. Edit `.env` with your NVIDIA-specific configuration:
   ```bash
   # NVIDIA AI Workbench API
   NVWB_API=https://api.nvidia-workbench.internal

   # Reverse proxy settings
   PROXY_PREFIX=/tutorial

   # Security
   SECRET_KEY=your-secure-key-here
   ALLOWED_DOMAINS=nvidia.com,developer.nvidia.com
   ```

## 🔧 Environment Configuration

### Key Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NVWB_API` | NVIDIA AI Workbench API endpoint | `https://api.nvidia-workbench.internal` |
| `PROXY_PREFIX` | Reverse proxy path prefix | `/tutorial` |
| `SECRET_KEY` | Application secret key | Auto-generated 64-char hex |
| `ALLOWED_DOMAINS` | Comma-separated allowed domains | `nvidia.com,developer.nvidia.com` |
| `REDIS_URL` | Redis cache URL | `redis://redis-service:6379` |

### Environment Files

- **`.env`** - Local development configuration
- **`variables.env`** - AI Workbench container environment
- **`deploy/environments/production.env`** - Production deployment
- **`deploy/environments/development.env`** - Development deployment

## 🐳 Deployment Options

### Option 1: Docker Compose (Recommended)

```bash
# Production deployment with monitoring
docker-compose up -d

# Development with hot reload
docker-compose -f docker-compose.dev.yml up
```

### Option 2: Kubernetes

```bash
# Deploy to Kubernetes cluster
kubectl apply -f deploy/kubernetes/

# Check deployment status
kubectl get pods -l app=tutorial-app
```

### Option 3: Direct Container

```bash
# Build and run
docker build -t nvidia-tutorial-app .
docker run -p 8501:8501 --env-file .env nvidia-tutorial-app
```

## 🔗 Integration Points

### AI Workbench API Integration

The application connects to NVIDIA AI Workbench via:

- **Unix Socket** (default): `/wb-svc-ro.socket`
- **HTTP API**: Configurable via `NVWB_API` environment variable

### Data Integration

- **Project Data**: Names, paths, Git status, environments
- **Application Data**: Running apps, URLs, states
- **Resource Data**: GPU allocations, package managers
- **Security**: Rate limiting, audit logging, input validation

### Monitoring Integration

```yaml
# Add to NVIDIA's Prometheus config
scrape_configs:
  - job_name: 'tutorial-app'
    static_configs:
      - targets: ['tutorial-app:9090']
```

## 🔒 Security Configuration

### Security Features Enabled

- **Input Sanitization**: All user inputs validated and sanitized
- **Rate Limiting**: 100 requests/minute per IP
- **Security Headers**: CSP, HSTS, X-Frame-Options
- **Domain Validation**: Only NVIDIA domains allowed
- **Audit Logging**: All API calls logged

### SSL/TLS Configuration

```nginx
# nginx configuration for SSL termination
server {
    listen 443 ssl;
    server_name tutorial.nvidia.com;

    ssl_certificate /etc/ssl/certs/tutorial-app.crt;
    ssl_certificate_key /etc/ssl/private/tutorial-app.key;

    location /tutorial/ {
        proxy_pass http://tutorial-app:8501/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoring & Observability

### Metrics Exposed

- **Application Metrics**: Request count, response times, error rates
- **Security Metrics**: Rate limit hits, blocked requests
- **Performance Metrics**: Cache hit rates, API response times
- **System Metrics**: CPU, memory, disk usage

### Grafana Dashboards

Pre-configured dashboards available at:
- `deploy/monitoring/grafana/dashboards/tutorial-app-dashboard.json`

### Health Checks

```bash
# Health check endpoint
curl http://localhost:8501/health

# Readiness probe for Kubernetes
kubectl exec tutorial-app -- curl http://localhost:8501/health
```

## 🧪 Testing & Validation

### Run Test Suite

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Run security tests
bandit -r src/
safety check
```

### Integration Testing

```bash
# Test AI Workbench API connectivity
python -c "from src.tutorial_app.common.wb_svc_client import list_projects; print(list_projects())"

# Test security features
python -c "from src.tutorial_app.common.security import InputSanitizer; print('Security module loaded')"
```

## 🚀 CI/CD Integration

### GitHub Actions

The repository includes CI/CD pipelines:

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: make test
      - name: Security scan
        run: make security-scan
      - name: Deploy to staging
        if: github.ref == 'refs/heads/main'
        run: make deploy-staging
```

### Deployment Scripts

- **`deploy/scripts/deploy.sh`** - Linux deployment script
- **`run_production.bat`** - Windows production runner
- **`setup_nvidia_integration.bat`** - Windows setup script

## 📚 API Documentation

Complete API documentation available at:
- `docs/API_REFERENCE.md` - Detailed API reference
- `docs/ARCHITECTURE_DECISIONS.md` - Architecture decisions

## 🆘 Troubleshooting

### Common Issues

1. **API Connection Failed**
   ```bash
   # Check API endpoint
   curl -I $NVWB_API/v1/query

   # Verify environment variables
   env | grep NVWB
   ```

2. **Rate Limiting**
   ```bash
   # Check rate limit logs
   docker logs tutorial-app | grep "rate limit"

   # Adjust limits in environment
   RATE_LIMIT_REQUESTS=200
   ```

3. **SSL Certificate Issues**
   ```bash
   # Verify certificates
   openssl s_client -connect tutorial.nvidia.com:443

   # Check certificate paths
   ls -la /etc/ssl/certs/
   ```

### Logs & Debugging

```bash
# View application logs
docker logs tutorial-app

# Enable debug logging
LOG_LEVEL=DEBUG
ENABLE_DEBUG_LOGGING=true

# Check Redis connectivity
docker exec tutorial-app redis-cli ping
```

## 📞 Support

For integration support or issues:

1. Check the troubleshooting section above
2. Review the [Developer Guide](docs/DEVELOPER_GUIDE.md)
3. Create an issue in the project repository
4. Contact the NVIDIA AI Workbench team

---

**🎉 Integration Complete!**

The NVIDIA AI Workbench Tutorial App is now configured and ready for deployment in your infrastructure. The application includes enterprise-grade security, monitoring, and performance optimizations suitable for production use.
