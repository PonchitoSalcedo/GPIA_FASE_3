import joblib
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelPredictor:
    def __init__(self, model_path='best_model.pkl', scaler_path='scaler.pkl'):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        logger.info("Modelo y scaler cargados")

    def predict(self, data):
        if isinstance(data, list):
            data = np.array(data)
        if data.ndim == 1:
            data = data.reshape(1, -1)
        data_scaled = self.scaler.transform(data)
        return self.model.predict(data_scaled)
