--Carga csv
incidentes = LOAD '/data/incidentes_limpios.csv'
  USING PigStorage(',')
  AS (fecha:chararray, tipo:chararray, subtipo:chararray, subtipo_normalizado:chararray, ciudad:chararray, calle:chararray, lat:float, lon:float);

--filtra
limpios = FILTER incidentes BY 
  (fecha IS NOT NULL) AND 
  (ciudad IS NOT NULL) AND 
  (subtipo_normalizado IS NOT NULL) AND
  (lat IS NOT NULL) AND
  (lon IS NOT NULL);

--junta por comuna y tipo
por_comuna_tipo = GROUP limpios BY (ciudad, subtipo_normalizado);

--estadisticas
stats_comuna_tipo = FOREACH por_comuna_tipo GENERATE 
  FLATTEN(group) AS (comuna, tipo_incidente),
  COUNT(limpios) AS total,
  MIN(lat) AS min_lat,
  MAX(lat) AS max_lat,
  MIN(lon) AS min_lon,
  MAX(lon) AS max_lon;

--junta por hora
incidentes_con_hora = FOREACH limpios GENERATE 
  SUBSTRING(fecha, 11, 2) AS hora,
  ciudad,
  subtipo_normalizado;

por_hora = GROUP incidentes_con_hora BY (hora, subtipo_normalizado);

stats_hora = FOREACH por_hora GENERATE
  FLATTEN(group) AS (hora, tipo_incidente),
  COUNT(incidentes_con_hora) AS total;

--resultados
STORE stats_comuna_tipo INTO '/output/stats_comuna_tipo' USING PigStorage(',');
STORE stats_hora INTO '/output/stats_hora' USING PigStorage(',');