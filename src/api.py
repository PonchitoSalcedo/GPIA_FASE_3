# src/api.py
# API REST para el modelo de predicción de precios de viviendas

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
import logging
from typing import Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# 1. DEFINIR EL ESQUEMA DE ENTRADA (Pydantic)
# ============================================================

class HousingFeatures(BaseModel):
    """Características de entrada para la predicción"""
    MedInc: float = Field(..., description="Ingreso medio del hogar", example=8.3252)
    HouseAge: float = Field(..., description="Antigüedad de la vivienda", example=41.0)
    AveRooms: float = Field(..., description="Promedio de habitaciones", example=6.9841)
    AveBedrms: float = Field(..., description="Promedio de dormitorios", example=1.0238)
    Population: float = Field(..., description="Población", example=322.0)
    AveOccup: float = Field(..., description="Promedio de ocupantes", example=2.5556)
    Latitude: float = Field(..., description="Latitud", example=37.88)
    Longitude: float = Field(..., description="Longitud", example=-122.23)

    class Config:
        schema_extra = {
            "example": {
                "MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.9841,
                "AveBedrms": 1.0238,
                "Population": 322.0,
                "AveOccup": 2.5556,
                "Latitude": 37.88,
                "Longitude": -122.23
            }
        }

# ============================================================
# 2. INICIALIZAR FastAPI Y CARGAR MODELO
# ============================================================

# Crear aplicación FastAPI
app = FastAPI(
    title="California Housing Price Prediction API",
    description="API para predecir el valor medio de viviendas en California",
    version="1.0.0"
)

# Variables globales para el modelo y scaler
model = None
scaler = None

# Orden de las características (debe coincidir con el entrenamiento)
FEATURE_ORDER = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 
                 'Population', 'AveOccup', 'Latitude', 'Longitude']

# ============================================================
# 3. FUNCIÓN PARA CARGAR EL MODELO
# ============================================================

def load_model():
    """Carga el modelo y el scaler desde los archivos"""
    global model, scaler
    
    try:
        model = joblib.load('best_model.pkl')
        scaler = joblib.load('scaler.pkl')
        logger.info("✅ Modelo y scaler cargados correctamente")
        return True
    except FileNotFoundError as e:
        logger.error(f"❌ Error cargando el modelo: {e}")
        logger.error("Asegúrate de que 'best_model.pkl' y 'scaler.pkl' existan")
        return False

# Cargar el modelo al iniciar la aplicación
load_model()

# ============================================================
# 4. ENDPOINTS DE LA API
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Verificar que el modelo esté cargado al iniciar"""
    if model is None:
        logger.warning("⚠️ El modelo no está cargado. Verifica los archivos.")

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "California Housing Price Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "/": "Información de la API",
            "/health": "Verificar estado del modelo",
            "/predict": "Realizar predicción",
            "/predict_batch": "Realizar predicciones por lote",
            "/docs": "Documentación interactiva (Swagger)"
        }
    }

@app.get("/health")
async def health_check():
    """Verificar que el modelo está disponible"""
    if model is None:
        return {
            "status": "unhealthy",
            "message": "Modelo no cargado",
            "model_loaded": False
        }
    return {
        "status": "healthy",
        "message": "Modelo disponible",
        "model_loaded": True,
        "model_type": type(model).__name__
    }

@app.post("/predict")
async def predict(features: HousingFeatures):
    """
    Endpoint para predecir el precio de una vivienda
    
    Recibe las 8 características y devuelve la predicción
    """
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Modelo no disponible. Contacta al administrador."
        )
    
    try:
        # Convertir a array en el orden correcto
        input_data = np.array([[
            features.MedInc,
            features.HouseAge,
            features.AveRooms,
            features.AveBedrms,
            features.Population,
            features.AveOccup,
            features.Latitude,
            features.Longitude
        ]])
        
        # Escalar los datos
        input_scaled = scaler.transform(input_data)
        
        # Realizar predicción
        prediction = model.predict(input_scaled)[0]
        
        # Calcular precio real (en dólares)
        price_dollars = prediction * 100000
        
        logger.info(f"✅ Predicción realizada: {price_dollars:.2f} USD")
        
        return {
            "success": True,
            "prediction": float(prediction),
            "price": float(price_dollars),
            "price_formatted": f"${price_dollars:,.2f}",
            "message": "Predicción realizada correctamente"
        }
        
    except Exception as e:
        logger.error(f"❌ Error en predicción: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")

@app.post("/predict_batch")
async def predict_batch(features_list: list[HousingFeatures]):
    """
    Endpoint para predecir múltiples viviendas
    
    Recibe una lista de características y devuelve las predicciones
    """
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Modelo no disponible. Contacta al administrador."
        )
    
    try:
        predictions = []
        prices = []
        
        for features in features_list:
            input_data = np.array([[
                features.MedInc,
                features.HouseAge,
                features.AveRooms,
                features.AveBedrms,
                features.Population,
                features.AveOccup,
                features.Latitude,
                features.Longitude
            ]])
            
            input_scaled = scaler.transform(input_data)
            pred = model.predict(input_scaled)[0]
            
            predictions.append(float(pred))
            prices.append(float(pred * 100000))
        
        logger.info(f"✅ Predicción por lote: {len(predictions)} muestras")
        
        return {
            "success": True,
            "predictions": predictions,
            "prices": prices,
            "count": len(predictions)
        }
        
    except Exception as e:
        logger.error(f"❌ Error en predicción por lote: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")

@app.get("/model_info")
async def model_info():
    """
    Información del modelo en producción
    """
    if model is None:
        return {"model_loaded": False}
    
    return {
        "model_loaded": True,
        "model_type": type(model).__name__,
        "model_version": "1.0.0",
        "feature_order": FEATURE_ORDER,
        "n_features": len(FEATURE_ORDER)
    }
