# Benchmarking & Civic Deficit Index
- Metrics: hospitals_per_10k, schools_per_1k_children, green_cover_pct, road_density_km_per_sqkm, water_points_per_10k
- Default weights: healthcare 0.25, education 0.20, roads 0.20, water 0.15, green 0.10, slum 0.10
- Deficit per metric = max(0, (target - value)/target)
- CDI = sum(deficit * weight)
- Update weights via admin page (UI stub) and persist to `admin_weights`
- Benchmarks loaded from CSV in demo; production uses `benchmark_results`
