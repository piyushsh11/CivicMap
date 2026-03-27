from typing import List, Optional
from pydantic import BaseModel


class WardGeometry(BaseModel):
    id: int
    name: str
    code: Optional[str]
    population: Optional[int]
    geom: dict
    centroid: Optional[dict]


class KPI(BaseModel):
    metric: str
    value: float
    target: float
    unit: str


class RecommendationOut(BaseModel):
    id: int
    ward_id: int
    title: str
    category: str
    description: str
    reason_summary: str
    severity: float
    priority_score: float
    urgency: str
    cost_band: str
    confidence: float
    impacted_population: Optional[int]
    expected_kpi_improvement: Optional[str]
    status: str


class ScenarioResult(BaseModel):
    scenario_id: int
    ward_id: int
    action: str
    before: dict
    after: dict
    cdi_delta: float


class ValidationSummary(BaseModel):
    ward_id: Optional[int]
    status: str
    confidence: float
    discrepancies: Optional[dict]
