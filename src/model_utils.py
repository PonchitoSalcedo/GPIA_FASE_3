import mlflow
import mlflow.sklearn
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_model(model_path='best_model.pkl', model_name='CaliforniaHousingModel'):
    mlflow.set_experiment("production_experiment")
    with mlflow.start_run(run_name="model_registration"):
        model = joblib.load(model_path)
        mlflow.sklearn.log_model(model, model_name)
        logger.info(f"Modelo registrado en MLflow: {model_name}")
