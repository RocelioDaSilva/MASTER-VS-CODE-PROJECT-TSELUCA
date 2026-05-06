# GEESP-Angola Database Schema

**Version:** 1.0  
**Database:** PostgreSQL 12+  
**Extensions:** PostGIS 3.0+ (for geospatial data)  
**Purpose:** Central repository for baseline survey data, aptitude maps, and project monitoring

---

## Tables

### 1. `projects` — Project Metadata
Stores high-level project information.

```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL UNIQUE,
    country VARCHAR(100) DEFAULT 'Angola',
    region VARCHAR(100),
    start_date DATE,
    pi_name VARCHAR(255),
    pi_email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. `survey_sites` — Geographic Survey Locations
Stores baseline survey site locations and metadata.

```sql
CREATE TABLE survey_sites (
    id SERIAL PRIMARY KEY,
    project_id INT NOT NULL REFERENCES projects(id),
    site_code VARCHAR(50) UNIQUE NOT NULL,
    site_name VARCHAR(255),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    location_geom GEOMETRY(Point, 4326),
    zone INT DEFAULT 1,
    population_baseline INT,
    survey_date DATE,
    survey_team VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_survey_sites_location ON survey_sites USING GIST (location_geom);
```

### 3. `households` — Household Survey Records
Baseline household survey responses.

```sql
CREATE TABLE households (
    id SERIAL PRIMARY KEY,
    survey_site_id INT NOT NULL REFERENCES survey_sites(id),
    household_id VARCHAR(100) UNIQUE NOT NULL,
    head_of_household VARCHAR(255),
    household_size INT,
    annual_income_usd DECIMAL(12,2),
    has_electricity BOOLEAN DEFAULT FALSE,
    primary_energy_source VARCHAR(100),
    willingness_to_pay DECIMAL(10,2),
    distance_to_grid_km DECIMAL(8,2),
    survey_completed_on DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. `aptitude_results` — MCDA Aptitude Map Data
Stores pixel-level aptitude scores for locations.

```sql
CREATE TABLE aptitude_results (
    id SERIAL PRIMARY KEY,
    project_id INT NOT NULL REFERENCES projects(id),
    location_geom GEOMETRY(Point, 4326),
    solar_irradiance_kwh_m2 DECIMAL(10,2),
    population_density INT,
    distance_to_grid_km DECIMAL(8,2),
    slope_percent DECIMAL(6,2),
    ndvi_score DECIMAL(5,3),
    aptitude_score DECIMAL(5,2),
    aptitude_class VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_aptitude_location ON aptitude_results USING GIST (location_geom);
```

### 5. `lcoe_results` — LCOE Technology Comparison
Stores LCOE calculations for technologies at each site.

```sql
CREATE TABLE lcoe_results (
    id SERIAL PRIMARY KEY,
    survey_site_id INT NOT NULL REFERENCES survey_sites(id),
    technology VARCHAR(100),
    capacity_mw DECIMAL(6,2),
    lcoe_usd_per_mwh DECIMAL(10,2),
    capex_usd DECIMAL(15,2),
    opex_annual_usd DECIMAL(12,2),
    irr_percent DECIMAL(5,2),
    payback_years INT,
    recommended BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. `monitoring_timeseries` — Real-time Monitoring Data (Optional)
Time-series data from installed systems.

```sql
CREATE TABLE monitoring_timeseries (
    id BIGSERIAL PRIMARY KEY,
    survey_site_id INT REFERENCES survey_sites(id),
    timestamp TIMESTAMP NOT NULL,
    solar_generation_kwh DECIMAL(10,3),
    battery_state_of_charge_percent INT,
    system_efficiency_percent DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_monitoring_timestamp ON monitoring_timeseries(timestamp);
CREATE INDEX idx_monitoring_site ON monitoring_timeseries(survey_site_id);
```

---

## Initialization Script

Run this to initialize the database:

```sql
-- Enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Import all tables as defined above
-- (copy full CREATE TABLE statements into PostgreSQL)

-- Grant access
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO geesp_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO geesp_user;
```

---

## Notes

- **Geospatial Queries:** Use `ST_Distance()`, `ST_Within()` for location-based queries
- **Backup:** `pg_dump geesp_angola > backup_$(date +%Y%m%d).sql`
- **Monitoring:** Add triggers for `updated_at` if needed
- **Scaling:** Partition `monitoring_timeseries` by time for large datasets

