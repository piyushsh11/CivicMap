# Architecture
- FastAPI server with Jinja2 templates for HTML rendering
- Static assets served from `/static`
- PostGIS-backed schema (see migrations/001_init.sql); demo mode uses flat files
- Service layer modules: benchmarks, recommendations, simulation, validation
- Pipeline stubs under `services/` to connect ingestion/inference/validation tasks
- Leaflet for interactive map; Chart.js for KPI/deficit visuals
- Datasets: Mumbai-first (wards, Census+BMC population, NSS/MOSPI benchmarks, Sentinel-2, OSM backbone, drone uploads)
- Pages: dashboard, map, ward detail, recommendations, simulation, validation, uploads, admin, report
