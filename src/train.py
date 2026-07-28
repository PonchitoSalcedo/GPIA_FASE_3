import mlflow
import mlflow.sklearn
import xgboost as xgb
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_xgboost(X_train, y_train, X_test, y_test, params=None):
    if params is None:
        params = {
            'n_estimators': 200,
            'max_depth': 6,
            'learning_rate': 0.05,
            'subsample': 0.8,
            'random_state': 42
        }

    model = xgb.XGBRegressor(**params)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)

    logger.info(f"R²: {r2:.4f}, RMSE: {rmse:.4f}, MAE: {mae:.4f}")

    joblib.dump(model, 'best_model.pkl')
    logger.info("Modelo guardado como best_model.pkl")

    return model, {'r2': r2, 'rmse': rmse, 'mae': mae}
