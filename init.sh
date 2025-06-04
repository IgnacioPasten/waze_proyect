#!/bin/bash

echo "limpiando contenedores y volumenes antiguos"
docker-compose down -v

echo "construyendo contenedores"
docker-compose build

echo "levantando servicios"
docker-compose up -d

echo "esperando a que los servicios esten listos"
sleep 30 

echo "Hadoop HDFS"
docker exec hadoop-pig bash -c "
  #HDFS
  hdfs dfs -mkdir -p /user/root
  hdfs dfs -mkdir -p /user/waze

  if [ -f '/data/incidentes_limpios.csv' ]; then
    hdfs dfs -put /data/incidentes_limpios.csv /user/waze/
    echo '📄 Archivo incidentes_limpios.csv copiado a HDFS'
  else
    echo 'no se encontro /data/incidentes_limpios.csv'
  fi

  #permisos
  hdfs dfs -chmod -R 777 /user
  echo 'permisos configurados en HDFS'

  #estructura
  echo 'estructura de HDFS:'
  hdfs dfs -ls -R /user
"

echo "proyecto iniciado -> servicios corriendo :)"
docker ps

echo "URLs:"
echo "Hadoop Namenode: http://localhost:50070"
echo "YARN ResourceManager: http://localhost:8088"
echo "MongoDB: mongodb://root:example@localhost:27017"