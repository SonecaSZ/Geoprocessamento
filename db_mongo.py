# db_mongo.py
from pymongo import MongoClient
from typing import List, Dict, Any
import os
from geoprocessamento import distance_km

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://ra12jrra_db_user:<Rauldudu2001->@cluster0.4pja9lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
DB_NAME = 'projeto_persistencia'
COLLECTION = 'locais'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
locais_col = db[COLLECTION]

try:
    locais_col.create_index([('coordenadas.latitude', 1), ('coordenadas.longitude', 1)])
except Exception:
    pass

def insert_local(document: Dict[str, Any]) -> str:
    result = locais_col.insert_one(document)
    return str(result.inserted_id)

def find_locais_by_city(cidade: str) -> List[Dict[str, Any]]:
    return list(locais_col.find({'cidade': cidade}))

def find_all_locais() -> List[Dict[str, Any]]:
    return list(locais_col.find())

def find_locais_nearby(center_lat: float, center_lon: float, radius_km: float) -> List[Dict[str, Any]]:
    results = []
    for doc in locais_col.find():
        c = doc.get('coordenadas', {})
        lat = c.get('latitude')
        lon = c.get('longitude')
        if lat is None or lon is None:
            continue
        d = distance_km((center_lat, center_lon), (lat, lon))
        if d <= radius_km:
            doc['_distance_km'] = round(d, 3)
            results.append(doc)
    results.sort(key=lambda x: x.get('_distance_km', 999999))
    return results
