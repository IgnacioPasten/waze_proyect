#!/bin/bash

echo "🧹 Limpiando contenedores y volúmenes antiguos..."
docker-compose down -v

echo "🚀 Construyendo contenedores..."
docker-compose build

echo "🔄 Levantando servicios..."
docker-compose up -d

echo "✅ Proyecto iniciado. Servicios corriendo:"
docker ps

