# Bitácora de trabajo — Pipeline de Churn con MLOps/GitOps

Registro cronológico del desarrollo, pensado como evidencia del proceso de
toma de decisiones (no solo del resultado final). Cada entrada corresponde
a uno o más commits del historial de Git (`git log --oneline --reverse`).

---

**10 jul — Estructura inicial**
Definí la estructura de carpetas separando claramente `data/`, `src/`,
`tests/`, `manifests/` y el workflow de CI/CD, para que cada responsabilidad
del ciclo de vida tuviera un lugar único y obvio.

**11 jul — Generación de datos**
Decisión: en vez de usar un CSV estático sin origen, escribí
`generate_data.py` como script reproducible. Así la generación de datos
también queda versionada y auditable, y cualquiera puede regenerar el
mismo dataset (semilla fija = 42).

**12 jul — Preprocesamiento centralizado**
Aquí tomé la decisión más importante para evitar bugs sutiles después:
`features.py` como único punto de preprocesamiento, importado tanto por
entrenamiento como por el servicio de inferencia. La alternativa —duplicar
la lógica de encoding en ambos lugares— es la causa más común de
"funciona en entrenamiento, falla en producción" (training-serving skew).

**14 jul — Entrenamiento y quality gate**
Implementé `train.py` con GridSearchCV sobre RandomForest. Definí un
umbral mínimo de ROC-AUC = 0.70 dentro del propio script: si no se cumple,
se lanza `SystemExit` y el pipeline de CI falla ahí mismo. Iteré sobre el
espacio de búsqueda de hiperparámetros dos veces: la primera solo variaba
`n_estimators`, y no mejoraba el AUC lo suficiente; agregar `max_depth` y
`min_samples_leaf` a la búsqueda subió el ROC-AUC de ~0.71 a 0.776 en el
conjunto de prueba.

**15 jul — Pruebas automatizadas**
Escribí primero las pruebas de datos (`test_data.py`) y luego las del
modelo (`test_model.py`). Decidí incluir una prueba específica para
categorías no vistas en entrenamiento (ej. un método de pago nuevo)
después de notar que, sin `handle_unknown="ignore"` en el
`OneHotEncoder`, el pipeline fallaba con un error en tiempo de inferencia
—exactamente el tipo de bug que solo aparece en producción si no se
prueba explícitamente.

**17 jul — Contenerización y serving**
Escribí el `Dockerfile` y `serve.py` (FastAPI). Decisión: además de
`/predict`, agregué `/health` desde el inicio para que el `HEALTHCHECK`
de Docker y el `readinessProbe`/`livenessProbe` de Kubernetes tuvieran
algo real que consultar.

**18 jul — Monitoreo**
Implementé `monitor.py` con la prueba de Kolmogorov-Smirnov para drift.
Consideré comparar solo promedios (más simple), pero lo descarté: un
cambio en la dispersión de los datos sin cambio en la media es un tipo de
drift real y común que un chequeo de promedio no detectaría.

**20 jul — CI/CD**
Construí el workflow de GitHub Actions completo: lint → pruebas de datos
→ pruebas de modelo + entrenamiento → build y push de imagen Docker →
actualización del manifiesto de despliegue. Encadené los jobs con `needs`
para que cada etapa dependa del éxito de la anterior.

**21 jul — GitOps y DVC**
Agregué los manifiestos de Kubernetes y la definición de `Application` de
ArgoCD con `syncPolicy.automated.selfHeal: true`. También escribí
`dvc.yaml` para declarar el pipeline de datos→modelo como un DAG
reproducible.

**23-24 jul — Evidencia de ejecución real**
Entrené el modelo end-to-end (ROC-AUC 0.776, accuracy 73.9%). Simulé 300
solicitudes de producción contra el modelo entrenado para generar
`audit_log.jsonl` real, y corrí `monitor.py` contra ese log: no se detectó
drift, latencia promedio de 11.99 ms. Esta evidencia queda en
`artifacts/metrics.json` y `docs/monitoring_report.json`.

**25 jul — Documentación**
Redacté el `README.md` documentando arquitectura, decisiones técnicas y
su justificación, y cómo correr todo el pipeline localmente.

**26 jul — Cierre de versionado**
Ajusté `.gitignore` para que el binario del modelo (`model.joblib`) no se
versione directamente en Git —eso es responsabilidad de DVC— manteniendo
el repositorio de código liviano.

---

## Reflexión sobre el proceso

La parte que más iteración tomó no fue el modelo en sí (llegar a un
ROC-AUC aceptable fue relativamente directo), sino diseñar los puntos de
control automáticos: decidir *dónde* exactamente debía vivir cada
quality gate para que fallara temprano y de forma explícita, en vez de
silenciosamente más adelante en el pipeline.
