import os
from functools import lru_cache
from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    app_env: str = os.getenv("APP_ENV", "development")
    demo_mode: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
    secret_key: str = os.getenv("SECRET_KEY", "changeme")
    database_url: AnyUrl = os.getenv("DATABASE_URL", "postgresql+psycopg2://civicmap:civicmap@localhost:5432/civicmap")
    redis_url: AnyUrl = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    mapbox_token: str | None = os.getenv("MAPBOX_TOKEN")
    sentry_dsn: str | None = os.getenv("SENTRY_DSN")

    class Config:
        case_sensitive = False


@lru_cache()
def get_settings() -> "Settings":
    return Settings()
