# SmartMine Vision AI — Specs

## Índice

| Spec | Capacidad | Status | Fase |
|------|-----------|--------|------|
| [SPEC-001](001-detection-pipeline/spec.md) | Pipeline de detección + compliance | implemented ✅ | 1 |
| [SPEC-002](002-phase1-hardening/spec.md) | Estabilización / deuda de Fase 1 | implemented ✅ | 1 |
| [SPEC-003](../docs/specs/SPEC-003-notebook-workflow.md) | Notebook workflow (nbstripout) — vive en `docs/specs/` | implemented ✅ | transversal |
| [SPEC-004](../docs/specs/SPEC-004-vehicle-dataset.md) | Vehicle dataset sourcing — vive en `docs/specs/` | implemented ✅ | transversal |
| [SPEC-005](005-model-training-validation/spec.md) | Model Training & Validation (GPU, mAP objetivo) | draft 📝 | 1.5 |
| [SPEC-006](006-batch-compliance-report/spec.md) | Batch Compliance Report (MVP comercial) | draft 📝 | MVP |
| _SPEC-007_ | Vehicle detection (capacidad propia) | planned | 2 |
| _SPEC-008_ | Multi-object tracking (BoT-SORT/ByteTrack) | planned | 3 |
| _SPEC-009_ | Proximity alerts | planned | 4 |
| _SPEC-010_ | Database + API | planned | 5 |
| _SPEC-011_ | Dashboard + deployment | planned | 6 |

> Nota (2026-07-02): la numeración se corrió — SPEC-003/004 fueron consumidos
> por los specs implementados en `docs/specs/`, así que las capacidades que
> este índice listaba como 003–009 pasan a 005–011. Ver
> `docs/strategy/2026-07_reporte_estrategico_board.md` §2.4.

## Estados

| Status | Significado |
|--------|-------------|
| `draft` | En redacción / discusión. No acordado aún. |
| `approved` | Acordado por el equipo. Listo para implementar. |
| `partially implemented` | Parte del alcance existe en código; faltan criterios. |
| `implemented` | Todos los acceptance criteria pasan. |
| `superseded` | Reemplazado por otro spec (con link al sucesor). |
