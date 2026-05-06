"""Canonical source: database/models.py. Re-exported here for backward compatibility."""
from database.models import Project, DailyGeneration, MaintenanceLog  # noqa: F401

__all__ = ["Project", "DailyGeneration", "MaintenanceLog"]

from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

# ============================================================================
# DATABASE MODELS
# ============================================================================


class Project(Base):
    """Project/Implementation site model"""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    project_id = Column(String(50), unique=True, nullable=False)
    community = Column(String(100), nullable=False)
    province = Column(String(100), nullable=False)
    status = Column(
        String(20), nullable=False
    )  # 'Operacional', 'Planejamento', 'Manutenção', 'Inativo'
    capacity_kw = Column(Float, nullable=False)
    installation_date = Column(DateTime, nullable=True)
    population_served = Column(Integer, nullable=False)
    annual_generation_mwh = Column(Float, nullable=False)
    system_health_percent = Column(Float, default=100.0)
    investment_usd = Column(Float, nullable=False)
    economic_status = Column(String(50), nullable=True)  # e.g., "ROI +12%"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "community": self.community,
            "province": self.province,
            "status": self.status,
            "capacity_kw": self.capacity_kw,
            "installation_date": self.installation_date,
            "population_served": self.population_served,
            "annual_generation_mwh": self.annual_generation_mwh,
            "system_health_percent": self.system_health_percent,
            "investment_usd": self.investment_usd,
            "economic_status": self.economic_status,
            "is_active": self.is_active,
        }


class DailyGeneration(Base):
    """Daily energy generation data"""

    __tablename__ = "daily_generation"

    id = Column(Integer, primary_key=True)
    project_id = Column(String(50), nullable=False)
    community = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False)
    generation_kwh = Column(Float, nullable=False)
    expected_generation_kwh = Column(Float, nullable=True)
    efficiency_percent = Column(Float, nullable=True)  # Calculated: actual/expected*100
    weather_condition = Column(String(20), nullable=True)  # 'sunny', 'cloudy', 'rainy'
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "community": self.community,
            "date": self.date,
            "generation_kwh": self.generation_kwh,
            "expected_generation_kwh": self.expected_generation_kwh,
            "efficiency_percent": self.efficiency_percent,
            "weather_condition": self.weather_condition,
        }


class MaintenanceLog(Base):
    """Maintenance and service records"""

    __tablename__ = "maintenance_logs"

    id = Column(Integer, primary_key=True)
    project = Column(String(100), nullable=False)
    maintenance_type = Column(String(100), nullable=False)  # 'Panel cleaning', 'Inspection', etc.
    date = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)  # 'Completed', 'In Progress', 'Scheduled'
    priority = Column(String(20), nullable=False)  # 'Low', 'Normal', 'High'
    description = Column(String(500), nullable=True)
    technician_name = Column(String(100), nullable=True)
    cost_usd = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "project": self.project,
            "maintenance_type": self.maintenance_type,
            "date": self.date,
            "status": self.status,
            "priority": self.priority,
            "description": self.description,
            "technician_name": self.technician_name,
            "cost_usd": self.cost_usd,
        }


class SystemHealthMetric(Base):
    """Historical system health measurements"""

    __tablename__ = "system_health_metrics"

    id = Column(Integer, primary_key=True)
    project_id = Column(String(50), nullable=False)
    community = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False)
    health_score = Column(Float, nullable=False)  # 0-100
    panel_efficiency_percent = Column(Float, nullable=True)
    inverter_status = Column(String(20), nullable=True)  # 'OK', 'Warning', 'Error'
    battery_status = Column(String(20), nullable=True)  # 'OK', 'Warning', 'Error'
    grid_connection_ok = Column(Boolean, nullable=True)
    last_inspection_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "community": self.community,
            "date": self.date,
            "health_score": self.health_score,
            "panel_efficiency_percent": self.panel_efficiency_percent,
            "inverter_status": self.inverter_status,
            "battery_status": self.battery_status,
            "grid_connection_ok": self.grid_connection_ok,
            "last_inspection_date": self.last_inspection_date,
        }


class KeyPerformanceIndicator(Base):
    """KPI snapshots (daily/weekly/monthly aggregates)"""

    __tablename__ = "kpis"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    period = Column(String(20), nullable=False)  # 'daily', 'weekly', 'monthly'
    total_systems_operational = Column(Integer, nullable=False)
    total_capacity_kw = Column(Float, nullable=False)
    total_population_served = Column(Integer, nullable=False)
    total_generation_mwh = Column(Float, nullable=False)
    average_system_health = Column(Float, nullable=False)
    total_maintenance_cost_usd = Column(Float, nullable=True)
    co2_avoided_tons = Column(Float, nullable=True)
    roi_percent = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "date": self.date,
            "period": self.period,
            "total_systems_operational": self.total_systems_operational,
            "total_capacity_kw": self.total_capacity_kw,
            "total_population_served": self.total_population_served,
            "total_generation_mwh": self.total_generation_mwh,
            "average_system_health": self.average_system_health,
            "total_maintenance_cost_usd": self.total_maintenance_cost_usd,
            "co2_avoided_tons": self.co2_avoided_tons,
            "roi_percent": self.roi_percent,
        }


# ============================================================================
# DATABASE CONNECTION & SESSION MANAGEMENT
# ============================================================================


class DatabaseManager:
    """Manages database connections and sessions"""

    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database manager

        Args:
            database_url: SQLAlchemy connection string
                         Default: sqlite:///geesp_monitoring.db
        """
        if database_url is None:
            db_path = Path("data/sqlite/geesp_monitoring.db")
            db_path.parent.mkdir(parents=True, exist_ok=True)
            database_url = f"sqlite:///{db_path}"

        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        self._initialize()

    def _initialize(self):
        """Initialize database engine and create tables"""
        try:
            self.engine = create_engine(self.database_url, echo=False)
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )

            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            logger.info(f"✓ Database initialized: {self.database_url}")
        except Exception as e:
            logger.error(f"✗ Database initialization failed: {e}")
            raise

    def get_session(self) -> Session:
        """Get new database session"""
        return self.SessionLocal()

    def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            logger.info("✓ Database connection closed")


# ============================================================================
# QUERY HELPERS
# ============================================================================


class ProjectRepository:
    """Data access layer for projects"""

    def __init__(self, session: Session):
        self.session = session

    def get_all_active(self):
        """Get all active projects"""
        return self.session.query(Project).filter(Project.is_active == True).all()

    def get_by_status(self, status: str):
        """Get projects by status"""
        return (
            self.session.query(Project)
            .filter(Project.status == status, Project.is_active == True)
            .all()
        )

    def get_by_province(self, province: str):
        """Get projects by province"""
        return (
            self.session.query(Project)
            .filter(Project.province == province, Project.is_active == True)
            .all()
        )

    def get_by_id(self, project_id: str):
        """Get project by ID"""
        return (
            self.session.query(Project)
            .filter(Project.project_id == project_id)
            .first()
        )

    def create(self, **kwargs):
        """Create new project"""
        project = Project(**kwargs)
        self.session.add(project)
        self.session.commit()
        logger.info(f"✓ Project created: {project.project_id}")
        return project

    def update(self, project_id: str, **kwargs):
        """Update project"""
        project = self.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")

        for key, value in kwargs.items():
            setattr(project, key, value)
        project.updated_at = datetime.utcnow()
        self.session.commit()
        logger.info(f"✓ Project updated: {project_id}")
        return project


class GenerationRepository:
    """Data access layer for generation data"""

    def __init__(self, session: Session):
        self.session = session

    def get_latest_by_project(self, project_id: str, days: int = 30):
        """Get latest generation data for project"""
        from datetime import timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return (
            self.session.query(DailyGeneration)
            .filter(
                DailyGeneration.project_id == project_id,
                DailyGeneration.date >= cutoff_date,
            )
            .order_by(DailyGeneration.date.desc())
            .all()
        )

    def get_by_date_range(self, start_date, end_date):
        """Get generation data for date range"""
        return (
            self.session.query(DailyGeneration)
            .filter(DailyGeneration.date >= start_date, DailyGeneration.date <= end_date)
            .order_by(DailyGeneration.date)
            .all()
        )

    def create(self, **kwargs):
        """Create new generation record"""
        record = DailyGeneration(**kwargs)
        self.session.add(record)
        self.session.commit()
        return record


class MaintenanceRepository:
    """Data access layer for maintenance logs"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_project(self, project_name: str):
        """Get maintenance logs for project"""
        return (
            self.session.query(MaintenanceLog)
            .filter(MaintenanceLog.project == project_name)
            .order_by(MaintenanceLog.date.desc())
            .all()
        )

    def get_overdue(self):
        """Get overdue scheduled maintenance"""
        return (
            self.session.query(MaintenanceLog)
            .filter(
                MaintenanceLog.status == "Scheduled",
                MaintenanceLog.date < datetime.utcnow(),
            )
            .order_by(MaintenanceLog.priority.desc())
            .all()
        )

    def get_recent(self, cutoff_date):
        """Get recent maintenance records since cutoff_date"""
        return (
            self.session.query(MaintenanceLog)
            .filter(MaintenanceLog.date >= cutoff_date)
            .order_by(MaintenanceLog.date.desc())
            .all()
        )

    def create(self, **kwargs):
        """Create new maintenance record"""
        record = MaintenanceLog(**kwargs)
        self.session.add(record)
        self.session.commit()
        logger.info(f"✓ Maintenance record created for {record.project}")
        return record


class KPIRepository:
    """Data access layer for KPIs"""

    def __init__(self, session: Session):
        self.session = session

    def get_latest_daily(self):
        """Get latest daily KPI snapshot"""
        return (
            self.session.query(KeyPerformanceIndicator)
            .filter(KeyPerformanceIndicator.period == "daily")
            .order_by(KeyPerformanceIndicator.date.desc())
            .first()
        )

    def get_by_period(self, period: str, days: int = 30):
        """Get KPI snapshots for period"""
        from datetime import timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return (
            self.session.query(KeyPerformanceIndicator)
            .filter(
                KeyPerformanceIndicator.period == period,
                KeyPerformanceIndicator.date >= cutoff_date,
            )
            .order_by(KeyPerformanceIndicator.date)
            .all()
        )

    def create(self, **kwargs):
        """Create new KPI snapshot"""
        kpi = KeyPerformanceIndicator(**kwargs)
        self.session.add(kpi)
        self.session.commit()
        logger.info(f"✓ KPI snapshot created for {kwargs.get('period')} period")
        return kpi


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_db_manager: Optional[DatabaseManager] = None


def get_database_manager(database_url: Optional[str] = None) -> DatabaseManager:
    """Get or create singleton database manager"""
    global _db_manager

    if _db_manager is None:
        _db_manager = DatabaseManager(database_url)

    return _db_manager


if __name__ == "__main__":
    # Example usage
    db = get_database_manager()
    session = db.get_session()

    # Create project
    project_repo = ProjectRepository(session)
    project = project_repo.create(
        project_id="PRJ-TEST-001",
        community="Test Community",
        province="Huíla",
        status="Operacional",
        capacity_kw=50.0,
        population_served=500,
        annual_generation_mwh=87.5,
        investment_usd=150000,
    )

    logger.info(f"Created project: {project.project_id}")

    # Query project
    retrieved = project_repo.get_by_id("PRJ-TEST-001")
    logger.info(f"Retrieved project: {retrieved.community if retrieved else 'Not found'}")

    session.close()
