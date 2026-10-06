# Cloud Provider Analytics

Proyecto individual para la primera entrega de **Minería de Datos II - ISTEA**.

**Estudiante:** Jose Emiliano Villaverde  
**Profesor:** Diego Mosquera  
**Entrega:** 7 de octubre de 2026

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

Todavía no se implementa el pipeline completo ni la conexión final con AstraDB.

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

## Preparación del entorno

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

## Limitaciones actuales

- No se implementó todavía el pipeline Bronze/Silver/Gold.
- El streaming real se simulará leyendo los JSONL desde un directorio.
- Cassandra/AstraDB se incorporará en la segunda etapa.
- Las escalas de NPS y CSAT deben confirmarse antes de definir reglas definitivas.

