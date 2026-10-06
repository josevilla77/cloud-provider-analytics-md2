# Arquitectura versión 1

## Patrón elegido

Arquitectura Lambda simplificada:

```text
CSV batch --------------------> PySpark batch -----------+
                                                         |
JSONL en directorio ----------> Structured Streaming ----+
                                                         v
Landing -> Bronze -> Silver -> Gold -> Cassandra/AstraDB -> Consumo
```

Las capacidades de calidad, metadatos, linaje, seguridad, observabilidad e idempotencia atraviesan todas las etapas.

## Responsabilidad de cada zona

- **Landing:** originales inmutables.
- **Bronze:** mismo grano, tipos controlados y trazabilidad.
- **Silver:** limpieza, validación, deduplicación, normalización y joins.
- **Gold:** marts preparados para las consultas del caso.
- **Quarantine:** registros que no cumplen los contratos de calidad.

## Consumo previsto

Las tablas de Cassandra/AstraDB permitirán consultas CQL y podrán alimentar reportes o visualizaciones. El dashboard completo no forma parte de la primera entrega.

