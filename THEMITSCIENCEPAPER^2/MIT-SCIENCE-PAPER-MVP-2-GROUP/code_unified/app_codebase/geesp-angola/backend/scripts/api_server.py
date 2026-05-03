"""Top-level shim to expose `app` at `scripts.api_server` for legacy tests."""
from .api.api_server import app

__all__ = ["app"]
