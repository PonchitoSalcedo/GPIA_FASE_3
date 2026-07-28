import joblib
import numpy as np

def test_model_loading():
    model = joblib.load('best_model.pkl')
    assert model is not None

def test_prediction_shape():
    model = joblib.load('best_model.pkl')
    scaler = joblib.load('scaler.pkl')
    dummy = np.random.randn(5, 8)
    dummy_scaled = scaler.transform(dummy)
    preds = model.predict(dummy_scaled)
    assert preds.shape[0] == 5
