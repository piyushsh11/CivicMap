from typing import Dict, Any
from shapely.geometry import shape, mapping


def polygon_centroid(geom: Dict[str, Any]) -> Dict[str, Any]:
    poly = shape(geom)
    c = poly.centroid
    return mapping(c)


def area_sq_km(geom: Dict[str, Any]) -> float:
    # Rough area using EPSG:3857 approximation
    poly = shape(geom)
    return poly.area / 1_000_000
