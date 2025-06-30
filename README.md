# waze_proyect

Creadores: Ignacio Pastén y Vicente Leiva

# Plataforma de Análisis de Tráfico en Región Metropolitana

Este proyecto es desarrollado para el análisis de tráfico en la Región Metropolitana, utilizando eventos a través de la plataforma Waze. El diseño se basa en microservicios configurados con Docker, permitiendo la extracción, almacenamiento, simulación y gestión de consultas de tráfico.

# Entrega 3

Nuevas funcionalidades agregadas
Sistema completo de visualización y análisis en tiempo real

Características principales de la Entrega 3:

**Sistema de Visualización Integrado:**
- Dashboards interactivos en Kibana para análisis en tiempo real
- Métricas avanzadas de rendimiento del cache (LRU vs FIFO)
- Monitoreo del sistema completo

**Pipeline Completo Integrado:**
- main.py como punto de entrada único del sistema completo
- Configuración automática de Elasticsearch y Kibana
- Sistema de métricas y logging

**Instalación y ejecución:**

1. Instalar dependencias Python:
```bash
   python install_requirements.py
```

2. Iniciar servicios Docker:
```bash
   docker-compose up -d
```

3. Ejecutar sistema completo:
```bash
   cd app
   python main.py
```

4. Para modo visualziación:
```bash
   python main.py --visualizar
```

**Acceso a visualizaciones:**
- Kibana Dashboard: http://localhost:5601/app/kibana
   ir a dashboards para ver gráficos e indicar "Last 24 hours"
- Elasticsearch: http://localhost:9200

**Opciones de ejecución:**
- `--skip-scraper`: omitir fase de scraping
- `--skip-processing`: omitir fase de procesamiento
- `--skip-cache`: omitir fase de cache

# Entrega 2

Nuevas funcionalidades agregadas
Procesamiento distribuido con Hadoop para manejar grandes volúmenes de datos

Scripts Pig para transformación y análisis de datos:

filtrar_homogeneizar.pig: Filtra y estandariza los datos de incidentes

analisis_agrupar_contar.pig: Realiza análisis agregados por tipo de incidente

Pipeline completo desde la recolección hasta el análisis

Requisitos adicionales
Docker Compose versión 1.29+

En sistemas Windows: tener instalado dos2unix para conversión de formatos de archivo

Instalación y ejecución:

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

**Módulos principales:**

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
Punto de entrada principal del sistema completo. Ejecuta todo el pipeline integrado:
- Scraping de datos de tráfico desde Waze
- Procesamiento y limpieza de datos (limpiador.py + Hadoop/Pig)
- Testing de sistemas de cache (LRU vs FIFO) con métricas avanzadas
- Visualización automática en Kibana con dashboards
- Monitoreo en tiempo real del sistema
- Configuración automática de Elasticsearch e índices
- Generación de reportes del sistema

Opciones de configuración:
- Políticas de cache (LRU o FIFO) con comparación automática
- Modo demostración con datos adicionales
- Generación de reportes y métricas
- Control granular de fases a ejecutar

6. limpiador.py
Procesa y limpia los datos extraídos, normalizando tipos de eventos y generando archivos CSV para análisis posterior.

**Módulos de visualización (Entrega 3):**

7. visualization_controller.py
Controlador central del sistema de visualización que coordina la creación de dashboards y métricas en tiempo real.

8. elasticsearch_logger.py
Maneja el logging de métricas del sistema hacia Elasticsearch para su posterior visualización en Kibana.

9. cache_metrics_logger.py
Sistema avanzado de logging específico para métricas de rendimiento del cache.

10. advanced_kibana_setup.py
Configuración automática de dashboards, visualizaciones e índices en Kibana.

# Configuración y Ejecución

Requisitos previos
- Tener Docker Desktop instalado y en ejecución.

Pasos de ejecución

1. Clona el repositorio y entra al directorio del proyecto:
```bash
   git clone https://github.com/IgnacioPasten/waze_proyect.git
   cd waze_proyect
```

2. Instala las dependencias Python (una sola vez):
```bash
   python install_requirements.py
```

3. Inicia los servicios Docker:
```bash
   docker-compose up -d
```

4. Ejecuta el sistema completo:
```bash
   cd app
   python main.py
```

Para modo demostración con datos adicionales:
```bash
   python main.py --demo-mode --generate-report
```

5. Monitorea la ejecución:
   - Los logs del sistema aparecen en la consola donde ejecutaste main.py
   - Accede a los dashboards en Kibana: http://localhost:5601/app/kibana
   - Revisa las métricas en Elasticsearch: http://localhost:9200
   - El archivo waze_system.log contiene logs detallados del sistema

