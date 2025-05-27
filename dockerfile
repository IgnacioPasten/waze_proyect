FROM python:3.10-slim

# pymongo
RUN pip install pymongo requests

# directorio de la app
WORKDIR /app

# contenido de app al contenedor
COPY app/ /app

# archivo requirements.txt al contenedor
COPY requirements.txt /app/

# dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# No definimos CMD aquí porque lo pusimos en docker-compose.yml