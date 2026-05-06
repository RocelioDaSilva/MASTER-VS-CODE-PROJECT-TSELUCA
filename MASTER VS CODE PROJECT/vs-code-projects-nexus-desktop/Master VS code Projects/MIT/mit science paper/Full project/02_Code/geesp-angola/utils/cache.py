"""Simple caching utilities used by dashboard pages and scripts.

This module provides lightweight, dependency-free caching primitives that
work in-process and are easy to unit test.
"""
from functools import wraps
from typing import Any, Callable, Dict, Tuple

_MEMO_CACHE: Dict[Tuple[str, Tuple[Any, ...], Tuple[Tuple[str, Any], ...]], Any] = {}


def simple_cache(key: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """A tiny cache decorator keyed by a string and function args.

    Not thread-safe; intended for Streamlit single-process usage in tests.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            k = (key, args, tuple(sorted(kwargs.items())))
            if k in _MEMO_CACHE:
                return _MEMO_CACHE[k]
            res = func(*args, **kwargs)
            _MEMO_CACHE[k] = res
            return res

        return wrapper

    return decorator


def cache_clear() -> None:
    """Clear the internal in-memory cache."""
    _MEMO_CACHE.clear()
