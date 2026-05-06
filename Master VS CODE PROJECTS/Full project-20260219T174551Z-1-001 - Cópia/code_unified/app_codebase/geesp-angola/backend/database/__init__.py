"""
GEESP-Angola database models package.

Consolidated model definitions for:
- Scenario management
- Analysis results
- Operational monitoring
- Site evaluations
- Map metadata

Exports all SQLAlchemy ORM classes and utilities for database management.
"""

from .models import (
    # Base declarative
    Base,
    # Scenario models
    Scenario,
    # Analysis result models
    AnalysisResult,
    ResultsMetadata,
    SiteEvaluation,
    Map,
    # Operational monitoring models
    Project,
    DailyGeneration,
    MaintenanceLog,
    # Utilities
    create_all_tables,
    drop_all_tables,
)

from .session import (
    engine,
    SessionLocal,
    init_db,
    get_db,
)

__all__ = [
    # Base
    "Base",
    # Scenario
    "Scenario",
    # Analysis
    "AnalysisResult",
    "ResultsMetadata",
    "SiteEvaluation",
    "Map",
    # Projects
    "Project",
    "DailyGeneration",
    "MaintenanceLog",
    # Utilities
    "create_all_tables",
    "drop_all_tables",
    # Session
    "engine",
    "SessionLocal",
    "init_db",
    "get_db",
]
