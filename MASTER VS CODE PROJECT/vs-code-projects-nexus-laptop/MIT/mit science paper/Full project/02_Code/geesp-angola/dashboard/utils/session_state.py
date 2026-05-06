"""
Session State Manager
Handles Streamlit session state initialization and access
"""

import streamlit as st
from typing import Any, Dict, Optional


class SessionState:
    """Centralizes session state management"""

    @staticmethod
    def init():
        """Initialize default session state variables"""
        if "current_page" not in st.session_state:
            st.session_state.current_page = "🏠 Início"
        
        if "weights" not in st.session_state:
            st.session_state.weights = {
                "Irradiação Solar": 25,
                "Demanda (Luzes Noturnas)": 25,
                "Acesso (Distância Rede)": 20,
                "Infraestrutura": 15,
                "Uso do Solo": 15,
            }
        
        if "current_analysis" not in st.session_state:
            st.session_state.current_analysis = None
        
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = []

    @staticmethod
    def set(key: str, value: Any):
        """Set a session state variable"""
        st.session_state[key] = value

    @staticmethod
    def get(key: str, default: Optional[Any] = None) -> Any:
        """Get a session state variable"""
        return st.session_state.get(key, default)

    @staticmethod
    def clear():
        """Clear all session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
