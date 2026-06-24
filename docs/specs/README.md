# SmartMine Vision AI — Specifications

Spec-Driven Development (SDD) para SmartMine Vision AI. Los specs son la
**fuente de verdad técnica** del proyecto: describen qué hace cada capacidad,
con qué criterios se considera terminada y cómo se diseñó.

## Cómo leer esto

1. **`constitution.md`** — principios y convenciones que **todo** spec respeta.
   Empezá por acá si sos nuevo en el repo.
2. **`SPEC-XXX-*.md`** — una capacidad por spec. Cada uno declara su `Status`.

## Índice de specs

| Spec | Capacidad | Status | Fase |
|------|-----------|--------|------|
| [SPEC-001](SPEC-001-detection-pipeline.md) | Pipeline de detección + compliance | draft · partially implemented | 1 |
| [SPEC-002](SPEC-002-phase1-hardening.md) | Estabilización / deuda de Fase 1 | draft | 1 |
| _SPEC-003_ | Model Training & Validation (fine-tuning, mAP) | planned | 1.5 |
| _SPEC-004_ | Data acquisition & reproducibility | planned | transversal |
| _SPEC-005_ | Vehicle detection (capacidad propia) | planned | 2 |
| _SPEC-006_ | Multi-object tracking (ByteTrack) | planned | 3 |
| _SPEC-007_ | Proximity alerts | planned | 4 |
| _SPEC-008_ | Database + API | planned | 5 |
| _SPEC-009_ | Dashboard + deployment | planned | 6 |

> La **propuesta comercial** (`../SmartMine_Vision_AI_Project_Proposal.md`) es un
> documento de **previsión / visión de negocio**, no un spec normativo. Sus
> números (mAP, FPS, tiempos) son metas a tener en cuenta, no criterios de "done".
> Ante conflicto, manda el spec.

## Estados de un spec

| Status | Significado |
|--------|-------------|
| `draft` | En redacción / discusión. No acordado aún. |
| `approved` | Acordado por el equipo. Listo para implementar. |
| `partially implemented` | Parte del alcance existe en código; faltan criterios. |
| `implemented` | Todos los acceptance criteria pasan. |
| `superseded` | Reemplazado por otro spec (con link al sucesor). |

## Template mínimo

Context & Problem · Goals / Non-Goals · Requirements (acceptance criteria) ·
Design notes · Open questions · Tasks. Ver cualquier `SPEC-00X` como referencia.
