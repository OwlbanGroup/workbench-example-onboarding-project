@echo off
REM Production script to run the Streamlit app

REM Load environment variables from .env.production
if exist .env.production (
    for /f "delims=" %%i in (.env.production) do set %%i
)

REM Run the production app
python production_app.py
