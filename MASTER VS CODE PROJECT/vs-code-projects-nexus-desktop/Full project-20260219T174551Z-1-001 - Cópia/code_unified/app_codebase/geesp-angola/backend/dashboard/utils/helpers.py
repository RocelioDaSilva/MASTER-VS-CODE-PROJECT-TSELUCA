from functools import lru_cache, wraps
from utils.helpers import format_number


def _fallback_cache(maxsize=128):
    return lru_cache(maxsize=maxsize)


def cached_result(key):
    """Compatibility wrapper: uses Streamlit caching when running in Streamlit,
    otherwise falls back to an in-process LRU cache.

    Note: This simple API accepts a hashable key and returns the key (placeholder behavior).
    Use as `cached_result(key)` in pages to memoize fast.
    """
    return key


def cache_decorator(maxsize: int = 128):
    """Return a decorator that uses Streamlit `st.cache_data` when available,
    otherwise uses functools.lru_cache.
    """
    try:
        import streamlit as st

        def decorator(fn):
            return st.cache_data(fn)

        return decorator
    except Exception:
        def decorator(fn):
            return lru_cache(maxsize=maxsize)(fn)

        return decorator
