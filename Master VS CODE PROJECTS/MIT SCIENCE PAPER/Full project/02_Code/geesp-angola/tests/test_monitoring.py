"""
Tests for GEESP-Angola Monitoring System
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add monitoring module to path
monitoring_path = Path(__file__).parent.parent / "monitoring"
sys.path.insert(0, str(monitoring_path))


def test_monitoring_app_imports():
    """Verify monitoring app can be imported (skip if streamlit/plotly/sqlalchemy missing)"""
    pytest.importorskip("sqlalchemy")
    try:
        import monitoring_app

        assert True
    except ImportError as e:
        # Skip test if dependencies not installed (e.g., local dev without pip install)
        if "streamlit" in str(e) or "plotly" in str(e):
            pytest.skip(f"Skipping test: required package not installed ({e})")
        else:
            pytest.fail(f"Monitoring app import failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error importing monitoring app: {e}")


def test_monitoring_data_structure():
    """Verify sample data has correct structure"""
    sample_projects = pd.DataFrame(
        {
            "Project_ID": ["PRJ-001", "PRJ-002"],
            "Community": ["Cacula", "Humpata"],
            "Province": ["Huíla", "Huíla"],
            "Status": ["Operacional", "Operacional"],
            "Capacity_kW": [50, 75],
            "Installation_Date": ["2025-06-15", "2025-07-20"],
            "Population_Served": [850, 1200],
            "Annual_Generation_MWh": [87.5, 131.25],
            "System_Health": [95, 92],
            "Investment_USD": [150000, 225000],
            "Economic_Status": ["ROI +12%", "ROI +8%"],
        }
    )

    # Check columns
    expected_cols = [
        "Project_ID",
        "Community",
        "Province",
        "Status",
        "Capacity_kW",
        "Installation_Date",
        "Population_Served",
        "Annual_Generation_MWh",
        "System_Health",
        "Investment_USD",
        "Economic_Status",
    ]

    for col in expected_cols:
        assert col in sample_projects.columns, f"Missing column: {col}"

    # Check data types
    assert sample_projects["Capacity_kW"].dtype in ["int64", "float64"]
    assert sample_projects["Population_Served"].dtype in ["int64", "float64"]
    assert sample_projects["System_Health"].dtype in ["int64", "float64"]


def test_monitoring_metrics_calculation():
    """Verify basic metric calculations"""
    sample_projects = pd.DataFrame(
        {
            "Status": ["Operacional", "Operacional", "Planejamento"],
            "Capacity_kW": [50, 75, 100],
            "Population_Served": [850, 1200, 1500],
            "System_Health": [95, 92, None],
        }
    )

    operacional = len(sample_projects[sample_projects["Status"] == "Operacional"])
    assert operacional == 2, "Operacional count incorrect"

    total_capacity = sample_projects[sample_projects["Status"] == "Operacional"][
        "Capacity_kW"
    ].sum()
    assert total_capacity == 125, "Total capacity calculation incorrect"

    total_pop = sample_projects[sample_projects["Status"] == "Operacional"][
        "Population_Served"
    ].sum()
    assert total_pop == 2050, "Total population calculation incorrect"

    avg_health = sample_projects[sample_projects["Status"] == "Operacional"][
        "System_Health"
    ].mean()
    assert abs(avg_health - 93.5) < 0.01, "Average health calculation incorrect"


def test_maintenance_data_structure():
    """Verify maintenance data structure"""
    sample_maintenance = pd.DataFrame(
        {
            "Project": ["Cacula", "Humpata"],
            "Type": ["Limpeza painéis", "Inspeção anual"],
            "Date": ["2025-08-15", "2025-08-10"],
            "Status": ["Concluído", "Concluído"],
            "Priority": ["Normal", "Normal"],
        }
    )

    expected_cols = ["Project", "Type", "Date", "Status", "Priority"]
    for col in expected_cols:
        assert col in sample_maintenance.columns, f"Missing column: {col}"

    assert len(sample_maintenance) >= 2, "Maintenance data too small"


def test_monitoring_app_file_exists():
    """Verify monitoring app file exists"""
    app_path = Path(__file__).parent.parent / "monitoring" / "monitoring_app.py"
    assert app_path.exists(), f"Monitoring app file not found at {app_path}"


def test_launch_script_exists():
    """Verify launch scripts exist"""
    bat_path = Path(__file__).parent.parent / "run_monitoring.bat"
    sh_path = Path(__file__).parent.parent / "run_monitoring.sh"

    assert bat_path.exists(), "Windows launch script (run_monitoring.bat) not found"
    assert sh_path.exists(), "Unix launch script (run_monitoring.sh) not found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
