# Reporte de entrenamiento — core-baseline-2 (SPEC-008 / AC-5)

**Fecha:** 2026-07-14 · **Corpus:** `smartmine_core` v2 (5.869 imgs, 26 clases, 48.390 anns)
**Modelo:** yolov8n · 640px · MPS (Apple M4) · fases 2 (ép.1-21, batch 8) → 2b (batch 16 + workers 8) → 2c (lr suave)
**Mejor checkpoint:** fase 2b · `models/ppe/yolov8n_smartmine_core-baseline-2.pt`

## Resultado global (val split v2, 459 imgs)

| Métrica | baseline-1 (18 cls) | baseline-2 (26 cls) |
|---|---:|---:|
| mAP50 global | 0.427* | 0.400 |
| mAP50-95 | 0.259* | 0.212 |
| **Núcleo seguridad (6 clases)** | 0.363 | **0.419** ✅ |

\* medido sobre el val split v1 (316 imgs, sin construction-ppe) — comparable solo como referencia.

## El hallazgo central: dos familias, dos destinos

**EPP como objeto separado — FUNCIONA (todas las clases nuevas debutaron arriba de 0.7):**

| Clase | AP50 | vs baseline-1 |
|---|---:|---|
| botas | **0.739** | nueva (gap ❌ → cubierto) |
| lentes_epp | **0.727** | nueva (gap ❌ → cubierto) |
| guantes_epp | **0.711** | nueva |
| safety_vest | **0.705** | 0.397 → +78% |
| hardhat | **0.700** | 0.563 → +24% |

**Estado embebido en la persona — NO FUNCIONA (todas hundidas):**

| Clase | AP50 |
|---|---:|
| person_con_casco | 0.194 |
| person_sin_chaleco | 0.145 |
| person_sin_guantes / con_guantes | 0.110 / 0.069 |
| person_sin_lentes | 0.038 |
| person_sin_botas | 0.034 |

**Conclusión (confirma el riesgo #1 de la auditoría con evidencia):** el modelo
detecta muy bien EPP como objeto; no puede aprender "persona en estado X" con
fuentes que anotan ese estado de forma inconsistente. Las clases embebidas
fragmentan a `person` y contradicen entre fuentes. El promedio global (0.400)
esconde un detector de EPP excelente lastrado por ~10 clases embebidas rotas.

## Decisión propuesta → schema v3 (spec siguiente)

Plegar las clases `person_(con|sin)_X` a `person` + ítems EPP separados, y
derivar el compliance en inferencia con el resolver híbrido de
`ppe_classifier.py` (overlap persona-EPP), que ya existe y fue diseñado para
esto. Schema de entrenamiento estimado: ~15 clases de objeto puro. Proyección:
mAP50 global >0.55 con los mismos datos.

## Lecciones operativas (entrenar en MPS)

- 4 crashes en ~70 épocas acumuladas (2 bugs distintos del backend Metal) +
  1 proceso colgado. El wrapper de auto-reintento fue imprescindible.
- `workers=0` (default de Ultralytics en MPS) triplica el tiempo de época;
  `workers=8, batch=16` lo llevó de 31 a ~9 min/ép en M4 (16 GB).
- Trampa de warm-restart: reiniciar con lr alto produce un bache que puede
  consumir la paciencia del early stopping contra el mejor punto heredado
  (pasó en 2b: cortó en ép. 21 con la curva subiendo).
- **Recomendación firme:** la corrida definitiva (schema v3, 100 épocas
  ininterrumpidas, y eventual yolov8s) debe hacerse en GPU CUDA (Colab T4
  gratis ≈ 2-3 h, o 2080 Ti local ≈ 3-4 h). MPS queda para smoke tests.

## Estado de gates

- Gate Fase 1 (mAP50 ≥ 0.50 global): **no alcanzado aún** — bloqueado por el
  schema, no por los datos. v3 + GPU es el camino.
- Gaps de datos restantes: protección auditiva ❌, uniforme ❌ (SPEC futuro /
  video de cliente vía SPEC-006).
