# Registro de decisiones

## D-001 - Arquitectura Lambda simplificada

**Estado:** aceptada para la primera versión.

Los CSV tienen comportamiento batch y los JSONL simulan eventos continuos. Separar los dos caminos permite usar la forma de procesamiento más adecuada en cada caso y juntarlos luego en Silver y Gold.

No se incorpora Kafka en el MVP inicial porque Structured Streaming puede leer directamente desde una carpeta. Kafka queda como posible mejora para un escenario productivo.

## D-002 - Landing separada de Bronze

**Estado:** aceptada.

Landing conserva los archivos originales sin modificarlos. Bronze mantiene el mismo grano, pero agrega tipos controlados, `ingest_ts`, `source_file` y `schema_version`.

## D-003 - Parquet para las zonas procesadas

**Estado:** aceptada.

Parquet conserva tipos, comprime mejor que CSV y permite leer columnas y particiones específicas.

## D-004 - DataFrames como API principal

**Estado:** aceptada.

Se usarán DataFrames de PySpark y funciones nativas. Los RDD se reservan para explicar los fundamentos internos de Spark o casos especiales.

## D-005 - Particionamiento inicial

**Estado:** propuesta a validar durante la implementación.

- Eventos: fecha del evento.
- Facturación: mes.
- Maestros pequeños: sin partición.
- Servicio: solo si el volumen final justifica la creación de más archivos.

## D-006 - Temas abiertos

- Confirmar la escala de NPS y CSAT.
- Comparar MAD y percentiles para detectar costos anómalos.
- Definir el watermark después de revisar los retrasos de los eventos.
- Evaluar conector Spark o `foreachBatch` para cargar AstraDB.

