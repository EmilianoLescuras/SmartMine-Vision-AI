# Catálogo de expansión de datasets — OPSIA / SmartMine

**Fecha:** 2026-07-16 · **Objetivo:** llevar el corpus al máximo de cobertura (minería +
oil & gas + EPP fino) para el entrenamiento definitivo en GPU (RTX 3080).
**Regla de oro:** ningún dataset entra al merge sin (1) verificación de licencia en su
página, (2) auditoría con nuestro script (conteos, badlines), (3) mapeo explícito en
`merge_datasets.py` con manifiesto. Proceso = SPEC-008.

Leyenda licencias: ✅ apta comercial verificada · ⚠️ verificar en la página del dataset
· ❌ no comercial (negociar o descartar) · 🏛️ académica (pedir permiso escrito)

---

## A. Ya integrados (corpus core v2 — 5.869 imgs)

| Dataset | Aporta | Licencia |
|---|---|---|
| css-data (Construction Site Safety) | EPP genérico en volumen | ✅ CC BY 4.0 |
| riskalert-mining | minería real | ✅ MIT |
| deteccion_escenarios v8 | minería real | ✅ CC BY 4.0 |
| construction-ppe (Ultralytics) | botas, lentes, guantes | ⚠️ AGPL-3.0 (mismo régimen que el stack; resolver con licencia Enterprise de Ultralytics antes de comercializar) |

## B. Catalogados en `download_datasets.py`, pendientes de mapear al merge

| Dataset | Aporta | Acción |
|---|---|---|
| **riskalertai v10** (workspace propio) | minería real, más volumen que riskalert v1 | P0 — mapear clases al schema y auditar |
| **construction_vehicles** (0925/construction-vehicle-inspection) | vehículos de obra | P1 — auditar clases y decidir mapeo |

## C. Maquinaria pesada y vehículos (minería)

| Prioridad | Dataset | Tamaño / clases | Licencia | Notas de mapeo |
|---|---|---|---|---|
| **P0** | [Heavy Equipment (Roboflow)](https://universe.roboflow.com/excavator-sampling/heavy-equipment) | 472 imgs, excavadoras/equipo pesado | ⚠️ | Refuerzo directo de `excavadora` (AP 0.38 → objetivo >0.6) |
| **P0** | [Mining Truck (Roboflow)](https://universe.roboflow.com/ryf09681065-gmail-com/mining-truck) | 92 imgs haul truck | ⚠️ | Chico pero es `volquete` real (nuestra clase más débil: AP 0.29) |
| **P0** | [Open Images V7 — subconjuntos](https://storage.googleapis.com/openimages/web/index.html) | miles: Truck, Van, Bulldozer, Excavator(?) | ✅ anotaciones CC BY 4.0 | Extraer con FiftyOne solo las clases objetivo; volumen legalmente limpio para `camion`/`camioneta` |
| **P1** | [ACID — Advanced Construction Image Dataset](https://www.acidb.net/dataset) | ~10.000 imgs, 10 clases de máquina (excavator, dozer, grader, dump truck, wheel loader, backhoe, cranes) | 🏛️ research — **enviar mail pidiendo licencia comercial** | El mejor corpus de maquinaria que existe; recuperaría `cargador_frontal` y `tractor` |
| **P1** | [SODA — Site Object Detection dAtaset](https://arxiv.org/pdf/2202.09554) | ~20k imgs, 15 clases de obra | ⚠️ | Personas + máquinas + materiales en obra real |
| **P1** | [AIDCON (aéreo)](https://www.mdpi.com/2072-4292/16/17/3295) | ~2.1k imgs aéreas de maquinaria | ⚠️ paper CC BY | Vista dron/altura — útil para cámaras altas de rajo |
| **P2** | [MOCS — Moving Objects in Construction Sites](https://www.sciencedirect.com/science/article/abs/pii/S0926580520310621) | 41.668 imgs, 13 clases, 174 sitios | ❌ CC BY-NC — comercial vía OTT Tsinghua | Solo si ACID no responde; volumen enorme |
| **P2** | COCO (subconjunto truck/person) | miles | ✅ CC BY 4.0 anotaciones | Robustez de dominio general, no minero |

## D. EPP fino (cerrar botas/lentes/guantes/auditiva definitivamente)

| Prioridad | Dataset | Aporta | Licencia |
|---|---|---|---|
| **P0** | [PPE Dataset for Workplace Safety (SiaBar)](https://universe.roboflow.com/siabar/ppe-dataset-for-workplace-safety) | 1.604 imgs con **ear-protection** (¡nuestro único gap total!) + boots + gloves | ⚠️ verificar en página |
| **P0** | [Safety Helmet and Reflective Jacket (Kaggle)](https://www.kaggle.com/datasets/niravnaik/safety-helmet-and-reflective-jacket) | 10.500 imgs casco+chaleco — volumen para el núcleo | ⚠️ verificar en página |
| **P1** | [Safety-boots detection (Roboflow)](https://universe.roboflow.com/construction-ppe-dataset/safety-boots-detection) + [safety-boots-rmxcj](https://universe.roboflow.com/ppe-datacustom/safety-boots-rmxcj) | refuerzo de botas | ⚠️ |
| **P1** | SHWD — Safety Helmet Wearing Dataset (GitHub njvisionpower) | ~7.5k imgs casco/persona | ⚠️ verificar repo |
| **P2** | [PPEs (Roboflow, personal-protective-equipment)](https://universe.roboflow.com/personal-protective-equipment/ppes-kaxsi) | EPP variado | ⚠️ |
| ❌ | SH17 (8k imgs, earmuffs+shoes+glasses) | cubre 3 gaps a la vez PERO | ❌ CC BY-NC-SA — solo como referencia; replicable con imágenes Pexels propias |

## E. Oil & Gas (nueva vertical)

| Prioridad | Dataset | Aporta | Licencia |
|---|---|---|---|
| **P0** | [Búsqueda Roboflow `class:coverall`](https://universe.roboflow.com/search?q=class:coverall) | **mamelucos/coveralls FR** — el uniforme estándar del petróleo; elegir 1-2 proyectos con más imgs y licencia apta | ⚠️ por proyecto |
| **P0** | [D-Fire (GitHub)](https://github.com/gaia-solutions-on-demand/DFireDataset) | 21.000+ imgs **fuego y humo** en formato YOLO | ⚠️ verificar términos del repo |
| **P1** | [FASDD](https://essd.copernicus.org/preprints/essd-2023-73/) | 120.000 imgs fuego/humo multi-escenario | ⚠️ open-access (ESSD suele ser CC BY 4.0 — verificar) |
| **P1** | [Smoke-Fire-Detection-YOLO (Kaggle)](https://www.kaggle.com/datasets/sayedgamal99/smoke-fire-detection-yolo) | fuego/humo listo en YOLO | ⚠️ |
| Nota | Detección de **fugas de gas** | — | Requiere cámaras térmicas/IR (OGI); fuera del alcance RGB actual — no prometer en marketing hasta tener hardware socio |

Clases nuevas que habilita esta vertical: `mameluco/coverall`, `fuego`, `humo` (al final
del schema, ids nuevos, sin romper los existentes).

## F. Robustez de condiciones (fase posterior)

- Negativos/backgrounds mineros: **ya los tenemos** (mining_area excluido del schema
  sirve como imágenes de fondo sin anotar — gratis).
- ExDark (baja luz) y DAWN (clima adverso): 🏛️ académicos — considerar solo para
  evaluación (medir robustez), no para entrenar comercialmente.

---

## Plan de entrenamiento con la RTX 3080 (10-12 GB)

| Corrida | Config | Tiempo estimado |
|---|---|---|
| Smoke test | yolov8s, 10 ép., 640px, batch 32 | ~15 min |
| **Baseline-3 (corpus actual)** | yolov8s, 100 ép., 640px, AutoBatch | **~2-3 h** |
| Baseline-4 (corpus + P0 nuevos) | yolov8s → yolov8m si VRAM alcanza, 100-150 ép. | ~3-6 h |

Recomendación de secuencia: **primero SPEC-009 (schema v3 de objetos puros)** con el
corpus actual en la 3080 — mide el techo real sin datos nuevos — y recién después la
ola de adquisición P0 de este catálogo, para poder atribuir cada mejora a su causa.

## Orden de ejecución sugerido

1. Mapear al merge lo ya descargable: riskalertai v10 + construction_vehicles (0 costo).
2. Descargar y auditar los P0 de C, D y E (verificando licencia página por página).
3. Mail a ACID pidiendo licencia comercial (costo cero, en paralelo).
4. SPEC de adquisición (proceso SPEC-008) + regenerar corpus + entrenar en la 3080.
