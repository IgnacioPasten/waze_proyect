#!/bin/bash

#variables de entorno
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/opt/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

#demonios Hadoop
export HDFS_NAMENODE_USER=hadoop
export HDFS_DATANODE_USER=hadoop
export HDFS_SECONDARYNAMENODE_USER=hadoop
export YARN_RESOURCEMANAGER_USER=hadoop
export YARN_NODEMANAGER_USER=hadoop
export YARN_CONF_DIR=$HADOOP_CONF_DIR

echo "export YARN_CONF_DIR=$HADOOP_CONF_DIR" >> /home/hadoop/.bashrc

if ! grep -q "127.0.0.1 hadoop" /etc/hosts; then
  echo "127.0.0.1 hadoop" >> /etc/hosts
fi

#sshd
echo "iniciando sshd"
service ssh start

if [ ! -d /hadoop/dfs/name/current ]; then
  echo "formateando NameNode"
  su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                  export HADOOP_HOME=$HADOOP_HOME; \
                  export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                  \$HADOOP_HOME/bin/hdfs namenode -format -force > /dev/null 2>&1"
else
  echo "NameNode ya existe -> no formateo."
fi

#HDFS
echo "iniciando NameNode"
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                \$HADOOP_HOME/bin/hdfs --daemon start namenode"

echo "iniciando DataNode"
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                \$HADOOP_HOME/bin/hdfs --daemon start datanode"

sleep 5

#permisos
echo "creando /tmp/hadoop-yarn/staging en HDFS y dando permisos"
su - hadoop -c "export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                \$HADOOP_HOME/bin/hdfs dfs -mkdir -p /tmp/hadoop-yarn/staging && \
                \$HADOOP_HOME/bin/hdfs dfs -chmod -R 777 /tmp/hadoop-yarn"

#YARN
echo "iniciando YARN"
su - hadoop -c "\
  export HADOOP_HOME=$HADOOP_HOME; \
  export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
  \$HADOOP_HOME/bin/yarn --daemon start resourcemanager && \
  \$HADOOP_HOME/bin/yarn --daemon start nodemanager"

echo "verificando YARN"
if pgrep -f ResourceManager >/dev/null; then
  echo "ResourceManager detectado -> PID: $(pgrep -f ResourceManager)"
else
  echo "ResourceManager no esta"
  echo "ultimos logs:"
  grep -i error /opt/hadoop/logs/*.log | tail -n 10
fi

#JobHistoryServer
echo "iniciando JobHistoryServer"
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                \$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver"

#permisos
echo "verificando /user/waze en HDFS"
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                \$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/waze && \
                \$HADOOP_HOME/bin/hdfs dfs -chmod 777 /user/waze"

if [ -f /app/incidentes_limpios.csv ]; then
  echo "cargando incidentes_limpios.csv desde /app"
  su - hadoop -c "\
    \$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/waze/input && \
    \$HADOOP_HOME/bin/hdfs dfs -put -f /app/incidentes_limpios.csv /user/waze/input/ && \
    \$HADOOP_HOME/bin/hdfs dfs -chmod -R 777 /user/waze"
else
  echo "/app/incidentes_limpios.csv no existe"
fi

echo "demonios en ejecucion:"
su - hadoop -c "export JAVA_HOME=$JAVA_HOME; \
                export HADOOP_HOME=$HADOOP_HOME; \
                export HADOOP_CONF_DIR=$HADOOP_CONF_DIR; \
                jps"

echo "init-hadoop.sh completado -> contenedor en ejecucion :)"
tail -f /dev/null
