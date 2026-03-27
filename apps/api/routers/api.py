from fastapi import APIRouter, HTTPException
from typing import List, Optional

from ..services.data_loader import load_geojson, load_population
from ..services.recommendations import RecommendationEngine
from ..services.benchmarks import BenchmarkEngine
from ..services.simulation import SimulationEngine
from ..services.validation import ValidationEngine
from pydantic import BaseModel

router = APIRouter(prefix="/api")


class SimulationRequest(BaseModel):
    ward_id: int
    action: str


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/cities")
def cities():
    geo = load_geojson()
    return [{"id": 1, "name": "Demo City", "wards": len(geo["features"]) }]


@router.get("/wards")
def wards():
    geo = load_geojson()
    return geo


@router.get("/wards/{ward_id}")
def ward_detail(ward_id: int):
    geo = load_geojson()
    feature = next((f for f in geo["features"] if f["properties"]["id"] == ward_id), None)
    if not feature:
        raise HTTPException(404, "Ward not found")
    bench = BenchmarkEngine()
    rec_engine = RecommendationEngine()
    kpis = bench.kpis_for_ward(ward_id)
    cdi = bench.civic_deficit_index(ward_id)
    recs = rec_engine.generate_for_ward(ward_id)
    return {"feature": feature, "kpis": kpis, "cdi": cdi, "recommendations": recs}


@router.get("/benchmarks")
def benchmarks():
    bench = BenchmarkEngine()
    return {"weights": bench.weights, "benchmarks": bench.df.to_dict(orient="records")}


@router.get("/benchmarks/{ward_id}")
def benchmark_for_ward(ward_id: int):
    bench = BenchmarkEngine()
    return {
        "kpis": bench.kpis_for_ward(ward_id),
        "cdi": bench.civic_deficit_index(ward_id),
    }


@router.get("/recommendations")
def recommendations(ward_id: Optional[int] = None):
    rec_engine = RecommendationEngine()
    if ward_id:
        return rec_engine.generate_for_ward(ward_id)
    geo = load_geojson()
    results = []
    for f in geo["features"]:
        results.extend(rec_engine.generate_for_ward(f["properties"]["id"]))
    return results


@router.post("/recommendations/generate")
def recommendations_generate(ward_id: int):
    rec_engine = RecommendationEngine()
    return rec_engine.generate_for_ward(ward_id)


@router.post("/simulations/run")
def run_simulation(req: SimulationRequest):
    sim = SimulationEngine()
    return sim.run(req.ward_id, req.action)


@router.get("/validation")
def validation(ward_id: Optional[int] = None):
    val = ValidationEngine()
    return {
        "latest": val.latest_validation(ward_id),
        "samples": val.audit_samples(ward_id),
    }


@router.get("/layers")
def layers():
    return {
        "infrastructure_classes": [
            "roads",
            "schools",
            "hospitals",
            "green",
            "slum_clusters",
            "water",
        ],
        "future_classes": [
            "electric_substations",
            "public_toilets",
            "bus_stops",
            "waste_sites",
            "sewage_assets",
            "parks",
            "anganwadis",
        ],
    }
