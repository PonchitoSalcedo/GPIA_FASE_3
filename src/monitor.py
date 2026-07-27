"""
Monitoreo del modelo en producción. Se ejecuta periódicamente (ej. cron
diario, o un job en el mismo cluster) y hace dos cosas:

1. Data drift: compara la distribución de las variables numéricas que llegan
   en producción (audit_log) contra la distribución de referencia usada en
   entrenamiento, con la prueba de Kolmogorov-Smirnov.
2. Salud operativa: latencia promedio/p95 y tasa de predicciones positivas,
   para detectar comportamientos anómalos del servicio.

Si se detecta drift significativo, el script termina con código de salida
distinto de cero, lo que permite conectarlo a una alerta en CI/CD o a un
cron con notificación (Slack/email) sin herramientas adicionales.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REFERENCE_DATA_PATH = Path("data/churn_data.csv")
AUDIT_LOG_PATH = Path("logs/audit_log.jsonl")
REPORT_PATH = Path("docs/monitoring_report.json")
DRIFT_PVALUE_THRESHOLD = 0.05
NUMERIC_FEATURES = ["tenure_months", "monthly_charges", "total_charges"]


def load_production_requests() -> pd.DataFrame:
    if not AUDIT_LOG_PATH.exists():
        return pd.DataFrame()
    records = [json.loads(line) for line in open(AUDIT_LOG_PATH)]
    rows = [r["input"] | {"latency_ms": r["latency_ms"], "prediction": r["prediction"]} for r in records]
    return pd.DataFrame(rows)


def check_drift(reference: pd.DataFrame, production: pd.DataFrame) -> dict:
    drift_results = {}
    for col in NUMERIC_FEATURES:
        stat, p_value = stats.ks_2samp(reference[col], production[col])
        drift_results[col] = {
            "ks_statistic": round(float(stat), 4),
            "p_value": round(float(p_value), 4),
            "drift_detected": bool(p_value < DRIFT_PVALUE_THRESHOLD),
        }
    return drift_results


def build_report() -> dict:
    reference = pd.read_csv(REFERENCE_DATA_PATH)
    production = load_production_requests()

    report = {"n_production_requests": len(production)}

    if production.empty:
        report["status"] = "SIN_DATOS_SUFICIENTES"
        return report

    report["drift"] = check_drift(reference, production)
    report["any_drift_detected"] = any(v["drift_detected"] for v in report["drift"].values())
    report["operational"] = {
        "avg_latency_ms": round(float(production["latency_ms"].mean()), 2),
        "p95_latency_ms": round(float(np.percentile(production["latency_ms"], 95)), 2),
        "positive_prediction_rate": round(float(production["prediction"].mean()), 4),
    }
    report["status"] = "DRIFT_DETECTADO" if report["any_drift_detected"] else "OK"
    return report


if __name__ == "__main__":
    REPORT_PATH.parent.mkdir(exist_ok=True)
    report = build_report()
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))
    if report.get("status") == "DRIFT_DETECTADO":
        sys.exit(1)
