# Auditoría de Datasets — OPSIA CV / SmartMine-Vision-AI

**Fecha:** 2026-07-12 · **Alcance:** carpeta `datasets/` completa (4 fuentes raw + corpus merged `smartmine_v1`)
**Método:** todos los números de este informe salen de contar archivos y parsear labels reales del repositorio local (script de auditoría, 12-jul-2026). Ninguna métrica es estimada.

---

## 1. Resumen ejecutivo

El corpus actual (`smartmine_v1`: **5.785 imágenes, 42.261 anotaciones, 32 clases**) permite entrenar un detector de **casco y chaleco en contexto industrial genérico**, pero **no cubre el producto que OPSIA vende**: cumplimiento EPP completo en minería.

Tres problemas estructurales:

1. **Sesgo de dominio.** El 91% de las anotaciones (38.352 de 42.261) viene de un solo dataset de **construcción urbana** (css-data). Solo ~2.980 imágenes tienen contexto minero real, y aportan apenas el 20% de las anotaciones. El modelo aprenderá obras en construcción, no rajos ni plantas mineras.
2. **Clases objetivo sin datos.** De los 7 requisitos del producto, **3 no tienen ni una sola anotación**: botas de seguridad, protección auditiva y uniforme del operario. Lentes tiene solo 240 instancias (insuficiente). La clase `person_con_chaleco` está **vacía** (0 instancias) y contamina el mAP promedio.
3. **Deuda de calidad heredada.** 185 líneas de labels malformadas (origen: `mining_area`), 271 archivos de label descartados silenciosamente por el merge, y una clase `camion` (4.179 instancias) que mezcla vehículos genéricos de construcción con eventos de ingreso vehicular de otro dataset — semántica destruida.

**Recomendación central:** antes de gastar GPU en reentrenar (SPEC-005), (a) reducir el schema activo a un núcleo entrenable, (b) sanear `mining_area`, (c) incorporar 2–3 datasets P0 con licencia comercial apta, y (d) activar el pipeline de datos propios de cliente (SPEC-006/D6), que es la única vía realista para botas, auditiva y uniforme en contexto minero.

---

## 2. Inventario por fuente (números medidos)

| Fuente | Origen / Licencia | Imgs | Anotaciones | Clases | Calidad observada |
|---|---|---:|---:|---:|---|
| `raw/ppe/css-data` | Roboflow *Construction Site Safety* · **CC BY 4.0** | 2.801 | 38.352 | 10/10 con datos | 24 labels vacíos (backgrounds). Contexto: construcción urbana + imágenes indoor (fuente origen incluye MIT Indoor Scenes como nulls). **0 líneas malformadas.** |
| `raw/vehicles/riskalert` | Roboflow *riskalert-mining* (workspace propio) · **MIT** | 712 | 2.345 | 34/34 con datos | 5 labels vacíos. **Minería real**, pero fragmentación extrema: 2.345 instancias repartidas en 34 clases → mediana ~30 inst/clase. 9 clases `VIA_*` son de escenario, no de objeto. |
| `raw/vehicles/deteccion_escenarios` | Roboflow *deteccion-de-escenarios-de-riesg* v8 · **CC BY 4.0** | 940 | 3.209 | 67/67 con datos | 6 labels vacíos. **Minería real**, pero 67 clases para 3.209 instancias (~48 inst/clase). Mayoría son clases de escenario/estado (VIA_*, CLIMA, ETIQUETA_*, BANO_QUIMICO…) no detectables como objeto. |
| `raw/vehicles/mining_area` | Roboflow *mining-area-vehicle-detection* · **CC BY 4.0** | 1.332 | 2.789 | 3/3 con datos | **185 líneas malformadas** (96 archivos train, 1 valid, 4 test) — única fuente sucia. Clases en indonesio, semántica de **evento** ("vehículo ajeno entra al área"), no de tipo de vehículo. |
| `merged/smartmine_v1` | Generado por `merge_datasets.py` | 5.785 | 42.261 | 31/32 con datos | **271 `missing_label`** (el merge descarta archivos cuyas anotaciones son 100% de clases fuera del schema; 41 ya venían vacíos de origen). **185 badlines heredadas de mining_area** — el merge las copia sin sanear. `person_con_chaleco` = 0 instancias. |

**Respuesta a la open question de SPEC-003:** los `bad_format` **no** son bug de `merge_datasets.py` — son suciedad de origen de `mining_area` (185 líneas, verificado split por split: 177+1+7). Los `missing_label`, en cambio, **sí los produce el merge** al descartar labels sin clases mapeables sin registrar el motivo. AC-1 se resuelve con cuarentena en origen + manifiesto en el merge.

### Distribución de clases del merged (las 32, medidas)

| # | Clase | Inst. | # | Clase | Inst. |
|--:|---|---:|--:|---|---:|
| 0 | person | 9.944 | 16 | volquete | 476 |
| 1 | person_con_casco | 907 | 17 | **camion** | **4.179** ⚠️ |
| 2 | person_sin_casco | 2.522 | 18 | excavadora | 459 |
| 3 | **person_con_chaleco** | **0** ❌ | 19 | retro_excavadora | 118 |
| 4 | person_sin_chaleco | 4.163 | 20 | cargador_frontal | 81 ⚠️ |
| 5 | person_con_guantes | 204 | 21 | motoniveladora | 128 |
| 6 | person_sin_guantes | 46 ⚠️ | 22 | tractor | 23 ⚠️ |
| 7 | person_con_lentes | 155 ⚠️ | 23 | rodillo | 120 |
| 8 | person_sin_lentes | 85 ⚠️ | 24 | cisterna_agua | 125 |
| 9 | person_con_respirador | 21 ⚠️ | 25 | safety_cone | 3.725 |
| 10 | person_sin_respirador | 55 ⚠️ | 26 | senalizacion | 43 ⚠️ |
| 11 | person_ropa_reflectiva | 650 | 27 | hardhat | 3.334 |
| 12 | person_sin_ropa_reflectiva | 101 | 28 | safety_vest | 3.135 |
| 13 | mask | 1.705 | 29 | animal | 149 |
| 14 | camioneta | 218 | 30 | polvo | 32 ⚠️ |
| 15 | minibus | 12 ⚠️ | 31 | machinery | 5.346 |

⚠️ = <150 instancias (por debajo del mínimo práctico para un AP por clase confiable). **12 de 32 clases** están en esa zona o vacías.

**Hallazgo de mapeo crítico:** `camion` = 4.179 instancias, que es exactamente `vehicle` genérico de css-data (1.628) + las 2 clases de vehículo de mining_area (715 + 1.836 = 2.551). Es decir: la clase "camión" del modelo en realidad significa "cualquier vehículo de construcción o cualquier vehículo entrando a un área minera". No es un camión.

---

## 3. Matriz de cobertura — objetivos del producto × datos reales

| Objetivo OPSIA | Estado | Evidencia (instancias) | Contexto minero |
|---|:-:|---|:-:|
| **Casco de seguridad** | ✅ | hardhat 3.334 + con_casco 907 + sin_casco 2.522 | ⚠️ ~85% construcción |
| **Chaleco reflectivo** | ⚠️ | safety_vest 3.135, pero `person_con_chaleco` = **0** y sin_chaleco 4.163 → el corpus enseña más "sin chaleco" que "con chaleco" | ⚠️ mayormente construcción |
| **Botas de seguridad** | ❌ | **0 anotaciones. La clase ni existe en el schema.** | — |
| **Lentes de protección** | ❌ | 240 en total (155 con + 85 sin). Objeto pequeño + <250 muestras = no entrenable hoy | ⚠️ |
| **Protección auditiva** (zonas de voladura) | ❌ | **0 anotaciones. La clase ni existe en el schema.** | — |
| **Uniforme completo del operario** | ❌ | Sin clase. Proxy más cercano: person_ropa_reflectiva (650) / sin (101) | ⚠️ |
| **Maquinaria pesada** | ⚠️ | volquete 476 ✅ · excavadora 459 ✅ · camioneta 218 ⚠️ · motoniveladora 128 / cisterna 125 / rodillo 120 / retro 118 ⚠️ · cargador_frontal 81 / tractor 23 / minibus 12 ❌ · camion 4.179 **contaminada** · machinery 5.346 genérica de construcción | ⚠️ mixto |

Lectura honesta: **hoy el modelo base puede aspirar a casco + chaleco + 2-3 vehículos.** El resto del pitch comercial (botas, lentes, auditiva, uniforme, flota completa) no tiene sustento de datos todavía.

---

## 4. Qué QUITAR / remediar (con justificación)

| # | Acción | Justificación |
|---|---|---|
| R1 | **Sacar `mining_area` del merge de detección de objetos** (o re-anotar). Cuarentenar sus 185 líneas malformadas con manifiesto. | Sus 3 clases son eventos de zona ("vehículo ajeno entra al área"), no tipos de objeto. Mapearlas a `camion` inyectó 2.551 falsas instancias de camión — el 61% de la clase. Además es la única fuente con labels corruptos. Su valor real es para una futura capa de eventos/geofencing, no para el detector. |
| R2 | **Desagregar `vehicle` (css) de `camion`**: mapear a una clase `vehiculo_generico` o descartarla. | Con R1+R2, `camion` queda solo con volquetes/camiones reales de fuentes mineras. Hoy la clase miente. |
| R3 | **Submuestrear css-data** (p.ej. tope ~40-50% de las anotaciones del corpus) y filtrar sus imágenes indoor/null heredadas de MIT Indoor Scenes. | Con 91% de las anotaciones, css define lo que el modelo aprende: obras urbanas. En producción (rajo, planta, voladura) el fondo no se parece en nada. |
| R4 | **Reducir el schema de entrenamiento de 32 a un núcleo de ~14 clases** (ver §6). Las 12 clases con <150 inst + la vacía se excluyen del `data.yaml` de entrenamiento (los datos quedan, no se borran). | Clases vacías/débiles hunden el mAP promedio y hacen ilegible el gate de SPEC-003/AC-5. `person_con_chaleco`=0 es un cero garantizado en el promedio. |
| R5 | **De `deteccion_escenarios` y `riskalert`, mapear solo las clases de objeto** (personas, vehículos, señalética física). Las clases de escenario (`VIA_*`, `CLIMA_*`, `ETIQUETA_*`, `BANO_QUIMICO*`, etc.) quedan explícitamente fuera con motivo en el manifiesto del merge. | Son las que hoy generan los 271 `missing_label` silenciosos. Un detector de objetos no puede aprender "vía no regada" como bounding box con ~1-14 muestras. |

**Nada se borra:** R1–R5 son cambios de mapeo/config + cuarentena con manifiesto. Los datos raw quedan intactos y trazables.

---

## 5. Qué AGREGAR (adquisiciones priorizadas)

> ⚖️ **Criterio de licencia:** OPSIA es una empresa. Solo se integran al corpus datasets con licencia apta para uso comercial (CC BY 4.0, MIT, Apache, CC0). Los NC se listan como referencia porque son negociables, pero **no se descargan al repo** sin acuerdo escrito.

### P0 — cierran gaps del producto, licencia apta

| Dataset | Cubre | Tamaño | Licencia | Nota de integración |
|---|---|---|---|---|
| [Safety Helmet and Reflective Jacket (Kaggle)](https://www.kaggle.com/datasets/niravnaik/safety-helmet-and-reflective-jacket) | casco + chaleco (volumen y balance del lado "con chaleco") | 10.500 imgs | Verificar en la página (Dataset Ninja la indexa como pública) | Mapear `safety_helmet→hardhat`, `reflective_jacket→safety_vest`. Corrige el desbalance con/sin chaleco. |
| [PPE Dataset for Workplace Safety (Roboflow/SiaBar)](https://universe.roboflow.com/siabar/ppe-dataset-for-workplace-safety) y [variante ppe-la0vn](https://universe.roboflow.com/ppe-la0vn/ppe-dataset-for-workplace-safety-qobrx) | **botas + protección auditiva** + guantes + lentes | miles (verificar por página) | Roboflow Universe — verificar CC BY 4.0 por proyecto | Primera fuente real para `botas` y `proteccion_auditiva`. Clases nuevas del schema v2. |
| [Safety-boots detection (Roboflow)](https://universe.roboflow.com/construction-ppe-dataset/safety-boots-detection) + [safety-boots-rmxcj](https://universe.roboflow.com/ppe-datacustom/safety-boots-rmxcj) | botas (refuerzo) | chico-mediano | verificar por página | Complemento de la fila anterior. |
| `construction_vehicles` + `riskalertai` v10 — **ya catalogados en `scripts/download_datasets.py` del repo OPSIA-CV** | maquinaria | — | Roboflow | Ejecutar el download y auditarlos con este mismo script antes de mergear. |

### P1 — maquinaria minera (volumen)

| Dataset | Cubre | Tamaño | Licencia | Nota |
|---|---|---|---|---|
| [Heavy Equipment (Roboflow)](https://universe.roboflow.com/excavator-sampling/heavy-equipment) | excavadoras y equipo pesado | 472 imgs | verificar | Refuerzo de excavadora/cargador. |
| [Mining Truck (Roboflow)](https://universe.roboflow.com/ryf09681065-gmail-com/mining-truck) | camión minero | 92 imgs | verificar | Chico pero es *haul truck real*. |
| [ACID — Advanced Construction Image Dataset](https://www.acidb.net/dataset) | 10 clases de máququina: excavator, dozer, grader, dump truck, wheel loader, backhoe, cranes… | ~10.000 imgs | **Research — pedir permiso comercial** | El mejor corpus de maquinaria; vale la pena el mail. |
| [MOCS — Moving Objects in Construction Sites](https://www.sciencedirect.com/science/article/abs/pii/S0926580520310621) | 13 categorías, 174 sitios | 41.668 imgs | **CC BY-NC — comercial vía OTT Tsinghua** | Solo si ACID no responde; trámite más pesado. |

### P2 — referencia / no integrables directo

| Dataset | Por qué importa | Bloqueo |
|---|---|---|
| [SH17 (GitHub)](https://github.com/ahmadmughees/SH17dataset) · [paper](https://arxiv.org/abs/2407.04590) | **El único dataset público que cubre exactamente nuestros 3 gaps a la vez**: earmuffs, safety-shoes, glasses (8.099 imgs, 75.994 inst, 17 clases) | **CC BY-NC-SA 4.0 — prohibido uso comercial.** Opciones: (a) pedir licencia comercial a los autores (U. Windsor), (b) **replicar su método**: las imágenes salen de Pexels (licencia libre) — podemos armar nuestro propio "OPSIA-PPE" scrapeando Pexels/Unsplash y anotando, que además queda como activo propio de la empresa. |
| **Uniforme del operario** | No existe dataset público de "uniforme corporativo minero" — es específico de cada cliente | Única vía: **datos propios**. El MVP de SPEC-006 (auditoría sobre video del cliente, con cláusula de consentimiento D6) genera exactamente este material. Anotar uniforme sobre esos videos por cliente. |

---

## 6. Riesgos del schema actual y propuesta v2

**Riesgos medidos:**
1. **Doble anotación semántica:** `person_con_casco` (embebida) coexiste con `hardhat` (separada). El mismo píxel de casco puntúa dos veces o ninguna según la fuente. El resolver híbrido lo maneja en inferencia, pero en entrenamiento confunde al modelo y en evaluación parte el AP entre dos clases.
2. **13 clases de 32 con ≤150 instancias** (incluida una en cero): el mAP macro queda dominado por clases no entrenables — es el motivo aritmético principal del mAP50=0.13 de baseline-7, junto con las 7 épocas.
3. **Desbalance con/sin invertido en chaleco:** 4.163 "sin" vs 0 "con" (embebidas). El modelo aprenderá que la gente no usa chaleco.

**Schema núcleo propuesto para Fase 1 (14 clases):**
`person`, `person_con_casco`, `person_sin_casco`, `hardhat`, `safety_vest`, `person_sin_chaleco`, `person_ropa_reflectiva`, `camioneta`, `volquete`, `excavadora`, `retro_excavadora`, `motoniveladora`, `rodillo`, `cisterna_agua` — todas con ≥100 instancias reales tras R1/R2, todas del dominio del producto. `mask`, `safety_cone`, `machinery` opcionales como auxiliares. El resto se reintroduce en v2 cuando las adquisiciones P0 les den masa (botas, lentes, auditiva, uniforme entran acá).

---

## 7. Plan de acción sugerido (en orden)

| Paso | Qué | Por qué primero | Spec relacionado |
|---|---|---|---|
| 1 | Sanear merge: R1 (mining_area fuera/cuarentena), R2 (vehicle≠camion), R5 (manifiesto de clases descartadas) + `find datasets -name "*.cache" -delete` | Sin datos limpios, ningún mAP es diagnóstico | SPEC-003 AC-1 |
| 2 | `data.yaml` sin paths absolutos | Portabilidad al equipo OPSIA (repo compartido) | SPEC-003 AC-2 |
| 3 | Schema núcleo 14 clases en un `smartmine_core.yaml` | El gate AC-5 se vuelve medible y honesto | SPEC-003 AC-5/AC-6 |
| 4 | Descargar y auditar P0 (mismo script de esta auditoría); verificar licencia página por página antes de mergear | Cierra casco/chaleco en volumen y abre botas/auditiva | SPEC-004 |
| 5 | Reentrenar baseline completo (100 épocas) sobre corpus saneado + schema núcleo | Recién acá el número significa algo | SPEC-005 |
| 6 | Mail de licencia comercial a ACID (y evaluar SH17 con autores) — en paralelo, costo cero | Desbloquea maquinaria y PPE fino a escala | — |
| 7 | Activar pipeline de datos propios vía MVP de compliance (video de cliente + consentimiento) | Única fuente realista de uniforme + contexto minero propio; además es el producto | SPEC-006 / D6 |

---

*Generado por auditoría automatizada sobre el working tree local (`develop`). Nota de sincronización: el `develop` de `OPSIA-CV/SmartMine-Vision-AI` está 10 commits adelante del clon local auditado; los conteos de datasets no se ven afectados (los datos viven solo en local), pero el reporte de validación del repo remoto (6.156 imgs) incluye fuentes aún no descargadas localmente.*
