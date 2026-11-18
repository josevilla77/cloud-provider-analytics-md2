# Cloud Provider Analytics

Proyecto individual de **Minería de Datos II - ISTEA**.

**Estudiante:** Jose Emiliano Villaverde  
**Profesor:** Diego Mosquera  
**Primera entrega:** 7 de octubre de 2026

**Segunda entrega:** 18 de noviembre de 2026

## Segunda entrega

La implementación ejecutable está en [entrega 2](entrega%202/README.md).
Incluye el notebook ejecutado en Colab, las capas Bronze/Silver/Gold en Parquet,
Quarantine, el diagrama actualizado, las consultas CQL y sus capturas de resultados.
La carga y las dos consultas en AstraDB están verificadas; la repetición de la
carga diaria conserva 11.050 filas antes y después.

Para ejecutar esta etapa, seguir el README de esa carpeta: **Colab con entorno
2026.07, Python 3.12, CPU**. Los resultados se conservan en
[Resultados_MD2_Jose.zip](entrega%202/Resultados_MD2_Jose.zip).

## Documentación de la primera entrega

Las secciones siguientes conservan el diseño inicial y las instrucciones de la
primera entrega. Su estado y sus limitaciones corresponden a esa etapa.

## ¿De qué trata el proyecto?

El caso representa a una empresa que ofrece servicios cloud. Los datos llegan desde archivos CSV y desde eventos JSONL que simulan un flujo continuo. La idea es construir, de manera progresiva, un pipeline que permita analizar costos, facturación, soporte y uso de productos.

Para el diseño inicial elegí una arquitectura Lambda simplificada:

- Los CSV se procesan por lotes con PySpark.
- Los eventos JSONL se procesan con Spark Structured Streaming.
- Los datos pasan por Landing, Bronze, Silver y Gold.
- Los registros inválidos se separan en Quarantine.
- Los resultados Gold se publicarán en Cassandra/AstraDB.

## Alcance de la primera entrega

Esta entrega se concentra en comprender el caso y dejar una base clara para la implementación. Incluye:

- análisis de las 5V;
- inventario y perfil inicial de las fuentes;
- arquitectura versión 1;
- diseño del Data Lake;
- flujos batch y streaming;
- ejemplo conceptual de MapReduce;
- matriz requisito-componente;
- supuestos, riesgos y plan de trabajo;
- exploración inicial reproducible.

En la primera entrega todavía no se implementaba el pipeline completo ni la conexión final con AstraDB. Ambos se implementaron en la segunda entrega, enlazada arriba.

## Estructura

```text
cloud-provider-analytics/
├── README.md
├── DECISIONS.md
├── requirements.txt
├── config/
│   └── config.example.yaml
├── data/
│   └── README.md
├── docs/
│   ├── arquitectura.md
│   ├── matriz_requisitos.md
│   └── Primer_Parcial_Mineria_Datos_II_Jose_Emiliano_Villaverde.pdf
├── evidence/
│   └── resumen_exploracion.csv
├── notebooks/
│   └── README.md
├── src/
│   └── exploracion_inicial.py
└── tests/
    └── test_estructura.py
```

## Preparación del entorno de la primera entrega

Requisitos:

- Python 3.11 o superior.
- Java 17.
- Git.

Crear y activar un entorno virtual:

```bash
python -m venv .venv
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ubicación del dataset

El ZIP entregado por la cátedra no se modifica. Se debe descomprimir de forma que exista esta ruta:

```text
data/landing/customers_orgs.csv
data/landing/users.csv
data/landing/resources.csv
data/landing/support_tickets.csv
data/landing/marketing_touches.csv
data/landing/nps_surveys.csv
data/landing/billing_monthly.csv
data/landing/usage_events_stream/*.jsonl
```

La carpeta `data/landing/` está ignorada por Git para evitar subir los datos originales al repositorio.

## Ejecutar la exploración

Desde la raíz del repositorio:

```bash
python src/exploracion_inicial.py --landing data/landing --output evidence/exploracion_generada.json
```

El script:

1. inicia una sesión local de Spark;
2. lee los siete CSV y los JSONL;
3. cuenta registros;
4. muestra los esquemas inferidos como evidencia exploratoria;
5. mide nulos y duplicados en las claves principales;
6. guarda un resumen JSON en `evidence/`.

Para esta primera exploración se permite observar el esquema inferido. En el pipeline de implementación se reemplazará por esquemas explícitos.

## Ejecutar la prueba básica

```bash
python -m unittest tests/test_estructura.py
```

## Decisiones importantes

Las decisiones y temas todavía abiertos están documentados en [DECISIONS.md](DECISIONS.md).

## Limitaciones de la primera entrega

- No se implementó todavía el pipeline Bronze/Silver/Gold.
- El streaming real se simulará leyendo los JSONL desde un directorio.
- Cassandra/AstraDB se incorporará en la segunda etapa.
- Las escalas de NPS y CSAT deben confirmarse antes de definir reglas definitivas.

