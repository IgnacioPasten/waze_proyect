import requests
import json
import time
from datetime import datetime
import os
import math
from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# conexión mongodb
client = MongoClient("mongodb://mongodb:27017/")
db = client["waze_data"]
collection = db["events"]

# configuración
WAZE_URL = "https://www.waze.com/live-map/api/georss"
HEADERS = {"User-Agent": "Mozilla/5.0"}
TOTAL_OBJETIVO = 10000 # total de eventos a obtener, se puede ajustar
EVENTOS_POR_CASILLA = 200
DELAY_MINUTOS = 5
DIRECTORIO_SALIDA = "data_eventos_waze"

eventos_uuid = set()

# coordenadas
TOP = -33.0
BOTTOM = -34.2
LEFT = -71.1
RIGHT = -70.3

os.makedirs(DIRECTORIO_SALIDA, exist_ok=True)

TRADUCCION_TIPO = {
    "HAZARD": "Peligro",
    "JAM": "Tráfico",
    "ACCIDENT": "Accidente",
    "ROAD_CLOSED": "Cierre de camino",
    "CHIT_CHAT": "Conversación",
    "POLICE": "Policía",
    "WEATHERHAZARD": "Condición climática",
}


def generar_casillas(n=52):
    casillas = []
    filas, columnas = 4, 13
    lat_step = (TOP - BOTTOM) / filas
    lon_step = (RIGHT - LEFT) / columnas

    for i in range(filas):
        for j in range(columnas):
            casilla = {
                "nombre": f"casilla_{i}_{j}",
                "top": TOP - i * lat_step,
                "bottom": TOP - (i + 1) * lat_step,
                "left": LEFT + j * lon_step,
                "right": LEFT + (j + 1) * lon_step,
            }
            casillas.append(casilla)
    return casillas


def obtener_eventos(casilla):
    params = {
        "top": casilla["top"],
        "bottom": casilla["bottom"],
        "left": casilla["left"],
        "right": casilla["right"],
        "env": "row",
        "types": "alerts",
    }

    try:
        resp = requests.get(WAZE_URL, params=params, headers=HEADERS)
        if resp.status_code == 200:
            data = resp.json()
            eventos_crudos = data.get("alerts", [])
            eventos_procesados = []

            for evento in eventos_crudos:
                uuid = evento.get("uuid") or evento.get("id")
                if not uuid or uuid in eventos_uuid:
                    continue
                eventos_uuid.add(uuid)

                comentarios = evento.get("comments", [])[:2]
                resumen_comentarios = [
                    {
                        "pulgar_arriba": c.get("isThumbsUp", False),
                        "texto": c.get("text", "").strip(),
                    }
                    for c in comentarios
                    if c.get("text", "").strip()
                ]

                evento_procesado = {
                    "fecha": datetime.fromtimestamp(
                        evento.get("pubMillis", 0) / 1000
                    ).isoformat(),
                    "tipo": TRADUCCION_TIPO.get(evento.get("type"), evento.get("type")),
                    "subtipo": evento.get("subtype"),
                    "calle": evento.get("street"),
                    "ciudad": evento.get("city"),
                    "reportado_por": evento.get("reportBy", "Anónimo"),
                    "usuario_municipal": evento.get("reportByMunicipalityUser", "false")
                    == "true",
                    "ubicacion": {
                        "lat": evento.get("location", {}).get("y"),
                        "lon": evento.get("location", {}).get("x"),
                    },
                    "comentarios": resumen_comentarios,
                    "casilla": casilla["nombre"],
                }

                eventos_procesados.append(evento_procesado)
                if len(eventos_procesados) >= EVENTOS_POR_CASILLA:
                    break

            return eventos_procesados
        else:
            logger.error(f"Error HTTP {resp.status_code} en {casilla['nombre']}")
            return []
    except Exception as e:
        logger.error(f"Error en solicitud {casilla['nombre']}: {e}")
        return []


def guardar_eventos(eventos, ciclo):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = os.path.join(DIRECTORIO_SALIDA, f"eventos_ciclo{ciclo}_{ts}.json")
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2)
    logger.info(f"Guardados {len(eventos)} eventos en {archivo}")


def main_loop():
    total = 0
    ciclo = 1
    casillas = generar_casillas()

    while total < TOTAL_OBJETIVO:
        logger.info(f"\n Ciclo #{ciclo} - Escaneando las 52 casillas...")
        eventos_ciclo = []

        for casilla in casillas:
            logger.info(f"→ Procesando {casilla['nombre']}...")
            eventos = obtener_eventos(casilla)
            eventos_ciclo.extend(eventos)
            logger.info(f"   {len(eventos)} eventos obtenidos")

        if eventos_ciclo:
            guardar_eventos(eventos_ciclo, ciclo)
            collection.insert_many(eventos_ciclo)

            total += len(eventos_ciclo)
            logger.info(f"Total acumulado: {total} eventos")
        else:
            logger.info("No se obtuvieron eventos en esta iteración.")

        ciclo += 1
        if total < TOTAL_OBJETIVO:
            logger.info(
                f"Esperando {DELAY_MINUTOS} minutos antes del siguiente ciclo..."
            )
            time.sleep(DELAY_MINUTOS * 60)


if __name__ == "__main__":
    main_loop()
