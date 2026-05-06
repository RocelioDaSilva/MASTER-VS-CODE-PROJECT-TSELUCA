"""
Error Handlers
Unified error handling for dashboard
"""

import streamlit as st
import logging
from typing import Callable, Any


logger = logging.getLogger("geesp_dashboard")


def safe_execution(func: Callable, *args, **kwargs) -> Any:
    """Execute function with error handling"""
    try:
        return func(*args, **kwargs)
    except FileNotFoundError as e:
        st.error(f"❌ Arquivo não encontrado: {str(e)}")
        logger.error(f"FileNotFoundError: {e}")
        return None
    except ValueError as e:
        st.error(f"❌ Erro de valor: {str(e)}")
        logger.error(f"ValueError: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Erro inesperado: {str(e)}")
        logger.error(f"Unexpected error: {e}")
        return None


def show_success(message: str):
    """Show success message"""
    st.success(f"✓ {message}")
    logger.info(message)


def show_warning(message: str):
    """Show warning message"""
    st.warning(f"⚠️ {message}")
    logger.warning(message)


def show_error(message: str):
    """Show error message"""
    st.error(f"❌ {message}")
    logger.error(message)


def show_info(message: str):
    """Show info message"""
    st.info(f"ℹ️ {message}")
    logger.info(message)
