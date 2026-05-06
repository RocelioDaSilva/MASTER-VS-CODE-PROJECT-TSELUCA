"""
Page Router
Handles multi-page navigation for Streamlit app
"""

import streamlit as st
from typing import Callable, Dict


class PageRouter:
    """Manages page navigation and rendering"""

    def __init__(self):
        self.pages: Dict[str, Callable] = {}

    def register(self, page_name: str, render_func: Callable):
        """Register a page"""
        self.pages[page_name] = render_func

    def render(self, current_page: str):
        """Render the current page"""
        if current_page in self.pages:
            self.pages[current_page]()
        else:
            st.error(f"Página '{current_page}' não encontrada.")

    def get_page_list(self) -> list:
        """Get list of registered pages"""
        return list(self.pages.keys())
