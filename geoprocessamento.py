# geoprocessamento.py
from math import radians, sin, cos, sqrt, atan2
from typing import Tuple, List, Dict

R = 6371.0

def haversine(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)

    a = sin(dphi/2.0)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2.0)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def distance_km(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    return haversine(coord1, coord2)

def filter_nearby(locations: List[Dict], center: Tuple[float, float], radius_km: float) -> List[Dict]:
    out = []
    for loc in locations:
        c = loc.get('coordenadas', {})
        lat = c.get('latitude')
        lon = c.get('longitude')
        if lat is None or lon is None:
            continue
        d = distance_km(center, (lat, lon))
        if d <= radius_km:
            loc_copy = dict(loc)
            loc_copy['_distance_km'] = round(d, 3)
            out.append(loc_copy)
    out.sort(key=lambda x: x['_distance_km'])
    return out
