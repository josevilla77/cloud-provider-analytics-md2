-- Crear cloud_analytics desde la interfaz de Astra. Usar una cuenta propia.
USE cloud_analytics;

CREATE TABLE IF NOT EXISTS org_daily_usage_by_service (
 org_id text, event_date date, service text,
 daily_cost_usd double, requests double, genai_tokens bigint,
 carbon_kg double, event_count bigint,
 PRIMARY KEY ((org_id), event_date, service)
) WITH CLUSTERING ORDER BY (event_date ASC, service ASC);

CREATE TABLE IF NOT EXISTS top_services_14d (
 org_id text, fecha_corte date, costo_14d double, service text,
 PRIMARY KEY ((org_id, fecha_corte), costo_14d, service)
) WITH CLUSTERING ORDER BY (costo_14d DESC, service ASC);

-- Organización usada en la ejecución verificada del notebook.
-- 1. Costos y requests por día y servicio, en un rango de fechas.
SELECT event_date, service, daily_cost_usd, requests
FROM org_daily_usage_by_service
WHERE org_id = 'org_0lvsnujz'
AND event_date >= '2025-08-18' AND event_date <= '2025-08-31';

-- 2. Los cinco servicios más costosos de los últimos 14 días del histórico.
SELECT service, costo_14d
FROM top_services_14d
WHERE org_id = 'org_0lvsnujz' AND fecha_corte = '2025-08-31'
LIMIT 5;
