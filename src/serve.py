"""
API de inferencia (FastAPI). Además de predecir, registra cada solicitud
en un log de auditoría estructurado: qué modelo (versión/hash), qué entrada,
qué salida, cuándo y con qué latencia. Esto es lo que después alimenta al
dashboard de monitoreo y permite responder "¿por qué el modelo decidió esto
el día X?" ante una auditoría.
"""
import hashlib
import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = Path("artifacts/model.joblib")
AUDIT_LOG_PATH = Path("logs/audit_log.jsonl")
MODEL_VERSION_PATH = Path("artifacts/metrics.json")

app = FastAPI(title="Churn Prediction API", version="1.0.0")
_model = None
_model_version_hash = None


class CustomerFeatures(BaseModel):
    tenure_months: int
    monthly_charges: float
    total_charges: float
    contract_type: str
    internet_service: str
    tech_support: str
    payment_method: str


def get_model():
    global _model, _model_version_hash
    if _model is None:
        _model = joblib.load(MODEL_PATH)
        _model_version_hash = hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest()[:12]
    return _model, _model_version_hash


def write_audit_record(request_id: str, payload: dict, prediction: int,
                        probability: float, latency_ms: float, model_version: str):
    AUDIT_LOG_PATH.parent.mkdir(exist_ok=True)
    record = {
        "request_id": request_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model_version": model_version,
        "input": payload,
        "prediction": prediction,
        "probability": round(probability, 4),
        "latency_ms": round(latency_ms, 2),
    }
    with open(AUDIT_LOG_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(features: CustomerFeatures):
    model, version = get_model()
    start = time.perf_counter()

    df = pd.DataFrame([features.model_dump()])
    proba = float(model.predict_proba(df)[0, 1])
    pred = int(proba >= 0.5)

    latency_ms = (time.perf_counter() - start) * 1000
    request_id = str(uuid.uuid4())
    write_audit_record(request_id, features.model_dump(), pred, proba, latency_ms, version)

    return {
        "request_id": request_id,
        "churn_prediction": pred,
        "churn_probability": round(proba, 4),
        "model_version": version,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
