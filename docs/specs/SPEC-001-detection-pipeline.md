# SPEC-001 — Detection & Compliance Pipeline (Fase 1)

Status: draft · partially implemented (4/6 acceptance criteria)
Created: 2026-06-21 · Owner: TBD · Phase: 1

---

## Context & Problem

Fase 1 entrega el **pipeline de software** que, dado un modelo YOLO y una imagen
o video, detecta personas / PPE / vehículos / entorno (esquema unificado de 32
clases) y clasifica a cada trabajador como SAFE / UNSAFE / UNKNOWN.

Alcance = **el software del pipeline**, no la calidad del modelo. El
entrenamiento, el fine-tuning y el objetivo de mAP son un hito separado
(SPEC-003 — Model Training & Validation). "Pipeline implementado" no equivale a
"modelo bueno": son dos cosas que se cierran por separado.

## Goals

- Detección sobre imagen y video con un modelo YOLOv8 (`src/ppe_detection/inference.py`).
- Clasificación de compliance por trabajador con resolución híbrida —señal
  embebida en la clase + señal espacial por IoU/center-containment—
  (`src/ppe_detection/ppe_classifier.py`).
- Notebooks 01–06 reproducibles, generados desde `scripts/generate_notebooks.py`.
- Esquema unificado de 32 clases y utilidades de dataset/visualización.

## Non-Goals

- Entrenar/validar el modelo o alcanzar un mAP objetivo → **SPEC-003**.
- Calidad de detección del modelo (depende de datos/entrenamiento).
- Limpieza/adquisición de datasets → SPEC-002 (registro) / SPEC-004.
- Módulos 2–6 (vehículos como capacidad propia, tracking, proximidad, DB/API, dashboard).

## Requirements (acceptance criteria)

| # | Criterio | Estado |
|---|----------|--------|
| AC-1 | `load_model` + `predict_image` devuelven `Detection` estructuradas (id, name, conf, bbox) | ✅ implementado |
| AC-2 | `classify_workers` asigna SAFE/UNSAFE/UNKNOWN con required = {hardhat, vest} | ✅ implementado |
| AC-3 | Inferencia de imagen y video guardan overlay en `outputs/` | ✅ implementado |
| AC-4 | Esquema de 32 clases y paths centralizados en `utils.py` | ✅ implementado |
| AC-5 | **Smoke test**: el pipeline corre end-to-end con `yolov8n.pt` genérico (COCO, sin fine-tuning) sobre ≥1 imagen y produce overlay + compliance **sin crashear** | 🔴 falla (nunca ejecutado; depende de SPEC-002 AC-1/AC-2) |
| AC-6 | Los notebooks generados importan solo API vigente de `src/` (sin `has_hardhat`/`has_vest`) | 🔴 roto (`generate_notebooks.py:1198`) |

La fase se considera **implementada** cuando AC-1…AC-6 pasan. Hoy: **4/6**.

> El **smoke test (AC-5)** es deliberadamente independiente del modelo: usa el
> `yolov8n.pt` pre-entrenado de COCO. Valida que el *pipeline* produce una salida
> sin crashear, sin exigir calidad de detección (eso es SPEC-003). De paso, hace
> saltar el bug del generador (AC-6).

## Design notes

- **Esquema unificado (32 clases):** fusiona PPE (con/sin casco, chaleco, guantes,
  lentes, respirador, reflectiva), vehículos mineros (volquete, excavadora,
  cargador frontal, …) y entorno (polvo, animal). Convive con dos codificaciones
  de compliance: embebida en la clase de persona (`person_sin_casco`) y objetos
  PPE separados (`hardhat`/`safety_vest`/`mask`) resueltos por overlap. Detalle
  completo en `src/ppe_detection/README.md`.
- **Resolución de compliance:** la señal embebida tiene prioridad; la espacial
  (IoU ≥ 0.05 o centro del item contenido en la persona) solo rellena atributos
  aún desconocidos. Required = {hardhat, vest}; el resto se reporta sin volcar a UNSAFE.
- **Flujo de notebooks:** `generate_notebooks.py` → 6 `.ipynb`. Ver constitution.

## Open questions

- La propuesta comercial describe 5 clases PPE y módulos 1/2 separados; la
  implementación tiene 32 clases unificadas (1+2 fusionados). ¿Se actualiza la
  propuesta a la realidad o conviven como niveles distintos? (decisión de producto)
- `person_con_chaleco` (id 3) no la emite ningún dataset → clase sin datos.
  ¿Se quita del esquema o se cubre solo por overlap de `safety_vest`?
- Umbral IoU 0.05 + center-containment sin validación cuantitativa.

## Tasks (para cerrar la fase)

- [ ] Arreglar `generate_notebooks.py` (`has_hardhat`/`has_vest` → `status`/`attributes`/`violations`) y regenerar → AC-6 (dep: SPEC-002 AC-1).
- [ ] Portabilidad de YAML/paths para poder ejecutar → AC-5 (dep: SPEC-002 AC-2).
- [ ] Escribir y correr el smoke test con `yolov8n.pt` (AC-5).
