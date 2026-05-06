"""
Initial database migration: Create core tables

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-02-10

Creates tables for:
- projects (solar implementation sites)
- daily_generation (energy generation records)
- maintenance_logs (service records)
- system_health_metrics (health snapshots)
- kpis (aggregated key performance indicators)
"""

from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision = "001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial tables"""
    
    # Create projects table
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.String(50), nullable=False),
        sa.Column("community", sa.String(100), nullable=False),
        sa.Column("province", sa.String(100), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("capacity_kw", sa.Float(), nullable=False),
        sa.Column("installation_date", sa.DateTime(), nullable=True),
        sa.Column("population_served", sa.Integer(), nullable=False),
        sa.Column("annual_generation_mwh", sa.Float(), nullable=False),
        sa.Column("system_health_percent", sa.Float(), server_default="100.0"),
        sa.Column("investment_usd", sa.Float(), nullable=False),
        sa.Column("economic_status", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="1"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id"),
    )

    # Create daily_generation table
    op.create_table(
        "daily_generation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.String(50), nullable=False),
        sa.Column("community", sa.String(100), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("generation_kwh", sa.Float(), nullable=False),
        sa.Column("expected_generation_kwh", sa.Float(), nullable=True),
        sa.Column("efficiency_percent", sa.Float(), nullable=True),
        sa.Column("weather_condition", sa.String(20), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_daily_generation_project_id", "daily_generation", ["project_id"])
    op.create_index("ix_daily_generation_date", "daily_generation", ["date"])

    # Create maintenance_logs table
    op.create_table(
        "maintenance_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project", sa.String(100), nullable=False),
        sa.Column("maintenance_type", sa.String(100), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("priority", sa.String(20), nullable=False),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column("technician_name", sa.String(100), nullable=True),
        sa.Column("cost_usd", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_maintenance_logs_project", "maintenance_logs", ["project"])
    op.create_index("ix_maintenance_logs_date", "maintenance_logs", ["date"])

    # Create system_health_metrics table
    op.create_table(
        "system_health_metrics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.String(50), nullable=False),
        sa.Column("community", sa.String(100), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("health_score", sa.Float(), nullable=False),
        sa.Column("panel_efficiency_percent", sa.Float(), nullable=True),
        sa.Column("inverter_status", sa.String(20), nullable=True),
        sa.Column("battery_status", sa.String(20), nullable=True),
        sa.Column("grid_connection_ok", sa.Boolean(), nullable=True),
        sa.Column("last_inspection_date", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_system_health_project_id", "system_health_metrics", ["project_id"])
    op.create_index("ix_system_health_date", "system_health_metrics", ["date"])

    # Create kpis table
    op.create_table(
        "kpis",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("period", sa.String(20), nullable=False),
        sa.Column("total_systems_operational", sa.Integer(), nullable=False),
        sa.Column("total_capacity_kw", sa.Float(), nullable=False),
        sa.Column("total_population_served", sa.Integer(), nullable=False),
        sa.Column("total_generation_mwh", sa.Float(), nullable=False),
        sa.Column("average_system_health", sa.Float(), nullable=False),
        sa.Column("total_maintenance_cost_usd", sa.Float(), nullable=True),
        sa.Column("co2_avoided_tons", sa.Float(), nullable=True),
        sa.Column("roi_percent", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_kpis_period", "kpis", ["period"])
    op.create_index("ix_kpis_date", "kpis", ["date"])


def downgrade() -> None:
    """Drop tables"""
    
    op.drop_index("ix_kpis_date", table_name="kpis")
    op.drop_index("ix_kpis_period", table_name="kpis")
    op.drop_table("kpis")
    
    op.drop_index("ix_system_health_date", table_name="system_health_metrics")
    op.drop_index("ix_system_health_project_id", table_name="system_health_metrics")
    op.drop_table("system_health_metrics")
    
    op.drop_index("ix_maintenance_logs_date", table_name="maintenance_logs")
    op.drop_index("ix_maintenance_logs_project", table_name="maintenance_logs")
    op.drop_table("maintenance_logs")
    
    op.drop_index("ix_daily_generation_date", table_name="daily_generation")
    op.drop_index("ix_daily_generation_project_id", table_name="daily_generation")
    op.drop_table("daily_generation")
    
    op.drop_table("projects")
