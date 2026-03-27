from typing import Dict, Any, List
import random

from .data_loader import load_benchmarks


class ValidationEngine:
    def __init__(self):
        self.bench = load_benchmarks()

    def latest_validation(self, ward_id: int | None = None) -> Dict[str, Any]:
        status = "ok" if random.random() > 0.2 else "needs_review"
        confidence = round(random.uniform(0.6, 0.95), 2)
        discrepancies = {
            "osm_vs_inference": round(random.uniform(-0.1, 0.1), 2),
            "nss_gap": round(random.uniform(-0.05, 0.05), 2),
        }
        return {
            "ward_id": ward_id,
            "status": status,
            "confidence": confidence,
            "discrepancies": discrepancies,
        }

    def audit_samples(self, ward_id: int | None = None) -> List[Dict[str, Any]]:
        samples = []
        for i in range(3):
            samples.append(
                {
                    "id": i + 1,
                    "location": f"sample-{i+1}",
                    "result": random.choice(["pass", "minor_issue", "fail"]),
                    "notes": "auto-generated for demo",
                }
            )
        return samples
