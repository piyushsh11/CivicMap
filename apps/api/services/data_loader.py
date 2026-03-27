import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any

# Prefer Mumbai production datasets when present; fall back to bundled sample.
ROOT = Path(__file__).resolve().parents[3] / "data"
MUMBAI_PATH = ROOT / "mumbai"
SAMPLE_PATH = ROOT / "sample"


def _pick(base_filename: str) -> Path:
    """Return the dataset path prioritising Mumbai assets."""
    mumbai_file = MUMBAI_PATH / base_filename
    if mumbai_file.exists():
        return mumbai_file
    return SAMPLE_PATH / base_filename


def load_geojson() -> Dict[str, Any]:
    with open(_pick("wards.geojson"), "r", encoding="utf-8") as f:
        return json.load(f)


def load_population() -> pd.DataFrame:
    return pd.read_csv(_pick("population.csv"))


def load_benchmarks() -> pd.DataFrame:
    return pd.read_csv(_pick("benchmarks.csv"))
