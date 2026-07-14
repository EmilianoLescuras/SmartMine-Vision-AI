# SPEC-008 — Adquisición P0: Construction-PPE (botas + lentes + guantes)

Status: draft · Created: 2026-07-13 · Owner: Emiliano · Phase: 1 (cobertura de clases)
Base: `docs/research/dataset_audit_opsia.md` (gaps ❌) + SPEC-007 (pipeline de merge saneado)

---

## Context & Problem

La auditoría midió 4 clases objetivo del producto **sin un solo dato**: botas,
lentes, protección auditiva y uniforme. Además `core-baseline-1` (mAP50 0.427)
mostró el núcleo EPP débil (person_con_casco AP50 0.18, safety_vest 0.40).

Se incorpora **Construction-PPE (Ultralytics)**: 1.416 imgs, 11.614 anns,
11 clases balanceadas (411–2.265 inst.), auditado con 0 badlines / 0 missing.
Verificado por hash: la copia de Kaggle circulante es idéntica → se usa el
original de Ultralytics (data.yaml + LICENSE incluidos), descartando duplicados.

## Riesgos conocidos (aceptados y documentados)

1. **Licencia AGPL-3.0.** Mismo régimen que el paquete `ultralytics` que ya usa
   todo el proyecto → OPSIA debe resolver licencia Enterprise de Ultralytics (o
   migrar a stack Apache) antes de comercializar, con o sin este dataset. No
   introduce un riesgo nuevo; queda registrado como riesgo comercial global.
2. **Dominio de las clases de violación.** Los `no_*` provienen en parte de
   fotos no industriales (eventos/recitales). Riesgo de aprender contexto en
   vez de ausencia de EPP. Se mide en la validación por clase de baseline-2.
3. **`none` (800 anns) se skippea**: semántica ambigua ("persona sin ningún
   EPP") no mapeable al schema de compliance por atributo.

## Requirements (acceptance criteria)

| # | Criterio | Estado |
|---|----------|--------|
| AC-1 | Dataset en `datasets/raw/ppe/construction_ppe/` con LICENSE y data.yaml originales. Soporte del merge para layout `images/<split>` (además de `<split>/images`). | ✅ cumplido |
| AC-2 | Schema v1 extendido **al final** (ids 0-32 intactos): 33 `guantes_epp`, 34 `botas`, 35 `lentes_epp`, 36 `person_sin_botas`. `utils.CLASS_NAMES`/`CLASS_COLORS` alineados. pytest verde. | ✅ cumplido |
| AC-3 | Mapeo: helmet→27, gloves→33, vest→28, boots→34, goggles→35, none→skip, Person→0, no_helmet→2, no_goggle→8, no_gloves→6, no_boots→36. | ✅ cumplido |
| AC-4 | Core v2 regenerado: entran las clases nuevas y los pares que superan ≥100 inst. post-merge (botas, lentes_epp, guantes_epp, person_sin_lentes, person_sin_guantes, person_sin_botas). Re-auditoría: 0 badlines / 0 missing. | ✅ cumplido |
| AC-5 | `core-baseline-2` entrenado (early stop) y comparado contra baseline-1 por clase en `docs/research/training_report_baseline2.md`. | ✅ cumplido |

## Non-Goals

- Protección auditiva y uniforme (siguen ❌ — próxima adquisición / datos propios).
- Resolver la licencia comercial de Ultralytics (decisión de negocio, no de datos).
