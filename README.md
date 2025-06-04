# waze_proyect

Creadores: Ignacio Pastén y Vicente Leiva

# Plataforma de Análisis de Tráfico en Región Metropolitana

Este proyecto es desarrollado para el análisis de tráfico en la Región Metropolitana, utilizando eventos a través de la plataforma Waze. El diseño se basa en microservicios configurados con Docker, permitiendo la extracción, almacenamiento, simulación y gestión de consultas de tráfico.


# Entrega 2

Nuevas funcionalidades agregadas
Procesamiento distribuido con Hadoop para manejar grandes volúmenes de datos

Scripts Pig para transformación y análisis de datos:

filtrar_homogeneizar.pig: Filtra y estandariza los datos de incidentes

analisis_agrupar_contar.pig: Realiza análisis agregados por tipo de incidente

Pipeline completo desde la recolección hasta el análisis

Requisitos adicionales
Docker Compose versión 1.29+

Espacio suficiente en disco para los volúmenes de Hadoop

En sistemas Windows: tener instalado dos2unix para conversión de formatos de archivo

Instalación y ejecución (Entrega 2)
Clona el repositorio (si no lo has hecho):

1. Clona el repositorio y entra al directorio del proyecto:**
```bash
   git clone https://github.com/IgnacioPasten/waze_proyect.git
   cd waze_proyect
```

2. Prepara el sistema con los comandos:
```bash
   docker-compose down -v
   dos2unix init-hadoop.sh
   chmod +x ./init-hadoop.sh
```

3. Ejecuta el sistema con los comandos:
```bash
   docker-compose build
   docker-compose up
```

4. Monitorea la ejecución:
   - En Docker Desktop, abre el contenedor llamado hadoop-pig para visualizar los logs del módulo funcionando.
   - El contenedor mongodb mostrara los logs de la base de datos.

# Entrega 1

# Descripción de los módulos

1. scraper.py
Extrae eventos desde la API de Waze dividiendo el área metropolitana en 52 casillas. Filtra, transforma y guarda los eventos en MongoDB. Soporta traducción de tipos de eventos y extracción de comentarios.

&nbsp;&nbsp;&nbsp;&nbsp;**En la variable `TOTAL_OBJETIVO` se puede ajustar la cantidad de eventos a obtener.**




2. storage.py
Módulo de acceso a datos que permite insertar y consultar eventos almacenados en la base MongoDB.

3. generator.py
Simula consultas de tráfico de diferentes ciudades usando dos modelos de llegada:
- Uniforme: intervalos constantes.
- Poisson: intervalos aleatorios con distribución exponencial.

4. cache.py
Implementa una caché con dos políticas de remoción:
- LRU (Least Recently Used)
- FIFO (First In First Out)

5. main.py
Punto de entrada principal del sistema, permite configurar:
- Política de remoción de caché (LRU o FIFO)
- Tasa de llegada de consultas (rate)
- Modelo de distribución (uniform o poisson)

# Configuración y Ejecución

Requisitos previos
- Tener Docker Desktop instalado y en ejecución.

Pasos de ejecución

1. Clona el repositorio y entra al directorio del proyecto:**
```bash
   git clone https://github.com/IgnacioPasten/waze_proyect.git
   cd waze_proyect
```
2. Configura el comportamiento deseado en app/main.py (o usar lo ya definido):
   - Define la política de caché (LRU o FIFO)
   - Define la tasa de arribo (rate)
   - Define el modelo de distribución (uniform o poisson)

3. Ejecuta el sistema con el comando:
```bash
   docker-compose up --build
```

4. Monitorea la ejecución:
   - En Docker Desktop, abre el contenedor llamado app para visualizar los logs de los módulos funcionando (scraper, generador, caché y almacenamiento).
   - El contenedor mongodb mostrara los logs de la base de datos.

