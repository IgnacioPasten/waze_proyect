-- Carga el archivo CSV con esquema
incidentes = LOAD '/user/waze/incidentes_limpios.csv' USING PigStorage(',') 
    AS (fecha:chararray, tipo:chararray, subtipo:chararray, subtipo_normalizado:chararray, ciudad:chararray, calle:chararray, lat:double, lon:double);

-- Filtra solo los incidentes de tipo "Tráfico"
incidentes_trafico = FILTER incidentes BY tipo == 'Tráfico';

-- Convierte ciudad a minúsculas
incidentes_trafico_lower = FOREACH incidentes_trafico GENERATE 
    fecha, 
    tipo, 
    subtipo, 
    subtipo_normalizado, 
    LOWER(ciudad) AS ciudad, 
    calle, 
    lat, 
    lon;

-- Borra la carpeta destino si ya existe (ejecutar manualmente antes en la terminal)
-- hdfs dfs -rm -r /user/waze/incidentes_trafico_limpios

-- Guarda los datos filtrados y procesados en HDFS en CSV
STORE incidentes_trafico_lower INTO '/user/waze/incidentes_trafico_limpios' USING PigStorage(',');
