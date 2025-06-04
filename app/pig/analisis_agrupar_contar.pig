-- Añadir al inicio del archivo
SET pig.exec.mapPartAgg true;  -- Optimizar agregaciones
SET pig.splitCombination true; -- Combinar archivos pequeños

-- Modificar el análisis temporal para incluir día de la semana
REGISTER '/opt/hadoop/share/hadoop/tools/lib/piggybank.jar';
DEFINE DayOfWeek org.apache.pig.piggybank.evaluation.datetime.extract.DayOfWeek();

-- ... (resto del script existente)

-- Añadir análisis por día de la semana
inc_semana = FOREACH incidentes GENERATE
    DayOfWeek(fecha_dt) AS dia_semana,
    ciudad,
    tipo;

grp_semana = GROUP inc_semana BY dia_semana;
stats_semana = FOREACH grp_semana GENERATE
    group AS dia_semana,
    COUNT(inc_semana) AS total;

STORE stats_semana INTO '/user/waze/output/estadisticas/conteo_por_dia_semana';