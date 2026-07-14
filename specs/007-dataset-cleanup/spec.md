# SPEC-007 — Dataset Cleanup & Core Training Schema

Status: implemented — en review (PR #7) · Created: 2026-07-12 · Owner: Emiliano · Phase: 1 (calidad de datos)
Base: `docs/research/dataset_audit_opsia.md` (auditoría 2026-07-12, números medidos)

---

## Context & Problem

La auditoría de datasets midió tres defectos estructurales del corpus
`merged/smartmine_v1` que hacen que cualquier entrenamiento sea no-diagnóstico:

1. **185 líneas de label malformadas** entran al corpus sin validación.
   Origen verificado: dataset `mining_area` (96 archivos train, 1 valid, 4 test).
   `merge_datasets.py` copia las líneas sin validar formato.
2. **271 imágenes quedan sin label** en el merged porque el merge descarta
   archivos cuyas anotaciones son 100% de clases skippeadas — sin registrar
   motivo. El validador los reporta como `missing_label` y no se puede
   distinguir un background legítimo de un label perdido.
3. **La clase `camion` (4.179 inst.) miente:** 61% son eventos de ingreso
   vehicular de `mining_area` ("Kendaraan masuk tambang" = evento de zona, no
   tipo de vehículo) y 39% son `vehicle` genérico de css-data. Además
   `person_con_chaleco` está vacía (0 inst.) y 12/32 clases tienen <150
   instancias — el mAP macro queda dominado por clases no entrenables
   (mAP50=0.13 en baseline-7).

## Goals

- Corpus v1 sin líneas malformadas ni `missing_label` inexplicados: todo
  descarte queda registrado en un **manifiesto de merge** (trazabilidad).
- Semántica de clases honesta: `camion` deja de mezclar eventos con objetos.
- Un **corpus de entrenamiento núcleo** (`smartmine_core`) con solo clases
  ≥100 instancias y semántica de objeto limpia, para que el próximo
  entrenamiento (SPEC-005) mida algo real.

## Non-Goals

- Adquirir datasets nuevos (P0/P1 de la auditoría) → spec de adquisición aparte.
- Entrenar el modelo (SPEC-005 lo hace, sobre el corpus de este spec).
- Capa de eventos/geofencing (donde `mining_area` sí aporta) → futuro.

## Requirements (acceptance criteria)

| # | Criterio | Estado |
|---|----------|--------|
| AC-1 | `merge_datasets.py` valida cada línea (5 campos, class id entero, 4 floats en [0,1]). Las inválidas NO entran al corpus y quedan en `_quarantine/manifest.json` con archivo, línea, contenido y motivo. | ✅ cumplido |
| AC-2 | Imágenes cuyas anotaciones se skippean al 100% reciben **label vacío explícito** (background intencional) y se contabilizan en el manifiesto. Resultado: 0 `missing_label` en el validador. | ✅ cumplido |
| AC-3 | `mining_area` sale del merge de detección de objetos (comentado con rationale — sus clases son eventos de zona). El corpus v1 no contiene sus 2.551 anotaciones ni sus 185 líneas corruptas. | ✅ cumplido |
| AC-4 | `vehicle` genérico de css-data se mapea a una clase nueva `vehiculo_generico` (id 32, al final — no rompe IDs existentes en `src/`). `camion` (17) queda vacía y documentada como reservada para datos reales de camión. | ✅ cumplido |
| AC-5 | El merge genera además `merged/smartmine_core/` con **18 clases núcleo** (todas ≥100 inst., semántica limpia) + `configs/yaml/smartmine_core.yaml`. Las clases excluidas y el motivo quedan en el manifiesto. | ✅ cumplido |
| AC-6 | Re-auditoría post-merge confirma: 0 badlines, 0 missing_label, conteos por clase publicados en el manifiesto. Caches YOLO invalidados (`find datasets -name "*.cache" -delete`). | ✅ cumplido |
| AC-7 | `pytest` verde y `utils.CLASS_NAMES` alineado con el schema v1 (33 clases). | ✅ cumplido |

## Schema núcleo (AC-5) — 18 clases

`person, person_con_casco, person_sin_casco, person_sin_chaleco,
person_ropa_reflectiva, person_sin_ropa_reflectiva, mask, hardhat,
safety_vest, safety_cone, camioneta, volquete, excavadora, retro_excavadora,
motoniveladora, rodillo, cisterna_agua, machinery`

Criterio de inclusión: ≥100 instancias medidas post-limpieza + relevancia
directa al producto (compliance EPP + vehículos mineros + auxiliares con masa).
Exclusiones documentadas: pares guantes/lentes/respirador (violación con <100
inst. → par indetectable), animal/polvo (ambientales débiles), camion y
vehiculo_generico (semántica genérica, no entrenables como clase de producto).

## Design notes

- Un solo pase del merge produce v1 (archivo completo, 33 clases) y core
  (entrenamiento, 18 clases). Core remapea vía unified_id → core_id.
- Nada se borra de `raw/`: mining_area queda en disco para la futura capa de
  eventos. La cuarentena es registro, no movimiento de archivos raw.
- El manifiesto (`merge_manifest.json`) vive junto al corpus (gitignoreado) y
  un resumen se imprime en consola; el reporte de re-auditoría va a
  `docs/research/` (versionado).
