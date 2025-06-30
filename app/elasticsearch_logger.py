try:
    from elasticsearch import Elasticsearch
except ImportError:
    try:
        from elasticsearch8 import Elasticsearch
    except ImportError:
        print("elasticsearch no disponible")
        Elasticsearch = None
        
from datetime import datetime

# inicio elasticsearch
try:
    if Elasticsearch:   
        es = Elasticsearch(
            "http://localhost:9200",
            verify_certs=False,
            request_timeout=60
        )
    else:
        es = None
except:
    es = None

def crear_indices_si_no_existen():
    if not es:
        print("elasticsearch no disponible")
        return
        
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
        "processing_metrics": {
            "timestamp": "date",
            "eventos_procesados": "integer",
            "tiempo_total": "float",
            "archivo_generado": "keyword",
            "fase": "keyword"
        },
        "trafico_sintetico": {
            "timestamp": "date",
            "modelo_generador": "keyword",
            "tasa": "integer",
            "consulta": "text"
        }
    }

    for index_name, fields in indices.items():
        try:
            if not es.indices.exists(index=index_name):
                mappings = {
                    "mappings": {
                        "properties": {
                            key: {"type": value}
                            for key, value in fields.items()
                        }
                    }
                }
                # Usar body para v7.x
                es.indices.create(index=index_name, body=mappings)
                print(f"Índice creado: {index_name}")
            else:
                print(f"Índice ya existe: {index_name}")
        except Exception as e:
            print(f"Error creando índice {index_name}: {e}")

def log_scraper_metrics(total_eventos: int, duracion: float):
    """
    Log metricas scraper
    """
    if not es:
        print("elasticsearch no disponible para logging")
        return
        
    try:
        doc = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_eventos": total_eventos,
            "duracion": duracion
        }
        res = es.index(index="scraper_metrics", document=doc)
        print(f"scraper log registrado: {res['result']}")
    except Exception as e:
        print(f"error: {e}")

def log_processing_metrics(eventos_procesados: int, tiempo_total: float, archivo_generado: str = None):
    """
    Log metricas procesamiento de datos
    """
    if not es:
        print("elasticsearch no disponible para logging")
        return
        
    try:
        doc = {
            "timestamp": datetime.utcnow().isoformat(),
            "eventos_procesados": eventos_procesados,
            "tiempo_total": tiempo_total,
            "archivo_generado": archivo_generado or "sin_archivo",
            "fase": "processing"
        }
        res = es.index(index="processing_metrics", document=doc)
        print(f"Processing log registrado: {res['result']}")
    except Exception as e:
        print(f"Error logging processing metrics: {e}")

def log_cache_event(politica: str, tasa: int, resultado: str):
    """
    Log eventos cache
    """
    if not es:
        print("elasticsearch no disponible para logging")
        return
        
    try:
        doc = {
            "timestamp": datetime.utcnow().isoformat(),
            "politica": politica,
            "tasa": tasa,
            "resultado": resultado
        }
        es.index(index="cache_metrics", document=doc)
    except Exception as e:
        print(f"Error logging cache event: {e}")
