--archivo csv
incidentes = LOAD '/user/waze/incidentes_limpios.csv' USING PigStorage(',') 
    AS (fecha:chararray, tipo:chararray, subtipo:chararray, subtipo_normalizado:chararray, ciudad:chararray, calle:chararray, lat:double, lon:double);

--tipo tráfico
incidentes_trafico = FILTER incidentes BY tipo == 'Tráfico';

--ciudad a minúsculas
incidentes_trafico_lower = FOREACH incidentes_trafico GENERATE 
    fecha, 
    tipo, 
    subtipo, 
    subtipo_normalizado, 
    LOWER(ciudad) AS ciudad, 
    calle, 
    lat, 
    lon;

-- hdfs dfs -rm -r /user/waze/incidentes_trafico_limpios

--guarda en csv
STORE incidentes_trafico_lower INTO '/user/waze/incidentes_trafico_limpios' USING PigStorage(',');
