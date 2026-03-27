from typing import Dict, Any
from copy import deepcopy
from .benchmarks import BenchmarkEngine


class SimulationEngine:
    def __init__(self):
        self.bench = BenchmarkEngine()

    def run(self, ward_id: int, action: str) -> Dict[str, Any]:
        before = self.bench.civic_deficit_index(ward_id)
        after_bench = deepcopy(self.bench)
        adjustment = self._adjustment(action)
        simulated_components = deepcopy(before["components"])
        for comp, delta in adjustment.items():
            if comp in simulated_components:
                simulated_components[comp]["deficit"] = max(
                    0.0, simulated_components[comp]["deficit"] - delta
                )
                simulated_components[comp]["weighted"] = simulated_components[comp]["deficit"] * simulated_components[comp]["weight"]
        after_cdi = round(sum(v["weighted"] for v in simulated_components.values()), 3)
        return {
            "ward_id": ward_id,
            "action": action,
            "before": before,
            "after": {"components": simulated_components, "cdi": after_cdi},
            "cdi_delta": round(before["cdi"] - after_cdi, 3),
        }

    @staticmethod
    def _adjustment(action: str) -> Dict[str, float]:
        return {
            "healthcare": 0.15 if "hospital" in action or "health" in action else 0,
            "education": 0.1 if "school" in action else 0,
            "green": 0.08 if "green" in action else 0,
            "water": 0.12 if "water" in action else 0,
            "roads": 0.1 if "road" in action else 0,
        }
