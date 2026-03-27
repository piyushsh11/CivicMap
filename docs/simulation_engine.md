# Scenario Simulation Engine
- Input: ward_id, action (add_hospital, add_school, increase_green, improve_road, add_water_point)
- For demo: apply fixed deficit deltas per component
- Output: before/after component deficits, CDI delta
- Persist to `scenario_runs` in production; UI shows JSON diff
- Extend by plugging action-specific models or budgeting constraints
