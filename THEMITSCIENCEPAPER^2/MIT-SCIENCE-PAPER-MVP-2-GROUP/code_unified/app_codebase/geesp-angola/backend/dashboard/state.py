"""
GEESP-Angola Dashboard State Management
Unified session state management for Streamlit dashboard
"""

import streamlit as st
from typing import Any, Dict, Optional


class SessionState:
    """Manages shared state across dashboard pages"""

    # Default state structure
    DEFAULT_STATE = {
        "scenarios": [],
        "current_scenario": None,
        "analysis_results": None,
        "last_mcda_weights": None,
        "selected_zones": [],
        "map_center": (-18.0, 14.75),
        "map_zoom": 8,
        "uploaded_files": [],
        "cache_data": {},
        "current_page": "🏠 Início",
        "weights": {
            "Irradiação Solar": 25,
            "Demanda (Luzes Noturnas)": 25,
            "Acesso (Distância Rede)": 20,
            "Infraestrutura": 15,
            "Uso do Solo": 15,
        },
    }

    @staticmethod
    def init():
        """Initialize session state with defaults"""
        for key, value in SessionState.DEFAULT_STATE.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get session state value"""
        SessionState.init()
        return st.session_state.get(key, default)

    @staticmethod
    def set(key: str, value: Any) -> None:
        """Set session state value"""
        SessionState.init()
        st.session_state[key] = value

    @staticmethod
    def update(updates: Dict[str, Any]) -> None:
        """Update multiple session state values"""
        SessionState.init()
        st.session_state.update(updates)

    @staticmethod
    def clear():
        """Clear all session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]

    @staticmethod
    def reset_to_defaults():
        """Reset session state to defaults"""
        SessionState.clear()
        SessionState.init()


def get_session_state():
    """Get/initialize session state"""
    SessionState.init()
    if 'scenarios' not in st.session_state:
        st.session_state.scenarios = []
    return st.session_state


def update_analysis_result(result: Dict[str, Any]) -> None:
    """Update analysis result in session"""
    SessionState.set("analysis_results", result)
    st.session_state.last_updated_result = st.session_state.get(
        'last_updated_result', 0
    )


def update_mcda_weights(weights: Dict[str, float]) -> None:
    """Update MCDA weights in session"""
    SessionState.set("last_mcda_weights", weights)


def add_scenario(scenario: Dict[str, Any]) -> None:
    """Add scenario to session"""
    scenarios = SessionState.get("scenarios", [])
    scenarios.append(scenario)
    SessionState.set("scenarios", scenarios)
    SessionState.set("current_scenario", scenario)


def get_current_scenario() -> Optional[Dict[str, Any]]:
    """Get current scenario from session"""
    return SessionState.get("current_scenario")


def set_current_scenario(scenario: Dict[str, Any]) -> None:
    """Set current scenario in session"""
    SessionState.set("current_scenario", scenario)


def get_analysis_results() -> Optional[Dict[str, Any]]:
    """Get analysis results from session"""
    return SessionState.get("analysis_results")


def get_mcda_weights() -> Optional[Dict[str, float]]:
    """Get MCDA weights from session"""
    return SessionState.get("last_mcda_weights")


def set_map_view(center: tuple, zoom: int) -> None:
    """Update map view in session"""
    SessionState.update({
        "map_center": center,
        "map_zoom": zoom,
    })


def get_map_view() -> tuple:
    """Get map view from session"""
    center = SessionState.get("map_center", (-18.0, 14.75))
    zoom = SessionState.get("map_zoom", 8)
    return center, zoom


__all__ = [
    "SessionState",
    "get_session_state",
    "update_analysis_result",
    "update_mcda_weights",
    "add_scenario",
    "get_current_scenario",
    "set_current_scenario",
    "get_analysis_results",
    "get_mcda_weights",
    "set_map_view",
    "get_map_view",
]
