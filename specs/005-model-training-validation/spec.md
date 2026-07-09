# SPEC-005 — Model Training & Validation (GPU, calidad objetivo)

Status: draft · pendiente de aprobación del board
Created: 2026-07-02 · Owner: TBD · Phase: 1.5

> Nota de numeración: `specs/README.md` listaba esta capacidad como
> "_SPEC-003_ planned", pero SPEC-003/004 ya fueron consumidos por
> `docs/specs/` (notebook workflow, vehicle dataset). Este spec adopta **005**
> para resolver la colisión; el índice debe actualizarse al aprobarse.

---

## Context & Problem

SPEC-001 entregó el pipeline de software y lo separó explícitamente de la
calidad del modelo ("pipeline implementado ≠ modelo bueno"). Esa segunda mitad
sigue abierta: el único modelo entrenado es un baseline de verificación en CPU
(mAP50 = 0.076 — subset 20%, 10 épocas, 416px). Los bloqueos técnicos que
impedían entrenar (bug de resolución de paths del dataset, bug de MPS) se
resolvieron el 2026-06-30 y el entorno quedó flexible CPU/GPU
(`trainer.recommended_train_config()`); falta ejecutar el entrenamiento real y
validar el resultado con rigor.

Además, el corpus tiene deuda cuantificada que afecta directamente la calidad
alcanzable: **643 imágenes sin label** (¿backgrounds legítimos o labels
perdidos en el merge?) y un esquema híbrido de 32 clases con fragmentación de
ejemplos (crítica en `production_roadmap.ipynb` §5.1).

## Goals

- Entrenar YOLOv8 (o YOLOv11, ver AC-6) en GPU sobre el corpus completo con el
  perfil CUDA existente (100 épocas, 640px, AutoBatch, early stopping).
- Triage de las 643 imágenes sin label: clasificarlas en *background legítimo*
  vs. *label perdido* (matching contra `datasets/raw/`), y corregir el merge
  si corresponde.
- Evaluación honesta: mAP50/mAP50-95 global y **por clase** sobre test set,
  con atención a recall de clases safety-critical (violaciones NO-casco /
  NO-chaleco).
- Decisión documentada sobre el esquema de clases (mantener 32 híbridas vs.
  reducir), basada en los resultados por clase.

## Non-Goals

- Detección de vehículos como capacidad propia (módulo 2 — spec futuro).
- Serving/optimización de inferencia (ONNX/TensorRT) más allá de lo ya hecho.
- El producto de reporting sobre video → SPEC-006.

## Acceptance Criteria

1. **AC-1:** Existe una corrida GPU completa registrada (métricas + curvas en
   `experiments/`), con el modelo resultante copiado a `models/ppe/` y su
   mAP50 real reportado en el spec (sea cual sea el número).
2. **AC-2:** Las 643 imágenes sin label tienen veredicto documentado
   (background / label recuperado / descartada) y el reporte de validación
   posterior al fix no reporta `missing_label` sin explicación.
3. **AC-3:** Tabla de métricas por clase en test set, con las clases de
   violación (safety-critical) destacadas y su recall reportado.
4. **AC-4:** Si mAP50 < 0.70 (meta de la propuesta — Principio II: meta, no
   contrato), el spec documenta el gap y el plan siguiente (más datos /
   cambio de esquema / modelo mayor) en vez de afirmar éxito.
5. **AC-5:** Licencias de las 5 fuentes del corpus (css-data + 4 vehiculares
   Roboflow) auditadas y documentadas: apto/no-apto para uso comercial.
6. **AC-6:** Comparación corta YOLOv8n vs YOLOv11n (mismo protocolo) para
   decidir la base de las siguientes fases — el benchmarking 2026 sugiere
   ventaja de v11 en escalas chicas (MDPI Electronics 15(6):1146).

## Dependencies

- Máquina con GPU CUDA (colaborador con desktop — el notebook 03 auto-configura).
- `datasets/raw/` completo en la máquina que corra el triage (AC-2).
