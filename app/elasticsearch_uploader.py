import csv
from datetime import datetime
from elasticsearch8 import Elasticsearch

es = Elasticsearch("http://localhost:9200")

total_insertados = 0
errores = 0

with open("incidentes_limpios.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for i, row in enumerate(reader, start=1):
        try:
            doc = {
                "timestamp": datetime.strptime(row["fecha"], "%Y-%m-%d %H:%M:%S").isoformat(),
                "tipo": row["tipo"],
                "subtipo": row["subtipo"],
                "subtipo_normalizado": row["subtipo_normalizado"],
                "ciudad": row["ciudad"] if row["ciudad"] else "Desconocido",
                "calle": row["calle"],
                "ubicacion": {
                    "lat": float(row["lat"]),
                    "lon": float(row["lon"])
                }
            }

            res = es.index(index="eventos_filtrados", document=doc)
            if res.get("result") == "created":
                total_insertados += 1
            else:
                print(f"[{i}] Inserción no confirmada: {res}")
        except Exception as e:
            errores += 1
            print(f"[{i}]  Error al indexar fila: {row}")
            print(f"    Error: {e}")

print(f"\n Total insertados: {total_insertados}")
print(f" Errores: {errores}")
