# Data Pipeline

1. **Ingestion** (services/ingestion):
   - Load Mumbai ward boundaries `data/mumbai/wards.geojson` (mandatory base layer)
   - Register Sentinel-2 manifest + tiles (`sentinel2_manifest.json`, `sentinel2_tiles/`)
   - Accept drone uploads (uploads page -> `data/mumbai/drone_uploads/` or object storage)
   - Import OSM backbone (`osm_extract.pbf`) and parse roads/amenities -> `osm_assets.geojson`
   - Ingest population CSV (Census + BMC) and NSS/MOSPI benchmark CSV

2. **Preprocessing** (services/preprocessing):
   - Tile imagery, reproject, clip to wards
   - Normalize radiometry; mask clouds for Sentinel-2

3. **Inference** (services/inference):
   - Segmentation: roads, green cover, slum proxy
   - Detection: schools, hospitals, water tanks
   - Produce GeoJSON/Parquet outputs with confidence

4. **Benchmarking** (services/benchmarking):
   - Spatial join detections with wards; compute densities
   - Compare against admin thresholds; store in `benchmark_results`

5. **Recommendation generation** (services/recommendations):
   - Rule triggers + score calculation
   - Persist to `recommendations`

6. **Simulation** (services/simulation):
   - Apply intervention deltas; recompute CDI

7. **Validation** (services/validation):
   - Aggregate validation vs NSS/MOSPI
   - Audit samples + drone verification status

Demo mode bypasses DB and reads from `data/sample`.
