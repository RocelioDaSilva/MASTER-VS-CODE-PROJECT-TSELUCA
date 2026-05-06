"""UI helper components for GEESP-Angola Streamlit pages.

Small, well-typed helper functions to keep pages concise and testable.
"""
from typing import Any, Dict, Optional

def metric_card(title: str, value: Any, delta: Optional[str] = None) -> Dict[str, Any]:
    """Return a small dictionary representing a metric card.

    This is deliberately lightweight and UI-agnostic to allow unit testing
    without requiring Streamlit rendering.
    """
    return {"title": title, "value": value, "delta": delta}


def simple_file_uploader_label(filename: str) -> str:
    """Produce a consistent label for a file uploader for a given file.

    Keeps pages consistent and simplifies tests.
    """
    return f"Upload {filename}"


def progress_message(stage: str, details: Optional[str] = None) -> str:
    """Return a standard progress message string."""
    if details:
        return f"{stage}: {details}"
    return stage
