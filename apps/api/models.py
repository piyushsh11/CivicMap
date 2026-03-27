from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, JSON, String


def ts_now():
    return datetime.utcnow()


class City(SQLModel, table=True):
    __tablename__ = "cities"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    state: Optional[str] = Field(default=None)
    population: Optional[int] = None
    bbox: Optional[str] = Field(default=None, description="GeoJSON bbox string")
    created_at: datetime = Field(default_factory=ts_now)
    updated_at: datetime = Field(default_factory=ts_now)

    wards: List["Ward"] = Relationship(back_populates="city")


class Ward(SQLModel, table=True):
    __tablename__ = "wards"
    id: Optional[int] = Field(default=None, primary_key=True)
    city_id: int = Field(foreign_key="cities.id")
    name: str = Field(index=True)
    code: Optional[str] = Field(default=None, index=True)
    population: Optional[int] = None
    area_sq_km: Optional[float] = None
    geom: Optional[str] = Field(default=None, description="GeoJSON polygon string")
    centroid: Optional[str] = None
    created_at: datetime = Field(default_factory=ts_now)
    updated_at: datetime = Field(default_factory=ts_now)

    city: Optional[City] = Relationship(back_populates="wards")
    benchmarks: List["BenchmarkResult"] = Relationship(back_populates="ward")
    deficits: List["CivicDeficitScore"] = Relationship(back_populates="ward")
    recommendations: List["Recommendation"] = Relationship(back_populates="ward")


class PopulationSegment(SQLModel, table=True):
    __tablename__ = "ward_population_segments"
    id: Optional[int] = Field(default=None, primary_key=True)
    ward_id: int = Field(foreign_key="wards.id")
    segment: str
    population: int
    created_at: datetime = Field(default_factory=ts_now)


class ImageryAsset(SQLModel, table=True):
    __tablename__ = "imagery_assets"
    id: Optional[int] = Field(default=None, primary_key=True)
    ward_id: Optional[int] = Field(default=None, foreign_key="wards.id")
    source_type: str = Field(description="sentinel|drone|osm")
    uri: str
    status: str = Field(default="registered")
    metadata: dict = Field(sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=ts_now)


class InfrastructureAsset(SQLModel, table=True):
    __tablename__ = "infrastructure_assets"
    id: Optional[int] = Field(default=None, primary_key=True)
    ward_id: int = Field(foreign_key="wards.id")
    category: str
    subtype: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = Field(default=None, description="GeoJSON point")
    source_type: str = Field(default="inferred")
    confidence: Optional[float] = None
    created_at: datetime = Field(default_factory=ts_now)


class BenchmarkResult(SQLModel, table=True):
    __tablename__ = "benchmark_results"
    id: Optional[int] = Field(default=None, primary_key=True)
    ward_id: int = Field(foreign_key="wards.id")
    metric: str
    value: float
    target: float
    unit: str = Field(default="per_10k")
    source: str = Field(default="benchmark_table")
    created_at: datetime = Field(default_factory=ts_now)

    ward: Optional[Ward] = Relationship(back_populates="benchmarks")


class CivicDeficitScore(SQLModel, table=True):
    __tablename__ = "civic_deficit_scores"
    id: Optional[int] = Field(default=None, primary_key=True)
    ward_id: int = Field(foreign_key="wards.id")
    component: str
    score: float
    weight: float
    created_at: datetime = Field(default_factory=ts_now)

    ward: Optional[Ward] = Relationship(back_populates="deficits")


class Recommendation(SQLModel, table=True):
    __tablename__ = "recommendations"
    id: Optional[int] = Field(default=None, primary_key=True)
    ward_id: int = Field(foreign_key="wards.id")
    title: str
    category: str
    description: str
    reason_summary: str
    reason_json: dict = Field(sa_column=Column(JSON))
    severity: float
    priority_score: float
    urgency: str
    cost_band: str
    impacted_population: Optional[int] = None
    expected_kpi_improvement: Optional[str] = None
    confidence: Optional[float] = None
    suggested_geometry: Optional[str] = None
    status: str = Field(default="proposed")
    created_at: datetime = Field(default_factory=ts_now)
    updated_at: datetime = Field(default_factory=ts_now)

    ward: Optional[Ward] = Relationship(back_populates="recommendations")


class ScenarioRun(SQLModel, table=True):
    __tablename__ = "scenario_runs"
    id: Optional[int] = Field(default=None, primary_key=True)
    ward_id: int = Field(foreign_key="wards.id")
    action: str
    assumptions: dict = Field(sa_column=Column(JSON))
    before_kpis: dict = Field(sa_column=Column(JSON))
    after_kpis: dict = Field(sa_column=Column(JSON))
    cdi_delta: float
    created_at: datetime = Field(default_factory=ts_now)


class ValidationRun(SQLModel, table=True):
    __tablename__ = "validation_runs"
    id: Optional[int] = Field(default=None, primary_key=True)
    ward_id: Optional[int] = Field(default=None, foreign_key="wards.id")
    validation_type: str
    status: str
    confidence: Optional[float] = None
    discrepancies: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=ts_now)


class ValidationSample(SQLModel, table=True):
    __tablename__ = "validation_samples"
    id: Optional[int] = Field(default=None, primary_key=True)
    validation_run_id: int = Field(foreign_key="validation_runs.id")
    location: Optional[str] = None
    result: str
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=ts_now)


class AdminThreshold(SQLModel, table=True):
    __tablename__ = "admin_thresholds"
    id: Optional[int] = Field(default=None, primary_key=True)
    metric: str
    target: float
    unit: str
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=ts_now)


class AdminWeight(SQLModel, table=True):
    __tablename__ = "admin_weights"
    id: Optional[int] = Field(default=None, primary_key=True)
    component: str
    weight: float
    created_at: datetime = Field(default_factory=ts_now)


class ModelRegistry(SQLModel, table=True):
    __tablename__ = "model_registry"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    version: str
    path: str
    status: str = Field(default="registered")
    metadata: dict = Field(default={}, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=ts_now)
