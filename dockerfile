# Usa una imagen oficial de Python
FROM python:3.10-slim

# Instala pymongo
RUN pip install pymongo requests

# Crea el directorio de la app
WORKDIR /app

# Copia el contenido de app al contenedor
COPY app/ /app

# No definimos CMD aquí porque lo pusimos en docker-compose.yml
