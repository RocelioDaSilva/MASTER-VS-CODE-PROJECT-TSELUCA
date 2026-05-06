"""Compatibility shim: re-export setup_project_paths for legacy imports

Some archived tests import `utils.import_helpers.setup_project_paths`.
This small shim keeps that import path working and delegates to the
consolidated `utils.helpers.setup_project_paths` implementation.
"""
from .helpers import setup_project_paths

__all__ = ["setup_project_paths"]
