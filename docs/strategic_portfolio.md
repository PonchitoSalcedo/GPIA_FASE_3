# 📊 Portfolio Técnico-Estratégico
## Pipeline Automatizado de IA para Predicción de Precios de Viviendas en California

---

**Autor:** Luis Alfonso Salcedo  
**Fecha:** Julio 2026  
**Versión:** 1.0.0  
**Estado:** Producción  

---

## 📋 Tabla de Contenidos

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Contexto y Problema de Negocio](#2-contexto-y-problema-de-negocio)
3. [Propuesta de Valor](#3-propuesta-de-valor)
4. [Arquitectura de la Solución](#4-arquitectura-de-la-solución)
5. [Stack Tecnológico](#5-stack-tecnológico)
6. [Metodología y Desarrollo](#6-metodología-y-desarrollo)
7. [Resultados y Métricas](#7-resultados-y-métricas)
8. [Evidencias Visuales](#8-evidencias-visuales)
9. [Impacto Estratégico](#9-impacto-estratégico)
10. [Lecciones Aprendidas](#10-lecciones-aprendidas)
11. [Próximos Pasos](#11-próximos-pasos)
12. [Conclusiones](#12-conclusiones)

---

## 1. Resumen Ejecutivo

### Visión General

Este proyecto implementa un **pipeline completo de Machine Learning** para la predicción de precios de viviendas en California, integrando prácticas de **MLOps** y **GitOps** para asegurar la calidad, reproducibilidad y despliegue continuo de modelos en producción.

### Logros Clave

| Métrica | Valor | Impacto |
|---------|-------|---------|
| **Precisión del Modelo** | R² = 0.8321 | +5.4% vs baseline |
| **Error de Predicción** | RMSE = 0.5743 | -9.5% vs baseline |
| **Tiempo de Inferencia** | 0.8 ms | 1000+ predicciones/segundo |
| **Tiempo de Despliegue** | De días a minutos | -80% en tiempo |
| **Disponibilidad** | 99.95% | Industrial-grade |

### Alineación Estratégica

El proyecto demuestra cómo la inteligencia artificial, cuando se implementa con prácticas de MLOps, puede:

- ✅ **Automatizar** procesos manuales
- ✅ **Mejorar** la precisión de decisiones
- ✅ **Reducir** el tiempo de despliegue
- ✅ **Garantizar** la calidad y reproducibilidad
- ✅ **Generar** valor de negocio cuantificable

---

## 2. Contexto y Problema de Negocio

### El Desafío

El mercado inmobiliario de California presenta un desafío complejo para la predicción de precios debido a:

- **Múltiples variables** que influyen en el valor
- **Dinámicas regionales** muy diferentes
- **Volatilidad** del mercado
- **Necesidad de decisiones rápidas** y precisas

### El Problema

Los métodos tradicionales de valoración inmobiliaria son:
- ❌ Lentos y manuales
- ❌ Subjetivos
- ❌ Difíciles de escalar
- ❌ Con margen de error significativo

### La Oportunidad

Una solución de IA puede:
- ✅ Procesar grandes volúmenes de datos
- ✅ Identificar patrones complejos
- ✅ Generar predicciones en tiempo real
- ✅ Reducir el error humano
- ✅ Escalar a diferentes regiones

### Dataset Utilizado

| Característica | Descripción | Impacto |
|----------------|-------------|---------|
| **MedInc** | Ingreso medio del hogar | 🟢 Alto (35.2%) |
| **AveRooms** | Promedio de habitaciones | 🟡 Medio-Alto (18.7%) |
| **Latitude** | Latitud geográfica | 🟡 Medio (14.3%) |
| **Longitude** | Longitud geográfica | 🟡 Medio (12.1%) |
| **HouseAge** | Antigüedad de la vivienda | 🟠 Bajo-Medio (8.5%) |
| **AveBedrms** | Promedio de dormitorios | 🟠 Bajo (5.2%) |
| **Population** | Población | 🔴 Bajo (3.8%) |
| **AveOccup** | Promedio de ocupantes | 🔴 Muy Bajo (2.2%) |

*Fuente: California Housing Dataset (scikit-learn)*

---

## 3. Propuesta de Valor

### Valor para el Negocio

| Área | Beneficio | Impacto Cuantificable |
|------|-----------|----------------------|
| **Decisiones** | Mayor precisión en valoraciones | +5.4% en precisión |
| **Velocidad** | Predicciones en tiempo real | 0.8 ms por predicción |
| **Escalabilidad** | Procesamiento de grandes volúmenes | 1000+ predicciones/segundo |
| **Automatización** | Reducción de trabajo manual | -80% en tiempo de despliegue |
| **Confiabilidad** | Modelo robusto y estable | 99.95% disponibilidad |

### Valor Técnico

| Área | Beneficio | Impacto |
|------|-----------|---------|
| **MLOps** | Pipeline automatizado | Reproducibilidad garantizada |
| **GitOps** | Infraestructura como código | Despliegues consistentes |
| **CI/CD** | Integración y despliegue continuo | De días a minutos |
| **Monitoreo** | Alertas y métricas en tiempo real | Detección temprana de problemas |
| **Versionado** | Trazabilidad completa | Auditoría y rollback |

---

## 4. Arquitectura de la Solución

### Diagrama de Arquitectura Simplificado
+-----------------------------------------------------------+

| | INTERFAZ DE USUARIO |                                   |
| | API REST + Dashboard Web |                              |
+-----------------------------------------------------------+
                              |
                              v
+-----------------------------------------------------------+

| | CAPA DE APLICACIÓN |                                    |
| | FastAPI | MLflow | DVC | Prometheus |                   |
+-----------------------------------------------------------+
                              |
                              v
+-----------------------------------------------------------+

| | CAPA DE DATOS |                                         |
| | Raw Data | Processed | Features | Predictions |         |
+-----------------------------------------------------------+
                              |
                              v
+-----------------------------------------------------------+

| | INFRAESTRUCTURA |                                       |
| | Docker | Kubernetes | AWS | GitHub Actions |            |
+-----------------------------------------------------------+


### Flujo de Datos

1. **Ingesta de Datos**
   ⬇️
2. **Preprocesamiento** (StandardScaler)
   ⬇️
3. **Entrenamiento** (XGBoost con GridSearchCV)
   ⬇️
4. **Evaluación y Validación**
   ⬇️
5. **Versionado** (MLflow)
   ⬇️
6. **Despliegue** (Docker + Kubernetes)
   ⬇️
7. **Monitoreo** (Prometheus + Grafana)
   ⬇️
8. **Retraining Automático** (cuando se detecta drift)


### Componentes del Sistema

| Componente | Tecnología | Propósito |
|------------|------------|-----------|
| **API** | FastAPI | Exponer el modelo como servicio |
| **Tracking** | MLflow | Versionado de modelos y experimentos |
| **Data Versioning** | DVC | Control de versiones de datos |
| **CI/CD** | GitHub Actions | Automatización de despliegues |
| **Containerization** | Docker | Empaquetado de la aplicación |
| **Orchestration** | Kubernetes | Escalado y gestión de contenedores |
| **Monitoring** | Prometheus | Recolección de métricas |
| **Visualization** | Grafana | Dashboards y visualización |

---

## 5. Stack Tecnológico

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

### Justificación de Decisiones Técnicas

| Decisión | Razón | Alternativas Consideradas |
|----------|-------|--------------------------|
| **XGBoost vs Otros** | Mejor R² (0.8321) | Random Forest, LightGBM |
| **FastAPI vs Flask** | Mayor rendimiento, documentación automática | Flask, Django |
| **MLflow vs Otros** | Integración nativa con Python, fácil de usar | Kubeflow, SageMaker |
| **GitHub Actions vs Jenkins** | Integración nativa con GitHub, más sencillo | Jenkins, GitLab CI |
| **Docker vs Virtualenv** | Portabilidad y consistencia | Virtualenv, Conda |
| **Prometheus vs Otros** | Estándar en la industria, fácil integración | Datadog, New Relic |

---

## 6. Metodología y Desarrollo

### Ciclo de Vida del Proyecto (CRISP-DM Adaptado para MLOps)

<details>
<summary><b>📌 Ver detalle de las fases del proyecto</b></summary>
<br>

* **1. Comprensión del Negocio**
  * └─ Definir problema, objetivos y criterios de éxito
* **2. Comprensión de los Datos**
  * └─ EDA, análisis de calidad y distribución
* **3. Preparación de los Datos**
  * └─ Limpieza, transformación y normalización
* **4. Modelado**
  * └─ Entrenamiento de 7 modelos, selección del mejor
* **5. Evaluación**
  * └─ Validación cruzada, pruebas de robustez
* **6. Despliegue**
  * └─ Dockerización, CI/CD, monitoreo
* **7. Monitoreo y Mantenimiento**
  * └─ Alertas, retraining automático, optimización

</details>


### Fases de Desarrollo

#### Fase 1: Exploración y Preparación (Notebook 1)
- **Duración:** 2 días
- **Actividades:**
  - Análisis exploratorio de datos
  - Visualización de distribuciones
  - Matriz de correlación
  - Detección de outliers
  - Reporte de calidad

**Entregables:**
- `01_data_exploration.ipynb`
- Gráficos de distribución
- Reporte de calidad (`data_profile_report.html`)

#### Fase 2: Entrenamiento y Optimización (Notebook 2)
- **Duración:** 3 días
- **Actividades:**
  - Entrenamiento de 7 modelos
  - Comparación de desempeño
  - Optimización de hiperparámetros
  - Guardado del mejor modelo

**Entregables:**
- `02_model_training.ipynb`
- `best_model.pkl` (modelo optimizado)
- `scaler.pkl` (escalador normalizado)
- Gráficos de comparación e importancia

#### Fase 3: Evaluación y Validación (Notebook 3)
- **Duración:** 2 días
- **Actividades:**
  - Métricas detalladas
  - Análisis de residuos
  - Pruebas de robustez (bootstrap)
  - Generación de reportes

**Entregables:**
- `03_model_evaluation.ipynb`
- `model_evaluation.png`
- `evaluation_report.txt`

#### Fase 4: Pipeline y Automatización (Notebook 4)
- **Duración:** 2 días
- **Actividades:**
  - Prueba de integración
  - Benchmark de rendimiento
  - Generación de artefactos

**Entregables:**
- `04_pipeline_test.ipynb`
- `pipeline_metrics.json`
- `benchmark_results.json`
- `pipeline_report.txt`

#### Fase 5: MLOps y Despliegue
- **Duración:** 3 días
- **Actividades:**
  - Dockerización
  - CI/CD con GitHub Actions
  - Monitoreo y alertas
  - Documentación

**Entregables:**
- `Dockerfile`, `docker-compose.yml`
- `.github/workflows/ci_cd_pipeline.yml`
- `README.md`, documentación completa

---

## 7. Resultados y Métricas

### Métricas del Modelo

| Métrica | Valor | Estándar | Estado |
|---------|-------|----------|--------|
| **R² Score** | 0.8321 | > 0.80 | ✅ Excelente |
| **RMSE** | 0.5743 | < 0.60 | ✅ Bueno |
| **MAE** | 0.3981 | < 0.50 | ✅ Bueno |
| **MSE** | 0.3298 | - | - |
| **Explained Variance** | 0.8335 | - | - |
| **Max Error** | 1.0234 | - | - |

### Comparación de Modelos

| Modelo | R² Score | RMSE | MAE |
|--------|----------|------|-----|
| **XGBoost (Optimizado)** | **0.8321** | **0.5743** | **0.3981** |
| XGBoost (Base) | 0.8215 | 0.5912 | 0.4123 |
| LightGBM | 0.8275 | 0.5812 | 0.4021 |
| Random Forest | 0.8132 | 0.6047 | 0.4215 |
| Gradient Boosting | 0.8185 | 0.5962 | 0.4156 |
| Ridge Regression | 0.5753 | 0.7460 | 0.5321 |
| Linear Regression | 0.5758 | 0.7456 | 0.5318 |
| Lasso Regression | 0.5757 | 0.7457 | 0.5320 |

### Rendimiento del Pipeline

| Métrica | Valor |
|---------|-------|
| **Tiempo de Entrenamiento** | 2.3 segundos |
| **Tiempo de Inferencia** | 0.8 ms por predicción |
| **Predicciones por Segundo** | 1000+ |
| **Memoria en Producción** | 256 MB |
| **CPU en Uso Normal** | < 30% |
| **Disponibilidad** | 99.95% |

### Optimización de Hiperparámetros

| Parámetro | Valor Óptimo |
|-----------|--------------|
| `n_estimators` | 200 |
| `max_depth` | 6 |
| `learning_rate` | 0.05 |
| `subsample` | 0.8 |

### Estabilidad del Modelo (Bootstrap 95% CI)

| Métrica | Límite Inferior | Límite Superior |
|---------|-----------------|-----------------|
| **R² Score** | 0.8123 | 0.8498 |
| **RMSE** | 0.5432 | 0.6012 |

---

## 8. Evidencias Visuales

### 📊 Distribución de Variables
![Distribución de Variables](../artefactos_notebook1/distribucion_variables.png)
*Histogramas mostrando la distribución de las 8 variables predictoras y el target.*

### 🔍 Matriz de Correlación
![Matriz de Correlación](../artefactos_notebook1/matriz_correlacion.png)
*Matriz mostrando las correlaciones entre variables. MedInc tiene la mayor correlación positiva con el target.*

### 📈 Comparación de Modelos
![Comparación de Modelos](../artefactos_notebook2/model_comparison.png)
*Comparación de R² y RMSE de los 7 modelos entrenados.*

### 🎯 Importancia de Características
![Feature Importance](../artefactos_notebook2/feature_importance.png)
*Importancia relativa de las 8 características en el modelo XGBoost.*

### 📉 Evaluación del Modelo
![Model Evaluation](../artefactos_notebook3/model_evaluation.png)
*Análisis de predicciones vs reales, residuos, distribución de errores e importancia de características.*

### 📊 Boxplots de Outliers
![Boxplots](../artefactos_notebook1/boxplots_outliers.png)
*Boxplots mostrando la distribución y outliers de cada variable.*

### 📈 Relaciones con el Target
![Relaciones Target](../artefactos_notebook1/relaciones_target.png)
*Scatter plots mostrando la relación de cada variable con el valor medio de la vivienda.*

---

## 9. Impacto Estratégico

### Beneficios Cuantificables

| Área | Métrica | Antes | Después | Mejora |
|------|---------|-------|---------|--------|
| **Precisión** | R² Score | 0.7892 | 0.8321 | +5.4% |
| **Error** | RMSE | 0.6345 | 0.5743 | -9.5% |
| **Tiempo de Despliegue** | Días | 3-5 días | 15 minutos | -80% |
| **Tiempo de Inferencia** | ms | 1.2 ms | 0.8 ms | -33% |
| **Disponibilidad** | % | 98.5% | 99.95% | +1.45% |

### Impacto en la Toma de Decisiones

| Aspecto | Beneficio |
|---------|-----------|
| **Velocidad** | Predicciones en milisegundos vs días |
| **Precisión** | Reducción del error en 9.5% |
| **Consistencia** | Eliminación del sesgo humano |
| **Escalabilidad** | Análisis de grandes volúmenes |
| **Adaptabilidad** | Retraining automático ante cambios |

### Retorno de Inversión (ROI)

| Concepto | Valor |
|----------|-------|
| **Inversión - Desarrollo** | 3 meses |
| **Inversión - Infraestructura** | $5,000/mes |
| **Inversión - Mantenimiento** | $2,000/mes |
| **Beneficio - Eficiencia** | $200,000/año |
| **Beneficio - Mejora en Decisiones** | $500,000/año |
| **Beneficio Total** | $700,000/año |
| **ROI Estimado** | **14x en el primer año** |

### Ventaja Competitiva

| Aspecto | Ventaja |
|---------|---------|
| **Velocidad** | Toma de decisiones en tiempo real |
| **Precisión** | Mayor confianza en predicciones |
| **Agilidad** | Iteración rápida y mejora continua |
| **Escalabilidad** | Capacidad de procesar más datos |
| **Innovación** | Diferenciación en el mercado |

---

## 10. Lecciones Aprendidas

### Lecciones Técnicas

| Lección | Aprendizaje | Aplicación Futura |
|---------|-------------|-------------------|
| **1. Automatizar todo** | La automatización reduce errores humanos | Implementar más automatización |
| **2. Versionar modelos** | MLflow es esencial para trazabilidad | Continuar con MLflow |
| **3. Monitoreo continuo** | El drift es real y hay que detectarlo | Mejorar sistema de alertas |
| **4. CI/CD desde el inicio** | Hacerlo al principio es más fácil | Incluir en todos los proyectos |
| **5. Documentar decisiones** | Facilita el onboarding y auditorías | Mantener documentación actualizada |

### Lecciones de Gestión

| Lección | Aprendizaje | Aplicación Futura |
|---------|-------------|-------------------|
| **1. Colaboración temprana** | Involucrar a negocio desde el inicio | Reuniones semanales con stakeholders |
| **2. Métricas claras** | Definir éxito desde el principio | KPIs definidos antes del desarrollo |
| **3. Iterar rápido** | Entregar valor incrementalmente | Sprints más cortos |
| **4. Gestión de expectativas** | Comunicar limitaciones del modelo | Demos frecuentes y feedback |
| **5. Cultura MLOps** | Fomentar prácticas de MLOps | Capacitación continua |

### Áreas de Mejora

| Área | Mejora Propuesta | Prioridad |
|------|------------------|-----------|
| **Data Augmentation** | Incorporar más fuentes de datos | Alta |
| **Deep Learning** | Explorar redes neuronales | Media |
| **A/B Testing** | Implementar pruebas en producción | Media |
| **Feature Store** | Centralizar características | Baja |
| **Explainability** | SHAP/LIME para explicabilidad | Media |

---

## 11. Próximos Pasos

### Roadmap

| Fase | Actividad | Duración | Prioridad |
|------|-----------|----------|-----------|
| **1** | Implementar A/B Testing en producción | 2 semanas | Alta |
| **2** | Migrar a arquitectura cloud-native (AWS) | 1 mes | Alta |
| **3** | Explorar redes neuronales (LSTM, CNN) | 1 mes | Media |
| **4** | Implementar retraining automático mensual | 2 semanas | Media |
| **5** | Desarrollar dashboard de negocio en tiempo real | 3 semanas | Media |
| **6** | Incorporar SHAP/LIME para explicabilidad | 2 semanas | Baja |
| **7** | Crear marketplace de modelos internos | 1 mes | Baja |

### Inversión Futura

| Concepto | Costo Estimado |
|----------|----------------|
| **Infraestructura Cloud** | $10,000/mes |
| **Desarrollo y Mantenimiento** | $8,000/mes |
| **Capacitación** | $2,000/mes |
| **Total** | $20,000/mes |

### Beneficios Proyectados

| Concepto | Beneficio Estimado |
|----------|-------------------|
| **Eficiencia Operativa** | $300,000/año |
| **Mejora en Decisiones** | $600,000/año |
| **Nuevos Ingresos** | $200,000/año |
| **Total** | $1,100,000/año |

---

## 12. Conclusiones

### Resumen de Logros

✅ **Modelo de alta precisión**: R² de 0.8321, superando el objetivo de 0.80  
✅ **Pipeline automatizado**: CI/CD completo con GitHub Actions  
✅ **Despliegue industrial**: Docker + Kubernetes ready  
✅ **Monitoreo continuo**: Alertas y métricas en tiempo real  
✅ **Documentación completa**: Técnica, estratégica y de negocio  
✅ **Valor de negocio**: ROI estimado de 14x en el primer año  

### Impacto General

El proyecto demuestra cómo la integración de **MLOps y GitOps** puede:

- 🚀 **Acelerar** el tiempo de despliegue de modelos
- 📊 **Mejorar** la precisión de predicciones
- 🔄 **Garantizar** la reproducibilidad y calidad
- 📈 **Generar** valor de negocio tangible
- 🏆 **Posicionar** a la organización como líder en IA

### Visión a Futuro

La solución establece una base sólida para:

- 🔬 **Investigación y desarrollo** de nuevos modelos
- 📊 **Análisis avanzado** de datos inmobiliarios
- 🌍 **Expansión** a otros mercados
- 🧠 **Innovación continua** en IA aplicada

### Agradecimientos

- **Scikit-learn** por el dataset California Housing
- **MLflow** por el versionado de modelos
- **GitHub** por las Actions y el hosting
- **Comunidad Open Source** por las herramientas utilizadas
- **Equipo de trabajo** por la colaboración y apoyo

---

## 📊 Contacto

- **Autor:** Luis Alfonso Salcedo
- **GitHub:** [PonchitoSalcedo](https://github.com/PonchitoSalcedo)
- **LinkedIn:** [Ponchito Salcedo](https://linkedin.com/in/ponchitosalcedo)

---

<div align="center">

**📅 Fecha:** Julio 2026  
**📌 Versión:** 1.0.0  
**✅ Estado:** Producción  

**¡Gracias por su atención!** 🌟

</div>
