# SmartMine Vision AI — Reporte Estratégico para el Board

> **Status:** `draft` — para discusión en reunión de board. Nada de este documento
> es un compromiso hasta que el board lo apruebe.
> **Fecha:** 2026-07-02
> **Alcance:** estado real del proyecto, brechas hacia producción, contexto de
> mercado y SOTA, **horizonte técnico por capa** (§4.3), roadmap comercial
> propuesto, MVP + quick-wins, y material para la reunión (agenda, decisiones,
> riesgos).
> **Método:** todo lo afirmado como *estado actual* fue verificado contra el
> repositorio (código, specs, historial de git, reportes de validación) al
> 2026-07-02. Las proyecciones y estimaciones están **marcadas explícitamente
> como estimaciones**. Las fuentes externas están citadas al final.
> **Complementa (no duplica):** [`docs/research/production_roadmap.ipynb`](../research/production_roadmap.ipynb)
> — el detalle *técnico* de cada brecha (arquitectura de streaming, serving,
> data flywheel, MLOps) vive ahí. Este documento es la capa *estratégica/comercial*.

---

## 1. Resumen ejecutivo

SmartMine Vision AI tiene hoy **un pipeline de detección de EPP funcional y
reproducible** (Módulo 1 de 6 de la propuesta), con buena gobernanza de
ingeniería (specs, constitution, notebooks regenerables, tests de la lógica de
compliance) — pero **sin un modelo entrenado a calidad objetivo, sin los
módulos 2–6, y sin ninguna pieza de producción** (API, DB, streaming, deploy).

El mercado valida la tesis: el segmento de *AI workplace safety* crece de
**USD 2.48B (2024) a una proyección de USD 29.82B (2033)** [F12], con
competidores fondeados (Intenseye USD 64M, Protex AI USD 36M, Voxel ~USD 61M)
cobrando entre **USD 15k y 100k+ anuales por sitio** [F12][F13]. Hay espacio
para un player LATAM/minería con precio de entrada bajo, pero la ventana exige
moverse: la diferenciación no va a estar en el modelo (commodity) sino en el
**despliegue vertical en minería, el costo y la cercanía al cliente**.

La recomendación central de este reporte: **acordar en el board un MVP acotado
de "reporte de cumplimiento EPP sobre video grabado"** (4–6 semanas de
esfuerzo estimado, aprovecha ~90% de lo ya construido), usarlo para conseguir
un primer piloto pago o carta de intención, y recién entonces financiar con
ese tracción el camino a tiempo real (tracking + proximidad + alertas), que es
lo que la propuesta original vende pero requiere ~4–6 meses más.

---

## 2. Estado actual del proyecto (verificado contra el repo)

### 2.1 Lo que existe y funciona ✅

| Componente | Evidencia | Estado |
|---|---|---|
| Pipeline de detección + compliance EPP (SW) | `specs/001` — 6/6 acceptance criteria | `implemented` |
| Hardening y reproducibilidad Fase 1 | `specs/002` — 7/7 criteria | `implemented` |
| Workflow de notebooks sin conflictos (nbstripout) | `docs/specs/SPEC-003` | `implemented` |
| Sourcing reproducible de datasets vehiculares | `docs/specs/SPEC-004`, `scripts/download_datasets.py` | `implemented` |
| Notebooks 01–06 del Módulo 1 ejecutan end-to-end | verificado en sesión 2026-06-30, 0 celdas con error | `validado` |
| Entrenamiento flexible CPU/GPU | `trainer.recommended_train_config()` — mismo notebook corre en laptop y desktop GPU | `validado` (GPU a nivel config; sin hardware CUDA disponible aún) |
| Export ONNX + benchmark de latencia CPU | `production_roadmap.ipynb` §3 (ejecutado) | `validado` |
| Clasificador híbrido de compliance (SAFE/UNSAFE/UNKNOWN) | `src/ppe_detection/ppe_classifier.py` + `tests/test_ppe_classifier.py` (único módulo con tests) | `implemented` |
| Gobernanza | constitution v1.0.0, spec-kit, conventional commits, ramas por feature | activa |

### 2.2 Lo que NO existe todavía (honesto) ❌

| Módulo de la propuesta | Estado real en el repo |
|---|---|
| **Modelo a calidad objetivo (mAP50 > 0.70)** | ❌ El único modelo entrenado es un baseline de verificación en CPU: **mAP50 = 0.076** (subset 20%, 10 épocas, 416px). Sirve para validar el pipeline, no para demo ni producción. **Nadie corrió aún el entrenamiento GPU completo.** |
| Módulo 2 — Detección de vehículos | ❌ Datasets descargados (4 fuentes Roboflow, 449 MB raw) y explorados (2 notebooks); **sin merge al corpus, sin entrenamiento**. `src/vehicle_detection/` está vacío. |
| Módulo 3 — Tracking (ByteTrack) | ❌ `src/tracking/` vacío. |
| Módulo 4 — Alertas de proximidad | ❌ `src/proximity/` vacío. |
| Módulo 5 — DB + API | ❌ `src/api/`, `src/database/` vacíos; `api/`, `database/` solo README. |
| Módulo 6 — Dashboard + deploy | ❌ `powerbi/`, `docker/` solo README/placeholder. Sin CI/CD. |
| Ingesta de video en vivo (RTSP) | ❌ Solo inferencia sobre archivos. No hay servicio de streaming. |

**Lectura ejecutiva:** el proyecto completó la **Fase 1 de 6** del plan de la
propuesta (que estimaba 28 semanas totales), con una salvedad importante: la
Fase 1 se declaró en la propuesta como "modelo con mAP50 > 0.70 + pipeline de
video operativo", y hoy tenemos **el pipeline sí, el modelo no**. El bloqueo
histórico (bug de paths que impedía entrenar, bug de MPS) se resolvió el
2026-06-30; el entrenamiento GPU real ya no tiene impedimentos técnicos, solo
falta ejecutarlo en una máquina con CUDA.

### 2.3 Calidad de datos — riesgo material, cuantificado

Del reporte de validación regenerado el 2026-06-30
(`docs/research/smartmine_validation_report.json`, verificado):

- Corpus unificado: **6.156 imágenes**, esquema de **32 clases**.
- **643 imágenes sin archivo de label** (YOLO las trata como *background* — si
  son labels perdidos en el merge, deprimen el recall silenciosamente).
- 1 duplicado detectado. Veredicto del validador: `ISSUES FOUND`.
- El esquema de 32 clases es **híbrido** (mezcla identidad + estado de
  compliance en la clase, ej. `person_con_casco`): funciona, pero fragmenta
  ejemplos entre clases y complica el aprendizaje — crítica técnica completa en
  `production_roadmap.ipynb` §5.1.

### 2.4 Deuda de gobernanza detectada (menor pero conviene cerrarla)

- **Colisión de numeración de specs:** `docs/specs/SPEC-003/004` (implementados:
  notebook workflow, vehicle dataset) vs. `specs/README.md` que lista
  *SPEC-003 Model Training* y *SPEC-004 Data acquisition* como `planned` con
  otro alcance. Decisión simple pero hay que tomarla (este reporte usa **005+**
  para los specs nuevos y esquiva el conflicto).
- Versión de Python **pendiente de unificación** (TODO explícito en la
  constitution: coexisten 3.12 / 3.13 / 3.14 según el entorno).
- Cobertura de tests limitada a `ppe_classifier` (139 líneas). El resto del
  pipeline no tiene red de seguridad.

---

## 3. Brechas hacia un sistema productivo

El detalle técnico por eje está en `production_roadmap.ipynb` (§2–§8). Resumen
estratégico de las 6 brechas, en orden de criticidad para comercializar:

| # | Brecha | Por qué importa comercialmente | Ref. técnica |
|---|---|---|---|
| 1 | **Modelo a calidad real** (GPU training + triage de los 643 labels + eval honesta por clase) | Sin mAP demostrable no hay demo creíble; es la puerta de todo lo demás | roadmap §4, §5 |
| 2 | **Ingesta de video en vivo** (RTSP → detección → eventos) | Es lo que la propuesta vende; hoy solo procesamos archivos | roadmap §2 |
| 3 | **Persistencia + API** (eventos consultables, evidencia de incidentes) | Sin registro auditable no hay caso de compliance, que es el driver de compra | roadmap §2 |
| 4 | **Serving optimizado** (ONNX/TensorRT, INT8, multi-stream) | Define el costo por cámara — el margen del negocio depende de esto | roadmap §3 |
| 5 | **MLOps mínimo** (experiment tracking, versionado de datos/modelos, retraining por sitio) | El fine-tuning por sitio es parte del delivery de cada cliente; hacerlo manual no escala | roadmap §6 |
| 6 | **Privacidad y gobernanza del dato** (DPIA, anonimización, retención) | Requisito de entrada en clientes enterprise y en varias jurisdicciones; también es diferenciador en la venta | roadmap §8, [F15] |

Dato de referencia para la brecha 4 (costo por cámara): en edge, un Jetson
Orin NX corre YOLOv8n a **~52 FPS (FP16) / ~65 FPS (INT8)**, y la cuantización
INT8 típicamente da **2–4× de speedup con ~1–2% de pérdida de precisión**
[F9][F10] — es decir, la meta de la propuesta (4–8 streams por GPU) es
alcanzable incluso en hardware edge de ~USD 700, no solo con una RTX 3090.

---

## 4. Contexto de mercado y estado del arte (para calibrar expectativas)

### 4.1 Mercado y competidores

- Mercado *AI in workplace safety*: **USD 2.48B (2024) → USD 29.82B proyectado (2033)** [F12].
- Competidores directos (visión sobre CCTV existente, mismo pitch que nuestra propuesta):
  **Intenseye** (USD 64M Serie B; enterprise, USD 100k+/año), **Protex AI**
  (USD 36M Serie B en ene-2025; USD 15–50k/año), **Voxel** (~USD 61M),
  más Surveily, Visionify (USD 15–40k/año), Observia, Everguard [F12][F13].
- En minería específicamente, el estándar de la industria para anti-colisión es
  **multi-sensor** (cámara + radar + LiDAR + tags + GNSS), con players como
  Sandvik/Newtrax que ya ofrecen *slow-to-stop* automático [F7][F8]. MSHA (EE.UU.)
  identificó en 2025 el *powered haulage* como la principal causa de
  fatalidades y empuja proximity detection como control [F7].

**Implicancia:** competir de frente con Intenseye/Voxel en enterprise global no
es viable hoy. El espacio defendible es: **(a)** minería/industria LATAM con
precio de entrada bajo y delivery cercano, **(b)** empezar por *compliance
reporting* (EPP) que es 100% software sobre cámaras existentes, y **(c)** ser
honestos en que la proximidad vehículo-persona *crítica de seguridad* (parar
una máquina) requiere fusión de sensores — nuestra alerta visual es una capa
de valor, no un sistema certificado de anti-colisión. Ese descargo, además,
nos protege legalmente.

### 4.2 Estado del arte técnico (síntesis)

- **Detección PPE:** los benchmarks públicos (SH17: 8.099 imágenes, 17 clases)
  reportan **mAP50 ~0.71 con YOLOv9-e** [F1][F2]; el benchmarking 2026 de
  YOLO26 vs YOLOv11 muestra que **YOLOv11 gana en escalas nano/small** y YOLO26
  en L/XL (+1.3–3.1 mAP50-95) [F3]. Lectura: nuestro objetivo mAP50 > 0.70 es
  ambicioso pero consistente con el SOTA; y para edge conviene evaluar YOLOv11n/s
  como upgrade de YOLOv8n (mismo ecosistema Ultralytics, cambio barato).
- **Tracking:** ByteTrack sigue siendo la base de producción; **BoT-SORT** (su
  evolución, hoy default en Ultralytics) lidera MOT17/MOT20 [F5][F6]. Adoptar
  el tracker default de Ultralytics nos da Módulo 3 casi "gratis" a nivel
  integración.
- **Edge/serving:** TensorRT + INT8 es el camino estándar (números en §3);
  DeepStream para multi-stream [F9][F10][F11].
- **Privacidad:** GDPR (y regímenes análogos) exigen DPIA, proporcionalidad,
  minimización y transparencia para videovigilancia laboral; la anonimización
  (blur de rostros) es práctica recomendada [F15]. **Pendiente de verificar**
  el marco exacto por jurisdicción objetivo (ej. Ley 25.326 en Argentina) —
  no lo investigamos en profundidad aún.

### 4.3 Horizonte técnico — apuestas y evolución por capa

Qué tecnología usamos hoy, a qué migramos y cuándo. Cada apuesta está atada a
la fase del roadmap (§5) que la necesita — adoptar antes de tiempo es costo sin
retorno. Detalle y alternativas evaluadas: `production_roadmap.ipynb` §2–§7.

| Capa | Hoy (F0–F1) | Corto plazo (F2, ~3–6 meses est.) | Mediano plazo (F3+, ~6–12 meses est.) |
|---|---|---|---|
| **Modelo** | YOLOv8n fine-tuned, esquema 32 clases híbrido | Evaluar **YOLOv11n/s** (gana en escalas chicas [F3], mismo API Ultralytics — cambio barato, gateado por SPEC-005 AC-6). Decisión sobre reducir el esquema de clases (§5.1 del roadmap: separar identidad de estado de compliance) | Modelo por sitio vía fine-tuning con datos del cliente (data flywheel); evaluar escala s/m si el edge lo banca |
| **Arquitectura** | Batch: video/imagen → pipeline en proceso único (notebooks / CLI del MVP) | Servicio de streaming: RTSP → decodificación → detección → **event bus** → persistencia. Un proceso por stream; sin microservicios prematuros | Multi-cámara con **DeepStream** (batching de streams en GPU [F11]) solo si un cliente real supera ~4–8 cámaras por nodo |
| **Serving** | ONNX Runtime **CPU** (ya validado; delivery del MVP sin GPU) | **TensorRT FP16** en la GPU del piloto; medir antes de optimizar | **INT8 + edge** (Jetson Orin: ~65 FPS YOLOv8n [F9][F10]) si el modelo on-premise/edge se vuelve requisito de venta |
| **Tracking / proximidad** | Ninguno (el MVP dedup temporal simple) | **BoT-SORT** vía Ultralytics (default, SOTA MOT17 [F6] — integración casi gratis) + proximidad 2D con calibración por homografía por cámara | Si un cliente exige anti-colisión *interventiva*: NO construirlo — integrar/partnerar con sistemas multi-sensor (posición honesta de §4.1) |
| **Datos** | Corpus estático 6.156 imgs; validación con script propio | Triage de labels (SPEC-005), pipeline de curación reproducible (versionado con **DVC** o equivalente), primer lote de video real de cliente | **Active learning**: minar del stream los frames de baja confianza → etiquetar → reentrenar (CVAT/FiftyOne; roadmap §4) |
| **MLOps** | Corridas manuales, métricas en `experiments/` | **Experiment tracking** (MLflow o W&B) desde la primera corrida GPU; registro de modelos con lineage dataset↔modelo | Retraining por sitio semi-automatizado; evaluación de regresión pre-deploy (gate de métricas por clase) |
| **Calidad/infra** | Tests solo en `ppe_classifier`; sin CI | **CI mínimo** (lint + tests + regeneración de notebooks verificada) + Docker del servicio de streaming | Observabilidad del servicio (métricas de FPS/latencia/drift por cámara) |

**Principio transversal:** cada migración se gatea por una necesidad medida
(FPS insuficiente, cliente con N cámaras, requisito contractual), nunca por
novedad. El costo de cambiar de YOLOv8→v11 es un flag; el costo de adoptar
DeepStream o microservicios antes de tiempo es semanas de plomería que el MVP
no necesita.

---

## 5. Roadmap propuesto hacia salida comercial

> ⚠️ **Todas las duraciones son estimaciones de esfuerzo**, asumiendo el equipo
> actual (colaboradores part-time, 1 máquina GPU disponible). No son fechas
> comprometidas; el board debe validar capacidad real antes de fijar fechas.

```
F0 Fundaciones      F1 MVP demo         F2 Pilot-ready        F3 Piloto + GA
(~3-4 sem est.)     (~4-6 sem est.)     (~8-10 sem est.)      (~6-8 sem est.)
─────────────────┬──────────────────┬─────────────────────┬──────────────────
GPU training real│ Vehículos merge  │ Tracking (BoT-SORT) │ Piloto en sitio
Triage 643 labels│  + retrain       │ Proximidad v1       │ Fine-tune con
Eval por clase   │ Reporte batch de │ DB + API eventos    │  datos del sitio
Audit licencias  │  compliance      │ RTSP live 1 cámara  │ Dashboard
  datasets       │  (producto MVP)  │ Docker + CI         │ Hardening + docs
Fix numeración   │ Demo comercial   │ Alertas             │ Pricing final
  specs          │  grabada         │                     │
```

| Fase | Gate de salida (criterio verificable) | Decisión de negocio asociada |
|---|---|---|
| **F0 — Fundaciones** | mAP50 real medido en test set + veredicto sobre los 643 labels + licencias de datasets auditadas | ¿El modelo da para demo? ¿El corpus es usable comercialmente? |
| **F1 — MVP demo** | Reporte de compliance sobre video de cliente generado end-to-end + demo grabada | Salir a buscar piloto pago / LOI |
| **F2 — Pilot-ready** | Stream RTSP en vivo con alertas persistidas, dockerizado, corriendo 72 h sin caerse | Firmar piloto con condiciones |
| **F3 — Piloto → GA** | Piloto de 4 semanas con métricas acordadas (precision de alertas, uptime) | Pricing, contrato tipo, GA |

**Total estimado a piloto: ~5–7 meses** — consistente con las ~22 semanas que
la propuesta original preveía para las fases 2–6, que en retrospectiva fue una
estimación razonable *de esfuerzo* pero no contemplaba capacidad part-time.

Dependencias duras: F1 depende del gate de modelo de F0; F2 depende de F1 solo
parcialmente (DB/API puede arrancar en paralelo); F3 depende de conseguir el
piloto (comercial, no técnico).

---

## 6. Propuesta de MVP + quick-wins

### 6.1 MVP: "Auditoría de cumplimiento EPP sobre video" (F1)

**Qué es:** el cliente sube (o enviamos a buscar) horas de video de sus cámaras;
el sistema devuelve un **reporte de cumplimiento EPP** — % de compliance por
período/cámara, capturas de cada infracción con timestamp, tendencias.
Sin tiempo real, sin instalación en sitio, sin hardware nuevo.

**Por qué este MVP y no el sistema completo:**
- Reusa ~90% de lo construido: pipeline de inferencia + clasificador de
  compliance + export ONNX (corre en CPU → cero costo de GPU en delivery).
- Es vendible como **servicio** (informe mensual / auditoría puntual) antes de
  tener producto: valida disposición a pagar con inversión mínima.
- Genera el activo más valioso para el roadmap: **video real de sitios
  mineros** para fine-tuning (con consentimiento contractual — el "data
  flywheel" del roadmap técnico §4).
- El gap actual es solo el modelo (F0) + una capa de reporting (~2 semanas
  est. sobre `nb06` + `ppe_classifier`).

**Spec draft creado:** `specs/006-batch-compliance-report/spec.md`.

### 6.2 Quick-wins de deuda técnica ofrecibles como servicio complementario

Priorizados por (valor comercial / esfuerzo estimado):

| # | Quick-win | Esfuerzo est. | Valor |
|---|---|---|---|
| 1 | **Entrenamiento GPU a mAP real** (bloquea todo; el entorno ya quedó listo para correrlo sin edits) | días (1 corrida + eval) | Habilita demo y cualquier venta |
| 2 | **Triage de los 643 labels faltantes** (script de matching contra `datasets/raw/`) | ~1 semana | Sube recall gratis; además es *productizable*: "auditoría de calidad de datasets" como servicio a terceros que entrenan sus propios modelos |
| 3 | **Reporte batch de compliance (el MVP mismo)** | ~2 semanas | Primer entregable facturable |
| 4 | **Auditoría de licencias de los datasets Roboflow** | días | Riesgo legal: sin esto no se puede comercializar nada entrenado sobre ese corpus |
| 5 | **Benchmark serving ONNX/TensorRT documentado** | ~1 semana | Define costo por cámara → input directo del pricing |
| 6 | Unificar versión de Python + cerrar numeración de specs | días | Higiene; desbloquea onboarding de colaboradores |

---

## 7. Material para la reunión de board

### 7.1 Agenda propuesta (90 min)

1. **Estado real vs. propuesta** (15') — §2 de este reporte. Aceptar la foto honesta.
2. **Mercado y posicionamiento** (10') — §4.1. ¿Acordamos el nicho (LATAM, compliance-first, precio de entrada bajo)?
3. **Horizonte técnico** (15') — §4.2–4.3. Validar las apuestas por capa (YOLOv11, BoT-SORT, TensorRT, DVC/MLflow) y sus gates de adopción.
4. **Decisión de MVP** (15') — §6. Go/no-go al MVP de auditoría batch.
5. **Roadmap y capacidad** (15') — §5. ¿Cuántas horas/semana reales aporta cada colaborador? Fechas se fijan *después* de esa respuesta.
6. **Riesgos y mitigaciones** (10') — §7.3.
7. **Acuerdos y owners** (10') — cada decisión con nombre y fecha de revisión.

### 7.2 Decisiones que el board debe tomar (no técnicas — nadie más puede tomarlas)

| # | Decisión | Opciones / recomendación |
|---|---|---|
| D1 | **Go/no-go MVP batch** | Recomendado: GO — es el camino de menor inversión a primera facturación |
| D2 | **Capacidad comprometida** | Horas/semana por colaborador + quién corre el training GPU esta semana |
| D3 | **Segmento y geografía inicial** | Recomendado: minería/construcción LATAM, 1–2 prospectos cálidos si existen |
| D4 | **Postura de pricing** | Referencia de mercado: USD 15–50k/año (tier Protex/Visionify) [F12][F13]; para auditoría batch, precio por informe/mes como entrada |
| D5 | **Claim de seguridad** | Recomendado: venderse como *compliance & monitoring*, NO como sistema anti-colisión certificado (implicancia legal, §4.1) |
| D6 | **Datos de clientes para fine-tuning** | Definir cláusula contractual estándar (consentimiento, retención, anonimización) |
| D7 | **Estructura** | ¿Portfolio profesional → producto comercial implica constituir algo? (societario/IP — fuera del alcance técnico, pero hay que agendarlo) |

### 7.3 Riesgos principales

| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| El modelo no llega a mAP demo-able con el corpus actual | Media | Alto | F0 lo mide en días; plan B: fine-tune desde pesos SH17/YOLOv11, reducir clases (roadmap §5.1) |
| **Licencias de datasets Roboflow no permiten uso comercial** | Media | Crítico | Quick-win #4 *antes* de vender nada; plan B: re-sourcing con datasets propios/licenciados |
| Capacidad part-time hace que el roadmap se estire | Alta | Medio | Fechas solo después de D2; gates por criterio, no por calendario |
| Competidores fondeados bajan precio / entran a LATAM | Media | Medio | Velocidad + nicho + servicio cercano; no competir en features enterprise |
| Privacidad/legal laboral por jurisdicción | Media | Alto | DPIA por despliegue; anonimización por defecto; asesoría legal antes del primer piloto [F15] |
| Bus factor (conocimiento concentrado) | Alta | Medio | La gobernanza existente (specs, constitution, notebooks generados) ya mitiga; mantenerla obligatoria |

### 7.4 Próximos pasos inmediatos propuestos (esta semana, si el board acuerda)

1. Correr el **entrenamiento GPU completo** (quien tenga la desktop CUDA — el
   notebook 03 ya auto-configura; cero edits necesarios).
2. **Auditar licencias** de las 5 fuentes Roboflow del corpus.
3. Revisar y aprobar (o corregir) los **specs draft 005 y 006**.
4. Fijar fecha de board con este reporte como pre-read.

---

## 8. Specs draft creados a partir de este reporte

Según el workflow del proyecto (CLAUDE.md — modo research), se dejaron en
estado `draft`, sin implementación:

- **`specs/005-model-training-validation/spec.md`** — entrenamiento GPU a
  calidad objetivo, triage de labels, evaluación honesta por clase (cierra el
  gate de F0).
- **`specs/006-batch-compliance-report/spec.md`** — el MVP de auditoría de
  cumplimiento EPP sobre video grabado (F1).

---

## 9. Fuentes

**Técnicas — PPE / detección:**
- [F1] [SH17: A Dataset for Human Safety and PPE Detection in Manufacturing Industry (arXiv 2407.04590)](https://arxiv.org/html/2407.04590v1)
- [F2] [SH17 dataset — GitHub](https://github.com/ahmadmughees/SH17dataset)
- [F3] [Scale-Dependent Performance Analysis of YOLO26 and YOLOv11 for PPE Detection (Electronics, 2026)](https://www.mdpi.com/2079-9292/15/6/1146)
- [F4] [SH17 (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S266644962400077X)

**Tracking / proximidad:**
- [F5] [ByteTrack (arXiv 2110.06864)](https://arxiv.org/abs/2110.06864)
- [F6] [BoT-SORT (arXiv 2206.14651)](https://arxiv.org/abs/2206.14651) · [Trackers en producción 2026 (Forasoft)](https://www.forasoft.com/learn/ai-for-video-engineering/articles-ai/multi-object-tracking-deepsort-bytetrack-ocsort)
- [F7] [What 'AI in mining' actually looks like in 2026 (Mining Technology)](https://www.mining-technology.com/sponsored/from-camera-clarity-to-collision-avoidance-what-ai-in-mining-actually-looks-like-in-2026/)
- [F8] [Sandvik/Newtrax — Proximity detection & collision avoidance](https://www.mining.sandvik/en/digital-solutions/safety-and-environment/proximity-detection-and-collision-avoidance/) · [Review CV anti-collision underground mines (Sensors)](https://www.mdpi.com/1424-8220/23/9/4294)

**Edge / serving:**
- [F9] [YOLOv8 benchmarks on NVIDIA Jetson (Seeed Studio)](https://www.seeedstudio.com/blog/2023/03/30/yolov8-performance-benchmarks-on-nvidia-jetson-devices/)
- [F10] [Benchmarking YOLOv8 on Jetson Orin NX (MDPI Computers)](https://www.mdpi.com/2073-431X/15/2/74)
- [F11] [YOLOv8 + TensorRT FP16/INT8 real-time (GitHub)](https://github.com/the0807/YOLOv8-ONNX-TensorRT) · [Energy efficiency YOLOv8/RT-DETR on edge (Sci. Reports)](https://www.nature.com/articles/s41598-026-46453-6)

**Mercado / competidores:**
- [F12] [The Safety Computer Vision Market Report (Protex AI)](https://www.protex.ai/the-safety-computer-vision-market-report) · [Intenseye vs Protex AI vs Spot AI (Voxel)](https://www.voxelai.com/industry-insights/intenseye-vs-protex-ai-vs-spot-ai)
- [F13] [Alternativas y pricing 2026 (Observia)](https://observia.ai/blog/cheap-alternatives-to-intenseye-best-standouts-for-ai-workplace-safety-softwares-in-2026/)
- [F14] [Protex AI — PitchBook profile](https://pitchbook.com/profiles/company/481588-75)

**Privacidad / regulación:**
- [F15] [Video surveillance under GDPR (Data Privacy Manager)](https://dataprivacymanager.net/video-surveillance-cctv-under-gdpr/) · [GDPR-compliant video anonymisation in OHS (Gallio)](https://gallio.pro/blog/gdpr-video-anonymisation-occupational-health-safety/) · [GDPR employee monitoring (GDPR Local)](https://gdprlocal.com/gdpr-employee-monitoring/)

**Internas:**
- `docs/SmartMine_Vision_AI_Project_Proposal.md` (visión comercial — Principio II: metas, no contrato)
- `docs/research/production_roadmap.ipynb` (detalle técnico por brecha)
- `docs/research/smartmine_validation_report.json` (estado del corpus, 2026-06-30)
- `specs/001`, `specs/002`, `docs/specs/SPEC-003/004` (estado implementado verificado)
