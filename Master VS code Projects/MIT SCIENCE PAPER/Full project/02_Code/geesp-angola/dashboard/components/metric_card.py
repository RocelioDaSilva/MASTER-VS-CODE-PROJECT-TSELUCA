def render_card(title: str, value, delta: str = "") -> dict:
    """Return a simple serializable representation of a metric card.

    Designed so pages can call this and render with Streamlit when available.
    """
    return {"title": title, "value": value, "delta": delta}
