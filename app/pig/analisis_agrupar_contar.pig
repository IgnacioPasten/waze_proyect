-- analisis_agrupar_contar.pig

-- 0) Registrar el JAR correcto (ajusta según lo que veas en /opt/pig/lib)
- REGISTER '/opt/pig-0.17.0-src/contrib/piggybank/java/build/piggybank.jar';
+ REGISTER '/opt/pig/lib/piggybank.jar';

  DEFINE Hour org.apache.pig.piggybank.evaluation.datetime.extract.Hour();

-- --------------------------------------------------------
-- Este script asume que ya existe '/user/waze/output/incidentes_homogeneizados'
-- --------------------------------------------------------

%default INPUT_HOMO '/user/waze/output/incidentes_homogeneizados';

-- 1. Cargo los datos (tab-separated)
incidentes = LOAD '$INPUT_HOMO' USING PigStorage('\t')
    AS (
        fecha_dt:datetime,
        ciudad:chararray,
        tipo:chararray,
        subtipo_norm:chararray,
        calle:chararray,
        lat:double,
        lon:double
    );

-- 2. Conteo por ciudad
grp_ciudad = GROUP incidentes BY ciudad;
conteo_ciudad = FOREACH grp_ciudad GENERATE
    group              AS ciudad,
    COUNT(incidentes)  AS total_incidentes;

STORE conteo_ciudad
    INTO '/user/waze/output/estadisticas/conteo_por_ciudad'
    USING PigStorage('\t');

-- 3. Conteo por tipo en todo el dataset
grp_tipo = GROUP incidentes BY tipo;
conteo_tipo = FOREACH grp_tipo GENERATE
    group              AS tipo,
    COUNT(incidentes)  AS total_incidentes_tipo;

STORE conteo_tipo
    INTO '/user/waze/output/estadisticas/conteo_por_tipo'
    USING PigStorage('\t');

-- 4. Conteo por (ciudad, tipo)
grp_ciud_tipo = GROUP incidentes BY (ciudad, tipo);
conteo_ciud_tipo = FOREACH grp_ciud_tipo GENERATE
    FLATTEN(group)     AS (ciudad_group:chararray, tipo_group:chararray),
    COUNT(incidentes)  AS total;

STORE conteo_ciud_tipo
    INTO '/user/waze/output/estadisticas/conteo_por_ciud_tipo'
    USING PigStorage('\t');

-- 5. Conteo opcional por hora del día
inc_hora = FOREACH incidentes GENERATE
    Hour(fecha_dt)     AS hora:int,
    ciudad             AS ciudad:chararray,
    tipo               AS tipo:chararray;

grp_hora = GROUP inc_hora BY hora;
conteo_hora = FOREACH grp_hora GENERATE
    group              AS hora,
    COUNT(inc_hora)    AS total_en_hora;

STORE conteo_hora
    INTO '/user/waze/output/estadisticas/conteo_por_hora'
    USING PigStorage('\t');
