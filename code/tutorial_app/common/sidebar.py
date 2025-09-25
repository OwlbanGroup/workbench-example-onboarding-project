"""Tooling for loading and rendering the custom sidebar.

This module provides the sidebar functionality for the NVIDIA AI Workbench tutorial
application, including navigation, progress tracking, and external links.

Key Features:
- YAML-based sidebar configuration
- Progress tracking for tutorial pages
- Navigation between pages
- External link management
- Icon integration

Example:
    >>> sidebar = Sidebar.from_yaml()
    >>> sidebar.render()
"""

import logging
from pathlib import Path
from typing import List, Optional, Tuple

import streamlit as st

from . import icons
from .security import SecretManager

# Configure logging first
logger = logging.getLogger(__name__)

try:
    from pydantic import BaseModel, Field, field_validator
    from pydantic_yaml import parse_yaml_raw_as

    PYDANTIC_V2_AVAILABLE = True
except ImportError:
    # Fallback to Pydantic v1
    from pydantic import BaseModel, Field, validator

    field_validator = validator
    try:
        from pydantic_yaml import parse_yaml_raw_as

        PYDANTIC_V2_AVAILABLE = False
    except ImportError:
        parse_yaml_raw_as = None
        logger.warning("pydantic_yaml not available, YAML loading disabled")

# Constants
SIDEBAR_YAML_PATH: Path = Path(__file__).parent.parent.joinpath("pages", "sidebar.yaml")
BASE_URL: str = SecretManager.get_secret("PROXY_PREFIX", "")
DEFAULT_PAGE_EXTENSION: str = ".py"
PAGES_DIRECTORY: str = "pages"
PROGRESS_COMPLETED: str = "✅"
PROGRESS_NOT_STARTED: str = "*(not started)*"
PROGRESS_FORMAT: str = "*({completed}/{total})*"
HIDDEN_MENU_LABEL: str = "__hidden__"
DEFAULT_COMPLETED_COUNT: int = 0
DEFAULT_TOTAL_COUNT: Optional[int] = None


class MenuItem(BaseModel):
    """Representation of an item in a menu.

    A menu item represents a single page or section in the tutorial application
    with optional progress tracking.

    Attributes:
        label: Display name for the menu item
        target: Target identifier for the page
        show_progress: Whether to show progress indicator

    Example:
        >>> item = MenuItem(label="Getting Started", target="overview", show_progress=True)
        >>> print(item.full_label)
        'Getting Started ✅'
    """

    label: str = Field(..., min_length=1, description="Display name for the menu item")
    target: str = Field(..., min_length=1, description="Target identifier for the page")
    show_progress: bool = Field(default=True, description="Whether to show progress indicator")

    @field_validator("label", "target")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        """Validate that string fields are not empty or whitespace-only."""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace-only")
        return v.strip()

    @property
    def progress_string(self) -> str:
        """Calculate the progress indicator with error handling.

        Returns:
            Progress string or empty string if progress is disabled

        Raises:
            RuntimeError: If session state access fails
        """
        if not self.show_progress:
            return ""

        try:
            completed = st.session_state.get(f"{self.target}_completed", DEFAULT_COMPLETED_COUNT)
            total = st.session_state.get(f"{self.target}_total", DEFAULT_TOTAL_COUNT)

            if total is None:
                return PROGRESS_NOT_STARTED
            if completed == total:
                return PROGRESS_COMPLETED
            return PROGRESS_FORMAT.format(completed=completed, total=total)

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.warning("Error calculating progress for %s: %s", self.target, e)
            return PROGRESS_NOT_STARTED

    @property
    def full_label(self) -> str:
        """Calculate the full label with progress indicator.

        Returns:
            Formatted label with progress information

        Example:
            >>> item = MenuItem(label="Test", target="test")
            >>> item.full_label  # Could be "Test *(1/3)*" or "Test ✅"
        """
        return f"{self.label} {self.progress_string}"

    @property
    def filepath(self) -> str:
        """Calculate the file path to the module.

        Returns:
            File path relative to the pages directory

        Example:
            >>> item = MenuItem(label="Overview", target="overview")
            >>> item.filepath
            'pages/overview.py'
        """
        return f"{PAGES_DIRECTORY}/{self.target}{DEFAULT_PAGE_EXTENSION}"

    @property
    def markdown(self) -> str:
        """Calculate markdown for link to URL.

        Returns:
            Markdown formatted link string

        Example:
            >>> item = MenuItem(label="Documentation", target="docs")
            >>> item.markdown
            '[Documentation](docs)'
        """
        return f"[{self.label}]({self.target})"


class Menu(BaseModel):
    """Representation of a menu section.

    A menu contains multiple menu items and represents a logical grouping
    of tutorial pages or sections.

    Attributes:
        label: Display name for the menu section
        children: List of menu items in this section

    Example:
        >>> menu = Menu(label="Basics", children=[item1, item2])
    """

    label: str = Field(..., min_length=1, description="Display name for the menu section")
    children: list[MenuItem] = Field(..., description="List of menu items in this section")

    @field_validator("label")
    @classmethod
    def validate_label(cls, v: str) -> str:
        """Validate menu label."""
        if not v or not v.strip():
            raise ValueError("Menu label cannot be empty")
        return v.strip()

    @field_validator("children")
    @classmethod
    def validate_children(cls, v: list[MenuItem]) -> list[MenuItem]:
        """Validate that children list is not empty."""
        if not v:
            raise ValueError("Menu must have at least one child item")
        return v


class Links(BaseModel):
    """Representation of external links in the sidebar.

    Contains URLs for documentation, help, and other external resources.

    Attributes:
        documentation: URL to documentation
        gethelp: URL to help resources
        about: URL to about page
        bugs: URL to bug reporting
        settings: URL to settings page

    Example:
        >>> links = Links(
        ...     documentation="https://docs.example.com",
        ...     gethelp="https://help.example.com"
        ... )
    """

    documentation: Optional[str] = Field(None, description="URL to documentation")
    gethelp: Optional[str] = Field(None, description="URL to help resources")
    about: Optional[str] = Field(None, description="URL to about page")
    bugs: Optional[str] = Field(None, description="URL to bug reporting")
    settings: Optional[str] = Field(None, description="URL to settings page")


class Sidebar(BaseModel):
    """Representation of a complete sidebar structure.

    The main sidebar configuration containing header, navigation menu,
    and external links.

    Attributes:
        header: Optional header text for the sidebar
        navbar: List of menu sections
        links: External links configuration

    Example:
        >>> sidebar = Sidebar.from_yaml()
        >>> sidebar.render()
    """

    header: Optional[str] = Field(None, description="Optional header text for the sidebar")
    navbar: list[Menu] = Field(..., description="List of menu sections")
    links: Links = Field(default_factory=Links, description="External links configuration")

    @field_validator("navbar")
    @classmethod
    def validate_navbar(cls, v: list[Menu]) -> list[Menu]:
        """Validate that navbar has at least one menu."""
        if not v:
            raise ValueError("Sidebar must have at least one menu")
        return v

    @classmethod
    def from_yaml(cls) -> "Sidebar":
        """Load the sidebar data from YAML file with error handling.

        Loads the sidebar configuration from the YAML file and parses it
        into a Sidebar instance.

        Returns:
            Sidebar instance loaded from YAML

        Raises:
            FileNotFoundError: If YAML file doesn't exist
            RuntimeError: If YAML parsing fails
        """
        try:
            if not SIDEBAR_YAML_PATH.exists():
                raise FileNotFoundError(f"Sidebar YAML file not found: {SIDEBAR_YAML_PATH}")

            with open(SIDEBAR_YAML_PATH, "r", encoding="UTF-8") as ptr:
                yaml_content = ptr.read()

            sidebar = parse_yaml_raw_as(cls, yaml_content)
            logger.info("Successfully loaded sidebar from %s", SIDEBAR_YAML_PATH)
            return sidebar

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to load sidebar from YAML: %s", e)
            raise RuntimeError(f"Could not load sidebar configuration: {e}")

    @property
    def home_page(self) -> Optional[str]:
        """Return the Python file path to the homepage.

        Finds the first available page in the navigation structure
        to use as the home page.

        Returns:
            Streamlit Page object for the home page, or None if no pages exist

        Raises:
            RuntimeError: If page creation fails
        """
        try:
            for menu in self.navbar:
                for item in menu.children:
                    if item and item.target:
                        return st.Page(item.filepath)
            return st.Page(f"{PAGES_DIRECTORY}/start{DEFAULT_PAGE_EXTENSION}")

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to create home page: %s", e)
            raise RuntimeError(f"Could not create home page: {e}")

    @property
    def page_list(self) -> List[str]:
        """Return a list of page file paths for multipage navigation.

        Creates a flat list of all page file paths from the menu structure for
        Streamlit's multipage navigation system.

        Returns:
            List of page file paths

        Raises:
            RuntimeError: If page list creation fails
        """
        try:
            pages = []
            for menu in self.navbar:
                for item in menu.children:
                    if item and item.target:
                        pages.append(item.filepath)

            logger.debug("Created page list with %d pages", len(pages))
            return pages

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to create page list: %s", e)
            raise RuntimeError(f"Could not create page list: {e}")

    def prev_and_next_nav(self, page_name: str) -> Tuple[Optional[str], Optional[str]]:
        """Determine the next and previous pages from current page name.

        Args:
            page_name: Name of the current page

        Returns:
            Tuple of (previous_page, next_page) file paths, or (None, None) if not found

        Raises:
            ValueError: If page_name is invalid
        """
        if not isinstance(page_name, str) or not page_name.strip():
            raise ValueError("Page name must be a non-empty string")

        try:
            all_pages = [item.filepath for menu in self.navbar for item in menu.children]
            current_page_path = f"{PAGES_DIRECTORY}/{page_name}{DEFAULT_PAGE_EXTENSION}"

            try:
                page_idx = all_pages.index(current_page_path)
            except ValueError:
                logger.warning("Page '%s' not found in navigation", page_name)
                return None, None

            prev_page = all_pages[page_idx - 1] if page_idx > 0 else None
            next_page = all_pages[page_idx + 1] if page_idx < len(all_pages) - 1 else None

            logger.debug("Navigation for '%s': prev=%s, next=%s", page_name, prev_page, next_page)
            return prev_page, next_page

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Error in navigation calculation for '%s': %s", page_name, e)
            return None, None

    def render_header(self) -> None:
        """Render the sidebar header with error handling.

        Logs errors but doesn't raise exceptions to prevent breaking the UI.
        """
        try:
            if self.header:
                st.markdown(f"## {self.header}")
                logger.debug("Rendered sidebar header: %s", self.header)
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to render sidebar header: %s", e)
            # Don't raise - just log and continue to prevent UI breakage

    def render_navbar(self) -> None:
        """Render the navigation menu with error handling.

        Renders all menu sections and their items, skipping hidden menus.
        Logs errors but continues to prevent UI breakage.
        """
        try:
            for menu in self.navbar:
                if menu.label == HIDDEN_MENU_LABEL:
                    continue

                st.markdown(f"### {menu.label}")
                for item in menu.children:
                    if item and item.target:
                        st.page_link(page=item.filepath, label=item.full_label, use_container_width=True)
            logger.debug("Successfully rendered navigation menu")
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to render navigation menu: %s", e)
            # Don't raise - just log and continue to prevent UI breakage

    def render_links(self) -> None:
        """Render external links toolbar with error handling.

        Creates HTML for the toolbar with icons and links to external resources.
        Logs errors but continues to prevent UI breakage.
        """
        try:
            html_parts = ['<div class="toolbar">']

            # Home link
            html_parts.append(f'<span role="button" title="Home"><a href="{BASE_URL}">{icons.HOME}</a></span>')

            # External links
            link_configs = [
                (self.links.documentation, "Documentation", icons.BOOK_4),
                (self.links.about, "About", icons.INFO),
                (self.links.gethelp, "Help", icons.HELP),
                (self.links.bugs, "Report a Bug", icons.BUGS),
                (self.links.settings, "Settings", icons.SETTINGS),
            ]

            for url, title, icon in link_configs:
                if url:
                    html_parts.append(f'<span role="button" title="{title}"><a href="{url}">{icon}</a></span>')

            html_parts.append("</div>")
            html_content = "".join(html_parts)

            st.html(html_content)
            logger.debug("Successfully rendered external links toolbar")

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to render external links: %s", e)
            # Don't raise - just log and continue to prevent UI breakage

    def render(self) -> None:
        """Render the complete sidebar with error handling.

        Orchestrates the rendering of header, links, and navigation menu.
        Logs errors but continues to prevent UI breakage.
        """
        try:
            logger.info("Starting sidebar render")
            self.render_header()
            self.render_links()
            self.render_navbar()
            logger.info("Successfully completed sidebar render")

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to render sidebar: %s", e)
            # Don't raise - just log and continue to prevent UI breakage


APP_SIDEBAR = Sidebar.from_yaml()
