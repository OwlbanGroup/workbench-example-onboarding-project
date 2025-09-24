"""Top level streamlit app page with security enhancements."""

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

nav = APP_SIDEBAR.page_list
pg = st.navigation(nav)
pg.run()
