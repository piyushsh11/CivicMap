from __future__ import annotations
from typing import List, Dict, Any
import math

from .benchmarks import BenchmarkEngine
from .data_loader import load_geojson, load_population

COST_BANDS = [
    (0.0, 0.4, "low"),
    (0.4, 0.7, "medium"),
    (0.7, 1.1, "high"),
]


class RecommendationEngine:
    def __init__(self):
        self.bench = BenchmarkEngine()
        self.population = load_population()

    @staticmethod
    def _humanize(metric: str) -> str:
        return metric.replace("_", " ").replace(" per ", " per ").title()

    def generate_for_ward(self, ward_id: int) -> List[Dict[str, Any]]:
        kpis = self.bench.kpis_for_ward(ward_id)
        recommendations: List[Dict[str, Any]] = []
        for kpi in kpis:
            if kpi["deficit"] <= 0:
                continue
            rec = self._recommendation_from_kpi(ward_id, kpi)
            if rec:
                recommendations.append(rec)
        recommendations.sort(key=lambda r: r["priority_score"], reverse=True)
        for idx, rec in enumerate(recommendations):
            rec["rank"] = idx + 1
        return recommendations

    def _recommendation_from_kpi(self, ward_id: int, kpi: Dict[str, Any]) -> Dict[str, Any]:
        component = self.bench._component_for_metric(kpi["metric"])
        impacted_pop = int(self._segment_population(ward_id, component))
        priority_score = round(min(1.0, kpi["deficit"] * 1.2 + impacted_pop / 100000), 3)
        severity = round(kpi["deficit"], 2)
        urgency = self._urgency(priority_score)
        cost_band = self._cost_band(kpi["deficit"])
        title, description = self._title_description(component, ward_id)
        return {
            "ward_id": ward_id,
            "title": title,
            "category": component,
            "description": description,
            "reason_summary": f"{self._humanize(kpi['metric'])} below target ({kpi['value']} vs {kpi['target']})",
            "reason_json": {
                "metric": kpi["metric"],
                "value": kpi["value"],
                "target": kpi["target"],
                "deficit": kpi["deficit"],
                "impacted_population": impacted_pop,
            },
            "severity": severity,
            "priority_score": priority_score,
            "urgency": urgency,
            "cost_band": cost_band,
            "impacted_population": impacted_pop,
            "expected_kpi_improvement": f"+{round(kpi['deficit']*kpi['target'],2)} {kpi['unit']}",
            "confidence": round(0.65 + 0.3 * (1 - kpi["deficit"]), 2),
            "status": "proposed",
        }

    def _segment_population(self, ward_id: int, component: str) -> int:
        seg_map = {
            "education": "children",
            "healthcare": "elderly",
            "water": "total",
            "roads": "total",
            "green": "total",
            "slum": "slum_population",
        }
        seg = seg_map.get(component, "total")
        row = self.population[(self.population.ward_id == ward_id) & (self.population.segment == seg)]
        if row.empty:
            return 0
        return int(row.population.values[0])

    @staticmethod
    def _urgency(priority_score: float) -> str:
        if priority_score > 0.8:
            return "immediate"
        if priority_score > 0.55:
            return "short-term"
        return "long-term"

    @staticmethod
    def _cost_band(deficit: float) -> str:
        if deficit >= 0.6:
            return "high"
        if deficit >= 0.35:
            return "medium"
        return "low"

    @staticmethod
    def _title_description(component: str, ward_id: int) -> tuple[str, str]:
        if component == "healthcare":
            return (
                "Add primary health center",
                "Healthcare coverage below benchmark; propose a PHC with 24x7 OPD to cut travel burden.",
            )
        if component == "education":
            return (
                "Add one public school",
                "High child population with low school seat ratio; prioritize inclusive school with toilets and ramps.",
            )
        if component == "roads":
            return (
                "Improve road connectivity",
                "Road density below target; add/upgrade connectors to reduce first/last mile friction.",
            )
        if component == "water":
            return (
                "Add community water point",
                "Water access gap; deploy resilient water kiosks with quality monitoring.",
            )
        if component == "green":
            return (
                "Increase green cover",
                "Green-deficit dense zone; add micro-park or Miyawaki patch near vulnerable clusters.",
            )
        return (
            "Request inspection",
            "Data discrepancy detected; schedule drone/field validation to resolve asset uncertainty.",
        )


class CandidateLocator:
    @staticmethod
    def suggested_point(feature: Dict[str, Any]) -> Dict[str, Any]:
        geom = feature["geometry"]
        coords = geom["coordinates"][0][0]
        return {"type": "Point", "coordinates": coords}
