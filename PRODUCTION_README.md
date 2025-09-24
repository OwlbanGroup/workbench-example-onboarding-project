# Production Deployment Guide

This guide explains how to deploy the Streamlit tutorial app in a production environment.

## Files Created

- `production_app.py`: Production version of the app with optimized settings.
- `Dockerfile`: For containerizing the app.
- `.env.production`: Environment variables for production.
- `run_production.bat`: Script to run the app in production on Windows.

## Deployment Options

### Option 1: Direct Run

1. Ensure all dependencies are installed (pip install -r requirements.txt).
2. Run `run_production.bat` or `python production_app.py`.

### Option 2: Docker

1. Build the image: `docker build -t streamlit-tutorial .`
2. Run the container: `docker run -p 8501:8501 streamlit-tutorial`

## Environment Variables

The app uses the following environment variables (set in .env.production):

- STREAMLIT_SERVER_HEADLESS: Run in headless mode.
- STREAMLIT_SERVER_PORT: Port to run on (default 8501).
- STREAMLIT_SERVER_ADDRESS: Address to bind to (0.0.0.0 for all interfaces).
- STREAMLIT_BROWSER_GATHER_USAGE_STATS: Disable usage stats.
- STREAMLIT_THEME_BASE: Set theme (dark/light).
- STREAMLIT_CLIENT_SHOW_SIDEBAR_NAVIGATION: Hide sidebar navigation.

## Notes

- The app is configured for production with no debug mode.
- Ensure security best practices for your deployment environment.
