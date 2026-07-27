"""
Pruebas de calidad de datos. Se ejecutan en cada push (integración continua)
para evitar que datos corruptos o con drift estructural lleguen a entrenar
un modelo nuevo.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.append(str(Path(__file__).parent.parent / "src"))
from features import FEATURE_COLUMNS, TARGET

DATA_PATH = Path(__file__).parent.parent / "data" / "churn_data.csv"


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(DATA_PATH)


def test_dataset_not_empty(df):
    assert len(df) > 100, "El dataset tiene muy pocas filas"


def test_required_columns_present(df):
    missing = set(FEATURE_COLUMNS + [TARGET]) - set(df.columns)
    assert not missing, f"Faltan columnas: {missing}"


def test_no_nulls_in_target(df):
    assert df[TARGET].isnull().sum() == 0


def test_target_is_binary(df):
    assert set(df[TARGET].unique()).issubset({0, 1})


def test_no_duplicate_customers(df):
    assert df["customer_id"].duplicated().sum() == 0


def test_numeric_ranges_are_sane(df):
    assert (df["tenure_months"] >= 0).all()
    assert (df["monthly_charges"] > 0).all()


def test_churn_rate_within_expected_band(df):
    # Alerta temprana de drift: si la tasa de churn se sale de un rango
    # razonable, algo cambió en el negocio o en la extracción de datos.
    rate = df[TARGET].mean()
    assert 0.05 <= rate <= 0.60, f"Tasa de churn fuera de rango esperado: {rate:.2%}"
