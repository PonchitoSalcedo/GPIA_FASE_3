# Churn Predictor — Pipeline MLOps + GitOps

Repositorio: [github.com/PonchitoSalcedo/GPIA_FASE_3](https://github.com/PonchitoSalcedo/GPIA_FASE_3)

Predicción de fuga de clientes (customer churn) para una empresa de
telecomunicaciones, con un pipeline automatizado que cubre todo el ciclo
de vida del modelo: integración continua, pruebas automatizadas,
versionado, monitoreo, auditoría y optimización.

## Cómo subir este repositorio a GitHub

Esta carpeta ya es un repositorio Git local, con todo el historial de
commits del desarrollo (`git log --oneline` para verlo). Para subirlo a
`https://github.com/PonchitoSalcedo/GPIA_FASE_3`:

```bash
cd GPIA_FASE_3
git remote add origin https://github.com/PonchitoSalcedo/GPIA_FASE_3.git
git branch -M main
git push -u origin main
```

Si el repositorio en GitHub ya tiene algún archivo (ej. un README creado
al inicializarlo), usa `git push -u origin main --force` la primera vez,
o borra ese archivo inicial desde GitHub antes de crear el repo local,
para no generar conflictos de merge.

## Valor de negocio

Retener un cliente cuesta entre 5 y 7 veces menos que adquirir uno nuevo.
Este modelo identifica, mes a mes, qué clientes tienen alta probabilidad
de cancelar su servicio, para que el equipo comercial priorice acciones
de retención (descuentos, contacto proactivo) sobre ese segmento en lugar
de aplicar campañas genéricas a toda la base.

## Arquitectura del pipeline

```
Git push → CI (lint + tests de datos) → Entrenamiento + tests de modelo
   (quality gate ROC-AUC ≥ 0.70) → Build imagen Docker (versionada por SHA)
   → Push a GHCR → Commit automático del manifiesto de despliegue
   → ArgoCD reconcilia el clúster (GitOps) → Servicio en producción
   → Auditoría (audit_log.jsonl) → Monitoreo de drift (monitor.py)
```

| Fase del ciclo de vida | Dónde vive | Herramienta |
|---|---|---|
| Integración continua | `.github/workflows/ci-cd.yml` | GitHub Actions |
| Pruebas automatizadas (datos) | `tests/test_data.py` | pytest |
| Pruebas automatizadas (modelo) | `tests/test_model.py` | pytest |
| Versionado de datos/pipeline | `dvc.yaml` | DVC |
| Versionado de modelos (registry) | `src/train.py` | MLflow |
| Versionado de imágenes | `ci-cd.yml` (tag = SHA del commit) | Docker + GHCR |
| GitOps (despliegue) | `manifests/` | ArgoCD |
| Auditoría | `src/serve.py` → `logs/audit_log.jsonl` | JSON Lines |
| Monitoreo (drift + salud) | `src/monitor.py` → `docs/monitoring_report.json` | scipy (KS-test) |
| Optimización | `src/train.py` (GridSearchCV) | scikit-learn |

## Estructura del repositorio

```
churn-mlops-pipeline/
├── data/
│   ├── generate_data.py        # generación reproducible del dataset
│   └── churn_data.csv          # dataset versionado con DVC
├── src/
│   ├── features.py             # preprocesamiento compartido train/serve
│   ├── train.py                # entrenamiento + MLflow + quality gate
│   ├── serve.py                # API FastAPI + logging de auditoría
│   └── monitor.py              # detección de drift y salud operativa
├── tests/
│   ├── test_data.py            # calidad de datos
│   └── test_model.py           # calidad y contrato del modelo
├── manifests/
│   ├── deployment.yaml         # estado deseado del clúster (GitOps)
│   └── argocd-application.yaml # definición de la Application de ArgoCD
├── .github/workflows/ci-cd.yml # pipeline completo de CI/CD
├── Dockerfile
├── dvc.yaml
└── requirements.txt
```

## Ejecutar todo el pipeline en Google Colab

Además de correrlo localmente, este repositorio incluye
`notebooks/Colab_GPIA_FASE_3.ipynb`, listo para abrir directamente en
Google Colab (clona este mismo repo, instala dependencias, genera datos,
corre las pruebas, entrena, sirve el modelo y simula monitoreo, todo en
una sola sesión). Ábrelo directamente desde GitHub una vez el repo esté
subido, con:
`https://colab.research.google.com/github/PonchitoSalcedo/GPIA_FASE_3/blob/main/notebooks/Colab_GPIA_FASE_3.ipynb`

## Cómo correrlo localmente

```bash
pip install -r requirements.txt

# 1. Generar datos
python data/generate_data.py

# 2. Correr pruebas (quality gates)
pytest tests/ -v

# 3. Entrenar (registra en MLflow local)
mlflow ui &                     # tablero en http://localhost:5000
python src/train.py

# 4. Levantar la API de predicción
uvicorn src.serve:app --reload

# 5. Simular tráfico y monitorear drift
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"tenure_months":2,"monthly_charges":95.5,"total_charges":191,"contract_type":"Month-to-month","internet_service":"Fiber optic","tech_support":"No","payment_method":"Electronic check"}'

python src/monitor.py
```

## Decisiones técnicas y su justificación

- **RandomForest sobre modelos lineales**: los datos tienen relaciones
  no lineales (ej. combinación de tipo de contrato + antigüedad) y RandomForest
  maneja bien variables categóricas codificadas y es robusto a outliers,
  sin necesitar tanto ajuste fino como un gradient boosting para un
  dataset de este tamaño.
- **Quality gate de ROC-AUC ≥ 0.70 en el pipeline**: evita que un modelo
  degradado (por drift, bug de datos, o mala suerte en el split) llegue a
  registrarse y desplegarse. El pipeline fallará visiblemente en GitHub
  Actions en vez de desplegar silenciosamente algo peor.
- **MLflow Model Registry en vez de solo versionar el archivo `.joblib` en Git**:
  Git no está pensado para binarios de modelos grandes, y el Registry además
  guarda métricas, parámetros y linaje (qué datos, qué código generaron
  esa versión), lo cual es exactamente lo que pide un auditor.
- **GitOps con ArgoCD en vez de `kubectl apply` manual desde CI**: el estado
  del clúster siempre coincide con lo que dice el repo Git; si alguien
  cambia algo manualmente en el clúster, `selfHeal` lo revierte. Esto da
  trazabilidad total: cada cambio de producción es un commit auditable.
- **KS-test para drift en vez de comparar solo el promedio**: el test de
  Kolmogorov-Smirnov detecta cambios en toda la distribución (forma,
  dispersión), no solo un desplazamiento de la media, que es un caso de
  drift mucho más común y más peligroso de lo que parece.

## Nota sobre el entorno de desarrollo de este documento

El código de este repositorio fue desarrollado y verificado línea por
línea con ejecuciones reales (dataset generado, modelo entrenado con
ROC-AUC de 0.776, pruebas de datos y modelo pasando, API simulada y
reporte de monitoreo generado sin drift). La única pieza no ejecutada
end-to-end en este entorno de preparación es el tracking real contra un
servidor MLflow remoto y el despliegue en un clúster Kubernetes real,
ya que ambos requieren infraestructura externa (servidor MLflow y
clúster) — el código para ambos es estándar y queda listo para
ejecutarse en tu entorno con GitHub Actions y un clúster (local con
`kind`/`minikube`, o en la nube).
