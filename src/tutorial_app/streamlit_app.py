"""Top level streamlit app page."""

import streamlit as st
import httpx

from tutorial_app.common.sidebar import APP_SIDEBAR
from tutorial_app.common.middleware import setup_middleware

# Backend URL
BACKEND_URL = "http://localhost:8000"


def main():
    """Main app function with middleware."""
    st.set_page_config(
        page_title=APP_SIDEBAR.header,
        layout="centered",
        menu_items={
            "Get help": APP_SIDEBAR.links.gethelp,
            "Report a bug": APP_SIDEBAR.links.bugs,
            "About": APP_SIDEBAR.links.about,
        },
    )

    # Backend health check
    try:
        with httpx.Client(base_url=BACKEND_URL, timeout=5.0) as client:
            response = client.get("/health")
            if response.status_code == 200:
                st.session_state.backend_status = "Connected"
            else:
                st.session_state.backend_status = "Unavailable"
    except httpx.RequestError:
        st.session_state.backend_status = "Disconnected"

    # Display backend status in sidebar
    with st.sidebar:
        st.write(f"Backend: {st.session_state.backend_status}")

    nav = [st.Page(path) for path in APP_SIDEBAR.page_list]
    pg = st.navigation(nav)
    pg.run()


# Apply middleware
main = setup_middleware(main)

if __name__ == "__main__":
    main()
