# Task: Fix type mismatch in Sidebar.page_list property

## Steps:

- [x] Update `src/tutorial_app/common/sidebar.py`: Change `page_list` to return `List[str]` (file paths) instead of `List[st.Page]`, update docstring accordingly. This resolves the type hint inconsistency while maintaining functionality.

- [x] Update `src/tutorial_app/streamlit_app.py`: Wrap the page_list paths in `st.Page` objects for `st.navigation()` compatibility.

- [x] Update `src/tutorial_app/streamlit_app_secure.py`: Wrap the page_list paths in `st.Page` objects for `st.navigation()` compatibility.

- [x] Update `app/tutorial_app/streamlit_app.py`: Wrap the page_list paths in `st.Page` objects for `st.navigation()` compatibility.

- [] Run integration tests: Execute `pytest src/tutorial_app/tests/test_integration.py::TestCompleteWorkflows::test_complete_sidebar_workflow` to verify the sidebar workflow still passes.

- [] Run property-based tests: Execute `pytest src/tutorial_app/tests/test_property_based.py` to ensure no regressions in sidebar properties.

- [] Optional: If mypy or type checking is configured, run it to confirm the type fix resolves any errors.

- [] Update any documentation if needed (e.g., API_REFERENCE.md mentions page_list as List[str], but no changes required based on current content).
