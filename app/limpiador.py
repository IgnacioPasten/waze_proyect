from pymongo import MongoClient
import csv
from datetime import datetime

def normalizar_tipo(subtipo):
    if "POT_HOLE" in subtipo:
        return "Hueco"
    elif "OBJECT_ON_ROAD" in subtipo:
        return "Objeto en la vía"
    elif "ROAD_CLOSED" in subtipo:
        return "Calle Cerrada"
    elif "ACCIDENT" in subtipo:
        return "Accidente"
    elif "JAM" in subtipo:
        return "Atasco"
    return "Otro"

client = MongoClient("mongodb://localhost:27017/")
db = client["waze_data"]
collection = db["events"]

with open("incidentes_limpios.csv", mode="w", newline="", encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(["fecha", "tipo", "subtipo", "subtipo_normalizado", "ciudad", "calle", "lat", "lon"])

    for evento in collection.find():
        if not all(k in evento for k in ["fecha", "tipo", "subtipo", "ciudad", "calle", "ubicacion"]):
            continue
        if not evento["fecha"] or not evento["ciudad"]:
            continue

        subtipo_normal = normalizar_tipo(evento["subtipo"])
        fecha = datetime.strptime(evento["fecha"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

        writer.writerow([
            fecha,
            evento["tipo"],
            evento["subtipo"],
            subtipo_normal,
            evento["ciudad"],
            evento["calle"],
            evento["ubicacion"]["lat"],
            evento["ubicacion"]["lon"]
        ])
