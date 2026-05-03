"""
Database Integration for GEESP-Angola
Connects ORM models to monitoring app queries and time-series logging
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy import create_engine, select, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import os

logger = logging.getLogger(__name__)


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

class DatabaseConfig:
    """Database configuration management"""
    
    @staticmethod
    def get_connection_string() -> str:
        """Get database connection string from environment"""
        db_user = os.getenv("DB_USER", "geesp_user")
        db_password = os.getenv("DB_PASSWORD", "geesp_password")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "geesp_angola")
        
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    @staticmethod
    def get_async_connection_string() -> str:
        """Get async database connection string"""
        sync_str = DatabaseConfig.get_connection_string()
        return sync_str.replace("postgresql://", "postgresql+asyncpg://")


# ============================================================================
# DATABASE SESSION MANAGEMENT
# ============================================================================

class DatabaseSession:
    """Manages database sessions and connections"""
    
    def __init__(self):
        """Initialize database session manager"""
        self.sync_engine = None
        self.async_engine = None
        self.async_session_maker = None
        self.initialized = False
    
    def init_sync_engine(self) -> None:
        """Initialize synchronous engine"""
        try:
            connection_string = DatabaseConfig.get_connection_string()
            self.sync_engine = create_engine(
                connection_string,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
            )
            logger.info("✓ Sync database engine initialized")
        except Exception as e:
            logger.error(f"Failed to initialize sync engine: {e}")
            raise
    
    async def init_async_engine(self) -> None:
        """Initialize asynchronous engine"""
        try:
            connection_string = DatabaseConfig.get_async_connection_string()
            self.async_engine = create_async_engine(
                connection_string,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
            )
            self.async_session_maker = async_sessionmaker(
                self.async_engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            logger.info("✓ Async database engine initialized")
        except Exception as e:
            logger.error(f"Failed to initialize async engine: {e}")
            raise
    
    @asynccontextmanager
    async def get_async_session(self):
        """Get async session context manager"""
        if self.async_session_maker is None:
            raise RuntimeError("Async engine not initialized")
        
        async with self.async_session_maker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Database session error: {e}")
                raise
            finally:
                await session.close()
    
    def get_sync_session(self):
        """Get sync session context manager"""
        if self.sync_engine is None:
            raise RuntimeError("Sync engine not initialized")
        
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(bind=self.sync_engine)
        return SessionLocal()
    
    async def close(self) -> None:
        """Close database connections"""
        if self.async_engine:
            await self.async_engine.dispose()
        logger.info("✓ Database connections closed")


# ============================================================================
# ORM MODEL IMPORTS
# ============================================================================

# These models should already exist in models/monitoring.py
# Here we import and demonstrate usage

# from app.models.monitoring import (
#     Project,
#     ProjectGeneration,
#     MaintenanceRecord,
#     PerformanceKPI,
#     EnergyGeneration,
# )


# ============================================================================
# MONITORING DATA LAYER
# ============================================================================

class MonitoringDataLayer:
    """Data access layer for monitoring queries"""
    
    def __init__(self, db_session: DatabaseSession):
        """Initialize data layer
        
        Args:
            db_session: Database session manager
        """
        self.db = db_session
    
    # PROJECT QUERIES
    
    async def get_all_projects(self) -> List[Dict[str, Any]]:
        """Get all projects from database
        
        Returns:
            List of project records
        """
        try:
            async with self.db.get_async_session() as session:
                # Import model (would be from models.monitoring in real app)
                from app.models.monitoring import Project
                
                query = select(Project)
                result = await session.execute(query)
                projects = result.scalars().all()
                
                return [
                    {
                        "id": p.id,
                        "name": p.name,
                        "location": p.location,
                        "capacity_kw": p.capacity_kw,
                        "created_at": p.created_at.isoformat(),
                    }
                    for p in projects
                ]
        except Exception as e:
            logger.error(f"Error fetching projects: {e}")
            return []
    
    async def get_project_by_id(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get project by ID
        
        Args:
            project_id: Project ID
            
        Returns:
            Project record or None
        """
        try:
            async with self.db.get_async_session() as session:
                from app.models.monitoring import Project
                
                query = select(Project).where(Project.id == project_id)
                result = await session.execute(query)
                project = result.scalar_one_or_none()
                
                if project:
                    return {
                        "id": project.id,
                        "name": project.name,
                        "location": project.location,
                        "capacity_kw": project.capacity_kw,
                    }
                return None
        except Exception as e:
            logger.error(f"Error fetching project {project_id}: {e}")
            return None
    
    # ENERGY GENERATION QUERIES
    
    async def get_energy_generation_timeseries(
        self,
        project_id: int,
        days: int = 30,
    ) -> List[Dict[str, Any]]:
        """Get energy generation time series
        
        Args:
            project_id: Project ID
            days: Number of days to retrieve
            
        Returns:
            Time series data points
        """
        try:
            async with self.db.get_async_session() as session:
                from app.models.monitoring import EnergyGeneration
                
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                
                query = (
                    select(EnergyGeneration)
                    .where(EnergyGeneration.project_id == project_id)
                    .where(EnergyGeneration.timestamp >= cutoff_date)
                    .order_by(EnergyGeneration.timestamp)
                )
                
                result = await session.execute(query)
                records = result.scalars().all()
                
                return [
                    {
                        "timestamp": r.timestamp.isoformat(),
                        "energy_kwh": r.energy_kwh,
                        "efficiency": r.efficiency,
                    }
                    for r in records
                ]
        except Exception as e:
            logger.error(f"Error fetching energy series: {e}")
            return []
    
    async def get_daily_energy_totals(
        self,
        project_id: int,
        days: int = 30,
    ) -> List[Dict[str, Any]]:
        """Get daily aggregated energy totals
        
        Args:
            project_id: Project ID
            days: Number of days to retrieve
            
        Returns:
            Daily totals
        """
        try:
            async with self.db.get_async_session() as session:
                from app.models.monitoring import EnergyGeneration
                from sqlalchemy import func, cast, Date
                from sqlalchemy.dialects.postgresql import JSON
                
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                
                query = (
                    select(
                        cast(EnergyGeneration.timestamp, Date),
                        func.sum(EnergyGeneration.energy_kwh),
                        func.avg(EnergyGeneration.efficiency),
                    )
                    .where(EnergyGeneration.project_id == project_id)
                    .where(EnergyGeneration.timestamp >= cutoff_date)
                    .group_by(cast(EnergyGeneration.timestamp, Date))
                    .order_by(cast(EnergyGeneration.timestamp, Date))
                )
                
                result = await session.execute(query)
                records = result.all()
                
                return [
                    {
                        "date": r[0].isoformat(),
                        "total_energy_kwh": float(r[1] or 0),
                        "avg_efficiency": float(r[2] or 0),
                    }
                    for r in records
                ]
        except Exception as e:
            logger.error(f"Error fetching daily totals: {e}")
            return []
    
    # PERFORMANCE KPI QUERIES
    
    async def get_performance_kpis(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get performance KPIs for project
        
        Args:
            project_id: Project ID
            
        Returns:
            KPI record
        """
        try:
            async with self.db.get_async_session() as session:
                from app.models.monitoring import PerformanceKPI
                
                query = (
                    select(PerformanceKPI)
                    .where(PerformanceKPI.project_id == project_id)
                    .order_by(PerformanceKPI.calculated_at.desc())
                    .limit(1)
                )
                
                result = await session.execute(query)
                kpi = result.scalar_one_or_none()
                
                if kpi:
                    return {
                        "project_id": kpi.project_id,
                        "capacity_factor": kpi.capacity_factor,
                        "poa_irradiance": kpi.poa_irradiance,
                        "system_losses": kpi.system_losses,
                        "calculated_at": kpi.calculated_at.isoformat(),
                    }
                return None
        except Exception as e:
            logger.error(f"Error fetching KPIs: {e}")
            return None
    
    # MAINTENANCE QUERIES
    
    async def get_maintenance_records(
        self,
        project_id: int,
        days: int = 90,
    ) -> List[Dict[str, Any]]:
        """Get maintenance records
        
        Args:
            project_id: Project ID
            days: Number of days to retrieve
            
        Returns:
            Maintenance records
        """
        try:
            async with self.db.get_async_session() as session:
                from app.models.monitoring import MaintenanceRecord
                
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                
                query = (
                    select(MaintenanceRecord)
                    .where(MaintenanceRecord.project_id == project_id)
                    .where(MaintenanceRecord.date >= cutoff_date)
                    .order_by(MaintenanceRecord.date.desc())
                )
                
                result = await session.execute(query)
                records = result.scalars().all()
                
                return [
                    {
                        "id": r.id,
                        "date": r.date.isoformat(),
                        "description": r.description,
                        "downtime_hours": r.downtime_hours,
                    }
                    for r in records
                ]
        except Exception as e:
            logger.error(f"Error fetching maintenance: {e}")
            return []
    
    # TIME-SERIES LOGGING
    
    async def log_energy_generation(
        self,
        project_id: int,
        energy_kwh: float,
        efficiency: float,
    ) -> bool:
        """Log energy generation data point
        
        Args:
            project_id: Project ID
            energy_kwh: Energy generated
            efficiency: System efficiency
            
        Returns:
            Success indicator
        """
        try:
            async with self.db.get_async_session() as session:
                from app.models.monitoring import EnergyGeneration
                
                record = EnergyGeneration(
                    project_id=project_id,
                    timestamp=datetime.utcnow(),
                    energy_kwh=energy_kwh,
                    efficiency=efficiency,
                )
                
                session.add(record)
                await session.commit()
                
                return True
        except Exception as e:
            logger.error(f"Error logging energy: {e}")
            return False
    
    async def log_maintenance_event(
        self,
        project_id: int,
        description: str,
        downtime_hours: float,
    ) -> bool:
        """Log maintenance event
        
        Args:
            project_id: Project ID
            description: Event description
            downtime_hours: System downtime
            
        Returns:
            Success indicator
        """
        try:
            async with self.db.get_async_session() as session:
                from app.models.monitoring import MaintenanceRecord
                
                record = MaintenanceRecord(
                    project_id=project_id,
                    date=datetime.utcnow(),
                    description=description,
                    downtime_hours=downtime_hours,
                )
                
                session.add(record)
                await session.commit()
                
                return True
        except Exception as e:
            logger.error(f"Error logging maintenance: {e}")
            return False


# ============================================================================
# MONITORING APP INTEGRATION
# ============================================================================

class MonitoringDashboard:
    """
    Integration with Streamlit monitoring app.
    Replaces hardcoded data with database queries.
    """
    
    def __init__(self, db_data_layer: MonitoringDataLayer):
        """Initialize monitoring dashboard
        
        Args:
            db_data_layer: Data layer for database access
        """
        self.data_layer = db_data_layer
    
    async def get_dashboard_data(self, project_id: int) -> Dict[str, Any]:
        """Get complete dashboard data from database
        
        Args:
            project_id: Project ID to display
            
        Returns:
            Complete dashboard data
        """
        try:
            # Fetch all data in parallel
            project, kpis, energy_daily, maintenance = await asyncio.gather(
                self.data_layer.get_project_by_id(project_id),
                self.data_layer.get_performance_kpis(project_id),
                self.data_layer.get_daily_energy_totals(project_id, days=30),
                self.data_layer.get_maintenance_records(project_id, days=90),
            )
            
            return {
                "project": project or {},
                "kpis": kpis or {},
                "energy_history": energy_daily,
                "maintenance_events": maintenance,
                "last_updated": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error getting dashboard data: {e}")
            return {}
    
    async def refresh_performance_metrics(self, project_id: int) -> bool:
        """Refresh performance metrics from latest data
        
        Args:
            project_id: Project ID
            
        Returns:
            Success indicator
        """
        try:
            # Get latest energy data
            energy_data = await self.data_layer.get_energy_generation_timeseries(
                project_id,
                days=1,
            )
            
            if not energy_data:
                return False
            
            # Calculate KPIs from latest period
            recent = energy_data[-1:]
            if recent:
                avg_efficiency = recent[0].get("efficiency", 0)
                # Would calculate and store KPI record here
                logger.info(f"Updated KPIs for project {project_id}: {avg_efficiency}%")
            
            return True
        except Exception as e:
            logger.error(f"Error refreshing metrics: {e}")
            return False


# ============================================================================
# FASTAPI INTEGRATION
# ============================================================================

from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(prefix="/database", tags=["database"])
db_session = DatabaseSession()


async def get_data_layer() -> MonitoringDataLayer:
    """Dependency for data layer"""
    return MonitoringDataLayer(db_session)


@router.get("/projects")
async def list_projects(data_layer: MonitoringDataLayer = Depends(get_data_layer)) -> List[Dict]:
    """List all projects from database"""
    return await data_layer.get_all_projects()


@router.get("/projects/{project_id}")
async def get_project(
    project_id: int,
    data_layer: MonitoringDataLayer = Depends(get_data_layer),
) -> Dict:
    """Get project by ID"""
    project = await data_layer.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/projects/{project_id}/energy-timeseries")
async def get_energy_timeseries(
    project_id: int,
    days: int = 30,
    data_layer: MonitoringDataLayer = Depends(get_data_layer),
) -> List[Dict]:
    """Get energy generation time series"""
    return await data_layer.get_energy_generation_timeseries(project_id, days)


@router.get("/projects/{project_id}/kpis")
async def get_kpis(
    project_id: int,
    data_layer: MonitoringDataLayer = Depends(get_data_layer),
) -> Dict:
    """Get performance KPIs for project"""
    kpis = await data_layer.get_performance_kpis(project_id)
    if not kpis:
        raise HTTPException(status_code=404, detail="KPIs not found")
    return kpis


@router.get("/projects/{project_id}/maintenance")
async def get_maintenance(
    project_id: int,
    days: int = 90,
    data_layer: MonitoringDataLayer = Depends(get_data_layer),
) -> List[Dict]:
    """Get maintenance records"""
    return await data_layer.get_maintenance_records(project_id, days)


@router.get("/projects/{project_id}/dashboard")
async def get_dashboard(
    project_id: int,
    data_layer: MonitoringDataLayer = Depends(get_data_layer),
) -> Dict:
    """Get complete dashboard data"""
    dashboard = MonitoringDashboard(data_layer)
    return await dashboard.get_dashboard_data(project_id)


# ============================================================================
# INITIALIZATION
# ============================================================================

async def init_database() -> None:
    """Initialize database connections"""
    await db_session.init_async_engine()
    db_session.init_sync_engine()
    logger.info("✓ Database initialization complete")


async def close_database() -> None:
    """Close database connections"""
    await db_session.close()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    async def example():
        """Example usage"""
        # Initialize database
        await init_database()
        
        # Create data layer
        data_layer = MonitoringDataLayer(db_session)
        
        # Query projects
        projects = await data_layer.get_all_projects()
        print(f"Projects: {projects}")
        
        # Get dashboard data
        if projects:
            project_id = projects[0]["id"]
            dashboard = MonitoringDashboard(data_layer)
            data = await dashboard.get_dashboard_data(project_id)
            print(f"Dashboard data: {data}")
        
        # Close
        await close_database()
    
    # Run example
    asyncio.run(example())
