from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from .settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url, echo=False, pool_pre_ping=True, future=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def session_scope() -> Generator:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    # For demo, create tables if not exist when using SQLite; for Postgres use migrations
    if settings.demo_mode and settings.database_url.startswith("sqlite"):
        SQLModel.metadata.create_all(engine)
