"""Production version of the Streamlit app."""

import sys
import os

sys.path.append(os.path.dirname(__file__))

import streamlit as st

# Import the main function from streamlit_app
sys.path.append("code/tutorial_app")
from streamlit_app import main

if __name__ == "__main__":
    # Set production environment
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_SERVER_PORT"] = "8501"
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
