"""
Database Model Tests
Tests for ORM models and data access layers
"""

import pytest
from pathlib import Path
import sys

# Skip entire module if sqlalchemy not installed (e.g. minimal env)
pytest.importorskip("sqlalchemy")

from datetime import datetime, timedelta
import tempfile

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "models"))

from models.monitoring import (
    DatabaseManager,
    Project,
    DailyGeneration,
    MaintenanceLog,
    SystemHealthMetric,
    KeyPerformanceIndicator,
    ProjectRepository,
    GenerationRepository,
    MaintenanceRepository,
    KPIRepository,
    get_database_manager,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_db():
    """Create temporary in-memory database for testing"""
    return DatabaseManager("sqlite:///:memory:")


@pytest.fixture
def session(temp_db):
    """Get session from temporary database"""
    sess = temp_db.get_session()
    yield sess
    sess.close()


# ============================================================================
# PROJECT MODEL TESTS
# ============================================================================

class TestProjectModel:
    """Test Project ORM model"""

    def test_project_creation(self, session):
        """Test creating a project"""
        project = Project(
            project_id="PRJ-001",
            community="Cacula",
            province="Huíla",
            status="Operacional",
            capacity_kw=50.0,
            population_served=850,
            annual_generation_mwh=87.5,
            investment_usd=150000,
        )

        session.add(project)
        session.commit()

        # Verify
        retrieved = session.query(Project).filter_by(project_id="PRJ-001").first()
        assert retrieved is not None
        assert retrieved.community == "Cacula"
        assert retrieved.status == "Operacional"

    def test_project_default_values(self, session):
        """Test project default values"""
        project = Project(
            project_id="PRJ-002",
            community="Test",
            province="Test",
            status="Planejamento",
            capacity_kw=100.0,
            population_served=500,
            annual_generation_mwh=100.0,
            investment_usd=200000,
        )

        session.add(project)
        session.commit()

        retrieved = session.query(Project).filter_by(project_id="PRJ-002").first()
        assert retrieved.system_health_percent == 100.0
        assert retrieved.is_active == True
        assert retrieved.created_at is not None

    def test_project_to_dict(self, session):
        """Test project serialization"""
        project = Project(
            project_id="PRJ-003",
            community="Test",
            province="Test",
            status="Operacional",
            capacity_kw=50.0,
            population_served=500,
            annual_generation_mwh=87.5,
            investment_usd=150000,
        )

        session.add(project)
        session.commit()

        retrieved = session.query(Project).filter_by(project_id="PRJ-003").first()
        proj_dict = retrieved.to_dict()

        assert proj_dict["project_id"] == "PRJ-003"
        assert proj_dict["community"] == "Test"
        assert proj_dict["capacity_kw"] == 50.0
        assert proj_dict["is_active"] == True


class TestDailyGenerationModel:
    """Test DailyGeneration ORM model"""

    def test_generation_record_creation(self, session):
        """Test creating generation record"""
        record = DailyGeneration(
            project_id="PRJ-001",
            community="Cacula",
            date=datetime(2025, 8, 15),
            generation_kwh=240.5,
            expected_generation_kwh=250.0,
        )

        session.add(record)
        session.commit()

        # Verify
        retrieved = session.query(DailyGeneration).filter_by(project_id="PRJ-001").first()
        assert retrieved is not None
        assert retrieved.generation_kwh == 240.5

    def test_generation_efficiency_calculation(self, session):
        """Test efficiency calculation"""
        record = DailyGeneration(
            project_id="PRJ-001",
            community="Cacula",
            date=datetime(2025, 8, 15),
            generation_kwh=240.0,
            expected_generation_kwh=250.0,
            efficiency_percent=96.0,
        )

        session.add(record)
        session.commit()

        retrieved = session.query(DailyGeneration).filter_by(project_id="PRJ-001").first()
        assert retrieved.efficiency_percent == 96.0


class TestMaintenanceLogModel:
    """Test MaintenanceLog ORM model"""

    def test_maintenance_record_creation(self, session):
        """Test creating maintenance record"""
        record = MaintenanceLog(
            project="Cacula",
            maintenance_type="Panel Cleaning",
            date=datetime(2025, 8, 20),
            status="Completed",
            priority="Normal",
            cost_usd=150.0,
        )

        session.add(record)
        session.commit()

        retrieved = session.query(MaintenanceLog).filter_by(project="Cacula").first()
        assert retrieved is not None
        assert retrieved.maintenance_type == "Panel Cleaning"
        assert retrieved.status == "Completed"


class TestSystemHealthMetricModel:
    """Test SystemHealthMetric ORM model"""

    def test_health_metric_creation(self, session):
        """Test creating health metric"""
        record = SystemHealthMetric(
            project_id="PRJ-001",
            community="Cacula",
            date=datetime(2025, 8, 20),
            health_score=95.0,
            panel_efficiency_percent=94.5,
            inverter_status="OK",
            battery_status="OK",
            grid_connection_ok=True,
        )

        session.add(record)
        session.commit()

        retrieved = session.query(SystemHealthMetric).filter_by(project_id="PRJ-001").first()
        assert retrieved is not None
        assert retrieved.health_score == 95.0
        assert retrieved.inverter_status == "OK"


class TestKPIModel:
    """Test KeyPerformanceIndicator ORM model"""

    def test_kpi_creation(self, session):
        """Test creating KPI snapshot"""
        kpi = KeyPerformanceIndicator(
            date=datetime(2025, 8, 20),
            period="daily",
            total_systems_operational=3,
            total_capacity_kw=200.0,
            total_population_served=3050,
            total_generation_mwh=543.75,
            average_system_health=90.5,
        )

        session.add(kpi)
        session.commit()

        retrieved = (
            session.query(KeyPerformanceIndicator)
            .filter_by(period="daily")
            .first()
        )
        assert retrieved is not None
        assert retrieved.total_systems_operational == 3
        assert retrieved.average_system_health == 90.5


# ============================================================================
# REPOSITORY TESTS
# ============================================================================

class TestProjectRepository:
    """Test ProjectRepository data access"""

    def test_get_all_active(self, session):
        """Test getting all active projects"""
        # Create test projects
        for i in range(3):
            project = Project(
                project_id=f"PRJ-{i:03d}",
                community=f"Community {i}",
                province="Huíla",
                status="Operacional",
                capacity_kw=50.0 + i * 10,
                population_served=500 + i * 100,
                annual_generation_mwh=87.5 + i * 10,
                investment_usd=150000,
                is_active=True,
            )
            session.add(project)

        session.commit()

        repo = ProjectRepository(session)
        active_projects = repo.get_all_active()

        assert len(active_projects) == 3

    def test_get_by_status(self, session):
        """Test getting projects by status"""
        # Create projects with different statuses
        for status in ["Operacional", "Planejamento", "Manutenção"]:
            project = Project(
                project_id=f"PRJ-{status}",
                community=f"Community {status}",
                province="Huíla",
                status=status,
                capacity_kw=50.0,
                population_served=500,
                annual_generation_mwh=87.5,
                investment_usd=150000,
            )
            session.add(project)

        session.commit()

        repo = ProjectRepository(session)
        operational = repo.get_by_status("Operacional")

        assert len(operational) == 1
        assert operational[0].status == "Operacional"

    def test_get_by_province(self, session):
        """Test getting projects by province"""
        for province in ["Huíla", "Gaza", "Huíla"]:
            project = Project(
                project_id=f"PRJ-{province}-{id(type)}",
                community=f"Community in {province}",
                province=province,
                status="Operacional",
                capacity_kw=50.0,
                population_served=500,
                annual_generation_mwh=87.5,
                investment_usd=150000,
            )
            session.add(project)

        session.commit()

        repo = ProjectRepository(session)
        huila_projects = repo.get_by_province("Huíla")

        assert len(huila_projects) == 2

    def test_create_project(self, session):
        """Test creating project via repository"""
        repo = ProjectRepository(session)
        project = repo.create(
            project_id="PRJ-CREATE",
            community="New Community",
            province="Huíla",
            status="Operacional",
            capacity_kw=50.0,
            population_served=500,
            annual_generation_mwh=87.5,
            investment_usd=150000,
        )

        assert project.project_id == "PRJ-CREATE"
        
        # Verify it was saved
        retrieved = repo.get_by_id("PRJ-CREATE")
        assert retrieved is not None

    def test_update_project(self, session):
        """Test updating project via repository"""
        repo = ProjectRepository(session)
        repo.create(
            project_id="PRJ-UPDATE",
            community="Original",
            province="Huíla",
            status="Planejamento",
            capacity_kw=50.0,
            population_served=500,
            annual_generation_mwh=87.5,
            investment_usd=150000,
        )

        # Update
        updated = repo.update("PRJ-UPDATE", status="Operacional", capacity_kw=75.0)

        assert updated.status == "Operacional"
        assert updated.capacity_kw == 75.0


class TestGenerationRepository:
    """Test GenerationRepository data access"""

    def test_get_latest_by_project(self, session):
        """Test getting latest generation records"""
        # Create records
        for i in range(5):
            date = datetime.now() - timedelta(days=5 - i)
            record = DailyGeneration(
                project_id="PRJ-001",
                community="Cacula",
                date=date,
                generation_kwh=240.0 + i * 10,
            )
            session.add(record)

        session.commit()

        repo = GenerationRepository(session)
        records = repo.get_latest_by_project("PRJ-001", days=30)

        assert len(records) == 5

    def test_get_by_date_range(self, session):
        """Test getting records by date range"""
        start_date = datetime(2025, 8, 1)
        end_date = datetime(2025, 8, 31)

        # Create records
        for i in range(30):
            date = start_date + timedelta(days=i)
            record = DailyGeneration(
                project_id="PRJ-001",
                community="Cacula",
                date=date,
                generation_kwh=240.0,
            )
            session.add(record)

        session.commit()

        repo = GenerationRepository(session)
        records = repo.get_by_date_range(start_date, end_date)

        assert len(records) == 30


class TestMaintenanceRepository:
    """Test MaintenanceRepository data access"""

    def test_get_by_project(self, session):
        """Test getting maintenance records for project"""
        # Create records
        for i in range(3):
            record = MaintenanceLog(
                project="Cacula",
                maintenance_type=f"Type {i}",
                date=datetime.now() - timedelta(days=i),
                status="Completed",
                priority="Normal",
            )
            session.add(record)

        session.commit()

        repo = MaintenanceRepository(session)
        records = repo.get_by_project("Cacula")

        assert len(records) == 3

    def test_get_overdue(self, session):
        """Test getting overdue scheduled maintenance"""
        # Create overdue and scheduled records
        overdue = MaintenanceLog(
            project="Cacula",
            maintenance_type="Overdue Work",
            date=datetime.now() - timedelta(days=10),
            status="Scheduled",
            priority="High",
        )
        session.add(overdue)

        future = MaintenanceLog(
            project="Cacula",
            maintenance_type="Future Work",
            date=datetime.now() + timedelta(days=10),
            status="Scheduled",
            priority="Normal",
        )
        session.add(future)

        session.commit()

        repo = MaintenanceRepository(session)
        overdue_items = repo.get_overdue()

        assert len(overdue_items) == 1
        assert overdue_items[0].maintenance_type == "Overdue Work"


class TestKPIRepository:
    """Test KPIRepository data access"""

    def test_get_latest_daily(self, session):
        """Test getting latest daily KPI"""
        # Create KPIs
        for i in range(3):
            date = datetime.now() - timedelta(days=2 - i)
            kpi = KeyPerformanceIndicator(
                date=date,
                period="daily",
                total_systems_operational=3,
                total_capacity_kw=200.0 + i * 10,
                total_population_served=3050,
                total_generation_mwh=543.75,
                average_system_health=90.5,
            )
            session.add(kpi)

        session.commit()

        repo = KPIRepository(session)
        latest = repo.get_latest_daily()

        assert latest is not None
        assert latest.period == "daily"

    def test_get_by_period(self, session):
        """Test getting KPIs by period"""
        # Create KPIs for different periods
        for period in ["daily", "weekly", "monthly"]:
            for i in range(2):
                kpi = KeyPerformanceIndicator(
                    date=datetime.now() - timedelta(days=i),
                    period=period,
                    total_systems_operational=3,
                    total_capacity_kw=200.0,
                    total_population_served=3050,
                    total_generation_mwh=543.75,
                    average_system_health=90.5,
                )
                session.add(kpi)

        session.commit()

        repo = KPIRepository(session)
        daily_kpis = repo.get_by_period("daily", days=30)

        assert len(daily_kpis) >= 2


# ============================================================================
# DATABASE MANAGER TESTS
# ============================================================================

class TestDatabaseManager:
    """Test DatabaseManager"""

    def test_database_initialization(self):
        """Test database manager initialization"""
        db = DatabaseManager("sqlite:///:memory:")
        session = db.get_session()

        assert session is not None
        assert db.engine is not None
        assert db.SessionLocal is not None

    def test_singleton_pattern(self):
        """Test singleton pattern"""
        db1 = get_database_manager("sqlite:///:memory:")
        db2 = get_database_manager("sqlite:///:memory:")

        assert db1 is db2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
