-- Cargar CSV limpio
raw_data = LOAD 'incidentes_limpios.csv' USING PigStorage(',')
    AS (fecha:chararray, tipo:chararray, subtipo:chararray, subtipo_normalizado:chararray,
        ciudad:chararray, calle:chararray, lat:double, lon:double);

-- Agrupar por comuna (ciudad)
por_ciudad = GROUP raw_data BY ciudad;

-- Contar incidentes por ciudad
cuenta_por_ciudad = FOREACH por_ciudad GENERATE group AS ciudad, COUNT(raw_data) AS total_incidentes;

-- Agrupar por tipo
por_tipo = GROUP raw_data BY subtipo_normalizado;
cuenta_por_tipo = FOREACH por_tipo GENERATE group AS tipo_incidente, COUNT(raw_data) AS cantidad;

-- Guardar resultados
STORE cuenta_por_ciudad INTO 'resultados/por_ciudad' USING PigStorage(',');
STORE cuenta_por_tipo INTO 'resultados/por_tipo' USING PigStorage(',');
