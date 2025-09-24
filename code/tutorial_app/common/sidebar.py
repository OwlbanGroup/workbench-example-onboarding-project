"""Tooling for loading and rendering the custom sidebar."""

import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_yaml import parse_yaml_raw_as
import streamlit as st

from . import icons

_SB_YAML = Path(__file__).parent.parent.joinpath("pages", "sidebar.yaml")
_BASE_URL = os.environ.get("PROXY_PREFIX", "")


class MenuItem(BaseModel):
    """Representation of an item in a menu."""

    label: str
    target: str
    show_progress: bool = True

    @property
    def progress_string(self) -> str:
        """Calculate the progress indicator."""
        if not self.show_progress:
            return ""
        completed = st.session_state.get(f"{self.target}_completed", 0)
        total = st.session_state.get(f"{self.target}_total", None)

        if total is None:
            return "*(not started)*"
        if completed == total:
            return "✅"
        return f"*({completed}/{total})*"

    @property
    def full_label(self) -> str:
        """Calculate the full label with progress."""
        return f"{self.label} {self.progress_string}"

    @property
    def filepath(self) -> str:
        """Calculate the ASSUMED file path to the module."""
        return f"pages/{self.target}.py"

    @property
    def markdown(self) -> str:
        """Calculate markdown for link to URL."""
        return f"[{self.label}]({self.target})"


class Menu(BaseModel):
    """Representation of a menu."""

    label: str
    children: list[MenuItem]


class Links(BaseModel):
    """Representation of links."""

    documentation: None | str = None
    gethelp: None | str = None
    about: None | str = None
    bugs: None | str = None
    settings: None | str = None


class Sidebar(BaseModel):
    """Representation of a sidebar structure."""

    header: str | None = None
    navbar: list[Menu]
    links: Links

    @classmethod
    def from_yaml(cls) -> "Sidebar":
        """Load the sidebar data from yaml."""
        with open(_SB_YAML, "r", encoding="UTF-8") as ptr:
            yml = ptr.read()

        return parse_yaml_raw_as(cls, yml)

    @property
    def home_page(self) -> None | str:
        """Return the python file path to the homepage."""
        for menu in self.navbar:
            for item in menu.children:
                return st.Page(f"pages/{item.target}.py")
        return st.Page("pages/start.py")

    @property
    def page_list(self) -> list[str]:
        """Return a list of streamlit pages for multipage nav."""
        return [st.Page(f"pages/{item.target}.py") for menu in self.navbar for item in menu.children]

    def prev_and_next_nav(self, page_name: str) -> tuple[str | None, str | None]:
        """Determine the next and previous pages from page_name."""
        all_pages = [f"pages/{item.target}.py" for menu in self.navbar for item in menu.children]

        try:
            page_idx = all_pages.index(f"pages/{page_name}.py")
        except ValueError:
            return None, None
        prev = all_pages[page_idx - 1] if page_idx > 0 else None
        nxt = all_pages[page_idx + 1] if page_idx < len(all_pages) - 1 else None
        return prev, nxt

    def render_header(self):
        """Render the sidebar from yaml."""
        st.markdown(f"## {self.header}")

    def render_navbar(self):
        """Render the sidebar from yaml."""
        for menu in self.navbar:
            if menu.label == "__hidden__":
                continue
            st.markdown(f"### {menu.label}")
            for item in menu.children:
                st.page_link(page=item.filepath, label=item.full_label, use_container_width=True)

    def render_links(self):
        """Render the sidebar from yaml."""
        html = '<div class="toolbar">'

        html += f'<span role="button" title="Home"><a href="{_BASE_URL}">{icons.HOME}</a></span>'
        if self.links.documentation:
            html += f'<span role="button" title="Documentation"><a href="{self.links.documentation}">{icons.BOOK_4}</a></span>'
        if self.links.about:
            html += f'<span role="button" title="About"><a href="{self.links.about}">{icons.INFO}</a></span>'
        if self.links.gethelp:
            html += f'<span role="button" title="Help"><a href="{self.links.gethelp}">{icons.HELP}</a></span>'
        if self.links.bugs:
            html += f'<span role="button" title="Report a Bug"><a href="{self.links.bugs}">{icons.BUGS}</a></span>'
        if self.links.settings:
            html += f'<span role="button" title="Settings"><a href="{self.links.settings}">{icons.SETTINGS}</a></span>'

        html += "</div>"

        st.html(html)

    def render(self):
        """Render the sidebar from yaml."""
        self.render_header()
        self.render_links()
        self.render_navbar()


APP_SIDEBAR = Sidebar.from_yaml()
