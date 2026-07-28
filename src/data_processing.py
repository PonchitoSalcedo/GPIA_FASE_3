import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, random_state=42, test_size=0.2):
        self.random_state = random_state
        self.test_size = test_size
        self.scaler = StandardScaler()
        self.feature_names = None

    def load_data(self):
        housing = fetch_california_housing()
        df = pd.DataFrame(housing.data, columns=housing.feature_names)
        y = pd.Series(housing.target, name='MedHouseVal')
        self.feature_names = housing.feature_names
        logger.info(f"Datos cargados: {df.shape[0]} registros")
        return df, y

    def preprocess_data(self, X, y=None):
        if y is not None:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        return X_scaled

    def split_data(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state
        )
        return {'X_train': X_train, 'X_test': X_test,
                'y_train': y_train, 'y_test': y_test}

    def save_scaler(self, path='scaler.pkl'):
        joblib.dump(self.scaler, path)
        logger.info(f"Scaler guardado en {path}")
