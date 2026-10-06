# Matriz requisito-componente

| Requisito | Componente | Evidencia esperada |
|---|---|---|
| Leer CSV y JSONL | PySpark batch | Esquemas, conteos y Bronze Parquet |
| Procesar eventos incrementales | Structured Streaming | Watermark, checkpoint y deduplicación |
| Conservar originales | Landing | Archivos intactos y trazables |
| Limpiar y relacionar datos | Silver | Reglas, joins y conteos |
| Separar inválidos | Quarantine | Razón de rechazo y muestra |
| Publicar métricas | Gold | Marts con grano documentado |
| Responder consultas | Cassandra/AstraDB | CQL y resultados reproducibles |
| Evitar duplicados | Checkpoint, claves y upserts | Conteos antes y después de reejecutar |
| Documentar decisiones | README y DECISIONS.md | Historial y justificaciones |

