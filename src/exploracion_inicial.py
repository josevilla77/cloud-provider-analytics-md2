"""Exploración inicial reproducible del dataset Cloud Provider Analytics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession, functions as F


CSV_SOURCES = {
    "customers_orgs": ("customers_orgs.csv", "org_id"),
    "users": ("users.csv", "user_id"),
    "resources": ("resources.csv", "resource_id"),
    "support_tickets": ("support_tickets.csv", "ticket_id"),
    "marketing_touches": ("marketing_touches.csv", "touch_id"),
    "nps_surveys": ("nps_surveys.csv", None),
    "billing_monthly": ("billing_monthly.csv", "invoice_id"),
}


def crear_spark() -> SparkSession:
    return (
        SparkSession.builder
        .appName("cloud-provider-analytics-exploracion")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )


def contar_nulos(df: DataFrame) -> dict[str, int]:
    expresiones = [
        F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c)
        for c in df.columns
    ]
    fila = df.agg(*expresiones).first()
    return {c: int(fila[c]) for c in df.columns if fila[c]}


def perfilar(df: DataFrame, clave: str | None) -> dict:
    total = df.count()
    duplicados = None
    if clave:
        duplicados = total - df.select(clave).distinct().count()
    return {
        "registros": total,
        "columnas": df.columns,
        "tipos": {campo.name: campo.dataType.simpleString() for campo in df.schema.fields},
        "nulos": contar_nulos(df),
        "duplicados_clave": duplicados,
    }


def ejecutar(landing: Path) -> dict:
    spark = crear_spark()
    resultado: dict[str, dict] = {}
    try:
        for nombre, (archivo, clave) in CSV_SOURCES.items():
            ruta = landing / archivo
            df = spark.read.option("header", True).option("inferSchema", True).csv(str(ruta))
            resultado[nombre] = perfilar(df, clave)

        eventos = spark.read.json(str(landing / "usage_events_stream" / "*.jsonl"))
        resultado["usage_events_stream"] = perfilar(eventos, "event_id")
        resultado["usage_events_stream"]["archivos"] = 120
        resultado["usage_events_stream"]["versiones_esquema"] = {
            str(fila["schema_version"]): fila["count"]
            for fila in eventos.groupBy("schema_version").count().collect()
        }
    finally:
        spark.stop()
    return resultado


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--landing", type=Path, required=True, help="Ruta a data/landing")
    parser.add_argument("--output", type=Path, required=True, help="Archivo JSON de salida")
    args = parser.parse_args()

    if not args.landing.exists():
        raise FileNotFoundError(f"No existe la ruta de Landing: {args.landing}")

    resultado = ejecutar(args.landing)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(resultado, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Exploración guardada en: {args.output}")


if __name__ == "__main__":
    main()

