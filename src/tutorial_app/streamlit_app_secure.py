"""Secure Streamlit application entry point for NVIDIA AI Workbench Tutorial.

This is a security-hardened version of the main application that includes
comprehensive security measures and audit logging. It serves as a reference
implementation for secure Streamlit application deployment.

Security Features:
- Enhanced security initialization with comprehensive checks
- Audit logging for all application events
- Security header configuration
- Input validation and sanitization
- Rate limiting for API calls
- Secure secret management

This version is intended for production deployments where security is paramount.
For development and testing, use the standard streamlit_app.py.

Note: This version modifies sys.path to ensure proper module loading.
Use with caution in shared environments.
"""

import sys

sys.path.append(".")

import streamlit as st

from common.sidebar import APP_SIDEBAR
from common.security import initialize_security, audit_log

# Initialize security measures
initialize_security()

# Log application start
audit_log("application_start")

st.set_page_config(
    page_title=APP_SIDEBAR.header,
    layout="centered",
    menu_items={
        "Get help": APP_SIDEBAR.links.gethelp,
        "Report a bug": APP_SIDEBAR.links.bugs,
        "About": APP_SIDEBAR.links.about,
    },
)

nav = [st.Page(path) for path in APP_SIDEBAR.page_list]
pg = st.navigation(nav)
pg.run()
