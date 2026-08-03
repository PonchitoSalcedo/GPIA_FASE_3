<img width="1536" height="2752" alt="Pipeline_MLOps_y_Valor_Estratégico" src="https://github.com/user-attachments/assets/4c9be85f-1d97-4b6e-8f83-c72b7b017524" />



# 🏠 Pipeline Automatizado de IA para Predicción de Precios de Viviendas en California

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![MLflow](https://img.shields.io/badge/MLflow-2.3.1-orange.svg)](https://mlflow.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0-blue.svg)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub%20Actions-brightgreen.svg)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Tabla de Contenidos

- [📖 Descripción del Proyecto](#-descripción-del-proyecto)
- [🎯 Problema de Negocio](#-problema-de-negocio)
- [🏗️ Arquitectura de la Solución](#️-arquitectura-de-la-solución)
- [📊 Resultados del Modelo](#-resultados-del-modelo)
- [🛠️ Stack Tecnológico](#️-stack-tecnológico)
- [🚀 Instalación y Configuración](#-instalación-y-configuración)
- [📓 Notebooks de Colab](#-notebooks-de-colab)
- [🐳 Despliegue con Docker](#-despliegue-con-docker)
- [🤖 CI/CD con GitHub Actions](#-cicd-con-github-actions)
- [📈 Monitoreo y Métricas](#-monitoreo-y-métricas)
- [📝 Documentación Técnica](#-documentación-técnica)
- [🤝 Contribuciones](#-contribuciones)
- [📄 Licencia](#-licencia)
- [📧 Contacto](#-contacto)

---

## 📖 Descripción del Proyecto

Este proyecto implementa un **pipeline completo de Machine Learning** para la predicción de precios de viviendas en California, integrando prácticas de **MLOps** y **GitOps** para asegurar la calidad, reproducibilidad y despliegue continuo de modelos en producción.

El pipeline cubre todas las fases del ciclo de vida de un modelo de IA:
- ✅ **Integración Continua** (CI)
- ✅ **Pruebas Automatizadas** de código y datos
- ✅ **Versionado de Modelos** con MLflow
- ✅ **Despliegue Continuo** (CD)
- ✅ **Monitoreo y Auditoría** en producción
- ✅ **Optimización del Sistema**

---

## 🎯 Problema de Negocio

### El Desafío
El mercado inmobiliario de California presenta un desafío complejo para la predicción de precios debido a la gran cantidad de variables que influyen en el valor de las viviendas.

### Dataset
- **Fuente:** California Housing Dataset (scikit-learn)
- **Registros:** 20,640 muestras
- **Variables:** 8 características predictoras
- **Target:** `MedHouseVal` (Valor medio de la vivienda en decenas de miles de dólares)

### Variables del Dataset

| Variable | Descripción |
|----------|-------------|
| **MedInc** | Ingreso medio de los hogares en el distrito |
| **HouseAge** | Antigüedad media de las viviendas |
| **AveRooms** | Número promedio de habitaciones |
| **AveBedrms** | Número promedio de dormitorios |
| **Population** | Población total del distrito |
| **AveOccup** | Promedio de ocupantes por hogar |
| **Latitude** | Latitud geográfica |
| **Longitude** | Longitud geográfica |

---

## ️ Arquitectura de la Solución

### Diagrama de Arquitectura

**🖥️ INTERFAZ DE USUARIO**
- API REST + Dashboard Web
  ↓
**⚙️ CAPA DE APLICACIÓN**
- FastAPI (Service)
- MLflow (Tracking)
- DVC (Versioning)
- Prometheus (Metrics)
  ↓
**💾 CAPA DE DATOS**
- Raw Data (CSV)
- Processed Data
- Features Store
- Predictions Store
  ↓
**🏗️ INFRAESTRUCTURA**
- Docker (Containers)
- Kubernetes (Cluster)
- AWS (Services)
- GitHub (Actions)

---

### Pipeline CI/CD

**🔄 GITHUB ACTIONS PIPELINE**

Testing (CI) → Training → Evaluation → Deploy (CD) → Monitor


---

## 📊 Resultados del Modelo

### Mejor Modelo: XGBoost Optimizado

| Métrica | Valor | Estándar | Estado |
|---------|-------|----------|--------|
| **R² Score** | 0.8321 | > 0.80 | ✅ Excelente |
| **RMSE** | 0.5743 | < 0.60 | ✅ Bueno |
| **MAE** | 0.3981 | < 0.50 | ✅ Bueno |
| **MSE** | 0.3298 | - | - |
| **Explained Variance** | 0.8335 | - | - |

### Hiperparámetros Óptimos

yaml
XGBoost Optimizado:
  n_estimators: 200
  max_depth: 6
  learning_rate: 0.05
  subsample: 0.8

## Importancia de Características

| Feature | Importancia | Impacto |
|---------|-------------|---------|
| **MedInc** | 35.2% | 🟢 Alto |
| **AveRooms** | 18.7% | 🟡 Medio-Alto |
| **Latitude** | 14.3% | 🟡 Medio |
| **Longitude** | 12.1% | 🟡 Medio |
| **HouseAge** | 8.5% | 🟠 Bajo-Medio |
| **AveBedrms** | 5.2% | 🔴 Bajo |
| **Population** | 3.8% | 🔴 Bajo |
| **AveOccup** | 2.2% | 🔴 Muy Bajo |

---

## Visualizaciones del Modelo

### 📊 Distribución de Variables
![Distribución de Variables](https://artefactos_notebook1/distribucion_variables.png)

### 🔍 Matriz de Correlación
![Matriz de Correlación](https://artefactos_notebook1/matriz_correlacion.png)

### ✅ Comparación de Modelos
![Comparación de Modelos](https://artefactos_notebook2/model_comparison.png)

### 🎯 Importancia de Características
![Importancia de Características](https://artefactos_notebook2/feature_importance.png)

### 📈 Evaluación del Modelo
![Evaluación del Modelo](https://artefactos_notebook3/model_evaluation.png)

---

## 🛠️ Stack Tecnológico

### Lenguajes y Frameworks

| Componente | Tecnología | Versión | Propósito |
|------------|------------|---------|-----------|
| **Lenguaje** | Python | 3.9 | Desarrollo principal |
| **ML** | scikit-learn | 1.2.2 | Modelos base |
| **ML** | XGBoost | 1.7.5 | Modelo principal |
| **ML** | LightGBM | 3.3.5 | Modelo alternativo |
| **API** | FastAPI | 0.95.2 | Servicios web |
| **API** | Uvicorn | 0.22.0 | Servidor ASGI |

### MLOps y DevOps

| Componente | Tecnología | Versión | Propósito |
|------------|------------|---------|-----------|
| **Tracking** | MLflow | 2.3.1 | Versionado de modelos |
| **Data Versioning** | DVC | 2.44.1 | Versionado de datos |
| **CI/CD** | GitHub Actions | - | Automatización |
| **Containerization** | Docker | 24.0 | Contenedores |
| **Orchestration** | Kubernetes | - | Orquestación |
| **Monitoring** | Prometheus | - | Métricas |
| **Visualization** | Grafana | - | Dashboards |

### Testing y Calidad

| Componente | Tecnología | Propósito |
|------------|------------|-----------|
| **Testing** | Pytest | Pruebas unitarias |
| **Coverage** | pytest-cov | Cobertura de código |
| **Linting** | Flake8 | Calidad de código |
| **Formatting** | Black | Formateo automático |

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.9+
- Git
- Docker (opcional, para despliegue)
- Cuenta de GitHub (para CI/CD)

### 1. Clonar el Repositorio

git clone https://github.com/PonchitoSalcedo/GPIA_FASE_3.git
cd GPIA_FASE_3

### 2. Crear y Activar Entorno Virtual

# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

### 3. Instalar Dependencias

pip install -r requirements.txt

### 4. Descargar el Modelo

El modelo ya está incluido en el repositorio:

best_model.pkl - Modelo XGBoost optimizado
scaler.pkl - Escalador StandardScaler

### 5. Ejecutar Predicciones

# Desde la línea de comandos
python src/predict.py

# O usando la API
uvicorn src.api:app --reload

### 6. Probar la API

# Health check
curl http://localhost:8000/health

# Predicción
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"MedInc": 8.3252, "HouseAge": 41, "AveRooms": 6.9841, "AveBedrms": 1.0238, "Population": 322, "AveOccup": 2.5556, "Latitude": 37.88, "Longitude": -122.23}'

---

## 📓 Notebooks de Colab

El proyecto incluye 4 notebooks que cubren todo el pipeline de desarrollo:

### 1. 📊 `01_data_exploration.ipynb`

**Análisis Exploratorio de Datos (EDA)**

- Carga y exploración del dataset
- Visualización de distribuciones
- Matriz de correlación
- Detección de outliers
- Reporte de calidad de datos

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PonchitoSalcedo/GPIA_FASE_3/blob/main/notebooks/01_data_exploration.ipynb)

---

### 2. 🤖 `02_model_training.ipynb`

**Entrenamiento de Modelos**

- Entrenamiento de 7 modelos diferentes
- Comparación de desempeño
- Optimización de hiperparámetros
- Guardado del mejor modelo

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PonchitoSalcedo/GPIA_FASE_3/blob/main/notebooks/02_model_training.ipynb)

---

### 3. ✅ `03_model_evaluation.ipynb`

**Evaluación y Análisis**

- Métricas detalladas
- Visualización de predicciones vs reales
- Análisis de residuos
- Pruebas de robustez (bootstrap)
- Reporte de evaluación

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PonchitoSalcedo/GPIA_FASE_3/blob/main/notebooks/03_model_evaluation.ipynb)

---

### 4. 🔄 `04_pipeline_test.ipynb`

**Prueba del Pipeline**

- Verificación de integración
- Benchmark de rendimiento
- Generación de artefactos
- Reporte final

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PonchitoSalcedo/GPIA_FASE_3/blob/main/notebooks/04_pipeline_test.ipynb)

---

## 🐳 Despliegue con Docker

### Construir la Imagen

docker build -t california-housing-mlops .

## Ejecutar el Contenedor

docker run -p 8000:8000 california-housing-mlops

## Usar Docker Compose (Servicios Completos)

# Iniciar todos los servicios
docker-compose up -d

# Verificar estado
docker-compose ps

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

---

### Servicios Disponibles

| Servicio | Puerto | URL |
|----------|--------|-----|
| **API** | 8000 | [http://localhost:8000](http://localhost:8000) |
| **MLflow** | 5000 | [http://localhost:5000](http://localhost:5000) |
| **Jupyter** | 8888 | [http://localhost:8888](http://localhost:8888) |
| **Prometheus** | 9090 | [http://localhost:9090](http://localhost:9090) |
| **Grafana** | 3000 | [http://localhost:3000](http://localhost:3000) |

---

## 🤖 CI/CD con GitHub Actions

### Pipeline Automatizado

El pipeline se ejecuta automáticamente en cada **push** o **pull request**:

**Stages:**

1. **Testing:**
   - Linting (Flake8)
   - Formatting (Black)
   - Unit Tests (Pytest)
   - Coverage Report

2. **Training:**
   - Entrenamiento de modelos
   - Versionado con MLflow

3. **Evaluation:**
   - Validación de métricas
   - Umbrales de calidad

4. **Deployment:**
   - Docker Build
   - Push a Registro
   - Despliegue a Producción

5. **Monitoring:**
   - Alertas
   - Notificaciones

---


## 📈 Monitoreo y Métricas

### Métricas en Tiempo Real

| Métrica | Descripción | Umbral |
|---------|-------------|--------|
| **R² Score** | Precisión del modelo | > 0.75 |
| **RMSE** | Error cuadrático medio | < 0.80 |
| **Latencia** | Tiempo de respuesta | < 500ms |
| **Drift** | Cambio en distribución | < 0.10 |
| **Uptime** | Disponibilidad | > 99.9% |

---

## 📚 Documentación Técnica

La documentación completa del proyecto está disponible en los siguientes recursos:

### 📄 Documentos
- [**Documento Técnico de Operación**](./documentos/Documento_Tecnico_Operacion.pdf) - Guía técnica completa del sistema
- [**Portfolio Técnico-Estratégico**](./documentos/Portfolio_Tecnico_Estrategico.pdf) - Visión estratégica del proyecto
- [**Documentación Operativa**](./documentos/operational_documentation.md) - Manual de operaciones
- [**Portfolio Estratégico**](./documentos/strategic_portfolio.md) - Planificación estratégica

### 🎥 Videos Demostrativos
- [**Pipeline MLOps - Predicción de Vivienda (Parte 1)**](./videos/Pipeline_MLOps_Prediccion_Vivienda_1.mp4)
- [**Pipeline MLOps - Predicción de Vivienda (Parte 2)**](./videos/Pipeline_MLOps_Prediccion_Vivienda_2.mp4)

### ❓ Preguntas Frecuentes
- [Preguntas del Proyecto](./videos/Preguntas_Proyecto.md)

> **Nota:** Los enlaces con `#` serán actualizados cuando los archivos estén disponibles.

### Guías Rápidas

| Guía | Descripción |
|------|-------------|
| Instalación | Configuración local |
| Docker | Despliegue con contenedores |
| API | Documentación de la API |
| Colab | Notebooks interactivos |

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. **Fork** el repositorio
2. Crear una **rama feature** (`git checkout -b feature/nueva-caracteristica`)
3. **Commit** de cambios (`git commit -m 'Agregar nueva característica'`)
4. **Push** a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear un **Pull Request**

### Estándares de Código

- ✅ Código formateado con **Black**
- ✅ Código verificado con **Flake8**
- ✅ Pruebas con **Pytest** (cobertura > 80%)
- ✅ Documentación actualizada

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Contacto

- **Autor:** Luis Alfonso Salcedo
- **GitHub:** [PonchitoSalcedo](https://github.com/PonchitoSalcedo)
- **LinkedIn:** [Ponchito Salcedo](https://linkedin.com/in/ponchito-salcedo)

---

## 🙏 Agradecimientos

- **Scikit-learn** por el dataset California Housing
- **MLflow** por el versionado de modelos
- **GitHub** por las Actions y el hosting
- **Comunidad Open Source** por las herramientas utilizadas

---

## 🏢 Última Actualización

- 📅 **Fecha:** Julio 2026
- 📌 **Versión:** 1.0.0
- ✅ **Estado:** Producción
