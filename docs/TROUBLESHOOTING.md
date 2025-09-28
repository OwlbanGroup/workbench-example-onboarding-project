# Troubleshooting Guide

This guide helps you resolve common issues when setting up and running the NVIDIA AI Workbench Tutorial App.

## Table of Contents

- [Quick Health Check](#quick-health-check)
- [Common Issues](#common-issues)
  - [Docker Issues](#docker-issues)
  - [Python/Dependencies Issues](#python-dependencies-issues)
  - [Service Connection Issues](#service-connection-issues)
  - [NVIDIA GPU Issues](#nvidia-gpu-issues)
  - [Application Errors](#application-errors)
- [Advanced Troubleshooting](#advanced-troubleshooting)
- [Getting Help](#getting-help)

## Quick Health Check

Run the health check script to quickly identify issues:

**Windows:**
```batch
.\health_check.bat
```

**Linux/macOS:**
```bash
./health_check.sh
```

## Common Issues

### Docker Issues

#### Docker Not Installed
**Symptoms:** `docker: command not found`
**Solution:**
- Install Docker Desktop for Windows/macOS
- For Linux, install Docker Engine
- Restart your terminal after installation

#### Docker Compose Services Not Starting
**Symptoms:** `docker-compose up -d` fails or services don't start
**Solution:**
1. Check Docker is running: `docker --version`
2. Clean up: `docker-compose down -v`
3. Rebuild: `docker-compose up -d --build`
4. Check logs: `docker-compose logs`

#### Port Conflicts
**Symptoms:** Services fail to start with "port already in use"
**Solution:**
1. Check what's using the ports: `netstat -ano | findstr :PORT` (Windows) or `lsof -i :PORT` (Linux)
2. Stop conflicting services or change ports in `docker-compose.yml`
3. Common ports: 8501 (Streamlit), 3000 (Grafana), 3001 (Gitea), 8000 (Backend), 9090 (Prometheus)

### Python/Dependencies Issues

#### Python Not Found
**Symptoms:** `python: command not found`
**Solution:**
- Install Python 3.8+ from python.org
- Ensure Python is in PATH
- Use `python3` instead of `python` on some systems

#### Dependencies Not Installed
**Symptoms:** Import errors when running the app
**Solution:**
```bash
pip install -r requirements.txt
```

#### Virtual Environment Issues
**Symptoms:** Packages installed but not found
**Solution:**
- Activate virtual environment: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux)
- Reinstall in virtual environment: `pip install -r requirements.txt`

### Service Connection Issues

#### Tutorial App Not Accessible
**Symptoms:** http://localhost returns connection refused
**Solution:**
1. Check if services are running: `docker-compose ps`
2. Check app logs: `docker-compose logs tutorial-app`
3. Verify port mapping in `docker-compose.yml`
4. Try direct access: http://localhost:8501

#### Backend API Not Responding
**Symptoms:** http://localhost:8000/health fails
**Solution:**
1. Check backend logs: `docker-compose logs backend`
2. Verify environment variables in `docker-compose.yml`
3. Check Redis connection: `docker-compose exec redis redis-cli ping`

#### Database Connection Failed
**Symptoms:** App shows database errors
**Solution:**
1. Check Redis is running: `docker-compose ps redis`
2. Check Redis logs: `docker-compose logs redis`
3. Verify REDIS_URL in environment files

### NVIDIA GPU Issues

#### NVIDIA GPU Not Detected
**Symptoms:** nvidia-smi not found or GPU not available
**Solution:**
- Install NVIDIA drivers
- Install CUDA toolkit
- For Docker: Install NVIDIA Docker support
- Verify GPU: `nvidia-smi`

#### CUDA Errors in Application
**Symptoms:** CUDA runtime errors
**Solution:**
1. Check CUDA version compatibility
2. Update NVIDIA drivers
3. Reinstall PyTorch/CUDA packages: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

### Application Errors

#### Import Errors
**Symptoms:** Module not found errors
**Solution:**
1. Check PYTHONPATH: `python -c "import sys; print(sys.path)"`
2. Ensure src/ is in path: `export PYTHONPATH=src:$PYTHONPATH`
3. Reinstall packages: `pip install -e .`

#### Streamlit Errors
**Symptoms:** Streamlit fails to start
**Solution:**
1. Check port availability
2. Clear Streamlit cache: `rm -rf ~/.streamlit`
3. Check configuration in `.streamlit/config.toml`

#### Authentication Issues
**Symptoms:** Login fails or permission errors
**Solution:**
1. Check secrets in `.streamlit/secrets.toml`
2. Verify environment variables
3. Check security module: `python -c "from src.tutorial_app.common.security import initialize_security"`

## Advanced Troubleshooting

### Docker Debug Mode
Run services with debug logging:
```bash
docker-compose up --build --force-recreate
```

### Application Debug Mode
Run with debug logging:
```bash
export LOG_LEVEL=DEBUG
streamlit run src/tutorial_app/streamlit_app.py
```

### Network Debugging
Check network connectivity:
```bash
# Test internal Docker network
docker-compose exec tutorial-app curl -f http://backend:8000/health

# Test external access
curl -f http://localhost/healthz
```

### Performance Issues
If the app is slow:
1. Check resource usage: `docker stats`
2. Monitor with Grafana: http://localhost:3000
3. Check Redis performance: `docker-compose exec redis redis-cli info`

### Logs Analysis
Collect all logs for analysis:
```bash
# Docker logs
docker-compose logs > docker-logs.txt

# Application logs (if logging to files)
find logs/ -name "*.log" -exec cat {} \;
```

## Getting Help

If you can't resolve the issue:

1. **Check Existing Resources:**
   - README.md for setup instructions
   - docs/DEVELOPER_GUIDE.md for development info
   - docs/API_REFERENCE.md for API details

2. **Run Diagnostics:**
   - Execute health check script
   - Collect system information: `python -c "import sys; print(sys.version)"`

3. **Community Support:**
   - Check GitHub Issues for similar problems
   - Create a new issue with:
     - Health check output
     - Error messages
     - System information
     - Steps to reproduce

4. **NVIDIA Support:**
   - For NVIDIA-specific issues, check NVIDIA AI Workbench documentation
   - Contact NVIDIA support for hardware/driver issues

## Prevention

To avoid common issues:
- Always run setup scripts in order
- Use virtual environments
- Keep Docker and dependencies updated
- Regularly run health checks
- Backup configuration before changes
