# Core datasets (Mumbai-first)

| Domain | Source | Format/Path | Notes |
| --- | --- | --- | --- |
| Ward boundaries | BMC official shapefile/GeoJSON | `data/mumbai/wards.geojson` | Mandatory base layer |
| Population | Census 2011 + BMC updates | `data/mumbai/population.csv` | Ward-level totals + segments |
| Benchmarks | NSS/MOSPI aggregates | `data/mumbai/benchmarks.csv` | Targets per KPI |
| Satellite | Sentinel-2 | `data/mumbai/sentinel2_manifest.json` + `sentinel2_tiles/` | Green cover & density |
| OSM backbone | Geofabrik/BBBike extract | `data/mumbai/osm_extract.pbf` | Roads/buildings/amenities |
| OSM-derived | Processed GeoJSON | `data/mumbai/osm_assets.geojson` | Optional cache of parsed layers |
| Drone imagery | Field uploads | `data/mumbai/drone_uploads/` | Verification & inspection |

## Expected CSV schemas
- `population.csv`: ward_id,segment,population (segments: children, elderly, slum_population, total)
- `benchmarks.csv`: ward_id,metric,value,target,unit

## Sentinel-2 manifest schema (json)
```
[{"tile": "43QFJ", "acquired": "2024-11-02", "cloud": 8.1, "path": "sentinel2_tiles/43QFJ_20241102.tif"}]
```

## How the app picks datasets
- At runtime loaders look in `data/mumbai/*`; if missing, they fall back to bundled `data/sample/*` so demo mode stays functional.

## Loading instructions (suggested)
- Download Mumbai ward boundary GeoJSON and place as `data/mumbai/wards.geojson`.
- Build population CSV from Census+BMC; save as `data/mumbai/population.csv`.
- Prepare KPI targets and save as `data/mumbai/benchmarks.csv`.
- Fetch Sentinel-2 scenes (e.g., via sentinelsat), preprocess to tiles per ward, log in `sentinel2_manifest.json`.
- Download OSM extract (`osm_extract.pbf`), preprocess roads/amenities into `osm_assets.geojson`.
- Configure drone upload storage (MinIO/S3) and mount to `data/mumbai/drone_uploads/` or update storage path in ingestion pipeline.
