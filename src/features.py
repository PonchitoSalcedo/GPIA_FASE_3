"""
Preprocesamiento compartido. Vive en un único módulo importado tanto por
train.py como por serve.py para evitar 'training-serving skew'
(que el modelo vea en producción features distintas a las de entrenamiento).
"""
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_FEATURES = ["tenure_months", "monthly_charges", "total_charges"]
CATEGORICAL_FEATURES = ["contract_type", "internet_service", "tech_support", "payment_method"]
TARGET = "churn"
FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
