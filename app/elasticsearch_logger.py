from elasticsearch8 import Elasticsearch
from datetime import datetime

es = Elasticsearch("http://localhost:9200")

def crear_indices_si_no_existen():
    indices = {
        "scraper_metrics": {
            "timestamp": "date",
            "total_eventos": "integer",
            "duracion": "float"
        },
        "cache_metrics": {
            "timestamp": "date",
            "politica": "keyword",
            "ciudad": "keyword",
            "resultado": "keyword"
        },
        "trafico_sintetico": {
            "timestamp": "date",
            "modelo_generador": "keyword",
            "tasa": "integer",
            "consulta": "text"
        }
    }

    for index_name, fields in indices.items():
        if not es.indices.exists(index=index_name):
            mappings = {
                "mappings": {
                    "properties": {
                        key: {"type": value}
                        for key, value in fields.items()
                    }
                }
            }
            es.indices.create(index=index_name, body=mappings)
            print(f"Índice creado: {index_name}")
        else:
            print(f"Índice ya existe: {index_name}")

def log_scraper_metrics(total_eventos: int, duracion: float):
    doc = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_eventos": total_eventos,
        "duracion": duracion
    }
    res = es.index(index="scraper_metrics", document=doc)
    print(f"Scraper log registrado: {res['result']}")
