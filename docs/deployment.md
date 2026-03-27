# Deployment

## Local
- Use uvicorn with reload for development
- `.env.example` provides defaults; copy to `.env`

## Docker Compose
- `docker-compose up --build`
- Services: api, db (PostGIS), redis

## Production considerations
- Run migrations (`psql -f migrations/001_init.sql` or Alembic)
- Serve via gunicorn + uvicorn workers behind nginx
- Configure HTTPS, HSTS, and Sentry DSN
- Mount Mumbai datasets to `data/mumbai/` (wards, population, benchmarks, Sentinel-2, OSM) or point ingestion to data lake
- Connect to external storage for imagery (S3/MinIO)
- Restrict CORS and add auth middleware
