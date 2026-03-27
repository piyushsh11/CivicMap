-- Seed sample city/wards for Postgres demo
INSERT INTO cities (id, name, state, population) VALUES (1, 'Demo City', 'KA', 113000) ON CONFLICT DO NOTHING;
INSERT INTO wards (id, city_id, name, code, population) VALUES
  (1, 1, 'Ward 12', 'W12', 52000),
  (2, 1, 'Ward 18', 'W18', 61000)
ON CONFLICT DO NOTHING;
