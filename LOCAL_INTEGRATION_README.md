# Local NVIDIA AI Workbench Integration

This document explains how to use the NVIDIA AI Workbench Tutorial App with your local NVIDIA AI Workbench installation.

## Quick Start

1. **Run the setup script:**
   ```batch
   setup_local_nvidia_workbench_simple.bat
   ```

2. **Start the application:**
   ```batch
   start-local.bat
   ```
   Or manually:
   ```batch
   streamlit run src/tutorial_app/streamlit_app.py
   ```

3. **Use workbench helper:**
   ```batch
   workbench-helper.bat
   ```

## Configuration Files

- **`.env.local`** - Local development environment variables
- **`variables.env`** - Updated with local integration settings

## Features

- ✅ Local NVIDIA AI Workbench integration
- ✅ Automatic environment configuration
- ✅ Helper scripts for common operations
- ✅ Development-friendly settings (relaxed security)
- ✅ Socket and HTTP communication support

## Troubleshooting

### Workbench Not Detected
If NVIDIA AI Workbench is not auto-detected:
1. Ensure it's installed and running
2. Check if the CLI is in your PATH
3. Run setup again or configure manually

### Connection Issues
- Check if NVIDIA AI Workbench is running
- Verify socket path: `/tmp/nvidia-workbench.sock`
- Check firewall settings for local connections

### Import Errors
- Ensure all dependencies are installed: `pip install -e .`
- Check Python path includes the `src` directory

## Security Note

This local integration uses relaxed security settings for development.
**Do not use these settings in production**

For production deployment, use the production scripts:
- `deploy\scripts\deploy_production.bat` (Windows)
- `deploy/scripts/deploy_production.sh` (Linux)
