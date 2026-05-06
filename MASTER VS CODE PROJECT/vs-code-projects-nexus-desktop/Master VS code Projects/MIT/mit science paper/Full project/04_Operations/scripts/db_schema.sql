-- GEESP-Angola: minimal DB schema for initialization
-- Idempotent SQL to create schema and essential tables

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS projects (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS survey_sites (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
  name TEXT,
  geom geometry(POINT, 4326),
  metadata JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS households (
  id SERIAL PRIMARY KEY,
  site_id INTEGER REFERENCES survey_sites(id) ON DELETE CASCADE,
  household_id TEXT,
  members INTEGER,
  income_estimate NUMERIC,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS aptitude_results (
  id SERIAL PRIMARY KEY,
  site_id INTEGER REFERENCES survey_sites(id) ON DELETE CASCADE,
  generated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  raster_file TEXT,
  summary JSONB
);

CREATE TABLE IF NOT EXISTS lcoe_results (
  id SERIAL PRIMARY KEY,
  site_id INTEGER REFERENCES survey_sites(id) ON DELETE CASCADE,
  technology TEXT,
  lcoe_usd_per_mwh DOUBLE PRECISION,
  details JSONB,
  computed_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS monitoring_timeseries (
  id SERIAL PRIMARY KEY,
  site_id INTEGER REFERENCES survey_sites(id) ON DELETE CASCADE,
  ts TIMESTAMP WITH TIME ZONE NOT NULL,
  metric TEXT,
  value DOUBLE PRECISION,
  metadata JSONB
);

-- Geospatial index examples
CREATE INDEX IF NOT EXISTS idx_survey_sites_geom ON survey_sites USING GIST (geom);

-- Simple vacuum/analyze suggestion (to be run by DBA)
-- VACUUM ANALYZE;
