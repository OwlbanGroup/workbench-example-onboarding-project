"""Top level streamlit app page."""

import streamlit as st

from common.sidebar import APP_SIDEBAR

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
