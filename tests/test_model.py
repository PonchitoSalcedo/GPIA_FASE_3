"""
Pruebas del modelo: no solo "corre sin error", sino que cumple un contrato
mínimo de desempeño y de forma de entrada/salida. Estas pruebas son el
'quality gate' que decide si el pipeline continúa hacia el build de Docker
y el despliegue, o si se detiene.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

sys.path.append(str(Path(__file__).parent.parent / "src"))
from features import FEATURE_COLUMNS, TARGET, build_preprocessor
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

DATA_PATH = Path(__file__).parent.parent / "data" / "churn_data.csv"
MIN_ACCEPTABLE_AUC = 0.70


@pytest.fixture(scope="module")
def trained_pipeline():
    df = pd.read_csv(DATA_PATH)
    X, y = df[FEATURE_COLUMNS], df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    pipe = Pipeline([
        ("preprocessor", build_preprocessor()),
        ("classifier", RandomForestClassifier(n_estimators=150, max_depth=8,
                                               random_state=42, class_weight="balanced")),
    ])
    pipe.fit(X_train, y_train)
    return pipe, X_test, y_test


def test_model_meets_minimum_auc(trained_pipeline):
    pipe, X_test, y_test = trained_pipeline
    proba = pipe.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, proba)
    assert auc >= MIN_ACCEPTABLE_AUC, f"AUC {auc:.3f} por debajo del umbral {MIN_ACCEPTABLE_AUC}"


def test_model_output_shape(trained_pipeline):
    pipe, X_test, _ = trained_pipeline
    preds = pipe.predict(X_test)
    assert len(preds) == len(X_test)
    assert set(preds).issubset({0, 1})


def test_model_handles_unseen_category_gracefully(trained_pipeline):
    # Simula una categoría nueva en producción que no existía en entrenamiento
    pipe, X_test, _ = trained_pipeline
    sample = X_test.iloc[[0]].copy()
    sample["payment_method"] = "Crypto"  # categoría inexistente en el entrenamiento
    pred = pipe.predict(sample)
    assert pred[0] in (0, 1)


def test_predictions_are_deterministic(trained_pipeline):
    pipe, X_test, _ = trained_pipeline
    p1 = pipe.predict(X_test.iloc[:20])
    p2 = pipe.predict(X_test.iloc[:20])
    assert (p1 == p2).all()
