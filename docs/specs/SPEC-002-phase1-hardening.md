# SPEC-002 — Phase 1 Hardening & Reproducibility

Status: draft
Created: 2026-06-21 · Owner: TBD · Phase: 1 (transversal a SPEC-001)

---

## Context & Problem

El pipeline de Fase 1 (SPEC-001) está escrito pero no es reproducible ni
verificado: hay un path absoluto de otra máquina, el generador de notebooks
quedó desincronizado del código (usa `has_hardhat`, atributo que ya no existe),
no hay tests, y algunos notebooks afirman resultados que nunca se computaron.

Este spec agrupa la **deuda y los bloqueos** cuyo outcome común es: *la Fase 1
corre en cualquier máquina, es consistente entre doc y código, y tiene una red
de seguridad mínima.* No agrega funcionalidad — estabiliza lo que ya hay.

## Goals

- Reproducibilidad: el pipeline corre en una máquina limpia sin editar paths.
- Consistencia doc↔código: notebooks y reportes no afirman lo no verificado.
- Red de seguridad: tests sobre la lógica pura (compliance).

## Non-Goals

- Features nuevas o módulos 2–6.
- Entrenar el modelo / objetivo de mAP → SPEC-003.
- CI/CD y Docker → spec de plataforma posterior.

## Requirements (acceptance criteria)

| # | Criterio | Prioridad | Bloquea |
|---|----------|-----------|---------|
| AC-1 | `generate_notebooks.py` usa solo la API vigente de `WorkerCompliance` (`status`, `attributes`, `violations`); notebooks regenerados | 🔴 alta | SPEC-001 AC-6 |
| AC-2 | Ni el YAML ni `merge_datasets.py` escriben paths absolutos; el dataset se resuelve relativo al repo | 🔴 alta | SPEC-001 AC-5, SPEC-003 |
| AC-3 | Versión de Python única y consistente en `requirements.txt`, `environment.yml` y el generador | 🟡 media | — |
| AC-4 | Tests unitarios de `ppe_classifier` (SAFE/UNSAFE/UNKNOWN, IoU, center-containment, precedencia de señal embebida) | 🟡 media | — |
| AC-5 | Conclusiones de notebooks reflejan estado real (marcadas `draft`/`previsión` o generadas de datos) — sin "Complete ✅" / "Clean" falsos | 🟡 media | — |
| AC-6 | `environment.yml` no asume hardware fijo (`cudatoolkit=11.8` condicional o documentado; coexiste con MPS/CPU) | 🟢 baja | — |
| AC-7 | `LICENSE` presente (el README declara MIT pero el archivo no existe) | 🟢 baja | — |

## Dependencies / orden sugerido

1. **AC-1 + AC-2** — desbloquean el smoke test de SPEC-001 y el training de SPEC-003. Empezar acá.
2. **AC-3, AC-4** — higiene de entorno + red de seguridad.
3. **AC-5** — honestidad de los notebooks.
4. **AC-6, AC-7** — cierre.

## Notes

- El dataset mergeado reporta `ISSUES FOUND`: 271 labels faltantes y ~185 líneas
  con formato malo (`docs/research/smartmine_validation_report.json`). La limpieza
  es prerequisito de un entrenamiento confiable, pero pertenece al hito de
  datos/training (SPEC-003/004), no a este spec — acá solo se registra para trazar la dependencia.
