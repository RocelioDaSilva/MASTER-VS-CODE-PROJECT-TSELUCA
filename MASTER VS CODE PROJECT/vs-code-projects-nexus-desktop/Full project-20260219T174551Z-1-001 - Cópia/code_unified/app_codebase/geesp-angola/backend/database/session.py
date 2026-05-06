"""
Database session management for GEESP-Angola.

Provides SQLAlchemy engine creation, session factory, and a FastAPI
dependency for per-request sessions with proper cleanup.
"""

import os
import logging
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from .models import Base

logger = logging.getLogger(__name__)

# Resolve database URL from environment or default to SQLite
DATABASE_URL = (
    os.getenv("GEESP_DATABASE_URL")
    or os.getenv("DATABASE_URL")
    or "sqlite:///data/sqlite/geesp.db"
)

# SQLite-specific: enable WAL mode and foreign keys for better concurrency
_connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=_connect_args,
    pool_pre_ping=True,
    echo=False,
)

if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create all tables that don't yet exist."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured")


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
