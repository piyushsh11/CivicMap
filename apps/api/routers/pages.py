from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from ..services.benchmarks import BenchmarkEngine
from ..services.recommendations import RecommendationEngine
from ..services.simulation import SimulationEngine
from ..services.validation import ValidationEngine
from ..services.data_loader import load_geojson

BASE_DIR = Path(__file__).resolve().parents[3]
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter()


@router.get("/dashboard")
def dashboard(request: Request):
    geo = load_geojson()
    bench = BenchmarkEngine()
    rec_engine = RecommendationEngine()
    wards = [f["properties"] for f in geo["features"]]
    top_recs = rec_engine.generate_for_ward(wards[0]["id"])
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "wards": wards,
            "bench": bench,
            "top_recs": top_recs,
        },
    )


@router.get("/map")
def map_page(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})


@router.get("/wards/{ward_id}")
def ward_page(request: Request, ward_id: int):
    bench = BenchmarkEngine()
    rec_engine = RecommendationEngine()
    geo = load_geojson()
    feature = next((f for f in geo["features"] if f["properties"]["id"] == ward_id), None)
    return templates.TemplateResponse(
        "ward_detail.html",
        {
            "request": request,
            "feature": feature,
            "kpis": bench.kpis_for_ward(ward_id),
            "cdi": bench.civic_deficit_index(ward_id),
            "recs": rec_engine.generate_for_ward(ward_id),
        },
    )


@router.get("/recommendations")
def recommendations_page(request: Request):
    rec_engine = RecommendationEngine()
    geo = load_geojson()
    recs = []
    for f in geo["features"]:
        recs.extend(rec_engine.generate_for_ward(f["properties"]["id"]))
    return templates.TemplateResponse("recommendations.html", {"request": request, "recs": recs})


@router.get("/simulation")
def simulation_page(request: Request):
    return templates.TemplateResponse("simulation.html", {"request": request})


@router.get("/validation")
def validation_page(request: Request):
    val = ValidationEngine()
    return templates.TemplateResponse(
        "validation.html",
        {"request": request, "latest": val.latest_validation(), "samples": val.audit_samples()},
    )


@router.get("/uploads")
def uploads_page(request: Request):
    return templates.TemplateResponse("uploads.html", {"request": request})


@router.get("/admin")
def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@router.get("/reports/ward/{ward_id}")
def ward_report(request: Request, ward_id: int):
    bench = BenchmarkEngine()
    rec_engine = RecommendationEngine()
    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "ward_id": ward_id,
            "kpis": bench.kpis_for_ward(ward_id),
            "cdi": bench.civic_deficit_index(ward_id),
            "recs": rec_engine.generate_for_ward(ward_id),
        },
    )
