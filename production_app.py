"""Production version of the Streamlit app."""

import sys
import os
import subprocess
import logging

# Set production environment variables
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
os.environ["STREAMLIT_SERVER_PORT"] = "8501"
os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Run the streamlit app
    sys.path.append("code/tutorial_app")
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "src/tutorial_app/streamlit_app.py",
                "--server.headless",
                "true",
                "--server.port",
                "8501",
                "--server.address",
                "0.0.0.0",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error("Error running Streamlit app: %s", e)
        sys.exit(1)
