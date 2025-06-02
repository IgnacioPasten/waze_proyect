#!/bin/bash

echo "🧹 Limpiando contenedores y volúmenes antiguos..."
docker-compose down -v

echo "🚀 Construyendo contenedores..."
docker-compose build

echo "🔄 Levantando servicios..."
docker-compose up -d

echo "⏳ Esperando a que los servicios estén listos..."
sleep 30  # Esperar 30 segundos para que Hadoop se inicie completamente

echo "🐘 Configurando Hadoop HDFS..."
docker exec hadoop-pig bash -c "
  # Crear directorios en HDFS
  hdfs dfs -mkdir -p /user/root
  hdfs dfs -mkdir -p /user/waze

  # Copiar datos a HDFS si existen
  if [ -f '/data/incidentes_limpios.csv' ]; then
    hdfs dfs -put /data/incidentes_limpios.csv /user/waze/
    echo '📄 Archivo incidentes_limpios.csv copiado a HDFS'
  else
    echo '⚠️  Advertencia: No se encontró /data/incidentes_limpios.csv'
  fi

  # Dar permisos
  hdfs dfs -chmod -R 777 /user
  echo '🔒 Permisos configurados en HDFS'

  # Verificar estructura
  echo '📂 Estructura de HDFS:'
  hdfs dfs -ls -R /user
"

echo "✅ Proyecto iniciado. Servicios corriendo:"
docker ps

echo "🔗 URLs de acceso:"
echo " - Hadoop Namenode: http://localhost:50070"
echo " - YARN ResourceManager: http://localhost:8088"
echo " - MongoDB: mongodb://root:example@localhost:27017"