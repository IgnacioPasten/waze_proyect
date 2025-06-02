#!/bin/bash

#
# init-hadoop.sh
# --------------------------------------------------------
# Arranca HDFS/YARN en modo “single‐node” como usuario 'hadoop',
# evitando el uso de start-dfs.sh/start-yarn.sh con SSH.
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

# 3) Asegurar que 'hadoop' resuelva a 127.0.0.1 (para SSH passwordless si hiciera falta)
if ! grep -q "127.0.0.1 hadoop" /etc/hosts; then
  echo "127.0.0.1 hadoop" >> /etc/hosts
fi

# 4) Arrancar el demonio SSH (aún lo dejamos por si algún comando lo requiere)
echo "▶ Iniciando sshd..."
service ssh start

# 5) Formatear NameNode SOLO la primera vez (como usuario 'hadoop')
if [ ! -d /hadoop/dfs/name/current ]; then
  echo "▶ Formateando NameNode (solo la primera vez)..."
  su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                  export HADOOP_HOME=$HADOOP_HOME; \
                  export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                  $HADOOP_HOME/bin/hdfs namenode -format -force > /dev/null 2>&1"
else
  echo "▶ Directorio de NameNode ya existe; no formateo."
fi

# 6) Arrancar HDFS “a mano” (NameNode + DataNode) en modo local
echo "▶ Iniciando NameNode..."
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                $HADOOP_HOME/bin/hdfs --daemon start namenode"

echo "▶ Iniciando DataNode..."
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                $HADOOP_HOME/bin/hdfs --daemon start datanode"

# 7) Esperar un par de segundos para que NameNode y DataNode suban correctamente
sleep 5

# 8) Arrancar YARN “a mano” (ResourceManager + NodeManager) en modo local
echo "▶ Iniciando ResourceManager..."
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                $HADOOP_HOME/bin/yarn --daemon start resourcemanager"

echo "▶ Iniciando NodeManager..."
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                $HADOOP_HOME/bin/yarn --daemon start nodemanager"

# 9) Iniciar JobHistoryServer como usuario 'hadoop'
echo "▶ Iniciando JobHistoryServer..."
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                $HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver"

# 10) Crear /user/waze en HDFS (si no existe) y dar permisos 777
echo "▶ Verificando /user/waze en HDFS..."
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/waze && \
                $HADOOP_HOME/bin/hdfs dfs -chmod 777 /user/waze"

# 11) Subir el CSV limpio si existe en /data
if [ -f /data/incidentes_limpios.csv ]; then
  echo "▶ Subiendo incidentes_limpios.csv a /user/waze/..."
  su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                  export HADOOP_HOME=$HADOOP_HOME; \
                  export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                  $HADOOP_HOME/bin/hdfs dfs -put -f /data/incidentes_limpios.csv /user/waze/"
else
  echo "▶ No existe /data/incidentes_limpios.csv; omito carga."
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
