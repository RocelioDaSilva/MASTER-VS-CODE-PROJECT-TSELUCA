"""
Unified SQLAlchemy ORM models for GEESP-Angola database.

This consolidated module contains all database models for:
- User authentication
- Scenario management
- Analysis results
- Operational monitoring
- Site evaluations

Consolidates original models from:
- backend/models/scenario.py
- backend/models/results.py  
- backend/models/models/monitoring.py
"""

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Create declarative base
Base = declarative_base()


# ============================================================================
# USER / AUTH MODELS
# ============================================================================


class User(Base):
    """User model for authentication."""

    __tablename__ = "users"

    id = Column(String(50), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


# ============================================================================
# SCENARIO MODELS (from scenario.py)
# ============================================================================


class Scenario(Base):
    """
    Scenario model for solar energy planning.
    
    Represents a solar suitability analysis scenario with configuration
    parameters for LCOE and MCDA calculations.
    
    Attributes:
        id: Primary key (string identifier)
        name: Scenario name
        description: Scenario description
        location: Geographic location data (JSON)
        status: Scenario status (active, paused, archived)
        config: Scenario configuration (JSON)
        created_at: Creation timestamp
        updated_at: Last update timestamp
        created_by: User who created the scenario
        analysis_results: Relationship to AnalysisResult
        site_evaluations: Relationship to SiteEvaluation
        maps: Relationship to Map
    """
    
    __tablename__ = "scenarios"
    
    id = Column(String(50), primary_key=True, unique=True, nullable=False)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    location = Column(JSON, nullable=True)  # {"latitude": ..., "longitude": ...}
    status = Column(String(50), default="active", nullable=False)
    config = Column(JSON, default={}, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(255), nullable=True)
    
    # Relationships — lazy='select' (explicit default) prevents implicit N+1 queries.
    # Use joinedload() / selectinload() at the query site when batch-loading related rows.
    analysis_results = relationship("AnalysisResult", back_populates="scenario", cascade="all, delete-orphan", lazy="select")
    site_evaluations = relationship("SiteEvaluation", back_populates="scenario", cascade="all, delete-orphan", lazy="select")
    maps = relationship("Map", back_populates="scenario", cascade="all, delete-orphan", lazy="select")
    
    def __repr__(self) -> str:
        return f"<Scenario(id={self.id}, name={self.name}, status={self.status})>"


# ============================================================================
# ANALYSIS RESULT MODELS (from scenario.py & results.py)
# ============================================================================


class AnalysisResult(Base):
    """
    Analysis result model for storing computation outputs.
    
    Stores results from LCOE, MCDA, validation, and other analysis engines.
    
    Attributes:
        id: Primary key
        scenario_id: Foreign key to Scenario
        analysis_type: Type of analysis (mcda, lcoe, validation)
        status: Analysis status (pending, running, completed, failed)
        results: Analysis results (JSON)
        processing_time_ms: Processing time in milliseconds
        error_message: Error message if failed
        parameters: Input parameters (JSON)
        created_at: Creation timestamp
        scenario: Relationship to Scenario
    """
    
    __tablename__ = "analysis_results"
    
    id = Column(String(50), primary_key=True, unique=True, nullable=False)
    scenario_id = Column(String(50), ForeignKey("scenarios.id"), nullable=False, index=True)
    analysis_type = Column(String(50), nullable=False)  # mcda, lcoe, validation
    status = Column(String(50), default="pending", nullable=False)  # pending, running, completed, failed
    results = Column(JSON, default={}, nullable=False)
    processing_time_ms = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    parameters = Column(JSON, default={}, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    scenario = relationship("Scenario", back_populates="analysis_results", lazy="select")
    
    def __repr__(self) -> str:
        return f"<AnalysisResult(id={self.id}, scenario={self.scenario_id}, type={self.analysis_type})>"


class ResultsMetadata(Base):
    """
    Results metadata model for tracking analysis outputs.
    
    Stores detailed metrics and measurement metadata from analysis sessions.
    
    Attributes:
        id: Primary key
        analysis_id: Foreign key to analysis
        metric_type: Type of metric (lcoe, ranking, score, etc.)
        value: Numeric result value
        unit: Unit of measurement
        confidence_interval: Confidence level
        metadata: Additional metadata (JSON)
        created_at: Creation timestamp
    """
    
    __tablename__ = "results_metadata"
    
    id = Column(String(50), primary_key=True, unique=True, nullable=False)
    analysis_id = Column(String(50), nullable=False, index=True)
    metric_type = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=True)
    confidence_interval = Column(Float, nullable=True)
    metadata = Column(JSON, default={}, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<ResultsMetadata(analysis={self.analysis_id}, type={self.metric_type}, value={self.value})>"


class SiteEvaluation(Base):
    """
    Site evaluation results model.
    
    Stores suitability scores and evaluation results for individual sites
    within a scenario's geographic region.
    
    Attributes:
        id: Primary key
        scenario_id: Foreign key to scenario
        site_name: Site name/identifier
        location: Site location (JSON with lat/lon)
        suitability_score: Overall suitability score (0-100)
        lcoe: Levelized Cost of Electricity ($/kWh)
        ranking: Site ranking within scenario
        recommendations: Site-specific recommendations (JSON)
        created_at: Creation timestamp
        scenario: Relationship to Scenario
    """
    
    __tablename__ = "site_evaluations"
    
    id = Column(String(50), primary_key=True, unique=True, nullable=False)
    scenario_id = Column(String(50), ForeignKey("scenarios.id"), nullable=False, index=True)
    site_name = Column(String(255), nullable=False)
    location = Column(JSON, nullable=False)  # {"latitude": ..., "longitude": ...}
    suitability_score = Column(Float, nullable=False)  # 0-100
    lcoe = Column(Float, nullable=True)  # $/kWh
    ranking = Column(Float, nullable=True)
    recommendations = Column(JSON, default={}, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    scenario = relationship("Scenario", back_populates="site_evaluations")
    
    def __repr__(self) -> str:
        return f"<SiteEvaluation(site={self.site_name}, score={self.suitability_score})>"


class Map(Base):
    """
    Generated map metadata model.
    
    Tracks metadata about maps generated from analysis results.
    
    Attributes:
        id: Primary key
        scenario_id: Foreign key to scenario
        map_type: Type of map (suitability, lcoe, risk, etc.)
        file_path: Path to generated map file
        format: Map file format (PDF, PNG, GeoJSON, etc.)
        created_at: Creation timestamp
        scenario: Relationship to Scenario
    """
    
    __tablename__ = "maps"
    
    id = Column(String(50), primary_key=True, unique=True, nullable=False)
    scenario_id = Column(String(50), ForeignKey("scenarios.id"), nullable=False, index=True)
    map_type = Column(String(50), nullable=False)  # suitability, lcoe, risk, etc.
    file_path = Column(String(512), nullable=False)
    format = Column(String(20), default="pdf", nullable=False)  # pdf, png, geojson
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    scenario = relationship("Scenario", back_populates="maps")
    
    def __repr__(self) -> str:
        return f"<Map(scenario={self.scenario_id}, type={self.map_type}, format={self.format})>"


# ============================================================================
# OPERATIONAL MONITORING MODELS (from monitoring.py)
# ============================================================================


class Project(Base):
    """
    Project/Implementation site model for operational tracking.
    
    Represents a real-world solar project deployment and its operational status.
    
    Attributes:
        id: Primary key (integer)
        project_id: String identifier for project
        community: Community/location name
        province: Province/region
        status: Project status ('Operacional', 'Planejamento', 'Manutenção', 'Inativo')
        capacity_kw: System capacity in kilowatts
        installation_date: Date system was installed
        population_served: Number of people served
        annual_generation_mwh: Expected annual generation in MWh
        system_health_percent: Current system health percentage
        investment_usd: Total investment in USD
        economic_status: Economic status summary (e.g., "ROI +12%")
        created_at: Record creation timestamp
        updated_at: Last update timestamp
        is_active: Whether project is actively monitored
        daily_generation: Relationship to DailyGeneration records
        maintenance_logs: Relationship to MaintenanceLog records
    """
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(String(50), unique=True, nullable=False)
    community = Column(String(100), nullable=False)
    province = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)  # 'Operacional', 'Planejamento', 'Manutenção', 'Inativo'
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
    
    # Relationships
    daily_generation = relationship("DailyGeneration", back_populates="project", cascade="all, delete-orphan")
    maintenance_logs = relationship("MaintenanceLog", back_populates="project", cascade="all, delete-orphan")
    
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
    
    def __repr__(self) -> str:
        return f"<Project(project_id={self.project_id}, community={self.community}, status={self.status})>"


class DailyGeneration(Base):
    """
    Daily energy generation data model.
    
    Tracks daily power generation metrics for operational monitoring.
    
    Attributes:
        id: Primary key
        project_id: String identifier for project
        community: Community reference
        date: Date of generation record
        generation_kwh: Actual generation in kWh
        expected_generation_kwh: Expected generation in kWh  
        efficiency_percent: Calculated efficiency (actual/expected*100)
        weather_condition: Weather conditions ('sunny', 'cloudy', 'rainy')
        created_at: Record creation timestamp
        project: Relationship to Project
    """
    
    __tablename__ = "daily_generation"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(String(50), ForeignKey("projects.project_id"), nullable=False, index=True)
    community = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False)
    generation_kwh = Column(Float, nullable=False)
    expected_generation_kwh = Column(Float, nullable=True)
    efficiency_percent = Column(Float, nullable=True)  # Calculated: actual/expected*100
    weather_condition = Column(String(20), nullable=True)  # 'sunny', 'cloudy', 'rainy'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="daily_generation")
    
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
    
    def __repr__(self) -> str:
        return f"<DailyGeneration(project={self.project_id}, date={self.date}, kwh={self.generation_kwh})>"


class MaintenanceLog(Base):
    """
    Maintenance and service records model.
    
    Tracks maintenance activities, repairs, and service events for projects.
    
    Attributes:
        id: Primary key
        project_id: String identifier for project
        project: Relationship to Project
        date: Date of maintenance
        maintenance_type: Type of maintenance (preventive, corrective, etc.)
        description: Description of work performed
        technician: Name of technician
        duration_hours: Duration of maintenance in hours
        parts_replaced: Parts that were replaced (JSON list)
        cost_usd: Cost of maintenance in USD
        notes: Additional notes
        created_at: Record creation timestamp
    """
    
    __tablename__ = "maintenance_logs"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(String(100), ForeignKey("projects.project_id"), nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    maintenance_type = Column(String(50), nullable=True)  # preventive, corrective, etc.
    description = Column(Text, nullable=False)
    technician = Column(String(100), nullable=True)
    duration_hours = Column(Float, nullable=True)
    parts_replaced = Column(JSON, default=[], nullable=False)
    cost_usd = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="maintenance_logs")
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "date": self.date,
            "maintenance_type": self.maintenance_type,
            "description": self.description,
            "technician": self.technician,
            "duration_hours": self.duration_hours,
            "parts_replaced": self.parts_replaced,
            "cost_usd": self.cost_usd,
            "notes": self.notes,
        }
    
    def __repr__(self) -> str:
        return f"<MaintenanceLog(project={self.project_id}, date={self.date}, type={self.maintenance_type})>"


# ============================================================================
# Database Initialization Helper
# ============================================================================


def create_all_tables(engine):
    """Create all tables in the database."""
    Base.metadata.create_all(engine)


def drop_all_tables(engine):
    """Drop all tables from the database (use with caution!)."""
    Base.metadata.drop_all(engine)
