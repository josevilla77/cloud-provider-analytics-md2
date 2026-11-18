# Segundo parcial - Cloud Provider Analytics

**Jose Emiliano Villaverde** · Minería de Datos II - ISTEA

El trabajo está en un solo notebook. Leo los datos, los limpio, calculo costos
diarios y cargo las tablas en Astra. No necesita Docker ni scripts externos.

## Cómo ejecutarlo

1. Abrir `Segundo_Parcial_Jose_Villaverde.ipynb` en Google Colab.
2. Elegir **Entorno de ejecución > Cambiar tipo de entorno > versión 2026.07,
   Python 3.12, CPU**. El notebook instala PySpark 3.5.3 y cassandra-driver 3.29.2.
3. Ejecutar las celdas en orden. En el paso 3 subir el ZIP original del dataset.
   BASE es `/content/md2_jose`: ahí se crean las capas y los checkpoints.
4. Revisar conteos y muestras. Ejecutar las pruebas de repetición y de eventos
   tardíos: en esta última deben quedar los IDs A y B.
5. Crear una base propia en Astra, esperar estado Active y crear el keyspace
   `cloud_analytics` desde su interfaz. Descargar su Secure Connect Bundle y
   generar un token con permisos para crear tablas, escribir y leer.
6. En el paso 21 subir el bundle ZIP e ingresar el token en el campo oculto.
   Ejecutar carga, repetición y dos consultas. `consultas.cql` es la referencia.
7. Ejecutar el paso 27 para descargar capas, checkpoints y evidencia. Descargar
   también el notebook desde **Archivo > Descargar > Descargar .ipynb**.

Para repetir el streaming, conservar Bronze y su checkpoint juntos.
Para empezar una prueba vacía, cambiar BASE y ejecutar todo en orden.
Colab puede borrar sus archivos al terminar la sesión: descargar antes de salir.

## Resultados comprobados

En la ejecución de Jose del 18/11/2026: 80 clientes, 800 usuarios, 240 facturas,
43.200 eventos Bronze, 40.956 válidos, 2.244 en Quarantine y 11.050 filas Gold.
En Astra se enviaron 11.050 filas diarias y 262 de ranking. Dos consultas devolvieron
resultados; al repetir la carga diaria quedaron 11.050 filas antes y después.

El notebook incluido conserva las salidas de la ejecución completa de esta versión.
`Resultados_MD2_Jose.zip` contiene Bronze, Silver, Gold, Quarantine, checkpoints
y los JSON de evidencia. `Evidencia_procesamiento.json` resume esa ejecución.
Silver incluye requests, cpu_hours y storage_gb_hours. La bandera costo_invalido
identifica 211 filas dentro de Quarantine. Se verificaron la repetición sin
duplicados, el balance de registros y la prueba de eventos tardíos.

## Decisiones

- Patrón híbrido: maestros por batch y eventos por Structured Streaming;
  ambos se unen en Silver. No hay Kafka ni una segunda capa de velocidad.
- Bronze conserva datos y metadatos; Silver limpia y enriquece con clientes;
  Gold resume por organización, día y servicio. Parquet particionado por fecha.
- Streaming usa event_id, checkpoint y watermark de 90 días para esta carga
  histórica de 60 días. La prueba separada de 10 minutos muestra el descarte de
  un evento tardío. Landing conserva el original para un eventual reproceso.
- Silver calcula requests, cpu_hours y storage_gb_hours según metric.
  Tokens y carbono conservan sus tipos y los valores desconocidos quedan nulos.
- Calidad: ID no nulo, fecha válida, costo >= -0.01, unidad cuando hay value y
  conversión numérica. costo_invalido marca el problema; Quarantine guarda el motivo.
- Tabla diaria: partición org_id, orden event_date y service para consultar fechas.
  Ranking: partición org_id y fecha_corte, orden por costo descendente.
  Los INSERT con la misma clave actualizan la fila. La prueba repite la misma
  entrada; un ranking recalculado con costos distintos requiere limpiar su corte.
- Analítica inicial: costo diario mayor al percentil 99, umbral observado 61.2773
  y 111 filas marcadas. Es exploratorio: no prueba errores ni fraude.
  Falta confirmar con el docente si acepta este alcance analítico.

## Gobierno y errores

Jose es responsable de la ejecución y revisión. El origen es el dataset del curso.
ingest_ts, source_file y las rutas conservan metadatos; el diagrama muestra el linaje.
Usar datos y evidencias sólo para el trabajo académico. Revisar las salidas antes
de publicarlas y restringir el acceso a la cuenta propia de Astra.
No subir tokens ni bundles a GitHub. El notebook usa getpass para ocultar el token.

Si falla Python, seleccionar el entorno indicado. Si pip avisa un conflicto con
dataproc-spark-connect, comprobar que Spark local indique 3.5.3.
AuthenticationFailed indica revisar token, permisos y bundle de la misma base.
Las advertencias de negociación del protocolo no impidieron la conexión probada.
Si se cerró la conexión al terminar el paso 26, repetir desde el paso 21.
Los errores detienen la ejecución; las salidas del notebook sirven como registro.

## Evidencias publicadas

El notebook ejecutado, el ZIP de resultados y los documentos están publicados
en esta carpeta. Las capturas de las dos consultas en Astra están en
[evidencias de funcionalidad en astra](evidencias%20de%20funcionalidad%20en%20astra/).
La publicación y las capturas ya están completas.

## Pendientes priorizados

- **Obligatorio para el cierre:** incorporar las correcciones del primer parcial
  cuando se disponga del feedback. Confirmar el alcance de analítica con el docente
  y completarlo si corresponde.
- **Deseable para el MVP final:** comparar costos con facturación, analizar por
  sector y automatizar un reproceso de tardíos.
- **Fuera de alcance de esta entrega:** Kafka, dashboard, Docker y despliegue continuo.
