# Civic Recommendation Engine

## Workflow
1. Pull KPI deficits per ward from BenchmarkEngine
2. Trigger rule if deficit > 0
3. Compute priority_score = min(1, deficit*1.2 + impacted_pop/100000)
4. Assign urgency bands (immediate/short-term/long-term) and cost band (low/medium/high)
5. Attach explainability payload (`reason_json`), confidence, expected KPI delta
6. Optionally locate candidate geometry (centroid or highest-density sub-cell)

## Categories (v1)
- healthcare, education, roads, water, green, inspection/slum

## Equity-aware hints
- Population segment boosts via impacted_pop term
- Add multiplier for slum_population in future if needed

## Extending
- Add new metric -> component mapping in `BenchmarkEngine._component_for_metric`
- Add new rule branch in `_title_description`
- Wire model outputs by writing InfrastructureAsset rows and re-computing deficits
