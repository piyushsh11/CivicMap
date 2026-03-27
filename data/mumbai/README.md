Place production Mumbai datasets here (outside repo for size). Expected filenames:
- wards.geojson                # Mumbai ward boundaries (BMC official)
- population.csv              # Ward-level population (Census + BMC estimates)
- benchmarks.csv              # NSS/MOSPI aggregates normalized to ward targets
- sentinel2_manifest.json     # Sentinel-2 scene metadata list
- sentinel2_tiles/            # Preprocessed Sentinel-2 clips per ward
- osm_extract.pbf             # OSM extract for Mumbai
- osm_assets.geojson          # Derived OSM amenities/roads if preprocessed
- drone_uploads/              # User uploads directory (configured storage)
