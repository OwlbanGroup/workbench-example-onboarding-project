# Quick Start Guide

Get the NVIDIA AI Workbench Tutorial App up and running in minutes!

## Prerequisites

- **Operating System:** Windows 10/11, macOS, or Linux
- **Docker:** Docker Desktop (Windows/macOS) or Docker Engine (Linux)
- **Python:** 3.8+ (optional for local development)
- **NVIDIA GPU:** Optional, for GPU-accelerated features

## One-Command Setup

### Windows
```batch
.\setup_all.bat
```

### Linux/macOS
```bash
./setup_all.sh
```

This automated script will:
- Check prerequisites
- Install dependencies
- Configure environment
- Set up NVIDIA integration
- Start all services

## Manual Setup (Alternative)

If automated setup fails:

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd workbench-example-onboarding-project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy environment template
cp deploy/environments/production.env .env

# Edit .env with your settings
# SECRET_KEY, database URLs, etc.
```

### 4. Start Services
```bash
docker-compose up -d
```

### 5. Run Application
```bash
streamlit run src/tutorial_app/streamlit_app.py
```

## Access the Application

Once running, access these URLs:

| Service | URL | Credentials |
|---------|-----|-------------|
| Tutorial App | http://localhost | - |
| Backend API | http://localhost:8000 | - |
| Gitea (Git) | http://localhost:3001 | admin/admin |
| Grafana | http://localhost:3000 | admin/admin |
| Prometheus | http://localhost:9090 | - |

## Health Check

Verify everything is working:

**Windows:**
```batch
.\health_check.bat
```

**Linux/macOS:**
```bash
./health_check.sh
```

## Tutorial Walkthrough

1. **Basic Tutorials (1-3):** Learn Streamlit fundamentals
2. **Advanced Tutorials:** Explore AI/ML integration
3. **NVIDIA Features:** GPU-accelerated workflows
4. **Settings:** Configure your environment

## Development Workflow

### Local Development
```bash
# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Install in development mode
pip install -e .

# Run tests
python run_all_tests.py

# Start development server
streamlit run src/tutorial_app/streamlit_app.py
```

### Docker Development
```bash
# Build and run in Docker
docker-compose up --build

# Run tests in container
docker-compose exec tutorial-app python run_all_tests.py
```

## NVIDIA Integration

For GPU support:

1. Install NVIDIA drivers and CUDA
2. Run NVIDIA setup: `.\setup_nvidia_integration.bat`
3. Verify GPU: `nvidia-smi`

## Troubleshooting

If something doesn't work:

1. Run health check script
2. Check logs: `docker-compose logs`
3. Restart services: `docker-compose restart`
4. See [Troubleshooting Guide](TROUBLESHOOTING.md)

## Next Steps

- Read [Developer Guide](DEVELOPER_GUIDE.md) for advanced topics
- Check [API Reference](API_REFERENCE.md) for integrations
- Explore [Architecture Decisions](ARCHITECTURE_DECISIONS.md)

## Support

- **Issues:** Check GitHub Issues
- **Documentation:** See docs/ folder
- **NVIDIA:** AI Workbench documentation

Happy coding! 🚀
