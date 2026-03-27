-- Minimal schema for CivicMap AI (PostgreSQL + PostGIS assumed)
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS cities (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  state TEXT,
  population INTEGER,
  bbox JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS wards (
  id SERIAL PRIMARY KEY,
  city_id INTEGER REFERENCES cities(id),
  name TEXT NOT NULL,
  code TEXT,
  population INTEGER,
  area_sq_km DOUBLE PRECISION,
  geom GEOMETRY(POLYGON, 4326),
  centroid GEOMETRY(POINT, 4326),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS wards_geom_idx ON wards USING GIST (geom);

CREATE TABLE IF NOT EXISTS benchmark_results (
  id SERIAL PRIMARY KEY,
  ward_id INTEGER REFERENCES wards(id),
  metric TEXT,
  value DOUBLE PRECISION,
  target DOUBLE PRECISION,
  unit TEXT,
  source TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS civic_deficit_scores (
  id SERIAL PRIMARY KEY,
  ward_id INTEGER REFERENCES wards(id),
  component TEXT,
  score DOUBLE PRECISION,
  weight DOUBLE PRECISION,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS recommendations (
  id SERIAL PRIMARY KEY,
  ward_id INTEGER REFERENCES wards(id),
  title TEXT,
  category TEXT,
  description TEXT,
  reason_summary TEXT,
  reason_json JSONB,
  severity DOUBLE PRECISION,
  priority_score DOUBLE PRECISION,
  urgency TEXT,
  cost_band TEXT,
  impacted_population INTEGER,
  expected_kpi_improvement TEXT,
  confidence DOUBLE PRECISION,
  suggested_geometry GEOMETRY,
  status TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS recommendations_geom_idx ON recommendations USING GIST (suggested_geometry);

CREATE TABLE IF NOT EXISTS scenario_runs (
  id SERIAL PRIMARY KEY,
  ward_id INTEGER REFERENCES wards(id),
  action TEXT,
  assumptions JSONB,
  before_kpis JSONB,
  after_kpis JSONB,
  cdi_delta DOUBLE PRECISION,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS validation_runs (
  id SERIAL PRIMARY KEY,
  ward_id INTEGER REFERENCES wards(id),
  validation_type TEXT,
  status TEXT,
  confidence DOUBLE PRECISION,
  discrepancies JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS validation_samples (
  id SERIAL PRIMARY KEY,
  validation_run_id INTEGER REFERENCES validation_runs(id),
  location GEOMETRY,
  result TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS admin_thresholds (
  id SERIAL PRIMARY KEY,
  metric TEXT,
  target DOUBLE PRECISION,
  unit TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS admin_weights (
  id SERIAL PRIMARY KEY,
  component TEXT,
  weight DOUBLE PRECISION,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS model_registry (
  id SERIAL PRIMARY KEY,
  name TEXT,
  version TEXT,
  path TEXT,
  status TEXT,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
