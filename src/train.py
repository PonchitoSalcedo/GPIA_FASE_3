"""
Entrenamiento del modelo de churn con:
 - Tracking de experimentos (MLflow): parámetros, métricas y artefactos.
 - Versionado de modelos (MLflow Model Registry): cada entrenamiento
   exitoso registra una nueva versión del modelo, nunca sobrescribe.
 - Optimización de hiperparámetros (GridSearchCV) documentada como
   evidencia de la fase de "optimización del sistema".

Uso:
    python src/train.py --data data/churn_data.csv --model-name churn-predictor
"""
import argparse
import json
import sys
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                              recall_score, roc_auc_score)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline

sys.path.append(str(Path(__file__).parent))
from features import FEATURE_COLUMNS, TARGET, build_preprocessor

MIN_ACCEPTABLE_AUC = 0.70  # gate de calidad: por debajo de esto, el pipeline falla


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = set(FEATURE_COLUMNS + [TARGET]) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas en el dataset: {missing}")
    return df


def train(data_path: str, model_name: str, experiment_name: str = "churn-prediction",
           output_dir: str = "artifacts") -> dict:
    df = load_data(data_path)
    X, y = df[FEATURE_COLUMNS], df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("preprocessor", build_preprocessor()),
        ("classifier", RandomForestClassifier(random_state=42, class_weight="balanced")),
    ])

    # Optimización de hiperparámetros: evidencia versionada de las decisiones técnicas
    param_grid = {
        "classifier__n_estimators": [100, 200],
        "classifier__max_depth": [6, 10, None],
        "classifier__min_samples_leaf": [1, 5],
    }

    mlflow.set_experiment(experiment_name)
    with mlflow.start_run() as run:
        search = GridSearchCV(pipeline, param_grid, cv=3, scoring="roc_auc", n_jobs=-1)
        search.fit(X_train, y_train)
        best_model = search.best_estimator_

        y_pred = best_model.predict(X_test)
        y_proba = best_model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred),
            "roc_auc": roc_auc_score(y_test, y_proba),
        }

        mlflow.log_params(search.best_params_)
        mlflow.log_metrics(metrics)
        mlflow.log_param("train_rows", len(X_train))
        mlflow.log_param("test_rows", len(X_test))

        # Prueba automatizada de calidad de modelo (gate del pipeline CI/CD)
        if metrics["roc_auc"] < MIN_ACCEPTABLE_AUC:
            mlflow.set_tag("status", "REJECTED_QUALITY_GATE")
            raise SystemExit(
                f"Modelo RECHAZADO: ROC-AUC {metrics['roc_auc']:.3f} "
                f"por debajo del umbral mínimo {MIN_ACCEPTABLE_AUC}"
            )

        mlflow.sklearn.log_model(
            best_model,
            artifact_path="model",
            registered_model_name=model_name,
        )
        mlflow.set_tag("status", "APPROVED")

        # Artefacto local adicional para el paso de Docker/serving
        out = Path(output_dir)
        out.mkdir(exist_ok=True)
        joblib.dump(best_model, out / "model.joblib")
        with open(out / "metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

        print(f"Run ID: {run.info.run_id}")
        print(f"Mejores hiperparámetros: {search.best_params_}")
        print(f"Métricas: {json.dumps(metrics, indent=2)}")
        return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/churn_data.csv")
    parser.add_argument("--model-name", default="churn-predictor")
    parser.add_argument("--output-dir", default="artifacts")
    args = parser.parse_args()
    train(args.data, args.model_name, output_dir=args.output_dir)
