#!/bin/bash

#
# init-hadoop.sh
# --------------------------------------------------------
# Arranca HDFS/YARN en modo “single-node” como usuario 'hadoop'
# --------------------------------------------------------

# 1) Variables de entorno obligatorias
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/opt/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# 2) Forzar que Hadoop ejecute demonios como usuario 'hadoop'
export HDFS_NAMENODE_USER=hadoop
export HDFS_DATANODE_USER=hadoop
export HDFS_SECONDARYNAMENODE_USER=hadoop
export YARN_RESOURCEMANAGER_USER=hadoop
export YARN_NODEMANAGER_USER=hadoop
export YARN_CONF_DIR=$HADOOP_CONF_DIR

echo "export YARN_CONF_DIR=$HADOOP_CONF_DIR" >> /home/hadoop/.bashrc

# 3) Asegurar que 'hadoop' resuelva a 127.0.0.1
if ! grep -q "127.0.0.1 hadoop" /etc/hosts; then
  echo "127.0.0.1 hadoop" >> /etc/hosts
fi

# 4) Arrancar SSH
echo "▶ Iniciando sshd..."
service ssh start

# 5) Formatear NameNode solo la primera vez
if [ ! -d /hadoop/dfs/name/current ]; then
  echo "▶ Formateando NameNode (solo la primera vez)..."
  su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                  export HADOOP_HOME=$HADOOP_HOME; \
                  export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                  \$HADOOP_HOME/bin/hdfs namenode -format -force > /dev/null 2>&1"
else
  echo "▶ Directorio de NameNode ya existe; no formateo."
fi

# 6) Arrancar HDFS (NameNode + DataNode)
echo "▶ Iniciando NameNode..."
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                \$HADOOP_HOME/bin/hdfs --daemon start namenode"

echo "▶ Iniciando DataNode..."
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                \$HADOOP_HOME/bin/hdfs --daemon start datanode"

# 7) Esperar un par de segundos para que HDFS suba
sleep 5

# 7.1) Crear /tmp/hadoop-yarn/staging y dar permisos 777
echo "▶ Creando /tmp/hadoop-yarn/staging en HDFS y dando permisos 777..."
su - hadoop -c "export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                \$HADOOP_HOME/bin/hdfs dfs -mkdir -p /tmp/hadoop-yarn/staging && \
                \$HADOOP_HOME/bin/hdfs dfs -chmod -R 777 /tmp/hadoop-yarn"

# Reemplazar la sección de YARN con:
echo "▶ Iniciando YARN..."
su - hadoop -c "\
  export HADOOP_HOME=$HADOOP_HOME; \
  export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
  \$HADOOP_HOME/bin/yarn --daemon start resourcemanager && \
  \$HADOOP_HOME/bin/yarn --daemon start nodemanager"

# Verificación directa
echo "▶ Verificando procesos YARN..."
if pgrep -f ResourceManager >/dev/null; then
  echo "✔ ResourceManager detectado (PID: $(pgrep -f ResourceManager))"
else
  echo "✖ ResourceManager NO está corriendo"
  echo "▶ Últimos logs:"
  grep -i error /opt/hadoop/logs/*.log | tail -n 10
fi

# 9) Iniciar JobHistoryServer
echo "▶ Iniciando JobHistoryServer..."
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                \$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver"

# 10) Crear /user/waze en HDFS y dar permisos 777
echo "▶ Verificando /user/waze en HDFS..."
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                \$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/waze && \
                \$HADOOP_HOME/bin/hdfs dfs -chmod 777 /user/waze"

# 11) Subir CSV desde /app/incidentes_limpios.csv (ruta dentro del contenedor)
if [ -f /app/incidentes_limpios.csv ]; then
  echo "▶ Subiendo incidentes_limpios.csv desde /app..."
  su - hadoop -c "\
    \$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/waze/input && \
    \$HADOOP_HOME/bin/hdfs dfs -put -f /app/incidentes_limpios.csv /user/waze/input/ && \
    \$HADOOP_HOME/bin/hdfs dfs -chmod -R 777 /user/waze"
else
  echo "⚠ Advertencia: /app/incidentes_limpios.csv no existe"
fi

# 12) Mostrar demonios en ejecución (jps)
echo "▶ Demonios en ejecución (jps):"
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                jps"

# 13) Mantener contenedor en ejecución
echo "▶ init-hadoop.sh completado. Contenedor en ejecución."
tail -f /dev/null
