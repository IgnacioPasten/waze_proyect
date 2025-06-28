
from datetime import datetime, timedelta
import random

from elasticsearch8 import Elasticsearch
es = Elasticsearch("http://localhost:9200")


# Datos base para simular eventos
tipos = ["Peligro", "Accidente", "Atasco", "Calle Cerrada", "Objeto en la vía"]
subtipos = {
    "Peligro": ["HAZARD_ON_ROAD_CONSTRUCTION", "HAZARD_WEATHER", "HAZARD_ANIMAL_ON_ROAD"],
    "Accidente": ["ACCIDENT_MINOR", "ACCIDENT_MAJOR"],
    "Atasco": ["JAM_TRAFFIC", "JAM_CONSTRUCTION"],
    "Calle Cerrada": ["ROAD_CLOSED_TEMPORARY", "ROAD_CLOSED_PERMANENT"],
    "Objeto en la vía": ["OBJECT_ON_ROAD", "OBJECT_ON_SHOULDER"]
}
subtipos_normalizados = {
    "HAZARD_ON_ROAD_CONSTRUCTION": "Otro",
    "HAZARD_WEATHER": "Otro",
    "HAZARD_ANIMAL_ON_ROAD": "Otro",
    "ACCIDENT_MINOR": "Accidente",
    "ACCIDENT_MAJOR": "Accidente",
    "JAM_TRAFFIC": "Atasco",
    "JAM_CONSTRUCTION": "Atasco",
    "ROAD_CLOSED_TEMPORARY": "Calle Cerrada",
    "ROAD_CLOSED_PERMANENT": "Calle Cerrada",
    "OBJECT_ON_ROAD": "Objeto en la vía",
    "OBJECT_ON_SHOULDER": "Objeto en la vía"
}

ciudades = ["Santiago", "Valparaíso", "Puente Alto", "Maipú", "La Florida"]
calles = ["Av. Providencia", "Calle Las Heras", "Ruta F-100-G", "Av. Apoquindo", "Calle San Martín"]

base_time = datetime(2025, 5, 27, 8, 0, 0)  # Fecha base

for i in range(20):  # Insertar 20 documentos
    tipo = random.choice(tipos)
    subtipo = random.choice(subtipos[tipo])
    doc = {
        "timestamp": (base_time + timedelta(minutes=i*15)).isoformat(),
        "tipo": tipo,
        "subtipo": subtipo,
        "subtipo_normalizado": subtipos_normalizados[subtipo],
        "ciudad": random.choice(ciudades),
        "calle": random.choice(calles),
        "ubicacion": {
            "lat": round(-33.0 + random.uniform(-0.1, 0.1), 6),
            "lon": round(-71.0 + random.uniform(-0.1, 0.1), 6)
        }
    }
    res = es.index(index="eventos_filtrados", document=doc)
    print(f"Inserción {i+1}: {res['result']}")
