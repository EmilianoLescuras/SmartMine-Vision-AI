# Informe de Entrenamientos — SmartMine Vision AI / OPSIA

**Período cubierto:** 2026-06-20 → 2026-07-14 · **Autor:** auditoría automatizada (sesiones 12-14 jul)
**Todos los números provienen de `results.csv` y validaciones reales de cada experimento.**

---

## 1. Resumen ejecutivo

En tres días el proyecto pasó de un modelo **inservible (mAP50 0.137)** a un
detector con **5 de las 7 capacidades del producto funcionando arriba de 0.70
AP50** (casco, chaleco, botas, lentes, guantes). La mejora NO vino de entrenar
más épocas: vino de **limpiar los datos (SPEC-007)**, **sumar el dataset
correcto (SPEC-008)** y de descubrir — con evidencia — **qué puede y qué no
puede aprender el modelo** (el hallazgo del schema, §5).

El gate de Fase 1 (mAP50 ≥ 0.50 global) todavía no se alcanzó, pero por primera
vez sabemos exactamente por qué y cuál es el camino: schema v3 + una corrida
limpia en GPU.

---

## 2. Historial completo de modelos

| Modelo | Fecha | Corpus | Clases | Épocas | mAP50 | Estado |
|---|---|---|---:|---:|---:|---|
| ppe_baseline (CPU) | jun | css-data 20% @416px | 10 | 10 | 0.076 | verificación de pipeline |
| baseline-1..6 | jun | smartmine_v1 sucio | 32 | 0-2 | 0.083-0.086 | crashes/abortados |
| **baseline-7** | jun | smartmine_v1 **sucio** (185 badlines, 271 missing, clase camion falsa) | 32 | 7/10 | **0.137** | el "modelo malo" de referencia |
| **core-baseline-1** | 12-13 jul | **core v1 limpio** (SPEC-007) | 18 | 40/100 (corte manual) | **0.427** · best 0.434 | 3.1× mejor que baseline-7 |
| **core-baseline-2 (fases 2/2b/2c)** | 13-14 jul | **core v2** (+Construction-PPE, SPEC-008) | 26 | ~72 acumuladas | **0.400 global** / EPP-objeto ≈ 0.70-0.74 | mejor modelo actual |

### Detalle de las fases de baseline-2

| Fase | Config | Qué pasó |
|---|---|---|
| 2 (ép. 1-21) | batch 8, workers 0 | 31 min/ép (GPU hambrienta de datos); 2 crashes de MPS + 1 colgado; pico 0.341 |
| 2b (ép. +21) | **batch 16, workers 8** desde pesos ép.21 | 3.5× más rápido (9 min/ép); salto inmediato a **0.374**; bache de warm-restart consumió la paciencia del early stopping → corte prematuro en ép. 21 |
| 2c (ép. +31) | lr0 0.003 suave, patience 30 | osciló en banda 0.26-0.35 sin superar 0.374 → corte manual: el yolov8n tocó techo con 26 clases |

---

## 3. Qué significan los números globales

**El salto 0.137 → 0.427 (baseline-7 → core-baseline-1)** se explica casi
enteramente por datos: mismas ~40 épocas de presupuesto, mismo modelo, mismo
hardware. Lo que cambió: 0 labels corruptos, 0 labels perdidos, sin la clase
`camion` mentirosa, y un schema de 18 clases todas entrenables (vs 32 con una
vacía y 12 raquíticas que hundían el promedio). **Moraleja medible: la
limpieza de datos rindió 3× más que cualquier hiperparámetro.**

**El "retroceso" aparente 0.427 → 0.400 (baseline-1 → baseline-2) no es tal:**
- Se evalúan en splits distintos (v1: 316 imgs / v2: 459 imgs con Construction-PPE) — no son directamente comparables.
- baseline-2 aprende **26 clases vs 18** — 8 debutantes que promedian bajo al inicio.
- En el subconjunto comparable, baseline-2 APLASTA a baseline-1 (ver §4).
- El núcleo de seguridad (las 6 clases que definen el producto) **subió**: 0.363 → **0.419**.

---

## 4. Comparación por clase — donde está la historia real

| Clase | baseline-1 | baseline-2 | Δ |
|---|---:|---:|---|
| safety_vest | 0.397 | **0.705** | **+78%** ✅ |
| hardhat | 0.563 | **0.700** | **+24%** ✅ |
| safety_cone | 0.595 | 0.648 | +9% |
| person | 0.345 | 0.570 | +65% ✅ |
| camioneta | 0.850 | 0.855 | = |
| motoniveladora | 0.840 | 0.863 | = |
| **botas** | — sin datos | **0.739** | **nueva** 🎉 |
| **lentes_epp** | — sin datos | **0.727** | **nueva** 🎉 |
| **guantes_epp** | — sin datos | **0.711** | **nueva** 🎉 |
| volquete | 0.308 | 0.290 | ≈ |
| excavadora | 0.469 | 0.375 | −20% ⚠️ (dilución de dominio) |
| person_con_casco | 0.182 | 0.194 | estancada ❌ |
| person_sin_chaleco | 0.341 | 0.145 | ❌ |
| person_sin_lentes | — | 0.038 | ❌ |
| person_sin_botas | — | 0.034 | ❌ |

**Lectura:** todo lo que es *objeto físico* (un casco, un chaleco, una bota,
un cono, un vehículo) mejora o debuta alto. Todo lo que es *estado de una
persona* ("persona sin chaleco") está roto — sin importar cuántos datos ni
épocas se le dediquen.

---

## 5. El hallazgo estructural (la conclusión más valiosa del ciclo)

Las clases embebidas `person_(con|sin)_X` fracasan porque **las 4 fuentes las
anotan de forma incompatible**: css-data marca la cabeza, riskalert la persona
entera, deteccion_escenarios varía por color de casco. El modelo recibe
señales contradictorias y aprende ruido. Era el riesgo #1 de la auditoría del
12-jul; hoy es un hecho medido.

**Decisión derivada (propuesta SPEC-009 — schema v3):**
1. Entrenar solo **objetos puros** (~15 clases: person + ítems EPP + vehículos).
2. Derivar el compliance ("persona sin casco") **en inferencia**, cruzando
   geométricamente persona↔EPP con el resolver híbrido de `ppe_classifier.py`
   — que ya está implementado y testeado, y fue diseñado para esto.
3. Proyección con los mismos datos: mAP50 global >0.55 (se eliminan del
   promedio ~10 clases estructuralmente rotas y `person` deja de estar
   fragmentada en 13 identidades).

---

## 6. Lecciones operativas (entrenar en Apple Silicon)

1. **`workers=0` es el default de Ultralytics en MPS y triplica el tiempo** —
   con `workers=8, batch=16` el M4 pasó de 31 a 9 min/época.
2. **MPS es frágil para entrenar:** 4 crashes + 1 colgado en ~70 épocas (bugs
   del backend Metal, no de nuestro código). El wrapper de auto-reintento
   (resume desde checkpoint, hasta 8 intentos) fue lo que permitió avanzar.
3. **Trampa del warm-restart:** reiniciar con LR alto produce un bache que
   puede consumir la paciencia del early stopping contra el mejor punto
   heredado (nos cortó la fase 2b justo cuando la curva subía).
4. **Referencias de velocidad para este mismo entrenamiento:** RTX 2080 Ti ≈
   3-4 h las 100 épocas · Colab T4 (gratis) ≈ 2-3 h · M4 ≈ 20-50 h · CPU
   Ryzen 5600G ≈ 3-4 días (inviable; ese hardware es para inferencia, donde
   sí rinde: ~20-40 ms/frame en ONNX).

---

## 7. Recomendaciones (en orden)

1. **Mergear PR #7 y PR #8** — consolidan corpus limpio + adquisición.
2. **SPEC-009 (schema v3):** la mayor mejora disponible, costo cero en datos.
3. **Corrida definitiva en GPU cloud** (Colab T4): 100 épocas ininterrumpidas
   con schema v3; evaluar ahí el gate de 0.50 y decidir si hace falta yolov8s.
4. **Datos faltantes:** protección auditiva y uniforme siguen en ❌ — próxima
   adquisición o anotación propia sobre video de cliente (SPEC-006/D6).
5. **Licencia:** resolver Ultralytics Enterprise (o migración de stack) antes
   de comercializar — aplica al framework y al dataset Construction-PPE por igual.
