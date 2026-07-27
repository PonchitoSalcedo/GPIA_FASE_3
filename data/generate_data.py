"""
Genera un dataset sintético de churn de clientes de telecomunicaciones.
En un proyecto real reemplazarías esto por la conexión a tu data warehouse
o por el dataset público 'Telco Customer Churn' (Kaggle/IBM).
Se deja como script versionado para que la generación de datos también
sea reproducible y quede bajo control de versiones (principio de MLOps).
"""
import numpy as np
import pandas as pd
from pathlib import Path

def generate_churn_dataset(n_samples: int = 5000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    tenure = rng.integers(0, 72, n_samples)
    monthly_charges = rng.normal(65, 30, n_samples).clip(15, 150)
    contract = rng.choice(["Month-to-month", "One year", "Two year"], n_samples, p=[0.55, 0.25, 0.20])
    internet_service = rng.choice(["DSL", "Fiber optic", "No"], n_samples, p=[0.35, 0.45, 0.20])
    tech_support = rng.choice(["Yes", "No"], n_samples, p=[0.3, 0.7])
    payment_method = rng.choice(
        ["Electronic check", "Mailed check", "Bank transfer", "Credit card"], n_samples
    )
    total_charges = monthly_charges * (tenure + 1) * rng.normal(1, 0.05, n_samples)

    # Señal real para que el modelo tenga algo que aprender (no ruido puro)
    churn_score = (
        -0.05 * tenure
        + 0.01 * monthly_charges
        + (contract == "Month-to-month") * 1.5
        + (internet_service == "Fiber optic") * 0.6
        + (tech_support == "No") * 0.5
        + (payment_method == "Electronic check") * 0.4
        + rng.normal(0, 1.0, n_samples)
    )
    churn_prob = 1 / (1 + np.exp(-(churn_score - 2.0)))
    churn = (rng.random(n_samples) < churn_prob).astype(int)

    df = pd.DataFrame({
        "customer_id": [f"CUST-{i:06d}" for i in range(n_samples)],
        "tenure_months": tenure,
        "monthly_charges": monthly_charges.round(2),
        "total_charges": total_charges.round(2),
        "contract_type": contract,
        "internet_service": internet_service,
        "tech_support": tech_support,
        "payment_method": payment_method,
        "churn": churn,
    })
    return df


if __name__ == "__main__":
    out_dir = Path(__file__).parent
    df = generate_churn_dataset()
    df.to_csv(out_dir / "churn_data.csv", index=False)
    print(f"Dataset generado: {len(df)} filas -> {out_dir / 'churn_data.csv'}")
    print(f"Tasa de churn: {df['churn'].mean():.2%}")
