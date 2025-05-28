-- Carga CSV con esquema (ajusta columnas según tu CSV)
incidentes = LOAD '/user/waze/incidentes_limpios.csv'
  USING PigStorage(',')
  AS (fecha:chararray, tipo:chararray, subtipo:chararray, subtipo_normalizado:chararray, ciudad:chararray, calle:chararray, lat:float, lon:float);

-- Filtra registros con datos faltantes
limpios = FILTER incidentes BY (fecha IS NOT NULL) AND (ciudad IS NOT NULL) AND (subtipo_normalizado IS NOT NULL);

-- Agrupa por ciudad (comuna)
por_comuna = GROUP limpios BY ciudad;

-- Cuenta incidentes por comuna
conteo_comuna = FOREACH por_comuna GENERATE group AS comuna, COUNT(limpios) AS total_incidentes;

-- Agrupa por tipo de incidente
por_tipo = GROUP limpios BY subtipo_normalizado;

-- Cuenta incidentes por tipo
conteo_tipo = FOREACH por_tipo GENERATE group AS tipo_incidente, COUNT(limpios) AS total;

-- Guarda resultados en HDFS
STORE conteo_comuna INTO '/user/waze/salida_conteo_comuna' USING PigStorage(',');
STORE conteo_tipo INTO '/user/waze/salida_conteo_tipo' USING PigStorage(',');
