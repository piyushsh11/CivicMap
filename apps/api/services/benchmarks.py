from typing import List, Dict, Any
import pandas as pd

from .data_loader import load_benchmarks

DEFAULT_WEIGHTS = {
    "healthcare": 0.25,
    "education": 0.20,
    "roads": 0.20,
    "water": 0.15,
    "green": 0.10,
    "slum": 0.10,
}


class BenchmarkEngine:
    def __init__(self, weights: Dict[str, float] | None = None):
        self.weights = weights or DEFAULT_WEIGHTS
        self.df = load_benchmarks()

    def kpis_for_ward(self, ward_id: int) -> List[Dict[str, Any]]:
        records = self.df[self.df["ward_id"] == ward_id]
        return [
            {
                "metric": row.metric,
                "value": row.value,
                "target": row.target,
                "unit": row.unit,
                "deficit": max(0.0, (row.target - row.value) / row.target),
            }
            for row in records.itertuples()
        ]

    def civic_deficit_index(self, ward_id: int) -> Dict[str, Any]:
        kpis = self.kpis_for_ward(ward_id)
        component_scores = {}
        for kpi in kpis:
            key = self._component_for_metric(kpi["metric"])
            weight = self.weights.get(key, 0.0)
            component_scores[key] = {
                "deficit": kpi["deficit"],
                "weight": weight,
                "weighted": kpi["deficit"] * weight,
            }
        total = sum(v["weighted"] for v in component_scores.values())
        return {"components": component_scores, "cdi": round(total, 3)}

    @staticmethod
    def _component_for_metric(metric: str) -> str:
        if "hospital" in metric:
            return "healthcare"
        if "school" in metric:
            return "education"
        if "road" in metric:
            return "roads"
        if "water" in metric:
            return "water"
        if "green" in metric:
            return "green"
        return "slum"
