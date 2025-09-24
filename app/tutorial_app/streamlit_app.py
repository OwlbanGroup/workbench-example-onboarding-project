"""Main Streamlit application entry point for NVIDIA AI Workbench Tutorial.

This module initializes the tutorial application with security measures,
configures the Streamlit page settings, and sets up navigation for all
tutorial pages.

The application provides an interactive learning platform for NVIDIA AI Workbench,
featuring tutorials on project creation, environment management, and advanced
AI development workflows.

Key Features:
- Security initialization with audit logging
- Responsive centered layout
- Multi-page navigation with progress tracking
- External link integration (help, documentation, bug reports)

Security:
- Initializes security measures on startup
- Logs application start events for audit purposes
- Applies security headers and input validation

Navigation:
- Dynamic page list generation from sidebar configuration
- Progress tracking for tutorial completion
- External links for support and documentation
"""

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

nav = APP_SIDEBAR.page_list
pg = st.navigation(nav)
pg.run()
