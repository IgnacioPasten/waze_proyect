SET pig.exec.mapPartAgg true;
SET pig.splitCombination true;

REGISTER '/opt/hadoop/share/hadoop/tools/lib/piggybank.jar';
DEFINE DayOfWeek org.apache.pig.piggybank.evaluation.datetime.extract.DayOfWeek();

--analisis x dia de la semana
inc_semana = FOREACH incidentes GENERATE
    DayOfWeek(fecha_dt) AS dia_semana,
    ciudad,
    tipo;

grp_semana = GROUP inc_semana BY dia_semana;
stats_semana = FOREACH grp_semana GENERATE
    group AS dia_semana,
    COUNT(inc_semana) AS total;

STORE stats_semana INTO '/user/waze/output/estadisticas/conteo_por_dia_semana';